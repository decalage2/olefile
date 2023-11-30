Detailed CHANGELOG
==================

olefile.py
----------
* 2023-11-30 v0.47.dev6:
    - fixed issue #142: isOleFile has a new data parameter to handle files in memory properly
    - fixed issue #156: write_sect now correctly detects when data is larger than the sector size
    - removed method get_document_variables, to be integrated in oletools (Word specific feature)
    - use GitHub actions for testing and Codecov for coverage, added python 3.8 to 3.12 (PR #157 by @hugovk)
* 2020-10-07 v0.47.dev4:
    - added VT_VECTOR support for properties (PR #135 by Maciej Kotowicz @mak)
    - olefile is now distributed as a wheel package (PR #130 by @hugovk)
    - olefile will not close a file handle if it was provided by the caller
      (PR #121 by Christian Herdtweck, issue #120)
* 2019-05-08 v0.47.dev3:
    - added methods get_userdefined_properties and get_document_variables (PR #114 by Malwrologist @DissectMalware)
* 2019-04-28 v0.47.dev2:
    - added exceptions OleFileError and NotOleFileError to replace IOError (PR #110 by Ken Peterson @TheElementalOfCreation)
* 2019-04-20 v0.47.dev1:
    - removed support for Python 3.4 (PR #118 by @hugovk)
* **2018-09-09 v0.46 PL**:
    - official v0.46 release
* 2018-09-05 v0.46dev2 PL:
    - fixed issue #96, disabled the VT dictionary which was not used anymore
* 2018-08-23 v0.46dev1 PL:
    - added main function (for pip entry points)
    - fixed bug in OleDirectoryEntry.dump
    - merged PR #93 by @enkelli, fixing issues #61, #103 and https://github.com/decalage2/oletools/issues/311
    - merged PR #94 by @enkelli, 'float' object cannot be interpreted as an integer
    - merged PR #101 by @OskarPersson, added context manager to OleFileIO
* 2018-01-15 v0.45dev5 PL:
    - fixed issue #79, added missing constants to \_\_all__
* 2018-01-07 v0.45dev4 PL:
    - merged PR #59 by @kijeong, olefile can now write mini streams
* 2017-11-20 v0.45dev3 PL:
    - fixed issue #81, raise an exception when attempting to open a stream after
      the file was closed.
* 2017-11-05 v0.45dev2 PL:
    - fixed issue #31, set all attributes in OleFileIO.\_\_init__, use force_FAT=True in loaddirectory
    - fixed issue #56, tests folder now included in the distribution package
    - fixed issues #70 and #73, an incorrect byte order is now ignored

(TODO: reverse order to have latest changes on top, use MD formatting)
```
History from PIL 1.1.6:
1997-01-20 fl   Created
1997-01-22 fl   Fixed 64-bit portability quirk
2003-09-09 fl   Fixed typo in OleFileIO.loadfat (noted by Daniel Haertle)
2004-02-29 fl   Changed long hex constants to signed integers

(only olefile/OleFileIO_PL changes compared to PIL 1.1.6)
2005-05-11 v0.10 PL: - a few fixes for Python 2.4 compatibility
                       (all changes flagged with [PL])
2006-02-22 v0.11 PL: - a few fixes for some Office 2003 documents which raise
                       exceptions in OleStream.__init__()
2006-06-09 v0.12 PL: - fixes for files above 6.8MB (DIFAT in loadfat)
                     - added some constants
                     - added header values checks
                     - added some docstrings
                     - getsect: bugfix in case sectors >512 bytes
                     - getsect: added conformity checks
                     - DEBUG_MODE constant to activate debug display
2007-09-04 v0.13 PL: - improved/translated (lots of) comments
                     - updated license
                     - converted tabs to 4 spaces
2007-11-19 v0.14 PL: - added OleFileIO._raise_defect() to adapt sensitivity
                     - improved _unicode() to use Python 2.x unicode support
                     - fixed bug in OleDirectoryEntry
2007-11-25 v0.15 PL: - added safety checks to detect FAT loops
                     - fixed OleStream which didn't check stream size
                     - added/improved many docstrings and comments
                     - moved helper functions _unicode and _clsid out of
                       OleFileIO class
                     - improved OleFileIO._find() to add Unix path syntax
                     - OleFileIO._find() is now case-insensitive
                     - added get_type() and get_rootentry_name()
                     - rewritten loaddirectory and OleDirectoryEntry
2007-11-27 v0.16 PL: - added OleDirectoryEntry.kids_dict
                     - added detection of duplicate filenames in storages
                     - added detection of duplicate references to streams
                     - added get_size() and exists() to OleDirectoryEntry
                     - added isOleFile to check header before parsing
                     - added __all__ list to control public keywords in pydoc
2007-12-04 v0.17 PL: - added _load_direntry to fix a bug in loaddirectory
                     - improved _unicode(), added workarounds for Python <2.3
                     - added set_debug_mode and -d option to set debug mode
                     - fixed bugs in OleFileIO.open and OleDirectoryEntry
                     - added safety check in main for large or binary
                       properties
                     - allow size>0 for storages for some implementations
2007-12-05 v0.18 PL: - fixed several bugs in handling of FAT, MiniFAT and
                       streams
                     - added option '-c' in main to check all streams
2009-12-10 v0.19 PL: - bugfix for 32 bit arrays on 64 bits platforms
                       (thanks to Ben G. and Martijn for reporting the bug)
2009-12-11 v0.20 PL: - bugfix in OleFileIO.open when filename is not plain str
2010-01-22 v0.21 PL: - added support for big-endian CPUs such as PowerPC Macs
2012-02-16 v0.22 PL: - fixed bug in getproperties, patch by chuckleberryfinn
                       (https://github.com/decalage2/olefile/issues/7)
                     - added close method to OleFileIO (fixed issue #2)
2012-07-25 v0.23 PL: - added support for file-like objects (patch by mete0r_kr)
2013-05-05 v0.24 PL: - getproperties: added conversion from filetime to python
                       datetime
                     - main: displays properties with date format
                     - new class OleMetadata to parse standard properties
                     - added get_metadata method
2013-05-07 v0.24 PL: - a few improvements in OleMetadata
2013-05-24 v0.25 PL: - getproperties: option to not convert some timestamps
                     - OleMetaData: total_edit_time is now a number of seconds,
                       not a timestamp
                     - getproperties: added support for VT_BOOL, VT_INT, V_UINT
                     - getproperties: filter out null chars from strings
                     - getproperties: raise non-fatal defects instead of
                       exceptions when properties cannot be parsed properly
2013-05-27       PL: - getproperties: improved exception handling
                     - _raise_defect: added option to set exception type
                     - all non-fatal issues are now recorded, and displayed
                       when run as a script
2013-07-11 v0.26 PL: - added methods to get modification and creation times
                       of a directory entry or a storage/stream
                     - fixed parsing of direntry timestamps
2013-07-24       PL: - new options in listdir to list storages and/or streams
2014-02-04 v0.30 PL: - upgraded code to support Python 3.x by Martin Panter
                     - several fixes for Python 2.6 (xrange, MAGIC)
                     - reused i32 from Pillow's _binary
2014-07-18 v0.31     - preliminary support for 4K sectors
2014-07-27 v0.31 PL: - a few improvements in OleFileIO.open (header parsing)
                     - Fixed loadfat for large files with 4K sectors (issue #3)
2014-07-30 v0.32 PL: - added write_sect to write sectors to disk
                     - added write_mode option to OleFileIO.__init__ and open
2014-07-31       PL: - fixed padding in write_sect for Python 3, added checks
                     - added write_stream to write a stream to disk
2014-09-26 v0.40 PL: - renamed OleFileIO_PL to olefile
2014-11-09       NE: - added support for Jython (Niko Ehrenfeuchter)
2014-11-13 v0.41 PL: - improved isOleFile and OleFileIO.open to support OLE
                       data in a string buffer and file-like objects.
2014-11-21       PL: - updated comments according to Pillow's commits
2015-01-24 v0.42 PL: - changed the default path name encoding from Latin-1
                       to UTF-8 on Python 2.x (Unicode on Python 3.x)
                     - added path_encoding option to override the default
                     - fixed a bug in _list when a storage is empty
2015-04-17 v0.43 PL: - slight changes in OleDirectoryEntry
2015-10-19           - fixed issue #26 in OleFileIO.getproperties
                       (using id and type as local variable names)
2015-10-29           - replaced debug() with proper logging
                     - use optparse to handle command line options
                     - improved attribute names in OleFileIO class
2015-11-05           - fixed issue #27 by correcting the MiniFAT sector
                       cutoff size if invalid.
2016-02-02           - logging is disabled by default
2016-04-26 v0.44 PL: - added enable_logging
                     - renamed _OleDirectoryEntry and _OleStream without '_'
                     - in OleStream use _raise_defect instead of exceptions
2016-04-27           - added support for incomplete streams and incorrect
                       directory entries (to read malformed documents)
2016-05-04           - fixed slight bug in OleStream
2016-11-27       DR: - added method to get the clsid of a storage/stream
                       (Daniel Roethlisberger)
2017-05-31 v0.45 BS: - PR #114 from oletools to handle excessive number of
                       properties:
                       https://github.com/decalage2/oletools/pull/114
```

setup.py
--------
```
2007-09-13 v0.01 PL: - first version
2007-11-10 v0.02 PL: - updated website URL
2007-12-04 v0.03 PL: - updated description, added debug_mode test
2009-09-11 v0.04 PL: - updated URL, e-mail, licence, disabled e-mail
2012-02-16 v0.05 PL: - added download URL on bitbucket
2012-09-11 v0.06 PL: - read long description from disk in rst format
2014-02-04 v0.07 PL: - added PyPI classifier for Python 3.x, added PL2 version
2014-09-26 v0.08 PL: - install the olefile package instead of modules
2014-10-10 v0.09 PL: - fixed compilation error on Python 3
2016-01-29 v0.10 PL: - fixed issue #28, removed DEBUG_MODE test
2016-01-05 v0.44 PL: - removed the legacy doc subfolder
```
