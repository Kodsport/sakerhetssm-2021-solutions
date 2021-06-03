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

#print(model(text_to_tensor("SSM{hejsan1234}").reshape((1,-1))))
#print(model(text_to_tensor("SSM{hejs4n12a4}").reshape((1,-1))))
#print(model(text_to_tensor("asdsadasdasdasa").reshape((1,-1))))

inp = torch.nn.Parameter(torch.zeros(flagsize*len(alphabet)))
#inp = torch.nn.Parameter(text_to_tensor("SSM{fl4wl3ss_l0g1n_syst3m}"))
optimizer = torch.optim.Adam((inp,), lr=0.001)
for epoch in range(4000):
    rinp = inp.reshape((flagsize,-1))

    a = (1-model(inp)[0])**2
    
    l = a
    if epoch%50==0:
        #print(a.detach().numpy(),c.detach().numpy(),d.detach().numpy())
        a = inp.reshape((flagsize,-1))
        print(l)
        s = [alphabet[ai] for ai in a.argmax(dim=1).tolist()]
        print("".join(s))
        
    optimizer.zero_grad()
    l.backward()
    optimizer.step()
