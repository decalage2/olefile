"""
Installation script for olefile using setuptools

To install this package, run:
    python setup.py install

"""


# --- IMPORTS -----------------------------------------------------------------

from setuptools import setup

from olefile import __version__, __author__


# --- METADATA ----------------------------------------------------------------

name         = "olefile"
version      = __version__
desc         = "Python package to parse, read and write Microsoft OLE2 files (Structured Storage or Compound Document, Microsoft Office)"
author       = __author__
author_email = "nospam@decalage.info"
url          = "https://www.decalage.info/python/olefileio"
license      = "BSD"
download_url = "https://github.com/decalage2/olefile/tarball/master"

with open('README.md') as f:
    long_desc = f.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Science/Research",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules"
]

# --- PACKAGES ----------------------------------------------------------------

packages = [
    "olefile",
]


# === MAIN ====================================================================

def main():
    setup(
        name=name,
        version=version,
        description=desc,
        long_description=long_desc,
        long_description_content_type='text/markdown',
        classifiers=classifiers,
        author=author,
        author_email=author_email,
        url=url,
        license=license,
#        package_dir=package_dir,
        packages=packages,
        download_url=download_url,
#        data_files=data_files,
#        scripts=scripts,
        python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    )


if __name__ == "__main__":
    main()
