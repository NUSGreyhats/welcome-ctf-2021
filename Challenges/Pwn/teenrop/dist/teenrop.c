/* gcc -fno-stack-protector ./teenrop.c -o teenrop */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>


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

char* menu = "Simple Phonebook ###\n1) Set contact\n2) Get contact";

unsigned long long read_ull()
{
    char buf[32];
    gets(buf);
    return strtoull(buf, 0, 10);
}

int main()
{
    setup();

    int choice;
    int exit = 0;

    unsigned long long nums[16];
    unsigned long long idx, value;

    do {
        puts(menu);
        printf("Choice: ");
        choice = read_ull();
        switch(choice)
        {
        case 1:
            idx = read_ull();
            value = read_ull();
            nums[idx] = value;
            break;
        case 2:
            idx = read_ull();
            value = nums[idx];
            printf("Value: %llu\n", value);
            break;
        default:
            exit = 1;
            break;
        }
    } while(!exit);

    puts("Bye");

    return 0;
}
