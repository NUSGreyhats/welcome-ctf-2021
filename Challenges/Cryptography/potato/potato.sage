from Crypto.Util.number import bytes_to_long, getPrime

FLAG = b"???"

n = len(FLAG) * 8
F = GF(2^n, 'x')
x = F.gen()

bits = format(bytes_to_long(FLAG), f'0{n}b')

g = 0

for i in range(n):
    if (bits[i] == '1'):g += x^i

a = getPrime(n)
A = g^a
coefficient = A.polynomial().list()

print(f'n = {n}')
print(f'mod = {F.modulus()}')
print(f'a = {a}')
print(f'coeff = {coefficient}')