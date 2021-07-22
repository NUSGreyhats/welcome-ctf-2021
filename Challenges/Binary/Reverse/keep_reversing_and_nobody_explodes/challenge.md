# Keep Reversing and Nobody Explodes

### Challenge Details
A simplified version of the game "Keep Talking and Nobody Explodes". Player is given a bomb to defuse within an amount of time. But instead of having a manual to follow, they have to reverse engineer a wasm binary to figure out how to complete each section of the bomb (maybe 3-4 sections?).

To prevent players from brute forcing, the bomb detonates when they make a wrong decision (cutting the wrong wire etc). A new bomb with a unique serial number is generated every time, and the bomb logic will depend on its serial number.

### Setup Instructions
Run `docker build -t keep_reversing .` to build the container.
Then run, `docker container run -d -p 3000:80 keep_reversing` and navigate to `localhost:3000`.

### Possible Hints
Hint: Observe the main JS file. See what functions are responsible for which module, and start from there.

### Key Concepts
Basic wasm reversing techniques.

### Solution
The serial number is made up of 2 letters from A-F, followed by a random 4-digit number, and 2 more letters from A-F.

#### Wire Module
 - 1 black wire
	 - Cut the black wire
 - 0 black wire
	 - 3 wires
	 	 - Cut the last
	 - 4 wires
	   - If second wire is red, cut the first
		 - Else if type of color >= 3, cut the (#type - 1) indexed wire
		 - Else, cut the second
	 - 5 wires
	   - If there is at least one green wire, cut the one before the last green wire (counting from top to bottom) (with wrap around)
		 - Else, cut the fourth
 - 2 or more black wires
   - 3 or 4 wires
	   - Cut the (#non-black wires) indexed wire
	 - 5 wires
	   - Cut the fourth

#### Sequence Buttons
Let the 4-digit number in the serial be k, the correct order to press is the (k%24)-th lexicographically smallest permutation.

i.e. ABCD, ABDC, ACBD, ACDB, ..., BACD, BADC, BCAD, ...
ABCD is the 0th smallest and ABDC is the 1st smallest. (Programmers count from 0 :P)

### Big Button
Take the 4 letters in the serial number: p,q,r,s. Let A represents 0, B represents 1, ..., F represents 5, then the player should press the button when there is p^q^r^s in any position of the timer.

### Learning Objectives
Intro to wasm RE.

### Flag
greyhats{Wh0_n33D5_a_p4rTnER}
