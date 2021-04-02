#!/usr/bin/env python3
import intelhex

ih = intelhex.IntelHex()
ih.fromfile('eeprom.hex', format='hex')

keymaskbits = {}
with open('firmware.asm', 'r') as fin:
    for line in fin:
        if line.strip().startswith('sbrc r16, '):
            testbit = int(line.strip().split('sbrc r16, ')[1])
            setbit = int(next(fin).strip().split('sbr r17, ')[1], 2)
            keymaskbits[testbit] = setbit

        if line.startswith('encrypted'):
            encrypted = [int(x, 16) for x in line.split('.DB')[1].strip().split(', ')]

# Build table to invert bit mixing of input
keymask = {}
for inval in range(256):
    addrval = 0
    for bit in range(8):
        if (inval>>bit)&1:
            addrval |= keymaskbits[bit]
    keymask[addrval] = inval
# Assert bijection
assert len(set(keymask.keys())) == 256
assert len(set(keymask.values())) == 256

# Build inverse EEPROM "S-box"
eeprom_inv = {}
for i in range(256):
    eeprom_inv[ih[i]] = i
# Assert bijection
assert len(set(eeprom_inv.keys())) == 256
assert len(set(eeprom_inv.values())) == 256

# Decrypt
flag = []
for c in encrypted:
    flag.append(keymask[eeprom_inv[c^69]])

print(bytes(flag).decode('ascii'))
