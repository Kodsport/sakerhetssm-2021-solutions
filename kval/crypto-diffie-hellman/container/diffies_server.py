#!/usr/bin/env python3
import sys
import random
from Crypto.Util.number import getPrime

BITS = 512

with open("secret", "r") as fin:
    secret = int(fin.read())


def decrypt(encrypted, shared_key):
    return (encrypted ^ shared_key).to_bytes(BITS//8, 'big').strip(b'\0').decode('utf-8')


def main():
    p = getPrime(BITS)
    print(f"p = {p}")
    g = random.randint(2, p-2)
    print(f"g = {g}")

    A = pow(g, secret, p)
    print(f"g^a mod p = {A}")

    B = int(input("g^b mod p = "))

    shared_key = pow(B, secret, p)

    encrypted = int(input("Encrypted message: "))
    decrypted = decrypt(encrypted, shared_key)


if __name__ == "__main__":
    main()
