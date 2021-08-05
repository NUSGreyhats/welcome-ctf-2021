from pwn import *
import hashlib

r = remote('localhost', 3000)

r.recvline()

flag = b''
block = 16

for i in range(100):
    r.recvline()
    payload = '00' * i
    r.sendline(payload)
    r.recvline()
    hashed = r.recvline()
    for j in range(32, 127):
        t = bytes([j]) + flag[:15]
        t += b'\0' * ((block - (len(t) % block)) % block)
        sha512 = hashlib.sha512()
        sha512.update(t)
        test = sha512.hexdigest()[:block * 2]
        if (test.encode() == hashed[block*2*4:block*2*5]):
            flag = bytes([j]) + flag
            print(flag)
            break