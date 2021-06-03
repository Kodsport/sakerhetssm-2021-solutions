#!/bin/env python3
import string, json, base64, sys

sys.setrecursionlimit(30)

def f():
    pass
CODE_TYPE = type(f.__code__)
FUNC_TYPE = type(f)

class NumberCell:
    def __init__(self, n):
        self.n = n

    @staticmethod
    def new():
        while True:
            try:
                n = int(input("Cell value:\n> "))
                return NumberCell(n)
            except:
                print("not a number")
            
    def eval(self, _):
        return str(self.n)

    def view(self):
        return str(self.n)

class FormulaCell:
    def __init__(self, formula):
        self.formula = formula

    @staticmethod
    def new():
        print("Create a Formula Cell. Not for the faint of heart.")
        while True:
            try:
                x = input("Formula import string:\n> ")
                x = base64.b64decode(x)
                x = json.loads(x)
                assert len(x) == 14
                x = CODE_TYPE(x[0], x[1], x[2], x[3], x[4], x[5], base64.b64decode(x[6]), tuple(x[7]), tuple(x[8]), tuple(x[9]), x[10], x[11], x[12], base64.b64decode(x[13]))
                x = FUNC_TYPE(x, globals())
                return FormulaCell(x)                
            except:
                print("Bad import string")

    def eval(self, sheet):
        return str(self.formula(sheet))

    def view(self):
        c = self.formula.__code__
        x = [c.co_argcount, c.co_posonlyargcount, c.co_kwonlyargcount, c.co_nlocals, c.co_stacksize, c.co_flags, base64.b64encode(c.co_code).decode(), c.co_consts, c.co_names, c.co_varnames, c.co_filename, c.co_name, c.co_firstlineno, base64.b64encode(c.co_lnotab).decode()]
        x = base64.b64encode(json.dumps(x).encode())
        return x.decode()

class Sheet:
    def __init__(self, w, h):
        self.grid = []
        for _ in range(h):
            row = []
            for _ in range(w):
                row.append(NumberCell(1))
            self.grid.append(row)
    
    def display(self):
        col_widths = [1]*len(self.grid[0])
        for row in self.grid:
            for col in range(len(row)):
                col_widths[col] = max(col_widths[col], len(row[col].eval(self)))
        separator = "+----+" + "+".join(["-"*(n+2) for n in col_widths]) + "+"
        print(separator)
        self.display_row(" ", [chr(ord("A")+i) for i in range(len(col_widths))], col_widths)
        print(separator)
        for (i, row) in enumerate(self.grid):
            self.display_row(str(i), [cell.eval(self) for cell in row], col_widths)
            print(separator)

    def display_row(self, first, values, col_widths):
        print("| "+"%2s"%first+" | " + " | ".join([("%"+str(n)+"s")%val for (val, n) in zip(values,col_widths)]) + " |")        

    def edit(self, r, c):
        while True:
            try:
                choice = int(input("1. Create number cell\n2. Create formula cell\n> "))
            except:
                print("Bad option!")
                continue
            if choice == 1:
                self.grid[r][c] = NumberCell.new()
                return
            elif choice == 2:
                self.grid[r][c] = FormulaCell.new()
                return
            else:
                print("Bad option")

    def view(self, r, c):
        print("Cell:", self.grid[r][c].view())

the_sheets = {}

def new_sheet():
    name = input("Name? ")
    the_sheets[name] = Sheet(10, 10)
    open_sheet(name)

def list_sheets():
    print("The Sheets:")
    for k in the_sheets.keys():
        print(k)

def open_sheet(name=""):
    if len(the_sheets) == 0:
        print("There are no sheets yet! Create one first!")
        return

    if name == "":
        list_sheets()
        name = input("Name? ")
        while name not in the_sheets:
            list_sheets()
            print("Sheet doesn't exist")
            name = input("Name? ")
    
    sheet = the_sheets[name]
    while True:
        print("------", name, "--------------------------")
        sheet.display()
        print("t <pos> - edit, w <pos> - view, e - close")
        choice = input("> ").split(" ")
        if choice[0] == "t":
            try:
                r, c = pos2rowcol(choice[1])
                sheet.edit(r, c)
            except:
                print("Bad row or col!")
        elif choice[0] == "w":
            try:
                r, c = pos2rowcol(choice[1])
                sheet.view(r, c)
            except:
                print("Bad row or col!")            
        elif choice[0] == "e":
            return
        else:
            print("Bad choice!")

def pos2rowcol(pos):
    assert len(pos) >= 2
    assert pos[0] in string.ascii_uppercase
    assert all([c in string.digits for c in pos[1:]])
    return int(pos[1:]), ord(pos[0])-ord("A")

def menu():
    print("Menu")
    print("1. Open sheet")
    print("2. New sheet")
    print("3. Exit")

def banner():
    print(""" ______     __  __     ______     __     __         __         ______    
/\  ___\   /\_\_\_\   /\___  \   /\ \   /\ \       /\ \       /\  __ \   
\ \  __\   \/_/\_\/_  \/_/  /__  \ \ \  \ \ \____  \ \ \____  \ \  __ \  
 \ \_____\   /\_\/\_\   /\_____\  \ \_\  \ \_____\  \ \_____\  \ \_\ \_\ 
  \/_____/   \/_/\/_/   \/_____/   \/_/   \/_____/   \/_____/   \/_/\/_/ 
Excel killa""")

def main():
    banner()
    while True:
        menu()
        try:
            choice = int(input("> "))
        except:
            print("Bad choice!")
            continue
        if choice == 1:
            open_sheet()
        elif choice == 2:
            new_sheet()
        elif choice == 3:
            print("Bye!")
            break
        else:
            print("Bad choice!")

if __name__ == "__main__":
    import random
    random.seed(0)
    example = Sheet(2, 12)
    for i in range(10):
        example.grid[i][0] = NumberCell(random.randint(1, 9)*100)
        example.grid[i][1] = NumberCell(random.randint(1, 9)*100)
    
    def sumcol0(sheet):
        res = 0
        for i in range(10):
            res += int(sheet.grid[i][0].eval(sheet))
        return str(res)
    def sumcol1(sheet):
        res = 0
        for i in range(10):
            res += int(sheet.grid[i][1].eval(sheet))
        return str(res)
    def total(sheet):
        return str(int(sheet.grid[10][0].eval(sheet))+int(sheet.grid[10][1].eval(sheet)))

    example.grid[10][0] = FormulaCell(sumcol0)
    example.grid[10][1] = FormulaCell(sumcol1)
    example.grid[11][0] = NumberCell(0)
    example.grid[11][1] = FormulaCell(total)
    the_sheets["budget"] = example
    main()
