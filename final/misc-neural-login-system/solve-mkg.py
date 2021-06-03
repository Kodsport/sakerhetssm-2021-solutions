import torch

alphabet = b"SM{abcdefghijklmnopqrstuvwxyz1234567890_}"
flagsize = 30

def text_to_tensor(txt):
    alphabet = "SM{abcdefghijklmnopqrstuvwxyz1234567890_}"
    txt.ljust(flagsize)
    t = torch.zeros((len(txt),len(alphabet)))
    for i in range(len(txt)):
        t[i][alphabet.index(txt[i])] = 1
    #print("SHAPE", t.shape)
    #print(t)
    #print()
    return t.flatten()

model = torch.load("model")

model = model[:-1]

print(model)
print(type(model))
print(model[0])

import sys

print()

password = bytearray(b"_"*flagsize)

#ylist = []
for pos in range(flagsize):
    val = -1000000.0
    cc = ' '
    for c in alphabet:
        password[pos] = c
        x = text_to_tensor(password.decode())
        res = model(x)
        #print(c, res)
        #ylist.append(res.item())
        if res > val:
            val = res
            cc = c
    if cc == ' ':
        print("PANIC")
    password[pos] = cc

print(repr(password))

'''
import matplotlib.pyplot as plt

plt.plot(list(range(41)), ylist)
plt.show()
'''

'''
t1 = torch.ones((flagsize, len(alphabet)))
res = model(t1.flatten())
res = res[0].item()
print("%.60g" % res)


print()

xx = model[0](t1.flatten())
print(xx)
'''
