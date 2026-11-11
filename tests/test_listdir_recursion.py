"""
Regression test for an unbounded-recursion DoS in OleFileIO._list()
(CWE-674 stack exhaustion) on a malformed OLE whose root directory entry is
its own child.

The root entry is loaded directly via _load_direntry(0) in loaddirectory() and
so never has its `used` flag set by append_kids(). A file whose root sid_child
points back to SID 0 therefore slips past the "referenced more than once" guard
in append_kids(): the root is appended to its own `kids` list, and because
_list() keeps no visited set it then recurses into the root forever.

This is the same class of bug as issue #103 ("olefile recurses infinitely while
opening a specific PowerPoint file"), whose fix added the `used` guard to
append_kids() but did not cover the directly-loaded root. With the root marked
`used` at load time, the existing guard rejects the self-reference, so
listdir() terminates instead of recursing.
"""
import struct
import sys

import olefile


def _self_referential_root_ole():
    """A minimal 1536-byte OLE2/CFBF file whose root entry, declared as a plain
    storage, names itself (SID 0) as its child."""
    SEC = 512
    NOSTREAM, EOC, FATSECT, FREE = 0xFFFFFFFF, 0xFFFFFFFE, 0xFFFFFFFD, 0xFFFFFFFF

    # header (512 bytes)
    h = bytearray(SEC)
    h[0:8] = bytes.fromhex("D0CF11E0A1B11AE1")  # CFBF magic
    struct.pack_into("<H", h, 24, 0x003E)   # minor version
    struct.pack_into("<H", h, 26, 0x0003)   # major version 3 (512-byte sectors)
    struct.pack_into("<H", h, 28, 0xFFFE)   # little-endian
    struct.pack_into("<H", h, 30, 0x0009)   # sector shift -> 512
    struct.pack_into("<H", h, 32, 0x0006)   # mini sector shift -> 64
    struct.pack_into("<I", h, 44, 1)          # 1 FAT sector
    struct.pack_into("<I", h, 48, 1)          # first directory sector = sector 1
    struct.pack_into("<I", h, 56, 0x1000)     # mini-stream cutoff
    struct.pack_into("<I", h, 60, EOC)        # first mini-FAT sector
    struct.pack_into("<I", h, 68, EOC)        # first DIFAT sector
    struct.pack_into("<I", h, 76, 0)          # DIFAT[0] -> FAT is sector 0
    for i in range(1, 109):
        struct.pack_into("<I", h, 76 + 4 * i, FREE)

    # FAT (sector 0)
    fat = bytearray(SEC)
    struct.pack_into("<I", fat, 0, FATSECT)   # sector 0 is the FAT
    struct.pack_into("<I", fat, 4, EOC)       # sector 1 (dir) ends its chain
    for i in range(2, 128):
        struct.pack_into("<I", fat, 4 * i, FREE)

    # directory (sector 1): entry 0 crafted, entries 1..3 empty
    d = bytearray(SEC)
    name = "Root Entry".encode("utf-16-le")
    d[0:len(name)] = name
    struct.pack_into("<H", d, 64, len(name) + 2)  # name length incl. null
    d[66] = 0x01                        # object type = STORAGE (so _list recurses)
    d[67] = 0x01                        # color = black
    struct.pack_into("<I", d, 68, NOSTREAM)   # left sibling
    struct.pack_into("<I", d, 72, NOSTREAM)   # right sibling
    struct.pack_into("<I", d, 76, 0)          # child SID = 0 (self-reference)
    struct.pack_into("<I", d, 116, EOC)       # starting sector
    return bytes(h) + bytes(fat) + bytes(d)


def test_listdir_self_referential_root_terminates(tmp_path):
    """listdir() must terminate on a self-referential root rather than recursing
    without bound. Before the fix this raises RecursionError; after it, listdir()
    returns normally (the root's self-reference is rejected, so it has no kids)."""
    path = tmp_path / "self_ref_root.ole"
    path.write_bytes(_self_referential_root_ole())

    # Bound the stack so a regression fails fast and contained instead of
    # thrashing; the fix makes the depth question moot.
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(500)
    try:
        ole = olefile.OleFileIO(str(path))   # default: non-fatal on malformed files
        try:
            entries = ole.listdir(streams=True, storages=True)
        finally:
            ole.close()
    finally:
        sys.setrecursionlimit(old_limit)

    assert entries == []


if __name__ == "__main__":
    import tempfile
    import pathlib
    with tempfile.TemporaryDirectory() as tmp:
        test_listdir_self_referential_root_terminates(pathlib.Path(tmp))
    print("PASS: listdir terminates on a self-referential root")
