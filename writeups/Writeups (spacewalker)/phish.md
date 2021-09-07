# Phish

We are given a number A, the product of 4 primes, as well as the value of phi(A). (Note that
if we let p, q, r, s be the primes, phi(A) = (p-1)(q-1)(r-1)(s-1).) We are given a flag,
but it is encrypted via RSA, where the primes are generated from one of p, q, r, s.
So, since we are not in the mood to break RSA for a CTF, let's focus on factoring A.

## Mathematical Insights

Googling 'factoring number with totient' gives [this](https://math.stackexchange.com/questions/191896/does-knowing-the-totient-of-a-number-help-factoring-it). I will try my best to explain it. (All the other answers suck, as they assume n is a semiprime. Sigh.)

We know that phi(n) must divide lambda(n), the least common
multiple of all the orders of elements of Z/nZ (wrt multiplication). So, we know that there must exist some divisor t of phi(n), for which 2t is divisible by lambda(n), but t is not. (t will have one less 2 in its prime factorization than lambda(n)).

What effect does this have? Consider a random r in [1, n - 1], and a prime divisor p of n. If r is a quadratic residue modulo p, then there must exist some k such that k^2 = r modulo p. Therefore,
```
r^t - 1 = k^2t - 1 = 0 (modulo p)
          (since k^(2t) = (k^lambda(n))^(???) = 1)
```

So if we compute gcd(r^t - 1, n), this number will be divisible by p.

What if r is not a quadratic residue? I don't know. gcd(r^t - 1, n) might still be divisible by p. But in that case, we'd just probably be happy, as long as the value of the gcd doesn't become n. This is because, if it is less than n, and greater than one, we know that we've found a nontrivial factor of n! (That is an exclamation mark, not a factorial symbol.)

So we just keep factoring on this way until we finally get to all numbers being prime.

## Implementation

Here is code:

```python
from random import randint
from math import gcd

def tryFindFactor(n, phi, tries=100):
    for _ in range(tries):
        r = randint(2, n - 1)
        phi2s = phi * 2
        while phi2s % 2 == 0:
            phi2s //= 2
            g = gcd((pow(r, phi2s, n) - 1) % n, n)
            if 1 < g and g < n:
                return g
    else:
        print("!!! tryFindFactor failed after", tries, "tries")

# A, phi, N and c are as in the output file

def tryBreakDown(n, phi):
    print("TBD", n, phi)
    print("size of n", len(bin(n)[2:]))
    if len(bin(n)) <= 2050: # we know we are looking for 2048-bit primes, so stop if we go below 2048-bits
        return [n]
    x = n
    while len(bin(x)) > 2050:
        x = tryFindFactor(n, phi)
        if x is None:
            print("!!! tryFindFactor failed, results may be meaningless")
            return [n]
    return [x] + tryBreakDown(n // x, phi // (x - 1))

factors = (tryBreakDown(A, phi))

# this code is just to invert the encryption
from gmpy2 import next_prime
import random
from Crypto.Util.number import long_to_bytes

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

for fac in factors:
    random.seed(fac)
    p = next_prime(random.randint(1 << 2047, 1 << 2048))
    q = next_prime(random.randint(1 << 2047, 1 << 2048))
    if (p * q != N):
        continue
    print("proceeding with", fac)
    phi = (p - 1) * (q - 1)
    e = 0x10001
    d = modinv(e, phi)
    m = pow(c, d, N)
    FLAG = long_to_bytes(m)
    print(FLAG)

```
