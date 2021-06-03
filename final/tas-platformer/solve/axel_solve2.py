import os
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
left(20)
still(20)
left(20)
jump(1)
right(40)

for i in range(25):
    jump(1)
    right(1)

still(40)

for i in range(40):
    jump(1)
    if (i % 2 == 0):
        right(1)
    else:
        still(1)

sprint_right(8)
right(20)
attack(10)
left(40)
for i in range(9):
    right(42)
    attack(1)
    if i != 8:
        left(25)
# jump(1)
# right(10)
# jump(1)
# right(30)
# still(200)
code = ""
for c in moves:
    code += str(c)+"\n"
code += str(0)

with open("moves", "w") as f:
    for c in moves:
        f.write(str(c)+"\n")
    f.write(str(0))
