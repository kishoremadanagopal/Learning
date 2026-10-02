@@@ part
id: 5
title: Recursion
level: Intermediate
blurb: Functions that call themselves: how recursion works on the call stack, how to measure its cost with recursion trees, divide and conquer (fast power, counting inversions, the master theorem), and backtracking (subsets, permutations, N-Queens, Sudoku).

@@@ lesson
id: recursion
title: Recursion and recursion trees
minutes: 22
summary: Base cases and recursive cases, tracing the call stack, recursion on nested structures, measuring cost with recursion trees, memoisation as a first fix, and when to use a loop instead.
---
A **recursive** function solves a problem by calling itself on a **smaller** version of the same problem. Every recursive function has two parts:

- a **base case**: an input so small the answer is obvious, returned directly (no further calls);
- a **recursive case**: break the problem into smaller pieces, call the function on them, and combine their answers.

```python
def factorial(n):
    if n <= 1:                    # base case: 0! = 1! = 1
        return 1
    return n * factorial(n - 1)   # recursive case: n! = n × (n-1)!

print(factorial(5))
```

### What actually happens: the call stack

Each call gets its own **frame** on the call stack (Lesson 17) with its own `n`. Calls pile up until a base case returns; then the frames finish in reverse order, each using the answer from the call above it.

![The call stack for factorial(4). Frames for n = 4, 3, 2 and 1 pile up while calls go down; factorial(1) returns 1, then each frame multiplies and returns: 2, 6, 24](figures/call-stack.svg)

```python
def factorial(n, depth=0):
    pad = "  " * depth
    print(f"{pad}factorial({n}) called")
    if n <= 1:
        print(f"{pad}base case -> 1")
        return 1
    result = n * factorial(n - 1, depth + 1)
    print(f"{pad}factorial({n}) returns {result}")
    return result

factorial(4)
```

### The leap of faith

When writing a recursive function, **don't** trace every level in your head. Instead:

