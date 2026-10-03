@@@ part
id: 10
title: Bits, Maths and Interview Practice
level: Advanced
blurb: The finishing tools: bit manipulation, the number theory that keeps coming up (primes, gcd, modular arithmetic, counting, randomness), a guide to recognising which pattern a problem needs, and full mock-interview problems worked from question to code.

@@@ lesson
id: bit-manipulation
title: Bit manipulation
minutes: 26
summary: Binary numbers in Python, the six bitwise operators, how Python handles negative numbers, the essential bit tricks, XOR puzzles, sets as bitmasks and enumerating subsets and submasks, and the maximum XOR of two numbers.
---
Every integer is stored in **binary**: 13 is `1101`, meaning 8 + 4 + 0 + 1. Working on the bits directly gives tiny, very fast solutions to some problems, packs a whole set of small numbers into one integer (the bitmask DP of Lesson 44), and appears all over systems code: permissions, flags, network masks, hashing, compression.

### Binary in Python

```python
print(bin(13), f"{13:b}", f"{13:08b}")      # '0b1101', '1101', zero-padded to 8 digits
print(int("1101", 2), 0b1101, 0xFF)         # reading binary, a binary literal, a hex literal
print((13).bit_length(), (13).bit_count())  # 4 bits needed, 3 of them are 1 (bit_count: Python 3.10+)
```

### The operators

| Operator | Name | Bit rule | Example (12 = 1100, 10 = 1010) |
|---|---|---|---|
| `a & b` | AND | 1 if both are 1 | `1000` = 8 |
| `a \| b` | OR | 1 if either is 1 | `1110` = 14 |
| `a ^ b` | XOR | 1 if they differ | `0110` = 6 |
| `~a` | NOT | flips every bit | `-13` (see below) |
| `a << k` | left shift | moves bits left: × 2ᵏ | `12 << 2` = 48 |
| `a >> k` | right shift | moves bits right: // 2ᵏ | `12 >> 2` = 3 |

![12 and 10 written as 4-bit rows 1100 and 1010, with the results of AND (1000), OR (1110) and XOR (0110) underneath, each bit lined up in its column](figures/bit-ops.svg)

```python
a, b = 12, 10
print(a & b, a | b, a ^ b, a << 2, a >> 2)
print(f"{a:04b} & {b:04b} = {a & b:04b}")
```

### Negative numbers and ~

Most languages store integers in a fixed number of bits using **two's complement**, where −x is `~x + 1`. Python's integers have **unlimited** size, but they behave as if negative numbers had infinitely many 1 bits on the left. So `~x == -x - 1`, and `x & -x` still isolates the lowest set bit. When you need a fixed width (to mimic a 32-bit C integer), mask with `& 0xFFFFFFFF`.

```python
print(~5, -5 & 0xFF, f"{-5 & 0xFF:08b}")     # -6, and -5 as an 8-bit pattern: 11111011
print(12 & -12)                              # 4: the lowest set bit of 1100
```

### The essential tricks

| Goal | Expression | Why |
|---|---|---|
| Is bit i set? | `x >> i & 1` (or `x & (1 << i)`) | moves bit i to the end |
| Set bit i | `x \| (1 << i)` | OR with a single 1 |
| Clear bit i | `x & ~(1 << i)` | AND with all 1s except bit i |
| Toggle bit i | `x ^ (1 << i)` | XOR flips |
| Lowest set bit | `x & -x` | Fenwick trees use this (Lesson 34) |
| Clear the lowest set bit | `x & (x - 1)` | subtracting 1 flips the lowest 1 and the 0s after it |
| Is x a power of two? | `x > 0 and x & (x - 1) == 0` | a power of two has exactly one 1 |
| Count the 1 bits | `x.bit_count()` | or loop `x &= x - 1` until 0 |
| Even or odd? | `x & 1` | the last bit |

```python
x = 0b10110
print(x >> 1 & 1, bin(x | 1), bin(x & ~(1 << 2)), bin(x ^ 0b11))
print([n for n in range(1, 70) if n & (n - 1) == 0])           # powers of two

def count_ones(x):                  # Brian Kernighan's method: one loop per 1 bit
    count = 0
    while x:
        x &= x - 1
        count += 1
    return count

print(count_ones(0b1011_0110), (0b1011_0110).bit_count())
```

### XOR puzzles

XOR has three properties that solve a whole family of puzzles: `x ^ x == 0`, `x ^ 0 == x`, and the order of XORs doesn't matter. So XOR-ing a list cancels out every value that appears an even number of times.

```python
from functools import reduce
from operator import xor

print(reduce(xor, [4, 1, 2, 1, 2]))          # the number that appears once: 4

def missing_number(nums):                    # 0..n with one number missing
    result = len(nums)
    for i, x in enumerate(nums):
        result ^= i ^ x                      # every present number cancels with its index
    return result

print(missing_number([3, 0, 1]), missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]))

a, b = 5, 9
a ^= b; b ^= a; a ^= b                       # swap without a temporary (just a curiosity in Python)
print(a, b)
```

### Sets as bitmasks

A set of items numbered 0 to n − 1 fits in one integer: bit i is 1 when item i is in the set. Union, intersection and difference become `|`, `&` and `& ~`, each a single machine-word operation for small n. Looping `mask` from 0 to 2ⁿ − 1 visits **every subset**, which is how bitmask DP enumerates its states.

```python
items = ["a", "b", "c"]
for mask in range(1 << len(items)):          # 0 .. 7: every subset
    subset = [items[i] for i in range(len(items)) if mask >> i & 1]
    print(f"{mask:03b}", subset)

A, B = 0b1011, 0b0110                        # {0, 1, 3} and {1, 2}
print(bin(A | B), bin(A & B), bin(A & ~B))   # union, intersection, difference
```

To visit every **submask** of a mask (every subset of a given set), use `sub = (sub - 1) & mask` until it reaches 0. Across all masks this totals O(3ⁿ), the standard trick for DP over subsets of subsets.

```python
mask = 0b1011
sub = mask
while sub:
    print(f"{sub:04b}", end=" ")
    sub = (sub - 1) & mask                   # the next smaller submask
print("0000")
```

### Maximum XOR of two numbers

Which pair of numbers has the largest XOR? Comparing all pairs is O(n²). Instead, decide the answer **one bit at a time from the top**: for each bit, ask "can the answer have a 1 here, given the bits already chosen?" Two numbers produce that answer prefix exactly when the XOR of their prefixes equals it, which is a set lookup. A **binary trie** over the bits (Lesson 33) is the other classic solution. That's the second exercise.

### Bit manipulation at a glance

| Problem | Trick | Time |
|---|---|---|
| The single number among pairs | XOR everything | O(n) |
| Missing number in 0..n | XOR with the indexes (or a sum formula) | O(n) |
| Power of two | `x & (x − 1) == 0` | O(1) |
| Count set bits | `bit_count()` or Kernighan's loop | O(1) / O(set bits) |
| Bits of every number 0..n | `bits[i] = bits[i >> 1] + (i & 1)` | O(n) |
| Every subset of n items | loop masks 0..2ⁿ − 1 | O(2ⁿ · n) |
| Maximum XOR pair | greedy bit by bit with a set (or a binary trie) | O(n · bits) |

:::exercise The single number
Every number in `nums` appears exactly **twice**, except one that appears once. Write `single_number(nums)` returning that number, in one pass with O(1) extra memory (no set, dict or sorting).
```python starter
def single_number(nums):
    pass

print(single_number([4, 1, 2, 1, 2]))   # 4
```
```python check
fn = need("single_number")
src = __source__
import re as _re
_code = "\n".join(line.split("#")[0] for line in src.splitlines())
if _re.search(r"\b(set|dict|Counter|sorted)\s*\(|\.sort\s*\(|\{\s*\}", _code):
    raise AssertionError("Solve it without a set, dict, Counter or sorting: O(1) extra memory. XOR has a property that makes pairs cancel out.")
test(fn, cases=[
    (([4, 1, 2, 1, 2],), 4, "the example"),
    (([2, 2, 1],), 1, "three numbers"),
    (([7],), 7, "a single number"),
    (([0, 5, 5],), 0, "the single number is zero"),
    (([-3, 8, 8, -1, -1],), -3, "negative numbers"),
    (([10**9, 3, 3],), 10**9, "a large number"),
])
```
```python solution
def single_number(nums):
    result = 0
    for x in nums:
        result ^= x          # pairs cancel (x ^ x == 0); the lone number survives (x ^ 0 == x)
    return result

print(single_number([4, 1, 2, 1, 2]))
```
hint: Which bitwise operator turns two copies of the same number into 0?
hint: XOR: `x ^ x == 0` and `x ^ 0 == x`, and the order of the XORs doesn't matter.
hint: Start with `result = 0` and XOR in every number; every pair cancels, leaving the single number.
approach:
1. **Understand:** exactly one number appears once, all others exactly twice; O(1) memory.
2. **Examples:** [4, 1, 2, 1, 2] → 4.
3. **Brute force:** count with a dict (O(n) memory) or sort and scan pairs (O(n log n)).
4. **Pattern:** **XOR cancellation**.
5. **Plan:** fold the list with `^`.
6. **Code and test:** one element, zero as the answer, negative numbers.
walkthrough:
**Line by line**

