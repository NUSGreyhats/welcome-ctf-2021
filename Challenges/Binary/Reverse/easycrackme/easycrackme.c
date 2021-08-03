// gcc easycrackme.c -o easycrackme

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void check1(char* key)
{
    puts("=== Check 1 ===");
    size_t l = strlen(key);
    if (key[l-1] == '\n') key[l-1] = 0;
    if (strlen(key) != 38)
    {
        puts("-- Failed check");
        exit(1);
    }
}

void check2(char* key)
{
    puts("=== Check 2 ===");
    if (strncmp(key, "greyhats{", 9) != 0)
    {
        puts("-- Failed check");
        exit(1);
    }
}

void check3(char* key)
{
    puts("=== Check 3 ===");
    if (key[strlen(key) - 1] != '}')
    {
        puts("-- Failed check");
        exit(1);
    }
}

void check4(char* key)
{
    puts("=== Check 4 ===");
    size_t s1 = strlen("greyhats{");
    size_t s2 = strchr(key, '_') - key;

	char* out;
    char* target = "olympics";

	out = malloc((s2 - s1)/2+1);
	for (size_t i=0; i<(s2 - s1)/2; i++) {
        char c1 = key[s1+i*2];
        if (c1 >= '0' && c1 <= '9') {
            c1 -= '0';
        } else if (c1 >= 'a' && c1 <= 'f') {
            c1 += - 'a' + 10;
        }

        char c2 = key[s1+i*2+1];
        if (c2 >= '0' && c2 <= '9') {
            c2 -= '0';
        } else if (c2 >= 'a' && c2 <= 'f') {
            c2 += - 'a' + 10;
        }

        out[i] = (c1 << 4) | c2;
	}
	out[(s2 - s1)/2] = '\0';

    if (strcmp(out, target) != 0)
    {
        puts("-- Failed check");
        exit(1);
    }

    free(out);
}

void check5(char* key)
{
    puts("=== Check 5 ===");
    size_t s1 = strchr(key, '_') + 1 - key;
    size_t s2 = strchr(key + s1, '_') - key;

	char* out;
    char* target = "in";

	out = malloc((s2 - s1)+1);
	for (size_t i=0; i<s2-s1; i++) {
        out[i] = key[s1+i] ^ ((i & 1) == 0 ? 0x20 : 0x21);
	}
	out[(s2-s1)*2] = '\0';

    if (strcmp(out, target) != 0)
    {
        puts("-- Failed check");
        exit(1);
    }

    free(out);
}

void check6(char* key)
{
    puts("=== Check 6 ===");
    size_t s1 = strchr(key, '_') + 1 - key;
    s1 = strchr(key + s1, '_') + 1 - key;
    size_t s2 = strchr(key + s1, '}') - key;

	char* out;
    char* target = "tokyo";

	if ((s2 - s1) % 4 != 0)
    {
        puts("-- Failed check");
        exit(1);
    }

    size_t len = s2 - s1;
    len = len / 4 * 3;
    for (size_t i = s2 - s1; i-- > 0; ) {
        if (key[s1+i] == '=')
            --len;
        else
            break;
    }

    out = malloc(len+1);

	size_t i;
	size_t j;
	int    v;

    int invs [] = { 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58,
	59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5,
	6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
	21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28,
	29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
	43, 44, 45, 46, 47, 48, 49, 50, 51 };

	for (i=0, j=0; i<len; i+=4, j+=3) {
		v = invs[key[s1+i]-43];
		v = (v << 6) | invs[key[s1+i+1]-43];
		v = key[s1+i+2]=='=' ? v << 6 : (v << 6) | invs[key[s1+i+2]-43];
		v = key[s1+i+3]=='=' ? v << 6 : (v << 6) | invs[key[s1+i+3]-43];

		out[j] = (v >> 16) & 0xFF;
		if (key[s1+i+2] != '=')
			out[j+1] = (v >> 8) & 0xFF;
		if (key[s1+i+3] != '=')
			out[j+2] = v & 0xFF;
	}

    if (strcmp(out, target) != 0)
    {
        puts("-- Failed check");
        exit(1);
    }

    free(out);
}

int main()
{
    printf("Tell me the key: ");
    char key[64];
    fgets(key, 64, stdin);

    check1(key);
    check2(key);
    check3(key);
    check4(key);
    check5(key);
    check6(key);

    puts("*** Passed all checks *** ");
    puts("*** Submit the key as the flag *** ");

    return 0;
}