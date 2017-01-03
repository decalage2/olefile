from __future__ import print_function

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

if __name__ == '__main__':
    unittest.main()
