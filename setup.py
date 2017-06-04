"""
Installation script for olefile using distutils

To install this package, run:
    python setup.py install

(setup script partly borrowed from cherrypy)
"""

#--- CHANGELOG ----------------------------------------------------------------

# 2007-09-13 v0.01 PL: - first version
# 2007-11-10 v0.02 PL: - updated website URL
# 2007-12-04 v0.03 PL: - updated description, added debug_mode test
# 2009-09-11 v0.04 PL: - updated URL, e-mail, licence, disabled e-mail
# 2012-02-16 v0.05 PL: - added download URL on bitbucket
# 2012-09-11 v0.06 PL: - read long description from disk in rst format
# 2014-02-04 v0.07 PL: - added PyPI classifier for Python 3.x, added PL2 version
# 2014-09-26 v0.08 PL: - install the olefile package instead of modules
# 2014-10-10 v0.09 PL: - fixed compilation error on Python 3
# 2016-01-29 v0.10 PL: - fixed issue #28, removed DEBUG_MODE test
# 2016-01-05 v0.44 PL: - removed the legacy doc subfolder


#--- TODO ---------------------------------------------------------------------


#--- IMPORTS ------------------------------------------------------------------

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys, os, fnmatch

from olefile import __version__, __author__


#--- METADATA -----------------------------------------------------------------

name         = "olefile"
version      = __version__
desc         = "Python package to parse, read and write Microsoft OLE2 files (Structured Storage or Compound Document, Microsoft Office) - Improved version of the OleFileIO module from PIL, the Python Image Library."
# read long description from disk in restructuredtext format:
long_desc    = open('olefile/README.rst').read()
author       = __author__
author_email = "https://www.decalage.info/contact"
url          = "https://www.decalage.info/python/olefileio"
license      = "BSD"
download_url = "https://github.com/decalage2/olefile/tarball/master"

classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Science/Research",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules"
]

#--- PACKAGES -----------------------------------------------------------------

packages=[
    "olefile",
]

modules = ['OleFileIO_PL']

##setupdir = '.'
##package_dir={'': setupdir}

#--- PACKAGE DATA -------------------------------------------------------------

## Often, additional files need to be installed into a package. These files are
## often data that?s closely related to the package?s implementation, or text
## files containing documentation that might be of interest to programmers using
## the package. These files are called package data.
##
## Package data can be added to packages using the package_data keyword argument
## to the setup() function. The value must be a mapping from package name to a
## list of relative path names that should be copied into the package. The paths
## are interpreted as relative to the directory containing the package
## (information from the package_dir mapping is used if appropriate); that is,
## the files are expected to be part of the package in the source directories.
## They may contain glob patterns as well.
##
## The path names may contain directory portions; any necessary directories will
## be created in the installation.


# the following functions are used to dynamically include package data without
# listing every file here:

def riglob(top, prefix='', pattern='*'):
    """
    recursive iterator glob
    - top: path to start searching from
    - prefix: path to use instead of top when generating file path (in order to
      choose the root of relative paths)
    - pattern: wildcards to select files (same syntax as fnmatch)

    Yields each file found in top and subdirectories, matching pattern
    """
    #print 'top=%s prefix=%s pat=%s' % (top, prefix, pattern)
    dirs = []
    for path in os.listdir(top):
        p = os.path.join(top, path)
        if os.path.isdir(p):
            dirs.append(path)
        elif os.path.isfile(p):
            #print ' - file:', path
            if fnmatch.fnmatch(path, pattern):
                yield os.path.join(prefix, path)
    #print ' dirs =', dirs
    for d in dirs:
        dtop = os.path.join(top, d)
        dprefix = os.path.join(prefix, d)
        #print 'dtop=%s dprefix=%s' % (dtop, dprefix)
        for p in riglob(dtop, dprefix, pattern):
            yield p

def rglob(top, prefix='', pattern='*'):
    """
    recursive glob
    Same as riglob, but returns a list.
    """
    return list(riglob(top, prefix, pattern))




package_data={
    'olefile': [
        'README.rst',
        'README.html',
        'LICENSE.txt',
        'CONTRIBUTORS.txt',
        # 'olefile.html',
        ]
        # doc folder: md, html, png
        # + rglob('olefile/doc', 'doc', '*.html')
        # + rglob('olefile/doc', 'doc', '*.md')
        # + rglob('olefile/doc', 'doc', '*.png'),
    }


#--- data files ---------------------------------------------------------------

# not used for now.

## The data_files option can be used to specify additional files needed by the
## module distribution: configuration files, message catalogs, data files,
## anything which doesn?t fit in the previous categories.
##
## data_files specifies a sequence of (directory, files) pairs in the following way:
##
## setup(...,
##       data_files=[('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
##                   ('config', ['cfg/data.cfg']),
##                   ('/etc/init.d', ['init-script'])]
##      )
##
## Note that you can specify the directory names where the data files will be
## installed, but you cannot rename the data files themselves.
##
## Each (directory, files) pair in the sequence specifies the installation
## directory and the files to install there. If directory is a relative path,
## it is interpreted relative to the installation prefix (Python?s sys.prefix for
## pure-Python packages, sys.exec_prefix for packages that contain extension
## modules). Each file name in files is interpreted relative to the setup.py
## script at the top of the package source distribution. No directory information
## from files is used to determine the final location of the installed file;
## only the name of the file is used.
##
## You can specify the data_files options as a simple sequence of files without
## specifying a target directory, but this is not recommended, and the install
## command will print a warning in this case. To install data files directly in
## the target directory, an empty string should be given as the directory.



##data_files=[
##    ('balbuzard', [
##        'balbuzard/README.txt',
##                  ]),
##]

##if sys.version_info >= (3, 0):
##    required_python_version = '3.0'
##    setupdir = 'py3'
##else:
##    required_python_version = '2.3'
##    setupdir = 'py2'

##data_files = [(install_dir, ['%s/%s' % (setupdir, f) for f in files])
##              for install_dir, files in data_files]


##def fix_data_files(data_files):
##    """
##    bdist_wininst seems to have a bug about where it installs data files.
##    I found a fix the django team used to work around the problem at
##    http://code.djangoproject.com/changeset/8313 .  This function
##    re-implements that solution.
##    Also see http://mail.python.org/pipermail/distutils-sig/2004-August/004134.html
##    for more info.
##    """
##    def fix_dest_path(path):
##        return '\\PURELIB\\%(path)s' % vars()
##
##    if not 'bdist_wininst' in sys.argv: return
##
##    data_files[:] = [
##        (fix_dest_path(path), files)
##        for path, files in data_files]
##fix_data_files(data_files)


#--- SCRIPTS ------------------------------------------------------------------

# not used for now.

#scripts = ["%s/cherrypy/cherryd" % setupdir]


#=== MAIN =====================================================================

def main():
##    # set default location for "data_files" to
##    # platform specific "site-packages" location
##    for scheme in list(INSTALL_SCHEMES.values()):
##        scheme['data'] = scheme['purelib']

    dist = setup(
        name=name,
        version=version,
        description=desc,
        long_description=long_desc,
        classifiers=classifiers,
        author=author,
        author_email=author_email,
        url=url,
        license=license,
##        package_dir=package_dir,
        packages=packages,
        package_data = package_data,
        py_modules = modules,
        download_url=download_url,
#        data_files=data_files,
#        scripts=scripts,
    )


if __name__ == "__main__":
    main()
