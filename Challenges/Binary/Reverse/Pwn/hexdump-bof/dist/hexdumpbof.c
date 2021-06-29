#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define SZ 0x20
#define OVERFLOW_SZ 0x10
#define TOTAL_SZ (SZ+OVERFLOW_SZ)

void print_buffer(char* buffer) {
    for (int i = 0; i < TOTAL_SZ * 3 + 4; i++) printf("-");
    printf("\n");
    printf("%-95s | %-23s | %-23s \n", "contents", "saved base ptr", "return address");
    for (int i = 0; i < TOTAL_SZ * 3 + 4; i++) printf("-");
    printf("\n");

    for (int i = 0; i < SZ; i++) {
        printf("%02x ", (buffer[i] & 0xff));
    }
    printf("| ");
    for (int i = SZ; i < SZ + 8; i++) {
        printf("%02x ", (buffer[i] & 0xff));
    }
    printf("| ");
    for (int i = SZ+8; i < SZ + 16; i++) {
        printf("%02x ", (buffer[i] & 0xff));
    }
    printf("\n");
    for (int i = 0; i < TOTAL_SZ * 3 + 4; i++) printf("-");
    printf("\n");
}

void vuln() {
    char buffer[SZ];
    memset(buffer, 0, SZ);

    while(1) {
        printf("Input:\n");
        fgets(buffer, TOTAL_SZ, stdin);
        print_buffer(buffer);
        printf("\nsaved base pointer\t: %p\nreturn address\t\t: %p\n", *((long*)(buffer + SZ)), *((long*)(buffer + SZ + 8)));
        printf("Go again? (Y/N) ");
        char again;
        scanf("%c", &again);
        printf("You entered: %c\n", again);
        if (again == 'N')
            break;
    }
}

void win() {
    system("/bin/sh");
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
    printf("=== HexDump Master ===\n");
    printf("Prints the input back at you, in hexdump format, including some extra data... I wonder what that data is :)\n");
    printf("Btw, there is an inaccessible function at %p (win). What will it do?\n\n", win);
    vuln();
    return 0;
}