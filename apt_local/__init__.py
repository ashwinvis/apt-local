#!/usr/bin/env python3
import subprocess
import shlex
import argparse
import os
import shutil
from glob import glob
import sys


def run(cmds):
    cmds = cmds.split('|')
    stdin = None
    for cmd in cmds[:-1]:
        cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE)
        stdin = proc.stdout

    cmd = shlex.split(cmds[-1])
    return subprocess.check_output(cmd, stdin=stdin)


def dpkgl():
    return run('dpkg -l | grep ii')


def depends(pkg):
    deps = run("apt-cache depends " + pkg + "| grep -e ' *Depends'").split()
    deps = [line.split(b':')[-1] for line in deps]
    deps = list(filter(b''.__ne__, deps))
    return deps


def download_and_extract(pkg):
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


def stow(pkg):
    return run('stow -v ' + pkg)


def install(args):
    pkg = args.pkg
    installed = dpkgl()
    deps = depends(pkg)
    print(deps)
    to_download = [pkg]
    to_download.extend([str(d) for d in deps if d not in installed])
    print(to_download)
    ans = ''
    ok_ans = ['y', 'yes', 'a', 'all']
    acceptable_ans = ['y', 'yes', 'n', 'no', 'a', 'all']
    for dep in to_download:
        while ans not in acceptable_ans:
            ans = input('Install ' + dep + '(y/n/a)').lower()

        if ans in ok_ans:
            download_and_extract(dep)
            try:
                stow(pkg)
            except subprocess.CalledProcessError:
                pass

            if ans != 'a' or ans != 'all':
                ans = ''


def main():
    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the "install" command
    parser_foo = subparsers.add_parser('install')
    parser_foo.add_argument('pkg')
    parser_foo.set_defaults(func=install)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
