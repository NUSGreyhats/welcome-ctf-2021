# A Note

### Challenge Details

My sources tell me that someone has left a note on my machine. Can you please help me find it? Please run this in a vm!

### Setup Instruction

Download the file. Please run it in a vm!!

### Possible hints

> Time is ticking. Tick tock tick tock...

### Key concept

- Dll injection
- Logic Bomb malware

### Solution

1. Extract the python script using pyinstaller or any preferred decompiler
2. We can see that the executable seem to be dropping 2 files to the temp folder, one executable and one dll file
3. The executable is just a injector to inject the dll file into the specified process
4. Decompile the dll file using ghidra or ida pro
5. From there we can see that the dll file gets the computer name and checks that it is 'hackerman'. This can be bypassed by setting the computer name or jumping through this condition using a debugger.
6. After that, it checks if the local time is exactly 14 Aug 2021, 7:00:00 PM GMT+08:00. This can be bypassed by setting the computer time or set using a debugger.
> Note that the time would be used as the seed for decrypting the msg
7. Now run it and it would inject a message box into notepad containing the flag.

***Alternatively, you can just manually reverse the dll file to get the encrypted message and key and xor it to get the flag.***

### Learning objective

This challenge is attempting to mimic a logic bomb malware that would be triggered when it finds the target computer name and ran at the right time. It also seeks to educate on dll injection which is a camouflage technique used by malwares to hide from the user. 

### Flag

```
greyhats{h3llo_th3r3_h4ck3rm4n_b33n_w41t1ng_4_u}
```
