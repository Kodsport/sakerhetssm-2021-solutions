#!/usr/bin/env python3

import csv
import gzip
import os
from PIL import Image

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 144
OUTPUT_DIR = 'render'

COLORS = {
    0: (255, 255, 255),
    1: (120, 120, 120),
    2: (50, 50, 50),
    3: (0, 0, 0)
}

with gzip.open('spy-game.csv.gz', mode='rt') as gzfin:
    # Print file header
    for _ in range(4):
        print(next(gzfin).strip())
    
    # Process CSV
    csvreader = csv.reader(gzfin)
    header = next(csvreader)
    print(header)

    frame = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
    row = 0
    col = 0
    frame_num = 0
    prev_d0, prev_d1, prev_hsync, prev_vsync, prev_clk = 0, 0, 0, 0, 0
    for line in csvreader:
        d0, d1, hsync, vsync, clk = [int(x) for x in line[1:]]
        if prev_hsync == 1 and hsync == 0:
            col = 0
            if row + 1 < SCREEN_HEIGHT:
                row += 1
        if prev_vsync == 1 and vsync == 0:
            if frame_num > 0 and row > 5:
                im = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT))
                for y in range(SCREEN_HEIGHT):
                    for x in range(SCREEN_WIDTH):
                        im.putpixel((x,y), COLORS[frame[y][x]])
                im.save(os.path.join(OUTPUT_DIR, f'frame_{frame_num}.png'))
            row = 0
            frame = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
            frame_num += 1
        if prev_clk == 0 and clk == 1:
            try:
                frame[row][col] = (d1 << 1 | d0)
            except IndexError as e:
                print(e)
                print(f'Frame: {frame_num}, Y: {row}, X: {col}')
                raise
            col += 1

        prev_d0, prev_d1, prev_vsync, prev_hsync, prev_clk = d0, d1, vsync, hsync, clk
        

