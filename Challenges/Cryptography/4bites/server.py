import hashlib
from random import randint

FLAG = b'greyhats{b@dPRNG+QKD=h@ck3d!!!}'

n = 1024
mod = 174063964518299711069668788749181472608683256519506953845957678021663479790503805130054996103933773128050079469402511808215999318969731313310594568270351166276458312376711993828352623947694042786055748003333138637438781936115718720589210722171329782548215473804182484259253296933564937708732223142168136245153

class Qubit:
    def __init__(self, value, basis):
        self.value = value
        self.basis = basis
    
    def measure(self, basis):
        if (basis == self.basis):
            return self.value
        self.value = randint(0, 1)
        self.basis = basis
        return self.value

class Alice:
    def __init__(self):
        self.bits = []
        self.basis = []
        self.qubits = []
        self.key = 0

    def refresh(self):
        self.bits = [randint(0, 1) for i in range(n)]
        self.basis = [randint(0, 1) for i in range(n)]
        self.qubits = [Qubit(self.bits[i], self.basis[i])for i in range(n)]

    def getSharedKey(self, basis):
        self.key = 0
        for i in range(n):
            if (self.basis[i] == basis[i]):
                self.key |= self.bits[i]
                self.key <<= 1
        return self.key

    def sendQubits(self):
        self.refresh()
        return self.qubits

    def sendBasis(self):
        return self.basis

class Bob:
    def __init__(self):
        self.u = randint(0, 1 << n)
        self.a = randint(0, 1 << n)
        self.b = randint(0, 1 << n)
        self.basis = []
        self.bits = []
        self.key = 0

    def refresh(self):
        self.basis = []
        self.u = (self.u * self.a + self.b) % mod
        temp = (self.u + self.b * self.a)**7 % mod
        for i in range(n):
            self.basis.append((temp >> i) & 1)
        self.basis.reverse()

    def getSharedKey(self, basis):
        self.key = 0
        for i in range(n):
            if (self.basis[i] == basis[i]):
                self.key |= self.bits[i]
                self.key <<= 1
        return self.key

    def measure(self, qubits):
        self.refresh()
        self.bits = []
        for i in range(n):
            bit = qubits[i].measure(self.basis[i])
            self.bits.append(bit)
    
    def sendBasis(self):
        return self.basis
        
    
class Challenge():
    def __init__(self):
        self.before_input = "Alice and Bob are exchanging key using Quantum key distribution (QKD) \nCan you retrieve their share key without being noticed?"
        self.start_exchange = f"\n#### Start Key Exchange\n\nAlice just sent {n} qubits to Bob, measure the qubits by specificing the basis.\n0 represents rectilinear basis \n1 represents diagonal basis \nSend your basis seperated by ',' \nBasis :"
        self.alice = Alice()
        self.bob = Bob()

    def encryptFlag(self, msg, shared_secret):
        sha512 = hashlib.sha512()
        sha512.update(str(shared_secret).encode('ascii'))
        key = sha512.digest()[:len(FLAG)]
        return bytes([i[0] ^ i[1] for i in zip(key, msg)])

    def challenge(self):
        print(self.before_input)
        for _ in range(20):
            print(self.start_exchange)
            qubits = self.alice.sendQubits()
            
            # Split client input by ','
            basis = input().split(',')
            
            assert len(basis) == n

            result = []

            for i in range(n):
                basis[i] = int(basis[i])
                assert 0 <= basis[i] <= 1
                result.append(qubits[i].measure(basis[i]))

            print("Measure result :")
            print(",".join(map(str, result)))
            
            self.bob.measure(qubits)
            print('Bob has received and measured the qubits')

            aliceBasis = self.alice.sendBasis()
            print('The Basis used by Alice :')
            print(",".join(map(str, aliceBasis)))

            bobBasis = self.bob.sendBasis()
            print('The Basis used by Bob :')
            print(",".join(map(str, bobBasis)))

            aliceKey = self.alice.getSharedKey(bobBasis)
            bobKey = self.bob.getSharedKey(aliceBasis)
            if (aliceKey != bobKey):
                print("Error Detected in shared key!!! Someone must be watching us!!!")
            else :
                print('Encrypted Flag :')
                c = self.encryptFlag(FLAG, aliceKey)
                print(c.hex())
                break
        else :
            print('Too many failures, goodbye!')

Challenge().challenge()