# Hashbrown

You have a flag broken up into 10 32-bit integers v_1, v_2, ..., v_10.
You are given ten constants C_1, C_2, ..., C_10, and H, such that

> `C_1 * v_1 + C_2 * v_2 + ... + C_10 * v_10 = H (mod 2^512)`

From this, we need to extract the flag.

If v_i could be anything, then you can probably generate v_1 to v_9 randomly, find v_10 using modular inverses, and win. But each value is bounded from 0 to 2^32 - 1, so we need to guarantee our solution is within that range.

## Where do you start???

Personally, I started by having hazy memories of this LLL 
something, but when I looked it up online, I had no idea why it worked, or how to make it work.

Then I remember where I first heard of its existence: from [this blog post](https://codeforces.com/blog/entry/60442)
about ways to counter string hashing algorithms. I read the 
linked posts, and had a vague idea of what was going on. Then
I stumbled on [this](https://www.readcube.com/articles/10.1007%2Fs001459900042), and how I maybe had a workable idea of what was going on. I will try to explain:

## Lattice reduction to win

A _lattice_ is somewhat like a vector space, except you can
only multiply things by discrete values. In our case, the
lattice we want is _sort of like_ the vector space R^n. This is why: if I had vectors
```text
  [=========] this range has 10 values
[ 1 0 0 ... 0 C_1 ]
[ 0 1 0 ... 0 C_2 ]
...
[ 0 0 0 ... 1 C_10]
```

letting them be R_1 to R_10, then 
```
C_1 * v_1 + ... + C_10 * v_10 = H
```
directly corresponds to
```
R_1 * v_1 + ... + R_10 * v_10 =
    [ v_1 v_2 ... v_10 H ]
```

Representing the equation in a way that maintains access to the v_i values, even in the end result, will be important later on. You can see that the lattice spanned by the 10 vectors above correspond precisely to valid values of (v_1, ..., v_10, H). (In fact, they are a basis.)

Now, there are magic algorithms called _lattice reduction_ algorithms that take a such a basis, and return an almost orthogonal (tbh I haven't gone through the precise definition of 'almost' for that) basis that generates the same space, except with 'short' basis vectors. By 'short', this means vectors with small magnitude. (Fun bonus fact: apparently, finding the shortest basis is NP-complete!)

That gives us a plan of attack:

- Somehow, encode the modulo and the = H condition into a set of basis vectors
- Feed our basis vectors into a lattice reduction algorithm (here, LLL will do)
- Hope that the values that emerge from the basis fit in our bound
- Win

## Refining the approach

Firstly, we're not taking values mod 2^512. We can address this by adding `[ 0 0 ... 0 2^512]` to our matrix, after thinking
about it for a while, you can observe that this lets the resulting value of `H` always be reduced by this modulo.

Now, we want to force `H` to be the value assigned to us. First, I cover the case where we want to force it to be zero.
In this case, we can simply multiply all the C_i values by a constant that is much larger than we expect any of the v_i values to be. That way, either the basis's value at that column
is zero, or it is a really big value; such that making the other values small cannot compensate. So that forces a zero sum.

Now, how do we force the sum of `H` to come out? A quick way is to simply include `H` in your list of values, apply
the algorithm to force a zero sum, and hope that
the coefficient that comes out for this is either 1 or -1.
(For completeness, the author's solution adds a column where `H`'s row has a 2^32 term, and all the other terms are zero. Once you've limited yourself to zero-sum solutions, that should force solutions where `H`'s coefficient is as small as possible; which forces a solution where that is one. But I did not need that yay)  

To sum up, we now have this lattice basis:

```
[1 0 ... 0 (K * C_1) ]
[0 1 ... 0 (K * C_2) ]
...
[0 0 ... 1 (K * C_10)]
[0 0 ... 0   2^512   ]
```
After applying LLL, we hope that one of our basis elements
will be precisely `[v_1 v_2 ... v_10 H]`, and that will be our flag.

And in our case, it is! Here is code:

```python
# Sage code, for getting the values
MOD = 1 <<  512
orig_num = [ 
    # the given values
]
nums = [v for v in orig_nums]
nrmax = 2 ** 32
rangeShift = -2**31
target = # ... the given value
for v in nums:
    target += v * rangeShift
    target %= MOD


nums.append(target)
n = len(nums)
K = 2**50

# build the LL matrix
M = []
for i, v in enumerate(nums):
    curRow = [0] * (n + 1)
    curRow[i] = 1
    curRow[n] = K * v
    M.append(curRow)
    
mod_row = [0] * (n + 1)
mod_row[n] = K * MOD
M.append(mod_row)

# Actually reduce
yeet = Matrix(M)
yeet_red = yeet.LLL()
print("LLL matrix:")
print(yeet_red)

possible_ans = yeet_red[0][:n]
print("original number list")
print(orig_nums)
print("sum check:")
print(sum(a * -(b + rangeShift) for a, b in zip(orig_nums, possible_ans)) % MOD) # if this is target, we're on the right track!

print("generating values (for the original problem):")
numbers = [-(b + rangeShift) % MOD for a, b in zip(orig_nums, possible_ans)]
print(numbers)
```

I slightly overcomplicated my solution, by first turning the [0, 2^32 - 1] range to [-2^31, 2^31], when simply extending it to [-2^32, 2^32] should be okay, I guess? But the same techniques will apply.

We get that the C values are 
```python
[1735550329, 1751217267, 2068594804, 929653555, 1600287283, 1634415967, 2033218930, 1600676149, 1751084344, 555819389]
```

which gives a flag of `greyhats{L@t7ic3_br3ak5_y0ur_ha5h_m8!!!}`. 
