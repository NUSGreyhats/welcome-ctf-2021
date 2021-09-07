
# Potato

The flag is encoded in the coefficients of a polynomial g
, a member of GF(2^n) where n = 272. However, we are not given g directly. Instead, we have g^A, for some given A.
Our task is to find g.

### A member of what?

GF(2^n) is the finite field of order 2^n. A _field_ in math is
a ring where all nonzero elements are units. In short, you can
add, subtract, multiply, and divide by things in this set, and 
it will mostly make sense. (But I think that I am still not describing it properly. You can try looking online for more accessible explanations. For now, all you will need to know is that F_p, the set of integers modulo a prime p, is also a field under the usual operations.)

We can actually represent elements of GF(2^n) as a polynomial of degree at most n, where the coefficients are either 0 or 1. 
To enforce this degree constraint when multiplication arises,
we can divide by some irreducible polynomial of degree n (the 
`modulus` in the input).

## Extracting the polynomial

Anyway. I spend nearly one hour googling things like "nth
roots in finite fields", only to stumble upon the fact that
you can just take it to the power of 1/A. Remember how I said that GF(2^n) works like F_p? Well, RSA does a very similar thing
with F_p. The ciphertext is the number c^e mod N, and you decipher it by turning it into (c^e)^d mod N, where it is known that d = 1/e (mod phi(N)). 

So what is our equivalent for phi(N) here? phi(N) is the order, or the number of elements, F_p has. The order of GF(2^n) is (2^n - 1) (you can verify this by the polynomial representation. Remember to exclude zero, since we're treating it as a group under multiplication.) Therefore, our plan is

- Compute B = A^-1 mod (2^n - 1)
- Compute (g^A)^B 
- Extract the flag from g^(AB) = g

Which we do using this Python program:

```python
from sympy import * # sympy!
x = symbols('x')

# n, modulus, A and coeff are as in the output
# just replace the ^ of the modulus with **

# Helper functions, since I couldn't be bothered
# to actually learn how sympy worked
def coeff_arr_to_poly(cfs):
    return sum(v * x**i for i, v in enumerate(cfs))

def reduce_coeffs_mod2(poly):
    coeffs = poly.as_poly(x).all_coeffs()[::-1]
    return coeff_arr_to_poly([v % 2 for v in coeffs])

def pmod(a, b):
    return reduce_coeffs_mod2(div(a, b)[1])

# This might be a library function, but this sort of
# algorithm is common in competitive programming, so eh
# This returns poly^e mod m, with coefficients taken mod 2
def scuff_modexp(poly, e, m):
    if e == 0: 
        return 1
    else:
        submult = scuff_modexp(pmod(poly * poly, m), e // 2, m)
        ans = pmod((1 if e % 2 == 0 else poly) * submult, m)
        return ans

ga = coeff_arr_to_poly(coeff) # get the poly representation

# some copy-pasted modular inverse code
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

rev_exp = modinv(a, 2**n - 1)
print("computed revexp", rev_exp)

# this is the value of g. computed with this line:
# print(scuff_modexp(ga, rev_exp, mod))
 
g = x**271 + x**269 + x**268 + x**267 + x**266 + x**265 + x**262 + x**259 + x**257 + x**251 + x**250 + x**247 + x**244 + x**241 + x**238 + x**235 + x**233 + x**231 + x**230 + x**227 + x**226 + x**219 + x**217 + x**215 + x**213 + x**211 + x**210 + x**209 + x**207 + x**206 + x**203 + x**201 + x**199 + x**198 + x**197 + x**196 + x**195 + x**193 + x**191 + x**190 + x**187 + x**186 + x**182 + x**179 + x**178 + x**177 + x**175 + x**169 + x**167 + x**166 + x**165 + x**164 + x**163 + x**161 + x**159 + x**157 + x**155 + x**154 + x**149 + x**148 + x**146 + x**145 + x**143 + x**138 + x**137 + x**135 + x**131 + x**130 + x**127 + x**125 + x**124 + x**121 + x**115 + x**114 + x**110 + x**109 + x**108 + x**106 + x**105 + x**103 + x**100 + x**99 + x**98 + x**97 + x**93 + x**92 + x**90 + x**89 + x**83 + x**82 + x**75 + x**73 + x**71 + x**70 + x**68 + x**67 + x**66 + x**65 + x**63 + x**62 + x**59 + x**58 + x**57 + x**53 + x**51 + x**50 + x**49 + x**47 + x**42 + x**41 + x**36 + x**34 + x**33 + x**31 + x**28 + x**27 + x**26 + x**25 + x**23 + x**21 + x**18 + x**17 + x**14 + x**11 + x**10 + x**9 + x**7 + x**6 + x**5 + x**2 + x

g_coeffs = (g.as_poly(x).all_coeffs()[::-1])
g_str = ''.join(str(v) for v in g_coeffs)
print(g_str)

from Crypto.Util.number import long_to_bytes

thing = long_to_bytes(int(g_str, 2))
print(thing) # flag!
```