- `result` starts at 0, the identity for XOR.
- XOR is commutative and associative, so the order is irrelevant: mentally group each pair together; each pair gives 0.
- What's left is 0 ^ single = single.

**Trace** on [4, 1, 2, 1, 2] (in binary):

| x | result after |
|---|---|
| 4 (100) | 100 |
| 1 (001) | 101 |
| 2 (010) | 111 |
| 1 (001) | 110 |
| 2 (010) | **100** = 4 |

**Complexity:** O(n) time, O(1) space.

**Common wrong approach:** `sum(set(nums)) * 2 - sum(nums)`. It works, but uses O(n) extra memory, which the problem rules out.
:::

:::exercise Maximum XOR of two numbers
Write `max_xor(nums)` returning the largest value of `a ^ b` over all pairs of numbers in `nums` (non-negative integers below 2²⁰; a list of one number gives 0). It must handle 50,000 numbers in about a second, so don't compare every pair.
```python starter
def max_xor(nums):
    pass

print(max_xor([3, 10, 5, 25, 2, 8]))   # 28: 5 ^ 25
```
```python check
fn = need("max_xor")
test(fn, cases=[
    (([3, 10, 5, 25, 2, 8],), 28, "the example"),
    (([0],), 0, "one number"),
    (([2, 4],), 6, "two numbers"),
    (([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70],), 127, "a longer list"),
    (([7, 7, 7],), 0, "all equal"),
    (([0, (1 << 20) - 1],), (1 << 20) - 1, "every bit different"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    return ([rng.randrange(1 << 20) for _ in range(n)],)
def _ref(nums):
    best = 0
    for bit in range(19, -1, -1):
        best <<= 1
        prefixes = {x >> bit for x in nums}
        if any((best | 1) ^ p in prefixes for p in prefixes): best |= 1
    return best
speed(fn, _make, _ref, sizes=(1_000, 6_000, 50_000), what="numbers",
      tip="Comparing every pair is O(n^2). Build the answer bit by bit from the top: for each bit, check (with a set of prefixes, or a binary trie) whether two numbers can make that bit 1.")
```
```python solution
def max_xor(nums):
    best = 0
    for bit in range(19, -1, -1):                 # from the highest bit down
        best <<= 1                                # make room for this bit
        prefixes = {x >> bit for x in nums}       # every number's top bits so far
        candidate = best | 1                      # try to make this bit 1
        # two prefixes p and q give `candidate` exactly when p ^ q == candidate, i.e. q == candidate ^ p
        if any(candidate ^ p in prefixes for p in prefixes):
            best = candidate
    return best

print(max_xor([3, 10, 5, 25, 2, 8]))
```
```python slow
def max_xor(nums):
    best = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            best = max(best, nums[i] ^ nums[j])
    return best
```
hint: A 1 in a high bit beats any combination of lower bits. So decide the answer's bits from the top, greedily: can this bit be 1?
hint: After choosing the top bits of the answer, look only at each number's top bits (its **prefix**, `x >> bit`). The answer prefix is possible if some two prefixes XOR to it. Since `p ^ q == c` means `q == c ^ p`, a set lookup checks it.
hint: For bit from 19 down to 0: `best <<= 1`; `prefixes = {x >> bit for x in nums}`; if any `(best | 1) ^ p` is in `prefixes`, set `best |= 1`. Return `best`.
approach:
1. **Understand:** the maximum over pairs; numbers below 2²⁰; one number → 0 (it can only pair with itself).
2. **Examples:** [3, 10, 5, 25, 2, 8] → 5 ^ 25 = 00101 ^ 11001 = 11100 = 28.
3. **Brute force:** every pair: O(n²).
4. **Pattern:** **greedy bit by bit** with prefix sets (or a **binary trie**: for each number, walk the trie choosing the opposite bit whenever possible).
5. **Plan:** 20 rounds; each round a set of prefixes and one membership test per prefix.
6. **Code and test:** one number, equal numbers, numbers differing in every bit.
walkthrough:
**Line by line**

- Bits are decided from 19 down to 0 because a higher bit is worth more than all lower bits together.
- `best <<= 1` shifts the bits decided so far up, leaving a 0 in the new position; `candidate` tries a 1 there.
- `prefixes` holds the numbers' top bits at this length. If p and q are both prefixes and `p ^ q == candidate`, then two numbers start with bits that XOR to the candidate, so the answer can keep that 1.
- Because `x ^ y == c` is the same as `y == c ^ x`, each prefix needs just one set lookup.

**Trace** on [3, 10, 5, 25, 2, 8] for the top 5 bits (bits 4 to 0 of 25 = 11001):

| bit | candidate | possible? | best |
|---|---|---|---|
| 4 | 1 | yes (25 starts with 1, others with 0) | 1 |
| 3 | 11 | yes (25 → 11, 5 → 00) | 11 |
| 2 | 111 | yes (110 ^ 001) | 111 |
| 1 | 1111 | no | 1110 |
| 0 | 11101 | no | **11100** = 28 |

(Bits 19 to 5 are 0 for every number, so they stay 0.)

**Complexity:** O(n × B) for B = 20 bits, O(n) space.

**Common wrong approach:** XOR-ing only the largest number with every other number. The best pair needn't include it: in [9, 8, 1], the largest number gives at most 9 ^ 1 = 8, but 8 ^ 1 = 9.
:::

:::quiz
? What is 12 ^ 10 (XOR of 1100 and 1010)?
+ 6 (0110)
- 8 (1000)
- 14 (1110)
= XOR keeps the bits where the two numbers differ.
? Which expression is true exactly when a positive x is a power of two?
+ x & (x − 1) == 0
- x & 1 == 0
- x ^ x == 0
= A power of two has a single 1 bit, and x − 1 turns it off.
? In Python, what does ~x equal?
+ −x − 1
- −x
- x with its last bit flipped
= Python behaves as if negative numbers had infinitely many leading 1 bits.
? How do you visit every subset of n items with bitmasks?
+ Loop mask from 0 to 2ⁿ − 1; item i is in the subset when bit i of mask is 1
- Loop from 0 to n
- Sort the items first
= Each integer below 2ⁿ is one subset.
:::

@@@ lesson
id: number-theory
title: Maths for coding problems
minutes: 28
summary: The number theory and counting that keep appearing: gcd and lcm with Euclid's algorithm, primes by trial division and the sieve of Eratosthenes, modular arithmetic and inverses, combinations modulo a prime, exact integers versus floating point, and randomness: shuffling and reservoir sampling.
---
A handful of mathematical tools come up again and again in coding problems: when answers are huge ("give the answer modulo 10⁹ + 7"), when a problem is secretly about divisibility or primes, or when you need to pick random items fairly. Python makes several of them one-liners, but you should know what's underneath.

### Greatest common divisor and least common multiple

**Euclid's algorithm:** gcd(a, b) = gcd(b, a mod b), stopping when b is 0. Each step at least halves the numbers every two rounds, so it's O(log min(a, b)). The **lcm** follows from it: lcm(a, b) = a × b / gcd(a, b).

```python
import math

def gcd(a, b):
    while b:
        a, b = b, a % b              # gcd(48, 18) -> gcd(18, 12) -> gcd(12, 6) -> gcd(6, 0) = 6
    return a

print(gcd(48, 18), math.gcd(48, 18), math.gcd(12, 18, 30))    # math.gcd accepts many numbers (3.9+)
print(48 * 18 // gcd(48, 18), math.lcm(4, 6, 10))
```

Uses: simplifying fractions, checking whether two numbers share a factor, repeating patterns (two cycles of lengths a and b line up every lcm(a, b) steps).

### Primes

To test one number, try divisors up to **√n**: if n = a × b, one of them is at most √n. O(√n). To find **all** primes below n, the **sieve of Eratosthenes** crosses out the multiples of each prime, starting at p² (smaller multiples were already crossed out by smaller primes). O(n log log n), practically linear.

![The numbers 2 to 30 in a grid. Multiples of 2 are crossed out in one colour, then multiples of 3 from 9, then multiples of 5 from 25. The numbers left, 2, 3, 5, 7, 11, 13, 17, 19, 23 and 29, are the primes](figures/sieve.svg)

