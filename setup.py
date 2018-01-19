from setuptools import setup, find_packages
from runpy import run_path
import os


here = os.path.abspath(os.path.dirname(__file__))

__version__ = '0.0.1b'

# Get the long description from the relevant file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

lines = long_description.splitlines(True)
long_description = ''.join(lines)

# Get the development status from the version string
if 'a' in __version__:
    devstatus = 'Development Status :: 3 - Alpha'
elif 'b' in __version__:
    devstatus = 'Development Status :: 4 - Beta'
else:
    devstatus = 'Development Status :: 5 - Production/Stable'

setup(
    name="apt-local",
    version=__version__,
    packages=find_packages(exclude=[]),
    entry_points={
        'console_scripts':
        ['apt-local = apt_local.__init__:main',
         ]},
    author='Ashwin Vishnu Mohanan',
    author_email='avmo@kth.se',
    description=(
        'Simple symlink-based package manager for local installations '
        '(without sudo)'),
    long_description=long_description,
    license="GPLv3",
    keywords=['debian', 'ubuntu', 'apt-get', 'packaging'],
    url="http://github.com/ashwinvis/apt-local",
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        devstatus,
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Installation/Setup',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        # Specify the Python versions you support here. In particular,
        # ensure that you indicate whether you support Python 2,
        # Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'],
)