1. Handle the base case.
2. **Assume** the function already works for any smaller input (that's the "leap of faith").
3. Use that smaller answer to build the answer for the current input.

For "sum of a list": assume `total(rest)` is correct; then `total(nums) = nums[0] + total(nums[1:])`. That's the whole function.

```python
def total(nums):
    if not nums:                     # base case: an empty list sums to 0
        return 0
    return nums[0] + total(nums[1:]) # trust that total() works on the rest

def reverse(s):
    if len(s) <= 1:
        return s
    return reverse(s[1:]) + s[0]

def is_palindrome(s):
    if len(s) <= 1:
        return True
    return s[0] == s[-1] and is_palindrome(s[1:-1])

print(total([3, 1, 4, 1, 5]), reverse("stack"), is_palindrome("racecar"))
```

(These slice-based versions copy the list or string at every level, so they're O(n²) overall; passing an index instead of slicing makes them O(n). Here they show the idea.)

### Where recursion shines: nested structures

Recursion is the natural fit for data that contains smaller copies of itself: folders inside folders, nested lists, JSON, trees and graphs (Parts 7 and 8).

```python
def count_files(folder):
    """folder: a dict whose values are either a file size (int) or another folder (dict)."""
    count = 0
    for name, item in folder.items():
        if isinstance(item, dict):
            count += count_files(item)     # a subfolder: same problem, smaller
        else:
            count += 1
    return count

drive = {"cv.pdf": 120, "photos": {"a.jpg": 900, "b.jpg": 850, "2025": {"c.jpg": 700}}, "notes.txt": 4}
print(count_files(drive))
```

### Measuring cost with a recursion tree

Draw each call as a node and its recursive calls as children. Then:

- **time** = (number of calls) × (work per call, not counting the recursive calls);
- **space** = the **depth** of the tree (the longest chain of calls waiting on the stack), plus any data each frame keeps.

Factorial makes one call per level: n calls, O(n) time, O(n) stack space. Now look at naive Fibonacci, where each call makes **two**:

```python
calls = 0

def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

for n in [10, 20, 25]:
    calls = 0
    print(f"fib({n}) = {fib(n):>6}   calls: {calls:,}")
```

![The recursion tree of fib(5): fib(5) calls fib(4) and fib(3); fib(4) calls fib(3) and fib(2); and so on down to fib(1) and fib(0). fib(3) appears twice and fib(2) three times: the same work is repeated](figures/fib-tree.svg)

The tree roughly doubles at each level, so the number of calls grows exponentially, about O(1.6ⁿ) (often written loosely as O(2ⁿ)). fib(40) would take over 300 million calls. The tree also shows **why**: the same subproblems (fib(3), fib(2)…) are solved again and again.

### The first fix: memoisation

Remember each answer the first time it's computed and reuse it. Now each fib(k) is computed once: O(n) time, O(n) space. This idea, **recursion + memo**, is the doorway to dynamic programming (Part 9).

```python
from functools import cache

@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(80))

def fib_memo(n, memo=None):          # the same thing by hand, with a dict
    memo = {} if memo is None else memo
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

print(fib_memo(80))
```

### Recursion or a loop?

- Python limits recursion depth to about 1,000 frames (`sys.getrecursionlimit()`), and each call is slower than a loop iteration. Python does **not** optimise tail calls, so even "tail-recursive" functions use one frame per call.
- So: when the depth could be large (a linked list of 100,000 nodes, counting down from a million), use a loop.
- Use recursion when the problem is naturally recursive and the depth stays modest: trees (depth ~ log n when balanced), nested data, divide and conquer, backtracking.
- `sys.setrecursionlimit(10_000)` raises the limit, but going too deep can crash the interpreter. Prefer rewriting with an explicit stack.

```python
import sys

print("limit:", sys.getrecursionlimit())

def depth(n):
    return 0 if n == 0 else 1 + depth(n - 1)

try:
    depth(5000)
except RecursionError as e:
    print("RecursionError:", e)

def depth_loop(n):                 # the same computation with a loop: no limit
    d = 0
    while n:
        n, d = n - 1, d + 1
    return d

print(depth_loop(5000))
```

### A classic: the Tower of Hanoi

Move n disks from peg A to peg C, one at a time, never putting a bigger disk on a smaller one. The recursive insight: to move n disks, move the top n − 1 out of the way to B, move the biggest to C, then move the n − 1 from B onto it.

```python
def hanoi(n, source, spare, target, moves):
    if n == 0:
        return
    hanoi(n - 1, source, target, spare, moves)    # clear the top n-1 onto the spare peg
    moves.append((source, target))                # move the biggest disk
    hanoi(n - 1, spare, source, target, moves)    # put the n-1 back on top of it

moves = []
hanoi(3, "A", "B", "C", moves)
print(len(moves), "moves:", moves)
```

The number of moves is 2ⁿ − 1: T(n) = 2·T(n − 1) + 1. Each extra disk doubles the work.

:::exercise Flatten a nested list
Write `flatten(items)` that takes a list which may contain numbers and other lists (nested to any depth) and returns one flat list of all the numbers, in order.
```python starter
def flatten(items):
    pass

print(flatten([1, [2, [3, 4]], 5]))   # [1, 2, 3, 4, 5]
```
```python check
test("flatten", [
    (([1, [2, [3, 4]], 5],), [1, 2, 3, 4, 5], "the example"),
    (([],), [], "an empty list"),
    (([1, 2, 3],), [1, 2, 3], "already flat"),
    (([[[[7]]]],), [7], "deeply nested"),
    (([[], [1, []], [[2], 3]],), [1, 2, 3], "empty lists inside"),
    (([[1, 2], [3, [4, [5, [6]]]]],), [1, 2, 3, 4, 5, 6], "mixed depths"),
])
```
```python solution
def flatten(items):
    flat = []
    for item in items:
        if isinstance(item, list):
            flat.extend(flatten(item))   # a smaller copy of the same problem
        else:
            flat.append(item)            # base case: a plain number
    return flat

print(flatten([1, [2, [3, 4]], 5]))
```
hint: Each item is either a number or a list. What should you do with a list item?
hint: A list item is the same problem, only smaller: flatten it with a recursive call and add all of its results.
hint: Loop over `items`; if `isinstance(item, list)`, `flat.extend(flatten(item))`; otherwise `flat.append(item)`. Return `flat`.
approach:
1. **Understand:** any nesting depth; keep the left-to-right order; empty lists contribute nothing.
2. **Examples:** [1, [2, [3, 4]], 5] → [1, 2, 3, 4, 5]; [[], [1, []]] → [1].
3. **Brute force:** loops can only handle a fixed depth: you'd need one loop per level.
4. **Pattern:** a structure that contains smaller copies of itself → **recursion**.
5. **Plan:** for each item: a list → flatten it recursively and extend; a number → append.
6. **Code and test:** empty lists inside, deep nesting, already flat.
walkthrough:
**Line by line**

- The loop visits the items left to right, so the order is kept.
- `isinstance(item, list)` decides which case we're in.
- For a list, the leap of faith: `flatten(item)` returns that sub-list's numbers, already flat; `extend` adds them all.
- A number is the base case: it's added as it is.
- An empty list simply loops zero times and returns `[]`.

**Trace** on `[1, [2, [3]]]`:

| call | item | action | returns |
|---|---|---|---|
| flatten([1, [2, [3]]]) | 1 | append | |
| | [2, [3]] | recurse ↓ | |
| flatten([2, [3]]) | 2 | append | |
| | [3] | recurse ↓ | |
| flatten([3]) | 3 | append | [3] |
| back in flatten([2, [3]]) | | extend with [3] | [2, 3] |
| back at the top | | extend with [2, 3] | [1, 2, 3] |

**Complexity:** O(n + d) time where n is the number of values and d the number of lists, O(depth) stack space (plus the output list).

**Common wrong approach:** `flat.append(flatten(item))` adds the flattened list as one item, giving `[1, [2, 3]]`.
:::

:::exercise Tower of Hanoi
Write `hanoi_moves(n)` returning the list of moves, as `(from_peg, to_peg)` pairs using pegs `"A"`, `"B"`, `"C"`, that move `n` disks from `"A"` to `"C"` following the rules. For `n = 0` return `[]`.
```python starter
def hanoi_moves(n):
    pass

print(hanoi_moves(2))   # [('A', 'B'), ('A', 'C'), ('B', 'C')]
```
```python check
fn = need("hanoi_moves")
def _valid_game(moves, n):
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    for m in moves:
        if not (isinstance(m, tuple) and len(m) == 2 and m[0] in pegs and m[1] in pegs):
            raise AssertionError(f"Each move must be a pair like ('A', 'C'); got {m!r}.")
        src, dst = m
        if not pegs[src]:
            raise AssertionError(f"Move {m}: peg {src} is empty.")
        disk = pegs[src][-1]
        if pegs[dst] and pegs[dst][-1] < disk:
            raise AssertionError(f"Move {m}: disk {disk} can't go on top of the smaller disk {pegs[dst][-1]}.")
        pegs[dst].append(pegs[src].pop())
    return pegs["C"] == list(range(n, 0, -1))
for n in range(0, 9):
    got = fn(n)
    if got is None:
        raise AssertionError("hanoi_moves returned None. Did you forget to return the list of moves?")
    if len(got) != 2 ** n - 1:
        raise AssertionError(f"For n = {n}, the shortest solution has {2 ** n - 1} moves, but yours has {len(got)}.")
    if not _valid_game(list(got), n):
        raise AssertionError(f"For n = {n}, the moves don't end with all disks on peg C.")
```
```python solution
def hanoi_moves(n):
    moves = []

    def move(k, source, spare, target):
        if k == 0:
            return                              # base case: nothing to move
        move(k - 1, source, target, spare)      # top k-1 disks out of the way
        moves.append((source, target))          # the biggest of the k disks
        move(k - 1, spare, source, target)      # the k-1 disks back on top

    move(n, "A", "B", "C")
    return moves

print(hanoi_moves(2))
```
hint: To move the **biggest** disk from A to C, where must the other n − 1 disks be?
hint: They must all be on B. So: move n − 1 disks A → B (using C as the spare), move the biggest A → C, then move n − 1 disks B → C (using A as the spare).
hint: Write a helper `move(k, source, spare, target)` that appends to a shared `moves` list; the base case `k == 0` does nothing. Call `move(n, "A", "B", "C")`.
approach:
1. **Understand:** one disk at a time; never a larger disk on a smaller one; the shortest sequence (2ⁿ − 1 moves).
2. **Examples:** n = 1 → [A→C]; n = 2 → [A→B, A→C, B→C].
3. **Brute force:** searching all sequences of moves is hopeless: the number of possible sequences explodes.
4. **Pattern:** a problem defined in terms of a smaller copy → **recursion** with a leap of faith.
5. **Plan:** move(k, src, spare, dst): move k − 1 src → spare; record src → dst; move k − 1 spare → dst.
6. **Code and test:** n = 0, 1, 2; check the count 2ⁿ − 1.
walkthrough:
**Line by line**

- `moves` lives in the outer function; the inner helper appends to it, so every call shares the same list.
- The helper's parameters say **which peg plays which role** at this level. Swapping the roles in the two recursive calls is the whole trick.
- Leap of faith: assume `move(k - 1, ...)` correctly moves k − 1 disks between any two pegs. Then moving k disks takes: k − 1 out of the way, one big move, k − 1 back.

**Trace** of `hanoi_moves(2)`:

| call | action |
|---|---|
| move(2, A, B, C) | first: move(1, A, C, B) |
| move(1, A, C, B) | move(0) does nothing; record **A→B**; move(0) |
| move(2, A, B, C) | record **A→C** |
| move(2, A, B, C) | then: move(1, B, A, C) → record **B→C** |

**Complexity:** O(2ⁿ) time (there are 2ⁿ − 1 moves to output), O(n) stack space.

**Common wrong approach:** keeping the same peg roles in both recursive calls, which tries to put the small disks where the big disk needs to go.
:::

:::quiz
? What must every recursive function have to avoid running forever?
+ A base case that returns without recursing, reached by making the input smaller each call
- A global variable
- A loop
= Without a base case that every path eventually reaches, the calls never stop (RecursionError in Python).
? Naive recursive Fibonacci is slow because:
+ It solves the same smaller problems again and again, so the call tree grows exponentially
- Python can't add large numbers
- Recursion is always slower than loops by a factor of 1000
= The recursion tree repeats fib(3), fib(2)... Memoisation removes the repeats.
? What decides the stack space of a recursive function?
+ The maximum depth of calls waiting at once
- The total number of calls
- The size of the output
= Only one path of the tree is on the stack at a time.
? Why prefer a loop over recursion for walking a 100,000-node linked list in Python?
+ The recursion would need 100,000 frames, far past Python's limit of about 1,000
- Loops give different answers
- Recursion can't use linked lists
= Python has no tail-call optimisation, so deep recursion overflows the call stack.
:::
EOF
echo ok
@@@ lesson
id: divide-and-conquer
title: Divide and conquer
minutes: 22
summary: Split a problem into halves, solve them recursively and combine: fast exponentiation, merge sort, counting inversions, maximum subarray, and the master theorem for working out the cost.
---
**Divide and conquer** is recursion with a particular shape:

1. **Divide** the problem into smaller subproblems, usually halves.
2. **Conquer** each subproblem recursively (tiny ones are base cases).
3. **Combine** the sub-answers into the answer.

Binary search (divide, then keep only one half), merge sort (sort both halves, merge them) and quicksort are all divide and conquer. The payoff is usually turning O(n) into O(log n), or O(n²) into O(n log n).

![Merge sort as divide and conquer on [38, 27, 43, 3, 9, 82, 10]: the top half of the picture splits the list in halves down to single items (divide); the bottom half merges sorted pairs back up into [3, 9, 10, 27, 38, 43, 82] (combine)](figures/divide-conquer.svg)

### Fast exponentiation: O(log n) instead of O(n)

Computing xⁿ by multiplying n times is O(n). But xⁿ = (x^(n/2))² when n is even, and x · x^(n−1) when n is odd. Halving the exponent at every step needs only about log₂ n steps: 2^1,000,000 takes 20 squarings, not a million multiplications.

```python
def power(x, n):
    if n == 0:
        return 1
    half = power(x, n // 2)          # solve the half-sized problem ONCE
    if n % 2 == 0:
        return half * half
    return half * half * x

print(power(3, 13), 3 ** 13)
```

The same idea with a loop, reading the exponent's binary digits, and with a **modulus** to keep numbers small (as in cryptography and "answer modulo 10⁹ + 7" interview questions):

```python
def power_mod(x, n, mod):
    result = 1
    x %= mod
    while n > 0:
        if n & 1:                    # this binary digit of n is 1
            result = result * x % mod
        x = x * x % mod              # x, x², x⁴, x⁸, ...
        n >>= 1                      # next binary digit
    return result

print(power_mod(2, 10**18, 10**9 + 7), pow(2, 10**18, 10**9 + 7))   # Python's built-in pow does the same
```

Note `half` is computed once and squared. Writing `power(x, n // 2) * power(x, n // 2)` makes **two** recursive calls and loses all the benefit: it's back to O(n).

### Merge sort: the classic

Split in half, sort each half recursively, merge the two sorted halves in linear time (Lesson 7's merge).

```python
def merge_sort(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left, right = merge_sort(nums[:mid]), merge_sort(nums[mid:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    return merged + left[i:] + right[j:]

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
```

There are log₂ n levels of splitting, and each level does O(n) work merging, so merge sort is **O(n log n)** time and O(n) extra space. Lesson 27 compares it with quicksort and heapsort.

### Counting inversions: piggy-backing on merge sort

An **inversion** is a pair i < j with nums[i] > nums[j]: how "unsorted" a list is (used to compare rankings, like two people's top-10 lists). Checking every pair is O(n²). During merge sort's merge, whenever an item from the **right** half is placed before items still waiting in the left half, it forms an inversion with **each** of them: count them all at once.

```python
def sort_and_count(nums):
    if len(nums) <= 1:
        return nums, 0
    mid = len(nums) // 2
    left, a = sort_and_count(nums[:mid])
    right, b = sort_and_count(nums[mid:])
    merged, i, j, count = [], 0, 0, a + b
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
            count += len(left) - i       # right[j] jumps ahead of every remaining left item
    return merged + left[i:] + right[j:], count

print(sort_and_count([2, 4, 1, 3, 5])[1])   # (2,1), (4,1), (4,3) -> 3
```

O(n log n) time, like merge sort.

### Maximum subarray, divide and conquer style

"The contiguous stretch with the largest sum" splits nicely: the best stretch is entirely in the left half, entirely in the right half, or **crosses the middle** (best suffix of the left + best prefix of the right). That's O(n log n). Kadane's algorithm (Lesson 42) later does it in O(n), but this version shows how a "crossing" case completes a divide-and-conquer solution.

```python
def max_subarray(nums, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo == hi:
        return nums[lo]
    mid = (lo + hi) // 2
    best_left_suffix, s = float("-inf"), 0
    for i in range(mid, lo - 1, -1):
        s += nums[i]; best_left_suffix = max(best_left_suffix, s)
    best_right_prefix, s = float("-inf"), 0
    for i in range(mid + 1, hi + 1):
        s += nums[i]; best_right_prefix = max(best_right_prefix, s)
    return max(max_subarray(nums, lo, mid), max_subarray(nums, mid + 1, hi),
               best_left_suffix + best_right_prefix)

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))   # 4 + -1 + 2 + 1 = 6
```

### The master theorem, in plain words

Many divide-and-conquer algorithms have a cost of the form T(n) = a·T(n/b) + O(n^d): **a** subproblems, each **1/b** the size, plus **O(n^d)** work to divide and combine. Compare the work at the top level with how fast the number of subproblems grows:

| Recurrence | Algorithm | Which wins | Result |
|---|---|---|---|
| T(n) = T(n/2) + O(1) | binary search | every level costs the same | **O(log n)** |
| T(n) = 2T(n/2) + O(n) | merge sort | every level costs the same | **O(n log n)** |
| T(n) = 2T(n/2) + O(1) | tree traversal, max of a list by halves | the leaves (bottom) dominate | **O(n)** |
| T(n) = T(n/2) + O(n) | quickselect (on average) | the top level dominates | **O(n)** |
| T(n) = 3T(n/2) + O(n) | Karatsuba multiplication | the leaves dominate | **O(n^1.58)** |
| T(n) = 2T(n − 1) + O(1) | Tower of Hanoi (not halving!) | — | **O(2ⁿ)** |

The rule behind the table: if a = bᵈ, every level does the same work, giving O(nᵈ log n); if a < bᵈ, the top level dominates, giving O(nᵈ); if a > bᵈ, the leaves dominate, giving O(n^(log_b a)). You rarely need the formula itself. Drawing the recursion tree and adding up the work per level gets the same answer.

### When divide and conquer fits

- The problem splits into **independent** subproblems of the same kind (unlike Fibonacci, whose subproblems overlap: that's dynamic programming's job).
- Combining sub-answers is cheaper than solving the whole problem directly.
- Bonus: independent halves can run **in parallel**, which is how big data frameworks (MapReduce, Spark) process huge datasets.

:::exercise Fast modular power
Write `fast_pow(x, n, mod)` returning xⁿ mod `mod` for integers x ≥ 0, n ≥ 0 and mod ≥ 2, using O(log n) multiplications. Don't use Python's built-in three-argument `pow` or `**` with a big exponent: the point is to write the halving yourself.
```python starter
def fast_pow(x, n, mod):
    pass

print(fast_pow(3, 13, 1000))   # 3^13 = 1594323, so 323
```
```python check
import re as _re
_code = "\n".join(ln.split("#")[0] for ln in __source__.splitlines())
if _re.search(r"(?<![\w.])pow\s*\(", _code) or "**" in _code:
    raise AssertionError("Write the halving yourself, without pow() or **.")
test("fast_pow", [
    ((3, 13, 1000), 323, "the example"),
    ((2, 10, 1000), 24, "2^10 = 1024"),
    ((5, 0, 7), 1, "any number to the power 0 is 1"),
    ((0, 5, 7), 0, "zero to a positive power"),
    ((7, 1, 13), 7, "power 1"),
    ((10, 3, 7), 6, "x bigger than the modulus"),
    ((2, 61, 10**9 + 7), 2**61 % (10**9 + 7), "a 61-bit power"),
    ((123456789, 98765, 10**9 + 7), 123456789**98765 % (10**9 + 7), "a large exponent"),
])
def _ref(x, n, m):
    r, x = 1, x % m
    while n:
        if n & 1: r = r * x % m
        x = x * x % m; n >>= 1
    return r
speed("fast_pow", lambda n: (3, n, 10**9 + 7), _ref, sizes=(1_000, 5_000_000, 10**15), what="as the exponent",
      tip="Multiplying n times is O(n). Use x^n = (x^(n/2))^2: square the half-power instead of recomputing it.")
```
```python solution
def fast_pow(x, n, mod):
    result = 1
    x %= mod
    while n > 0:
        if n % 2 == 1:          # odd exponent: take one x into the result
            result = result * x % mod
        x = x * x % mod         # square the base
        n //= 2                 # halve the exponent
    return result

print(fast_pow(3, 13, 1000))
```
```python slow
def fast_pow(x, n, mod):
    result = 1
    for _ in range(n):
        result = result * x % mod
    return result
```
hint: If you already know x^(n/2), how do you get xⁿ in one more multiplication?
hint: Square it: xⁿ = (x^(n/2))² when n is even; when n is odd, multiply in one extra x. Each step halves n.
hint: Loop: `if n % 2: result = result * x % mod`; then `x = x * x % mod; n //= 2`. Take `% mod` after **every** multiplication to keep numbers small.
approach:
1. **Understand:** huge exponents (up to 10¹⁵ in the speed test), answer modulo `mod`, n = 0 gives 1.
2. **Examples:** 3¹³ mod 1000 = 323; 2¹⁰ mod 1000 = 24; 5⁰ = 1.
3. **Brute force:** multiply n times: O(n), impossible for n = 10¹⁵.
4. **Pattern:** **divide and conquer**: halve the exponent (binary exponentiation).
5. **Plan:** result = 1; while n: if n is odd, result *= x; x = x²; n //= 2 (all mod `mod`).
6. **Code and test:** n = 0, n = 1, x larger than mod.
walkthrough:
**Line by line**

- Write n in binary: 13 = 1101₂ = 8 + 4 + 1, so x¹³ = x⁸ · x⁴ · x¹.
- `x` takes the values x, x², x⁴, x⁸… by squaring each round.
- When the current binary digit of n is 1 (`n % 2 == 1`), that power of x is part of the answer, so multiply it into `result`.
- `n //= 2` moves to the next binary digit. The loop runs once per binary digit: about log₂ n times.
- `% mod` after each multiplication keeps every number below mod², so the arithmetic stays fast.

**Trace** of 3¹³ mod 1000:

| n (binary) | odd? | result | x after squaring |
|---|---|---|---|
| 13 (1101) | yes | 3 | 9 |
| 6 (110) | no | 3 | 81 |
| 3 (11) | yes | 243 | 6561 % 1000 = 561 |
| 1 (1) | yes | 243 × 561 % 1000 = 323 | … |

**Complexity:** O(log n) time, O(1) space.

**Common wrong approach:** recursing as `fast_pow(x, n // 2, mod) * fast_pow(x, n // 2, mod)`: two half-sized calls per level add up to n calls, so it's O(n) again.
:::

:::exercise Count inversions
Write `count_inversions(nums)` returning the number of pairs `i < j` with `nums[i] > nums[j]`. Must handle 100,000 numbers.
```python starter
def count_inversions(nums):
    pass

print(count_inversions([2, 4, 1, 3, 5]))   # 3
```
```python check
test("count_inversions", [
    (([2, 4, 1, 3, 5],), 3, "the example"),
    (([1, 2, 3, 4],), 0, "already sorted"),
    (([4, 3, 2, 1],), 6, "reversed: every pair"),
    (([],), 0, "empty"),
    (([7],), 0, "one number"),
    (([2, 2, 1],), 2, "equal numbers aren't an inversion with each other"),
    (([3, 1, 2, 3, 1],), 5, "repeats"),
])
def _ref(nums):
    def go(a):
        if len(a) <= 1: return a, 0
        m = len(a) // 2
        l, x = go(a[:m]); r, y = go(a[m:])
        out, i, j, c = [], 0, 0, x + y
        while i < len(l) and j < len(r):
            if l[i] <= r[j]: out.append(l[i]); i += 1
            else: out.append(r[j]); j += 1; c += len(l) - i
        return out + l[i:] + r[j:], c
    return go(list(nums))[1]
speed("count_inversions", lambda n: [(i * 7919) % 100003 for i in range(n)], _ref, sizes=(1_000, 4_000, 100_000), what="numbers",
      tip="Checking every pair is O(n²). Count during merge sort: when an item from the right half is placed first, it's smaller than every item left in the left half.")
```
```python solution
def count_inversions(nums):
    def sort_count(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort_count(a[:mid])
        right, y = sort_count(a[mid:])
        merged, i, j, count = [], 0, 0, x + y
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
                count += len(left) - i     # right[j] is smaller than all remaining left items
        return merged + left[i:] + right[j:], count

    return sort_count(list(nums))[1]

print(count_inversions([2, 4, 1, 3, 5]))
```
```python slow
def count_inversions(nums):
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                count += 1
    return count
```
hint: Split the list in half. Inversions are either inside the left half, inside the right half, or across the halves. The first two are smaller copies of the problem.
hint: If both halves are **sorted**, cross inversions are easy to count while merging them.
hint: Merge as in merge sort; when you take `right[j]` before `left[i]`, it's smaller than **all** of `left[i:]`, so add `len(left) - i`. Return (sorted list, count) from the recursive helper.
approach:
1. **Understand:** count pairs out of order; equal values don't count; up to 100,000 numbers.
2. **Examples:** [2, 4, 1, 3, 5] → 3: (2,1), (4,1), (4,3). [4, 3, 2, 1] → 6.
3. **Brute force:** every pair: O(n²), about 5 billion checks for 100,000 numbers.
4. **Pattern:** **divide and conquer** riding on **merge sort**.
5. **Plan:** helper returns (sorted, count); count = left count + right count + cross count found during the merge.
6. **Code and test:** sorted, reversed, duplicates (use `<=` so equal values aren't counted).
walkthrough:
**Line by line**

- `sort_count` returns two things: the sorted list (needed for the merge above it) and the number of inversions inside it.
- Inversions within each half are counted by the recursive calls (`x` and `y`).
- During the merge, both halves are sorted. Taking `right[j]` while `left[i:]` is still waiting means every one of those waiting items is bigger than `right[j]` and sits before it in the original list: `len(left) - i` inversions at once.
- `left[i] <= right[j]` takes the left item on ties, so equal values are never counted.

**Trace** of the top-level merge for [2, 4, 1, 3, 5], with halves [2, 4] (sorted, 0 inside) and [1, 3, 5] (sorted, 0 inside):

| left waiting | right[j] | take | count added |
|---|---|---|---|
| 2, 4 | 1 | 1 (right) | 2 (beats 2 and 4) |
| 2, 4 | 3 | 2 (left) | 0 |
| 4 | 3 | 3 (right) | 1 (beats 4) |
| 4 | 5 | 4 (left) | 0 |

Total: 3.

**Complexity:** O(n log n) time, O(n) space.

**Common wrong approach:** adding just 1 when a right item is taken, which misses the inversions with the other items still waiting in the left half.
:::

:::quiz
? What are the three steps of divide and conquer?
+ Divide into smaller subproblems, solve them recursively, combine their answers
- Sort, search, return
- Guess, check, repeat
= Binary search, merge sort and fast power all follow this shape.
? Why does fast exponentiation compute the half-power only once?
+ Calling it twice would double the work at every level, bringing it back to O(n)
- Python caches it automatically
- To avoid integer overflow
= One call per level gives log n levels of O(1) work.
? Merge sort's recurrence is T(n) = 2T(n/2) + O(n). Its cost is:
+ O(n log n)
- O(n)
- O(n²)
= log n levels, each doing O(n) merging work.
? Which problem is NOT a good fit for plain divide and conquer?
+ Fibonacci, because its subproblems overlap and get recomputed
- Sorting a list
- Searching a sorted list
= Overlapping subproblems call for memoisation or dynamic programming instead.
:::

@@@ lesson
id: backtracking
title: "Backtracking: subsets, permutations, N-Queens"
minutes: 24
summary: Build answers one choice at a time and undo choices that lead nowhere. The choose-explore-unchoose template for subsets, permutations, combinations, combination sums, N-Queens, Sudoku and word search, with pruning.
---
Some questions ask for **every** solution, or for **any** arrangement satisfying rules: all subsets, all orderings, a valid Sudoku, a way to place queens. **Backtracking** builds a candidate one choice at a time; as soon as a partial candidate can't possibly work, it **undoes** the last choice and tries the next option. It's depth-first search over a tree of decisions.

![The decision tree for the subsets of [1, 2, 3]. At each level we decide whether to include one number: include 1 or not, then 2, then 3. The eight leaves are the eight subsets, from [1, 2, 3] down to []. Backtracking walks this tree depth first](figures/backtracking-tree.svg)

### The template: choose, explore, unchoose

```py-static
def backtrack(path, choices):
    if is_complete(path):
        record(path)
        return
    for choice in choices:
        if not valid(path, choice):   # pruning: skip choices that can't lead anywhere
            continue
        path.append(choice)           # choose
        backtrack(path, ...)          # explore
        path.pop()                    # unchoose: undo, so the next choice starts clean
```

The `path.pop()` is what makes it **back**tracking: one shared list is reused for every candidate instead of copying it at each step. Record a **copy** (`path[:]`) when you save a solution, or later pops will empty it.

### Subsets: include or skip each item

```python
def subsets(nums):
    result, path = [], []

    def go(i):
        if i == len(nums):
            result.append(path[:])       # a copy!
            return
        path.append(nums[i])             # choose: include nums[i]
        go(i + 1)
        path.pop()                       # unchoose
        go(i + 1)                        # skip nums[i]

    go(0)
    return result

print(subsets([1, 2, 3]))
```

n items give 2ⁿ subsets, each up to n long: **O(n · 2ⁿ)** time. No algorithm can be faster than the size of its output.

### Permutations: every ordering

At each position, try every number not used yet.

```python
def permutations(nums):
    result, path, used = [], [], [False] * len(nums)

    def go():
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True; path.append(x)       # choose
            go()                                 # explore
            used[i] = False; path.pop()          # unchoose

    go()
    return result

print(permutations([1, 2, 3]))
```

n! orderings, each n long: **O(n · n!)**. 10 items already give 3.6 million permutations.

### Combinations: choose k of n

Only move **forward** (start the loop after the last chosen index), so [1, 2] and [2, 1] aren't both produced. Pruning: stop early if there aren't enough numbers left to reach k.

```python
def combinations(n, k):
    result, path = [], []

    def go(start):
        if len(path) == k:
            result.append(path[:])
            return
        for x in range(start, n - (k - len(path)) + 2):   # prune: leave room for the rest
            path.append(x)
            go(x + 1)
            path.pop()

    go(1)
    return result

print(combinations(4, 2))
```

There are C(n, k) = n! / (k!(n − k)!) combinations.

### Python's shortcuts

For plain generation, `itertools` does it in C, and much faster. Write backtracking yourself when you need **pruning** or custom rules, which is what interviews test.

```python
from itertools import permutations, combinations, product

print(list(combinations([1, 2, 3, 4], 2)))
print(len(list(permutations(range(5)))))          # 5! = 120
print(list(product("AB", repeat=2)))              # every 2-letter string from A and B
```

### N-Queens: pruning with sets

Place n queens on an n × n board so that no two attack each other (same row, column or diagonal). Place one queen per row; for each row, try every column that isn't attacked. Squares on the same diagonal share `row - col`; on the same anti-diagonal they share `row + col`. Three sets make each check O(1).

![A 4 × 4 board with a solution: queens in row 0 column 1, row 1 column 3, row 2 column 0, row 3 column 2. Squares attacked by the first queen are shaded along its column and both diagonals](figures/n-queens.svg)

```python
def solve_queens(n):
    cols, diag, anti = set(), set(), set()
    board, solutions = [], []

    def place(row):
        if row == n:
            solutions.append(board[:])
            return
        for c in range(n):
            if c in cols or (row - c) in diag or (row + c) in anti:
                continue                                  # attacked: prune this branch
            cols.add(c); diag.add(row - c); anti.add(row + c); board.append(c)
            place(row + 1)
            cols.remove(c); diag.remove(row - c); anti.remove(row + c); board.pop()

    place(0)
    return solutions

sols = solve_queens(4)
print(len(sols), "solutions for n = 4:", sols)
for c in sols[0]:
    print(" ".join("Q" if i == c else "." for i in range(4)))
print("n = 8:", len(solve_queens(8)), "solutions")
```

Without pruning there would be 8⁸ ≈ 16.7 million ways to put one queen in each row of an 8 × 8 board; pruning visits only a few thousand partial boards.

### Sudoku: fill a cell, check, undo

```python
def solve_sudoku(grid):
    """grid: 9 lists of 9 ints, 0 for empty. Fills it in place; returns True if solved."""
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                for d in range(1, 10):
                    if ok(grid, r, c, d):
                        grid[r][c] = d           # choose
                        if solve_sudoku(grid):   # explore
                            return True
                        grid[r][c] = 0           # unchoose
                return False                     # no digit fits: backtrack
    return True                                  # no empty cells left

def ok(grid, r, c, d):
    if d in grid[r] or any(grid[i][c] == d for i in range(9)):
        return False
    br, bc = 3 * (r // 3), 3 * (c // 3)
    return all(grid[br + i][bc + j] != d for i in range(3) for j in range(3))

puzzle = [[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]]
print(solve_sudoku(puzzle))
for row in puzzle[:3]:
    print(row)
```

### Word search in a grid

Does a word appear as a path of neighbouring cells (no cell used twice)? Start from every cell, extend letter by letter, and mark cells as used while they're on the current path.

```python
def exists(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False
        saved, board[r][c] = board[r][c], "#"          # choose: mark as used
        found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = saved                            # unchoose: unmark
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))

grid = [list("ABCE"), list("SFCS"), list("ADEE")]
print(exists(grid, "ABCCED"), exists(grid, "SEE"), exists(grid, "ABCB"))
```

Worst case O(r · c · 4ᴸ) for a word of length L, but the letter check prunes almost every branch immediately.

### Recognising a backtracking problem

Clue words: "all possible", "every combination", "generate", "find any arrangement", "place", "partition into", "n ≤ 15 or so". Small limits are a hint: exponential algorithms are only acceptable when n is small.

:::exercise All subsets
Write `all_subsets(nums)` returning a list of every subset of `nums` (a list of distinct integers), each subset as a list. The order of the subsets, and of the numbers inside each, doesn't matter.
```python starter
def all_subsets(nums):
    pass

print(all_subsets([1, 2, 3]))
```
```python check
def _norm(result):
    return sorted(tuple(sorted(s)) for s in result)
test("all_subsets", [
    (([1, 2, 3],), [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]], "the example"),
    (([],), [[]], "the empty list has one subset: itself"),
    (([7],), [[], [7]], "one number"),
    (([4, 1],), [[], [1], [4], [1, 4]], "two numbers"),
    ((list(range(10)),), [[x for x in range(10) if m >> x & 1] for m in range(1 << 10)], "ten numbers (1,024 subsets)"),
], key=_norm)
```
```python solution
def all_subsets(nums):
    result, path = [], []

    def go(i):
        if i == len(nums):
            result.append(path[:])      # record a copy of the current subset
            return
        path.append(nums[i])            # include nums[i]
        go(i + 1)
        path.pop()                      # undo
        go(i + 1)                       # exclude nums[i]

    go(0)
    return result

print(all_subsets([1, 2, 3]))
```
hint: For each number there are exactly two choices. What are they?
hint: Include it or leave it out. Make the two choices recursively for index i, then move on to index i + 1; at the end of the list you have one complete subset.
hint: `go(i)`: if `i == len(nums)`, append `path[:]`. Otherwise `path.append(nums[i]); go(i + 1); path.pop(); go(i + 1)`.
approach:
1. **Understand:** distinct numbers; 2ⁿ subsets including [] and the whole list; any order.
2. **Examples:** [1, 2] → [], [1], [2], [1, 2].
3. **Brute force:** count from 0 to 2ⁿ − 1 and use the binary digits as include/exclude flags: also valid, O(n · 2ⁿ).
4. **Pattern:** "all possible" → **backtracking** over include/exclude decisions.
5. **Plan:** recursive go(i) with a shared path; base case records a copy; two branches per number.
6. **Code and test:** the empty list must give [[]].
walkthrough:
**Line by line**

- `path` is the subset being built; `result` collects finished subsets.
- At `i == len(nums)` every number has been decided, so `path` is one complete subset. `path[:]` stores a **copy**: storing `path` itself would store the same list object 8 times, which is empty by the end.
- The include branch appends, recurses, then pops, so `path` is back to how it was before the exclude branch runs.

**Trace** for [1, 2] (the order subsets are recorded):

| decisions | path recorded |
|---|---|
| include 1, include 2 | [1, 2] |
| include 1, exclude 2 | [1] |
| exclude 1, include 2 | [2] |
| exclude 1, exclude 2 | [] |

**Complexity:** O(n · 2ⁿ) time (2ⁿ subsets, copying each costs up to n), O(n) recursion depth plus the output.

**Common wrong approach:** `result.append(path)` without copying: every entry is the same list, and the final answer is a list of empty lists.
:::

:::exercise All permutations
Write `all_permutations(nums)` returning every ordering of `nums` (distinct integers) as a list of lists, in any order.
```python starter
def all_permutations(nums):
    pass

print(all_permutations([1, 2, 3]))
```
```python check
from itertools import permutations as _p
import re as _re
_code = "\n".join(ln.split("#")[0] for ln in __source__.splitlines())
if "itertools" in _code or _re.search(r"(?<![\w])permutations\s*\(", _code):
    raise AssertionError("Write the backtracking yourself, without itertools.permutations.")
test("all_permutations", [
    (([1, 2, 3],), [list(t) for t in _p([1, 2, 3])], "the example"),
    (([],), [[]], "an empty list has one ordering"),
    (([5],), [[5]], "one number"),
    (([0, 1],), [[0, 1], [1, 0]], "two numbers"),
    ((list(range(6)),), [list(t) for t in _p(range(6))], "six numbers (720 orderings)"),
], key=lambda r: sorted(map(tuple, r)))
```
```python solution
def all_permutations(nums):
    result, path = [], []
    used = [False] * len(nums)

    def go():
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])     # choose nums[i] for this position
            go()                     # fill the remaining positions
            path.pop()               # unchoose
            used[i] = False

    go()
    return result

print(all_permutations([1, 2, 3]))
```
hint: Fill the positions one at a time. For the current position, which numbers can you put there?
hint: Any number not already used. Track used numbers with a list of booleans (or a set), and undo the mark after exploring.
hint: `go()`: if the path is full, record a copy. Else for each unused i: mark, append, `go()`, pop, unmark.
approach:
1. **Understand:** distinct numbers; n! orderings; an empty list has exactly one (empty) ordering.
2. **Examples:** [1, 2] → [1, 2], [2, 1].
3. **Brute force:** generate all n-length sequences and keep those without repeats: nⁿ candidates, far too many.
4. **Pattern:** **backtracking** with a "used" marker.
5. **Plan:** shared path + used flags; at each level try every unused number; choose, recurse, unchoose.
6. **Code and test:** [], one number, check the count is n!.
walkthrough:
**Line by line**

- `used[i]` says whether `nums[i]` is already in `path`, an O(1) check (searching `path` would be O(n)).
- Each level of recursion fills one position, trying every unused number in turn.
- After the recursive call returns, undoing **both** `path.append` and `used[i] = True` restores the state for the next choice in the loop.
- When the path is as long as `nums`, it's a full ordering: record a copy.

**Trace** of the first branches for [1, 2, 3]:

| path | next choice | result so far |
|---|---|---|
| [] | 1 | |
| [1] | 2 → [1, 2] → 3 | [1, 2, 3] |
| [1] | 3 → [1, 3] → 2 | [1, 3, 2] |
| [] | 2 | … [2, 1, 3], [2, 3, 1] … |

**Complexity:** O(n · n!) time, O(n) extra space plus the output.

**Common wrong approach:** forgetting `used[i] = False` after the call, so each number can be used only once in the whole search and most orderings are missed.
:::

:::exercise N-Queens: count the solutions
Write `count_queens(n)` returning how many ways there are to place `n` non-attacking queens on an n × n board. It must handle n up to 9 in about a second, so prune attacked squares instead of trying every board.
```python starter
def count_queens(n):
    pass

print(count_queens(4))   # 2
```
```python check
test("count_queens", [
    (1, 1, "n = 1"),
    (2, 0, "n = 2 has no solution"),
    (3, 0, "n = 3 has no solution"),
    (4, 2, "n = 4"),
    (5, 10, "n = 5"),
    (6, 4, "n = 6"),
    (8, 92, "n = 8: the classic 92"),
])
def _ref(n):
    count = 0
    def place(r, cols, d, a):
        nonlocal count
        if r == n: count += 1; return
        for c in range(n):
            if c in cols or r - c in d or r + c in a: continue
            cols.add(c); d.add(r - c); a.add(r + c)
            place(r + 1, cols, d, a)
            cols.remove(c); d.remove(r - c); a.remove(r + c)
    place(0, set(), set(), set())
    return count
speed("count_queens", lambda n: n, _ref, sizes=(6, 8, 9), what="as the board size", factor=10, floor=0.1,
      tip="Don't build every full board and check it afterwards. Place one queen per row and skip attacked columns and diagonals using sets (row - col and row + col identify the diagonals).")
```
```python solution
def count_queens(n):
    cols, diag, anti = set(), set(), set()
    count = 0

    def place(row):
        nonlocal count
        if row == n:
            count += 1                       # all rows filled: one more solution
            return
        for c in range(n):
            if c in cols or row - c in diag or row + c in anti:
                continue                     # this square is attacked
            cols.add(c); diag.add(row - c); anti.add(row + c)
            place(row + 1)
            cols.remove(c); diag.remove(row - c); anti.remove(row + c)

    place(0)
    return count

print(count_queens(4))
```
```python slow
from itertools import permutations

def count_queens(n):
    count = 0
    for cols in permutations(range(n)):      # every arrangement, then check
        if len({r - c for r, c in enumerate(cols)}) == n and len({r + c for r, c in enumerate(cols)}) == n:
            count += 1
    return count
```
hint: Each row must hold exactly one queen. So place queens row by row: what do you need to know to decide whether a column is safe?
hint: Whether that column, that diagonal (`row - col`) or that anti-diagonal (`row + col`) already has a queen. Keep three sets.
hint: `place(row)`: if `row == n`, count one solution. Else, for each column `c` not attacked: add to the three sets, `place(row + 1)`, then remove from the three sets.
approach:
1. **Understand:** count arrangements, not print them; queens attack along rows, columns and diagonals.
2. **Examples:** n = 4 → 2; n = 2 and 3 → 0; n = 8 → 92.
3. **Brute force:** try all n! column orders and check diagonals at the end: 9! = 362,880 full boards checked.
4. **Pattern:** **backtracking with pruning**, using sets for O(1) attack checks.
5. **Plan:** one queen per row; skip attacked columns early; count when every row is filled.
6. **Code and test:** n = 1, 2, 3, 4, 8.
walkthrough:
**Line by line**

- Placing exactly one queen per row means rows never clash, so only columns and diagonals need checking.
- On one diagonal (going down-right), `row - col` is the same for every square; on an anti-diagonal (down-left), `row + col` is. Three sets turn "is this square attacked?" into three O(1) lookups.
- `nonlocal count` lets the inner function update the counter.
- Removing from the sets after the call is the "unchoose" step, freeing the column and diagonals for the next column in the loop.

**Trace** of n = 4 (the first solution found):

| row | columns tried | placed at |
|---|---|---|
| 0 | 0 | 0 → later dead ends: back up |
| 0 | 1 | 1 |
| 1 | 0 attacked (diagonal), 1 (column), 2 (diagonal), 3 | 3 |
| 2 | 0 | 0 |
| 3 | 2 | 2 → solution [1, 3, 0, 2] |

**Complexity:** O(n!) in the worst case, but pruning cuts the search to a tiny fraction; O(n) space.

**Common wrong approach:** checking diagonals with `abs(row1 - row2) == abs(col1 - col2)` against every queen placed so far works, but costs O(n) per check; the sets make it O(1).
:::

:::exercise Combination sum
Write `combination_sum(candidates, target)` returning every **combination** (as a sorted list) of numbers from `candidates` (distinct positive integers) that adds up to `target`. Each number may be used **any number of times**. Combinations are unordered: return [2, 2, 3] once, not also [3, 2, 2]. The order of the combinations doesn't matter.
```python starter
def combination_sum(candidates, target):
    pass

print(combination_sum([2, 3, 6, 7], 7))   # [[2, 2, 3], [7]]
```
```python check
def _norm(r):
    return sorted(tuple(sorted(c)) for c in r)
def _brute(cands, t):
    out = []
    cands = sorted(cands)
    def go(start, left, path):
        if left == 0: out.append(path[:]); return
        for i in range(start, len(cands)):
            if cands[i] > left: break
            path.append(cands[i]); go(i, left - cands[i], path); path.pop()
    go(0, t, [])
    return out
cases = [(([2, 3, 6, 7], 7), "the example"), (([2, 3, 5], 8), "several answers"), (([2], 1), "impossible"),
         (([1], 3), "one number used three times"), (([7, 3, 2], 18), "unsorted candidates"), (([5, 10], 3), "all too big")]
test("combination_sum", [(a, _brute(*a), lab) for a, lab in cases], key=_norm)
fn = need("combination_sum")
got = fn([2, 3, 6, 7], 7)
if got is not None and len(got) != len(set(map(tuple, map(sorted, got)))):
    raise AssertionError("The same combination appears twice in different orders. Only move forward through the candidates (start the loop at the current index).")
```
```python solution
def combination_sum(candidates, target):
    candidates = sorted(candidates)
    result, path = [], []

    def go(start, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            x = candidates[i]
            if x > remaining:
                break                       # sorted: every later number is too big too
            path.append(x)
            go(i, remaining - x)            # i, not i + 1: x may be used again
            path.pop()

    go(0, target)
    return result

print(combination_sum([2, 3, 6, 7], 7))
```
hint: How do you avoid producing [2, 2, 3] and [3, 2, 2] as different answers?
hint: Only pick numbers at or after the index of the last number you picked. Reuse is allowed, so you may pick the same index again.
hint: Sort the candidates. `go(start, remaining)`: if remaining is 0, record a copy; loop i from `start`; break if `candidates[i] > remaining`; choose, `go(i, remaining - x)`, unchoose.
approach:
1. **Understand:** unlimited reuse; no duplicate combinations; return an empty list if impossible.
2. **Examples:** [2, 3, 6, 7], 7 → [2, 2, 3], [7]; [2], 1 → [].
3. **Brute force:** generate every sequence up to length target/min and keep sorted unique ones that sum to target: huge, with duplicates to remove.
4. **Pattern:** **backtracking** with a start index (combinations, not permutations) and **pruning** on sorted input.
5. **Plan:** sort; go(start, remaining); try candidates from start; stay at the same index to allow reuse; stop early when a candidate is too big.
6. **Code and test:** impossible targets, single candidates, unsorted input.
walkthrough:
**Line by line**

- Sorting lets us `break` as soon as a candidate exceeds what's left: every later candidate is bigger, so that whole branch is pruned.
- `start` makes each combination come out in non-decreasing order, which is exactly one ordering per combination: no duplicates.
- `go(i, remaining - x)` passes `i`, not `i + 1`, so the same number can be chosen again.
- `remaining == 0` means the path sums to the target: record a copy.

**Trace** for [2, 3, 6, 7], target 7:

| path | remaining | next |
|---|---|---|
| [2] | 5 | try 2 |
| [2, 2] | 3 | try 2 → [2, 2, 2] leaves 1: 2 > 1, break |
| [2, 2] | 3 | try 3 → [2, 2, 3] leaves 0: **record** |
| [2] | 5 | try 3 → [2, 3] leaves 2: 3 > 2, break |
| [3], [6] | 4, 1 | no completions |
| [7] | 0 | **record** |

**Complexity:** exponential in target / smallest candidate in the worst case; pruning keeps it small in practice. O(target / smallest) recursion depth.

**Common wrong approach:** looping from 0 every time, which produces every ordering of each combination.
:::

:::quiz
? What are the three steps inside a backtracking loop?
+ Choose, explore (recurse), unchoose (undo)
- Sort, search, return
- Divide, conquer, combine
= Undoing the choice restores the state for the next option.
? Why record path[:] instead of path?
+ path is one shared list that later pops will change; the copy freezes the current solution
- path[:] is faster to append
- Python requires slices in recursion
= Without a copy, every saved entry points to the same list.
? How many subsets does a list of 10 distinct items have?
- 10
- 100
+ 1,024
= Each item is in or out: 2^10 = 1,024.
? What makes N-Queens fast enough with backtracking?
+ Pruning: attacked squares are skipped before exploring them
- Trying every board and checking at the end
- Sorting the board
= Cutting off dead branches early avoids almost all of the n^n boards.
:::
