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

