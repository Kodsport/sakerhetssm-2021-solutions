import base64
import string

# TODO Connect to the server remotely
sin = open("sin", "wb")
sout = open("sout", "rb")

for line in sout:
    if line.startswith(b"here is flag: "):
        # print(line)
        split = line.split(b"here is flag: ")
        flag_encoded = split[1]
        break

flag_encrypted = base64.b64decode(flag_encoded)
#print(flag_encrypted)
#print(len(flag_encrypted))

# valid input chars would be [a-zA-Z0-9{}-_]
# the server will only read 1000 requests before quitting,
# so comment/uncomment these and create subarrays to stay below the limit
chars = ""
chars += string.ascii_lowercase[14:]
#chars += string.ascii_uppercase
chars += string.digits
#chars += '-' + '_'
# print(chars)
# print((chars[0] + chars[0]).encode())
#print(len(chars))

T = [[bytearray(b"") for i in range(len(chars))] for j in range(len(chars))]

# build the "database" of encrypted char pairs
for i in range(0, len(chars)):
    for j in range(0, len(chars)):
        encoded = base64.b64encode((chars[i] + chars[j]).encode())
        # print(encoded)

        sin.write(encoded + b"\n")
        sin.flush()
        line = sout.readline()
        # print(line)
        split = line.split(b">")
        encrypted = base64.b64decode(split[1])
        # print(encrypted)
        T[i][j] = encrypted

for i in range(0, (int) (len(flag_encrypted) / 4)):
    part = flag_encrypted[i*4 : i*4 + 4]
    found = False
    for j in range(len(chars)):
        for k in range(len(chars)):
            if T[j][k] == part:
                print(chars[j] + chars[k])
                found = True
    if found == False:
        print("no match")
