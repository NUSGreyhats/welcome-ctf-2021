/* gcc -no-pie -fno-stack-protector ./kidrop.c -o kidrop */
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>

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

void vuln()
{
    char buf[32];
    gets(buf);
}

int main()
{
    setup();
    puts("How are you?");
    vuln();
    return 0;
}
