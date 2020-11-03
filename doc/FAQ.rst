==========================
Frequently Asked Questions
==========================

Can I extract all images from MS OLE2 documents with olefile?
-------------------------------------------------------------
Not directly: images are not always stored the same way, and it also depends on the format.

For example in Powerpoint presentations, you may find a stream named "Pictures"
when running "olefile yourfile.ppt". You may extract the stream by using the
openstream() method on the OleFileIO object, but you will usually get a binary
stream containing several picture files. You may also extract it manually using
tools such as SSView (http://www.mitec.cz/ssv.html).

Then the only way I've found so far is to use file carving tools which are
able to determine the beginning and the end of each picture in a binary file.
These tools are not always easy to use but if you're interested have a look
at https://pypi.org/project/hachoir-subfile/
and http://www.forensicswiki.org/wiki/Tools:Data_Recovery#Carving.

If you really need to automate the process then you have to study Microsoft
specifications (at http://www.microsoft.com/interop/docs/officebinaryformats.mspx)
and find the right way to parse MS Office documents...

A lot of people (including me) would be very interested if you find a solution! ;-)

Does olefile support password protected files?
----------------------------------------------
Actually there is no encryption at the OLE / compound file container level
(see `[MS-CFB] <https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-cfb/53989ce4-7b05-4f8d-829b-d08d6148375b>`_ specifications).
When encryption is used by an application such as MS Office to protect data in a file, it is always done at the application level
(see `[MS-OFFCRYPTO] <https://docs.microsoft.com/en-us/openspecs/office_file_formats/ms-offcrypto/3c34d72a-1a61-4b52-a893-196f9157f083>`_).
An OLE file is just a container, that can store data organised in streams and storages.
It is up to the application to manage the data (and potentially encryption).
So olefile does not manage encryption by itself.
For example if you need to decrypt/encrypt data in MS Office files, there are other libraries
such as `msoffcrypto-tool <https://github.com/nolze/msoffcrypto-tool>`_ that can handle it on top of olefile.
I use it in `oletools <https://github.com/decalage2/oletools>`_.
