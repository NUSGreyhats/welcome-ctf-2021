import string
import random
import hashlib

FLAG = b'???'

alpha = list(string.ascii_lowercase)
random.shuffle(alpha)

# OTP xor encryption
def encryptFlag(msg, shared_secret):
    sha512 = hashlib.sha512()
    sha512.update(str(shared_secret).encode('ascii'))
    key = sha512.digest()[:len(msg)]
    return bytes([i[0] ^ i[1] for i in zip(key, msg)])

def encrypt(word):
    word = list(word)
    for i in range(len(word)):
        word[i] = alpha[ord(word[i]) - ord('a')]
    return "".join(word)

words = open('words.txt', 'r').read().split('\n')

random.shuffle(words)

words = words[:10000]
key = " ".join(words[-5:])

for i in range(len(words)):
    words[i] = encrypt(words[i])

output = open('fries.txt', 'w')
output.write("\n".join(words))

enc = encryptFlag(FLAG, key)

print(key)

open('encrypted_flag', 'wb').write(enc)