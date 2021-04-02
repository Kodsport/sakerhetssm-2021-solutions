#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import ast

with open('mystiskt.txt', 'r') as fin:
    for line in fin:
        line = ast.literal_eval(line.strip())
        line = np.array(line)
        plt.plot(*line.T, '.')
        plt.show()
# will plot _ as -
