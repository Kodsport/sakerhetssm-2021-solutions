#!/usr/bin/env python3

BYTES = 256

with open("key", "rb") as fin:
    key = fin.read()
with open("flag", "rb") as fin:
    flag = fin.read()


def encrypt(msg, key):
    return bytes([a^b for a,b in zip(list(msg),list(key))])


def main():
    while True:
        print("What do you want to do?")
        print("1: Get encrypted flag")
        print("2: Encrypt your own message")
        print("3: Exit")
        c = input("Choice? ")

        if c == "1":
            print(encrypt(flag,key).hex())
        elif c == "2":
            msg = input("Your message: ").encode()
            print(encrypt(msg,key).hex())
        else:
            return


if __name__ == "__main__":
    main()
