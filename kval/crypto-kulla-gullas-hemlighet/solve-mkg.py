#!/bin/env python3
import sys

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
n = 2
ciphertext = "TQNHCAREVUTRJTIÄKZJÖAUJXBVKWFÅLHBEKA"
ciphertext = [alphabet.index(x) for x in ciphertext]
print(ciphertext)

# MVHKG
knownp = [alphabet.index(x) for x in "VHKG"]
def decrypt(key):
    if dec(ciphertext[-2:], key) != knownp[2:] or dec(ciphertext[-4:-2], key) != knownp[:2]:
        return None, False
    flag = []
    for i in range(0, len(ciphertext), 2):
        flag += dec(ciphertext[i:i+2], key)
    return flag, True

def dec(cc, key):
    res = []
    for r in range(n):
        t = 0
        for c in range(n):
            t = (t + key[r][c]*cc[c]) % mod
        res.append(t)
    return res


mod = len(alphabet)
print(mod, pow(mod, 4))
for a in range(mod):
    print(a, mod)
    for b in range(mod):
        for c in range(mod):
            for d in range(mod):
                key = [[a,b],[c,d]]
                flag, correct = decrypt(key)
                if correct:
                    #print("YES")
                    #print(key)
                    #print(flag)
                    print(''.join([alphabet[x] for x in flag]))
                    #sys.exit(0)
