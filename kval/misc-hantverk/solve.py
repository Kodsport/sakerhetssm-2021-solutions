#!/bin/env python3
from PIL import Image

with open("chall.txt") as f:
    pattern = f.read().strip()

letters = pattern.split("\n")

width, height = 400, 12
letter_width = 15
img = Image.new("RGB", (width, height), "white")
pix = img.load()

for (letter_index, letter) in enumerate(letters):
    letter = letter.split(", ")
    x, y = letter_index*letter_width, 0
    direction = 1 # 1 for right, -1 for left
    i = 0
    while i < len(letter):
        p = letter[i]
        if p == "avsluta och fäst tråden":
            break
        elif p == "1 lm" and letter[i + 1] == "vänd":
            direction *= -1
            x += direction
            y += 1
            i += 2
        elif p.endswith("lm") or p.endswith("fm"):
            num = int(p.split(" ")[0])
            for j in range(num):
                pix[x + j*direction, y] = (0, 0, 0)
            x += num*direction
            i += 1
        else:
            print("bad:", repr(p))
            break

img.save("flag.png") 
