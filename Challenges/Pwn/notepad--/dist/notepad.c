#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define NAME_SZ 0x10
#define CONTENT_SZ 0x20
#define NOTES_SZ 10

typedef struct Note {
    char name[NAME_SZ];
    char content[CONTENT_SZ];
} Note;

Note notes[NOTES_SZ];

Note* get_note() {
    int idx = 0;
    printf("Index: ");
    scanf("%d", &idx);

    if (idx >= NOTES_SZ) {
        printf("Index out of range!");
        exit(-1);
    }

    return &notes[idx];
}

void create_note() {
    Note* note = get_note();
    printf("Name: ");
    read(0, note->name, NAME_SZ);
    printf("Content: ");
    read(0, note->content, CONTENT_SZ);
}

void view_note() {
    Note* note = get_note();
    printf("Name: ");
    puts(note->name);
    printf("Content: ");
    puts(note->content);
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
    printf("========== Notepad-- Professional Edition ==========\n");
    printf("[1] Create Note\n");
    printf("[2] View Note\n");

    while (1)
    {
        int opt = 0;
        printf("> ");
        scanf("%d", &opt);

        if (opt == 1) {
            create_note();
        } else if (opt == 2) {
            view_note();
        } else if (opt == 3) {
            break;
        }
    }
    
    return 0;
}
