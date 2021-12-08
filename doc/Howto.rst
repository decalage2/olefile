=================================
How to use olefile - API overview
=================================

This page is part of the documentation for
`olefile <http://olefile.readthedocs.io/en/latest/>`__. It
explains how to use all its features to parse and write OLE files. For
more information about OLE files, see :doc:`OLE_Overview`.

olefile can be used as an independent module or with PIL/Pillow. The
main functions and methods are explained below.

For more information, see also the :doc:`olefile`, sample code at
the end of the module itself, and docstrings within the code.

Import olefile
--------------

When the :py:mod:`olefile` package has been installed, it can be imported in
Python applications with this statement:

::

    import olefile

As of version 0.30, the code has been changed to be compatible with
Python 3.x. As a consequence, compatibility with Python 2.5 or older is
not provided anymore.

Test if a file is an OLE container
----------------------------------

Use :py:func:`olefile.isOleFile` to check if the first bytes of the file contain the
Magic for OLE files, before opening it. isOleFile returns True if it is
an OLE file, False otherwise (new in v0.16).

::

    assert olefile.isOleFile('myfile.doc')

The argument of isOleFile can be (new in v0.41):

-  the path of the file to open on disk (bytes or unicode string smaller
   than 1536 bytes),
-  or a bytes string containing the file in memory. (bytes string longer
   than 1535 bytes),
-  or a file-like object (with read and seek methods).

Open an OLE file from disk
--------------------------

Create an :py:class:`olefile.OleFileIO` object with the file path as parameter:

::

    ole = olefile.OleFileIO('myfile.doc')

Since olefile v0.46, the recommended way to open an OLE file is to use
OleFileIO as a context manager, using the "with" clause:

::

    with olefile.OleFileIO('myfile.doc') as ole
        # perform all operations on the ole object

This guarantees that the OleFileIO object is closed when exiting
the with block, even if an exception is triggered.
It will call :py:meth:`olefile.OleFileIO.close` automatically.

(new in v0.46)


Open an OLE file from a bytes string
------------------------------------

This is useful if the file is already stored in memory as a bytes
string.

::

    ole = olefile.OleFileIO(s)


Note: olefile checks the size of the string provided as argument to
determine if it is a file path or the content of an OLE file. An OLE
file cannot be smaller than 1536 bytes. If the string is larger than
1535 bytes, then it is expected to contain an OLE file, otherwise it is
expected to be a file path.

(new in v0.41)

Open an OLE file from a file-like object
----------------------------------------

This is useful if the file is not on disk but only available as a
file-like object (with read, seek and tell methods).

::

    ole = olefile.OleFileIO(f)

If the file-like object does not have seek or tell methods, the easiest
solution is to read the file entirely in a bytes string before parsing:

::

    data = f.read()
    ole = olefile.OleFileIO(data)

How to handle malformed OLE files
---------------------------------

By default, the parser is configured to be as robust and permissive as
possible, allowing to parse most malformed OLE files. Only fatal errors
will raise an exception. It is possible to tell the parser to be more
strict in order to raise exceptions for files that do not fully conform
to the OLE specifications, using the ``raise_defect`` option (new in
v0.14):

::

    ole = olefile.OleFileIO('myfile.doc', raise_defects=olefile.DEFECT_INCORRECT)

When the parsing is done, the list of non-fatal issues detected is
available as a list in the :py:attr:`olefile.OleFileIO.parsing_issues` attribute of the OleFileIO
object (new in 0.25):

::

    print('Non-fatal issues raised during parsing:')
    if ole.parsing_issues:
        for exctype, msg in ole.parsing_issues:
            print('- %s: %s' % (exctype.__name__, msg))
    else:
        print('None')

Open an OLE file in write mode
------------------------------

Before using the write features, the OLE file must be opened in
read/write mode, by using the option ``write_mode=True``:

::

    ole = olefile.OleFileIO('test.doc', write_mode=True)

(new in v0.40)

The code for write features is new and it has not been thoroughly tested
yet. See `issue #6 <https://github.com/decalage2/olefile/issues/6>`__
for the roadmap and the implementation status. If you encounter any
issue, please send me your `feedback <http://www.decalage.info/en/contact>`__
or `report issues <https://github.com/decalage2/olefile/issues>`__.

