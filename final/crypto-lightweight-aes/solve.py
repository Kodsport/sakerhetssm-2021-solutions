from pwn import *
import base64, sys

r = remote("localhost", 50000)
r.readuntil("flag: ")
flag = base64.b64decode(r.readline())
print("flag", repr(flag))
r.close()

lookup = {}
i = 0
while i < 0x10000:
    r = remote("localhost", 50000)
    r.readuntil("flag:")
    print(i)
    for _ in range(1000):
        r.readuntil(">")
        b = bytes([i % 0x100, i//0x100])
        r.sendline(base64.b64encode(b))
        cc = r.readline()
        c = base64.b64decode(cc)
        if c in lookup:
            print("PANIC")
            sys.exit(0)
        lookup[c] = b
        i += 1
        if i >= 0x10000:
            break
    r.close()

print("LOOK", len(lookup))

chunksize = 4

f = b""
for i in range(0, len(flag), chunksize):
    f += lookup[flag[i:i+chunksize]]

print(f)

#r.interactive()
