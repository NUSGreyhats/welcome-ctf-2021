#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

/*
insert:
    movabs rdx, imm64
    cmp rdx, rsi
    jne +6 or wtv, past ret
    mov rax, imm64
    ret

at the end insert:
    mov rax, -1,
    ret

when we delete we replace the insert shellcode with jmp +smth, but the smth is off by 1 :)


so we will mmap a rwx region to hold shellcode
*/

void hashmap_lookup()
void hashmap_insert()
void hashmap_delete()

void timeout(int signum) {
    printf("Timeout!");
    exit(-1);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, timeout);
    alarm(60);
}

int main() { 
    setup();
    return 0;
}

