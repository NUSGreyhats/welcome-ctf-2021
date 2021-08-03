/* gcc -no-pie -fno-stack-protector ./bof.c -o bof */
#include <stdio.h>

void vuln()
{
    char buf[32];
    gets(buf);
}

int main()
{
    puts("How are you?");
    vuln();
    return 0;
}
