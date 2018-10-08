"""Package Manager
==================
A generic package manager adaptable to another OS just by changing the
``__init__`` call. Also a tribute to famed ArchLinux package manager.

"""
import subprocess
import os
import shutil
from collections import OrderedDict
from configparser import ConfigParser
import sys
from .system import Debian


class PackageManager(object):
    def __init__(self, OS=None):
        self.oper = OS()
        self.envs = OrderedDict(
            zip(
                (
                    "PATH",
                    "LD_LIBRARY_PATH",
                    "LIBRARY_PATH",
                    "CPATH",
                    "XDG_DATA_DIRS",
                    "XDG_DATA_HOME",
                ),
                ("bin", "lib", "lib", "include", "share", "share"),
            )
        )

        self.ok_ans = ["y", "yes", "a", "all"]
        self.acceptable_ans = ["y", "yes", "n", "no", "a", "all", "q", "quit"]

        os.makedirs(os.path.expanduser("~/.config"), exist_ok=True)
        self.config_file = os.path.expanduser("~/.config/apt-local.conf")

    def ask(self, question, ans=""):
        while ans not in self.acceptable_ans:
            ans = input(
                "{} {} ".format(question, "([y]es/[n]o/yes to [a]ll/[q]uit):")
            ).lower()

        return ans

    def install(self, args):
        oper = self.oper
        config = self.read_config()
        os.chdir(config.get("default", "path"))

        for pkg in args.pkg:
            installed = oper.list_installed()
            deps = oper.depends(pkg)
            print("Dependencies:", *deps)

            to_download = [pkg]  # [pkg.encode('utf-8')]
            to_download.extend([d for d in deps if d not in installed])
            print("Packages to be installed:", *to_download)

            ans = ""
            for dep in to_download:
                ans = self.ask("{} {}".format("Install", dep, ans))

                if ans in ("q", "quit"):
                    sys.exit(0)

                if ans in self.ok_ans:
                    oper.download_and_extract(dep)
                    try:
                        oper.stow(pkg)
                    except subprocess.CalledProcessError:
                        print("Error while stowing")
                        pass

                if ans != "a" or ans != "all":
                    ans = ""

    def uninstall(self, args):
        pkg = args.pkg
        oper = self.oper

        config = self.read_config()
        path = config.get("default", "path")
        os.chdir(path)
        dirs = os.listdir()

        ans = ""
        for pkg in args.pkg:
            if pkg not in dirs:
                raise FileNotFoundError("Cannot find the package " + pkg)

            ans = self.ask("{} {}".format("Uninstall", pkg), ans)

            if ans in self.ok_ans:
                oper.unstow(pkg)
                shutil.rmtree(pkg)

            if ans != "a" or ans != "all":
                ans = ""

    def search(self, args):
        for pkg in args.pkg:
            self.oper.search(pkg)

    def read_config(self):
        config = ConfigParser()
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(
                "Cannot find configuration file "
                + self.config_file
                + '. Have you tried "apt-local set-path"?'
            )

        config.read(self.config_file)
        return config

    def list(self, args):
        config = self.read_config()
        path = config.get("default", "path")

        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path, item)):
                print(item)

    def show_path(self, args):
        config = self.read_config()
        print("path =", config.get("default", "path"))

        print("environment variables:")
        for env in self.envs:
            print("{}={}".format(env, os.getenv(env)))

    def set_path(self, args):
        path = args.path

        config = ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)

        config["default"] = {"path": path}
        with open(self.config_file, "w") as configfile:
            config.write(configfile)

        print(
            "apt-local path is set as",
            path,
            "\nEnsure that you have the environment variables configured (for eg. in ~/.bashrc):\n",
        )

        for env, subdir in self.envs.items():
            print("export {0}=${0}:{1}{2}{3}".format(env, path, os.sep, subdir))
