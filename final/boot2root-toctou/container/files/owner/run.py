# Can be run with sudo!
import random
import hashlib, os
import time
import subprocess

print("[SETUP] Initializing context...")
time.sleep(random.random())
print("[SETUP] Dismogrifying subsystems...")
time.sleep(random.random())
print("[SETUP] Optifying lenses...")
time.sleep(random.random())
print("[SETUP] Done!")

EXEC_FILE = "/home/guest/exec"
DATA_DIR = "/home/guest/edata/"

if hashlib.sha256(open(EXEC_FILE, "br").read()).hexdigest() != '0f0a6f69f675a1cc82e21e843747cf4b8518159edb90b72eb2fd33a0d2c6fbc1':
    exit(EXEC_FILE + " doesn't match!")

data_hashsum = bytes(32)
for f in os.listdir(DATA_DIR):
    f_hash = hashlib.sha256(open(os.path.join(DATA_DIR, f), "br").read()).digest()
    data_hashsum = bytes([(x + y) % 256 for x, y in zip(f_hash, data_hashsum)])

if data_hashsum.hex() != 'c976432b430dce9276200a2a01fc23e31a40a5b404067926bd23fab4782c9470':
    exit(DATA_DIR + " doesn't match!")

print("[SETUP] Running!")
subprocess.run(EXEC_FILE)
