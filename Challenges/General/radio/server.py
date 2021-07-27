#!/usr/bin/env python3

import random
import math

FLAG = b'greyhats{IT5_e45Y_70_S3nD_D@T4_W17h_RaD10w4ve}'.hex()

mapp = {
    '0' : (-3, 3), '4' : (-1, 3), 'c' : (1, 3), '8' : (3, 3),
    '1' : (-3, 1), '5' : (-1, 1), 'd' : (1, 1), '9' : (3, 1),
    '3' : (-3, -1), '7' : (-1, -1), 'f' : (1, -1), 'b' : (3, -1),
    '2' : (-3, -3), '6' : (-1, -3), 'e' : (1, -3), 'a' : (3, -3)
}

f = round(random.uniform(1, 10), 2)
calculated = {}
period = 1/f

def I(t):
    index = int(t/(period*4))
    return mapp[FLAG[index]][0]

def Q(t):
    index = int(t/(period*4))
    return mapp[FLAG[index]][1]

def S(t):
    if (t in calculated):
        return calculated[t]
    real = math.sin(2 * math.pi * f * t) * I(t) + math.cos(2 * math.pi * f * t) * Q(t)
    result = real + random.uniform(-0.2, 0.2)
    calculated[t] = result
    return calculated[t]

n = 10000

print(
'''
             .==============.
   __________||_/########\_||__________
  |(O)____ : [FM 103.7] ooooo : ____(O)|      NUS Greyhats
  |  /::::\:  _________  +|+  :/::::\  | -=<  welcome you to
  |  \;;;;/: |    |    | |+|  :\;;;;/  |      Welcome CTF 2021!!!!
  |________:_ooooo+==ooo______:________|nad   
''')
print()
print()

print('QAM Constellation Diagram')
print(
'''
 0000 0100 | 1100 1000
           |
 0001 0101 | 1101 1001
 ----------|----------
 0010 0111 | 1111 1011
           |
 0011 0110 | 1110 1010
'''
)

print('Finally I managed to get close to my targets X-X')
print()
print('I suspect that the targets are sending radiowave signal with QAM to communicate with each other.')
print('Luckily, I have this radiowave signal reciever with me to intercept their message...')
print()
print('But I don\'t know how to use this machine T-T...')
print('--------------------------------------------------')
print('This machine will detect radiowave signal')
print('Input time t in microsecond to know the amplitude at time t')
print(f'However it will only allow you to query {n} different t, so use your query wisely!')
print('--------------------------------------------------')
print('Detecting radiowave signal from surrounding...')
print('RF signal found!!')
print()
print(f'Frequency = {f}(GHz)')
print(f'Total signal time = {period * 4 * len(FLAG)}(μs)')
print()
print('Starting Query...')
print('Note : 0 <= t <= Total signal time')
print(f'Input up to {n} different time (μs) seperated by space :')
t = input().split()
if (len(t) > n):
    print(f'Only {n} different time!')
    exit(0)

amplitude = []

for i in range(len(t)):
    t[i] = float(t[i])
    if (0 <= t[i] < period * 4 * len(FLAG)):
        amplitude.append(str(S(t[i])))
    else:
        print('Error : Make sure 0 <= t <= Total signal time!!')
        exit(0)

print('Amplitudes :')
print(' '.join(amplitude))
print()
print('Good luck in finding the secret message! Bye~~')