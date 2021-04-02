import time
import sys
import subprocess
import re

DEBUG = False

server = subprocess.Popen(["python3", "server.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
start = time.time()

def readline():
    line = server.stdout.readline()
    if DEBUG:
        print("<", line.decode("utf-8"), file=sys.stderr)
    return line

def send(st):
    if isinstance(st, str):
        st = st.encode("utf-8")
    st += b"\n"
    if DEBUG:
        print(">", st.decode("utf-8"), file=sys.stderr)
    server.stdin.write(st)
    server.stdin.flush()

r_game_start = re.compile(br".*mellan (\d+) och (\d+). Du har (\d+).*")
r_is_right = re.compile(br".*Du gissade r..tt.*")
r_is_hi = re.compile(br".*F..r h..gt!")
r_flag = re.compile(br"<flag>")

n_normals = 15

nums = []

for _ in range(30 - 12):
    l = readline()
    m = r_game_start.match(l)
    if not m: continue

    low, high, guesses = [int(x.decode("utf-8")) for x in m.groups()]
    high += 1

    readline()

    while True:
        guess = (low + high) // 2
        send(str(guess))

        hl = readline()

        if r_is_right.match(hl):
            nums.append(guess)
            break

        n_left = readline()

        if r_is_hi.match(hl):
            high = guess
        else:
            low = guess

def rand(seed):
    state = seed
    while True:
        state = ((state * 1103515245) + 12345) & 0x7fffffff
        yield state

real_rng = None
for absdelta in range(5000):
    if real_rng is not None: break
    for delta in [-absdelta, absdelta]:
        seed = int(start * 1000) + delta

        rng = rand(seed)
        is_correct = True
        for n in nums:
            if next(rng) % 10001 != n:
                is_correct = False
                break

        if is_correct:
            real_rng = rng
            break

while True:
    l = readline()
    if r_flag.match(l):
        break
    if l == b"": break
    m = r_game_start.match(l)
    if not m: continue

    low, high, guesses = [int(x.decode("utf-8")) for x in m.groups()]
    high += 1

    readline()

    num = next(rng) % 10001
    send(str(num))

flag = readline()
print(flag.decode("utf-8"), end="")
