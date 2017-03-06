from __future__ import print_function
import os
from shutil import copy2

try:
    import unittest2 as unittest  # Python 2.6
except ImportError:
    import unittest


import OleFileIO_PL as OleFileIO


class TestOlefile(unittest.TestCase):

    def setUp(self):
        self.non_ole_file = "tests/images/flower.jpg"
        self.ole_file = "tests/images/test-ole-file.doc"

    def test_isOleFile_false(self):
        is_ole = OleFileIO.isOleFile(self.non_ole_file)
        self.assertFalse(is_ole)

    def test_isOleFile_true(self):
        is_ole = OleFileIO.isOleFile(self.ole_file)
        self.assertTrue(is_ole)

    def test_exists_worddocument(self):
        ole = OleFileIO.OleFileIO(self.ole_file)
        exists = ole.exists('worddocument')
        self.assertTrue(exists)

    def test_exists_no_vba_macros(self):
        ole = OleFileIO.OleFileIO(self.ole_file)
        exists = ole.exists('macros/vba')
        self.assertFalse(exists)

    def test_get_type(self):
        ole = OleFileIO.OleFileIO(self.ole_file)
        doc_type = ole.get_type('worddocument')
        self.assertEqual(doc_type, OleFileIO.STGTY_STREAM)

    def test_get_size(self):
        ole = OleFileIO.OleFileIO(self.ole_file)
        size = ole.get_size('worddocument')
        self.assertGreater(size, 0)

    def test_get_rootentry_name(self):
        ole = OleFileIO.OleFileIO(self.ole_file)
        root = ole.get_rootentry_name()
        self.assertEqual(root, "Root Entry")

    def test_meta(self):
        ole = OleFileIO.OleFileIO(self.ole_file)
        meta = ole.get_metadata()
        self.assertEqual(meta.author, b"Laurence Ipsum")
        self.assertEqual(meta.num_pages, 1)
        
    def test_minifat_writing(self):
        ole_file_copy = "tests/images/test-ole-file-copy.doc"
        minifat_stream_name = "\x01compobj"
        if os.path.isfile(ole_file_copy):
            os.remove(ole_file_copy)
        copy2(self.ole_file, ole_file_copy)
        
        ole = OleFileIO.OleFileIO(ole_file_copy, write_mode = True)
        stream = ole.openstream(minifat_stream_name)
        self.assertTrue(stream.size < ole.minisectorcutoff)
        str_read = stream.read()
        self.assertTrue(len(str_read) == stream.size)
        self.assertTrue(str_read != '\x00' * stream.size)
        stream.close()
        ole.write_stream(minifat_stream_name, '\x00' * stream.size)
        ole.close()
    
        ole = OleFileIO.OleFileIO(ole_file_copy)
        stream = ole.openstream(minifat_stream_name)
        self.assertTrue(stream.size < ole.minisectorcutoff)
        str_read_replaced = stream.read()
        self.assertTrue(len(str_read_replaced) == stream.size)
        self.assertTrue(str_read_replaced != str_read)
        self.assertTrue(str_read_replaced == '\x00' * len(str_read))
        stream.close()
        ole.close()
        os.remove(ole_file_copy)

if __name__ == '__main__':
    unittest.main()
