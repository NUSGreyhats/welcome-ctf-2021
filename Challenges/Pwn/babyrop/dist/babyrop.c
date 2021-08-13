/* gcc -no-pie -fno-stack-protector ./babyrop.c -o babyrop */
#include <stdio.h>

char *favorite_shell = "/bin/sh";

int main() {
    puts("The time now is:");
    system("date");

    printf("My favorite shell is %s\n", favorite_shell);

    char buf[32];
    gets(buf);
    return 0;
}
