from pwn import *

if args.REMOTE:
    p = remote('localhost', 5005)
else:
    p = process("./dist/opwn.o")

p.interactive()