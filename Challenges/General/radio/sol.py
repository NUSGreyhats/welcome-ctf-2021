from pwn import *
from math import sin, cos
from Crypto.Util.number import long_to_bytes

r = remote('localhost', 3000)

con = [
    [0,4,12,8],
    [1,5,13,9],
    [3,7,15,11],
    [2,6,14,10]
]

def mapp1(x):
    minimum = 3
    index = 0
    arr = [-3, -1, 1, 3]
    for i in range(4):
        if abs(x-arr[i]) < minimum:
            index = i
            minimum = abs(x-arr[i])
    return index

def mapp2(x):
    minimum = 3
    index = 0
    arr = [3, 1, -1, -3]
    for i in range(4):
        if abs(x-arr[i]) < minimum:
            index = i
            minimum = abs(x-arr[i])
    return index

r.recvuntil('Frequency = ')
f = float(r.recvuntil('(')[:-1])
t = (1/f)
r.recvuntil('Total signal time = ')
total = float(r.recvuntil('(')[:-1])
n = int(total/t/4)
rounds = 100

times = []
for i in range(n):
    for j in range(rounds):
        times.append(t * 4 * i + t * 4 / rounds * j)

r.sendline(' '.join(map(str,times)))
r.recvuntil('Amplitudes :\n')
amp = list(map(float, r.recvline().split()))

I = []
Q = []

for i in range(n):
    for j in range(rounds):
        index = i * rounds + j
        I.append(amp[index] * sin(2 * math.pi * f * times[index]) * 2)
        Q.append(amp[index] * cos(2 * math.pi * f * times[index]) * 2)

ans = 0

for i in range(n):
    
    arr = I[i*rounds : (i+1) * rounds]
    maxi = max(arr); mini = min(arr)
    a = mapp1((maxi + mini)/2)

    arr = Q[i*rounds : (i+1) * rounds]
    maxi = max(arr); mini = min(arr)
    b = mapp2((maxi + mini)/2)

    ans <<= 4
    ans += con[b][a]

print(long_to_bytes(ans))
