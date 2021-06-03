from pathlib import Path

INPUTS = {"A": 0b1, "W": 0b10, "S": 0b100,
          "D": 0b1000, "B": 0b10000, 'SPACE': 0b100000}


moves = []
moves += [INPUTS["A"]] * 15
moves += [INPUTS["D"]] * 10
moves += [INPUTS["B"]]
moves += [INPUTS["D"]] * 40
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"]] * 46


# Right, up, left, up, right
moves += [INPUTS["D"]] * 45
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"]] * 64
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"]] * 35
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"]] * 1

moves += [INPUTS["D"] | INPUTS["W"], INPUTS["D"]]*50

moves += [INPUTS["D"]]*60
moves += [INPUTS["A"], INPUTS["A"] | INPUTS["W"]]*35
moves += [INPUTS["D"], INPUTS["D"] | INPUTS["W"]]*45
moves += [INPUTS["A"]]*10
moves += [INPUTS["A"], INPUTS["A"] | INPUTS["W"]]*30
moves += [INPUTS["D"]]*10
moves += [INPUTS["D"], INPUTS["D"] | INPUTS["W"]]*35

moves += [INPUTS["A"], INPUTS["A"] | INPUTS["W"]]*30
moves += [INPUTS["A"]]*5
moves += [INPUTS["D"]]*79
moves += [INPUTS["A"], INPUTS["A"] | INPUTS["W"]]*20


#moves += [INPUTS["A"]] * 0
#moves += [0] * 5
#moves += [INPUTS["W"]] * 1
moves += [INPUTS["A"]] * 15
moves += [INPUTS["W"]] * 1
moves += [INPUTS["A"]] * 46
moves += [0] * 5
moves += [INPUTS["W"]] * 1
moves += [INPUTS["A"]] * 40
#moves += [INPUTS["W"]] * 1
moves += [INPUTS["A"]] * 42
moves += [INPUTS["D"]] * 35
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"]] * 24
moves += [0] * 33
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"], INPUTS["D"] | INPUTS["W"]]*15

"""
moves += [INPUTS["D"]] * 90
moves += [INPUTS["W"]] * 1
moves += [0] * 20
moves += [INPUTS["A"]] * 21
moves += [INPUTS["A"] | INPUTS["W"]] * 1
moves += [INPUTS["A"]] * 5
"""

for i in range(7):
    moves += [INPUTS["D"]] * 20
    moves += [INPUTS["W"] | INPUTS["D"]]

moves += [INPUTS["D"]] * 50
moves += [0] * 55
moves += [INPUTS["SPACE"]]
for i in range(10):
    moves += [INPUTS["A"]] * 24
    moves += [INPUTS["D"]] * 42
    moves += [INPUTS["SPACE"]]

Path("moves").write_text("\n".join([str(m) for m in moves]))
