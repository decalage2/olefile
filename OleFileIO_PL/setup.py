# Setup script for OleFileIO_PL - Philippe Lagadec

# History:
# 2007-09-13 v0.01 PL: - first version
# 2007-11-10 v0.02 PL: - updated website URL
# 2007-12-04 v0.03 PL: - updated description, added debug_mode test
# 2009-09-11 v0.04 PL: - updated URL, e-mail, licence, disabled e-mail

import distutils.core

from OleFileIO_PL import __version__, __author__, DEBUG_MODE

# debug mode should be off for usual releases:
if DEBUG_MODE:
    raise ValueError, "WARNING: DEBUG_MODE should be False !"

kw = {
    'name': "OleFileIO_PL",
    'version': __version__,
    'description': "A Python module to parse and read Microsoft OLE2 files (Structured Storage or Compound Document, Microsoft Office) - Improved version of the OleFileIO module from PIL, the Python Image Library.",
    'author': __author__,
    #'author_email': "decalage(a)laposte.net",
    'url': "http://www.decalage.info/python/olefileio",
    'license': "updated PIL license (see source code or LICENCE.txt)",
    'py_modules': ['OleFileIO_PL'],
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
            'Topic :: Software Development :: Libraries :: Python Modules'
          ]
    if 'download_url' in distutils.core.setup_keywords:
        kw['download_url'] = "http://www.decalage.info/python/olefileio"

distutils.core.setup(**kw)
