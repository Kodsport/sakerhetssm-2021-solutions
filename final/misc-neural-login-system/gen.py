import torch
import random

alphabet = "SM{abcdefghijklmnopqrstuvwxyz1234567890_}"
flag = "SSM{neural_login_87e9465S0So7}"

def text_to_tensor(txt):
    txt.ljust(len(flag))
    t = torch.zeros((len(txt),len(alphabet)))
    for i in range(len(txt)):
        t[i][alphabet.index(txt[i])] = 1
    return t.flatten()


X_txt = []
for i in range(500):
    X_txt.append(flag)

for i in range(len(flag)):
    for k in range(len(alphabet)):
        f = list(flag[:])
        f[i]=alphabet[k]
        X_txt.append("".join(f))

for i in range(500):
    X_txt.append("".join([alphabet[random.randint(0,len(alphabet)-1)] for _ in range(len(flag))]))

X = torch.stack([text_to_tensor(x) for x in X_txt])
Y = torch.tensor([x==flag for x in X_txt]).type(torch.float32)


model = torch.nn.Sequential(
    torch.nn.Linear(len(X[0]),200),
    torch.nn.ReLU(),
    torch.nn.Linear(200,200),
    torch.nn.ReLU(),
    torch.nn.Linear(200,1),
    torch.nn.Sigmoid(),
)
loss = torch.nn.BCELoss()
print(X.shape)
print(Y.shape)

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
for epoch in range(500):
    l = loss(model(X)[:,0],Y)
    if epoch%100==0:
        print(l)
    optimizer.zero_grad()
    l.backward()
    optimizer.step()

torch.save(model,"model")
