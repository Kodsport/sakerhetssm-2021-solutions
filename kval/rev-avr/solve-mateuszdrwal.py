import binascii
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


encrypted = binascii.unhexlify(
    "bbbbae6f3edebe796749de216779f0de8d79f0de4979de47eba4deb71149defb0859de3e0ade4b592d4949c1de0a3e034b6c2d76"
)
eeprom = intelhex.IntelHex("eeprom.hex").tobinarray()

unxored = [i ^ 69 for i in encrypted]

unsubstituted = [eeprom.index(i) for i in unxored]

all_shuffled = [shuffle_bits(i) for i in range(256)]

unshuffled = [all_shuffled.index(i) for i in unsubstituted]

print(bytes(unshuffled).decode())