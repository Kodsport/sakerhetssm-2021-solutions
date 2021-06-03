import sys
sys.setrecursionlimit(10000000)

#Logic
F = lambda x: lambda y: x
T =  lambda x: lambda y: y

logic_not = lambda a: lambda x: lambda y: a(y)(x)
logic_and = lambda a: lambda b: a(F)(b)
logic_or = lambda a: lambda b: a(b)(T)

#Pair
pair = lambda a: lambda b: lambda z: z(a)(b)

#Numbers
succ = lambda num: lambda f: lambda x: num(f)(f(x)) 

zero = lambda f: lambda x: x
one = succ(zero)
two = succ(one)
three = succ(two)
four = succ(three)

pred = lambda num: num(lambda p: pair(succ(p(F)))(p(F)))(pair(zero)(zero))(T)

add = lambda numA: lambda numB: lambda f: lambda x: numA(f)(numB(f)(x))
sub = lambda numA: lambda numB: numB(pred)(numA)
mult = lambda numA: lambda numB: lambda f: numA(numB(f))
exp = lambda numA: lambda numB: numA(numB)
square = lambda x: mult(x)(x)

iszero = lambda num: num(lambda ign: F)(T)
numeq = lambda numA: lambda numB: logic_and(iszero(sub(numA)(numB)))(iszero(sub(numB)(numA)))
#print(iszero(two)(False)(True))

#Lists
nil = lambda f:lambda x: x
cons = lambda head: lambda tail: lambda f: lambda x: tail(f)(f(head)(x))

numtochurch = lambda num: zero if num==0 else succ(numtochurch(num-1))
listtochurch = lambda l: nil if l==[] else cons(numtochurch(l[-1]))(listtochurch(l[:-1]))


printnum = (lambda num: num(lambda x:x+1)(0))
printlist = lambda l: l(lambda hd: lambda transtl: [printnum(hd)]+transtl)([])
#print(printlist(listtochurch([1,2,3,4])))

flag = listtochurch(list(map(ord, list(input()))))
secret = lambda l: lambda x: l(lambda hd:lambda transtl:pair(add(transtl(F))(mult(transtl(T))(hd)))(pred(transtl(T))))(pair(zero)(x))(F)

print(printnum(secret(flag)(one)))
print(printnum(secret(flag)(two)))
print(printnum(secret(flag)(three)))
print(printnum(secret(flag)(four)))

