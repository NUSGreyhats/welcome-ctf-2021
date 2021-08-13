import hashlib
from cipher_solver.simple import SimpleSolver

def decryptFlag(msg, shared_secret):
    sha512 = hashlib.sha512()
    sha512.update(str(shared_secret).encode('ascii'))
    key = sha512.digest()[:len(msg)]
    return bytes([i[0] ^ i[1] for i in zip(key, msg)])

words = open('fries.txt', 'r').read()

s = SimpleSolver(words)
s.solve()
key = ' '.join(s.plaintext().split()[-5:])
enc = open('encrypted_flag', 'rb').read()
print(key)
print(decryptFlag(enc, key))