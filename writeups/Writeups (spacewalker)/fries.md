# Fries

We are given a wordlist, except it's a massive [cryptogram](https://en.wikipedia.org/wiki/Cryptogram). We are also given the flag, but it is encrypted with a one-time pad,
whose key is derived from the wordlist.

First I tried to do a simple frequency analysis on the wordlist to get the words, but I failed spectacularly. So I decided to not reinvent the wheel and use a cryptogram solver like [this one](https://www.quipqiup.com/) on the last 100 words or so. After that, I just coded decryption. I was stuck on this for a while since I was using the ciphered wordlist for decryption, lol

Code:
```python
from collections import defaultdict

enc_wordlist = []
with open("fries.txt", "r") as fries:
    enc_wordlist = [s.strip() for s in fries.readlines()]

# I gave up... this is quipqiupped from the last 100 words
decrypted = """rhyolites goozle etym plashy pedophobia unpainful floralize slabs cartmaking frenchman newsprint histiophorus larked
stictidaceae metropolite unjogging ballsy hyperprophetic corolla montanas overcrowdedly alnagership stackhousiaceae wargus ravens
shipways flan perplexedness epistemonical visaed mongol fimbricated gymmal syndeses indictional livening geneticism wehee dringle
imposterous lithobiid breathier cockles unavailability idyller autospray prussianize amidols biochron hawing breezed aliyah
unslashed stumpiness tewit cuboctahedron transgressions postanal noughtly osmotherapy nominators lagenae ungabled macabre
sublanguage sheuchs obside wakif peppershrike albigenses prenegotiated unaffiliated interjugal supernumeraryship noosers arne
ditchdown misgraded tpke kibbutz chalazogam birrus smoucher midstout sabbatean chymia dromic rewear nonfunded compurgatorial
gusseting pertusaria bimanal industrochemical acierates stethy cherubimical nontarnishing achoke bechirp""".split()
encrypted = enc_wordlist[-100:]

decryptor = defaultdict(lambda: '?')
for a, b in zip(decrypted, encrypted):
    assert(len(a) == len(b))
    for aa, bb in zip(a, b):
        decryptor[bb] = aa

relevant = enc_wordlist[:10000]
for w in relevant[-5:]:
    print(''.join(decryptor[c] for c in w))

relevant = decrypted[-5:]
with open("fries_enc_flag", "rb") as enc_flag:
    shared_secret = " ".join(relevant[-5:])
    enc_msg = bytearray(enc_flag.read())
    print(shared_secret)
    # from encryptor
    import hashlib
    sha512 = hashlib.sha512()
    sha512.update(str(shared_secret).encode('ascii'))
    key = sha512.digest()[:len(enc_msg)]
    print(enc, e) for k, e in zip(key, enc_msg)])
    print(''.join([chr(k ^ e) for k, e in
        zip(key, enc_msg)]))

```
