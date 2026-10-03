@@@ part
id: 1
title: Foundations
level: Beginner
blurb: What data structures and algorithms are, a 6-step method for any coding problem, and how to measure code with Big-O: time, space, best and worst cases, and the real cost of Python's built-ins.

@@@ lesson
id: what-is-dsa
title: What data structures and algorithms are
minutes: 12
summary: Data structures organise data; algorithms are step-by-step recipes. Why the right choice turns hours into milliseconds, and how this course checks your code.
---
A **data structure** is a way of organising data in memory so that certain jobs are fast. An **algorithm** is a precise, step-by-step recipe for solving a problem. You've already used both: a Python `list` is a data structure, and "go through the list and keep the biggest number so far" is an algorithm.

![Seven small pictures of the data structures in this course: an array of boxes in a row, a linked list of boxes joined by arrows, a stack of plates, a queue of people, a hash table with buckets, a tree branching downwards, and a graph of connected dots](figures/structures-overview.svg)

| Data structure | Picture it as | Great at | Lessons |
|---|---|---|---|
| **Array / list** | numbered boxes in a row | jumping to position *i* | 6–12 |
| **Hash table** (`dict`, `set`) | labelled drawers | "is this here?", "what's stored under this key?" | 13–14 |
| **Stack** | a pile of plates | undo, matching brackets | Part 4 |
| **Queue** | a line of people | first come, first served | Part 4 |
| **Linked list** | a chain of boxes with arrows | inserting in the middle | Part 4 |
| **Tree** | a family tree | sorted data, hierarchies | Part 7 |
| **Graph** | cities and roads | networks, routes, dependencies | Part 8 |

### Why it matters: the same question, two speeds

"Do these two lists share any item?" Here are two correct answers. The first checks every pair; the second puts one list into a `set` first:

```python
import time

a = list(range(0, 20_000, 2))      # 10,000 even numbers
b = list(range(1, 20_000, 2))      # 10,000 odd numbers: no overlap, the worst case

start = time.perf_counter()
found = any(x in b for x in a)            # 'in' on a list checks item by item
print("list:", found, f"{time.perf_counter() - start:.2f} s")

start = time.perf_counter()
b_set = set(b)
found = any(x in b_set for x in a)        # 'in' on a set jumps straight to the answer
print("set: ", found, f"{time.perf_counter() - start:.4f} s")
```

Same answer, but the set version is hundreds of times faster, and the gap grows with the data. With a million items, the list version would take hours. Choosing the right structure is most of the work. This course teaches you to see that **before** you write the slow version.

### Where you'll use DSA

- **Coding interviews.** Almost every software, data and AI engineering interview includes a problem-solving round built on exactly these topics.
- **Real work.** Deduplicating records (sets), finding the top 10 results (heaps), scheduling tasks that depend on each other (graphs), autocomplete (tries), caching (hash tables and linked lists).
- **AI engineering.** Agent workflows are graphs, retrieval ranks the top *k* results with heaps, tokenizers use tries and hashing, and dynamic programming appears in sequence alignment and beam search.

### How exercises work in this course

Exercises ask you to write a **function**. When you press **Check**, the sandbox runs it against **hidden test cases**, like coding-interview sites do, including edge cases such as empty lists. Many exercises also have a **speed check** on large inputs. If something fails, you'll see the exact input, what was expected and what your function returned.

Stuck? Every exercise has a **help ladder**: 🧭 **Approach** (how to think about it), 💡 **three hints**, each giving away a bit more, and ✅ a **walkthrough** that explains the solution line by line with a trace of it running.

Here's a function and a call, the shape of every exercise:

```python
def find_max(nums):
    best = nums[0]                # the first number is the biggest seen so far
    for n in nums[1:]:            # look at every other number once
        if n > best:
            best = n              # found a bigger one: remember it
    return best                   # return the answer (don't just print it)

print(find_max([3, 8, 2, 8, 5]))
print(find_max([-7, -3, -9]))
```

