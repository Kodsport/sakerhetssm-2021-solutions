import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from structure import *
import struct
import numpy as np
import math

data = open("../ftl.c", "r").read()
lines = [l.strip() for l in data.split("\n")]
lines = lines[lines.index("int main() {")+1:]

i = 0
cvars = []
while True:
    if lines[i].startswith("uint64_t"):
        cvars.append(lines[i].split()[1])
        i += 1
    else:
        break

stack = []
while True:
    l = lines[i]
    i += 1
    if l.startswith("for"):
        times = int(l.split(" < ")[1].split("U")[0])
        stack.append(Loop(times, []))
    elif l.startswith("}"):
        loop = stack.pop()
        if stack == []:
            p = loop
            break
        stack[-1].contents.append(loop)
    else:
        var, val = l.split(" = ")
        val = val[:-1] # remove ;
        factors = []
        for vvar in cvars:
            d = {v: 0 for v in cvars}
            d[vvar] = 1
            factors.append(eval(val, d))
        r = Reassignment(cvars.index(var), factors)
        stack[-1].contents.append(r)


vars_end = p.into_matrix() @ np.ones([len(cvars)], dtype=dtype)
locals = {cvar: vars_end[i].item() for i, cvar in enumerate(cvars)}

cs = []

flag = b""
while True:
    l = lines[i]
    i += 1
    if l.startswith("uint64_t"):

        var, val = l.split(" = ")
        var = var.split(" ")[1]
        val = val[:-1]

        res = ((1 << 64) - 1) & eval(val.replace("U", ""), locals)

        flag += struct.pack("Q", res)
    else:
        break

print("Did ~10^" + str(math.log10(p.get_complexity())), "calculations (should be ~10^80)", file=sys.stderr)
sys.stdout.buffer.write(flag)
