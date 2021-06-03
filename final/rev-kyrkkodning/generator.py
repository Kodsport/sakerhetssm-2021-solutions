import random

def gen_num(x):
    if x<5:
        return ["zero","one","two","three","four"][x]
    if x<17:
        f = random.randint(2,min(6,x//2))
        if x%f==0:
            return "mult({})({})".format(gen_num(f), gen_num(x//f))
        else:
            return "add(mult({})({}))({})".format(gen_num(f),gen_num(x//f),gen_num(x%f))
    if x>16:
        b = random.randint(2,4)
        if x>200:
            b = random.randint(5,10)
        ex = 0
        while b**(ex+1)<=x:
            ex+=1
        if b**ex==x:
            return "exp({})({})".format(gen_num(b), gen_num(ex))
        else:
            return "add(exp({})({}))({})".format(gen_num(b),gen_num(ex),gen_num(x-b**ex))

def suffix_thing(flag, p):
    ans = 0
    for i in range(p):
        ans += (ord(flag[-p+i])-50)*(i+1)
    return ans

flag = "SSM{l4mbd4_m4st3r}"


rows = []

for i in range(1,len(flag)+1):
    print(suffix_thing(flag,i))
    rows.append("print(numeq(secret(flag)({}))({})(False)(True))".format(gen_num(i),gen_num(suffix_thing(flag,i))))


print("\n".join(rows))