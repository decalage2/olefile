"""Synthetic regressions: no external or potentially malicious samples."""
import array
import struct
import unittest
from olefile import olefile as impl


def directory_entry():
    # OleDirectoryEntry is an old-style class on Python 2.7.
    if hasattr(impl.OleDirectoryEntry, '__new__'):
        return impl.OleDirectoryEntry.__new__(impl.OleDirectoryEntry)
    import new
    return new.instance(impl.OleDirectoryEntry)


class TestMalformedProperties(unittest.TestCase):
    def setUp(self):
        self.ole = impl.OleFileIO()

    def parse(self, data, kind):
        return self.ole._parse_property(data, 0, 2, kind, False, [])

    def test_huge_unsupported_vector_rejected(self):
        with self.assertRaises(ValueError):
            self.parse(struct.pack('<I', 0xffffffff), impl.VT_VECTOR | impl.VT_EMPTY)

    def test_unsupported_vector_does_not_repeat_without_progress(self):
        with self.assertRaises(ValueError):
            self.parse(struct.pack('<I', 2) + b'xx', impl.VT_VECTOR | impl.VT_EMPTY)

    def test_huge_variant_vector_rejected(self):
        with self.assertRaises(ValueError):
            self.parse(struct.pack('<I', 0xffffffff), impl.VT_VECTOR | impl.VT_VARIANT)

    def test_supported_vector_preserved(self):
        self.assertEqual(self.parse(struct.pack('<III', 2, 17, 23),
                                    impl.VT_VECTOR | impl.VT_UI4), [17, 23])

    def test_empty_vector_preserved(self):
        self.assertEqual(self.parse(struct.pack('<I', 0),
                                    impl.VT_VECTOR | impl.VT_EMPTY), [])

    def test_truncated_blob_vector_rejected(self):
        with self.assertRaises(ValueError):
            self.parse(struct.pack('<II', 1, 100) + b'x', impl.VT_VECTOR | impl.VT_BLOB)

    def test_null_variant_has_type_header_progress(self):
        self.assertEqual(self.parse(struct.pack('<III', 2, impl.VT_EMPTY, impl.VT_NULL),
                                    impl.VT_VECTOR | impl.VT_VARIANT), [None, None])


class TestSectorChains(unittest.TestCase):
    def entry(self, mini=False):
        entry = directory_entry()
        entry.entry_type = impl.STGTY_STREAM
        entry.size = 10
        entry.is_minifat = mini
        entry.isectStart = 0
        entry.sect_chain = None
        return entry

    def test_cycles_and_invalid_indices(self):
        for fat in ([0], [1, 0], [99], [-1], [impl.FREESECT]):
            for mini in (False, True):
                ole = impl.OleFileIO()
                ole.fat = ole.minifat = fat
                entry = self.entry(mini)
                with self.assertRaises(impl.OleFileError):
                    entry.build_sect_chain(ole)
                self.assertIsNone(entry.sect_chain)

    def test_fat_loading_appends_in_place(self):
        ole = impl.OleFileIO()
        ole.fat = array.array(impl.UINT32, [4])
        original = ole.fat
        ole.getsect = lambda sector: struct.pack('<II', 7, 8)
        ole.loadfat_sect(array.array(impl.UINT32, [0, impl.ENDOFCHAIN]))
        self.assertIs(ole.fat, original)
        self.assertEqual(list(ole.fat), [4, 7, 8])


