olefile documentation
=====================

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    olefile




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

olefile v0.43 documentation
===========================

This is the home page of the documentation for olefile. The latest
version can be found
`online <https://bitbucket.org/decalage/olefileio_pl/wiki>`__, otherwise
a copy is provided in the doc subfolder of the package.

`olefile <http://www.decalage.info/olefile>`__ is a Python package to
parse, read and write `Microsoft OLE2
files <http://en.wikipedia.org/wiki/Compound_File_Binary_Format>`__
(also called Structured Storage, Compound File Binary Format or Compound
Document File Format), such as Microsoft Office 97-2003 documents, Image
Composer and FlashPix files, Outlook messages, StickyNotes, several
Microscopy file formats, McAfee antivirus quarantine files, etc.

**Quick links:** `Home page <http://www.decalage.info/olefile>`__ -
`Download/Install <https://bitbucket.org/decalage/olefileio_pl/wiki/Install>`__
- `Documentation <https://bitbucket.org/decalage/olefileio_pl/wiki>`__ -
`Report
Issues/Suggestions/Questions <https://bitbucket.org/decalage/olefileio_pl/issues?status=new&status=open>`__
- `Contact the author <http://decalage.info/contact>`__ -
`Repository <https://bitbucket.org/decalage/olefileio_pl>`__ - `Updates
on Twitter <https://twitter.com/decalage2>`__

Documentation pages
-------------------

-  [[License]]
-  [[Install]]
-  [[Contribute]], Suggest Improvements or Report Issues
-  [[OLE\_Overview]]
-  [[API]] and Usage

Features
--------

-  Parse, read and write any OLE file such as Microsoft Office 97-2003
   legacy document formats (Word .doc, Excel .xls, PowerPoint .ppt,
   Visio .vsd, Project .mpp), Image Composer and FlashPix files, Outlook
   messages, StickyNotes, Zeiss AxioVision ZVI files, Olympus FluoView
   OIB files, etc
-  List all the streams and storages contained in an OLE file
-  Open streams as files
-  Parse and read property streams, containing metadata of the file
-  Portable, pure Python module, no dependency

olefile can be used as an independent module or with PIL/Pillow.

olefile is mostly meant for developers. If you are looking for tools to
analyze OLE files or to extract data (especially for security purposes
such as malware analysis and forensics), then please also check my
`python-oletools <http://www.decalage.info/python/oletools>`__, which
are built upon olefile and provide a higher-level interface.

History
-------

olefile is based on the OleFileIO module from
`PIL <http://www.pythonware.com/products/pil/index.htm>`__, the
excellent Python Imaging Library, created and maintained by Fredrik
Lundh. The olefile API is still compatible with PIL, but since 2005 I
have improved the internal implementation significantly, with new
features, bugfixes and a more robust design. From 2005 to 2014 the
project was called OleFileIO\_PL, and in 2014 I changed its name to
olefile to celebrate its 9 years and its new write features.

As far as I know, this module is the most complete and robust Python
implementation to read MS OLE2 files, portable on several operating
systems. (please tell me if you know other similar Python modules)

Since 2014 olefile/OleFileIO\_PL has been integrated into
`Pillow <http://python-imaging.github.io/>`__, the friendly fork of PIL.
olefile will continue to be improved as a separate project, and new
versions will be merged into Pillow regularly.

Main improvements over the original version of OleFileIO in PIL:
----------------------------------------------------------------

-  Compatible with Python 3.x and 2.6+
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

--------------

olefile documentation
---------------------

-  [[Home]]
-  [[License]]
-  [[Install]]
-  [[Contribute]], Suggest Improvements or Report Issues
-  [[OLE\_Overview]]
-  [[API]] and Usage
