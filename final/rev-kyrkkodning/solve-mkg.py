import sys
sys.setrecursionlimit(100000000)

A = lambda x: lambda y: x
B = lambda x: lambda y: y
C = lambda a: lambda x: lambda y: a(y)(x)

D = lambda a: lambda b: a(A)(b)
E = lambda a: lambda b: a(b)(B)

F = lambda a: lambda b: lambda z: z(a)(b)
G = lambda num: lambda f: lambda x: num(f)(f(x)) 

H = lambda f: lambda x: x

I = G(H)
J = G(I)
K = G(J)
L = G(K)

M = lambda num: num(lambda p: F(G(p(A)))(p(A)))(F(H)(H))(B)
N = lambda numA: lambda numB: lambda f: lambda x: numA(f)(numB(f)(x))

O = lambda numA: lambda numB: numB(M)(numA)
P = lambda numA: lambda numB: lambda f: numA(numB(f))
Q = lambda numA: lambda numB: numB(numA)
R = lambda x: P(x)(x)
S = lambda num: num(lambda ign: A)(B)

T = lambda numA: lambda numB: D(S(O(numA)(numB)))(S(O(numB)(numA)))

U = lambda f: lambda x: x
V = lambda head: lambda tail: lambda f: lambda x: tail(f)(f(head)(x))
W = lambda num: H if num==0 else G(W(num-1))

X = lambda l: U if l==[] else V(W(l[-1]))(X(l[:-1]))
#Y = X([ord(c)-50 for c in input()])

Z = lambda l: lambda x: l(lambda hd:lambda transtl:F(N(transtl(A))(P(transtl(B))(hd)))(M(transtl(B))))(F(H)(x))(A)

# T(Z(Y)(AAAA))(BBBB)(False)(True)

