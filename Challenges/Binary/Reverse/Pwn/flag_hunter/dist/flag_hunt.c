#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>

struct Warrior
{
	int type;
	int health;
	int mana;
};

struct Guardian
{
	int type;
	char health;
	int damage;
	int heal;
};

void practice() {
	// practice mode is to give hint about integer overflow
	printf("As the legend goes:\n");
	printf("Everything has a limit\n");
	printf("Nothing in this world is higher than 127\n");
	printf("    skill 1: Refresh Mana [cost : 0 MP]\n");
	printf("    skill 2: Defense [cost : 25 MP]\n");
	printf("    skill 3: heal 10 health [cost : 50 MP]\n");
	printf("    skill 4: quit\n");

	char health = 80;
	int mana = 50;
	while (1) {
		printf("Your health: %d mana: %d\n", health, mana);
		int choice = 0;
		while (1) {
			printf("Your choice of skill:\n");
			scanf("%d", &choice);
			if (choice >= 1 && choice <= 4) {
				break;
			}
		}
		if (choice == 1) {
			printf("Your mana refreshed to 50\n");
			mana = 50;
		} else if (choice == 2) {
			if (mana >= 25) {
				mana -= 25;
				printf("Your enter defence mode\n");
			} else {
				printf("Your mana not enough\n");
			}
		} else if (choice == 3) {
			if (mana >= 50) {
				mana -= 50;
				health += 10;
				printf("Your health + 10\n");
			} else {
				printf("Your mana not enough\n");
			}
		} else if (choice == 4) {
			return;
		}
	}
}

void hunt() {
	int a;
	struct Warrior warrior;
	while (1) {
		printf("Choose your hero 1. Mage 2. Slayer\n");
		scanf("%d", &a);
		if (a == 1) {
			warrior.type = 1;
			warrior.health = 42;
			warrior.mana = 50;
			printf("Your hero: Mage\n");
			printf("    [1] Magic Bullet: Deal 20 Damage [cost : 10 MP]\n");
			printf("    [2] Magic Book: Refresh Mana [cost : 0 MP]\n");
			printf("    [3] Mana Shield: Defense [cost : 25 MP]\n");;
			break;
		} else if (a == 2) {
			// this hero is wrong option, just to confuse player
			warrior.type = 2;
			warrior.health = 50;
			warrior.mana = 0;
			printf("Your hero: Slayer\n");
			printf("    [1] Slash: Deals 20 Damage\n");
			printf("    [2] Deadly Slash: Sacrifices 20 health and deals 40 damage\n");
			break;
		}
	}

	srand((unsigned) time(NULL));
	struct Guardian guardian;
	int random = rand() % 2;
	if (random == 0) {
		printf("Greyhats Flag Guardian has appeared.\n");
		guardian.type = 1;
		guardian.health = 80;
		guardian.damage = 10;
		guardian.heal = 4;
	} else if (random == 1) {
		printf("Grayhats Flag Guardian has appeared.\n");
		guardian.type = 2;
		guardian.health = 50;
		guardian.damage = 30;
		guardian.heal = 5;
	}

	while (1) {
		if (guardian.type == 1) {
			printf("Greyhats Flag Guardian health: %d damage: %d\n", guardian.health, guardian.damage);
		} else if (guardian.type == 2) {
			printf("Grayhats Flag Guardian health: %d damage: %d\n", guardian.health, guardian.damage);
		}
		printf("Your helath: %d mana: %d\n", warrior.health, warrior.mana);
		if (warrior.type == 1) {
			printf("    [1] Magic Bullet: Deal 20 Damage [cost : 10 MP]\n");
			printf("    [2] Magic Book: Refresh Mana [cost : 0 MP]\n");
			printf("    [3] Mana Shield: Defense [cost : 25 MP]\n");
			a = 0;
			while (1) {
				printf("Your choice of skill:\n");
				scanf("%d", &a);
				if (a == 1) {
					if (warrior.mana >= 10) {
						warrior.mana -= 10;
						guardian.health -= 20;
						printf("Magic Bullet deals 20 damage to the Flag Guardian!\n");
					} else {
						printf("Your mana not enough!\n");
					}
					warrior.health -= guardian.damage;
					printf("Guardian cause %d damage to you!\n", guardian.damage);
					guardian.health += guardian.heal;
					printf("Guardian heals %d health!\n", guardian.heal);
					break;
				} else if (a == 2) {
					warrior.mana = 50;
					printf("Your mana has been refreshed\n");
					warrior.health -= guardian.damage;
					printf("Guardian cause %d damage to you!\n", guardian.damage);
					guardian.health += guardian.heal;
					printf("Guardian heals %d health!\n", guardian.heal);
					break;
				} else if (a == 3) {
					if (warrior.mana >= 25) {
						warrior.mana -= 25;
						printf("Your enter defence mode\n");
						guardian.health += guardian.heal;
						printf("Guardian heals %d health!\n", guardian.heal);
					} else {
						printf("Your mana not enough!\n");
					}
					break;
				}
			}
		} else if (warrior.type == 2) {
			printf("    [1] Slash: Deals 20 Damage\n");
			printf("    [2] Deadly Slash: Sacrifices 20 health and deals 40 damage\n");
			a = 0;
			while (1) {
				printf("Your choice of skill:\n");
				scanf("%d", &a);
				if (a == 1) {
					guardian.health -= 20;
					warrior.health -= guardian.damage;
					printf("Slash deals 20 damage to the Flag Guardian!\n");
					printf("Guardian cause %d damage to you!\n", guardian.damage);
					guardian.health += guardian.heal;
					printf("Guardian heals %d health!\n", guardian.heal);
					break;
				} else if (a == 2) {
					if (warrior.health >= 20) {
						warrior.health -= 20;
						guardian.health -= 40;
						printf("Deadly Slash deals 40 damage to the Flag Guardian!\n");
						warrior.health -= guardian.damage;
						printf("Guardian cause %d damage to you!\n", guardian.damage);
						guardian.health += guardian.heal;
						printf("Guardian heals %d health!\n", guardian.heal);
					} else {
						printf("Your health not enough!\n");
					}
					break;
				}
			}
		}
		if (warrior.health <= 0) {
			printf("Your health: %d\n", warrior.health);
			printf("You lose\n");
			break;
		}
		if (guardian.health <= 0) {
			printf("Flag Guardian's health: %d\n", guardian.health);
			printf("You win\n");
			printf("greyhats{1nt3rger_OooOooverflow_in_3ss3nce}\n");
			exit(0);
		}
	}

}

void playgame() {
	printf("Welcome to Flag Hunter. The world relies on you to defeat the Flag Guardian.\n");
	int a;
	while (1) {
		printf("Choose Your play mode: 1. practice 2. hunt\n");
		scanf("%d", &a);
		if (a == 1) {
			practice();
		}
		else if (a == 2) {
			hunt();
		}
	}
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
    alarm(180);
}

int main() {
	setup();
	playgame();
	return 0;
}
