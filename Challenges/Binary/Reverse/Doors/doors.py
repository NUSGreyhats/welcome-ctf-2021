#!/usr/bin/python3
import random
import sys


flag = "greyhats{"

parts = [
    [0xa5, 0x8f, 0x64, 0x2e],
    [0x13, 0x77, 0x2a, 0xa7],
    [0xb2, 0xe6, 0x23, 0xec],
    [0xa6, 0xe7, 0x70, 0xb7],
]

# You don't need to worry about this part

def xor(part, keys):
    return "".join([chr(c ^ key) for c, key in zip(part, keys)])

def decode(idx, seed):
    part = parts[idx]
    random.seed(seed)
    keys = [random.randint(0, 0xff) for _ in range(4)]
    return xor(part, keys)

def door1():
    global flag

    print("Door 1/4")
    print("Enter the passcode:")
    try:
        key = int(input())
    except:
        print("What are you doing...")
        sys.exit(1)

    if (key & 0xfff) == 0x246 and (key >> 12) == 0x942:
        print("Correct!\n")
    else:
        print("I don't know you. Go away.")
        sys.exit(1)

    flag += decode(0, key) + "_"

def door2():
    global flag

    print("Door 2/4")
    print("Enter the passcode:")
    try:
        key = int(input())
    except:
        print("What are you doing...")
        sys.exit(1)

    if (key % 1000) ** 3 == 78402752 and ((key // 1000) ^ 861) == 189:
        print("Correct!\n")
    else:
        print("I don't know you. Go away.")
        sys.exit(1)

    flag += decode(1, key) + "_"

def door3():
    global flag

    print("Door 3/4")
    print("Enter the passcode:")
    try:
        key = int(input())
    except:
        print("What are you doing...")
        sys.exit(1)

    random.seed(52318)
    pos = [i for i in range(7)]
    random.shuffle(pos)

    key_ = 0
    for p in pos:
        dg = key % (10 ** (p + 1))
        dg //= 10 ** p
        key -= dg * (10 ** p)
        key_ *= 10
        key_ += dg

    if key != 0:
        print("I don't know you. Go away.")
        sys.exit(1)

    if key_ == 2478123:
        print("Correct!\n")
    else:
        print("I don't know you. Go away.")
        sys.exit(1)

    flag += decode(2, key) + "_"

def door4():
    global flag

    print("Door 4/4")
    print("Enter the passcode:")
    try:
        key = int(input())
    except:
        print("What are you doing...")
        sys.exit(1)

    hhs = [
        b'919c5ab6d04ee9d1c81335692d2ed68e',
        b'9f7e8841c1d64dfde51953fccecde2cf',
        b'bcb34c837111773983f4860ee51cb1b6',
        b'e48b14700f10e3d8f3ad25b73a0d20db',
        b'835f2ff9473cfc787d4f1c08ad5037c9',
        b'c3e3b06937f539a2e52b834a4f1d27fc',
    ]

    import hashlib
    import binascii
    for i in range(6):
        dg = key % 10
        key //= 10
        hh = binascii.hexlify(hashlib.md5(f"{i}_{dg}_{key}".encode()).digest())

        if hhs[i] != hh:
            print("I don't know you. Go away.")
            sys.exit(1)

    if key != 0:
        print("I don't know you. Go away.")
        sys.exit(1)

    print("Correct!\n")
    flag += decode(3, key) + "}"


if __name__ == "__main__":
    door1()
    door2()
    door3()
    door4()

    print(flag)