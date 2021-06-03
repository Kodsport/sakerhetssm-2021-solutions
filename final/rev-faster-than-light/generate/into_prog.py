import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from structure import *
import numpy as np
import pickle
import struct

flag = b"SSM{f0r3ver_in_darkness}"
splits = [
    flag[i:i+8]
    for i in range(0, len(flag), 8)
]
flag_bytes = [
    struct.unpack("Q", split)[0]
    for split in splits
]

def xgcd(a, b):
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

p = pickle.load(open("block.pkl", "br"))

vv = p.into_matrix() @ np.ones([len(cvars), 1], dtype=dtype)


x, y = 0, 0

for i in range(len(cvars)):
    for j in range(i + 1, len(cvars)):
        if np.gcd(vv[i], vv[j]) == 1:
            x = i
            y = j

a, b = vv[x][0].item(), vv[y][0].item()
g, n, m = xgcd(a, b)

# TODO kanske köra någon lattice grej så saker blir små?

cdefs = []
cs = []

for i, fbyte in enumerate(flag_bytes):
    fbyte = np.array(fbyte, dtype=dtype)
    mult = np.array([random.randrange(0, ulimit) for _ in range(len(cvars))], dtype=dtype)
    mult[x] = 0
    mult[y] = 0
    diff = fbyte - (mult @ vv)[0]
    mult[x] = np.array(n, dtype=dtype) * np.array(diff, dtype=dtype)
    mult[y] = np.array(m, dtype=dtype) * np.array(diff, dtype=dtype)

    cval = " + ".join([
        f"{cvars[i]}*{mult[i]}U" for i in range(len(mult))
    ])
    c = f"c{i}"
    cdefs.append(f"{dytype} {c} = {cval};")
    cs.append(f"&{c}")

code = ""
code += "#include<stdint.h>" + "\n"
code += "#include<stdio.h>" + "\n"
code += "int main() {" + "\n"
for cvar in cvars:
    code += f"    {dytype} {cvar} = 1;" + "\n"
code += p.into_c(indentation=1) + "\n"
for cdef in cdefs:
    code += "    " + cdef + "\n"
code += '    printf("' + "%.8s" * len(flag_bytes) + '\\n", ' + ", ".join(cs) + ");" + "\n"
code += "}" + "\n"

with open("../ftl.c", "w") as f:
    f.write(code)
