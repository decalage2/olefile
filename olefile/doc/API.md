How to use olefile
==================

olefile can be used as an independent module or with PIL/Pillow. The main functions and methods are explained below. 

For more information, see also the file **olefile.html**, sample code at the end of the module itself, and docstrings within the code.



Import olefile
--------------

	:::python
		import olefile

As of version 0.30, the code has been changed to be compatible with Python 3.x. As a consequence, compatibility with Python 2.5 or older is not provided anymore. However, a copy of OleFileIO_PL v0.26 (with some backported enhancements) is available as olefile2.py. When importing the olefile package, it falls back automatically to olefile2 if running on Python 2.5 or older. (new in v0.40)

If you think olefile should stay compatible with Python 2.5 or older, please [contact me](http://decalage.info/contact).
		

## Test if a file is an OLE container

Use isOleFile to check if the first bytes of the file contain the Magic for OLE files, before opening it. isOleFile returns True if it is an OLE file, False otherwise (new in v0.16).

	:::python
		assert olefile.isOleFile('myfile.doc')

		
## Open an OLE file from disk

Create an OleFileIO object with the file path as parameter:

	:::python
		ole = olefile.OleFileIO('myfile.doc')

## Open an OLE file from a file-like object

This is useful if the file is not on disk, e.g. already stored in a string or as a file-like object.

	:::python
		ole = olefile.OleFileIO(f)

For example the code below reads a file into a string, then uses BytesIO to turn it into a file-like object.

	:::python
		data = open('myfile.doc', 'rb').read()
		f = io.BytesIO(data) # or StringIO.StringIO for Python 2.x
		ole = olefile.OleFileIO(f)

## How to handle malformed OLE files

By default, the parser is configured to be as robust and permissive as possible, allowing to parse most malformed OLE files. Only fatal errors will raise an exception. It is possible to tell the parser to be more strict in order to raise exceptions for files that do not fully conform to the OLE specifications, using the raise_defect option (new in v0.14):

	:::python
		ole = olefile.OleFileIO('myfile.doc', raise_defects=olefile.DEFECT_INCORRECT)

When the parsing is done, the list of non-fatal issues detected is available as a list in the parsing_issues attribute of the OleFileIO object (new in 0.25):

	:::python
        print('Non-fatal issues raised during parsing:')
        if ole.parsing_issues:
            for exctype, msg in ole.parsing_issues:
                print('- %s: %s' % (exctype.__name__, msg))
        else:
            print('None')


## Open an OLE file in write mode

Before using the write features, the OLE file must be opened in read/write mode:

	:::python
    	ole = olefile.OleFileIO('test.doc', write_mode=True)

(new in v0.40)

The code for write features is new and it has not been thoroughly tested yet. See [issue #6](https://bitbucket.org/decalage/olefileio_pl/issue/6/improve-olefileio_pl-to-write-ole-files) for the roadmap and the implementation status. If you encounter any issue, please send me your [feedback](http://www.decalage.info/en/contact) or [report issues](https://bitbucket.org/decalage/olefileio_pl/issues?status=new&status=open).


## Syntax for stream and storage path

Two different syntaxes are allowed for methods that need or return the path of streams and storages:

1) Either a **list of strings** including all the storages from the root up to the stream/storage name. For example a stream called "WordDocument" at the root will have ['WordDocument'] as full path. A stream called "ThisDocument" located in the storage "Macros/VBA" will be ['Macros', 'VBA', 'ThisDocument']. This is the original syntax from PIL. While hard to read and not very convenient, this syntax works in all cases.

2) Or a **single string with slashes** to separate storage and stream names (similar to the Unix path syntax). The previous examples would be 'WordDocument' and 'Macros/VBA/ThisDocument'. This syntax is easier, but may fail if a stream or storage name contains a slash. (new in v0.15)

Both are case-insensitive.

Switching between the two is easy:

	:::python
		slash_path = '/'.join(list_path)
		list_path  = slash_path.split('/')


## Get the list of streams

listdir() returns a list of all the streams contained in the OLE file, including those stored in storages. Each stream is listed itself as a list, as described above. 

	:::python
		print(ole.listdir())

Sample result:

	:::python
		[['\x01CompObj'], ['\x05DocumentSummaryInformation'], ['\x05SummaryInformation']
		, ['1Table'], ['Macros', 'PROJECT'], ['Macros', 'PROJECTwm'], ['Macros', 'VBA',
		'Module1'], ['Macros', 'VBA', 'ThisDocument'], ['Macros', 'VBA', '_VBA_PROJECT']
		, ['Macros', 'VBA', 'dir'], ['ObjectPool'], ['WordDocument']]

As an option it is possible to choose if storages should also be listed, with or without streams (new in v0.26):

	:::python
		ole.listdir (streams=False, storages=True)

		
## Test if known streams/storages exist:

exists(path) checks if a given stream or storage exists in the OLE file (new in v0.16). The provided path is case-insensitive.

	:::python
		if ole.exists('worddocument'):
		    print("This is a Word document.")
		    if ole.exists('macros/vba'):
		         print("This document seems to contain VBA macros.")
	
	
