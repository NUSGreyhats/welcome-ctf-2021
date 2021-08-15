import random
from gmpy2 import next_prime
from Crypto.Util.number import getPrime, bytes_to_long

f = open('output.txt','w')

FLAG = b'???'

primes = [getPrime(2048) for _ in range(4)]

A = 1
phi = 1

for p in primes:
    A *= p
    phi *= p-1

f.write(f'A = {A}\n')
f.write(f'phi = {phi}\n')

random.seed(primes[0])

# Standard RSA
p = next_prime(random.randint(1 << 2047, 1 << 2048))
q = next_prime(random.randint(1 << 2047, 1 << 2048))

N = p*q
m = bytes_to_long(FLAG)
e = 0x10001
c = pow(m, e, N)

f.write(f'N = {N}\n')
f.write(f'c = {c}\n')