========
Features
========

-  Parse, read and write any OLE file such as Microsoft Office 97-2003
   legacy document formats (Word .doc, Excel .xls, PowerPoint .ppt,
   Visio .vsd, Project .mpp), Image Composer and FlashPix files, Outlook
   messages, StickyNotes, Zeiss AxioVision ZVI files, Olympus FluoView
   OIB files, etc
-  List all the streams and storages contained in an OLE file
-  Open streams as files
-  Parse and read property streams, containing metadata of the file
-  Portable, pure Python module, no dependency

olefile can be used as an independent module or with `PIL <http://www.pythonware.com/products/pil/>`__
/ `Pillow <https://python-pillow.org/>`__.

olefile is mostly meant for developers. If you are looking for tools to
analyze OLE files or to extract data (especially for security purposes
such as malware analysis and forensics), then please also check my
`python-oletools <https://www.decalage.info/python/oletools>`__, which
are built upon olefile and provide a higher-level interface.
