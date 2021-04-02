#!/usr/bin/env python3

import struct

FLAG = 'SSM{Y0ur_staff_1s_br0ken!}'

target = bytearray(FLAG.encode('ascii'))
"""
for(size_t idx = 0; idx < input_len; idx++) {
    input[idx] += 2*(idx+1);
}
"""
if len(target) % 2 == 1:
    target.append(b'\0')
for i in range(0, len(target)):
    target[i] += 2*(i+1)

"""
uint16_t *input2 = (uint16_t*)input;
for(size_t idx = 0; idx < (input_len+2-1)/2; idx++) {
    input2[idx] ^= 0x1337;
}
"""
for i in range(0, len(target), 2):
    target[i:i+2] = struct.pack('<H', 0x1337 ^ struct.unpack('<H', target[i:i+2])[0])

print("""
#include <stddef.h>

unsigned char TARGET[] = { %s };
size_t TARGET_LEN = %d;
""".strip() % (', '.join(str(x) for x in target), len(target)))