class TestDirectoryTraversal(unittest.TestCase):
    def node(self, name, kind, kids=None):
        entry = directory_entry()
        entry.name, entry.entry_type, entry.kids = name, kind, kids or []
        return entry

    def test_self_referential_storage(self):
        root = self.node('root', impl.STGTY_ROOT)
        storage = self.node('storage', impl.STGTY_STORAGE)
        root.kids = [storage]
        storage.kids = [storage]
        ole = impl.OleFileIO()
        ole.root = root
        self.assertEqual(ole.listdir(storages=True), [['storage']])
        self.assertTrue(ole.parsing_issues)

    def test_deep_tree_and_order(self):
        leaf = self.node('leaf', impl.STGTY_STREAM)
        names = ['s%d' % i for i in range(1100)]
        tree = leaf
        for name in reversed(names):
            tree = self.node(name, impl.STGTY_STORAGE, [tree])
        ole = impl.OleFileIO()
        ole.root = self.node('root', impl.STGTY_ROOT, [tree, self.node('last', impl.STGTY_STREAM)])
        self.assertEqual(ole.listdir(), [names + ['leaf'], ['last']])

    def test_unicode_property_length_comes_from_count(self):
        ole = impl.OleFileIO()
        data = struct.pack('<I', 3) + 'Hi\0'.encode('utf-16le')
        value, size = ole._parse_property_basic(data, 0, 2, impl.VT_LPWSTR, False, [])
        self.assertEqual(value, 'Hi\0')
        self.assertEqual(size, len(data))


    def test_root_is_marked_used_before_children_are_loaded(self):
        import io
        ole = impl.OleFileIO()
        root = directory_entry()
        root.olefile = ole
        root.sid, root.name = 0, 'Root Entry'
        root.sid_child, root.sid_left, root.sid_right = 0, impl.NOSTREAM, impl.NOSTREAM
        root.entry_type, root.used = impl.STGTY_ROOT, False
        root.kids, root.kids_dict = [], {}
        class DirectoryStream(io.BytesIO):
            size = 128
        ole._open = lambda *args, **kwargs: DirectoryStream(b'x' * 128)
        def load(sid):
            ole.direntries[sid] = root
            return root
        ole._load_direntry = load
        ole.loaddirectory(0)
        self.assertTrue(root.used)
        self.assertEqual(root.kids, [])
        self.assertTrue(ole.parsing_issues)

class TestPublicErrorsAndInterrupts(unittest.TestCase):
    def test_public_errors_are_same_classes(self):
        import olefile
        self.assertIs(olefile.OleFileError, impl.OleFileError)
        self.assertIs(olefile.NotOleFileError, impl.NotOleFileError)
        self.assertTrue(issubclass(olefile.NotOleFileError, olefile.OleFileError))
        self.assertTrue(issubclass(olefile.OleFileError, IOError))

    def property_stream(self, kind=impl.VT_UI4, payload=None):
        import io
        if payload is None:
            payload = struct.pack('<I', 42)
        # PropertySetStream header, one section, one property at offset 16.
        section = struct.pack('<IIII', 20 + len(payload), 1, 2, 16)
        section += struct.pack('<I', kind) + payload
        return io.BytesIO(b'\0' * 24 + struct.pack('<I', 1) +
                          b'\0' * 16 + struct.pack('<I', 48) + section)

    def test_codepage_is_unsigned_and_other_i2_properties_stay_signed(self):
        for value in (1252, 65001):
            data = struct.pack('<HH', value, 0)
            ole = impl.OleFileIO()
            self.assertEqual(ole._parse_property_basic(data, 0, 1, impl.VT_I2, False, []),
                             (value, 2))
            expected = value - 65536 if value >= 32768 else value
            self.assertEqual(ole._parse_property_basic(data, 0, 2, impl.VT_I2, False, []),
                             (expected, 2))

    def test_property_value_interrupts_propagate(self):
        for exception in (KeyboardInterrupt, SystemExit):
            ole = impl.OleFileIO()
            ole.openstream = lambda filename: self.property_stream()
            def interrupt(*args):
                raise exception('stop')
            ole._parse_property = interrupt
            with self.assertRaises(exception):
                ole.getproperties('metadata')

    def test_property_header_interrupts_propagate(self):
        for exception in (KeyboardInterrupt, SystemExit):
            class InterruptedStream(object):
                def read(self, *args):
                    raise exception('stop')
            ole = impl.OleFileIO()
            ole.openstream = lambda filename: InterruptedStream()
            with self.assertRaises(exception):
                ole.getproperties('metadata')

    def test_userdefined_section_interrupts_propagate(self):
        for exception in (KeyboardInterrupt, SystemExit):
            class InterruptedStream(object):
                def __init__(self):
                    self.first = True
                def read(self, *args):
                    if self.first:
                        self.first = False
                        return b'\0' * 24 + struct.pack('<I', 1)
                    raise exception('stop')
            ole = impl.OleFileIO()
            ole.openstream = lambda filename: InterruptedStream()
            with self.assertRaises(exception):
                ole.get_userdefined_properties('metadata')

    def test_recoverable_property_errors_still_reported(self):
        ole = impl.OleFileIO()
        ole.openstream = lambda filename: self.property_stream()
        def invalid(*args):
            raise ValueError('invalid property')
        ole._parse_property = invalid
        self.assertEqual(ole.getproperties('metadata'), {})
        self.assertTrue(ole.parsing_issues)

    def test_getproperties_recovers_from_huge_vector(self):
        ole = impl.OleFileIO()
        ole.openstream = lambda filename: self.property_stream(
            impl.VT_VECTOR | impl.VT_EMPTY, struct.pack('<I', 0xffffffff))
        self.assertEqual(ole.getproperties('metadata'), {})
        self.assertTrue(ole.parsing_issues)

    def test_valid_property_unchanged(self):
        ole = impl.OleFileIO()
        ole.openstream = lambda filename: self.property_stream()
        self.assertEqual(ole.getproperties('metadata'), {2: 42})


