# Setup script for OleFileIO_PL - Philippe Lagadec

# History:
# 2007-09-13 v0.01 PL: - first version
# 2007-11-10 v0.02 PL: - updated website URL
# 2007-12-04 v0.03 PL: - updated description, added debug_mode test
# 2009-09-11 v0.04 PL: - updated URL, e-mail, licence, disabled e-mail
# 2012-02-16 v0.05 PL: - added download URL on bitbucket
# 2012-09-11 v0.06 PL: - read long description from disk in rst format
# 2014-02-04 v0.07 PL: - added PyPI classifier for Python 3.x, added PL2 version

import distutils.core
import sys

from OleFileIO_PL import __version__, __author__, DEBUG_MODE

# debug mode should be off for usual releases:
if DEBUG_MODE:
    raise ValueError("WARNING: DEBUG_MODE should be False !")

modules = ['OleFileIO_PL']
if sys.version_info < (3,):
    modules.append('OleFileIO_PL2')

kw = {
    'name': "OleFileIO_PL",
    'version': __version__,
    'description': "A Python module to parse and read Microsoft OLE2 files (Structured Storage or Compound Document, Microsoft Office) - Improved version of the OleFileIO module from PIL, the Python Image Library.",
    # read long description from disk in restructuredtext format:
    'long_description': open('README.txt').read(),
    'author': __author__,
    #'author_email': "decalage(a)laposte.net",
    'url': "http://www.decalage.info/python/olefileio",
    'license': "updated PIL license (see source code or LICENCE.txt)",
    'py_modules': modules,
    }


# If we're running Python 2.3, add extra information
if hasattr(distutils.core, 'setup_keywords'):
    if 'classifiers' in distutils.core.setup_keywords:
        kw['classifiers'] = [
            'Development Status :: 4 - Beta',
            'License :: OSI Approved', #'License :: PIL license (see source code)',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules'
          ]
    if 'download_url' in distutils.core.setup_keywords:
        kw['download_url'] = "https://bitbucket.org/decalage/olefileio_pl/downloads"

distutils.core.setup(**kw)
