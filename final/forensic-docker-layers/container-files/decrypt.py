import hashlib
from pathlib import Path
from sys import argv
enc_txt, key_txt = argv[1], argv[2]
enc = Path(enc_txt).read_bytes()
key = hashlib.md5(Path(key_txt).read_bytes()).digest()*2
assert len(enc) == len(key)
flag = ''.join([chr(i ^ j) for i, j in zip(key, enc)])
assert flag.startswith('SSM{')
print(flag)
