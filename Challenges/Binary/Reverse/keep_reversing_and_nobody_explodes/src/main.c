#include <stdio.h>
#include <stdlib.h>
#include <emscripten/emscripten.h>

char wirePass = 0, seqPass = 0, condPass = 0;

int hash[30] = {121,73,138,107,184,217,242,46,93,113,90,147,248,92,60,106,123,80,11,219,134,62,60,208,21,55,232,31,21,69};
int key[30] = {30,59,239,18,208,184,134,93,38,38,50,163,167,50,15,89,63,101,84,186,217,78,8,162,65,89,173,77,104,69};

/**
 * Return value (status code):
 * 		0 => nothing
 * 		1 => cleared (module passed)
 * 		2 => failed  (explode)
 * 
 * Color references:
 * 		0 => black
 * 		1 => red
 * 		2 => yellow
 * 		3 => green
 *		4 => blue 
 */

char getWireIndex(char color[], int length) {
	int black = 0;
	for (int i = 0; i < length; i++) {
		color[i] -= '0';
		if (color[i] == 0) black++;
	}

	if (black == 1) {
		for (int i = 0; i < length; i++) {
			if (color[i] == 0) {
				return i;
			}
		}
	}
	else if (black == 0) {
		if (length == 3) return 2;
		else if (length == 4) {
			if (color[1] == 1) return 0;
			else {
				int freq[5] = {0, 0, 0, 0, 0};
				for (int i = 0; i < length; i++) {
					freq[color[i]] = 1;
				}

				int types = 0;
				for (int i = 0; i < 5; i++) {
					types += freq[i];
				}
				return types - 1;
			}
		}
		else {
			int green = 0, index;
			for (int i = 0; i < length; i++) {
				if (color[i] == 3) {
					green++;
					index = i;
				}
			}
			if (green) return (index - 1) % length;
			else return 3;
		}
	}
	else if (length == 5) {
		return 3;
	}
	else {
		int result = 0;
		for (int i = 0; i < length; i++) {
			if (color[i]) result++;
		}
		return result;
	}
	return -1;
}

EMSCRIPTEN_KEEPALIVE
void cc(char cuts[], int count, char color[], int colorLen) {
	char index = getWireIndex(color, colorLen);

	for (int i = 0; i < count; i++) {
		if (cuts[i] - '0' != index) {
			wirePass = 2;
			return;
		}
	}
	wirePass = 1;
}

char* func(int n) {
	int freq[4] = {1, 1, 1, 1};
	char* output = (char *) malloc(5);
	int k = 0;
	n %= 24;
	while (k < 4) {
		int i = 0, rank = 0;

		int fact = 1;
		for (int j = 2; j <= 3-k; j++)
			fact *= j;

		for (; i < 4; i++) {
			if (freq[i] == 0) continue;
			if (++rank * fact > n) break;
		}
		n -= --rank*fact;
		output[k++] = 'A' + i;
		freq[i] = 0;
	}
	output[k] = '\0';
	return output;
}

EMSCRIPTEN_KEEPALIVE
void ca(char sequence[], int sequenceLen, int serialNum) {
	char* target = func(serialNum);
	char ok = 1;
	for (int i = 0; i < sequenceLen && ok; i++) {
		if (sequence[i] != target[i]) ok = 0;
	}
	if (!ok) seqPass = 2;
	else if (sequenceLen == 4) seqPass = 1;
	else seqPass = 0;
}

EMSCRIPTEN_KEEPALIVE
void cb(char time[], int timeLen, char serial[]) {
	char digit = (serial[0]-'A') ^ (serial[1]-'A') ^ (serial[6]-'A') ^ (serial[7]-'A');
	for (int i = 0; i < timeLen; i++) {
		if (digit == time[i] - '0') {
			condPass = 1;
			return;
		}
	}
	condPass = 2;
}

EMSCRIPTEN_KEEPALIVE
char* check() {
	if (wirePass & 2 || seqPass & 2 || condPass & 2)
		return "Bomb exploded :( Be a little more careful next time, will ya?";
	else if (wirePass & 1 && seqPass & 1 && condPass & 1) {
		char* flag = (char *) malloc(30);
		for (int i = 0; i < 30; i++) {
			flag[i] = key[i] ^ hash[i];
		}
		puts(flag);
		;return flag;
	}
	return "";
}
