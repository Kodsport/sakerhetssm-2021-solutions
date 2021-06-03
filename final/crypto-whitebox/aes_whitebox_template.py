#!/usr/bin/env python3

import itertools
import sys
import secrets
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

class Encryptor:
    tables = %s

    def encrypt(self, plaintext):
        self.plain_state = [[x for x in plaintext[4*i:4*(i+1)]] for i in range(4)]

        for i in range(9):
            self.__round_encrypt(self.plain_state, self.tables[i])

        self.__apply_table(self.plain_state, self.tables[9])
        self.__shift_rows(self.plain_state)
        self.__apply_table(self.plain_state, self.tables[10])

        return bytes(itertools.chain(*self.plain_state))


    def __apply_table(self, state_matrix, table):
        for i in range(4):
            for j in range(4):
                state_matrix[i][j] = table[i*4+j][state_matrix[i][j]]

    def __round_encrypt(self, state_matrix, table):
        self.__apply_table(state_matrix, table)
        self.__shift_rows(state_matrix)
        self.__mix_columns(state_matrix)


    def __shift_rows(self, s):
        s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


    def __mix_single_column(self, a):
        t = a[0] ^ a[1] ^ a[2] ^ a[3]
        u = a[0]
        a[0] ^= t ^ xtime(a[0] ^ a[1])
        a[1] ^= t ^ xtime(a[1] ^ a[2])
        a[2] ^= t ^ xtime(a[2] ^ a[3])
        a[3] ^= t ^ xtime(a[3] ^ u)


    def __mix_columns(self, s):
        for i in range(4):
            self.__mix_single_column(s[i])

if __name__ == '__main__':
    plaintext = sys.stdin.buffer.read()
    if len(plaintext) %% 16 == 0:
        plaintext += b'\x10'*16
    else:
        pad_amount = 16-(len(plaintext) %% 16)
        plaintext += bytes([pad_amount]*pad_amount)
    enc = Encryptor()

    prev = secrets.token_bytes(16)
    sys.stdout.write(prev.hex())
    for i in range(0, len(plaintext), 16):
        cur = enc.encrypt(bytes(x^y for x,y in zip(prev, plaintext[i:i+16])))
        sys.stdout.write(cur.hex())
        prev = cur
