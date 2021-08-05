#include <stdio.h>

/* gcc -no-pie -fno-stack-protector ./fetusrop.c -o fetusrop */
void win(int a, int b)
{
    if (a == 0xcafe && b == 0x1337)
        system("/bin/bash");
}

int main(){
    char buf[32];
    gets(buf);
    return 0;
}
