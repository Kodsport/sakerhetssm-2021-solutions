import itertools


def test_solution(sol):
    xor0 = sol[15] ^ sol[8]
    xor1 = sol[12] ^ sol[13]
    xor2 = sol[8] ^ sol[12]
    xor3 = sol[10] ^ sol[0]
    xor4 = sol[13] ^ sol[9]
    xor5 = sol[14] ^ sol[11]
    xor6 = sol[11] ^ sol[10]
    xor7 = sol[9] ^ sol[14]
    xor8 = sol[7] ^ sol[15]
    xor9 = sol[2] ^ sol[3]
    xor10 = sol[6] ^ sol[1]
    xor11 = sol[1] ^ sol[2]
    xor12 = sol[0] ^ sol[4]
    xor13 = sol[3] ^ sol[5]
    xor14 = sol[4] ^ sol[6]
    xor15 = sol[5] ^ sol[7]
    return all(
        [
            not xor0,
            not xor1,
            xor2,
            not xor3,
            not xor4,
            not xor5,
            xor6,
            not xor7,
            xor8,
            xor9,
            xor10,
            xor11,
            not xor12,
            xor13,
            not xor14,
            xor15,
        ]
    )


for potential_solution in itertools.product([True, False], repeat=16):
    if test_solution(potential_solution):
        string = "".join("1" if bit else "0" for bit in potential_solution)
        print("0b" + "".join(reversed(string[:8])), "0b" + string[8:])
        print(hex(int("".join(reversed(string[:8])), 2)), hex(int(string[8:], 2)))
        print(potential_solution)