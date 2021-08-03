#!/usr/bin/python3
import subprocess
import time
import os
from itertools import cycle

#
#   PyMakeFile /s
#

TEMP_FNAME = "binary_bytes.h"

def brrrr(x):
    y = (x + 0xDEADBEEF) * x
    return y & 0xFFFFFFFF

def xor(p: bytearray, seed: bytes) -> bytearray:
    ret = []
    key = (seed[3] << 24) | (seed[2] << 16) | (seed[1] << 8) | seed[0]
    c = 0
    for i in range(len(p)):
        ret.append(p[i] ^ (key >> (8*c) & 0xFF))
        c += 1
        if c == 4:
            key = brrrr(key)
            c = 0
    return bytearray(ret)

def hexstr(h: bytearray):
    return ''.join(["\\x" + hex(x)[2:] for x in h])

FLAG = b"greyhats{p4cK_@ll_th3_th1Ng5!!!}"
FLAG = [FLAG[i:i+4] for i in range(0, len(FLAG), 4)][::-1]

if not os.path.exists("build"):
    os.mkdir("build")

# Build base binary
subprocess.run("gcc -s end.c -o build/out-0", shell=True)

for i in range(0, 8):
    with open(f"build/out-{i}", "rb") as ff:
        enc = xor(ff.read(), FLAG[i])
        enc = hexstr(enc)

        with open(TEMP_FNAME, "w") as f:
            f.write("static char BINARY[] = \"{}\";".format(enc))

        subprocess.run("gcc -s layer.c -o build/out-{}".format(i+1), shell=True)
        print("Built out-{}".format(i+1))
        time.sleep(0.1)

os.remove(TEMP_FNAME)