```python
import math

def is_prime(n):
    if n < 2:
        return False
    for d in range(2, math.isqrt(n) + 1):     # isqrt: exact integer square root
        if n % d == 0:
            return False
    return True

def primes_below(n):
    is_p = [True] * n
    is_p[0:2] = [False, False]
    for p in range(2, math.isqrt(n - 1) + 1):
        if is_p[p]:
            for multiple in range(p * p, n, p):
                is_p[multiple] = False
    return [i for i, flag in enumerate(is_p) if flag]

def factorise(n):                              # prime factors by trial division: O(√n)
    factors, d = [], 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)                      # whatever is left is a prime
    return factors

print(is_prime(97), is_prime(91), primes_below(30))
print(factorise(360), factorise(2 ** 31 - 1))
```

### Modular arithmetic

When answers would have thousands of digits, problems ask for them **modulo** a prime, usually 10⁹ + 7 (a prime that fits comfortably in 32 bits, so products fit in 64 bits in other languages). You can take the remainder after **every** addition, subtraction and multiplication, so numbers stay small:

- (a + b) mod m = ((a mod m) + (b mod m)) mod m, and the same for − and ×.
- **Division doesn't work that way.** Dividing by b means multiplying by b's **modular inverse**: the number b⁻¹ with b × b⁻¹ ≡ 1 (mod m). It exists when gcd(b, m) = 1. For a prime m, **Fermat's little theorem** gives b⁻¹ = b^(m−2) mod m.

```python
MOD = 10**9 + 7

print(pow(3, 200, MOD))                  # fast modular power, built in (Lesson 22 wrote it by hand)
inv3 = pow(3, -1, MOD)                   # modular inverse (Python 3.8+)
print(inv3, 3 * inv3 % MOD, pow(3, MOD - 2, MOD) == inv3)
print(10 * inv3 % MOD == 10 * pow(3, MOD - 2, MOD) % MOD)    # "10 / 3" in modular arithmetic
print(-7 % 3, (-7) // 3)                 # Python's % is never negative for a positive modulus (C and Java give -1)
```

### Counting: permutations and combinations

- Orderings of n items: n!. Ordered choices of k from n: P(n, k) = n! / (n − k)!.
- Unordered choices of k from n: C(n, k) = n! / (k! (n − k)!), "n choose k". `math.comb` and `math.perm` compute them exactly.
- **Pascal's rule** C(n, k) = C(n − 1, k − 1) + C(n − 1, k) builds a table by DP, handy for small n or when you need many values.
- For many C(n, k) **modulo a prime**, precompute factorials and **inverse factorials** once (O(n)), then each query is O(1): C(n, k) = n! × (k!)⁻¹ × ((n − k)!)⁻¹ mod p. That's the second exercise.

```python
import math

print(math.factorial(5), math.perm(5, 2), math.comb(5, 2))

pascal = [[1]]
for n in range(1, 6):                       # Pascal's triangle: each entry is the sum of the two above
    prev = pascal[-1]
    pascal.append([1] + [prev[k - 1] + prev[k] for k in range(1, n)] + [1])
for row in pascal:
    print(row)

catalan = [math.comb(2 * n, n) // (n + 1) for n in range(8)]
print("Catalan numbers:", catalan)          # balanced bracket strings, binary tree shapes, ...
```

Counting problems in interviews are often a C(n, k) in disguise: paths in a grid (C(m + n − 2, m − 1), Lesson 43), ways to choose a team, the number of binary strings with k ones. The **Catalan numbers** count balanced bracket sequences of n pairs and binary trees with n nodes.

### Exact integers, inexact floats

Python's `int` never overflows, so you'll never see the wrap-around bugs of C or Java. **Floats** are the danger: they're binary fractions with about 15–16 significant digits, so many decimals can't be stored exactly.

```python
import math
from fractions import Fraction
from decimal import Decimal

print(0.1 + 0.2, 0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3))
print(Fraction(1, 10) + Fraction(2, 10), Decimal("0.1") + Decimal("0.2"))
print(int(math.sqrt(10**30 - 1)), math.isqrt(10**30 - 1))   # float sqrt is off by one for big integers
print(2**64, 7 // 2, -7 // 2, round(2.5), round(3.5))       # floor division rounds down; round() rounds half to even
```

Rules of thumb: compare floats with `math.isclose`, keep money in integer cents (or `Decimal`), use `math.isqrt` for integer square roots, and use `//` for integer division. Note that `round(2.5)` is 2: Python rounds halves to the nearest **even** number.

### Randomness: shuffling and sampling

**Fisher-Yates shuffle:** walk from the end, swapping each position with a random position at or before it. Every permutation is equally likely, in O(n). (Swapping each item with a random position anywhere looks similar but is biased.) `random.shuffle` does this.

**Reservoir sampling:** pick k items uniformly at random from a **stream** too long to store, in one pass: keep the first k, then replace a random kept item with item i (counting from 0) with probability k / (i + 1).

```python
import random

def fisher_yates(items, rng):
    items = items[:]
    for i in range(len(items) - 1, 0, -1):
        j = rng.randint(0, i)                  # a position at or before i
        items[i], items[j] = items[j], items[i]
    return items

def reservoir(stream, k, rng):
    sample = []
    for i, item in enumerate(stream):
        if i < k:
            sample.append(item)
        else:
            j = rng.randint(0, i)              # keep item i with probability k / (i + 1)
            if j < k:
                sample[j] = item
    return sample

rng = random.Random(42)                         # seeded, so the run is reproducible
print(fisher_yates(list(range(10)), rng))
print(reservoir(range(1_000_000), 5, rng))

counts = [0] * 10                               # each of 10 items should be picked about 3 / 10 of the time
for _ in range(20_000):
    for x in reservoir(range(10), 3, rng):
        counts[x] += 1
print([round(c / 20_000, 2) for c in counts])
```

Randomness also protects algorithms from worst-case inputs: random pivots in quicksort and quickselect (Lesson 27), random hash seeds, and treaps and skip lists (Lesson 31).

### Maths at a glance

| Task | Method | Time |
|---|---|---|
| gcd / lcm | Euclid; lcm = a·b / gcd | O(log min(a, b)) |
| Is n prime? | trial division to √n | O(√n) |
| All primes below n | sieve of Eratosthenes | O(n log log n) |
| Prime factors of n | trial division | O(√n) |
| aᵇ mod m | `pow(a, b, m)` (fast exponentiation) | O(log b) |
| Modular inverse | `pow(a, -1, m)`, or a^(m−2) for prime m | O(log m) |
| Many C(n, k) mod p | factorial and inverse-factorial tables | O(n) once, O(1) per query |
| Integer square root | `math.isqrt` | O(log n) |
| Shuffle | Fisher-Yates (`random.shuffle`) | O(n) |
| k random items from a stream | reservoir sampling | O(n) time, O(k) memory |

:::exercise Count the primes
Write `count_primes(n)` returning how many prime numbers are **less than** `n`. It must handle n = 2,000,000 in well under a second.
```python starter
def count_primes(n):
    pass

print(count_primes(10))   # 4: 2, 3, 5, 7
```
```python check
fn = need("count_primes")
test(fn, cases=[
    ((10,), 4, "the example"),
    ((0,), 0, "zero"),
    ((1,), 0, "one"),
    ((2,), 0, "2 itself isn't counted (strictly less than n)"),
    ((3,), 1, "just 2"),
    ((100,), 25, "below 100"),
    ((1000,), 168, "below 1,000"),
])
def _ref(n):
    if n < 3: return 0
    s = [True] * n; s[0] = s[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, n, i): s[j] = False
    return sum(s)
speed(fn, lambda n: (n,), _ref, sizes=(10_000, 400_000, 2_000_000), what="as n", factor=10,
      tip="Testing every number by trial division is O(n √n). Use the sieve of Eratosthenes: one list of flags, crossing out the multiples of each prime p from p * p.")
```
```python solution
def count_primes(n):
    if n < 3:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p < n:
        if is_prime[p]:
            for multiple in range(p * p, n, p):    # smaller multiples were crossed out by smaller primes
                is_prime[multiple] = False
        p += 1
    return sum(is_prime)                           # True counts as 1

print(count_primes(10))
```
```python slow
def count_primes(n):
    count = 0
    for x in range(2, n):
        if all(x % d for d in range(2, int(x ** 0.5) + 1)):
            count += 1
    return count
```
hint: Testing each number separately repeats a lot of work. Instead of asking "is x prime?", cross out the numbers that **can't** be prime.
hint: Sieve of Eratosthenes: start with every number marked prime; for each p still marked, cross out p², p² + p, p² + 2p, … (any smaller multiple has a smaller factor and is already crossed out).
hint: `is_prime = [True] * n`, mark 0 and 1 False; for p while `p * p < n`: if `is_prime[p]`, set every `is_prime[m]` for m in `range(p * p, n, p)` to False. Return `sum(is_prime)`.
approach:
1. **Understand:** strictly less than n; 0, 1 and 2 give 0.
2. **Examples:** n = 10 → 2, 3, 5, 7 → 4.
3. **Brute force:** trial division for each number: O(n √n).
4. **Pattern:** **sieve of Eratosthenes**.
5. **Plan:** a flag list; cross out multiples starting at p²; only p up to √n needed; count the remaining flags.
6. **Code and test:** n ≤ 2, n = 3, known counts (25 below 100, 168 below 1,000).
walkthrough:
**Line by line**

