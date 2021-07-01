#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

typedef unsigned long long Value;

typedef struct Node {
    Value value;
    struct Node* left;
    struct Node* right;
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
        Node* cur = *curRef;
        if (cur == NULL)
            return NULL;
        else if (value == cur->value)
            return curRef;
        else if (value > cur->value)
            curRef = &cur->right;
        else /* if (value < cur->value) */
            curRef = &cur->left;
    }
}

void delete(Node** nodeRef) {
    if (nodeRef == NULL)
        return;

    Node* node = *nodeRef;

    if (node->left == NULL && node->right == NULL) {
        free(node);
        // *nodeRef = NULL; // TODO introduce bug here?
    }
    else if (node->right != NULL) {
        Node** curRef = &node->right;
        while (1) {
            Node* cur = *curRef;
            if (cur->left == NULL) {
                node->value = cur->value;
                delete(curRef);
                return;
            }
            else {
                curRef = &cur->left;
            }
        }
    }
    else if (node->left != NULL) {
        Node** curRef = &node->left;
        while (1) {
            Node* cur = *curRef;
            if (cur->right == NULL) {
                node->value = cur->value;
                delete(curRef);
                return;
            }
            else {
                curRef = &cur->right;
            }
        }
    }
}

void print(Node* node) {
    if (node == NULL)
        return;
    print(node->left);
    printf("%lld ", node->value);
    print(node->right);
}

void view() {
    print(root);
    puts("");
}

void menu() {
    puts("==== CS2040 Assignment 1 ====");
    puts("[1] Insert Value");
    puts("[2] Delete Value");
    puts("[3] View in-order traversal of tree");
    puts("[4] Quit, but give me 5.0 CAP and a A+ for this mod");
}

Value prompt(char* text) {
    Value opt;
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