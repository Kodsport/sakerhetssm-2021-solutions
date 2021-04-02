from sympy.ntheory.modular import crt
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

def num2txt(num):
	return bytearray.fromhex(hex(num)[2:]).decode()

names = ["alice", "bob", "carol"]

pubs = []

for name in names:
	f = open("public_keys/" + name + ".pub", "r")
	key = RSA.import_key(f.read())
	f.close()
	pubs.append((key.n, key.e))

encrypted = []

for name in names:
	f = open("messages/" + name + ".txt", "r")
	encrypted.append(int(f.read(), base=16))
	f.close()

# use the chinese remainder theorem to extract the message
x = crt([n for (n,e) in pubs], encrypted)[0]
m = nth_root(x, 3)
print(num2txt(m))
