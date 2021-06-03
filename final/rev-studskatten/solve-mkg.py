import string, sys

enc_flag = [(0, 'a'),

            (2, 'm'),
            (3, 'n'),
            (4, 'a'),
            (5, 'l'),
            (6, 'f'),
            (7, 'h'),
            (8, 'b'),
            (9, 'k'),
            (10, 'm'),
            (11, 'k'),
            (12, 'x'),
            (13, 'u'),

            (15, 'd'),
            (16, 'p'),
            
            (18, 'm'),
            (19, 's'),
            (20, 'x'),
            (21, 'e'),
            (22, 'x'),
            (23, 'j'),
            (24, 'u'),

            (26, 'p'),
            (27, 's'),
            (28, 's')]

def encrypt(i, l, c):
    if i%l == 1:
        c = 'w'
    p = i
    p = (p+5)%l
    p = (p*7)%l
    p = pow(p, 3, l)

    cc = chr(((ord(c) - ord("a") + p) % 26) + ord("a"))

    p = (p+3)%l
    p = (p*11)%l
    p = pow(p, 5, l)
    return (p, cc)

assert encrypt(1, 5, 'a') == (1, 'z')
assert encrypt(2, 5, 'b') == (2, 'f')
assert encrypt(3, 5, 'c') == (4, 'd')
assert encrypt(4, 5, 'd') == (0, 'f')
assert encrypt(5, 5, 'e') == (3, 'e')

# zzbxy
# fzfed

d = {}
for l in range(20, 60):
    print("l:", l)
    for i in range(1, l+1):
        for c in string.ascii_lowercase:
            p, cc = encrypt(i, l, c)
            if (p, cc) not in d:
                d[(p, cc)] = []
            d[(p, cc)].append((l, i, c))

#print(d)
print(len(d))

flag = []
for t in enc_flag:
    if t not in d:
        print("PANIC")
        sys.exit()
    flag.append(d[t])

for l in range(20, 60):
    good = True
    for v in flag:
        good = good and any([ll == l for (ll, ii, cc) in v])
        if not good:
            break
    if not good:
        continue
    print("cand:", l)
    x = []
    for v in flag:
        y = [(ll,ii,cc) for (ll,ii,cc) in v if ll == l]
        assert len(y) == 1 or y[0][1] == 1, y
        x.append((y[0][1], y[0][2]))
    x.sort()
    x = ''.join([y[1] for y in x])
    print(x)

print("done")
