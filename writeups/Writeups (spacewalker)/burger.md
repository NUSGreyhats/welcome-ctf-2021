# Burger

We are given a service that, given a string `S`, will split
`S | flag` into blocks of 16 characters (after padding with zero bytes), hash each with SHA-512,
and give us the hash of each block. From this, we have to acquire the flag.

The idea is the same as breaking AES-ECB, in that we want to limit the number of unknown characters in a block. That way, we can easily brute force what those characters are.

We start by sending `S` whose length is such that the last character of the flag is in its own block, together with 15 bytes of padding. Since we only have 256 hashes to go through, we can learn what this character is. 

```
                              this block can only have
                              hashes from a very small
                              set 
AAAAAAAAAAAAAAAA | AA ..... | }\x00\x00...
```

We then increase our padding's length by one, adding another character to the last block, and brute-forcing what that character is. We can continue in this manner until we find the whole flag. Just take note that the character you want may not be in the last block, as you go into smaller and smaller positions in the string.

> Actually, I think during the CTF, my exploit code failed when it got to the first 2 characters, but by that point, I had ??eyhats{...} so I didn't need to look for those two characters.

Code:

```python
from pwn import *
from math import ceil

#r = process("server_public.py")
r = remote("challs1.nusgreyhats.org", 5210)
r.clean()

def get_hash(s):
    assert len(s) % 2 == 0
    assert all(c in "abcdef1234567890" for c in s)
    r.send((s+"\n").encode())
    out = r.recv(numb=10**5, timeout=2).decode().split("\n")
    print("hash request gives", out[1])
    return out[1]

import hashlib

block = 16

def hash_block(block):
    assert(len(block) == block)
    sha512 = hashlib.sha512()
    sha512.update(block.encode())
    return sha512.hexdigest()[:block * 2]

def pad_block(bl):
    return bl + '\0' * (block - (bl % block))

chars_extracted = "\0" * 15 # reversed
for push_len in range(9, 9 + 54):
    tail_end = chars_extracted[-15:]
    expected_chars = {}
    for c in range(0, 256):
        hashed = hash_block(chr(c) + tail_end[-15:][::-1])
        expected_chars[hashed] = c
    print("result of a is ", hash_block('a' + tail_end[-15:][::-1]))
    print("that was block", 'a' + tail_end[-15:][::-1])
    result = get_hash("aa" * push_len)
    blocks = [result[i:i + 2*block] for i in range(0, len(result), 2*block)]
    print("need block", -1 - (push_len - 8) // block, "on pl", push_len, "id", push_len - 9)
    print("out of", blocks)
    need_block = blocks[-1 - (push_len - 8) // block]
    print("that is", need_block)
    chars_extracted += chr(expected_chars[need_block])
    print("got", chars_extracted[::-1])
```