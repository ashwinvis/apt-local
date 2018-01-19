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


def run(cmds):
    cmds = cmds.split('|')
    stdin = None
    for cmd in cmds[:-1]:
        cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE)
        stdin = proc.stdout

    cmd = shlex.split(cmds[-1])
    return subprocess.check_output(cmd, stdin=stdin)


class System(object):
    def stow(self, pkg):
        return run('stow -v ' + pkg)

    def unstow(self, pkg):
        return run('stow -D -v ' + pkg)


class Debian(System):
    def list_installed(self):
        return run('dpkg -l | grep ii')

    def depends(self, pkg):
        deps = run("apt-cache depends " + pkg + "| grep -e ' *Depends'").split()
        deps = [line.split(b':')[-1] for line in deps]
        deps = list(filter(b''.__ne__, deps))
        return deps

    def download_and_extract(self, pkg):
        dest = '/tmp/apt-local'
        cwd = os.getcwd()
        os.makedirs(dest, exist_ok=True)
        os.chdir(dest)
        run('apt-get download ' + pkg)
        deb = glob(pkg + '*.deb')[0]
        run('dpkg -X ' + deb + ' ' + pkg)
        os.chdir(cwd)
        os.makedirs(os.path.join(cwd, pkg, 'bin'), exist_ok=True)
        try:
            shutil.move(os.path.join(dest, pkg, 'usr'), os.path.join(cwd, pkg))
        except FileNotFoundError:
            print('No directory like {}/{}/{}'.format(dest, pkg, 'usr'))

        try:
            shutil.move(os.path.join(dest, pkg, 'bin'), os.path.join(cwd, pkg, 'bin'))
        except FileNotFoundError:
            print('No directory like {}/{}/{}'.format(dest, pkg, 'bin'))
