#!/bin/env python3

flag = "lite is i isteet"

letters = {"l": ("3 lm, 1 lm, vänd, "
                +"3 fm, 1 lm, vänd, "*7
                +"3 fm, 7 lm, 1 lm, vänd, 10 fm, "
                +"avsluta och fäst tråden"),
           "i": ("3 lm, 1 lm, vänd, "
                +"3 fm, 1 lm, vänd, "*8
                +"3 fm, "
                +"avsluta och fäst tråden"),
           "t": ("10 lm, 1 lm, vänd, 6 fm, 1 lm, vänd, "
                +"3 fm, 1 lm, vänd, "*8
                +"3 fm, "
                +"avsluta och fäst tråden"),
           "e": ("10 lm, 1 lm, vänd, 10 fm, 1 lm, vänd, "
                +"3 fm, 1 lm, vänd, "*2
                +"3 fm, 7 lm, 1 lm, vänd, 10 fm, 1 lm, vänd, "
                +"3 fm, 1 lm, vänd, "*2
                +"3 fm, 7 lm, 1 lm, vänd, 10 fm, "
                +"avsluta och fäst tråden"),
           "s": ("10 lm, 1 lm, vänd, 10 fm, 1 lm, vänd, "
                +"3 fm, 1 lm, vänd, "*2
                +"3 fm, 7 lm, 1 lm, vänd, "
                +"3 fm, 1 lm, vänd, "*2
                +"3 fm, 7 lm, 1 lm, vänd, 10 fm, "
                +"avsluta och fäst tråden"),
           " ": ""}

pattern = ""
for l in flag:
    if l in letters:
        pattern += letters[l]
    pattern += "\n"

print(pattern.strip())
