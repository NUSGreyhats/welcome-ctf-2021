import hashlib
from pwn import *
from sage.all import *

def decryptFlag(msg, shared_secret):
    sha512 = hashlib.sha512()
    sha512.update(str(shared_secret).encode('ascii'))
    key = sha512.digest()[:len(msg)]
    return bytes([i[0] ^ i[1] for i in zip(key, msg)])

def genOutput(u, a, b):
    output = u**2
    output += 3 * b * u
    output += 5 * a * b 
    output += 7 * a**3
    output += 13 * b**5
    output += 17
    return output

def extractBit(x, i):
    return (x >> i) & 1

def getSharedKey(basis_1, basis_2):
    key = 0
    for i in range(n - 1, -1, -1):
        basis1 = extractBit(basis_1, i)
        basis2 = extractBit(basis_2, i)
        if (basis1 == basis2):
            key <<= 1
            key += extractBit(result, i)
    return key

mod = 174063964518299711069668788749181472608683256519506953845957678021663479790503805130054996103933773128050079469402511808215999318969731313310594568270351166276458312376711993828352623947694042786055748003333138637438781936115718720589210722171329782548215473804182484259253296933564937708732223142168136245153

n = 1024

r = remote('localhost', 3000, level='debug')

arr = []

for i in range(4):
    r.recvuntil('Basis :\n')
    r.sendline("00"*128)
    r.recvuntil('Bob :\n')
    bobBasis = int(r.recvline(), 16)
    r.recvline()
    arr.append(bobBasis)

## Gorbner_basis begin

a, u, b = gens(PolynomialRing(Zmod(mod), ['a','u','b']))

d = pow(23, -1, mod - 1)
f = u
ideal = []

for i in range(4):
    ideal.append(genOutput(f, a, b) - pow(arr[i], d, mod))
    f = (a * f + a + b + a * b)

I = Ideal(ideal)
B = I.groebner_basis()

## Gorbner_basis end
a = int((-B[0](a = 0))) % mod
u = int(-B[1](u = 0)) % mod
b = int(-B[2](b = 0)) % mod

# Calculate the basis

for i in range(4):
    u = a * u + a + b + a * b
basis = pow(genOutput(u, a, b), 23, mod)

r.recvuntil('Basis :\n')
r.sendline(hex(basis)[2:].zfill(128 * 2))
r.recvuntil('result :\n')
result = int(r.recvline(), 16)
r.recvuntil('Alice :\n')
aliceBasis = int(r.recvline(), 16)
r.recvuntil('Flag :\n')
flag = r.recvline()

key = getSharedKey(aliceBasis, basis)

print(key)

print(decryptFlag(bytes.fromhex(flag.decode()), key))