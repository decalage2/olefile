=======
History
=======

olefile is based on the `OleFileIO module <http://svn.effbot.org/public/tags/pil-1.1.7/PIL/OleFileIO.py>`__
from `PIL <http://www.pythonware.com/products/pil/index.htm>`__ v1.1.7, the
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
`Pillow <http://python-imaging.github.io/>`__, the friendly fork of PIL.

In January 2017, it was decided to remove olefile from Pillow 4.0.0 and
to install it as an external dependency. This will avoid issues
due to the maintenance of the olefile code in two repositories.

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
