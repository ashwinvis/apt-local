apt-local
=========

[![image](https://img.shields.io/pypi/v/apt_local.svg)](https://pypi.python.org/pypi/apt_local)
[![image](https://img.shields.io/travis/ashwinvis/apt-local.svg)](https://travis-ci.org/ashwinvis/apt-local)
[![Documentation
Status](https://readthedocs.org/projects/apt-local/badge/?version=latest)](https://apt-local.readthedocs.io/en/latest/?badge=latest)

Simple symlink-based package manager for local installations (without sudo)

* Free software: GNU General Public License v3

* Documentation: https://apt-local.readthedocs.io.

# Features

Meant for Debian-based distributions: such as Debian / Ubuntu /
Linux Mint and so on.

This package is born out of the frustration of a typical grad student
who has no admin-rights over the machine, and has to rely on the
system-admin over and over for installation of that "X" package.

## Requirements

  - Debian-based OS or atleast `dpkg`, `apt-get` and `apt-cache`
    installed
  - GNU Stow: [HTTP](https://ftp.gnu.org/gnu/stow/) |
    [FTP](ftp://ftp.gnu.org/gnu/stow/) |
    [Git](https://savannah.gnu.org/git/?group=stow) |
    [CPAN](https://metacpan.org/pod/distribution/Stow/bin/stow)

If Stow is not available in the system you may use [this
script](https://gist.github.com/ashwinvis/a533c210d1ba788479a3724558e4d873)
to install it.

<div class="warning">
<div class="admonition-title">
Warning
</div>

This is an experimental project, and often results in hit-or-miss
situation. The advantages with apt-local is a lightweight installation
and installing packages requires no compilation. If you want a more
robust package manager use one of the following:

  - NixOS/nix
  - conda/conda
  - fsquillace/junest
  - bpkg/bpkg

</div>

## Quick start

Install the package using **either** of the following commands

``` bash
python setup.py install --user  # with the source code
pip install apt-local --user  # without the source code
```

To get started choose a local directory where you would like the package
to be installed. For example `~/.local` or
`<path-to-scratch-directory>/.local` and a directory called `apt-cache`
(name can be anything) **under it** (very important\!). This can simply
be done as:

``` bash
apt-local set-path ~/.local/apt-cache
apt-local show-path
```

Installing a `.deb` package is made as simple as:

``` bash
usage: apt-local install [-h] pkg

positional arguments:
  pkg
```

For example `apt-local install wget`.

## Usage

The subcommands serve self-explanatory purposes. The subcommands
`set-path` and `show-path` are used to configure path and display the
configured path respectively.

``` bash
usage: apt-local [-h] {install,uninstall,list,set-path,show-path} ...

positional arguments:
  {install,uninstall,list,set-path,show-path}

optional arguments:
  -h, --help            show this help message and exit
```

Make your installation useable by setting up environment variables such
as `PATH`, `LD_LIBRARY_PATH`, `CPATH` etc. in the `~/.profile` or
`~/.bashrc`. The following snippet can be adapted:

``` bash
export PATH=$PATH:$HOME/.local/bin
export CPATH=$CPATH:$HOME/.local/include
export LIBRARY_PATH=$LIBRARY_PATH:$HOME/.local/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/.local/lib
```

# Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[ashwinvis/cookiecutter-pypackage](https://github.com/ashwinvis/cookiecutter-pypackage)
project template.