- `is_prime` has one flag per number from 0 to n − 1; 0 and 1 are not prime.
- The loop only needs p with p² < n: a composite number below n has a factor at most √n, so it's crossed out by then.
- Crossing out starts at p × p because p × 2, p × 3, … were already crossed out as multiples of 2, 3, ….
- `sum(is_prime)` counts the True values.

**Trace** for n = 30: p = 2 crosses out 4, 6, …, 28; p = 3 crosses out 9, 15, 21, 27 (and others already gone); p = 5 crosses out 25. p = 6 has 36 > 30, so stop: 10 primes remain.

**Complexity:** O(n log log n) time, O(n) space.

**Common wrong approach:** starting the inner loop at 2p and running p all the way to n: still correct, but much slower; or forgetting that n itself isn't counted.
:::

:::exercise Combinations modulo a prime
`queries` is a list of pairs `(n, k)` with 0 ≤ n ≤ 100,000. Write `comb_mod(queries)` returning a list with C(n, k) mod 1,000,000,007 for each pair (0 when k < 0 or k > n). It must answer 20,000 queries quickly: `math.comb` builds huge exact numbers and is far too slow for that many.
```python starter
MOD = 10**9 + 7

def comb_mod(queries):
    pass

print(comb_mod([(5, 2), (10, 0), (10, 10), (3, 5)]))   # [10, 1, 1, 0]
```
```python check
import math as _math
fn = need("comb_mod")
_M = 10**9 + 7
test(fn, cases=[
    (([(5, 2), (10, 0), (10, 10), (3, 5)],), [10, 1, 1, 0], "the example"),
    (([(0, 0)],), [1], "C(0, 0)"),
    (([(52, 5)],), [2598960], "poker hands"),
    (([(100, 50)],), [_math.comb(100, 50) % _M], "a number bigger than the modulus"),
    (([(100000, 50000)],), [_math.comb(100000, 50000) % _M], "the largest n"),
    (([(7, -1), (7, 8)],), [0, 0], "k outside 0..n"),
])
import random as _random
def _make(m):
    rng = _random.Random(m)
    out = []
    for _ in range(m):
        n = rng.randint(50_000, 100_000)
        out.append((n, rng.randint(0, n)))
    return (out,)
def _ref(queries):
    N = max(n for n, k in queries) + 1
    f = [1] * N
    for i in range(1, N): f[i] = f[i - 1] * i % _M
    inv = [1] * N; inv[N - 1] = pow(f[N - 1], _M - 2, _M)
    for i in range(N - 1, 0, -1): inv[i - 1] = inv[i] * i % _M
    return [f[n] * inv[k] % _M * inv[n - k] % _M if 0 <= k <= n else 0 for n, k in queries]
speed(fn, _make, _ref, sizes=(5, 30, 20_000), what="queries (n up to 100,000)", factor=5,
      tip="math.comb computes the exact (enormous) number every time. Precompute factorials mod p and their inverses once; then each answer is fact[n] * inv_fact[k] * inv_fact[n - k] % p.")
```
```python solution
MOD = 10**9 + 7

def comb_mod(queries):
    N = max((n for n, k in queries), default=0) + 1
    fact = [1] * N
    for i in range(1, N):
        fact[i] = fact[i - 1] * i % MOD                 # i! mod p
    inv_fact = [1] * N
    inv_fact[N - 1] = pow(fact[N - 1], MOD - 2, MOD)    # Fermat: a^(p-2) is a's inverse mod a prime p
    for i in range(N - 1, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD         # 1/(i-1)! = i/i!
    out = []
    for n, k in queries:
        if k < 0 or k > n:
            out.append(0)
        else:
            out.append(fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD)
    return out

print(comb_mod([(5, 2), (10, 0), (10, 10), (3, 5)]))
```
```python slow
import math

MOD = 10**9 + 7

def comb_mod(queries):
    return [math.comb(n, k) % MOD if 0 <= k <= n else 0 for n, k in queries]
```
hint: C(n, k) = n! / (k! (n − k)!). Factorials mod p are easy to build in one loop. What replaces the division?
hint: Multiplying by modular inverses. For a prime p, the inverse of a is `pow(a, p - 2, p)`. Precompute `fact[i]` and `inv_fact[i]` for every i up to the largest n, once.
hint: Build `fact` with `fact[i] = fact[i-1] * i % MOD`. Set `inv_fact[N-1] = pow(fact[N-1], MOD - 2, MOD)`, then go down with `inv_fact[i-1] = inv_fact[i] * i % MOD`. Answer each query as `fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD`.
approach:
1. **Understand:** many queries; answers mod a prime; k outside 0..n gives 0.
2. **Examples:** C(5, 2) = 10; C(3, 5) = 0.
3. **Brute force:** `math.comb` per query: exact big integers with tens of thousands of digits.
4. **Pattern:** **precompute once, answer in O(1)**: factorial and inverse-factorial tables with **modular inverses**.
5. **Plan:** tables up to the largest n; one inverse with `pow`, the rest by a backwards loop.
6. **Code and test:** C(0, 0), k out of range, the largest n.
walkthrough:
**Line by line**

- `fact[i]` holds i! mod p, built from the previous value.
- Only **one** `pow` call is needed: the inverse of N−1 factorial. Because (i − 1)! = i! / i, its inverse is `inv_fact[i] * i`, so the loop fills the rest going down.
- Each answer multiplies three precomputed numbers, taking `% MOD` after each product so the numbers stay small.
- Out-of-range k is answered with 0 before indexing.

**Trace** for C(5, 2) (small numbers, so the modulus never kicks in): fact = 1, 1, 2, 6, 24, 120; 5! / (2! · 3!) = 120 / (2 · 6) = 10, computed as 120 × inverse(2) × inverse(6).

**Complexity:** O(N + Q) time for the largest n = N and Q queries (plus one O(log p) power), O(N) space.

**Common wrong approach:** computing `fact[n] // (fact[k] * fact[n - k])` with the modded factorials. Integer division of remainders gives nonsense; modular division must use inverses.
:::

:::quiz
? What does Euclid's algorithm compute, and how fast?
+ The greatest common divisor, in O(log min(a, b)) steps
- The least common multiple, in O(a × b)
- All divisors, in O(n)
= gcd(a, b) = gcd(b, a mod b); the numbers shrink quickly.
? Why does the sieve of Eratosthenes start crossing out multiples of p at p²?
+ Smaller multiples of p have a smaller prime factor and are already crossed out
- p² is the first multiple that is even
- To save memory
= For example, 3 × 2 = 6 was already crossed out as a multiple of 2.
? How do you divide by b when working modulo a prime p?
+ Multiply by b's modular inverse, pow(b, p − 2, p) or pow(b, -1, p)
- Use integer division //
- Take the remainder first, then divide
= Division doesn't distribute over mod; multiplying by the inverse does.
? What does reservoir sampling achieve?
+ k uniformly random items from a stream, in one pass and O(k) memory
- Sorting a stream
- The k largest items of a stream
= Item i replaces a kept item with probability k / (i + 1).
:::

@@@ lesson
id: problem-patterns
title: Recognising the pattern
minutes: 26
summary: Turning a new problem into a known one: reading the input size to pick a target complexity, clue words that point to each technique, choosing a data structure by the operation that must be fast, an edge-case checklist, and the Python toolkit for interviews.
---
After 48 lessons you know dozens of techniques. The hard part of a new problem is usually **step 4 of the 6-step method** (Lesson 2): spotting which technique it needs. This lesson collects the signals, so you can go from "I've never seen this" to "this is a sliding window" in a minute.

### Signal 1: the input size tells you the target complexity

Python manages very roughly 10⁷ simple steps per second (compiled languages perhaps 10⁸–10⁹). Coding judges usually allow about 1–2 seconds, so the limits on n say which complexity the intended solution has:

