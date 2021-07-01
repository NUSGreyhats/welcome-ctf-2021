import hashlib
from pwn import *
from sage.all import *

def decryptFlag(msg, shared_secret):
    sha512 = hashlib.sha512()
    sha512.update(str(shared_secret).encode('ascii'))
    key = sha512.digest()[:len(msg)]
    return bytes([i[0] ^ i[1] for i in zip(key, msg)])

mod = 174063964518299711069668788749181472608683256519506953845957678021663479790503805130054996103933773128050079469402511808215999318969731313310594568270351166276458312376711993828352623947694042786055748003333138637438781936115718720589210722171329782548215473804182484259253296933564937708732223142168136245153

n = 1024

r = remote('localhost', 8888, level='debug')

arr = []

for i in range(19):
    r.recvuntil('Basis :\n')
    r.sendline(','.join(['0' for i in range(1024)]))
    r.recvuntil('Bob :\n')
    bobBasis = int(b''.join(r.recvline().split(b',')), 2)
    r.recvline()
    arr.append(bobBasis)

## Gorbner_basis begin

a, u, b = gens(PolynomialRing(Zmod(mod), ['a','u','b']))

f = u
ideal = []

for i in range(19):
    ideal.append((f + a * b)**7 - arr[i])
    f = (a * f + b)

I = Ideal(ideal)
B = I.groebner_basis()

## Gorbner_basis end

b7 = int((-B[0](b = 0))) % mod
a = int(-B[1](a = 0)) % mod
u = int(-B[2](u = 0, b = 1)) % mod

# Calculate the basis

for i in range(19):
    u = a * u + 1
temp = (b7 * (u + a)**7) % mod
basis = []
for i in range(n):
    basis.append((temp >> i) & 1)
basis.reverse()

r.recvuntil('Basis :\n')
r.sendline(','.join(map(str,basis)))
r.recvuntil('result :\n')
result = r.recvline().split(b',')
r.recvuntil('Alice :\n')
aliceBasis = r.recvline().split(b',')
r.recvuntil('Flag :\n')
flag = r.recvline()

# Calculate the key

key = 0
for i in range(n):
    if (basis[i] == int(aliceBasis[i])):
        key |= int(result[i])
        key <<= 1

print(decryptFlag(bytes.fromhex(flag.decode()), key))




