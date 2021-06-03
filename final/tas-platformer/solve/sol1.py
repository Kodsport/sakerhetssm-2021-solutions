from pathlib import Path

INPUTS = {"A": 0b1, "W": 0b10, "S": 0b100, "D": 0b1000, "B": 0b10000, 'SPACE': 0b100000}


moves = []

# Going down to button
moves += [INPUTS["D"]] * 45
moves += [INPUTS["A"]] * 2
moves += [0] * 25
moves += [INPUTS["A"]] * 77
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"]] * 17
moves += [0] * 19
moves += [INPUTS["W"]] * 1
moves += [0] * 15
moves += [INPUTS["D"]] * 20
moves += [INPUTS["B"]] * 1
moves += [INPUTS["A"]] * 11
moves += [0] * 30
moves += [INPUTS["D"]] * 20
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"]] * 70
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"]] * 30
moves += [INPUTS["W"]] * 1
moves += [0] * 10
moves += [INPUTS["A"]] * 6
moves += [0] * 8
moves += [INPUTS["D"]] * 8
moves += [INPUTS["W"]] * 1
moves += [0] * 10
moves += [INPUTS["A"]] * 7
moves += [0] * 8
moves += [INPUTS["D"]] * 3
moves += [INPUTS["W"]] * 1

# Right, up, left, up, right
moves += [INPUTS["D"]] * 45
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"]] * 64
moves += [INPUTS["W"]] * 1
moves += [INPUTS["D"]] * 35
moves += [INPUTS["W"]] * 1
moves += [INPUTS["A"]] * 15
moves += [0] * 10

moves += [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,8,0,0,0,0,0,0,0,0,8,8,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,8,8,8,8,8,8,0,0,0,0,0,0,8,8,8,8,8,8,8,8,8,8,8,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,8,8,8,8,8,8,8,8,10,10,10,10,10,10,10,10,10,10,8,8,8,8,10,10,10,10,10,10,10,10,10,10,10,10,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,9,9,9]

moves += [INPUTS["D"]]*40
moves += [INPUTS["A"]]*70
moves += [INPUTS["D"]]*110
moves += [INPUTS["A"]]*75
moves += [INPUTS["D"]]*110
moves += [INPUTS["A"]]*75
moves += [INPUTS["D"]]*83
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
moves += [INPUTS["D"]] * 90
moves += [INPUTS["W"]] * 1
moves += [0] * 20
moves += [INPUTS["A"]] * 21
moves += [INPUTS["A"] | INPUTS["W"]] * 1
moves += [INPUTS["A"]] * 5

for i in range(7):
    moves += [INPUTS["D"]] * 20
    moves += [INPUTS["W"]|INPUTS["D"]]

moves += [INPUTS["D"]] * 50
moves += [0] * 55
moves += [INPUTS["SPACE"]]
for i in range(10):
    moves += [INPUTS["A"]] * 8
    moves += [0] * 75
    moves += [INPUTS["D"]] * 16
    moves += [INPUTS["SPACE"]]

Path("moves").write_text("\n".join([str(m) for m in moves]))
