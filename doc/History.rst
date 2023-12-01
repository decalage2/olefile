=======
History
=======

..
    old URLs that don't work anymore:
    http://svn.effbot.org/public/tags/pil-1.1.7/PIL/OleFileIO.py
    http://www.pythonware.com/products/pil/index.htm

olefile is based on the `OleFileIO module <https://github.com/python-pillow/Pillow/blob/f05f8001c556a25d409b03aa50e967c11008dfba/PIL/OleFileIO.py>`__
from `PIL <https://fr.wikipedia.org/wiki/Python_Imaging_Library>`__ v1.1.7, the
excellent Python Imaging Library, created and maintained by Fredrik
Lundh. The olefile API is still compatible with PIL, but since 2005 I
have improved the internal implementation significantly, with new
features, bugfixes and a more robust design.

From 2005 to 2014 the
project was called **OleFileIO\_PL**, and in 2014 I changed its name to
**olefile** to celebrate its 9 years and its new write features.

As far as I know, this module is the most complete and robust Python
implementation to read MS OLE2 files, portable on several operating
systems. (please tell me if you know other similar Python modules)

Since 2014 olefile/OleFileIO\_PL has been integrated into
`Pillow <https://python-pillow.org/>`__, the friendly fork of PIL.

In January 2017, it was decided to remove olefile from Pillow 4.0.0 and
to install it as an external dependency. This will avoid issues
due to the maintenance of the olefile code in two repositories.

Main improvements over the original version of OleFileIO in PIL:
----------------------------------------------------------------

-  Compatible with Python 3.5+ and 2.7
-  Many bug fixes
-  Support for files larger than 6.8MB
-  Support for 64 bits platforms and big-endian CPUs
-  Robust: many checks to detect malformed files
-  Runtime option to choose if malformed files should be parsed or raise
   exceptions
-  Improved API
-  Metadata extraction, stream/storage timestamps (e.g. for document
   forensics)
-  Can open file-like objects
-  Added setup.py and install.bat to ease installation
-  More convenient slash-based syntax for stream paths
-  Write features

Detailed History
----------------

See the `full changelog <https://github.com/decalage2/olefile/blob/master/CHANGELOG.md>`__ for more details.

- **2023-11-30 v0.47 (in development)**:
    - fixed issue #142: isOleFile has a new data parameter to handle files in memory properly
    - fixed issue #156: write_sect now correctly detects when data is larger than the sector size
    - use GitHub actions for testing and Codecov for coverage, added python 3.8 to 3.12 (PR #157 by @hugovk)
    - added VT_VECTOR support for properties (PR #135 by Maciej Kotowicz @mak)
    - olefile is now distributed as a universal wheel package in PyPI (PR #130 by @hugovk)
    - olefile will not close a file handle if it was provided by the caller
      (PR #121 by Christian Herdtweck, issue #120)
    - added exceptions OleFileError and NotOleFileError to replace IOError (PR #110 by Ken Peterson @TheElementalOfCreation)
    - added get_userdefined_properties to parse user-defined properties (PR #114 by @DissectMalware)
-  **2018-09-09 v0.46**: OleFileIO can now be used as a context manager
   (with...as), to close the file automatically (see
   `doc <https://olefile.readthedocs.io/en/latest/Howto.html#open-an-ole-file-from-disk>`__).
   Improved handling of malformed files, fixed several bugs.
-  2018-01-24 v0.45: olefile can now overwrite streams of any size,
   improved handling of malformed files, fixed several
   `bugs <https://github.com/decalage2/olefile/milestone/4?closed=1>`__,
   end of support for Python 2.6 and 3.3.
-  2017-01-06 v0.44: several bugfixes, removed support for Python
   2.5 (olefile2), added support for incomplete streams and incorrect
   directory entries (to read malformed documents), added getclsid,
   improved `documentation <http://olefile.readthedocs.io/en/latest>`__
   with API reference.
-  2017-01-04: moved the documentation to
   `ReadTheDocs <http://olefile.readthedocs.io/en/latest>`__
-  2016-05-20: moved olefile repository to
   `GitHub <https://github.com/decalage2/olefile>`__
-  2016-02-02 v0.43: fixed issues
   `#26 <https://github.com/decalage2/olefile/issues/26>`__ and
   `#27 <https://github.com/decalage2/olefile/issues/27>`__, better
   handling of malformed files, use python logging.
-  2015-01-25 v0.42: improved handling of special characters in
   stream/storage names on Python 2.x (using UTF-8 instead of Latin-1),
   fixed bug in listdir with empty storages.
-  2014-11-25 v0.41: OleFileIO.open and isOleFile now support OLE files
   stored in byte strings, fixed installer for python 3, added support
   for Jython (Niko Ehrenfeuchter)
-  2014-10-01 v0.40: renamed OleFileIO_PL to olefile, added initial
   write support for streams >4K, updated doc and license, improved the
   setup script.
-  2014-07-27 v0.31: fixed support for large files with 4K sectors,
   thanks to Niko Ehrenfeuchter, Martijn Berger and Dave Jones. Added
   test scripts from Pillow (by hugovk). Fixed setup for Python 3
   (Martin Panter)
-  2014-02-04 v0.30: now compatible with Python 3.x, thanks to Martin
   Panter who did most of the hard work.
-  2013-07-24 v0.26: added methods to parse stream/storage timestamps,
   improved listdir to include storages, fixed parsing of direntry
   timestamps
-  2013-05-27 v0.25: improved metadata extraction, properties parsing
   and exception handling, fixed `issue
   #12 <https://github.com/decalage2/olefile/issues/12>`__
-  2013-05-07 v0.24: new features to extract metadata (get_metadata
   method and OleMetadata class), improved getproperties to convert
   timestamps to Python datetime
-  2012-10-09: published
   `python-oletools <https://www.decalage.info/python/oletools>`__, a
   package of analysis tools based on OleFileIO_PL
-  2012-09-11 v0.23: added support for file-like objects, fixed `issue
   #8 <https://github.com/decalage2/olefile/issues/8>`__
-  2012-02-17 v0.22: fixed issues #7 (bug in getproperties) and #2
   (added close method)
-  2011-10-20: code hosted on bitbucket to ease contributions and bug
   tracking
-  2010-01-24 v0.21: fixed support for big-endian CPUs, such as PowerPC
   Macs.
-  2009-12-11 v0.20: small bugfix in OleFileIO.open when filename is not
   plain str.
-  2009-12-10 v0.19: fixed support for 64 bits platforms (thanks to Ben
   G. and Martijn for reporting the bug)