| Largest n | Target complexity | Typical techniques |
|---|---|---|
| ≤ 10 | O(n!) | permutations, backtracking |
| ≤ 20–25 | O(2ⁿ), O(2ⁿ · n) | subsets, bitmask DP, meet in the middle |
| ≤ 100–500 | O(n³) | Floyd-Warshall, interval DP |
| ≤ 2,000–5,000 | O(n²) | 2-D DP, all pairs |
| ≤ 10⁵–10⁶ | O(n log n) or O(n) | sorting, heaps, binary search, two pointers, hashing, sliding window |
| ≤ 10⁹ or more | O(log n) or O(1) | binary search on the answer, maths, fast exponentiation |

If n is 10⁵ and your idea is O(n²), it's the wrong idea, however correct it is.

### Signal 2: clue words

| Clue in the problem | Think of | Lessons |
|---|---|---|
| "sorted array", "find a pair", "in place" | two pointers, binary search | 7, 24 |
| "contiguous subarray / substring", "longest / shortest window" | sliding window | 8 |
| "sum of a range", "subarray sums to k" | prefix sums (+ hash map) | 9, 14 |
| "seen before", "duplicate", "count occurrences", "anagram" | hash set / dict / Counter | 13, 14 |
| "next greater", "previous smaller", "span" | monotonic stack | 18 |
| "matching brackets", "undo", "nested" | stack | 17 |
| "minimum / maximum of a sliding window" | monotonic deque | 19 |
| "recently used", "evict" | dict + linked list (OrderedDict) | 20 |
| "all subsets / permutations / combinations", "place n queens" | backtracking | 23 |
| "minimise the maximum", "smallest x such that…" | binary search on the answer | 25 |
| "k-th largest", "top k", "closest k", "merge k sorted" | heap | 32 |
| "running median" | two heaps | 32 |
| "prefix", "autocomplete", "dictionary of words" | trie | 33 |
| "range query with updates" | Fenwick or segment tree | 34 |
| "grid", "islands", "connected", "reach" | BFS / DFS | 35 |
| "shortest path", "fewest steps" (unweighted) | BFS | 36 |
| "prerequisites", "order of tasks", "dependencies" | topological sort | 37 |
| "cheapest route", "weighted" | Dijkstra, Bellman-Ford | 38 |
| "groups merge", "connect", "redundant edge" | union-find | 39 |
| "count the ways", "minimum cost", "is it possible", choices that affect later choices | dynamic programming | 41–44 |
| "intervals", "meetings", "overlap" | sort + sweep, heap | 46 |
| "appears once while others appear twice", "subsets of ≤ 20 items" | bit manipulation | 47 |
| "modulo 10⁹ + 7", "primes", "divisible" | number theory | 48 |

### Signal 3: which operation must be fast?

Often the brute force is fine except for **one** repeated operation. Pick the structure that makes that operation cheap:

| Repeated operation | Structure | Cost |
|---|---|---|
| "Is x here?", "how many times?" | `set`, `dict`, `Counter` | O(1) |
| Smallest / largest, with inserts | heap | O(log n) |
| Items in sorted order, with inserts and "next bigger than x" | sorted list + `bisect`, or `SortedList` | O(log n) search |
| Add / remove at both ends | `deque` | O(1) |
| Last in, first out | list as a stack | O(1) |
| Range sums on fixed data | prefix sums | O(1) per query |
| "Are a and b connected?" while merging groups | union-find | ~O(1) |
| Strings by prefix | trie | O(length) |

### Edge-case checklist

Run through this list before you say "done":

- **Empty** input, a **single** item, **two** items.
- All items **equal**; already **sorted**; sorted in **reverse**.
- **Negative** numbers, **zero**, very **large** numbers (and overflow in other languages).
- **Duplicates**, where the problem assumed distinct values.
- The answer at the **very start** or **very end**; **no** valid answer (−1, None, empty list).
- Off-by-one: inclusive vs exclusive ranges, `<` vs `<=` in loops and binary search.
- Deep recursion on the largest input (use a loop or an explicit stack).

### The Python interview toolkit

Knowing the standard library saves minutes and bugs. These are the pieces used most in this course:

```python
from collections import Counter, defaultdict, deque
from itertools import accumulate, combinations, pairwise, groupby
from bisect import bisect_left, insort
from functools import cache
import heapq, math

words = "the quick cat and the lazy dog and the cat".split()
print(Counter(words).most_common(2))                     # counting
groups = defaultdict(list)
for w in words:
    groups[len(w)].append(w)                             # grouping without key checks
print(dict(groups))
print(list(accumulate([3, 1, 4, 1, 5])))                 # prefix sums
print(list(pairwise([1, 4, 9, 16])))                     # neighbouring pairs (3.10+)
print([(k, len(list(g))) for k, g in groupby("aaabccdd")])   # run-length groups
print(list(combinations("abc", 2)))
q = deque([1, 2, 3]); q.appendleft(0); q.pop(); print(q)
s = [10, 20, 30]; insort(s, 25); print(s, bisect_left(s, 25))
print(heapq.nlargest(2, [5, 1, 9, 3]), math.inf > 10**100)
print(sorted(words, key=lambda w: (-len(w), w))[:3])     # sort by length descending, then alphabetically
```

| Need | Use |
|---|---|
| counts, most common | `Counter`, `.most_common(k)` |
| dict of lists / ints without key checks | `defaultdict(list)`, `defaultdict(int)` |
| queue / deque / sliding window | `deque`, `.popleft()`, `deque(maxlen=k)` |
| heap, top k | `heapq.heappush/heappop`, `nlargest`, `nsmallest`, `merge` |
| sorted insert, lower/upper bound | `bisect_left`, `bisect_right`, `insort` |
| prefix sums, pairs, groups | `accumulate`, `pairwise`, `groupby` |
| subsets, orders, grids of options | `combinations`, `permutations`, `product` |
| memoisation, custom sort | `@cache`, `cmp_to_key` |
| integer maths | `math.gcd`, `math.lcm`, `math.isqrt`, `math.comb`, `pow(a, b, m)` |
| infinity | `math.inf` or `float("inf")` |

### Talking through a problem

Interviewers grade **how** you get to the answer as much as the answer:

1. Restate the problem and ask about the input: sizes, sorted or not, duplicates, negative numbers, what to return when there's no answer.
2. Work through an example out loud.
3. State the brute force and its complexity **before** optimising: "Checking every pair is O(n²); n is 10⁵, so I need better."
4. Name the pattern and why it fits: "The array is sorted and we want a pair, so two pointers."
5. Code it cleanly with clear names; narrate the tricky lines.
6. Test with your example and an edge case; then give the final time and space complexity.

If you're stuck, say what you've ruled out and why; ask for a hint early rather than late; and offer the brute force rather than nothing.

:::exercise Product of everything else
Write `product_except_self(nums)` returning a list where item i is the product of every number in `nums` **except** `nums[i]`. Don't use division (the list may contain zeros), and make it O(n): 100,000 numbers in well under a second.
```python starter
def product_except_self(nums):
    pass

print(product_except_self([1, 2, 3, 4]))       # [24, 12, 8, 6]
print(product_except_self([-1, 1, 0, -3, 3]))  # [0, 0, 9, 0, 0]
```
```python check
fn = need("product_except_self")
import re as _re
_code = "\n".join(line.split("#")[0] for line in __source__.splitlines())
if "/" in _code:
    raise AssertionError("Solve it without division ( / or // ): a zero in the list would break it. Multiply what's on the left of each position by what's on its right.")
test(fn, cases=[
    (([1, 2, 3, 4],), [24, 12, 8, 6], "the example"),
    (([-1, 1, 0, -3, 3],), [0, 0, 9, 0, 0], "one zero"),
    (([0, 0, 2],), [0, 0, 0], "two zeros"),
    (([5, 7],), [7, 5], "two numbers"),
    (([2, 2, 2, 2],), [8, 8, 8, 8], "equal numbers"),
    (([-2, 3, -4],), [-12, 8, -6], "negative numbers"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    return ([rng.choice([-1, 1]) for _ in range(n)],)
def _ref(nums):
    n = len(nums); out = [1] * n; p = 1
    for i in range(n): out[i] = p; p *= nums[i]
    p = 1
    for i in range(n - 1, -1, -1): out[i] *= p; p *= nums[i]
    return out
speed(fn, _make, _ref, sizes=(1_000, 5_000, 100_000), what="numbers",
      tip="Multiplying everything else for each position is O(n^2). Compute running products from the left and from the right; each answer is left product x right product.")
```
```python solution
def product_except_self(nums):
    n = len(nums)
    answer = [1] * n
    left = 1
    for i in range(n):
        answer[i] = left            # product of everything to the left of i
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= right          # times the product of everything to the right of i
        right *= nums[i]
    return answer

print(product_except_self([1, 2, 3, 4]))
print(product_except_self([-1, 1, 0, -3, 3]))
```
```python slow
def product_except_self(nums):
    out = []
    for i in range(len(nums)):
        p = 1
        for j in range(len(nums)):
            if j != i:
                p *= nums[j]
        out.append(p)
    return out
```
hint: The product of everything except `nums[i]` splits into two parts. Which?
hint: The product of everything to the **left** of i times the product of everything to the **right** of i. Both can be built as running products, like prefix sums (Lesson 9).
hint: First pass left to right: `answer[i] = left; left *= nums[i]`. Second pass right to left: `answer[i] *= right; right *= nums[i]`.
approach:
1. **Understand:** no division; zeros and negatives allowed; the output has the same length.
2. **Examples:** [1, 2, 3, 4] → [24, 12, 8, 6].
3. **Brute force:** for each i, multiply all the others: O(n²). Dividing the total by `nums[i]` fails on zeros (and is banned here).
4. **Pattern:** **prefix and suffix products**.
5. **Plan:** a left-to-right pass storing left products, then a right-to-left pass multiplying in right products.
6. **Code and test:** one zero, two zeros, two numbers, negatives.
walkthrough:
**Line by line**

