INPUTS = {"A": 0b1, "W": 0b10, "S": 0b100,
          "D": 0b1000, "B": 0b10000, 'SPACE': 0b100000}


moves = []


def right(steps):
    moves.extend([INPUTS["D"]] * steps)


def left(steps):
    moves.extend([INPUTS["A"]] * steps)


def jump(steps):
    moves.extend([INPUTS["W"]] * steps)


def button():
    moves.append(INPUTS["B"])


def attack(steps):
    moves.extend([INPUTS["SPACE"]] * steps)


def still(steps):
    moves.extend([0] * steps)


def fly(steps):
    for i in range(steps):
        jump(1)
        still(1)


def sprint_right(steps):
    for i in range(steps):
        right(20)
        jump(1)


left(15)
right(5)
button()

right(35)
jump(1)
right(125)
fly(280)
still(127)


moves += [0] * 40
moves += [INPUTS["A"]] * 20
moves += [INPUTS["D"]] * 40
moves += [INPUTS["D"], INPUTS["D"] | INPUTS["W"]] * 10
moves += [INPUTS["D"]] * 5
moves += [0] * 33
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"], INPUTS["D"] | INPUTS["W"]]*80

moves += [INPUTS["D"]] * 50
moves += [0] * 55
moves += [INPUTS["SPACE"]]
for i in range(10):
    moves += [INPUTS["A"]] * 24
    moves += [INPUTS["D"]] * 42
    moves += [INPUTS["SPACE"]]

code = ""
for c in moves:
    code += str(c)+"\n"
code += str(0)

with open("moves", "w") as f:
    for c in moves:
        f.write(str(c)+"\n")
    f.write(str(0))
