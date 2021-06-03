import itertools

carry = 0


def rol(r):
    global carry
    r = (r << 1) | carry
    carry = not r == r % 0x100
    return r % 0x100


def translate(r16, r17):
    r18 = 0
    loop = 0
    while True:
        if loop == 0:
            loop = 1
            if not r18 & (1 << 0):
                continue
            r16 = r16 ^ 0xFF

        if loop == 1:
            loop = 2
            if not r18 & (1 << 1):
                continue
            r17 = r17 ^ 0xFF

        if loop == 2:
            loop = 3
            if not r18 & (1 << 2):
                continue
            r16 = (r16 + 1) % 0x100

        if loop == 3:
            loop = 4
            if not r18 & (1 << 3):
                continue
            r17 = (r17 - 2) % 0x100

        if loop == 4:
            loop = 5
            if not r18 & (1 << 4):
                continue
            r16 = ((r16 << 4) % 0x100) | (r16 >> 4)

        if loop == 5:
            loop = 6
            if not r18 & (1 << 5):
                continue
            r16 = rol(r16)
            r16 = rol(r16)
            r16 = rol(r16)
            r16 = rol(r16)
            r17 = rol(r17)
            r17 = rol(r17)
            r17 = rol(r17)
            r17 = rol(r17)
            r16 = rol(r16)
            r16 = rol(r16)
            r16 = rol(r16)
            r16 = rol(r16)
            r16 = rol(r16)

            assert not carry

        if loop == 6:
            loop = 7
            if not r18 & (1 << 6):
                continue
            r16 = r16 ^ r17

        if loop == 7:
            loop = 8
            if not r18 & (1 << 7):
                continue
            r17 = ((r17 << 4) % 0x100) | (r17 >> 4)

        if loop == 8:
            r18 = (r18 + 1) % 0x100
            if not r18:
                break
            loop = 0

    return r16, r17


outputs = set()

for r16 in range(256):
    for r17 in range(256):
        output = translate(r16, r17)
        assert output not in outputs
        outputs.add(output)
        if output[0] == 0b01100101 and output[1] == 0b10011001:
            print(r16, r17)
