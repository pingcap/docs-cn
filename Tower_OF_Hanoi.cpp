// C++ program for the above approach

#include <bits/stdc++.h>
using namespace std;

// Function to increment binary counter
int increment(int* counter, int n)
{
	int i = 0;

	while (true) {

		// Stores the Bitwise XOR of
		// the i-th bit of N and 1
		int a = counter[i] ^ 1;

		// Stores the Bitwise AND of
		// the i-th bit of N and 1
		int b = counter[i] & 1;

		// Swaps the i-th bit of N
		counter[i] = a;

		// If b is equal to zero
		if (b == 0)
			break;

		// Increment i by 1
		i = i + 1;
	}

	// Return i
	return i;
}

// Function to print order of movement
// of disks across three rods to place
// all disks on the third rod from the
// first rod
void TowerOfHanoi(int N)
{
	// Stores the binary representation
	// of a state
	int counter[N] = { 0 };

	// Traverse the range [0, 2^N - 1]
	for (int step = 1;
		step <= pow(2, N) - 1; step++) {

		// Stores the position of the
		// rightmost unset bit
		int x = increment(counter, N) + 1;

		// Print the Xth bit
		cout << "Move disk " << x
			<< " to next circular"
			<< " right rod \n";
	}
}

// Driver Code
int main()
{
	int N = 3;
	TowerOfHanoi(N);

	return 0;
}
