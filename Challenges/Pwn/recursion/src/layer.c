#define _GNU_SOURCE
#include <sys/mman.h>
#include <errno.h>
#include <unistd.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "binary_bytes.h"
extern char BINARY[];
#define BINARY_LEN (sizeof(BINARY))

uint32_t brrrr(uint32_t x) {
    uint64_t y = x + 0xDEADBEEF;
    y *= x;
    return (y & 0xFFFFFFFF);
}

int main(int argc, char* argv[]) {

    if (argc != 2) {
        printf("No arguments given >:O");
        return EINVAL;
    }

    if (strlen(argv[1]) % 4 != 0) {
        return EINVAL;
    }

    const char* fstr = argv[1];
    char xor[4] = {0};

    int len = (sizeof(xor) > strlen(fstr) ? strlen(fstr) : sizeof(xor));
    memcpy(xor, fstr, len);

    int fd = memfd_create(xor, MFD_CLOEXEC);
    if (fd < 0) {
        return errno;
    }
    
    uint32_t key = (xor[3] << 24) | (xor[2] << 16) | (xor[1] << 8) | xor[0];
    int c = 0;
    for (int i = 0; i < BINARY_LEN; i++) {
        BINARY[i] ^= (key >> (8*c++));
        if (c == 4) {
            key = brrrr(key);
            c = 0;
        }
    }

    // Write to fd
    ssize_t offset = 0;
    ssize_t rem = BINARY_LEN;
    do {
        ssize_t rc = write(fd, BINARY+offset, rem);
        if (rc == -1) {
            if (errno == EINTR) continue;
            return errno;
        }
        offset += rc;
        rem -= rc;
    } while (rem < 0);

    // Create argument
    char* const next_argv[] = {"", (argv[1] + 4), NULL};
    char* const envp[] = {NULL};
    if (fexecve(fd, next_argv, envp) == -1) {
        return errno;
    }

    return 0;
}