print(numeq(secret(flag)(one))(add(exp(two)(mult(three)(two)))(add(exp(two)(add(mult(two)(two))(one)))(add(exp(three)(three))(two))))(False)(True))
print(numeq(secret(flag)(two))(add(exp(mult(two)(add(mult(two)(two))(one)))(two))(add(exp(add(mult(two)(four))(one))(two))(add(exp(three)(four))(add(exp(three)(four))(mult(add(mult(two)(two))(one))(two))))))(False)(True))
print(numeq(secret(flag)(three))(add(exp(add(mult(four)(two))(one))(two))(add(exp(add(mult(three)(two))(two))(three))(add(exp(three)(four))(four))))(False)(True))
print(numeq(secret(flag)(four))(add(exp(add(mult(two)(four))(one))(three))(add(exp(mult(two)(four))(two))(add(exp(add(mult(three)(two))(one))(two))(add(exp(mult(three)(two))(three))(add(exp(three)(three))(add(exp(four)(two))(mult(add(mult(two)(two))(one))(two))))))))(False)(True))
#print(numeq(secret(flag)(add(mult(two)(two))(one)))(add(exp(mult(three)(two))(four))(add(exp(add(mult(two)(two))(one))(three))(add(exp(add(mult(three)(two))(two))(two))(add(exp(two)(add(mult(two)(three))(one)))(add(exp(two)(add(mult(two)(two))(one)))(one))))))(False)(True))
#print(numeq(secret(flag)(mult(three)(two)))(add(exp(add(mult(two)(two))(one))(four))(add(exp(mult(two)(add(mult(two)(two))(one)))(three))(add(exp(mult(add(mult(two)(two))(one))(two))(two))(add(exp(mult(two)(add(mult(two)(two))(one)))(two))(add(exp(mult(four)(two))(two))(add(exp(add(mult(four)(two))(one))(two))(add(exp(add(mult(two)(two))(one))(three))(add(exp(two)(add(mult(two)(three))(one)))(add(exp(three)(three))(add(exp(two)(four))(mult(mult(three)(two))(two))))))))))))(False)(True))
#print(numeq(secret(flag)(add(mult(three)(two))(one)))(add(exp(mult(three)(two))(four))(add(exp(mult(four)(two))(three))(add(exp(mult(three)(two))(three))(add(exp(mult(three)(two))(three))(add(exp(add(mult(two)(three))(one))(three))(add(exp(add(mult(two)(two))(one))(three))(add(exp(add(mult(four)(two))(two))(two))(add(exp(mult(two)(three))(three))(one)))))))))(False)(True))
#print(numeq(secret(flag)(mult(four)(two)))(add(exp(mult(two)(three))(four))(add(exp(add(mult(two)(two))(one))(four))(add(exp(add(mult(two)(two))(one))(four))(add(exp(mult(three)(two))(four))(add(exp(two)(add(mult(two)(two))(one)))(three))))))(False)(True))
#print(numeq(secret(flag)(add(mult(two)(four))(one)))(add(exp(add(mult(two)(two))(one))(add(mult(two)(two))(one)))(add(exp(add(mult(four)(two))(two))(three))(add(exp(mult(three)(three))(two))(add(exp(add(mult(two)(four))(one))(two))(add(exp(mult(four)(two))(three))(add(exp(four)(two))(add(exp(three)(three))(two))))))))(False)(True))
#print(numeq(secret(flag)(add(mult(three)(three))(one)))(add(exp(add(mult(two)(four))(one))(three))(add(exp(add(mult(two)(two))(one))(add(mult(two)(two))(one)))(add(exp(mult(two)(four))(three))(add(exp(mult(two)(three))(four))(add(exp(add(mult(two)(three))(one))(two))(add(exp(add(mult(three)(two))(two))(two))(add(exp(three)(four))(add(exp(four)(two))(add(exp(three)(three))(add(exp(four)(two))(one)))))))))))(False)(True))
#print(numeq(secret(flag)(add(mult(add(mult(two)(two))(one))(two))(one)))(add(exp(add(mult(four)(two))(one))(four))(add(exp(add(mult(four)(two))(one))(two))(add(exp(add(mult(two)(three))(one))(three))(add(exp(four)(three))(add(exp(three)(three))(add(mult(add(mult(two)(two))(one))(three))(one)))))))(False)(True))
#print(numeq(secret(flag)(mult(four)(three)))(add(exp(add(mult(three)(two))(one))(four))(add(exp(mult(two)(add(mult(two)(two))(one)))(three))(add(exp(mult(three)(two))(four))(add(exp(add(mult(two)(four))(one))(three))(add(exp(add(mult(two)(four))(one))(three))(add(exp(add(mult(four)(two))(one))(three))(add(exp(mult(two)(three))(four))(add(exp(mult(three)(two))(two))(add(exp(three)(four))(add(exp(four)(three))(add(exp(two)(four))(add(mult(three)(two))(one)))))))))))))(False)(True))
#print(numeq(secret(flag)(add(mult(four)(three))(one)))(add(exp(add(mult(two)(two))(one))(add(mult(two)(two))(one)))(add(exp(add(mult(two)(three))(one))(four))(add(exp(add(mult(two)(three))(one))(four))(add(exp(mult(two)(add(mult(two)(two))(one)))(three))(add(exp(mult(add(mult(two)(two))(one))(two))(two))(add(exp(add(mult(three)(two))(one))(three))(add(exp(add(mult(two)(two))(one))(three))(add(exp(mult(three)(two))(three))(add(exp(two)(mult(two)(three)))(add(exp(three)(two))(add(mult(four)(three))(three))))))))))))(False)(True))
#print(numeq(secret(flag)(add(mult(add(mult(two)(two))(one))(two))(four)))(add(exp(mult(four)(two))(four))(add(exp(mult(three)(three))(four))(add(exp(mult(three)(two))(three))(add(exp(add(mult(three)(three))(one))(two))(add(exp(add(mult(four)(two))(two))(two))(add(exp(add(mult(two)(two))(one))(three))(add(exp(two)(mult(three)(two)))(add(exp(three)(three))(add(exp(two)(four))(add(mult(add(mult(two)(two))(one))(two))(two)))))))))))(False)(True))
#print(numeq(secret(flag)(mult(add(mult(two)(two))(one))(three)))(add(exp(mult(three)(two))(add(mult(two)(two))(one)))(add(exp(add(mult(four)(two))(one))(three))(add(exp(mult(four)(two))(four))(add(exp(add(mult(two)(three))(one))(two))(add(exp(mult(three)(three))(two))(add(exp(mult(four)(two))(two))(add(exp(four)(three))(add(exp(four)(three))(mult(three)(three))))))))))(False)(True))
#print(numeq(secret(flag)(add(mult(add(mult(two)(two))(one))(three))(one)))(add(exp(add(mult(two)(two))(one))(add(mult(two)(two))(one)))(add(exp(mult(add(mult(two)(two))(one))(two))(four))(add(exp(add(mult(three)(two))(one))(three))(add(exp(mult(two)(four))(three))(add(exp(add(mult(two)(three))(one))(three))(add(exp(add(mult(two)(two))(one))(three))(add(exp(add(mult(two)(four))(one))(two))(add(exp(two)(mult(two)(three)))(add(exp(three)(three))(add(exp(two)(add(mult(two)(two))(one)))(three)))))))))))(False)(True))
#print(numeq(secret(flag)(add(exp(four)(two))(one)))(add(exp(mult(three)(two))(add(mult(two)(two))(one)))(add(exp(add(mult(three)(two))(two))(four))(add(exp(mult(two)(add(mult(two)(two))(one)))(three))(add(exp(add(mult(four)(two))(two))(three))(add(exp(add(mult(two)(two))(one))(four))(add(exp(mult(three)(two))(four))(add(exp(add(mult(three)(two))(one))(three))(add(exp(add(mult(four)(two))(one))(two))(add(exp(mult(three)(three))(two))(add(exp(four)(three))(add(exp(two)(mult(two)(three)))(add(exp(two)(add(mult(two)(two))(one)))(add(exp(three)(two))(add(mult(two)(mult(two)(three)))(one)))))))))))))))(False)(True))
