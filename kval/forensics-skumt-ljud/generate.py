#!/usr/bin/env python3
import sys
import numpy as np
from scipy.io.wavfile import write

flag = sys.argv[1]
message = b"\x00" + b"\xf0" * 4 + flag.encode() + b"\x00"

sample_frequency = 44100
clock_time = 2000
frequency = 3000
sample_count = clock_time * len(message) * 8

sound = np.arange(sample_count) / sample_frequency
sound = np.sin(2 * np.pi * 3000 * sound)

for i, char in enumerate(message):
    for j in range(8):
        bit = i * 8 + j
        if not char & (0b10000000 >> j):
            sound[clock_time * bit : clock_time * (bit + 1)] = np.zeros(clock_time)

write("ljud.wav", 44100, np.int16(sound / np.max(np.abs(sound)) * 32767 / 8))
