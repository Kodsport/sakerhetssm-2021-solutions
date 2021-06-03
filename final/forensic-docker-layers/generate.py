import hashlib
from pathlib import Path
flag = b'SSM{d0ck3r_15_n07_4lw4y5_54f3!!}'
path = Path("container-files/")
key = hashlib.md5((path/Path("password.txt")).read_bytes()).digest()*2
assert len(flag) == len(key)
enc = bytes(bytearray([i ^ j for i, j in zip(key, flag)]))
(path/Path("enc.txt")).write_bytes(enc)
