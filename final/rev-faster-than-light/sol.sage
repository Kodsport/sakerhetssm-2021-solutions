import json

tree = json.load(open("tree.json","r"))

ID = Matrix(Zmod(2**64),matrix.identity(7))

def getM(l):
    a = Matrix([1,0,0,0,0,0,0])
    b = Matrix([0,1,0,0,0,0,0])
    c = Matrix([0,0,1,0,0,0,0])
    d = Matrix([0,0,0,1,0,0,0])
    e = Matrix([0,0,0,0,1,0,0])
    f = Matrix([0,0,0,0,0,1,0])
    g = Matrix([0,0,0,0,0,0,1])

    v,ex = l.split(" = ")

    M = Matrix(ID)
    M[ord(v)-ord('a')] = eval(ex)

    if sum(M)[0] == 0 and sum(M)[1] == 0  and sum(M)[2] == 0:
        print(l)

    return M

def getMatrix(tree):
    M = ID
    name, parts = tree

    #if len(json.dumps(tree)) == 25402:
    #    print(sum(sum(M)))

    if name == "statement":
        for p in parts:
            M = getMatrix(p)*M

            if sum(M)[0] == 0 and sum(M)[1] == 0  and sum(M)[2] == 0:
                print(getMatrix(p))

    if name == "forloop":
        num = parts[2]
        statement = parts[-1]
        M = getMatrix(statement)**int(num[1]) * M

        if sum(M)[0] == 0 and sum(M)[1] == 0  and sum(M)[2] == 0:
            print(getMatrix(statement))
            print(getMatrix(statement)**int(num[1]))
            print(num[1])
            exit()

    if name == "assignment":
        var = parts[0][1][0][1]
        expr = parts[1][1][0][1]
        M = getM(var + " = " + expr)

    
    return M

M = getMatrix(tree)


a = sum(M[0])
b = sum(M[1])
c = sum(M[2])
d = sum(M[3])
e = sum(M[4])
f = sum(M[5])
g = sum(M[6])