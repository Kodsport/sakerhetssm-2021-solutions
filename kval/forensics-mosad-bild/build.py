#!/usr/bin/env python3

import struct
import zlib

with open('original.png', 'rb') as fin:
    data = bytearray(fin.read())

data[0x10:0x14] = struct.pack('>I', 0)
data[0x14:0x18] = struct.pack('>I', 0)
data[0x1D:0x21] = struct.pack('>I', (zlib.crc32(data[0x0C:0x1D])) & 0xFFFFFFFF)

with open('mosad.png', 'wb') as fout:
    fout.write(data)
