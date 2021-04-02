# bevisar att det bara finns en lösning
import itertools

def testa_lösning(a, b, c, d, e, f, g, h):
    or1 = a or c
    and1 = b and h
    not1 = not or1
    xor1 = and1 ^ not1
    or2 = d or e
    and2 = and1 and f
    or3 = xor1 or or2
    xor2 = g ^ and2
    and3 = and2 and or3
    or4 = xor2 or and3
    not2 = not or4
    and4 = not2 and g
    return and4

for testlösning in itertools.product([True, False], repeat=8):
    if testa_lösning(*testlösning):
        print(testlösning)