:::exercise Smallest number
Write a function `find_min(nums)` that returns the **smallest** number in a non-empty list, **without** using Python's built-in `min()`.
```python starter
def find_min(nums):
    # your code here
    pass
```
```python check
import re
if re.search(r"(?<![\w.])min\(", "\n".join(l.split("#")[0] for l in __source__.splitlines())):
    raise AssertionError("Solve it without the built-in min(): keep track of the smallest number yourself.")
test("find_min", [
    ([4, 2, 9], 2, "a short list"),
    ([7], 7, "a list with one number"),
    ([-3, -10, -1], -10, "negative numbers"),
    ([5, 5, 5], 5, "all the same"),
    ([9, 8, 7, 6, 1], 1, "the smallest at the end"),
    ([1, 8, 7, 6, 9], 1, "the smallest at the start"),
    ([2.5, 0.5, 1.5], 0.5, "decimals"),
])
```
```python solution
def find_min(nums):
    smallest = nums[0]
    for n in nums[1:]:
        if n < smallest:
            smallest = n
    return smallest
```
hint: Copy the idea of `find_max` above: keep the "smallest so far" in a variable.
hint: Start with `smallest = nums[0]`. Then loop over the rest and replace `smallest` whenever you meet a smaller number.
hint: `for n in nums[1:]: if n < smallest: smallest = n`, then `return smallest` after the loop (not inside it).
approach:
1. **Understand:** input is a non-empty list of numbers; output is one number, the smallest. No `min()`.
2. **Examples:** `[4, 2, 9]` → 2. Edge cases: one number `[7]` → 7; all negative `[-3, -10, -1]` → -10; the smallest first or last.
3. **Brute force:** for each number, check whether it's smaller than all the others. That works but compares every pair: O(n²).
4. **Pattern:** a **running best**: walk through once, remembering the best so far. Very common.
5. **Plan:** start with the first number as "smallest so far"; for each other number, if it's smaller, remember it instead; at the end, return what you remembered.
6. **Code and test:** write it, then try the edge cases in your head: does a one-item list work? (The loop over `nums[1:]` simply doesn't run.)
walkthrough:
**Line by line**

- `smallest = nums[0]`: before looking at anything else, the first number is the smallest we've seen. Don't start with `0`: for `[4, 2, 9]` the answer would wrongly be 0.
- `for n in nums[1:]:` visits every other number exactly once.
- `if n < smallest: smallest = n` keeps the running best up to date.
- `return smallest` comes **after** the loop. Returning inside the loop would stop after the first comparison.

**Trace** on `[4, 2, 9]`:

| step | n | n < smallest? | smallest |
|---|---|---|---|
| start | – | – | 4 |
| 1 | 2 | yes | 2 |
| 2 | 9 | no | 2 |
| end | | | returns **2** |

**Complexity:** O(n) time, because each number is looked at once; O(1) extra space, because we only keep one variable. (Strictly, `nums[1:]` makes a copy; `for i in range(1, len(nums))` avoids it.)

**Common wrong approach:** `smallest = 0` as the starting value. It looks fine on lists containing 0 or negatives, but returns 0 for `[4, 2, 9]`. Always start from a real element (or `float("inf")`).
:::

:::exercise Count the evens
Write `count_evens(nums)` that returns how many numbers in the list are even. An empty list has 0 evens.
```python starter
def count_evens(nums):
    pass
```
```python check
test("count_evens", [
    ([1, 2, 3, 4], 2, "a mixed list"),
    ([], 0, "an empty list"),
    ([1, 3, 5], 0, "no evens"),
    ([2, 4, 6], 3, "all evens"),
    ([0, -2, -3], 2, "zero and negatives (0 and -2 are even)"),
])
```
```python solution
def count_evens(nums):
    count = 0
    for n in nums:
        if n % 2 == 0:
            count += 1
    return count
```
hint: A number is even when `n % 2 == 0` (it divides by 2 with nothing left over).
hint: Keep a counter that starts at 0 and goes up by 1 for each even number.
hint: `count = 0`, then `for n in nums: if n % 2 == 0: count += 1`, then `return count`.
approach:
1. **Understand:** input a list (maybe empty); output a count, an integer ≥ 0.
2. **Examples:** `[1, 2, 3, 4]` → 2. Edge cases: `[]` → 0; negatives (`-2` is even); `0` is even.
3. **Brute force:** this is already simple: look at every number once.
4. **Pattern:** a **counter** updated in one pass.
5. **Plan:** counter = 0; for each number, if even, add 1; return the counter.
6. **Code and test:** check the empty list: the loop never runs and the counter stays 0. 
walkthrough:
**Line by line**

- `count = 0` handles the empty list for free: if the loop never runs, we return 0.
- `n % 2 == 0` is the even test. It works for negatives too in Python: `-3 % 2` is `1`, `-2 % 2` is `0`.
- `count += 1` adds one each time.

**Trace** on `[1, 2, 3, 4]`:

| n | even? | count |
|---|---|---|
| 1 | no | 0 |
| 2 | yes | 1 |
| 3 | no | 1 |
| 4 | yes | 2 |

**Complexity:** O(n) time, O(1) space.

**Shorter version:** `return sum(1 for n in nums if n % 2 == 0)` does the same in one line. Understand the loop first; use the one-liner once it's obvious to you.
:::

:::quiz
? What is an algorithm?
- A Python library
+ A precise, step-by-step recipe for solving a problem
- A kind of list
= Data structures organise data; algorithms are the recipes that use them.
? Why was the set version of "do two lists share an item?" so much faster?
+ Checking `x in some_set` jumps straight to the answer instead of scanning every item
- Sets use less memory
- Sets are sorted
= A list check looks at items one by one; a set uses hashing (Lesson 13).
? Your function prints the right answer but the checker says it returned None. Why?
+ It prints instead of returning; a function without return gives back None
- The checker is broken
- print is slower than return
= Tests look at what the function returns. Use `return answer`.
? Which structure fits "undo the last action" best?
- Queue
+ Stack
- Graph
= The last thing done is the first thing undone: last in, first out.
:::

@@@ lesson
id: problem-solving
title: How to approach any problem: the 6-step method
minutes: 18
summary: Understand, examples, brute force, spot the pattern, plan, code and test. A repeatable method for interviews and real work, shown on a full example.
---
Most people stare at a problem, start typing, and get lost. Strong problem solvers follow a **routine**. Use these six steps on every exercise in this course until they're automatic:

![Six steps in a row: 1 Understand, 2 Examples, 3 Brute force, 4 Spot the pattern, 5 Plan, 6 Code and test, with a loop arrow from test back to plan](figures/six-steps.svg)

| Step | Ask yourself | Why it matters |
|---|---|---|
| **1. Understand** | What goes in? What comes out? What are the limits (size, negatives, empty, duplicates)? | Half of wrong answers solve the wrong problem. |
| **2. Examples** | Work 2–3 examples by hand, including an **edge case** (empty, one item, all the same, negative). | Examples reveal the rules and become your tests. |
| **3. Brute force** | What's the simplest correct way, even if slow? What's its Big-O? | A correct slow answer beats a fast wrong one, and it's a starting point. |
| **4. Spot the pattern** | Do clue words point to a known technique? Where is the brute force wasting work? | Most problems are a known pattern in disguise (cheat sheet table). |
| **5. Plan** | Write the steps in plain words or pseudocode. Check the plan on your examples. | Fixing a plan is cheaper than fixing code. |
| **6. Code and test** | Translate the plan; run your examples and edge cases; state the time and space cost. | Testing finds mistakes before someone else does. |

In an interview, **say each step out loud**. Interviewers grade your thinking as much as your final code, and in 2026 many interviews explicitly ask you to explain trade-offs.

### A full example: "contains duplicate"

> Write `has_duplicate(nums)` that returns `True` if any value appears at least twice in the list, else `False`.

**1. Understand.** Input: a list of numbers, possibly empty, possibly huge. Output: `True` or `False`.

**2. Examples.** `[1, 2, 3, 1]` → `True`. `[1, 2, 3]` → `False`. Edge cases: `[]` → `False`; `[5]` → `False`; `[7, 7]` → `True`.

**3. Brute force.** Compare every pair:

```python
def has_duplicate_brute(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):    # every pair (i, j) once
            if nums[i] == nums[j]:
                return True
    return False

print(has_duplicate_brute([1, 2, 3, 1]), has_duplicate_brute([1, 2, 3]), has_duplicate_brute([]))
```

Correct, but two nested loops over *n* items: about n²/2 comparisons, **O(n²)**. For a million items that's 500 billion comparisons.

**4. Spot the pattern.** The waste: for each number, we search the whole rest of the list again. If we **remembered** the numbers we'd already seen in a structure with instant lookup, each check would be O(1). Clue words like "appears twice", "seen before" and "duplicate" point to a **hash set** (Lesson 14).

**5. Plan.** Make an empty set `seen`. For each number: if it's already in `seen`, return `True`; otherwise add it. If the loop finishes, return `False`.

**6. Code and test.**

```python
def has_duplicate(nums):
    seen = set()
    for n in nums:
        if n in seen:          # O(1) on average
            return True
        seen.add(n)
    return False

for test_input in ([1, 2, 3, 1], [1, 2, 3], [], [5], [7, 7]):
    print(test_input, has_duplicate(test_input))
```

**Cost:** O(n) time (one pass, O(1) per check), O(n) extra space for the set. We traded memory for speed, which is the most common trade-off in DSA.

There's a third option: sort first, then duplicates sit next to each other. That's O(n log n) time and no set, a good middle ground when memory is tight. Knowing **several** solutions and their trade-offs is exactly what interviewers look for.

### Common clue words

| If the problem says… | Think about… |
|---|---|
| "sorted array", "find a pair" | two pointers, binary search |
| "contiguous subarray / substring", "longest / shortest window" | sliding window |
| "sum of a range", "subarray sum equals k" | prefix sums (+ hash map) |
| "seen before", "duplicate", "count", "anagram" | hash map / set |
| "matching brackets", "next greater", "undo" | stack |
| "top k", "k-th largest", "closest k" | heap |
| "shortest path", "fewest steps" in a grid or network | BFS |
| "all combinations / permutations / subsets" | backtracking |
| "number of ways", "minimum cost", "can you reach" with choices | dynamic programming |

You'll meet every one of these in the course; the cheat sheet has the full table.

:::exercise Contains duplicate
Write `has_duplicate(nums)` that returns `True` if any value appears at least twice, otherwise `False`. It must handle a list of 50,000 numbers quickly.
```python starter
def has_duplicate(nums):
    pass
```
```python check
test("has_duplicate", [
    ([1, 2, 3, 1], True, "a duplicate far apart"),
    ([1, 2, 3], False, "no duplicates"),
    ([], False, "an empty list"),
    ([5], False, "one number"),
    ([7, 7], True, "two equal numbers"),
    ([-1, 0, 1, -1], True, "negative duplicates"),
])
def _ref(nums):
    return len(set(nums)) < len(nums)
speed("has_duplicate", lambda n: list(range(n)), _ref, sizes=(1_000, 5_000, 50_000), what="numbers",
      tip="Checking every pair is O(n²). Remember the numbers you've seen in a set, where `in` is O(1).")
```
```python solution
def has_duplicate(nums):
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False
```
```python slow
def has_duplicate(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False
```
hint: The slow way compares every pair. What if you remembered every number you've already passed?
hint: Use a `set` called `seen`. Checking `n in seen` takes the same short time however big the set is.
hint: For each `n`: if `n in seen`, return True; else `seen.add(n)`. After the loop, return False.
approach:
1. **Understand:** list in (maybe empty, maybe 50,000 long); `True`/`False` out.
2. **Examples:** `[1, 2, 3, 1]` → True; `[]` → False; `[7, 7]` → True.
3. **Brute force:** compare every pair with two loops: correct but O(n²), too slow for 50,000 numbers (over a billion comparisons).
4. **Pattern:** "seen before" → **hash set**. Each lookup is O(1) on average.
5. **Plan:** empty set; for each number, if it's in the set → True, else add it; end → False.
6. **Code and test:** run the examples. State the cost: O(n) time, O(n) space.
walkthrough:
**Line by line**

- `seen = set()` will hold every number we've already passed.
- `if n in seen: return True`: we've met this value before, so it's a duplicate. We can stop at once.
- `seen.add(n)` remembers the current number for later checks.
- `return False` only runs if the loop finished without finding a repeat.

**Trace** on `[1, 2, 3, 1]`:

| n | n in seen? | seen after |
|---|---|---|
| 1 | no | {1} |
| 2 | no | {1, 2} |
| 3 | no | {1, 2, 3} |
| 1 | **yes** → return True | |

**Complexity:** O(n) time, O(n) space.

**One-liner:** `return len(set(nums)) < len(nums)` (a set drops duplicates, so it's shorter if there were any). Also O(n), but it always processes the whole list, while the loop can stop early.

**Common wrong approach:** the nested loop. It passes the small tests and fails the speed check: at 50,000 numbers it needs about 1.25 billion comparisons.
:::

:::exercise Second largest
Write `second_largest(nums)` that returns the second-largest **distinct** value, or `None` if there isn't one. For `[3, 9, 9, 4]` the answer is 4 (the largest is 9; the next different value is 4). Do it in **one pass**, without sorting.
```python starter
def second_largest(nums):
    pass
```
```python check
if uses("sorted(") or uses(".sort("):
    raise AssertionError("Solve it in one pass without sorting: keep the largest and second largest as you go.")
test("second_largest", [
    ([3, 9, 9, 4], 4, "a repeated maximum"),
    ([1, 2], 1, "two numbers"),
    ([5], None, "one number (no second largest)"),
    ([], None, "an empty list"),
    ([7, 7, 7], None, "all the same"),
    ([-5, -1, -3], -3, "negative numbers"),
    ([10, 1, 9, 2], 9, "second largest after the largest"),
    ([1, 9, 10], 9, "largest at the end"),
])
```
```python solution
def second_largest(nums):
    first = second = None
    for n in nums:
        if first is None or n > first:
            second = first          # the old largest becomes the second largest
            first = n
        elif n != first and (second is None or n > second):
            second = n
    return second
```
hint: Keep **two** running values: the largest so far and the second largest so far.
hint: When a new number beats the largest, the old largest becomes the second largest. When it's only bigger than the second (and not equal to the largest), update the second.
hint: Start both as `None`. For each n: if `first is None or n > first`: `second, first = first, n`; elif `n != first and (second is None or n > second)`: `second = n`.
approach:
1. **Understand:** distinct values matter: `[9, 9]` has no second largest. Empty or one value → `None`.
2. **Examples:** `[3, 9, 9, 4]` → 4; `[5]` → None; `[7, 7, 7]` → None; `[-5, -1, -3]` → -3.
3. **Brute force:** sort the distinct values and take the second from the end: O(n log n). Fine in real code, but the exercise asks for one pass.
4. **Pattern:** a **running best**, extended to two variables. Each new number can change the first, the second, or nothing.
5. **Plan:** first = second = None. For each n: bigger than first → shift first down to second, n becomes first; else if different from first and bigger than second → n becomes second.
6. **Code and test:** check `[9, 9, 4]`: the second 9 must not become "second" (that's why we test `n != first`).
walkthrough:
**Line by line**

- `first = second = None`: `None` means "not found yet". It's safer than starting at 0, because the numbers might all be negative.
- `if first is None or n > first:` a new largest. The old largest is now the second largest, so `second = first` happens **before** `first = n`.
- `elif n != first and (second is None or n > second):` not a new largest, but a new second largest, as long as it isn't equal to the largest (distinct values only).
- `return second` is `None` when there were fewer than two distinct values.

**Trace** on `[3, 9, 9, 4]`:

| n | case | first | second |
|---|---|---|---|
| 3 | new largest | 3 | None |
| 9 | new largest | 9 | 3 |
| 9 | equal to first: skip | 9 | 3 |
| 4 | new second | 9 | 4 |

**Complexity:** O(n) time, O(1) space, versus O(n log n) for sorting.

**Common wrong approaches:** starting `first` and `second` at 0 (fails on all-negative lists), and forgetting `n != first` (then `[9, 9]` returns 9).
:::

:::quiz
? What is step 3, "brute force", for?
+ Getting a simple correct solution and its cost, as a starting point to improve
- Writing the fastest possible code first
- Skipping the examples
= A correct slow answer shows you understand the problem and where the waste is.
? Which is an edge case for a list problem?
+ An empty list
- A list of 5 normal numbers
- A sorted list of positive numbers
= Edge cases are the unusual inputs at the boundaries: empty, one item, all equal, negatives, huge.
? The words "contiguous subarray" and "longest" suggest which pattern?
- Binary search
+ Sliding window
- Backtracking
= A window that grows and shrinks over a contiguous range.
? The set solution to "contains duplicate" uses O(n) extra space. What did we get for it?
+ O(n) time instead of O(n²)
- Nothing; it's the same speed
- Sorted output
= Trading memory for speed is the most common trade-off in DSA.
:::

@@@ lesson
id: big-o
title: Big-O: how running time grows
minutes: 20
summary: Count steps, keep the fastest-growing term, drop the constants. The common complexity classes from O(1) to O(2ⁿ), and how to read the Big-O of loops.
---
Timing code with a stopwatch depends on the computer, the language and what else is running. **Big-O notation** describes something more stable: **how the number of steps grows as the input grows**. If the input doubles, does the work stay the same, double, or quadruple?

![Growth of the common complexity classes as n goes from 1 to 20: O(1) and O(log n) stay almost flat, O(n) is a straight line, O(n log n) curves up gently, O(n²) climbs steeply, and O(2ⁿ) shoots off the top of the chart almost at once](figures/big-o-growth.svg)

| Big-O | Name | Example | n = 1,000 | n = 1,000,000 |
|---|---|---|---|---|
| O(1) | constant | `d[key]`, `nums[i]` | 1 step | 1 step |
| O(log n) | logarithmic | binary search | ~10 | ~20 |
| O(n) | linear | one loop over the data | 1,000 | 1,000,000 |
| O(n log n) | linearithmic | good sorting (`sorted`) | ~10,000 | ~20,000,000 |
| O(n²) | quadratic | a loop inside a loop | 1,000,000 | 10¹² (hours) |
| O(2ⁿ) | exponential | trying every subset | more than atoms in the universe | – |

A computer does very roughly 10⁷–10⁸ simple Python steps per second. So O(n²) on a million items (10¹² steps) takes hours, while O(n log n) takes a second.

### The two rules

1. **Drop constants.** 3n + 5 steps is O(n). Big-O is about the **shape** of growth, not exact counts.
2. **Keep only the fastest-growing term.** n² + 100n + 7 is O(n²). For large n, the n² part dwarfs everything else.

### Reading the Big-O of code

```python
def total(nums):                 # O(n): the loop body runs n times
    s = 0
    for x in nums:
        s += x
    return s

def all_pairs(nums):             # O(n²): n iterations, each doing n iterations
    pairs = 0
    for a in nums:
        for b in nums:
            pairs += 1
    return pairs

def halvings(n):                 # O(log n): n is cut in half each time
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps

print(total([1, 2, 3]), all_pairs([1, 2, 3]), halvings(1_000_000))
```

- **Sequential** steps **add**: a loop over n followed by another loop over n is O(n + n) = O(n).
- **Nested** steps **multiply**: a loop over n inside a loop over m is O(n × m).
- **Halving** each time gives O(log n): 1,000,000 halves to 1 in about 20 steps. (In computing, log means log base 2.)

### Count it yourself

Watch the step counts grow as n doubles:

```python
def count_steps(n):
    linear = sum(1 for _ in range(n))
    quadratic = sum(1 for _ in range(n) for _ in range(n))
    return linear, quadratic

for n in [10, 20, 40, 80]:
    lin, quad = count_steps(n)
    print(f"n={n:>3}   O(n): {lin:>4} steps   O(n²): {quad:>5} steps")
```

When n doubles, the O(n) column doubles and the O(n²) column **quadruples**. That's how you recognise them from timings too.

### Careful: hidden loops

One line of Python can hide a loop. `x in my_list`, `my_list.index(x)`, `my_list.count(x)`, `min(nums)`, `sum(nums)`, slicing `nums[a:b]` and `sorted(nums)` all look at many items. Putting one inside a loop multiplies:

```python
def slow_unique(nums):            # looks like one loop, but 'in result' scans a list: O(n²)
    result = []
    for x in nums:
        if x not in result:
            result.append(x)
    return result

print(slow_unique([3, 1, 3, 2, 1]))
```

Lesson 5 lists the real cost of every common Python operation.

:::exercise Name the complexity
Make a dictionary `answers` mapping each function name to its Big-O, written exactly as one of `"O(1)"`, `"O(log n)"`, `"O(n)"`, `"O(n log n)"`, `"O(n²)"`. In each function, `n` is `len(nums)`.

```py-static
def first(nums):
    return nums[0]

def pairs_with_sum(nums, target):
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                count += 1
    return count

def sum_and_max(nums):
    s = 0
    for x in nums:
        s += x
    biggest = nums[0]
    for x in nums:
        biggest = max(biggest, x)
    return s, biggest

def digits(n):
    count = 0
    while n > 0:
        n //= 10
        count += 1
    return count

def sorted_median(nums):
    return sorted(nums)[len(nums) // 2]
```

For `digits`, use n as the number itself.
```python starter
answers = {
    "first": "",
    "pairs_with_sum": "",
    "sum_and_max": "",
    "digits": "",
    "sorted_median": "",
}
```
```python check
exp = {"first": "O(1)", "pairs_with_sum": "O(n²)", "sum_and_max": "O(n)", "digits": "O(log n)", "sorted_median": "O(n log n)"}
got = need("answers", dict)
for k, v in exp.items():
    g = str(got.get(k, "")).replace("^2", "²").replace(" ", "").lower()
    if g != v.replace(" ", "").lower():
        raise AssertionError(f"Check `{k}` again." + {"sum_and_max": " Two loops one after the other add up, they don't multiply.", "digits": " Each step divides n by 10: how many times can you do that?", "sorted_median": " What does sorted() cost?"}.get(k, ""))
```
```python solution
answers = {
    "first": "O(1)",            # one step, whatever the length
    "pairs_with_sum": "O(n²)",  # a loop inside a loop
    "sum_and_max": "O(n)",      # two loops one after another: n + n
    "digits": "O(log n)",       # n shrinks 10 times each step
    "sorted_median": "O(n log n)",  # dominated by sorting
}
```
hint: Look for loops. Nested loops multiply; loops one after the other add.
hint: `digits` divides n by 10 each step: a number with d digits takes d steps, and d grows like log n. `sorted()` costs O(n log n).
hint: first → O(1); pairs_with_sum → O(n²); sum_and_max → O(n); digits → O(log n); sorted_median → O(n log n).
approach:
1. **Understand:** for each function, ask "if the input doubles, how much more work?"
2. **Examples:** try n = 10 and n = 20 in your head and count loop iterations.
3. **Brute force:** count the exact steps, then simplify.
4. **Pattern:** the rules: drop constants, keep the dominant term; nested loops multiply, sequential loops add; halving or dividing → log.
5. **Plan:** label each loop with how many times it runs, combine, simplify.
6. **Code and test:** fill in the dictionary.
walkthrough:
| Function | Reasoning | Big-O |
|---|---|---|
| `first` | one index lookup, no loop | O(1) |
| `pairs_with_sum` | outer loop n times × inner loop up to n times ≈ n²/2 | O(n²) |
| `sum_and_max` | n steps, then another n steps: 2n, drop the constant | O(n) |
| `digits` | each step divides n by 10; a 6-digit number takes 6 steps; digits ≈ log₁₀ n | O(log n) |
| `sorted_median` | sorting is O(n log n), the lookup is O(1); keep the biggest term | O(n log n) |

**Why the base of the log doesn't matter:** log₁₀ n and log₂ n differ only by a constant factor (about 3.3), and Big-O drops constants. So both are just O(log n).

**Common mistake:** calling `sum_and_max` O(n²) because it has two loops. Only **nested** loops multiply.
:::

:::exercise From O(n) to O(1)
`sum_to(n)` should return 1 + 2 + … + n (and 0 for n = 0). A loop works but is O(n). Write a version that is **O(1)**: the same tiny amount of work for n = 10 or n = 10,000,000.
```python starter
def sum_to(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total
```
```python check
test("sum_to", [
    (1, 1, "n = 1"),
    (0, 0, "n = 0"),
    (4, 10, "n = 4 (1 + 2 + 3 + 4)"),
    (100, 5050, "n = 100"),
])
if not isinstance(need("sum_to")(10), int):
    raise AssertionError("Return a whole number (int). Tip: use // instead of / so the result isn't a float.")
speed("sum_to", lambda n: n, lambda n: n * (n + 1) // 2, sizes=(10**5, 10**6, 3 * 10**7), what="as n",
      tip="A loop does n additions. There's a formula for 1 + 2 + … + n that needs only one multiplication and one division.")
```
```python solution
def sum_to(n):
    return n * (n + 1) // 2
```
```python slow
def sum_to(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total
```
hint: Pair the numbers from both ends: 1 + n, 2 + (n − 1), 3 + (n − 2)… What does each pair add up to?
hint: Each pair adds up to n + 1, and there are n / 2 pairs.
hint: `return n * (n + 1) // 2` (use `//` so the answer stays a whole number).
approach:
1. **Understand:** same answer as the loop, but the work must not grow with n.
2. **Examples:** n = 4 → 10; n = 100 → 5050; n = 0 → 0.
3. **Brute force:** the starter loop: O(n). With n = 10,000,000 it does ten million additions.
4. **Pattern:** sometimes **maths** removes a loop entirely. Look for a formula.
5. **Plan:** write the sum forwards and backwards and add them up: each column is n + 1, and there are n columns, so twice the sum is n(n + 1).
6. **Code and test:** check n = 0 and n = 1 by hand.
walkthrough:
**The idea (Gauss's trick):**

```text
   1 +   2 + ... + 100
 100 +  99 + ... +   1
 ---------------------
 101 + 101 + ... + 101   (100 times) = 100 × 101
```

So twice the sum is n × (n + 1), and the sum is n × (n + 1) / 2.

- `n * (n + 1)` is always even (one of two neighbouring numbers is even), so `// 2` divides exactly and keeps an `int`. With `/` you'd get a float like `5050.0`, and floats lose precision for huge numbers.

**Trace:** n = 4 → 4 × 5 = 20 → 20 // 2 = **10** = 1 + 2 + 3 + 4. ✓

**Complexity:** O(1) time and space: one multiplication and one division, whatever n is.

**Lesson:** before optimising a loop, ask whether you need the loop at all.
:::

:::quiz
? An algorithm takes 3n² + 50n + 1000 steps. Its Big-O is:
- O(3n²)
+ O(n²)
- O(n² + n)
= Drop constants and keep only the fastest-growing term.
? If n doubles, how much longer does an O(n²) algorithm take?
- Twice as long
+ About four times as long
- The same
= (2n)² = 4n².
? A loop over n items, followed by a separate loop over the same n items, is:
+ O(n)
- O(n²)
- O(2ⁿ)
= Sequential loops add: n + n = 2n, which is O(n).
? Which line hides an O(n) loop?
- `nums[5]`
+ `if x in nums:` (where nums is a list)
- `d[key]` (where d is a dict)
= `in` on a list checks items one by one.
:::

@@@ lesson
id: space-and-cases
title: Space, best and worst cases, amortised cost
minutes: 17
summary: Measure memory as well as time, tell best, average and worst cases apart, see why list.append is O(1) "amortised", and work in place.
---
Big-O measures **memory** too. **Space complexity** counts the **extra** memory an algorithm needs as the input grows, not counting the input itself.

```python
def reversed_copy(nums):          # O(n) extra space: builds a whole new list
    return nums[::-1]

def reverse_in_place(nums):       # O(1) extra space: just two index variables
    i, j = 0, len(nums) - 1
    while i < j:
        nums[i], nums[j] = nums[j], nums[i]   # swap the ends, move inwards
        i += 1
        j -= 1

data = [1, 2, 3, 4, 5]
print(reversed_copy(data), data)
reverse_in_place(data)
print(data)
```

An algorithm that changes its input directly with O(1) extra memory is called **in place**. It saves memory, but it destroys the original, so only do it when that's allowed. A function that changes its input in place usually returns `None` (like `list.sort()`), to remind callers that it didn't make a copy.

Recursion also uses memory: every call that hasn't finished yet waits on the **call stack** (Lesson 21). A recursion 1,000 levels deep uses O(1,000) space even if it creates no lists.

### Best, average and worst case

The same algorithm can take different time on different inputs of the same size. Searching a list for a value:

```python
def linear_search(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1

nums = list(range(1, 11))
print(linear_search(nums, 1))    # best case: found at the first position
print(linear_search(nums, 10))   # worst case: found at the last position
print(linear_search(nums, 99))   # worst case: not there, every item checked
```

| Case | When | Cost |
|---|---|---|
| **Best** | target is first | O(1) |
| **Average** | target somewhere in the middle | about n/2 steps → O(n) |
| **Worst** | target last or missing | O(n) |

When people say "the complexity" without qualification, they usually mean the **worst case**, because it's a guarantee. Some algorithms are quoted by their average case when the worst is rare, like quicksort (O(n log n) on average, O(n²) worst; Lesson 26) and hash tables (O(1) on average, O(n) worst; Lesson 13).

### Amortised cost: why append is O(1)

A Python list keeps some spare room at the end. `append` normally just fills the next free slot: O(1). When the room runs out, Python allocates a **bigger** block (roughly 1.125–1.5 times the size, depending on the size) and copies everything across: O(n) for that one append.

![A list's capacity over 17 appends: most appends just fill a free slot (cheap), and occasionally the list is full, so all items are copied into a bigger block (expensive). Because the block grows by a fixed factor, copies get rarer as the list grows](figures/amortized-append.svg)

Because the capacity grows by a **factor** (not by a fixed amount), copies become rarer as the list grows. Averaged over many appends, each one costs O(1). That's **amortised O(1)**: an occasional expensive step, paid for by many cheap ones. You can watch the capacity jumps:

```python
import sys

nums = []
last = sys.getsizeof(nums)
for i in range(40):
    nums.append(i)
    size = sys.getsizeof(nums)
    if size != last:
        print(f"after {len(nums):>2} items the list grew to {size} bytes")
        last = size
```

(The exact sizes depend on the Python version; the pattern is what matters.)

:::exercise Reverse in place
Write `reverse_in_place(nums)` that reverses the list **in place** using O(1) extra space: swap items, don't build a new list, and don't use `reverse()`, `reversed()` or slicing. The function should return `None`.
```python starter
def reverse_in_place(nums):
    pass
```
```python check
if uses("reverse(") or uses("reversed(") or uses("[::-1]"):
    raise AssertionError("Swap the items yourself with two indexes, without reverse(), reversed() or [::-1].")
f = need("reverse_in_place")
for data, label in [([1, 2, 3, 4, 5], "an odd-length list"), ([1, 2, 3, 4], "an even-length list"), ([], "an empty list"), ([7], "one item"), ([1, 1, 2], "duplicates")]:
    original = list(data)
    arg = list(data)
    out = f(arg)
    if out is not None:
        raise AssertionError(f"reverse_in_place should change the list and return None, but it returned {out!r}.")
    if arg != original[::-1]:
        raise AssertionError(f"Fails on {label}: after reverse_in_place({original}), the list is {arg}, but it should be {original[::-1]}.")
```
```python solution
def reverse_in_place(nums):
    i, j = 0, len(nums) - 1
    while i < j:
        nums[i], nums[j] = nums[j], nums[i]
        i += 1
        j -= 1
```
hint: Swap the first and last items, then the second and second-to-last, and so on.
hint: Use two indexes: `i` from the start and `j` from the end. Swap, then move them towards each other.
hint: `i, j = 0, len(nums) - 1`; `while i < j:` swap with `nums[i], nums[j] = nums[j], nums[i]`, then `i += 1; j -= 1`. No return needed.
approach:
1. **Understand:** change the given list itself; return nothing; O(1) extra memory.
2. **Examples:** `[1, 2, 3, 4]` → `[4, 3, 2, 1]`; odd length `[1, 2, 3]` → `[3, 2, 1]` (the middle stays); `[]` and `[7]` stay the same.
3. **Brute force:** build a reversed copy and copy it back: O(n) extra space, not allowed here.
4. **Pattern:** **two pointers** from opposite ends (Lesson 7).
5. **Plan:** i at the start, j at the end; while i < j: swap, step inwards.
6. **Code and test:** for an empty list, j = −1 and the loop never runs. Good.
walkthrough:
**Line by line**

- `i, j = 0, len(nums) - 1` point at the two ends.
- `while i < j:` stops when the pointers meet (odd length: the middle item stays put) or cross (even length).
- `nums[i], nums[j] = nums[j], nums[i]` swaps in one line: Python evaluates the right side first, then assigns both.
- No `return`: the function returns `None`, and the caller's list has changed, because a list is passed by reference.

**Trace** on `[1, 2, 3, 4, 5]`:

| i | j | list after swap |
|---|---|---|
| 0 | 4 | [5, 2, 3, 4, 1] |
| 1 | 3 | [5, 4, 3, 2, 1] |
| 2 | 2 | stop (i == j) |

**Complexity:** O(n) time (n/2 swaps), O(1) extra space.

**Common wrong approach:** `nums = nums[::-1]` inside the function. That builds a new list and points the **local** name at it; the caller's list is unchanged.
:::

:::exercise Find the index
Write `index_of(nums, target)` that returns the **first** index where `target` appears, or `-1` if it isn't there. Don't use `.index()`.
```python starter
def index_of(nums, target):
    pass
```
```python check
if uses(".index("):
    raise AssertionError("Loop through the list yourself instead of using .index().")
test("index_of", [
    (([4, 2, 9], 9), 2, "the target at the end"),
    (([4, 2, 9], 4), 0, "the target first (best case)"),
    (([4, 2, 9], 7), -1, "a missing target (worst case)"),
    (([], 1), -1, "an empty list"),
    (([5, 3, 5], 5), 0, "duplicates: return the FIRST index"),
])
```
```python solution
def index_of(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
```
hint: `enumerate(nums)` gives you each index together with its item.
hint: Return as soon as you find a match; that way you return the first one.
hint: `for i, x in enumerate(nums): if x == target: return i`, then `return -1` after the loop.
approach:
1. **Understand:** first position of `target`, or −1. Lists can be empty or contain duplicates.
2. **Examples:** `([4, 2, 9], 9)` → 2; `([5, 3, 5], 5)` → 0 (first); `([], 1)` → −1.
3. **Brute force:** this is **linear search**, already the natural solution for an unsorted list: O(n).
4. **Pattern:** a scan with an **early return**.
5. **Plan:** walk with index; on a match return the index; after the loop return −1.
6. **Code and test:** best case O(1) (first item), worst case O(n) (missing).
walkthrough:
**Line by line**

- `for i, x in enumerate(nums):` gives `(0, first item)`, `(1, second item)`, …
- `if x == target: return i` leaves the function at the **first** match, so later duplicates don't matter.
- `return -1` is reached only when nothing matched. −1 is a common "not found" signal because it can't be a real index… although careful: in Python, `nums[-1]` is valid (the last item), so callers must check for −1 before using it.

**Trace** on `([4, 2, 9], 9)`:

| i | x | x == 9? |
|---|---|---|
| 0 | 4 | no |
| 1 | 2 | no |
| 2 | 9 | **yes** → return 2 |

**Complexity:** O(n) worst case, O(1) best case, O(1) space. On a **sorted** list, binary search does it in O(log n) (Lesson 23).
:::

:::quiz
? What does space complexity measure?
+ How the extra memory an algorithm needs grows with the input
- The size of the source code
- How much disk space Python uses
= Like time complexity, but for memory, not counting the input itself.
? What does "in place" mean?
+ The algorithm changes its input directly, using O(1) extra memory
- The algorithm runs in one place in the code
- It returns a copy
= Swapping inside the list instead of building a new one.
? Why is list.append called amortised O(1)?
+ Most appends are O(1); the occasional O(n) resize is spread over many appends
- It is always exactly one step
- It is O(n) but nobody minds
= Growing the capacity by a factor makes resizes rare enough to average out.
? Linear search for a value that isn't in the list is the:
- Best case
+ Worst case
- Average case
= Every item must be checked before you can say "not found".
:::

@@@ lesson
id: python-costs
title: The real cost of Python's built-ins
minutes: 18
summary: What each list, dict, set and string operation really costs, the traps that hide O(n) inside one line, and how to time code with time.perf_counter.
---
Python makes many operations one line long, but one line doesn't mean one step. Knowing the cost of the built-ins is the fastest way to spot slow code.

![Two pictures of looking for a value. In a list, Python checks the boxes one by one from the start: O(n). In a set or dict, Python computes the hash of the value and jumps straight to the right bucket: O(1) on average](figures/list-vs-set.svg)

### Lists

| Operation | Example | Cost |
|---|---|---|
| index, assign | `a[i]`, `a[i] = x` | O(1) |
| length | `len(a)` | O(1) |
| append, pop from the end | `a.append(x)`, `a.pop()` | O(1) amortised |
| insert / pop at the front or middle | `a.insert(0, x)`, `a.pop(0)` | O(n): everything after it shifts |
| search | `x in a`, `a.index(x)`, `a.count(x)` | O(n) |
| remove by value | `a.remove(x)` | O(n) |
| slice | `a[i:j]` | O(j − i): it copies |
| copy, extend | `a.copy()`, `a + b`, `a.extend(b)` | O(n) / O(len(b)) |
| min, max, sum | `min(a)` | O(n) |
| sort | `a.sort()`, `sorted(a)` | O(n log n) |

### Dicts and sets (hash tables)

| Operation | Example | Average cost |
|---|---|---|
| look up, insert, delete | `d[k]`, `d[k] = v`, `del d[k]`, `s.add(x)` | O(1) |
| membership | `k in d`, `x in s` | O(1) |
| iterate | `for k in d` | O(n) |
| set union / intersection | `s | t`, `s & t` | O(len(s) + len(t)) / O(min(len(s), len(t))) |

Keys must be **hashable** (unchangeable): numbers, strings, tuples yes; lists and dicts no. Lesson 13 shows why.

### Strings

Strings are **immutable**: every "change" builds a new string. Indexing and `len` are O(1); `s + t`, slicing, `s.replace`, `s.lower()` and `sub in s` are O(n). To build a long string from many pieces, collect the pieces in a list and `"".join(pieces)` once at the end: O(total length).

### Deques for the front

`collections.deque` adds and removes at **both** ends in O(1). Use it whenever you'd call `pop(0)` or `insert(0, x)` on a list (queues, Lesson 17):

```python
from collections import deque
import time

n = 50_000
items = list(range(n))
start = time.perf_counter()
while items:
    items.pop(0)                      # O(n) each: shifts everything left
print(f"list.pop(0):     {time.perf_counter() - start:.3f} s")

items = deque(range(n))
start = time.perf_counter()
while items:
    items.popleft()                   # O(1) each
print(f"deque.popleft(): {time.perf_counter() - start:.3f} s")
```

### Timing code yourself

`time.perf_counter()` is a precise clock. Measure a few sizes and look at the **ratio**: if doubling n doubles the time, it's O(n); if it quadruples, it's O(n²).

```python
import time

def timed(func, arg):
    start = time.perf_counter()
    func(arg)
    return time.perf_counter() - start

def in_list_many(n):
    data = list(range(n))
    return sum(1 for x in range(n) if x in data)     # n searches of O(n) each

def in_set_many(n):
    data = set(range(n))
    return sum(1 for x in range(n) if x in data)     # n searches of O(1) each

for n in [1_000, 2_000, 4_000]:
    print(f"n={n:>5}  list: {timed(in_list_many, n):.4f} s   set: {timed(in_set_many, n):.5f} s")
```

The list version roughly quadruples each time n doubles (O(n²) overall); the set version roughly doubles (O(n)). Timings bounce around a bit from run to run; the trend is what counts. For careful measurements, the `timeit` module repeats a statement many times and reports the best.

:::exercise Items in both lists
Write `common_items(a, b)` that returns a **sorted** list of the values that appear in both lists, each value once. It must be fast for lists of 50,000 numbers.
```python starter
def common_items(a, b):
    result = []
    for x in a:
        if x in b and x not in result:
            result.append(x)
    return sorted(result)
```
```python check
test("common_items", [
    (([1, 2, 3, 4], [3, 4, 5]), [3, 4], "a simple overlap"),
    (([1, 2], [3, 4]), [], "no overlap"),
    (([], [1, 2]), [], "an empty list"),
    (([2, 2, 1], [2, 2]), [2], "duplicates: each value once"),
    (([5, 1, 3], [3, 1, 5]), [1, 3, 5], "the result must be sorted"),
])
def _ref(a, b):
    return sorted(set(a) & set(b))
speed("common_items", lambda n: (list(range(0, 2 * n, 2)), list(range(n, 3 * n))), _ref,
      sizes=(1_000, 12_000, 50_000), what="numbers in each list",
      tip="`x in b` scans the whole list b every time. Turn the lists into sets first: `in` and `&` on sets are fast.")
```
```python solution
def common_items(a, b):
    return sorted(set(a) & set(b))
```
```python slow
def common_items(a, b):
    result = []
    for x in a:
        if x in b and x not in result:
            result.append(x)
    return sorted(result)
```
hint: The starter is correct but slow: `x in b` and `x not in result` are both O(n) list scans inside a loop.
hint: Sets make membership O(1), and `set_a & set_b` gives the values in both sets directly.
hint: `return sorted(set(a) & set(b))`.
approach:
1. **Understand:** values in both lists, no repeats, sorted ascending.
2. **Examples:** `[1, 2, 3, 4]` and `[3, 4, 5]` → `[3, 4]`; duplicates `[2, 2, 1]`, `[2, 2]` → `[2]`.
3. **Brute force:** the starter: for each x in a, scan b (and the result): O(n × m).
4. **Pattern:** repeated membership checks → **set**. Set intersection does exactly "in both".
5. **Plan:** convert both to sets, intersect, sort.
6. **Code and test:** cost: O(n + m) for the sets and intersection, plus O(k log k) to sort the k common values.
walkthrough:
**Line by line**

- `set(a)` and `set(b)` build hash sets: O(len(a) + len(b)). They also remove duplicates for free.
- `&` is set intersection: it loops over the smaller set and checks each value in the other, O(1) per check.
- `sorted(...)` returns a list in ascending order.

**Trace** on `([5, 1, 3], [3, 1, 5, 9])`:

| step | value |
|---|---|
| set(a) | {1, 3, 5} |
| set(b) | {1, 3, 5, 9} |
| intersection | {1, 3, 5} |
| sorted | [1, 3, 5] |

**Complexity:** O(n + m + k log k) time and O(n + m) space, versus O(n × m) for the starter. With 50,000 numbers each, that's about 100,000 steps instead of 2.5 billion.
:::

:::exercise Remove every copy
Write `remove_all(nums, x)` that returns a **new** list with every occurrence of `x` removed, keeping the order of the others. It must be fast for 50,000 numbers.
```python starter
def remove_all(nums, x):
    result = list(nums)
    while x in result:
        result.remove(x)
    return result
```
```python check
test("remove_all", [
    (([1, 2, 1, 3], 1), [2, 3], "two copies"),
    (([1, 2, 3], 9), [1, 2, 3], "nothing to remove"),
    (([], 1), [], "an empty list"),
    (([4, 4, 4], 4), [], "everything removed"),
    (([3, 1, 2, 1], 1), [3, 2], "order kept"),
])
def _ref(nums, x):
    return [v for v in nums if v != x]
speed("remove_all", lambda n: ([0, 1] * (n // 2), 0), _ref, sizes=(1_000, 25_000, 100_000), what="numbers",
      tip="Each `remove` scans from the start and shifts everything after it: O(n) per call, O(n²) overall. Build the answer in one pass instead.")
```
```python solution
def remove_all(nums, x):
    return [v for v in nums if v != x]
```
```python slow
def remove_all(nums, x):
    result = list(nums)
    while x in result:
        result.remove(x)
    return result
```
hint: The starter calls `x in result` and `result.remove(x)` once per copy, and each call is O(n).
hint: Instead of deleting from a list, build a new list containing only the values you want to keep.
hint: `return [v for v in nums if v != x]`.
approach:
1. **Understand:** a new list, same order, without any `x`.
2. **Examples:** `([1, 2, 1, 3], 1)` → `[2, 3]`; nothing to remove → unchanged copy; all removed → `[]`.
3. **Brute force:** the starter: repeated `remove`, each O(n) → O(n²) when many copies.
4. **Pattern:** **filter in one pass**: keep what you want instead of deleting what you don't.
5. **Plan:** loop once, append every value that isn't x.
6. **Code and test:** O(n) time, O(n) space for the new list.
walkthrough:
**Line by line**

- `[v for v in nums if v != x]` is a list comprehension: it visits each value once and keeps the ones that aren't `x`, in order.

**Why the starter is slow:** `remove` finds the first copy (scanning from the start) and then **shifts every later item left by one** to close the gap. With 25,000 copies in a 50,000-item list, that's about 25,000 × 25,000 steps.

**Trace** on `([1, 2, 1, 3], 1)`:

| v | v != 1? | result so far |
|---|---|---|
| 1 | no | [] |
| 2 | yes | [2] |
| 1 | no | [2] |
| 3 | yes | [2, 3] |

**Complexity:** O(n) time, O(n) space.

**General lesson:** deleting from the middle of a list in a loop is a classic hidden O(n²). Filter into a new list instead.
:::

:::quiz
? What does `nums.insert(0, x)` cost on a list of n items?
- O(1)
+ O(n), because every item shifts one place right
- O(log n)
= Inserting at the front moves everything. Use a deque for fast front operations.
? Which is O(1) on average?
- `x in some_list`
+ `x in some_set`
- `some_list.count(x)`
= Sets and dicts use hashing.
? Doubling n made your function take about four times longer. It's probably:
- O(n)
+ O(n²)
- O(log n)
= Quadratic time grows with the square of n.
? What's the efficient way to build a long string from many pieces?
+ Collect the pieces in a list and join them once with "".join(pieces)
- Add them one by one with +
- Convert each piece to a list
= join builds the result once, in O(total length).
:::
