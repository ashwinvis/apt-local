"""System tools
===============
Contains all functions with atleast one subprocess call. To be replaced in the
future with a suitable python API layer.

"""
import subprocess
import shlex
import os
import shutil
from glob import glob
from tempfile import gettempdir
from pathlib import Path


def run(cmds):
    cmds = cmds.split("|")
    stdin = None
    for cmd in cmds[:-1]:
        cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE)
        stdin = proc.stdout

    cmd = shlex.split(cmds[-1])
    return subprocess.check_output(cmd, stdin=stdin).decode("utf-8", "strict")


def mv(path_from, path_to):
    try:
        shutil.move(str(path_from), str(path_to))
    except shutil.Error:
        # Try to move directory contents
        if path_to.exists():
            for path_from_child in path_from.glob("*"):
                mv(path_from_child, path_to)
        else:
            raise
    except FileNotFoundError:
        print("No directory like {}".format(path_from))


class System(object):
    def stow(self, pkg):
        return run("stow -v " + pkg)

    def unstow(self, pkg):
        return run("stow -D -v " + pkg)


class Debian(System):
    def list_installed(self):
        return run("dpkg -l | grep ii")

    def depends(self, pkg):
        deps = run("apt-cache depends " + pkg + "| grep -e ' *Depends'").split()
        deps = [line.split(":")[-1] for line in deps]
        deps = set(filter("".__ne__, deps))
        return deps

    def search(self, pkg):
        pkgs = run("apt-cache search {0} | grep {0}".format(pkg))
        print(pkgs)

    def download_and_extract(self, pkg):
        dest = Path(gettempdir()) / "apt-local"
        cwd = Path.cwd()
        os.makedirs(str(dest), exist_ok=True)
        os.chdir(str(dest))

        run("apt-get download {}".format(pkg))
        deb = glob(pkg + "*.deb")[0]
        run("dpkg -X " + deb + " " + pkg)

        os.chdir(str(cwd))
        for path_from in (dest / pkg / "usr").glob("*"):
            mv(path_from, cwd / pkg)

        mv(dest / pkg / "bin", cwd / pkg)