- After the first loop, `answer[i]` is the product of `nums[0..i−1]` (1 for i = 0).
- The second loop walks backwards with `right` = the product of `nums[i+1..]`, multiplying it in.
- Each value is used in the running product only **after** being skipped for its own position, which is what "except self" needs.
- Two passes and one output list: no division anywhere, so zeros are handled naturally.

**Trace** on [1, 2, 3, 4]:

| i | left before | after pass 1 | right before | final answer[i] |
|---|---|---|---|---|
| 0 | 1 | 1 | 24 | 24 |
| 1 | 1 | 1 | 12 | 12 |
| 2 | 2 | 2 | 4 | 8 |
| 3 | 6 | 6 | 1 | 6 |

**Complexity:** O(n) time, O(1) extra space besides the output.

**Common wrong approach:** total product divided by `nums[i]`: it crashes (or is wrong) as soon as the list contains a zero.
:::

:::exercise Top k frequent
Write `top_k_frequent(nums, k)` returning the `k` most frequent values in `nums`, in any order. The answer is guaranteed to be unique (no ties at the cut-off).
```python starter
from collections import Counter

def top_k_frequent(nums, k):
    pass

print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))   # [1, 2] in any order
```
```python check
fn = need("top_k_frequent")
_k = lambda r: sorted(r) if isinstance(r, (list, tuple, set)) else r
test(fn, key=_k, cases=[
    (([1, 1, 1, 2, 2, 3], 2), [1, 2], "the example"),
    (([1], 1), [1], "one number"),
    (([4, 4, 5, 5, 5, 6], 1), [5], "k = 1"),
    (([7, 8, 9], 3), [7, 8, 9], "every value"),
    (([-1, -1, 2, 2, 2, 3, 3, 3, 3], 2), [2, 3], "negative values"),
    (([5, 3, 5, 3, 5, 1, 3, 5], 2), [3, 5], "interleaved"),
])
```
```python solution
from collections import Counter

def top_k_frequent(nums, k):
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]      # buckets[f]: values seen exactly f times
    for value, f in counts.items():
        buckets[f].append(value)
    result = []
    for f in range(len(nums), 0, -1):                 # from the highest frequency down
        for value in buckets[f]:
            result.append(value)
            if len(result) == k:
                return result
    return result

print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))
```
hint: First count how often each value appears. Then you need the k values with the largest counts.
hint: `Counter(nums).most_common(k)` does it (O(n log n) or O(n log k)). A heap of size k works too. For O(n), use **bucket sort**: a frequency can't exceed n.
hint: Make `buckets[f]` = the values appearing f times, for f from 0 to n. Walk f from n down to 1, collecting values until you have k.
approach:
1. **Understand:** k values with the highest counts; any order; no ties at the boundary.
2. **Examples:** [1, 1, 1, 2, 2, 3], k = 2 → [1, 2].
3. **Brute force:** count, then sort the distinct values by count: O(n log n), already acceptable.
4. **Pattern:** **counting + bucket sort** (or a heap of size k).
5. **Plan:** Counter, buckets indexed by frequency, read from the top.
6. **Code and test:** k = 1, k = number of distinct values, negatives.
walkthrough:
**Line by line**

- `Counter` counts every value in O(n).
- Frequencies are between 1 and n, so a list of n + 1 buckets can hold every value at its frequency: no comparison sort needed.
- Reading buckets from the highest frequency down yields values in decreasing frequency; stop at k.

**Trace** on [1, 1, 1, 2, 2, 3], k = 2: counts {1: 3, 2: 2, 3: 1}; buckets[3] = [1], buckets[2] = [2], buckets[1] = [3]; reading down collects 1, then 2: done.

**Complexity:** O(n) time and space. `Counter.most_common(k)` uses a heap: O(n log k).

**Common wrong approach:** returning the first k distinct values or sorting the values themselves instead of their counts.
:::

:::quiz
? The input size is up to 10⁵. Which complexity should you aim for?
+ O(n log n) or better
- O(n²)
- O(2ⁿ)
= 10¹⁰ steps (n²) is far too slow; 10⁵ × 17 is fine.
? "Find the minimum time such that all the work finishes" with a yes/no check that's easy for a given time suggests:
+ Binary search on the answer
- A trie
- Topological sort
= If time t works, any larger t also works: a monotonic test.
? You repeatedly need the smallest item while also inserting new ones. Which structure?
+ A heap
- A sorted list rebuilt each time
- A stack
= Push and pop-min are O(log n).
? Which of these is the best first move in an interview after understanding the question?
+ Work an example and state a brute-force solution with its complexity
- Start coding the most optimised solution immediately
- Ask for the answer
= A correct baseline and a clear complexity target guide the optimisation.
:::

@@@ lesson
id: mock-interviews
title: Mock interviews
minutes: 30
summary: Full interview problems worked from the question to tested code (longest consecutive sequence, a time-based key-value store), then three classic practice problems (trapping rain water, minimum window substring, decode string), and how to keep practising after the course.
---
This last lesson puts everything together. Each worked problem follows the 6-step method exactly as you'd say it out loud in an interview: understand, examples, brute force, pattern, plan, code and test. Then it's your turn with three well-known problems that mix several techniques.

### Worked problem 1: longest consecutive sequence

> Given an unsorted list of integers, return the length of the longest run of **consecutive** values (in any order in the list). It must be O(n).

**1. Understand.** [100, 4, 200, 1, 3, 2] contains 1, 2, 3, 4: length 4. Duplicates may appear and count once; an empty list gives 0. The O(n) requirement rules out sorting.

**2. Examples.** [0, 3, 7, 2, 5, 8, 4, 6, 0, 1] → 0..8 → 9. [] → 0. [5, 5] → 1.

**3. Brute force.** Sort, then count runs: O(n log n), simple and a good thing to say first. Without sorting, checking `x + 1 in list` repeatedly is O(n²) or worse.

**4. Pattern.** "Is x + 1 present?" in O(1) means a **hash set**. The waste in the naive set version is counting the same run from every member; only start counting at a value whose predecessor **isn't** in the set: the start of a run.

**5. Plan.** Put everything in a set. For each value x with x − 1 not in the set, count upwards while x + 1, x + 2, … are present. Track the longest run.

**6. Code and test.**

```python
def longest_consecutive(nums):
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 in values:
            continue                    # not the start of a run: it'll be counted from its start
        length = 1
        while x + length in values:
            length += 1
        best = max(best, length)
    return best

for test in ([100, 4, 200, 1, 3, 2], [0, 3, 7, 2, 5, 8, 4, 6, 0, 1], [], [5, 5], [-2, -1, 1]):
    print(test, longest_consecutive(test))
```

**Complexity, said out loud:** "Each value is the start of at most one counted run, and each step of a run's `while` loop visits a different value, so the inner loop runs at most n times **in total**: O(n) time, O(n) space for the set."

### Worked problem 2: a time-based key-value store

> Design `TimeMap` with `set(key, value, timestamp)` and `get(key, timestamp)`, which returns the value set for that key at the **latest timestamp ≤ the given one** (or "" if none). Timestamps passed to `set` are strictly increasing.

**1–2. Understand and examples.** set("foo", "bar", 1); get("foo", 1) → "bar"; get("foo", 3) → "bar"; set("foo", "bar2", 4); get("foo", 4) → "bar2"; get("foo", 3) → "bar"; get("foo", 0) → "".

