import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import pickle
import math
import random

import numpy as np

from structure import *

np.set_printoptions(edgeitems=30, linewidth=100000)

# Returns tree, n
def generate(wanted_n, max_depth, min_nodes):
    class UlimitExceeded(Exception):
        pass

    def subgenerate(wanted_n, max_depth, min_nodes):
        if max_depth == 0:
            def gen_n():
                if random.random() < 0.3:
                    return random.randint(-10, 10)
                return 0

            while True:
                l = Reassignment(random.randrange(len(cvars)), [gen_n() for _ in range(len(cvars))])
                if np.linalg.det(l.into_matrix()) != 0:
                    return l

        def gen_n():
            nn = max(5 * wanted_n / ulimit, wanted_n ** 0.5)
            x = random.expovariate(1 / nn)
            if x <= nn:
                return x
            return gen_n()

        l = Loop(1, [subgenerate(gen_n(), max_depth - 1, random.randint(2, min_nodes))])
        while l.n_nodes() < min_nodes or len(l.contents) < 2:
            l.contents.append(subgenerate(gen_n(), random.randrange(max_depth), random.randint(2, min_nodes)))

        random.shuffle(l.contents)

        if l.get_complexity() == 0:
            print(l.into_c())

        l.ntimes = int(2 + wanted_n / l.get_complexity())

        if np.linalg.det(l.into_matrix()) == 0:
            return subgenerate(wanted_n, max_depth, min_nodes)

        if l.ntimes > ulimit:
            raise UlimitExceeded()
        return l

    while True:
        try:
            return subgenerate(wanted_n, max_depth, min_nodes)
        except UlimitExceeded as _:
            print(":(")
            pass

# Program:
# int a = 1, b = 1, t=0;
#
# for (int i = 0; i < 10; i++) {
#    t = a;
#    a = a + b
#    b = t;
# }

# p = Loop(
#     10,
#     [
#         Reassignment(2, [1, 0, 0]),
#         Reassignment(0, [1, 1, 0]),
#         Reassignment(1, [0, 0, 1]),
#     ]
# )

# print(p.into_c());
# print(p.into_matrix())

while True:
    p = generate(10**80, 10, 10)
    print("Found!")
    print(repr(p.into_matrix()))
    vv = p.into_matrix() @ np.ones([len(cvars), 1], dtype=dtype)
    gcd = np.gcd(vv, vv.T)
    print(gcd)
    if np.isin(1, gcd):
        pickle.dump(p, open("block.pkl", "wb"))
        break
