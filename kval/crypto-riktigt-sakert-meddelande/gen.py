import os
import sympy
from sympy.ntheory.modular import crt
import secrets
from Crypto.PublicKey import RSA

# https://stackoverflow.com/questions/356090/how-to-compute-the-nth-root-of-a-very-big-integer
def nth_root(x, n):
	high = 1
	while high ** n <= x:
		high *= 2
	low = high//2
	while low < high:
		mid = (low + high) // 2
		if low < mid and mid**n < x:
			low = mid
		elif high > mid and mid**n > x:
			high = mid
		else:
			return mid
	return mid + 1

def txt2num(text):
	text = text.encode('utf-8')
	num = 0
	for c in text:
		num = (num << 8) + c
	return num

def public_keys():
	e = 3
	p = sympy.nextprime(secrets.randbits(1024))
	q = sympy.nextprime(secrets.randbits(1024))
	n = p*q
	return (n,e)

pubs = [public_keys() for _ in range(3)]

flag = "Hejsan,\nHär kommer den superhemliga nyckeln. Dela den inte med någon annan!!!\nSSM{b3_c4refu1_w1th_e}"

encrypted = [pow(txt2num(flag), e, n) for (n, e) in pubs]

# assert that everything is correct
x = crt([n for (n,e) in pubs], encrypted)[0]
assert(nth_root(x, 3) == txt2num(flag))

keys = [RSA.construct((n, e)) for (n,e) in pubs]

names = ["alice", "bob", "carol"]

if not os.path.exists("public_keys/"):
	os.mkdir("public_keys/")
for i in range(len(names)):
	f = open("public_keys/" + names[i] + ".pub", "w")
	f.write(keys[i].export_key().decode("utf-8"))
	f.close()

if not os.path.exists("messages/"):
	os.mkdir("messages/")
for i in range(len(names)):
	f = open("messages/" + names[i] + ".txt", "w")
	f.write(hex(encrypted[i]))
	f.close()
