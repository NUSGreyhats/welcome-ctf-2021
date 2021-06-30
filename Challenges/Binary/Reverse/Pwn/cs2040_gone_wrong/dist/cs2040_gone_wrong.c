#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

typedef unsigned long long Value;

typedef struct Node {
    Value value;
    Node* left;
    Node* right;
} Node;

Node* root = NULL;

void insert(Value value) {
    Node* ins = malloc(sizeof(Node));
    ins->value = value;

    if (root == NULL) {
        root = ins;
        return;
    }

    Node* cur = root;
    while(1) {
        if (value > cur->value) {
            if (cur->right == NULL) {
                cur->right = ins;
                return;
            } else {
                cur = cur->right;
            }
        } else {
            if (cur->left == NULL) {
                cur->left = ins;
                return;
            } else {
                cur = cur->left;
            }
        }
    }
}

Node** find(Value value) {
    Node** curRef = &root;

    while(1) {
        if (*curRef == NULL)
            return NULL;
        else if (value == *curRef->value)
            return curRef;
        else if (value > *curRef->value)
            curRef = &curRef->right;
        else /* if (value < *curRef->value) */
            curRef = &curRef->left;
    }
}

void delete(Node** nodeRef) {
    if (nodeRef == NULL)
        return;

    if (*nodeRef->left == NULL && *nodeRef->right == NULL) {
        free(*nodeRef);
        *nodeRef = NULL; // TODO introduce bug here?
    }
    else if (*nodeRef->right != NULL) {
        Node** curRef = nodeRef->right; // TODO sus
        while (1) {
            if (*curRef->left == NULL) {
                *nodeRef->value = *curRef->value;
                delete(curRef);
                return;
            }
            else {
                curRef = curRef->left;
            }
        }
    }
    else if (*nodeRef->left != NULL) {
        Node** curRef = nodeRef->left; // TODO sus
        while (1) {
            if (*curRef->right == NULL) {
                *nodeRef->value = *curRef->value;
                delete(curRef);
                return;
            }
            else {
                curRef = curRef->right;
            }
        }
    }
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

Value prompt(char* text) {
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
            delete(find(prompt("Node Value")));
        else if (opt == 3)
            view();
        else if (opt == 4)
            break;
    }
    return 0;
}