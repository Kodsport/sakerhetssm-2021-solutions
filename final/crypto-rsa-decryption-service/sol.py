from pwn import *
from sympy.core.numbers import mod_inverse

n = 2067870294958011057055285955402906046606048790411055875169573453537686332172209267408004747919606628058370206526960367880892445668185569509285031022814760278300660074538992941238982588619494964193409210892923688858242586013830561156541927776274966180885997095053592128354967440372151112352802070424021271867709873
e = 65537
c = 830144780125940486197043594519402775647010555742811842359207814917520372239224390038268506983945590914017447501759733518435739075026545060636422666418129968749711859639488111365290895840446401503036619441634142308550050624037073448524383606576227140182555712049129024301943559994704154884416671330162459299359164


def f(c):
    r = remote("localhost",50000)
    r.recvuntil("): ")
    r.sendline(str(c))
    r.recvline()
    res = r.recvline().decode()
    print(res)
    r.close()
    return int(res[-5:-1])

pa = 0
ans = 0
inv = 1
for i in range(60):
    ans += 10000**i*((f(c*pow(inv,e,n))-(ans*inv)%n)%10000)
    inv*=mod_inverse(10000,n)
    print(ans)
    #print(chr(ans%256))

print(ans.to_bytes(100,"big"))