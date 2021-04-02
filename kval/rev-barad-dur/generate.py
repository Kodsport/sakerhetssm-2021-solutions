#!/usr/bin/env python3

import struct
from Crypto.Cipher import ARC4

FLAG = 'SSM{I_4m_n0_mAn!!}'
rc4_key = "You fool! No man can kill me!\n"

target = bytearray(FLAG.encode('ascii'))
"""
for(size_t idx = 0; idx < input_len; idx++) {
    input[idx] = (input[idx] << 4) | (input[idx] >> 4);
}
"""
if len(target) % 2 == 1:
    target.append(b'\0')
for i in range(0, len(target)):
    target[i] = ((target[i] << 4) & 0xFF) | (target[i] >> 4)

"""
unsigned char x = 0x13;
unsigned char y = 0x37;
for(size_t idx = 0; idx < (input_len+2-1)/2; idx++) {
    input[2*idx] ^= x;
    input[2*idx+1] ^= y;
    y = input[2*idx+1];
    x = input[2*idx];
}
"""
x = 0x13
y = 0x37
for idx in range(0, len(target), 2):
    target[idx] ^= x
    target[idx+1] ^= y
    y = target[idx+1]
    x = target[idx]


"""
RC4(msg, strlen(msg), input, input, 2*((input_len+2-1)/2));
"""
arc4 = ARC4.new(rc4_key.encode('ascii'))
target = arc4.encrypt(target)

print("""
#include <stddef.h>

unsigned char TARGET[] = { %s };
size_t TARGET_LEN = %d;
""".strip() % (', '.join(str(x) for x in target), len(target)))
