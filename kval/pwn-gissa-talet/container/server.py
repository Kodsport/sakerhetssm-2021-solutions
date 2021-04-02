#!/usr/bin/env python3

import math
import os
import time

NUM_ROUNDS = 30
MIN_NUM = 0
MAX_NUM = 10000
DEBUG = False

def debug(s):
    if DEBUG:
        print(f'DEBUG: {s}')

def rand(seed):
    state = seed
    while True:
        state = ((state * 1103515245) + 12345) & 0x7fffffff
        yield state


def get_rand():
    seed = int(time.time() * 1000)
    debug(f'seed: {seed}')
    rng = rand(seed)
    return rng


def play_game(rng, target_min, target_max, attempts):
    range_size = target_max - target_min + 1
    target = target_min + (next(rng) % range_size)
    debug(f"target={target}")
    print(f"Jag tänker på ett tal mellan {target_min} och {target_max}. Du har {attempts} försök på dig att gissa vilket det är.")
    while attempts > 0:
        print(f"Du har {attempts} försök kvar.")
        while True:
            guess = input("Vilket tal tänker jag på? ")
            try:
                guess = int(guess)
                break
            except ValueError:
                print("Vänligen ange ett heltal.")
        
        if guess > target:
            print("För högt!")
        elif guess < target:
            print("För lågt!")
        elif guess == target:
            print("Grattis! Du gissade rätt.")
            return True
        attempts -= 1
    print("Tyvärr! Du fick slut på gissningar")
    return False


def main():
    rng = get_rand()
    print("Välkommen! Nu ska vi spela ett spel.")
    for round_num in range(NUM_ROUNDS):
        num_attempts = NUM_ROUNDS-round_num
        result = play_game(rng, MIN_NUM, MAX_NUM, num_attempts)
        if not result:
            break
        if num_attempts == int(math.log2(MAX_NUM-MIN_NUM))+1:
            print("Grattis! Bra jobbat såhär långt. Du får ett litet pris! Hoppas du gillar kod.")
            with open(os.path.realpath(__file__), 'r') as fin:
                print("<code>")
                print(fin.read().strip())
                print("</code>")
        if num_attempts == 1:
            print("Wow! Grattis! Här får du ett ännu finare pris!")
            with open('/home/ctf/flag.txt', 'r') as fin:
                print("<flag>")
                print(fin.read().strip())
                print("</flag>")

if __name__ == '__main__':
    main()