Syntax for stream and storage paths
-----------------------------------

Two different syntaxes are allowed for methods that need or return the
path of streams and storages:

1) Either a **list of strings** including all the storages from the root
   up to the stream/storage name. For example a stream called
   "WordDocument" at the root will have ``['WordDocument']`` as full path. A
   stream called "ThisDocument" located in the storage "Macros/VBA" will
   be ``['Macros', 'VBA', 'ThisDocument']``. This is the original syntax
   from PIL. While hard to read and not very convenient, this syntax
   works in all cases.

2) Or a **single string with slashes** to separate storage and stream
   names (similar to the Unix path syntax). The previous examples would
   be ``'WordDocument'`` and ``'Macros/VBA/ThisDocument'``. This syntax is
   easier, but may fail if a stream or storage name contains a slash
   (which is normally not allowed, according to the Microsoft
   specifications [MS-CFB]). (new in v0.15)

Both are case-insensitive.

Switching between the two is easy:

::

    slash_path = '/'.join(list_path)
    list_path  = slash_path.split('/')

**Encoding**:

-  Stream and Storage names are stored in Unicode format in OLE files,
   which means they may contain special characters (e.g. Greek,
   Cyrillic, Japanese, etc) that applications must support to avoid
   exceptions.
-  **On Python 2.x**, all stream and storage paths are handled by
   olefile in bytes strings, using the **UTF-8 encoding** by default. If
   you need to use Unicode instead, add the option
   ``path_encoding=None`` when creating the OleFileIO object. This is
   new in v0.42. Olefile was using the Latin-1 encoding until v0.41,
   therefore special characters were not supported.
-  **On Python 3.x**, all stream and storage paths are handled by
   olefile in unicode strings, without encoding.

Get the list of streams
-----------------------

:py:meth:`olefile.OleFileIO.listdir` returns a list of all the streams contained in the OLE file,
including those stored in storages. Each stream is listed itself as a
list, as described above.

::

    print(ole.listdir())

Sample result:

::

    [['\x01CompObj'], ['\x05DocumentSummaryInformation'], ['\x05SummaryInformation']
    , ['1Table'], ['Macros', 'PROJECT'], ['Macros', 'PROJECTwm'], ['Macros', 'VBA',
    'Module1'], ['Macros', 'VBA', 'ThisDocument'], ['Macros', 'VBA', '_VBA_PROJECT']
    , ['Macros', 'VBA', 'dir'], ['ObjectPool'], ['WordDocument']]

As an option it is possible to choose if storages should also be listed,
with or without streams (new in v0.26):

::

    ole.listdir (streams=False, storages=True)

Test if known streams/storages exist:
-------------------------------------

:py:meth:`olefile.OleFileIO.exists` checks if a given stream or storage exists in the OLE file
(new in v0.16). The provided path is case-insensitive.

::

    if ole.exists('worddocument'):
        print("This is a Word document.")
        if ole.exists('macros/vba'):
             print("This document seems to contain VBA macros.")

Read data from a stream
-----------------------

:py:meth:`olefile.OleFileIO.openstream` opens a stream as a file-like object. The provided path
is case-insensitive.

The following example extracts the "Pictures" stream from a PPT file:

::

    pics = ole.openstream('Pictures')
    data = pics.read()

Get information about a stream/storage
--------------------------------------

Several methods can provide the size, type and timestamps of a given
stream/storage:

:py:meth:`olefile.OleFileIO.get_size` returns the size of a stream in bytes (new in v0.16):

::

    s = ole.get_size('WordDocument')

:py:meth:`olefile.OleFileIO.get_type` returns the type of a stream/storage, as one of the
following constants: :py:data:`olefile.STGTY_STREAM` for a stream, :py:data:`olefile.STGTY_STORAGE` for a
storage, :py:data:`olefile.STGTY_ROOT` for the root entry, and ``False`` for a non existing
path (new in v0.15).

::

    t = ole.get_type('WordDocument')

:py:meth:`olefile.OleFileIO.getctime` and :py:meth:`olefile.OleFileIO.getmtime` return the creation and
modification timestamps of a stream/storage, as a Python datetime object
with UTC timezone. Please note that these timestamps are only present if
the application that created the OLE file explicitly stored them, which
is rarely the case. When not present, these methods return None (new in
v0.26).