values = [
    (I, N(Q(K)(K))(N(Q(K)(K))(N(Q(L)(J))(N(P(J)(J))(I))))),
    (J, N(Q(N(P(J)(K))(I))(J))(N(Q(J)(N(P(K)(J))(I)))(N(Q(K)(K))(P(N(P(J)(J))(I))(J))))),
    (K, N(Q(N(P(J)(K))(I))(K))(N(P(J)(N(P(J)(J))(I)))(I))),
    (L, N(Q(N(P(J)(L))(I))(J))(N(Q(P(J)(N(P(J)(J))(I)))(J))(N(Q(P(K)(J))(K))(N(Q(K)(L))(N(Q(K)(L))(I)))))),
    (N(P(J)(J))(I), N(Q(N(P(K)(J))(I))(K))(N(Q(P(K)(J))(K))(N(Q(P(J)(L))(J))(N(Q(N(P(J)(J))(I))(K))(N(Q(K)(L))(J)))))),
    (P(J)(K), N(Q(N(P(J)(K))(I))(K))(N(Q(P(K)(J))(K))(N(Q(N(P(L)(J))(I))(J))(N(Q(P(N(P(J)(J))(I))(J))(J))(N(Q(N(P(K)(J))(I))(K))(N(Q(J)(L))(N(P(J)(J))(I)))))))),
    (N(P(K)(J))(I), N(Q(P(K)(J))(L))(N(Q(K)(L))(N(Q(K)(K))(N(Q(K)(K))(N(P(J)(J))(I)))))),
    (P(L)(J), N(Q(N(P(J)(L))(I))(K))(N(Q(P(L)(J))(K))(N(Q(P(J)(L))(K))(N(Q(L)(J))(N(Q(L)(J))(N(Q(L)(J))(P(K)(L)))))))),
    (N(P(L)(J))(I), N(Q(N(P(L)(J))(I))(K))(N(Q(P(K)(J))(L))(N(Q(J)(N(P(K)(J))(I)))(N(Q(J)(N(P(J)(J))(I)))(N(P(J)(K))(I)))))),
    (N(P(L)(J))(J), N(Q(P(K)(J))(L))(N(Q(N(P(J)(K))(I))(K))(N(Q(N(P(J)(J))(I))(L))(N(Q(N(P(J)(K))(I))(K))(N(P(K)(L))(J)))))),
    (N(P(K)(K))(J), N(Q(N(P(K)(J))(J))(K))(N(Q(N(P(J)(J))(I))(L))(N(Q(P(J)(N(P(J)(J))(I)))(K))(N(Q(N(P(K)(K))(I))(J))(N(Q(P(K)(K))(K))(N(Q(K)(L))(N(Q(J)(N(P(J)(J))(I)))(N(Q(J)(L))(K))))))))),
    (P(K)(L), N(Q(N(P(J)(K))(I))(L))(N(Q(N(P(K)(J))(I))(K))(N(Q(N(P(J)(K))(I))(K))(N(Q(N(P(J)(J))(I))(K))(N(Q(N(P(K)(J))(J))(J))(N(Q(P(K)(K))(J))(N(Q(N(P(J)(J))(I))(K))(N(Q(J)(N(P(J)(K))(I)))(N(Q(J)(L))(N(P(K)(J))(J))))))))))),
    (N(P(N(P(J)(J))(I))(J))(K), N(Q(N(P(K)(J))(J))(L))(N(Q(K)(K))(N(Q(J)(N(P(J)(J))(I)))(N(Q(L)(J))(I))))),
    (N(P(N(P(J)(J))(I))(J))(L), N(Q(N(P(J)(L))(I))(K))(N(Q(N(P(K)(J))(J))(K))(N(Q(P(K)(J))(L))(N(Q(P(J)(N(P(J)(J))(I)))(K))(N(Q(P(K)(J))(K))(N(Q(P(N(P(J)(J))(I))(J))(K))(P(K)(N(P(J)(J))(I))))))))),
    (P(K)(N(P(J)(J))(I)), N(Q(N(P(J)(K))(I))(L))(N(Q(P(N(P(J)(J))(I))(J))(K))(N(Q(P(J)(N(P(J)(J))(I)))(K))(N(Q(N(P(L)(J))(I))(K))(N(Q(P(J)(L))(J))(N(Q(N(P(L)(J))(I))(J))(N(Q(K)(L))(N(Q(L)(K))(N(Q(K)(J))(P(L)(J))))))))))),
    (N(P(N(P(J)(J))(I))(K))(I), N(Q(P(J)(K))(L))(N(Q(P(L)(J))(L))(N(Q(P(J)(L))(K))(N(Q(P(K)(J))(K))(N(P(J)(P(K)(J)))(I)))))),
    (N(Q(J)(L))(I), N(Q(N(P(K)(J))(J))(L))(N(Q(P(J)(K))(L))(N(Q(P(K)(J))(L))(N(Q(J)(N(P(K)(J))(I)))(N(Q(K)(K))(N(Q(J)(L))(K))))))),
    (N(Q(J)(L))(J), N(Q(P(K)(K))(L))(N(Q(P(J)(K))(K))(N(Q(N(P(L)(J))(I))(K))(N(Q(J)(P(J)(K)))(N(Q(K)(K))(N(Q(L)(J))(N(P(L)(J))(K)))))))),
]

def addOne(x):
    return x+1

'''
Y = X([ord(c)-50 for c in "abcdefghijklmnopqr"])
for i in range(18):
    target = values[i][1](addOne)(0)
    x = Z(Y)(values[i][0])
    y = x(addOne)(0)
    print(y, target)

print("--------")
Y = X([ord(c)-50 for c in "mnopqr"])
for i in range(6):
    target = values[i][1](addOne)(0)
    x = Z(Y)(values[i][0])
    y = x(addOne)(0)
    print(y, target)
# we can bruteforce byte for byte from the end
'''

flag = ""
for (i, num) in enumerate(values):
    n = num[1](addOne)(0)
    good = False
    for j in range(50, 128):
        Y = X([ord(c)-50 for c in chr(j)+flag])
        x = Z(Y)(values[i][0])(addOne)(0)
        if x == n:
            flag = chr(j) + flag
            print(flag)
            good = True
            break
    if not good:
        print("PANIC")
        break

print(flag)
print("done")
