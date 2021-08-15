#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

typedef long long num;
typedef char byte;

byte* hashmap;
num hashmap_len;

void hashmap_lookup(num k, num* v) {
    *v = ((num (*)(num))hashmap)(k); // ezpz liao, O(1) onli!
}

void hashmap_insert(num k, num v) {
    if(v == -1) return;

    // magic incantation to add entry as code. still O(1), of course

    byte* entry;
    entry = &hashmap[26 * hashmap_len];
    entry[0] = 0x48;
    entry[1] = 0xBA;
    *((num*)&entry[2]) = k;
    entry[10] = 0x48;
    entry[11] = 0x39;
    entry[12] = 0xFA;
    entry[13] = 0x75;
    entry[14] = 0x0b;
    entry[15] = 0x48;
    entry[16] = 0xB8;
    *((num*)&entry[17]) = v;
    entry[25] = 0xC3;

    entry = &hashmap[26 * ++hashmap_len];
    entry[0] = 0x48;
    entry[1] = 0xB8;
    *((num*)&entry[2]) = -1;
    entry[10] = 0xC3;
}

void hashmap_delete(num idx) {
    byte* entry;
    entry = &hashmap[26 * idx];
    memset(entry, 0x90, 26);
    entry[0] = 0xEB;
    entry[1] = 0x19;
}

num read_int(char* prompt) {
    num i;
    printf("%s: ", prompt);
    scanf("%llu", &i);
    return i;
}

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

    printf("========== O(pwn) HashMap as a Service ==========\n");

    hashmap = mmap(
        (void*)0x1337000,                       // allocate memory @ 0x1337000 ..
        0x1000,                                 // with size 0x1000 ..
        PROT_READ | PROT_WRITE | PROT_EXEC,     // with perms read-write-exec (rwx)
        MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    if (hashmap < 0) {
        perror("cannot allocate hashmap");
        exit(-1);
    }

    while(1) {
        printf("[1] Insert\n");
        printf("[2] Lookup\n");
        printf("[3] Delete\n");
        num opt = read_int("Option");
        num k, v, i;
        switch(opt) {
            case 1:
                k = read_int("Key");
                v = read_int("Value");
                hashmap_insert(k, v);
                break;
            case 2:
                k = read_int("Key");
                hashmap_lookup(k, &v);
                if (v == -1) {
                    printf("Not found\n");
                } else {
                    printf("Value: %lld\n", v);
                }
                break;
            case 3:
                i = read_int("Index");
                hashmap_delete(i);
                break;
        }
    }


    return 0;
}