**3. Brute force.** Store a list of (timestamp, value) per key and scan it backwards on every `get`: O(n) per query.

**4. Pattern.** Timestamps arrive **in increasing order**, so each key's list is already **sorted**: "the latest timestamp ≤ t" is a **binary search** (`bisect_right` − 1), O(log n). A dict of lists gives per-key storage.

**5–6. Plan, code and test.**

```python
from bisect import bisect_right
from collections import defaultdict

class TimeMap:
    def __init__(self):
        self.times = defaultdict(list)      # key -> sorted timestamps
        self.values = defaultdict(list)     # key -> values, in the same order

    def set(self, key, value, timestamp):
        self.times[key].append(timestamp)   # stays sorted: timestamps only increase
        self.values[key].append(value)

    def get(self, key, timestamp):
        i = bisect_right(self.times[key], timestamp) - 1   # the last timestamp <= the query
        return self.values[key][i] if i >= 0 else ""

tm = TimeMap()
tm.set("foo", "bar", 1)
print(repr(tm.get("foo", 1)), repr(tm.get("foo", 3)))
tm.set("foo", "bar2", 4)
print(repr(tm.get("foo", 4)), repr(tm.get("foo", 3)), repr(tm.get("foo", 0)), repr(tm.get("nope", 5)))
```

**Follow-up questions to expect:** "What if timestamps can arrive out of order?" (insert with `insort`, O(n) per set, or use a balanced tree / `SortedList`); "What about memory for keys with millions of versions?" (keep only recent versions, or archive old ones). Thinking about follow-ups shows depth.

### Three practice problems

The exercises below are interview classics that combine techniques: **two pointers** with a running maximum, a **sliding window** with counts, and a **stack** (or recursion) for nested structure.

![The elevation map [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1] drawn as grey bars, with the trapped water shown in blue between them. Water above each bar reaches the smaller of the tallest bar on its left and the tallest on its right; 6 units are trapped in total](figures/rain-water.svg)

### Keep practising

- **Mix your practice.** After a course organised by topic, the real skill is choosing the technique. Practise **mixed** problem sets where the topic isn't announced, and use the clue-word table from Lesson 49.
- **Space it out.** Re-solve problems you found hard after a few days, then a few weeks, without looking at your old solution.
- **Time yourself** (about 20–35 minutes per medium problem) and practise explaining aloud, as you would to an interviewer.
- **Write the brute force first** when stuck, then ask where it wastes work.
- **Use online judges** (LeetCode, HackerRank, Codeforces and similar) for a steady supply of problems with hidden tests, like the checks in this course.
- **Use AI assistants as a tutor, not a crutch:** ask for a hint or to explain a concept or a bug, but write the solution yourself; the skill only grows when you do the thinking.
- **Keep the cheat sheet and glossary** of this course nearby; they summarise every pattern and its complexity.

:::exercise Trapping rain water
`heights` gives the heights of bars of width 1. Write `trap(heights)` returning how many units of rain water are trapped between the bars after it rains. It must be O(n): 200,000 bars in well under a second.
```python starter
def trap(heights):
    pass

print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # 6
print(trap([4, 2, 0, 3, 2, 5]))                     # 9
```
```python check
fn = need("trap")
test(fn, cases=[
    (([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6, "the first example"),
    (([4, 2, 0, 3, 2, 5],), 9, "the second example"),
    (([],), 0, "no bars"),
    (([5],), 0, "one bar"),
    (([1, 2, 3, 4],), 0, "rising: water runs off"),
    (([3, 0, 3],), 3, "a single pit"),
    (([5, 4, 1, 2],), 1, "the right wall is lower"),
    (([2, 0, 2, 0, 2],), 4, "two pits"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    return ([rng.randint(0, 100) for _ in range(n)],)
def _ref(h):
    l, r, lm, rm, w = 0, len(h) - 1, 0, 0, 0
    while l < r:
        if h[l] < h[r]:
            lm = max(lm, h[l]); w += lm - h[l]; l += 1
        else:
            rm = max(rm, h[r]); w += rm - h[r]; r -= 1
    return w
speed(fn, _make, _ref, sizes=(1_000, 4_000, 200_000), what="bars",
      tip="Scanning left and right for the tallest bars at every position is O(n^2). Use two pointers that move inwards with running maximums (or precompute left-max and right-max arrays).")
```
```python solution
def trap(heights):
    left, right = 0, len(heights) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if heights[left] < heights[right]:
            # the right side has a bar at least this tall, so the left wall decides the water here
            left_max = max(left_max, heights[left])
            water += left_max - heights[left]
            left += 1
        else:
            right_max = max(right_max, heights[right])
            water += right_max - heights[right]
            right -= 1
    return water

print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
print(trap([4, 2, 0, 3, 2, 5]))
```
```python slow
def trap(heights):
    total = 0
    for i in range(len(heights)):
        tallest_left = 0
        for j in range(i + 1):
            tallest_left = max(tallest_left, heights[j])
        tallest_right = 0
        for j in range(i, len(heights)):
            tallest_right = max(tallest_right, heights[j])
        total += min(tallest_left, tallest_right) - heights[i]
    return total
```
hint: How much water sits above one bar? It depends on the tallest bar to its left and the tallest bar to its right.
hint: Water above bar i is `min(max_left, max_right) - heights[i]`. Precomputing both maximums as arrays gives O(n) time and O(n) space. Can two pointers avoid the arrays?
hint: Move pointers inwards from both ends, keeping `left_max` and `right_max`. Always move the side with the **lower** bar: that side's maximum is the limiting wall, because the other side is known to have something at least as tall.
approach:
1. **Understand:** bars of width 1; water can't spill over the ends; return the total.
2. **Examples:** [3, 0, 3] → 3; [1, 2, 3, 4] → 0.
3. **Brute force:** for each bar, scan for the tallest on each side: O(n²).
4. **Pattern:** **prefix maximums**, refined into **two pointers** with running maximums.
5. **Plan:** pointers at both ends; process the lower side, adding `side_max - height`.
6. **Code and test:** empty, one bar, rising heights, a lower right wall.
walkthrough:
**Line by line**

- If `heights[left] < heights[right]`, there's a bar on the right at least as tall as anything we need: the water at `left` is limited only by `left_max`, which we know exactly.
- Updating `left_max` first means a bar taller than everything before it adds 0 water and becomes the new wall.
- The symmetric branch handles the right side. Each step moves one pointer inwards, so the loop runs n − 1 times.

**Trace** on [4, 2, 0, 3, 2, 5]:

| left, right | lower side | side max | water added | total |
|---|---|---|---|---|
| 0, 5 | left (4 < 5) | 4 | 0 | 0 |
| 1, 5 | left (2) | 4 | 2 | 2 |
| 2, 5 | left (0) | 4 | 4 | 6 |
| 3, 5 | left (3) | 4 | 1 | 7 |
| 4, 5 | left (2) | 4 | 2 | **9** |

**Complexity:** O(n) time, O(1) space.

**Common wrong approach:** adding up dips between neighbouring bars only. Water depends on the tallest bars anywhere to the left and right, not on the neighbours.
:::

