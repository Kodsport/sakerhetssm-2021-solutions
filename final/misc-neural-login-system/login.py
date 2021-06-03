import torch

alphabet = "SM{abcdefghijklmnopqrstuvwxyz1234567890_}"
flagsize = 30

def text_to_tensor(txt):
    txt.ljust(flagsize)
    t = torch.zeros((len(txt),len(alphabet)))
    for i in range(len(txt)):
        t[i][alphabet.index(txt[i])] = 1
    return t.flatten()

model = torch.load("model")

print("What is the password?")
password = input()

if model(text_to_tensor(password))[0]>0.8:
    print("Yes! How???")
else:
    print("Wrong password. Haha!")