::

    c = ole.getctime('WordDocument')
    m = ole.getmtime('WordDocument')

The root storage is a special case: You can get its creation and
modification timestamps using the OleFileIO.root attribute (new in
v0.26):

::

    c = ole.root.getctime()
    m = ole.root.getmtime()

Note: all these methods are case-insensitive.

Overwriting a sector
--------------------

The :py:meth:`olefile.OleFileIO.write_sect` method can overwrite any sector of the file. If the
provided data is smaller than the sector size (normally 512 bytes,
sometimes 4KB), data is padded with null characters. (new in v0.40)

Here is an example:

::

    ole.write_sect(0x17, b'TEST')

Note: following the `MS-CFB
specifications <http://msdn.microsoft.com/en-us/library/dd942138.aspx>`__,
sector 0 is actually the second sector of the file. You may use -1 as
index to write the first sector.

Overwriting a stream
--------------------

The :py:meth:`olefile.OleFileIO.write_stream` method can overwrite an existing stream in the file.
Important: The new stream data must be the exact same size as the existing one,
it is not possible to change the size of a stream.
Since v0.45, this method works on any stream (stored in the main FAT or the MiniFAT).

For example, you may change text in a MS Word document:

::

    ole = olefile.OleFileIO('test.doc', write_mode=True)
    data = ole.openstream('WordDocument').read()
    data = data.replace(b'foo', b'bar')
    ole.write_stream('WordDocument', data)
    ole.close()

(new in v0.40)

Extract metadata
----------------

:py:meth:`olefile.OleFileIO.get_metadata` will check if standard property streams exist, parse all
the properties they contain, and return an :py:class:`olefile.OleFileIO.OleMetadata` object with the
found properties as attributes (new in v0.24).

::

    meta = ole.get_metadata()
    print('Author:', meta.author)
    print('Title:', meta.title)
    print('Creation date:', meta.create_time)
    # print all metadata:
    meta.dump()

Available attributes include:

::

    codepage, title, subject, author, keywords, comments, template,
    last_saved_by, revision_number, total_edit_time, last_printed, create_time,
    last_saved_time, num_pages, num_words, num_chars, thumbnail,
    creating_application, security, codepage_doc, category, presentation_target,
    bytes, lines, paragraphs, slides, notes, hidden_slides, mm_clips,
    scale_crop, heading_pairs, titles_of_parts, manager, company, links_dirty,
    chars_with_spaces, unused, shared_doc, link_base, hlinks, hlinks_changed,
    version, dig_sig, content_type, content_status, language, doc_version

See the source code of the :py:class:`olefile.OleFileIO.OleMetadata` class for more information.

Parse a property stream
-----------------------

:py:meth:`olefile.OleFileIO.getproperties` can be used to parse any property stream that is
not handled by get_metadata. It returns a dictionary indexed by
integers. Each integer is the index of the property, pointing to its
value. For example in the standard property stream
``'\x05SummaryInformation'``, the document title is property
#2, and the subject is #3.

::

    p = ole.getproperties('specialprops')

By default as in the original PIL version, timestamp properties are
converted into a number of seconds since Jan 1,1601. With the option
``convert_time``, you can obtain more convenient Python datetime objects
(UTC timezone). If some time properties should not be converted (such as
total editing time in ``'\x05SummaryInformation'``), the list
of indexes can be passed as no\_conversion (new in v0.25):

::

    p = ole.getproperties('specialprops', convert_time=True, no_conversion=[10])

Close the OLE file
------------------

Unless your application is a simple script that terminates after
processing an OLE file, do not forget to close each OleFileIO object
after parsing to close the file on disk. (new in v0.22)

::

    ole.close()


Enable logging
--------------

See :py:func:`olefile.enable_logging`

Use olefile as a script for testing/debugging
---------------------------------------------

olefile can also be used as a script from the command-line to display
the structure of an OLE file and its metadata, for example:

::

    olefile.py myfile.doc

You can use the option ``-c`` to check that all streams can be read fully,
and ``-d`` to generate very verbose debugging information.

You may also add the option ``-l debug`` to display debugging messages
(very verbose).

