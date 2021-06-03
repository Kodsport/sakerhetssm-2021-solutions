from pwn import *

r = remote("localhost",50000)

r.recvuntil("? ")
r.sendline("1")
enc_flag = bytes.fromhex(r.recvline().decode())
r.recvuntil("? ")
r.sendline("2")
r.recvuntil(": ")
r.sendline("A"*256)
enc_msg = bytes.fromhex(r.recvline().decode())

for a,b in zip(list(enc_msg),list(enc_flag)):
    print(chr(a^b^ord('A')), end="")






