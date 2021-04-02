import sys
import intelhex


def shuffle_bits(addr):
    newaddr = 0
    newaddr |= (addr >> 0 & 1) << 4
    newaddr |= (addr >> 1 & 1) << 1
    newaddr |= (addr >> 2 & 1) << 5
    newaddr |= (addr >> 3 & 1) << 0
    newaddr |= (addr >> 4 & 1) << 2
    newaddr |= (addr >> 5 & 1) << 6
    newaddr |= (addr >> 6 & 1) << 7
    newaddr |= (addr >> 7 & 1) << 3
    return newaddr


flag = sys.argv[1].encode()
eeprom = intelhex.IntelHex("eeprom.hex").tobinarray()


shuffled = [shuffle_bits(i) for i in flag]

substituted = [eeprom[i] for i in shuffled]

xored = [i ^ 69 for i in substituted]

print(hex(flag[0]))
print(hex(shuffled[0]))
print(hex(substituted[0]))
print(hex(xored[0]))
print(bytes(xored).hex())
