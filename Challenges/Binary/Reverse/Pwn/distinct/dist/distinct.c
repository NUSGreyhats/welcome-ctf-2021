#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define SZ 0x10

typedef void (*hh)(void);

unsigned long long nums[SZ];
hh handler;

void sort(unsigned long long* arr, unsigned long long len) {
    unsigned long tmp = 0;
    for(int i = 0; i <= len; i++) {
        for(int j = i; j <= len; j++) {
            if (arr[i] < arr[j]) continue;
            tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
        }
    }
}

void unique() {
    printf("Elements are unique\n");
}

void repeated() {
    printf("Elements are repeated\n");
}

int again() {
    char inp[8];
    printf("Enter Again? (Y/N) ");
    scanf("%6s", inp);
    return inp[0] != 'N';
}

void check() {
    do {
        handler = &unique;

        memset(nums, 0, sizeof nums);

        for (int i = 0; i < SZ; i++) {
            printf("#%d: ", i);
            scanf("%llu", &nums[i]);
        }

        sort(nums, SZ);

        for (int i = 0; i < SZ-1; i++) {
            if (nums[i] == nums[i+1]) {
                handler = &repeated;
            }
        }

        printf("You have entered: \n");

        for (int i = 0; i < SZ; i++) {
            printf("%llu ", nums[i]);
        }
        printf("\n");
    }
    while (again());
}

void timeout(int signum) {
    printf("Timeout!");
    exit(-1);
}

void win() {
    system("/bin/sh");
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
    check();
    handler();
    return 0;
}