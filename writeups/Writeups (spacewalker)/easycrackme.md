# Easycrackme

As the name implies, it is a crackme. I'm still new to reversing so I can't say it's easy, though.

We jump to main, and find that it applies a series
of 6 checks to the input: (Code is decompiled using Ghidra, some variables possibly renamed by me)

```c
  printf("Tell me the key: ");
  fgets(key,0x40,stdin);
  check_1(key);
  check_2(key);
  check_3(key);
  check_4(key);
  check_5(key);
  check_6(key);
  puts("*** Passed all checks *** ");
  puts("*** Submit the key as the flag *** ");
```

From here, we need to look at each check and see what it does.

- Check 1 is if the string's length is 0x26, or 38.
- Check 2 is if the string's first 9 characters are `greyhats{`.
- Check 3 is if the string's last character is a `}`.

The checks get more complicated from here.

### Check 4

Check 4 first finds an underscore in the string. It then goes through characters in pairs, from just after the `{` to before the `_`, turning `'0', ..., '9'` into zero to nine, and 
`'A', ..., 'F'` to 10 to 15, leaving other characters untouched. It then sets a character in an initially empty string:
```c
__s1[i] = (byte)((int)firstChar << 4) | secondChar
```
and in the end, checks if that string is `olympics`. So to pass this check, we just need to add hex-encoded `olympics` in the flag.

### Check 5

Check 5 takes a substring between the first and second underscore of the string. It then XORs `[0x20, 0x21, 0x20, 0x21, ...]` to the string, as if decrypting a one-time pad. At the end, it checks if the string is `in`. So we just need to XOR `in` with `\x20\x21` to pass the check.

> There is a bug here, where the substring is not properly null-terminated. Thankfully, the bug does not arise on my teammate's computer, where the substing probably already contains null bytes by sheer luck.

### Check 6

Check 6 uses equal signs. That's all I took from it, since my
teammate (correctly) guessed that it base64 decodes the string, then checks if it is equal to `tokyo`.

### Putting the checks together...

we get `greyhats{6f6c796d70696373_IO_dG9reW8=}`, which is also the flag.