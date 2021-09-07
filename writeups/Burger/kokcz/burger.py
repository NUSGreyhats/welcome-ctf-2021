import hashlib
import socket

def getChar(knownChars: str, hash: str) -> chr:
    for i in range(256):
        testChar = chr(i)
        testHash = hashlib.sha512((knownChars + testChar).encode()).hexdigest()[:32]
        if testHash == hash:
            return testChar

def getHashes(maxChars: int) -> list:
    host = "challs1.nusgreyhats.org"
    port = 5210
    hashes = []
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.recv(1024)                # discard welcome message
    for i in range(maxChars):
        s.send(('61' * i + '\n').encode())
        hashes.append(s.recv(1024).decode().split('\n')[1])
    s.close()
    return hashes
        
def getFlag(flagLen: int) -> str:
    hashes = getHashes(16)
    flag = ''
    known15 = 'a'*15
    for i in range(flagLen):
        listIndex = 15 - (i % 16)
        hashStart = (i // 16) * 32
        hash32 = hashes[listIndex][hashStart:hashStart + 32]
        guessChar = getChar(known15, hash32)
        flag += guessChar
        known15 = known15[1:] + guessChar
    return flag

print(getFlag(56))