class TestEmptyStreamWrites(unittest.TestCase):
    def setUp(self):
        self.ole = impl.OleFileIO()
        self.entry = directory_entry()
        self.entry.entry_type = impl.STGTY_STREAM
        self.entry.size = 0
        self.ole.direntries = [self.entry]
        self.ole._find = lambda name: 0

    def test_empty_write_requires_no_minifat_or_sector_chain(self):
        self.assertIsNone(self.ole.write_stream('empty', b''))
        self.assertIsNone(self.ole.minifat)

    def test_empty_stream_cannot_be_extended(self):
        with self.assertRaises(ValueError):
            self.ole.write_stream('empty', b'x')

    def test_empty_write_still_requires_bytes(self):
        with self.assertRaises(TypeError):
            self.ole.write_stream('empty', None)


class TestStreamLimits(unittest.TestCase):
    def make_stream(self, size, fat, strict=False):
        import io
        class ReadBudget(io.BytesIO):
            reads = 0
            def seek(self, *args):
                if self.reads >= 3:
                    raise IOError('synthetic read budget exhausted')
                return io.BytesIO.seek(self, *args)
            def read(self, *args):
                self.reads += 1
                return io.BytesIO.read(self, *args)
        fp = ReadBudget(b'abcdwxyz')
        ole = impl.OleFileIO(raise_defects=impl.DEFECT_INCORRECT if strict else impl.DEFECT_FATAL)
        ole.fp = fp
        stream = impl.OleStream(fp, 0, size, 0, 4, fat, 8, ole)
        return stream, fp, ole

    def test_oversized_cyclic_stream_is_bounded_and_salvaged(self):
        stream, fp, ole = self.make_stream(1024, [0])
        self.assertEqual(fp.reads, 1)
        self.assertEqual(stream.getvalue(), b'abcd')
        self.assertEqual(stream.size, 4)
        self.assertTrue(ole.parsing_issues)

    def test_oversized_stream_preserves_available_data(self):
        stream, fp, ole = self.make_stream(1024, [1, impl.ENDOFCHAIN])
        self.assertEqual(stream.read(), b'abcdwxyz')
        self.assertEqual(stream.size, 8)
        self.assertEqual(fp.reads, 2)

    def test_strict_parser_rejects_oversized_stream(self):
        with self.assertRaises(impl.OleFileError):
            self.make_stream(1024, [0], strict=True)

    def test_sector_array_errors_use_public_exception(self):
        ole = impl.OleFileIO()
        for data in (b'x', b'xx', b'xxx'):
            with self.assertRaises(impl.OleFileError):
                ole.sect2array(data)
        for data in (struct.pack('<II', 17, 23), array.array(impl.UINT32, [17, 23])):
            self.assertEqual(list(ole.sect2array(data)), [17, 23])


class TestMetadataPropertyIds(unittest.TestCase):
    def test_document_summary_reserved_id_does_not_shift_values(self):
        class Properties(object):
            def exists(self, name):
                return name == '\x05DocumentSummaryInformation'
            def getproperties(self, name, **kwargs):
                return {0x12: 'legacy-unused', 0x18: 'signature', 0x19: 'reserved',
                        0x1a: 'content', 0x1b: 'status', 0x1c: 'language', 0x1d: 'version'}
        metadata = impl.OleMetadata()
        metadata.parse_properties(Properties())
        self.assertEqual(metadata.unused, 'legacy-unused')
        self.assertEqual(metadata.dig_sig, 'signature')
        self.assertEqual(metadata.content_type, 'content')
        self.assertEqual(metadata.content_status, 'status')
        self.assertEqual(metadata.language, 'language')
        self.assertEqual(metadata.doc_version, 'version')
