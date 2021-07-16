#!/usr/bin/env python3

import hashlib

FLAG = b'greyhats{y0U_Kn0W_7He_53cRet_n0W}'

assert len(FLAG) == 33

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

while True:
    print('Please input your text in hexadecimal :')
    text = bytes.fromhex(input())
    text = hash(text)
    print('Here\'s the hashed value :')
    print(text)        