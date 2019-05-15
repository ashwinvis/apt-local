#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Top-level package for apt-local."""

__author__ = """Ashwin Vishnu Mohanan"""
__email__ = 'ashwinvis@protonmail.com'
__version__ = '0.0.2b0'

import subprocess
import argparse
import os

from . import system
from .pacman import PackageManager


def init_pacman():
    # TODO: read configuration
    # TODO: load from a pickled package manager instance.
    return PackageManager(system.Debian)


pacman = init_pacman()


def init_parser():
    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the "install" command, etc.
    parser_install = subparsers.add_parser("install")
    parser_install.add_argument("pkg", nargs="+")
    parser_install.set_defaults(func=pacman.install)

    parser_uninstall = subparsers.add_parser("uninstall")
    parser_uninstall.add_argument("pkg", nargs="+")
    parser_uninstall.set_defaults(func=pacman.uninstall)

    parser_list = subparsers.add_parser("list")
    parser_list.set_defaults(func=pacman.list)

    parser_set_path = subparsers.add_parser("search")
    parser_set_path.add_argument("pkg", nargs="+")
    parser_set_path.set_defaults(func=pacman.search)

    parser_set_path = subparsers.add_parser("set-path")
    parser_set_path.add_argument("path")
    parser_set_path.set_defaults(func=pacman.set_path)

    parser_show_path = subparsers.add_parser("show-path")
    parser_show_path.set_defaults(func=pacman.show_path)

    return parser


def main():
    curdir = os.getcwd()
    parser = init_parser()
    try:
        args = parser.parse_args()
        args.func(args)
    finally:
        os.chdir(curdir)


if __name__ == "__main__":
    main()
