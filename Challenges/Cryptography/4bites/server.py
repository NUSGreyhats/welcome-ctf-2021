#!/usr/bin/env python3

import hashlib
from secrets import randbits

FLAG = b'greyhats{W1th_Gr03bn3R_B@s15_b@dPRNG+QKD=h@ck3d!!!}'

n = 1024
mod = 174063964518299711069668788749181472608683256519506953845957678021663479790503805130054996103933773128050079469402511808215999318969731313310594568270351166276458312376711993828352623947694042786055748003333138637438781936115718720589210722171329782548215473804182484259253296933564937708732223142168136245153

def extractBit(x, i):
    return (x >> i) & 1

class Qubit:
    def __init__(self, value, basis):
        self.value = value
        self.basis = basis
    
    def measure(self, basis):
        if (basis == self.basis):
            return self.value
        self.value = randbits(1)
        self.basis = basis
        return self.value

class User:
    def __init__(self):
        self.bits = 0
        self.basis = 0
        self.key = 0

    def getSharedKey(self, basis):
        self.key = 0
        for i in range(n - 1, -1, -1):
            basis1 = extractBit(self.basis, i)
            basis2 = extractBit(basis, i)
            if (basis1 == basis2):
                self.key <<= 1
                self.key += extractBit(self.bits, i)
        return self.key

    def sendBasis(self):
        return self.basis

class Alice(User):
    def __init__(self):
        User.__init__(self)

    def refresh(self):
        self.bits = randbits(n)
        self.basis = randbits(n)

    def sendQubits(self):
        self.refresh()
        qubits = [0 for _ in range(n)]
        for i in range(n):
            bit = extractBit(self.bits, i)
            basis = extractBit(self.basis, i)
            qubits[i] = Qubit(bit, basis)
        return qubits


class Bob(User):
    def __init__(self):
        User.__init__(self)
        self.u = randbits(n)
        self.a = randbits(n)
        self.b = randbits(n)

    def refresh(self):
        self.u = (self.u * self.a + self.a + self.b + self.a * self.b) % mod
        self.basis = self.genOutput()

    def genOutput(self):
        output = self.u**2
        output += 3 * self.b * self.u
        output += 5 * self.a * self.b
        output += 7 * self.a**3
        output += 13 * self.b**5
        output += 17
        return pow(output, 23, mod)

    def receiveQubits(self, qubits):
        self.refresh()
        self.bits = 0
        for i in range(n):
            bit = qubits[i].measure(extractBit(self.basis, i))
            self.bits += bit << i
        
    
class Challenge():
    def __init__(self):
        self.before_input = "Alice and Bob are exchanging key using Quantum key distribution (QKD)\nCan you retrieve their share key without being noticed?\n\n0 represents rectilinear basis\n1 represents diagonal basis\nSend your basis in hex"
        self.start_exchange = f"\n#### Start Key Exchange\n\nAlice just sent {n} qubits to Bob, measure the qubits by specificing the basis.\nBasis :"
        self.alice = Alice()
        self.bob = Bob()

    def encryptFlag(self, msg, shared_secret):
        sha512 = hashlib.sha512()
        sha512.update(str(shared_secret).encode('ascii'))
        key = sha512.digest()[:len(FLAG)]
        return bytes([i[0] ^ i[1] for i in zip(key, msg)])

    def challenge(self):
        print(self.before_input)
        for _ in range(5):
            print(self.start_exchange)

            # Alice send qubits
            qubits = self.alice.sendQubits()
            
            # Interception Begins
            try:
                basis = bytes.fromhex(input())
            except:
                print('Error: The input must be a valid hexadecimal string')
                exit(0)
            
            assert len(basis) == n//8

            basis = int.from_bytes(basis, 'big')

            result = 0

            for i in range(n):
                bit = qubits[i].measure(extractBit(basis, i))
                result += bit << i

            print("Measure result :")
            print(hex(result))

            # Interception Ends
            
            # Bob receive qubits
            self.bob.receiveQubits(qubits)
            print('Bob has received and measured the qubits')

            # Alice send basis
            aliceBasis = self.alice.sendBasis()
            print('The Basis used by Alice :')
            print(hex(aliceBasis))

            # Bob send basis
            bobBasis = self.bob.sendBasis()
            print('The Basis used by Bob :')
            print(hex(bobBasis))

            # check shared key
            aliceKey = self.alice.getSharedKey(bobBasis)
            bobKey = self.bob.getSharedKey(aliceBasis)
            if (aliceKey != bobKey):
                print("Error Detected in shared key!!! Someone must be watching us!!! Let's try again")
            else :
                # encrypt flag with shared key
                print('Encrypted Flag :')
                c = self.encryptFlag(FLAG, aliceKey)
                print(c.hex())
                exit(0)
        
        print('Too many failures, perhaps we should change our communication channel..')

Challenge().challenge()