@@ bit-manipulation
topics: binary in Python, AND, OR, XOR, NOT and shifts, negative numbers and two's complement, setting, clearing and testing bits, the lowest set bit, powers of two, counting bits, XOR puzzles, sets as bitmasks, enumerating subsets and submasks, maximum XOR of two numbers
terms:
- **Bit:** a single binary digit, 0 or 1.
- **Bitwise operator:** an operator that works on each bit position: & (AND), | (OR), ^ (XOR), ~ (NOT), << and >> (shifts).
- **XOR (exclusive or):** 1 where two bits differ; x ^ x = 0 and x ^ 0 = x.
- **Two's complement:** the usual way to store negative integers, where −x equals ~x + 1.
- **Bitmask:** an integer whose bits record which items of a small set are present.
- **Lowest set bit:** the rightmost 1 bit of a number, isolated by x & −x.
- **Submask:** a mask whose 1 bits are a subset of another mask's 1 bits.
mistakes:
- Forgetting operator precedence: `x & 1 == 0` means `x & (1 == 0)`; write `(x & 1) == 0`.
- Expecting fixed-width overflow in Python; mask with `& 0xFFFFFFFF` when you need 32-bit behaviour.
- Using `x & (x − 1) == 0` as a power-of-two test without also checking x > 0.
- Comparing all pairs for a maximum XOR instead of building the answer bit by bit.

glance:
- Test / set / clear / toggle bit i | x >> i & 1, x OR (1 << i), x & ~(1 << i), x ^ (1 << i) | O(1) | O(1)
- Lowest set bit / clear it | x & −x / x & (x − 1) | O(1) | O(1)
- Power of two | x > 0 and x & (x − 1) == 0 | O(1) | O(1)
- Count set bits | x.bit_count(), or Kernighan's loop | O(1) / O(set bits) | O(1)
- Single number among pairs | XOR everything | O(n) | O(1)
- All subsets of n items | masks 0 .. 2ⁿ − 1 | O(2ⁿ · n) | O(1) per mask
- All submasks of every mask | sub = (sub − 1) & mask | O(3ⁿ) | O(1)
- Maximum XOR pair | greedy per bit with a prefix set, or a binary trie | O(n · bits) | O(n)

@@ number-theory
topics: gcd and lcm with Euclid's algorithm, primality by trial division, the sieve of Eratosthenes, prime factorisation, modular arithmetic, modular inverses and Fermat's little theorem, factorials, permutations and combinations, Pascal's triangle, Catalan numbers, float precision and exact arithmetic, Fisher-Yates shuffle, reservoir sampling
terms:
- **gcd / lcm:** the greatest common divisor / least common multiple of two numbers.
- **Euclid's algorithm:** gcd(a, b) = gcd(b, a mod b) until b is 0.
- **Prime:** an integer greater than 1 whose only divisors are 1 and itself.
- **Sieve of Eratosthenes:** finds all primes below n by crossing out multiples of each prime.
- **Modular arithmetic:** arithmetic on remainders after division by a modulus m.
- **Modular inverse:** the number b⁻¹ with b · b⁻¹ ≡ 1 (mod m); it replaces division.
- **Fermat's little theorem:** for a prime p and a not divisible by p, a^(p−1) ≡ 1, so a^(p−2) is a's inverse.
- **Combination C(n, k):** the number of ways to choose k items from n when order doesn't matter.
- **Reservoir sampling:** choosing k random items from a stream in one pass with O(k) memory.
mistakes:
- Dividing modded numbers with `/` or `//` instead of multiplying by an inverse.
- Taking the modulus only at the end, letting numbers grow huge (slow in Python, overflow elsewhere).
- Comparing floats with `==`, or using `int(math.sqrt(n))` for big integers instead of `math.isqrt`.
- Writing a "shuffle" that swaps with any position, which isn't uniform; use Fisher-Yates.

glance:
- gcd / lcm | Euclid; lcm = a · b // gcd | O(log min(a, b)) | O(1)
- Primality | trial division up to √n | O(√n) | O(1)
- All primes below n | sieve of Eratosthenes | O(n log log n) | O(n)
- Prime factorisation | trial division | O(√n) | O(log n)
- Modular power / inverse | pow(a, b, m) / pow(a, −1, m) | O(log b) | O(1)
- Many C(n, k) mod p | factorial and inverse-factorial tables | O(n) once, O(1) per query | O(n)
- Uniform shuffle | Fisher-Yates | O(n) | O(1) in place
- k random items from a stream | reservoir sampling | O(n) | O(k)

@@ problem-patterns
topics: input size and target complexity, clue words and the techniques they point to, choosing a data structure by its fastest operation, an edge-case checklist, the Python standard-library toolkit, talking through a problem in an interview
terms:
- **Target complexity:** the running time the input limits allow, read from the largest n.
- **Clue word:** a phrase in a problem that points to a technique, such as "top k" → heap.
- **Edge case:** an unusual input, like an empty list or all-equal values, that often breaks code.
- **Bucket sort:** placing items into buckets by a small-range key (such as a count) instead of comparing them.
- **Prefix and suffix products:** running products from the left and right, combined per position.
mistakes:
- Optimising before having any correct solution.
- Ignoring the input limits, which say which complexity is needed.
- Testing only the given example and skipping the edge cases.
- Coding silently in an interview instead of explaining the approach and trade-offs.

glance:
- n ≤ 10 / 20 / 500 / 5,000 / 10⁶ / 10⁹ | n! / 2ⁿ / n³ / n² / n log n / log n | — | —
- Product of all others, no division | left products × right products | O(n) | O(1) extra
- Top k frequent | Counter + buckets by count (or most_common(k)) | O(n) (O(n log k)) | O(n)
- Counting / grouping | Counter, defaultdict | O(n) | O(n)
- Sorted inserts and lower bounds | bisect_left, insort | O(log n) search, O(n) insert | O(n)

@@ mock-interviews
topics: the 6-step method in a full interview, longest consecutive sequence with a hash set, a time-based key-value store with binary search, follow-up questions, trapping rain water with two pointers, minimum window substring with a sliding window, decoding nested strings with a stack, how to keep practising
terms:
- **Mock interview:** practising a problem under interview conditions: timed, explained aloud, tested.
- **Follow-up question:** an interviewer's change to the problem to see how the design adapts.
- **Running maximum:** the largest value seen so far while scanning, updated in O(1) per step.
- **Variable-size sliding window:** a window that grows on the right until valid and shrinks on the left while it stays valid.
- **Mixed practice:** solving problems without being told which technique they need.
mistakes:
- Counting a consecutive run from every member instead of only from its start.
- Using a set where duplicates matter (minimum window needs counts).
- Reading only one digit of a multi-digit repeat count.
- Practising only one topic at a time and never choosing the technique yourself.

glance:
- Longest consecutive sequence | set; count runs only from values with no predecessor | O(n) | O(n)
- Time-based key-value store | dict of sorted lists + bisect_right | O(1) set, O(log n) get | O(n)
- Trapping rain water | two pointers; move the lower side with its running max | O(n) | O(1)
- Minimum window substring | sliding window with need counts and a missing counter | O(len(s) + len(t)) | O(alphabet)
- Decode nested string | stack of (text before, count) | O(output) | O(depth + output)
