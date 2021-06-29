#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

typedef unsigned long long value;

typedef struct Node {
    value value;
    Node* left;
    Node* right;
} Node;

Node* root = NULL;

void insert(value value) {
    Node* ins = malloc(sizeof(Node));
    ins->value = value;

    if (root == NULL) {
        root = ins;
        return;
    }


}

void delete(value value) {

}

void view() {

}

void menu() {
    puts("==== CS2040 Assignment 1 ====");
    puts("[1] Insert Value");
    puts("[2] Delete Value");
    puts("[3] View in-order traversal of tree");
    puts("[4] Quit, but give me 5.0 CAP and a A+ for this mod");
}

value prompt(char* text) {
    int opt;
    printf("%s: ", text);
    scanf("%llu", &opt);
    return opt;
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
    menu();

    while(1) {
        int opt = prompt("Option");
        if (opt == 1)
            insert(prompt("Node Value"));
        else if (opt == 2)
            delete(prompt("Node Value"));
        else if (opt == 3)
            view();
        else if (opt == 4)
            break;
    }
    return 0;
}