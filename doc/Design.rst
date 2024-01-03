=====================================
Design Notes (for olefile developers)
=====================================

This page provides useful information about the internal design of olefile,
for olefile developers and contributors.

OLE file structure
------------------

An OLE file contains the following elements:

- Header
- FAT
- DIFAT
- miniFAT
- Directory
- Streams
- Mini streams

Header
------

TODO

Sectors
-------

An OLE file is organized in sectors of fixed size, which is either 512 bytes (the most common case)
or 4096 bytes. The size of an OLE file is always a multiple of the sector size.

In olefile, the sector size is stored in **OleFileIO.sector_size**.

The first sector of the file (at offset 0) contains the header and the beginning of the FAT.
The second sector has the index 0. To compute the offset of a sector in the file from its index,
the formula is offset = (index + 1)*sector_size.

olefile provides the methods **OleFileIO.getsect()** and **OleFileIO.write_sect()** to read and to write
sectors in the file.

FAT
---

The FAT (File Allocation Table) is used to link sectors together in a set of chains, in
order to build streams of data.

The FAT is simply an array of integers (32 bits). Each item of the FAT represents a sector in the OLE file.
The first item corresponds to the sector with index 0, the second item is sector 1, etc.
The value of each integer is the index of the next sector in the chain.
Each chain of sectors contains the data of a stream.

Some FAT entries may have special values:

- -1 (olefile.FREESECT): unused sector
- -2 (olefile.ENDOFCHAIN): last sector of a stream
- -3 (olefile.FATSECT): FAT sector
- -4 (olefile.DIFSECT): DIFAT sector

In olefile, the FAT is stored in the attribute **OleFileIO.fat**, which is an array of integers
(array.array(UINT32)). This is more effective than a list.

The number of sectors used in the FAT is stored in **OleFileIO.num_fat_sectors**.

The FAT is parsed and loaded by the method **OleFileIO.loadfat()**, called at the end of OleFileIO.open().

For debugging purposes, OleFileIO.dumpfat() can print the FAT content on the console.

Reference: [MS-CFB] section 2.3

DIFAT
-----

The Double-Indirected FAT (DIFAT) is a chain of sectors which contain the indexes of all the FAT sectors.
The DIFAT can be seen as an array of 32-bits integers. Each integer is the index of a FAT sector.

The beginning of the DIFAT is stored right after the OLE header, from the byte with offset 76 to offset 511.
Those bytes contain the 109 first items of the DIFAT (76+4*109 = 512).

For an OLE file up to 6.8MB (with sectors of 512 bytes), 109 sectors is enough to store the whole FAT
(109 * 512/4 * 512 = 6.8MB). For larger files, additional sectors are used to extend the DIFAT.
Each DIFAT sector is an array of 32-bits integers, in which each item is the index of a FAT sector.
The last item in a DIFAT sector is the index of the next DIFAT sector.

In olefile, the number of additional DIFAT sectors is stored in **OleFileIO.num_difat_sectors**.
If the file is larger than 6.8MB, then num_difat_sectors>0, and the index of the first DIFAT sector
is stored in **OleFileIO.first_difat_sector**.

The DIFAT and the FAT are parsed and loaded by the method **OleFileIO.loadfat()**,
called at the end of OleFileIO.open().
loadfat calls loadfat_sect() to parse each sector of the DIFAT, which calls sect2array to convert sector
data to an array of integers.

In the current version of olefile, the DIFAT is *NOT* stored in OleFileIO.

Reference: [MS-CFB] section 2.5