:::exercise Minimum window substring
Write `min_window(s, t)` returning the shortest substring of `s` that contains every character of `t` (counting duplicates: if t has two "a"s, the window needs two). Return "" if there's none; if several shortest windows exist, return the leftmost. It must be O(len(s) + len(t)): a 100,000-character `s` in well under a second.
```python starter
from collections import Counter

def min_window(s, t):
    pass

print(min_window("ADOBECODEBANC", "ABC"))   # "BANC"
print(min_window("a", "aa"))                # ""
```
```python check
fn = need("min_window")
test(fn, cases=[
    (("ADOBECODEBANC", "ABC"), "BANC", "the example"),
    (("a", "a"), "a", "one character"),
    (("a", "aa"), "", "not enough copies"),
    (("aa", "aa"), "aa", "duplicates in t"),
    (("abc", "d"), "", "a missing character"),
    (("ab", "b"), "b", "the answer at the end"),
    (("cabwefgewcwaefgcf", "cae"), "cwae", "a longer string"),
    (("bba", "ab"), "ba", "the leftmost shortest window"),
])
from collections import Counter as _C
def _make(n):
    return ("z" + "abc" * ((n - 2) // 3) + "z", "zz")
def _ref(s, t):
    need = _C(t); missing = len(t); left = 0; best = (float("inf"), 0, 0)
    for right, ch in enumerate(s):
        if need[ch] > 0: missing -= 1
        need[ch] -= 1
        if missing == 0:
            while need[s[left]] < 0:
                need[s[left]] += 1; left += 1
            if right - left + 1 < best[0]: best = (right - left + 1, left, right + 1)
            need[s[left]] += 1; missing += 1; left += 1
    return "" if best[0] == float("inf") else s[best[1]:best[2]]
speed(fn, _make, _ref, sizes=(300, 1_500, 100_000), what="characters in s",
      tip="Trying every start and extending to the right is O(n^2). Use a sliding window: grow the right edge until the window is valid, then shrink the left edge as far as it stays valid, tracking how many characters are still missing.")
```
```python solution
from collections import Counter

def min_window(s, t):
    need = Counter(t)             # how many more of each character the window needs (negative = spare)
    missing = len(t)              # characters of t still missing from the window
    left = 0
    best_len, best_start = float("inf"), 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1          # this character fills a real need
        need[ch] -= 1
        while missing == 0:       # the window s[left..right] is valid: try to shrink it
            if right - left + 1 < best_len:
                best_len, best_start = right - left + 1, left
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1      # removed a needed character: the window is no longer valid
            left += 1
    return "" if best_len == float("inf") else s[best_start:best_start + best_len]

print(min_window("ADOBECODEBANC", "ABC"))
print(min_window("a", "aa"))
```
```python slow
from collections import Counter

def min_window(s, t):
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        have = Counter()
        for j in range(i, len(s)):
            have[s[j]] += 1
            if all(have[c] >= k for c, k in need.items()):
                if not best or j - i + 1 < len(best):
                    best = s[i:j + 1]
                break
    return best
```
hint: "Shortest substring containing…" is a variable-size **sliding window** (Lesson 8). When should the window grow, and when should it shrink?
hint: Grow the right edge until the window contains everything; then shrink from the left while it still does, recording the length each time. To check validity in O(1), keep `need` counts and a single number `missing` of characters still needed.
hint: `need = Counter(t)`, `missing = len(t)`. For each new char: if `need[ch] > 0`, `missing -= 1`; then `need[ch] -= 1`. While `missing == 0`: record the window, add the left char back (`need[s[left]] += 1`; if it becomes > 0, `missing += 1`), and move `left` on.
approach:
1. **Understand:** counts matter (duplicates in t); shortest window; leftmost on ties; "" if impossible.
2. **Examples:** "ADOBECODEBANC", "ABC" → "BANC"; "a", "aa" → "".
3. **Brute force:** every start, extend until valid: O(n²) windows (each check also costs time).
4. **Pattern:** **sliding window with counts** and a `missing` counter for O(1) validity checks.
5. **Plan:** expand right; while valid, record and shrink from the left.
6. **Code and test:** duplicates in t, impossible cases, answer at the end, ties.
walkthrough:
**Line by line**

- `need[c]` starts as the count of c in t; it goes negative when the window holds spare copies.
- `missing` counts characters of t not yet covered. A character only reduces it if it was still needed (`need[ch] > 0` before decrementing).
- While `missing == 0`, every window from `left` to `right` is valid; recording before shrinking means the shortest valid window ending at `right` is seen. Strict `<` keeps the leftmost on ties.
- Removing `s[left]` gives back one copy; if that makes its need positive, the window just lost a required character.
- Each index enters and leaves the window once: O(n).

**Trace** on s = "bba", t = "ab" (need a: 1, b: 1, missing 2):

| right | char | missing after | valid windows recorded | left after |
|---|---|---|---|---|
| 0 | b | 1 | — | 0 |
| 1 | b | 1 (spare b) | — | 0 |
| 2 | a | 0 | "bba" (3), then "ba" (2) | 2 |

**Complexity:** O(len(s) + len(t)) time, O(alphabet) space.

**Common wrong approach:** using a set of t's characters, which ignores duplicates ("aa" needs two a's), or checking the whole `Counter` for validity at every step, which multiplies the work by the alphabet size.
:::

:::exercise Decode string
Strings are encoded as `k[text]`, meaning `text` repeated k times; brackets can nest, and plain letters can appear anywhere. Write `decode(s)` returning the decoded string. For example "3[a2[c]]" → "accaccacc". k is a positive integer that may have several digits.
```python starter
def decode(s):
    pass

print(decode("3[a]2[bc]"))     # aaabcbc
print(decode("3[a2[c]]"))      # accaccacc
print(decode("2[abc]3[cd]ef")) # abcabccdcdcdef
```
```python check
fn = need("decode")
test(fn, cases=[
    (("3[a]2[bc]",), "aaabcbc", "two groups"),
    (("3[a2[c]]",), "accaccacc", "nested"),
    (("2[abc]3[cd]ef",), "abcabccdcdcdef", "letters after the groups"),
    (("abc",), "abc", "no brackets"),
    (("",), "", "empty"),
    (("10[a]",), "aaaaaaaaaa", "a two-digit count"),
    (("2[a2[b2[c]]]",), "abccbccabccbcc", "three levels deep"),
    (("x1[y]z",), "xyz", "a count of 1"),
])
```
```python solution
def decode(s):
    stack = []                     # (text before the bracket, repeat count) for each open bracket
    current, number = "", 0
    for ch in s:
        if ch.isdigit():
            number = number * 10 + int(ch)          # counts can have several digits
        elif ch == "[":
            stack.append((current, number))         # save where we were
            current, number = "", 0                 # start the text inside the brackets
        elif ch == "]":
            before, k = stack.pop()
            current = before + current * k          # finish the group and rejoin the outer text
        else:
            current += ch
    return current

print(decode("3[a]2[bc]"))
print(decode("3[a2[c]]"))
print(decode("2[abc]3[cd]ef"))
```
hint: Brackets nest, like the bracket-matching problem in Lesson 17. What must you remember when you meet `[`, so you can finish the job at the matching `]`?
hint: At `[`, push the text built so far and the repeat count onto a stack, then start fresh. At `]`, pop them and set `current = text_before + current * count`.
hint: Keep `current` (the text being built) and `number` (digits read so far: `number = number * 10 + int(ch)`). Letters are appended to `current`. Return `current` at the end.
approach:
1. **Understand:** nested groups; multi-digit counts; letters outside groups; empty input.
2. **Examples:** "3[a2[c]]": inner "2[c]" → "cc", so "acc" × 3.
3. **Brute force:** repeatedly find an innermost `k[...]` with a regular expression and expand it until none remain: correct, but each pass rebuilds the string.
4. **Pattern:** **stack for nested structure** (recursion works too).
5. **Plan:** scan once; digits build a number; `[` pushes state; `]` pops and repeats; letters append.
6. **Code and test:** two-digit counts, three nesting levels, text before and after groups.
walkthrough:
**Line by line**

- `number = number * 10 + int(ch)` turns consecutive digits like "10" into 10.
- At `[`, the outer text and the count are saved, and `current` restarts for the inside of the group.
- At `]`, the inner text is repeated and appended to the saved outer text, which becomes `current` again: exactly how nesting unwinds.
- Letters simply extend `current`, inside or outside brackets.

**Trace** on "3[a2[c]]":

| char | stack | current | number |
|---|---|---|---|
| 3 | | "" | 3 |
| [ | ("", 3) | "" | 0 |
| a | ("", 3) | "a" | 0 |
| 2 | ("", 3) | "a" | 2 |
| [ | ("", 3), ("a", 2) | "" | 0 |
| c | ("", 3), ("a", 2) | "c" | 0 |
| ] | ("", 3) | "a" + "c" × 2 = "acc" | 0 |
| ] | — | "" + "acc" × 3 = **"accaccacc"** | 0 |

**Complexity:** O(length of the output) time (building the repeated strings), O(nesting depth + output) space.

**Common wrong approach:** reading only one digit for the count, so "10[a]" becomes "0[a]" after a stray "1".
:::

:::quiz
? In "longest consecutive sequence", why only start counting at x when x − 1 isn't in the set?
+ So each run is counted once from its start, keeping the total work O(n)
- Because negative numbers aren't allowed
- To sort the numbers
= Counting from every member of a run would make it O(n²).
? Why is binary search valid in the TimeMap's get?
+ Timestamps are appended in increasing order, so each key's list is already sorted
- Because keys are sorted
- Python lists are always sorted
= "Latest timestamp ≤ t" is bisect_right − 1 on a sorted list.
? In the two-pointer rain-water solution, which side moves?
+ The side with the lower bar, because its own maximum limits the water there
- Always the left side
- The side with the taller bar
= The other side is known to have a bar at least as tall.
? What is the best way to practise after finishing a topic-by-topic course?
+ Mixed problem sets where the technique isn't announced, revisited over time
- Re-reading the same lesson many times
- Memorising solutions word for word
= Choosing the technique is the skill interviews test.
:::
