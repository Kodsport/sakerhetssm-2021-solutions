import random
import intelhex

eeprom = list(range(256))
random.shuffle(eeprom)

with open("eeprom.hex", "w") as f:
    ih = intelhex.IntelHex()
    ih.frombytes(eeprom)
    ih.write_hex_file(f)