## Read data from a stream

openstream(path) opens a stream as a file-like object. The provided path is case-insensitive.

The following example extracts the "Pictures" stream from a PPT file:

	:::python
	    pics = ole.openstream('Pictures')
	    data = pics.read()


## Get information about a stream/storage

Several methods can provide the size, type and timestamps of a given stream/storage:

get_size(path) returns the size of a stream in bytes (new in v0.16):

	:::python
		s = ole.get_size('WordDocument')

get_type(path) returns the type of a stream/storage, as one of the following constants: STGTY\_STREAM for a stream, STGTY\_STORAGE for a storage, STGTY\_ROOT for the root entry, and False for a non existing path (new in v0.15).

	:::python
		t = ole.get_type('WordDocument')

get\_ctime(path) and get\_mtime(path) return the creation and modification timestamps of a stream/storage, as a Python datetime object with UTC timezone. Please note that these timestamps are only present if the application that created the OLE file explicitly stored them, which is rarely the case. When not present, these methods return None (new in v0.26).

	:::python
		c = ole.get_ctime('WordDocument')
		m = ole.get_mtime('WordDocument')
	
The root storage is a special case: You can get its creation and modification timestamps using the OleFileIO.root attribute (new in v0.26):

	:::python
		c = ole.root.getctime()
		m = ole.root.getmtime()

Note: all these methods are case-insensitive.

## Overwriting a sector

The write_sect method can overwrite any sector of the file. If the provided data is smaller than the sector size (normally 512 bytes, sometimes 4KB), data is padded with null characters. (new in v0.40)

Here is an example:

	:::python
        ole.write_sect(0x17, b'TEST')

Note: following the [MS-CFB specifications](http://msdn.microsoft.com/en-us/library/dd942138.aspx), sector 0 is actually the second sector of the file. You may use -1 as index to write the first sector.


## Overwriting a stream

The write_stream method can overwrite an existing stream in the file. The new stream data must be the exact same size as the existing one. For now, write_stream can only write streams of 4KB or larger (stored in the main FAT).

For example, you may change text in a MS Word document:

	:::python
        ole = olefile.OleFileIO('test.doc', write_mode=True)
	    data = ole.openstream('WordDocument').read()
	    data = data.replace(b'foo', b'bar')
	    ole.write_stream('WordDocument', data)
	    ole.close()

(new in v0.40)



## Extract metadata

get_metadata() will check if standard property streams exist, parse all the properties they contain, and return an OleMetadata object with the found properties as attributes (new in v0.24).

	:::python
		meta = ole.get_metadata()
		print('Author:', meta.author)
		print('Title:', meta.title)
		print('Creation date:', meta.create_time)
		# print all metadata:
		meta.dump()

Available attributes include:

	:::text
	    codepage, title, subject, author, keywords, comments, template,
	    last_saved_by, revision_number, total_edit_time, last_printed, create_time,
	    last_saved_time, num_pages, num_words, num_chars, thumbnail,
	    creating_application, security, codepage_doc, category, presentation_target,
	    bytes, lines, paragraphs, slides, notes, hidden_slides, mm_clips,
	    scale_crop, heading_pairs, titles_of_parts, manager, company, links_dirty,
	    chars_with_spaces, unused, shared_doc, link_base, hlinks, hlinks_changed,
	    version, dig_sig, content_type, content_status, language, doc_version

See the source code of the OleMetadata class for more information.


## Parse a property stream

get\_properties(path) can be used to parse any property stream that is not handled by get\_metadata. It returns a dictionary indexed by integers. Each integer is the index of the property, pointing to its value. For example in the standard property stream '\x05SummaryInformation', the document title is property #2, and the subject is #3.  

	:::python
		p = ole.getproperties('specialprops')

By default as in the original PIL version, timestamp properties are converted into a number of seconds since Jan 1,1601. With the option convert\_time, you can obtain more convenient Python datetime objects (UTC timezone). If some time properties should not be converted (such as total editing time in '\x05SummaryInformation'), the list of indexes can be passed as no_conversion (new in v0.25):

	:::python
		p = ole.getproperties('specialprops', convert_time=True, no_conversion=[10])


## Close the OLE file

Unless your application is a simple script that terminates after processing an OLE file, do not forget to close each OleFileIO object after parsing to close the file on disk. (new in v0.22)

	:::python
		ole.close()
		
## Use olefile as a script for testing/debugging
		
olefile can also be used as a script from the command-line to display the structure of an OLE file and its metadata, for example:

	:::text
		olefile.py myfile.doc

You can use the option -c to check that all streams can be read fully, and -d to generate very verbose debugging information.

--------------------------------------------------------------------------

olefile documentation
---------------------

- [[Home]]
- [[License]]
- [[Install]]
- [[Contribute]], Suggest Improvements or Report Issues
- [[OLE_Overview]]
- [[API]] and Usage
