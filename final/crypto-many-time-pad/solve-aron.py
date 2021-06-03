# The encrypted string as given by the server
encrypted_flag = bytes.fromhex("e1d402b76665d82a994c1adf0809c7ba0d0c644d1cfe805e789ed183ffeee1a41fcb")
# print(len(encrypted_flag))

# TODO Connect to the server remotely
sin = open("sin", "wb")
sout = open("sout", "rb")

test = "a" * len(encrypted_flag)
#print(test)

sin.write(b"2\n")
sin.flush()

for line in sout:
    if line.startswith(b"3:"):
        break

sin.write(test.encode() + b"\n")
sin.flush()

encrypted_test = bytes.fromhex(sout.readline().split(b"Your message: ")[1][:-1].decode())
key = [a^b for a,b in zip(list(encrypted_test), list(test.encode()))]
#print(bytes(key))

decrypted_flag = [a^b for a,b in zip(list(encrypted_flag),list(key))]
print(bytes(decrypted_flag))
