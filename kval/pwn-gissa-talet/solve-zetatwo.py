#!/usr/bin/env python3

from pwn import *


def rand(seed):
    state = seed
    while True:
        state = ((state * 1103515245) + 12345) & 0x7fffffff
        yield state

def rand_mod(seed, num_min, num_max):
    range_size = num_max - num_min + 1
    for val in rand(seed):
        yield num_min + (val % range_size)

def test_seed(seed, target):
    cand_sequence = list(zip(target, rand_mod(seed, 0, 10000)))
    return all(x==y for x,y in cand_sequence)


def find_seed(start_time, target):
    for cand_seed in range(start_time - 1000, start_time + 1000):
        if test_seed(cand_seed, target):
            return cand_seed
    return False


start_time = int(time.time() * 1000)
r = process(['python3', 'server.py'], level='info')

answers = []

rng = None
for round_num in range(30):
    game_params = r.recvline_contains('Jag tänker på ett tal mellan '.encode('utf-8')).strip().split()
    num_min, num_max, attempts = int(game_params[6]), int(game_params[8][:-1]), int(game_params[11])
    log.info('Game: %d-%d, attempts: %d', num_min, num_max, attempts)
    min_guess = num_min
    max_guess = num_max

    if rng:
        min_guess = next(rng)
        max_guess = min_guess

    for _ in range(attempts):
        guess = (min_guess+max_guess)//2
        log.info('Guessing: %d', guess)
        r.recvuntil('Vilket tal tänker jag på? '.encode('utf-8'))
        r.sendline(str(guess))
        result = r.recvline().decode('utf-8')
        if result.startswith('För högt!'):
            log.debug('Too high')
            max_guess = guess
        elif result.startswith('För lågt!'):
            log.debug('Too low')
            min_guess = guess + 1
        elif result.startswith('Grattis!'):
            log.info('Success!')
            answers.append(guess)

            if round_num == 16:
                r.recvline_contains('<code>')
                r.recvline_contains('</code>')
                seed = find_seed(start_time, answers)
                if not seed:
                    log.error('Failed to find seed for sequence %s', str(answers))
                log.info('Seed: %d', seed)
                rng = rand_mod(seed, 0, 10000)
                for _ in range(round_num+1): next(rng)

            if round_num == 29:
                r.recvline_contains('<flag>')
                flag = r.recvline().strip().decode('utf-8')
                r.recvline_contains('</flag>')
                log.info('Flag: %s', flag)
            
            break
    else:
        print(answers)
        log.error('Failed to win!')
