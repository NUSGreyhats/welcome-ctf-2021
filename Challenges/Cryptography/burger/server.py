#!/usr/bin/env python3

import hashlib

FLAG = b'greyhats{B3lanJa_m3_Burg3R_1f_y0u_3njoyed_7he_Ch@ll3n93}'

assert len(FLAG) == 56

block = 16

def hash(text):
    res = ''
    text = text + FLAG
    # padding
    text += b'\0' * (block - (len(text) % block))
    for i in range(0, len(text), block):
        sha512 = hashlib.sha512()
        sha512.update(text[i:i + block])
        res += sha512.hexdigest()[:block * 2]
    return res

print('Welcome to Burger hashing machine!!!')

for _ in range(100):
    print('Please input your text in hexadecimal :')
    try:
        text = bytes.fromhex(input())
    except:
        print('Error: The input must be a valid hexadecimal string')
        exit(0)
    text = hash(text)
    print('Here\'s the hashed value :')
    print(text)