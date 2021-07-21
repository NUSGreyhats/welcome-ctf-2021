/* gcc -no-pie -fno-stack-protector ./kidrop.c -o kidrop */
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
