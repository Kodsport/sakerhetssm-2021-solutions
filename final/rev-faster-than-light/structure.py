import math
import random
from abc import ABC, abstractmethod

import numpy as np

np.set_printoptions(edgeitems=30, linewidth=100000)

dytype = "uint64_t"
dtype = "uint64"
ulimit = 2**64
cvars = ["a", "b", "c", "d", "e", "f", "g"]

class Code(ABC):
    @abstractmethod
    def into_c(self, indentation=0, dyvars=set()):
        pass

    @abstractmethod
    def into_matrix(self):
        pass

    @abstractmethod
    def n_nodes(self):
        pass

    @abstractmethod
    def get_complexity(self):
        pass

class Reassignment(Code):
    # var = int, linear_combination = list of ints
    def __init__(self, var, linear_combination):
        self.var = var
        self.linear_combination = linear_combination

    def into_c(self, indentation=0, dyvars=set()):
        ind = "    " * indentation
        lincomb = None
        x = list(enumerate(self.linear_combination))
        random.shuffle(x)
        for i, λ in x:
            v = cvars[i]
            if λ == 0:
                continue
            elif λ == 1:
                if lincomb == None:
                    lincomb = f"{v}"
                else:
                    lincomb += f" + {v}"
            elif λ == -1:
                if lincomb == None:
                    lincomb = f"-{v}"
                else:
                    lincomb += f" - {v}"
            elif λ < 0:
                if lincomb == None:
                    lincomb = f"{λ} * {v}"
                else:
                    lincomb += f" - {-λ} * {v}"
            else:
                if lincomb == None:
                    lincomb = f"{λ} * {v}"
                else:
                    lincomb += f" + {λ} * {v}"

        if lincomb == None:
            lincomb = "0"
        return ind + cvars[self.var] + " = " + lincomb + ";"

    def into_matrix(self):
        m = np.eye(len(cvars), dtype=dtype)
        m[self.var] = self.linear_combination
        return m

    def n_nodes(self):
        return 1

    def get_complexity(self):
        return 1

# Contains many code blocks in order
class Container(Code):
    # contents = list of Code
    def __init__(self, contents):
        self.contents = contents

    def into_matrix(self):
        m = np.eye(len(cvars), dtype=dtype)
        for c in self.contents:
            m = np.dot(c.into_matrix(), m)
        return m

    def n_nodes(self):
        return sum(c.n_nodes() for c in self.contents)

class Loop(Container):
    # contents = list of Code
    def __init__(self, ntimes, contents):
        super().__init__(contents)
        self.ntimes = ntimes

    def into_c(self, indentation=0, dyvars=set()):
        ind = "    " * indentation

        i = 0
        while True:
            vname = f"i{i}"
            if vname not in dyvars:
                break
            i += 1
        ndyvars = dyvars | {vname}

        inner = "\n".join(c.into_c(indentation+1, ndyvars) for c in self.contents)

        return ind + f"for ({dytype} {vname} = 0; {vname} < {self.ntimes}U; {vname}++) {{\n" + inner + "\n" + ind + "}"

    def into_matrix(self):
        inner = super().into_matrix()
        return np.linalg.matrix_power(inner, self.ntimes)

    def get_complexity(self):
        return self.ntimes * sum(c.get_complexity() for c in self.contents)
