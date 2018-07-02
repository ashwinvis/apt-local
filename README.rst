apt-local
=========

Simple symlink-based package manager for local installations (without sudo).
Meant for Debian-based distributions: such as Debian / Ubuntu / Linux Mint and
so on.

This package is born out of the frustration of a typical grad student who has
no admin-rights over the machine, and has to rely on the system-admin over and
over for installation of that "X" package.

Requirements
------------

-  Debian-based OS or atleast ``dpkg``, ``apt-get`` and ``apt-cache`` installed
-  GNU Stow: `HTTP <https://ftp.gnu.org/gnu/stow/>`__ \|
   `FTP <ftp://ftp.gnu.org/gnu/stow/>`__ \|
   `Git <https://savannah.gnu.org/git/?group=stow>`__ \|
   `CPAN <https://metacpan.org/pod/distribution/Stow/bin/stow>`__

If Stow is not available in the system you may use `this
script <https://gist.github.com/ashwinvis/a533c210d1ba788479a3724558e4d873>`__
to install it.

.. warning::

   This is an experimental project, and often results in hit-or-miss situation.
   The advantages with apt-local is a lightweight installation and installing
   packages requires no compilation. If you want a more robust package manager
   use one of the following:

   - NixOS/nix
   - conda/conda
   - fsquillace/junest
   - bpkg/bpkg

Quick start
-----------

Install the package using **either** of the following commands

.. code:: bash

    python setup.py install --user  # with the source code
    pip install apt-local --user  # without the source code

To get started choose a local directory where you would like the package to be
installed. For example ``~/.local`` or ``<path-to-scratch-directory>/.local``
and a directory called ``apt-cache`` (name can be anything) **under it** (very
important!).  This can simply be done as:

.. code:: bash

    apt-local set-path ~/.local/apt-cache
    apt-local show-path

Installing a ``.deb`` package is made as simple as:

.. code:: bash

    usage: apt-local install [-h] pkg

    positional arguments:
      pkg

For example ``apt-local install wget``.

Usage
-----

The subcommands serve self-explanatory purposes. The subcommands ``set-path``
and ``show-path`` are used to configure path and display the configured path
respectively.

.. code:: bash

   usage: apt-local [-h] {install,uninstall,list,set-path,show-path} ...

   positional arguments:
     {install,uninstall,list,set-path,show-path}

   optional arguments:
     -h, --help            show this help message and exit


Make your installation useable by setting up environment variables such as
``PATH``, ``LD_LIBRARY_PATH``, ``CPATH`` etc. in the ``~/.profile`` or
``~/.bashrc``. The following snippet can be adapted:

.. code:: bash

    export PATH=$PATH:$HOME/.local/bin
    export CPATH=$CPATH:$HOME/.local/include
    export LIBRARY_PATH=$LIBRARY_PATH:$HOME/.local/lib
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/.local/lib
