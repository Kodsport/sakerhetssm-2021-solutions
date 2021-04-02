import binascii

def stage1(target):
    for i in range(len(target)-1):
        target[i+1] = ((target[i+1] << 4) | (target[i+1] >> 4)) & 0xff
    return target

def stage2(target):
    for i in range(0, len(target)-2, 2)[::-1]:
        varA = target[i + 1 - 2] if i + 1 - 2 >= 0 else 0x13
        varB = target[i + 2 - 2] if i + 2 - 2 != 0 else 0x37
        target[i + 1] ^= varA
        target[i + 2] ^= varB
    return target

def stage3(target):
    xor_stream = binascii.unhexlify(b'7c93e5ab666218c06b2af3ef93b412b39a67cb0e')
    for i in range(len(target)):
        target[i] = target[i] ^ xor_stream[i]
    return target

target = bytearray(binascii.unhexlify(b'5a91171e00223d56bb5a206a9625f1306b33'))
print(target)

target = stage3(target)
target = bytearray(b' ') + target
print(target)

target = stage2(target)
print(target)

target = stage1(target)
print(target)
