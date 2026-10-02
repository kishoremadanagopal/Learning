@@@ part
id: 2
title: Arrays and Strings
level: Beginner
blurb: The workhorse structures and the patterns built on them: two pointers, sliding windows, prefix sums, 2-D grids, string building and pattern matching (KMP and Rabin-Karp).

@@@ lesson
id: arrays
title: Arrays and Python lists
minutes: 18
summary: How arrays sit in memory, why indexing is O(1) but inserting is O(n), the loop patterns you'll use everywhere, and in-place tricks like rotating with three reversals.
---
An **array** stores items in one **contiguous** block of memory, side by side. Because every slot is the same size, the computer finds slot *i* with one calculation: start address + i × slot size. That's why **indexing is O(1)**, whatever the length.

![An array drawn as eight boxes side by side with indexes 0 to 7 above them. Reading index 5 jumps straight there. Inserting at index 2 forces every box from index 2 onwards to shift one place to the right](figures/array-memory.svg)

A Python `list` is a **dynamic array**: a contiguous block of references (pointers) to the actual objects, with spare room at the end so it can grow (Lesson 4). That gives lists the classic array costs:

| Operation | Cost | Why |
|---|---|---|
| `a[i]`, `a[i] = x` | O(1) | address arithmetic |
| `a.append(x)`, `a.pop()` | O(1) amortised | the end has spare room |
| `a.insert(i, x)`, `a.pop(i)`, `del a[i]` | O(n − i) | items after i shift |
| `x in a` | O(n) | no shortcut: check one by one |

(In lower-level languages like C or Java, arrays have a fixed size. Python's `array` module and NumPy arrays store raw numbers instead of references, which is faster and smaller for numeric work.)

### Loop patterns

```python
nums = [5, 3, 8, 1]

for x in nums:                        # values only
    print(x, end=" ")
print()
for i, x in enumerate(nums):          # index and value
    print(f"{i}:{x}", end=" ")
print()
for i in range(len(nums) - 1):        # neighbouring pairs (i, i + 1)
    print(nums[i], "->", nums[i + 1], end="   ")
print()
for x in reversed(nums):              # backwards, without copying
    print(x, end=" ")
print()
```

Off-by-one errors live in the `range` bounds. If the loop body uses `nums[i + 1]`, the loop must stop at `len(nums) - 1`.

### The running-minimum pattern: best time to buy and sell

Prices of a share on consecutive days. Buy once, sell later. What's the most profit? Brute force tries every buy day with every later sell day: O(n²). One pass is enough if you remember the **cheapest price so far**: selling today, the best you could have done is today's price minus that minimum.

```python
def max_profit(prices):
    cheapest = float("inf")
    best = 0
    for p in prices:
        cheapest = min(cheapest, p)          # best day to have bought, up to today
        best = max(best, p - cheapest)       # profit if we sell today
    return best

print(max_profit([7, 1, 5, 3, 6, 4]))   # buy at 1, sell at 6
print(max_profit([7, 6, 4, 3, 1]))      # prices only fall: don't trade
```

### Rotating in place with three reversals

Rotating `[1, 2, 3, 4, 5, 6, 7]` right by 3 gives `[5, 6, 7, 1, 2, 3, 4]`. Slicing (`nums[-k:] + nums[:-k]`) builds new lists, O(n) space. A neat in-place trick: reverse the whole list, then reverse the first k items and the rest separately.

```python
def reverse(nums, i, j):                 # reverse nums[i..j] in place
    while i < j:
        nums[i], nums[j] = nums[j], nums[i]
        i, j = i + 1, j - 1

nums = [1, 2, 3, 4, 5, 6, 7]
k = 3
reverse(nums, 0, len(nums) - 1);  print(nums)   # [7, 6, 5, 4, 3, 2, 1]
reverse(nums, 0, k - 1);          print(nums)   # [5, 6, 7, 4, 3, 2, 1]
reverse(nums, k, len(nums) - 1);  print(nums)   # [5, 6, 7, 1, 2, 3, 4]
```

:::exercise Best time to buy and sell
Write `max_profit(prices)` returning the largest profit from one buy followed by one later sell, or 0 if no profit is possible. It must handle 100,000 prices quickly. Try it before scrolling up!
```python starter
def max_profit(prices):
    pass
```
```python check
test("max_profit", [
    ([7, 1, 5, 3, 6, 4], 5, "buy at 1, sell at 6"),
    ([7, 6, 4, 3, 1], 0, "falling prices"),
    ([], 0, "no prices"),
    ([5], 0, "one day"),
    ([2, 4, 1], 2, "the lowest price comes too late to use"),
    ([3, 3, 3], 0, "flat prices"),
    ([1, 2, 4, 2, 5, 7, 2, 4, 9, 0], 8, "the best buy is the first day, best sell near the end"),
])
def _ref(prices):
    lo, best = float("inf"), 0
    for p in prices:
        lo = min(lo, p); best = max(best, p - lo)
    return best
import random
speed("max_profit", lambda n: [_r.randint(1, 10_000) for _r in [random.Random(n)] for _ in range(n)], _ref,
      sizes=(1_000, 6_000, 100_000), what="prices",
      tip="Trying every buy day with every sell day is O(n²). Keep the cheapest price seen so far and check today's profit against it.")
```
```python solution
def max_profit(prices):
    cheapest = float("inf")
    best = 0
    for p in prices:
        cheapest = min(cheapest, p)
        best = max(best, p - cheapest)
    return best
```
```python slow
def max_profit(prices):
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best
```
hint: If you sell on a given day, which buy day would you have wanted?
hint: The cheapest price **before** today. Keep it in a variable as you walk through the days.
hint: `cheapest = inf, best = 0`; for each p: `cheapest = min(cheapest, p)`, `best = max(best, p - cheapest)`.
approach:
1. **Understand:** buy before you sell; at most one trade; no profit possible → 0. Empty list → 0.
2. **Examples:** `[7, 1, 5, 3, 6, 4]` → 5 (buy 1, sell 6). `[2, 4, 1]` → 2: the 1 comes after the peak, so it doesn't help.
3. **Brute force:** every pair (buy i, sell j > i): O(n²), about 5 billion pairs for 100,000 days.
4. **Pattern:** **running minimum**: for each sell day, the best buy day is the cheapest day before it.
5. **Plan:** track the cheapest price so far and the best profit so far in one pass.
6. **Code and test:** check the falling list (profit stays 0) and the empty list.
walkthrough:
**Line by line**

- `cheapest = float("inf")`: before any day, nothing has been seen; infinity is bigger than any real price, so the first price replaces it.
- `best = 0`: "don't trade" is always allowed, so profit never goes below 0.
- `cheapest = min(cheapest, p)`: update the best buy price up to and including today.
- `best = max(best, p - cheapest)`: the profit if we sell today. (Buying and selling on the same day gives 0, which is harmless.)

**Trace** on `[7, 1, 5, 3, 6, 4]`:

| p | cheapest | p − cheapest | best |
|---|---|---|---|
| 7 | 7 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 5 | 1 | 4 | 4 |
| 3 | 1 | 2 | 4 |
| 6 | 1 | 5 | **5** |
| 4 | 1 | 3 | 5 |

**Complexity:** O(n) time, O(1) space.

**Common wrong approach:** `max(prices) - min(prices)`. For `[2, 4, 1]` it gives 3, but the minimum (1) comes **after** the maximum, so that trade is impossible.
:::

:::exercise Rotate in place
Write `rotate(nums, k)` that rotates the list **right** by `k` steps **in place** (O(1) extra space) and returns `None`. `k` can be bigger than the length. Don't use slicing to build new lists.
```python starter
def rotate(nums, k):
    pass
```
```python check
import re
code = "\n".join(l.split("#")[0] for l in __source__.splitlines())
if re.search(r"\[[^\]]*:[^\]]*\]", code) or ".insert(" in code or ".pop(" in code:
    raise AssertionError("Rotate in place with swaps (for example the three-reversal trick), without slices, insert or pop.")
f = need("rotate")
for data, k, label in [([1, 2, 3, 4, 5, 6, 7], 3, "k = 3"), ([1, 2], 3, "k bigger than the length"),
                       ([], 4, "an empty list"), ([1, 2, 3], 0, "k = 0"), ([1, 2, 3], 3, "k equal to the length"),
                       ([9], 5, "one item"), ([1, 2, 3, 4, 5, 6], 2, "an even length")]:
    arg = list(data)
    out = f(arg, k)
    n = len(data)
    expected = data[-(k % n):] + data[:-(k % n)] if n and k % n else list(data)
    if out is not None:
        raise AssertionError(f"rotate should change the list in place and return None, but it returned {out!r}.")
    if arg != expected:
        raise AssertionError(f"Fails on {label}: rotate({data}, {k}) left the list as {arg}, but it should be {expected}.")
```
```python solution
def rotate(nums, k):
    n = len(nums)
    if n == 0:
        return
    k %= n                        # rotating by n is the same as not rotating

    def reverse(i, j):
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i, j = i + 1, j - 1

    reverse(0, n - 1)             # whole list
    reverse(0, k - 1)             # first k items
    reverse(k, n - 1)             # the rest
```
hint: Rotating by `k` and by `k % len(nums)` give the same result. Handle the empty list first.
hint: Use the three-reversal trick: reverse everything, then reverse the first k items, then reverse the rest.
hint: Write a helper `reverse(i, j)` that swaps inwards with two pointers, then call it on `(0, n-1)`, `(0, k-1)` and `(k, n-1)`.
approach:
1. **Understand:** move each item k places right, wrapping around; change the list itself; k may exceed n.
2. **Examples:** `[1..7]`, k = 3 → `[5, 6, 7, 1, 2, 3, 4]`. `[1, 2]`, k = 3 → same as k = 1 → `[2, 1]`. `[]` → stays empty.
3. **Brute force:** rotate by one step, k times (each step O(n)): O(n·k). Or build a new list: O(n) space.
4. **Pattern:** **reversal trick** + **two pointers**. Reversing the whole list puts the last k items first, but backwards; reversing each part fixes the order inside it.
5. **Plan:** n = len; if 0 stop; k %= n; reverse all; reverse first k; reverse rest.
6. **Code and test:** check k = 0 (reverse(0, −1) does nothing, then reversing the rest restores the original).
walkthrough:
**Line by line**

- `k %= n` turns k = 10 on 7 items into 3. Without it, `reverse(0, k - 1)` would use indexes past the end.
- The inner `reverse(i, j)` is the two-pointer swap from Lesson 4. It can change `nums` because it modifies the list object, not the name.
- Three calls do the rotation.

**Trace** on `[1, 2, 3, 4, 5, 6, 7]`, k = 3:

| step | list |
|---|---|
| reverse all | [7, 6, 5, 4, 3, 2, 1] |
| reverse first 3 | [5, 6, 7, 4, 3, 2, 1] |
| reverse the rest | [5, 6, 7, 1, 2, 3, 4] |

**Why it works:** after reversing everything, the last k items are at the front but backwards, and the first n − k items are at the back, also backwards. Reversing each block puts both blocks the right way round.

**Complexity:** O(n) time (each item is swapped at most twice), O(1) space.
:::

:::quiz
? Why is `a[i]` O(1) for an array?
+ The address is computed directly: start + i × slot size
- Python remembers every index you've used
- Arrays are always short
= Contiguous, equal-size slots make any position one calculation away.
? What does `a.insert(0, x)` cost on a list of n items?
- O(1)
+ O(n)
- O(log n)
= Every existing item shifts right by one.
? In "best time to buy and sell", why doesn't `max(prices) - min(prices)` work?
+ The minimum might come after the maximum, which is an impossible trade
- It's too slow
- max and min don't work on lists
= You must buy before you sell, so order matters.
? Rotating right by k = 10 on a list of 7 items is the same as rotating by:
- 10
+ 3
- 7
= 10 % 7 = 3: every 7 steps brings the list back to where it started.
:::

@@@ lesson
id: two-pointers
title: Two pointers
minutes: 18
summary: Two indexes that move towards each other or in the same direction. Turns many O(n²) pair searches on sorted data into O(n), and powers in-place clean-ups.
---
**Two pointers** means keeping two indexes into the data and moving them according to a rule. There are two main shapes:

![Two pointer patterns. Opposite ends: a sorted array with L at the left end and R at the right end moving towards each other. Same direction: a slow pointer W marks where to write the next kept item, and a fast pointer R reads ahead through the array](figures/two-pointers.svg)

| Shape | How the pointers move | Typical problems |
|---|---|---|
| **Opposite ends** | `left` from the start, `right` from the end, moving inwards | pair with a target sum in a **sorted** array, palindromes, reversing, container with most water |
| **Same direction** (fast/slow, read/write) | `fast` reads every item; `slow` marks where to write | removing duplicates or zeros in place, partitioning, merging sorted lists |

### Opposite ends: a pair with a given sum (sorted input)

With sorted numbers, look at the smallest and largest. If their sum is too small, the only way to increase it is to move `left` right; if too big, move `right` left. Each step rules out one number for good, so it's O(n):

```python
def pair_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        if s < target:
            left += 1            # need a bigger sum
        else:
            right -= 1           # need a smaller sum
    return []

print(pair_sum_sorted([1, 3, 4, 6, 8, 11], 10))   # 4 + 6
print(pair_sum_sorted([1, 2, 3], 100))
```

Why can't it miss the answer? When the sum is too small with `nums[left]` and the **largest** remaining number, `nums[left]` can't be part of any pair (every other partner is smaller still), so it's safe to drop.

### Opposite ends: a palindrome check

A **palindrome** reads the same forwards and backwards. Compare the outer characters and move inwards, skipping anything that isn't a letter or digit:

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        elif s[left].lower() != s[right].lower():
            return False
        else:
            left, right = left + 1, right - 1
    return True

print(is_palindrome("A man, a plan, a canal: Panama"))
print(is_palindrome("race a car"))
```

This uses O(1) extra space; `cleaned == cleaned[::-1]` is simpler but builds two new strings.

### Same direction: write pointer and read pointer

Move every zero to the end, keeping the order of the other numbers, in place. `write` is where the next non-zero goes; `read` scans everything:

```python
def move_zeros(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1

data = [0, 1, 0, 3, 12]
move_zeros(data)
print(data)
```

### Merging two sorted lists

Two pointers, one in each list, always taking the smaller front item. This is the heart of merge sort (Lesson 26):

```python
def merge(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])            # one of these is empty
    out.extend(b[j:])
    return out

print(merge([1, 4, 9], [2, 3, 10, 11]))
```

:::exercise Pair with target sum
`nums` is sorted in increasing order. Write `pair_sum_sorted(nums, target)` that returns `[i, j]` (with `i < j`) for any two positions whose values add up to `target`, or `[]` if there are none. Use O(1) extra space and make it fast for 100,000 numbers.
```python starter
def pair_sum_sorted(nums, target):
    pass
```
```python check
def _valid(got, nums, target):
    exists = any(nums[a] + nums[b] == target for a in range(len(nums)) for b in range(a + 1, len(nums)))
    if not exists:
        return got == []
    return isinstance(got, (list, tuple)) and len(got) == 2 and 0 <= got[0] < got[1] < len(nums) and nums[got[0]] + nums[got[1]] == target
test("pair_sum_sorted", [
    (([1, 3, 4, 6, 8, 11], 10), [2, 3], "the example"),
    (([1, 2, 3], 100), [], "no pair"),
    (([], 5), [], "an empty list"),
    (([5], 10), [], "one number can't pair with itself"),
    (([-4, -1, 0, 2, 7], -5), [0, 1], "negative numbers"),
    (([2, 2, 3], 4), [0, 1], "a pair of equal values"),
    (([1, 5, 9], 14), [1, 2], "the pair at the end"),
], valid=_valid)
def _ref(nums, target):
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target: return [l, r]
        if s < target: l += 1
        else: r -= 1
    return []
speed("pair_sum_sorted", lambda n: (list(range(0, 2 * n, 2)), 2 * n + 1), _ref, sizes=(1_000, 6_000, 100_000),
      what="numbers", valid=lambda got, nums, t: got == [],
      tip="Checking every pair is O(n²). Start one pointer at each end: if the sum is too small move the left one right, if too big move the right one left.")
```
```python solution
def pair_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        if s < target:
            left += 1
        else:
            right -= 1
    return []
```
```python slow
def pair_sum_sorted(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```
hint: The list is sorted. Look at the smallest and the largest number together.
hint: If their sum is too small, the smallest number can't be in any pair: move the left pointer right. If too big, move the right pointer left.
hint: `left, right = 0, len(nums) - 1`; `while left < right`: compute `s`; equal → return; `s < target` → `left += 1`; else `right -= 1`. After the loop, `return []`.
approach:
1. **Understand:** sorted input; return two different positions whose values sum to target, or []. Any valid pair is accepted.
2. **Examples:** `[1, 3, 4, 6, 8, 11]`, 10 → `[2, 3]` (4 + 6). `[5]`, 10 → `[]` (can't use the same item twice).
3. **Brute force:** all pairs: O(n²).
4. **Pattern:** **sorted** + **pair** → two pointers from opposite ends.
5. **Plan:** compare the sum with the target and move the pointer that can fix it; stop when they meet.
6. **Code and test:** O(n) time, O(1) space. (Unsorted input? Then use a hash map: Lesson 14.)
walkthrough:
**Line by line**

- `left, right = 0, len(nums) - 1` start at the two ends.
- `while left < right:` stops before a pointer pairs with itself.
- `s < target` → `left += 1`: a bigger left value is the only way to increase the sum.
- `else: right -= 1`: the sum is too big, so try a smaller right value.

**Trace** on `[1, 3, 4, 6, 8, 11]`, target 10:

| left | right | values | sum | action |
|---|---|---|---|---|
| 0 | 5 | 1 + 11 | 12 | too big → right − 1 |
| 0 | 4 | 1 + 8 | 9 | too small → left + 1 |
| 1 | 4 | 3 + 8 | 11 | too big → right − 1 |
| 1 | 3 | 3 + 6 | 9 | too small → left + 1 |
| 2 | 3 | 4 + 6 | **10** | return [2, 3] |

**Why it's correct:** every move throws away one value that provably can't be in a valid pair, so no answer is skipped.

**Complexity:** O(n) time (the pointers together move at most n steps), O(1) space.
:::

:::exercise Remove duplicates in place
`nums` is sorted. Write `remove_duplicates(nums)` that rearranges it **in place** so the first `k` items are the distinct values in order, and returns `k`. What's left after position k doesn't matter. Use O(1) extra space (no sets, no new lists).
```python starter
def remove_duplicates(nums):
    pass
```
```python check
if uses("set(") or uses("sorted("):
    raise AssertionError("Do it in place with two pointers, without building a set or a new list.")
f = need("remove_duplicates")
for data, label in [([1, 1, 2], "a short list"), ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], "many duplicates"), ([], "an empty list"),
                    ([5], "one item"), ([2, 2, 2], "all the same"), ([1, 2, 3], "no duplicates"), ([-3, -3, 0, 7, 7], "negatives")]:
    arg = list(data)
    k = f(arg)
    expected = sorted(set(data))
    if not isinstance(k, int):
        raise AssertionError(f"Fails on {label}: return k, the number of distinct values (got {k!r}).")
    if k != len(expected) or arg[:k] != expected:
        raise AssertionError(f"Fails on {label}: remove_duplicates({data}) returned {k} and the list starts {arg[:max(k, 0)]}; "
                             f"expected {len(expected)} with the list starting {expected}.")
```
```python solution
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 1                          # nums[0] is always kept
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```
hint: Because the list is sorted, equal values sit next to each other.
hint: Use a `write` pointer for where the next new value goes, and a `read` pointer that scans. Compare each value with the last one you kept.
hint: If empty return 0. `write = 1`; for `read` from 1: if `nums[read] != nums[write - 1]`: `nums[write] = nums[read]`, `write += 1`. Return `write`.
approach:
1. **Understand:** in place; return how many distinct values; the list must start with them in order.
2. **Examples:** `[1, 1, 2]` → 2, list starts `[1, 2]`. `[]` → 0. `[2, 2, 2]` → 1.
3. **Brute force:** `sorted(set(nums))` then copy back: O(n) extra space, not allowed.
4. **Pattern:** **same-direction two pointers** (read/write). Sorted → duplicates are adjacent.
5. **Plan:** keep the first value; scan the rest; copy a value forward only if it differs from the last kept one.
6. **Code and test:** check `[]`, one item, and all-equal.
walkthrough:
**Line by line**

- `if not nums: return 0` handles the empty list, where `nums[0]` would fail.
- `write = 1`: the first value is always kept, so the next free spot is index 1.
- `nums[read] != nums[write - 1]` compares with the **last kept** value, not with the previous item read.
- `return write`: everything before `write` is the distinct values.

**Trace** on `[0, 0, 1, 1, 2]`:

| read | nums[read] | last kept | new? | list (first write items) | write |
|---|---|---|---|---|---|
| start | | 0 | | [0] | 1 |
| 1 | 0 | 0 | no | [0] | 1 |
| 2 | 1 | 0 | yes | [0, 1] | 2 |
| 3 | 1 | 1 | no | [0, 1] | 2 |
| 4 | 2 | 1 | yes | [0, 1, 2] | 3 |

Returns **3**.

**Complexity:** O(n) time, O(1) space.
:::

:::quiz
? When does the opposite-ends pair search work?
+ When the array is sorted
- On any array
- Only when all numbers are positive
= Sorted order is what tells you which pointer to move.
? In the pair search, the sum is smaller than the target. What do you do?
+ Move the left pointer right, to a bigger value
- Move the right pointer left
- Move both pointers
= Only a bigger left value can increase the sum.
? In the read/write pattern, what does the write pointer mark?
+ Where the next item to keep should go
- The item being read
- The end of the list
= Read scans everything; write builds the result at the front.
? What is the time complexity of merging two sorted lists of sizes n and m?
- O(n × m)
+ O(n + m)
- O(log n)
= Each step moves one pointer forward.
:::

@@@ lesson
id: sliding-window
title: Sliding window
minutes: 20
summary: Keep a running window over a contiguous range and update it as it slides, instead of recomputing. Fixed-size and variable-size windows, each O(n).
---
Many problems ask about **contiguous** runs: "the largest sum of any 5 days in a row", "the longest substring with no repeated letter". The brute force looks at every start and end: O(n²) windows, often with O(n) work each. A **sliding window** keeps track of the current run and **updates** it as it moves, so each item enters and leaves once: O(n).

![A row of numbers with a window of size 3 highlighted. As the window slides one step right, one number leaves on the left and one joins on the right, so the new sum is the old sum minus the leaving number plus the joining number](figures/sliding-window.svg)

### Fixed-size window

Largest sum of k consecutive numbers. Instead of re-adding k numbers for every position, slide: add the number that enters, subtract the one that leaves.

```python
def max_window_sum(nums, k):
    window = sum(nums[:k])                    # the first window
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]       # one joins, one leaves
        best = max(best, window)
    return best

print(max_window_sum([2, 1, 5, 1, 3, 2], 3))   # 5 + 1 + 3
```

### Variable-size window: grow and shrink

When the window's size isn't fixed, use two pointers, `left` and `right`. Move `right` to **grow** the window; when the window breaks the rule, move `left` to **shrink** it until it's valid again. Track the best valid window as you go.

Shortest subarray with sum at least a target (all numbers positive):

```python
def min_len_at_least(nums, target):
    left = 0
    total = 0
    best = float("inf")
    for right, x in enumerate(nums):
        total += x                             # grow
        while total >= target:                 # valid: try to shrink
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == float("inf") else best

print(min_len_at_least([2, 3, 1, 2, 4, 3], 7))   # [4, 3]
```

Even with a `while` inside the `for`, it's O(n): `left` only ever moves forward, so across the whole run it moves at most n times. This **"each pointer moves at most n times"** argument is how you prove sliding windows are linear.

Longest substring without a repeated character, using a set for what's in the window:

```python
def longest_unique(s):
    seen = set()
    left = best = 0
    for right, ch in enumerate(s):
        while ch in seen:                    # repeat: shrink from the left
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best

print(longest_unique("abcabcbb"), longest_unique("bbbbb"), longest_unique("pwwkew"))
```

### The template

```py-static
left = 0
state = empty                      # sum, counts, set... whatever the rule needs
for right in range(len(data)):
    add data[right] to state
    while the window is invalid:   # (or: if the window is too big, for fixed size)
        remove data[left] from state
        left += 1
    update the answer with the window [left, right]
```

Sliding windows need the rule to be **monotonic**: once a window is invalid, growing it can't make it valid again. With negative numbers, "sum at least target" breaks that, and you need prefix sums (Lesson 9) instead.

:::exercise Best k days in a row
Write `max_window_sum(nums, k)` that returns the largest sum of any `k` consecutive numbers. You can assume `1 <= k <= len(nums)`. Numbers can be negative. Make it fast for 100,000 numbers with k = 5,000.
```python starter
def max_window_sum(nums, k):
    pass
```
```python check
test("max_window_sum", [
    (([2, 1, 5, 1, 3, 2], 3), 9, "the example"),
    (([4], 1), 4, "one number"),
    (([1, 2, 3], 3), 6, "k equals the length"),
    (([-5, -2, -3], 2), -5, "all negative"),
    (([3, -1, 4, -10, 5, 5], 2), 10, "the best window at the end"),
    (([9, 1, 1, 1], 1), 9, "k = 1"),
])
def _ref(nums, k):
    w = sum(nums[:k]); best = w
    for i in range(k, len(nums)):
        w += nums[i] - nums[i - k]; best = max(best, w)
    return best
import random
speed("max_window_sum", lambda n: ([_r.randint(-100, 100) for _r in [random.Random(n)] for _ in range(n)], n // 20), _ref,
      sizes=(2_000, 40_000, 100_000), what="numbers",
      tip="Re-adding k numbers for every position is O(n·k). Slide the window: add the number that joins and subtract the one that leaves.")
```
```python solution
def max_window_sum(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best
```
```python slow
def max_window_sum(nums, k):
    best = float("-inf")
    for i in range(len(nums) - k + 1):
        best = max(best, sum(nums[i:i + k]))
    return best
```
hint: Two neighbouring windows share k − 1 numbers. Don't add them up again.
hint: Moving the window right by one: the number at `i` joins and the number at `i - k` leaves.
hint: `window = sum(nums[:k])`, `best = window`; for `i` from k to the end: `window += nums[i] - nums[i - k]`, `best = max(best, window)`.
approach:
1. **Understand:** contiguous runs of exactly k; return the biggest sum; negatives allowed (so the answer can be negative).
2. **Examples:** `[2, 1, 5, 1, 3, 2]`, k = 3 → 9 (5 + 1 + 3). `[-5, -2, -3]`, k = 2 → −5.
3. **Brute force:** sum every window: O(n·k). With n = 100,000 and k = 5,000 that's 500 million additions.
4. **Pattern:** "k consecutive" → **fixed-size sliding window**.
5. **Plan:** sum the first window; slide: add the new number, subtract the old; track the max.
6. **Code and test:** start `best` from the first window, not 0, so all-negative inputs work.
walkthrough:
**Line by line**

- `window = sum(nums[:k])` is the only full sum we ever compute: O(k).
- `for i in range(k, len(nums))`: `i` is the index of the number **joining** the window; `i - k` is the one **leaving**.
- `window += nums[i] - nums[i - k]` updates in O(1).
- `best = window` at the start (not 0), because with all-negative numbers 0 isn't a real window sum.

**Trace** on `[2, 1, 5, 1, 3, 2]`, k = 3:

| window | joins | leaves | sum | best |
|---|---|---|---|---|
| [2, 1, 5] | | | 8 | 8 |
| [1, 5, 1] | 1 | 2 | 7 | 8 |
| [5, 1, 3] | 3 | 1 | 9 | **9** |
| [1, 3, 2] | 2 | 5 | 6 | 9 |

**Complexity:** O(n) time, O(1) space.
:::

:::exercise Longest substring without repeats
Write `longest_unique(s)` returning the length of the longest substring (a contiguous run of characters) with no repeated character. Make it fast for strings of 200,000 characters.
```python starter
def longest_unique(s):
    pass
```
```python check
test("longest_unique", [
    ("abcabcbb", 3, '"abcabcbb" (abc)'),
    ("bbbbb", 1, "all the same letter"),
    ("pwwkew", 3, '"pwwkew" (wke; "pwke" is not contiguous)'),
    ("", 0, "an empty string"),
    ("a", 1, "one character"),
    ("abcdef", 6, "no repeats at all"),
    ("abba", 2, '"abba" (the window must never move backwards)'),
    ("dvdf", 3, '"dvdf" (vdf)'),
])
def _ref(s):
    last = {}; left = best = 0
    for r, ch in enumerate(s):
        if ch in last and last[ch] >= left: left = last[ch] + 1
        last[ch] = r; best = max(best, r - left + 1)
    return best
speed("longest_unique", lambda n: "".join(chr(0x4E00 + i % 150) for i in range(n)), _ref,
      sizes=(2_000, 40_000, 200_000), what="characters",
      tip="Restarting from every position is O(n²) or worse. Keep one window: move the right end forward, and when a repeat appears move the left end just past it.")
```
```python solution
def longest_unique(s):
    seen = set()
    left = best = 0
    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best
```
```python slow
def longest_unique(s):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i:j + 1])) == j - i + 1:
                best = max(best, j - i + 1)
            else:
                break
    return best
```
hint: Keep a window `s[left:right + 1]` that never contains a repeat, and a set of the characters in it.
hint: Each new character extends the window on the right. If it's already in the set, shrink from the left until it isn't.
hint: For each `right, ch`: `while ch in seen: seen.remove(s[left]); left += 1`, then `seen.add(ch)` and `best = max(best, right - left + 1)`.
approach:
1. **Understand:** substring = contiguous; return a length; empty string → 0.
2. **Examples:** "abcabcbb" → 3; "pwwkew" → 3 ("wke"); "abba" → 2.
3. **Brute force:** for every start, extend until a repeat: O(n²) or O(n³) with set rebuilding.
4. **Pattern:** "longest contiguous … with no repeats" → **variable sliding window** + a **set** of what's inside.
5. **Plan:** grow right; while the new character is already inside, remove from the left; record the window length.
6. **Code and test:** "abba" is the classic trap: make sure `left` only moves forward.
walkthrough:
**Line by line**

- `seen` holds exactly the characters in `s[left:right + 1]`.
- `while ch in seen:` the new character would repeat, so shrink from the left until the old copy is gone. `left` only moves forward.
- `seen.add(ch)` then extends the window.
- `right - left + 1` is the window's length.

**Trace** on `"pwwkew"`:

| right | ch | shrink? | window | best |
|---|---|---|---|---|
| 0 | p | | p | 1 |
| 1 | w | | pw | 2 |
| 2 | w | remove p, w | w | 2 |
| 3 | k | | wk | 2 |
| 4 | e | | wke | 3 |
| 5 | w | remove w | kew | 3 |

**Complexity:** O(n) time (each character is added once and removed at most once), O(k) space for the set, where k is the number of distinct characters.

**Faster variant:** store each character's **last index** in a dict and jump `left` straight past the old copy: `left = max(left, last[ch] + 1)`. The `max` is what makes "abba" work.
:::

:::quiz
? Which problem suits a sliding window?
+ Longest contiguous run of days with rising temperatures
- Sorting a list
- Finding the shortest path in a map
= Contiguous runs are what windows track.
? Why is a variable sliding window O(n) even with a while loop inside the for loop?
+ The left pointer only moves forward, so it moves at most n times in total
- The while loop never runs
- Python optimises it
= Count total pointer moves, not loop nesting.
? When moving a fixed window of size k one step right, the new sum is:
+ old sum + the number that joins − the number that leaves
- old sum + the number that joins
- the sum of the k new numbers, recomputed
= Only two numbers change.
? Why can't "shortest subarray with sum at least target" use this window with negative numbers?
+ Shrinking or growing no longer moves the sum in a predictable direction
- Negative numbers can't be added
- The window would be too big
= The window needs a monotonic rule; with negatives use prefix sums.
:::

@@@ lesson
id: prefix-sums
title: Prefix sums and difference arrays
minutes: 17
summary: Precompute running totals once, then answer any range-sum question in O(1). Difference arrays do the reverse for range updates. Plus the 2-D version.
---
If you'll be asked "what's the sum from index i to j?" many times, adding up the range every time costs O(n) per question. A **prefix sum** array stores the running total, so every range sum becomes **one subtraction**.

![An array 3, 1, 4, 1, 5, 9 with its prefix array 0, 3, 4, 8, 9, 14, 23 underneath. The sum of indexes 2 to 4 (4 + 1 + 5 = 10) equals prefix[5] minus prefix[2] = 14 − 4](figures/prefix-sums.svg)

`prefix[i]` = sum of the first `i` numbers (so `prefix[0] = 0`). Then:

> sum of `nums[i..j]` (inclusive) = `prefix[j + 1] - prefix[i]`

```python
from itertools import accumulate

nums = [3, 1, 4, 1, 5, 9]
prefix = [0]
for x in nums:
    prefix.append(prefix[-1] + x)
print(prefix)

def range_sum(i, j):                 # inclusive i..j, O(1)
    return prefix[j + 1] - prefix[i]

print(range_sum(2, 4), range_sum(0, 5), range_sum(3, 3))
print(list(accumulate(nums, initial=0)))    # the same prefix array in one line
```

Building the prefix array is O(n); each query is O(1). With q queries: O(n + q) instead of O(n·q).

The extra 0 at the front avoids special cases: without it, a range starting at index 0 needs an `if`.

### Pivot index: left sum equals right sum

Prefix sums also give "everything to the left" in O(1). The **pivot index** is where the sum of the numbers to the left equals the sum to the right:

```python
def pivot_index(nums):
    total = sum(nums)
    left = 0
    for i, x in enumerate(nums):
        if left == total - left - x:     # right sum = total - left - the pivot itself
            return i
        left += x
    return -1

print(pivot_index([1, 7, 3, 6, 5, 6]))   # 1 + 7 + 3 = 11 = 5 + 6
```

### Difference arrays: many range updates

The reverse problem: "add 5 to every item from i to j", many times, then read the final array. A **difference array** records only where changes start and stop: `diff[i] += v` and `diff[j + 1] -= v`, O(1) per update. A prefix sum over `diff` at the end rebuilds the array:

```python
from itertools import accumulate

n = 8
diff = [0] * (n + 1)
for i, j, v in [(1, 3, 5), (2, 6, 2), (0, 7, 1)]:    # add v to positions i..j
    diff[i] += v
    diff[j + 1] -= v
print(list(accumulate(diff[:n])))
```

Typical uses: booking systems (how many rooms are taken each night), counting how many intervals cover each point.

### 2-D prefix sums

For a grid, `P[r][c]` = sum of the rectangle from (0, 0) to (r − 1, c − 1). Any rectangle sum then takes four lookups (inclusion–exclusion):

```python
grid = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]
R, C = len(grid), len(grid[0])
P = [[0] * (C + 1) for _ in range(R + 1)]
for r in range(R):
    for c in range(C):
        P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]

def rect_sum(r1, c1, r2, c2):        # inclusive corners
    return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]

print(rect_sum(1, 1, 2, 2))          # 5 + 6 + 8 + 9
```

:::exercise Many range sums
Write `range_sums(nums, queries)` where each query is a pair `(i, j)` (inclusive, `0 <= i <= j < len(nums)`). Return a list with the sum of `nums[i..j]` for each query, in order. It must be fast for 100,000 numbers and 100,000 queries.
```python starter
def range_sums(nums, queries):
    return [sum(nums[i:j + 1]) for i, j in queries]
```
```python check
test("range_sums", [
    (([3, 1, 4, 1, 5, 9], [(2, 4), (0, 5), (3, 3)]), [10, 23, 1], "the example"),
    (([5], [(0, 0)]), [5], "one number"),
    (([1, 2, 3], []), [], "no queries"),
    (([-2, 0, 3, -5, 2, -1], [(0, 2), (2, 5), (0, 5)]), [1, -1, -3], "negative numbers"),
])
def _ref(nums, queries):
    p = [0]
    for x in nums: p.append(p[-1] + x)
    return [p[j + 1] - p[i] for i, j in queries]
import random
def _make(n):
    r = random.Random(n)
    return [r.randint(-1000, 1000) for _ in range(n)], [tuple(sorted((r.randrange(n), r.randrange(n)))) for _ in range(n)]
speed("range_sums", _make, _ref, sizes=(1_000, 15_000, 100_000), what="numbers and queries",
      tip="Summing each range again is O(n) per query. Build a prefix-sum array once, then each query is prefix[j + 1] - prefix[i].")
```
```python solution
def range_sums(nums, queries):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    return [prefix[j + 1] - prefix[i] for i, j in queries]
```
```python slow
def range_sums(nums, queries):
    return [sum(nums[i:j + 1]) for i, j in queries]
```
hint: The starter re-adds every range from scratch. Precompute something once instead.
hint: Build `prefix` where `prefix[k]` is the sum of the first k numbers, starting with `prefix[0] = 0`.
hint: Then the sum of `nums[i..j]` is `prefix[j + 1] - prefix[i]`.
approach:
1. **Understand:** many (i, j) questions about one fixed array; inclusive ranges.
2. **Examples:** `[3, 1, 4, 1, 5, 9]`: (2, 4) → 4 + 1 + 5 = 10.
3. **Brute force:** the starter: sum each slice: O(n) per query, O(n·q) total.
4. **Pattern:** "many range-sum queries on fixed data" → **prefix sums**.
5. **Plan:** build prefix with a leading 0; answer each query with one subtraction.
6. **Code and test:** check a range that starts at 0 (uses `prefix[0] = 0`).
walkthrough:
**Line by line**

- `prefix = [0]`: the sum of the first 0 numbers.
- `prefix.append(prefix[-1] + x)`: each entry is the previous total plus the next number.
- `prefix[j + 1] - prefix[i]`: (sum of the first j + 1 numbers) minus (sum of the first i numbers) leaves exactly `nums[i..j]`.

**Trace** for `nums = [3, 1, 4, 1, 5, 9]`:

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| prefix[k] | 0 | 3 | 4 | 8 | 9 | 14 | 23 |

Query (2, 4): `prefix[5] - prefix[2]` = 14 − 4 = **10**.

**Complexity:** O(n + q) time, O(n) extra space. For 100,000 numbers and queries, that's about 200,000 steps instead of up to 10 billion.
:::

:::exercise Pivot index
Write `pivot_index(nums)` returning the first index where the sum of the numbers strictly to its left equals the sum strictly to its right (an empty side counts as 0), or `-1` if there's none. Make it O(n): fast for 100,000 numbers.
```python starter
def pivot_index(nums):
    pass
```
```python check
test("pivot_index", [
    ([1, 7, 3, 6, 5, 6], 3, "the example"),
    ([1, 2, 3], -1, "no pivot"),
    ([2, 1, -1], 0, "pivot at index 0 (left side is empty)"),
    ([], -1, "an empty list"),
    ([5], 0, "one number (both sides empty)"),
    ([-1, -1, 0, 1, 1, 0], 5, "pivot at the end"),
    ([0, 0, 0], 0, "several pivots: return the first"),
])
def _ref(nums):
    total, left = sum(nums), 0
    for i, x in enumerate(nums):
        if left == total - left - x: return i
        left += x
    return -1
speed("pivot_index", lambda n: [1] * n + [0] if n % 2 else [1] * n, _ref, sizes=(1_000, 10_000, 100_000), what="numbers",
      tip="Calling sum() on both sides at every index is O(n²). Keep a running left sum; the right sum is total - left - nums[i].")
```
```python solution
def pivot_index(nums):
    total = sum(nums)
    left = 0
    for i, x in enumerate(nums):
        if left == total - left - x:
            return i
        left += x
    return -1
```
```python slow
def pivot_index(nums):
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i + 1:]):
            return i
    return -1
```
hint: If you know the total and the sum to the left of i, you can work out the sum to the right without another loop.
hint: right = total − left − nums[i].
hint: `total = sum(nums)`, `left = 0`; for each i: if `left == total - left - nums[i]` return i; then `left += nums[i]`. Return −1.
approach:
1. **Understand:** left side and right side exclude the pivot itself; empty side = 0; first pivot wins.
2. **Examples:** `[1, 7, 3, 6, 5, 6]` → 3 (11 = 11). `[2, 1, -1]` → 0 (left 0, right 1 + −1 = 0).
3. **Brute force:** for each i, sum both sides: O(n²).
4. **Pattern:** **running prefix** + the total.
5. **Plan:** total once; walk with a running left sum; compare before adding the current number.
6. **Code and test:** the order matters: compare **before** `left += x`.
walkthrough:
**Line by line**

- `total = sum(nums)` once: O(n).
- At index i, `left` is the sum of `nums[0..i-1]`, because we add `x` only **after** the comparison.
- `total - left - x` is the right side: everything minus the left part minus the pivot itself.

**Trace** on `[1, 7, 3, 6, 5, 6]` (total 28):

| i | x | left | right = 28 − left − x | equal? |
|---|---|---|---|---|
| 0 | 1 | 0 | 27 | no |
| 1 | 7 | 1 | 20 | no |
| 2 | 3 | 8 | 17 | no |
| 3 | 6 | 11 | 11 | **yes** → 3 |

**Complexity:** O(n) time, O(1) space.
:::

:::quiz
? With `prefix[0] = 0` and `prefix[k]` = sum of the first k numbers, the sum of nums[i..j] inclusive is:
+ prefix[j + 1] − prefix[i]
- prefix[j] − prefix[i]
- prefix[j] + prefix[i]
= The first j + 1 numbers minus the first i numbers.
? What does a prefix-sum array cost to build and to query?
+ O(n) to build, O(1) per query
- O(1) to build, O(n) per query
- O(n log n) to build
= One pass to build, one subtraction per question.
? A difference array makes which operation O(1)?
+ Adding a value to every item in a range
- Finding the maximum
- Sorting
= Mark the start and the end of the change; a final prefix sum applies them all.
? How many lookups does a 2-D prefix sum need for any rectangle sum?
- One
+ Four
- One per cell in the rectangle
= Inclusion–exclusion: add the big rectangle, subtract two strips, add back the doubly subtracted corner.
:::

@@@ lesson
id: matrices
title: 2-D grids and matrices
minutes: 18
summary: Grids as lists of lists, the aliasing trap when creating them, moving to neighbours with direction lists, and classic operations: transpose, rotate, spiral order and searching a sorted matrix.
---
Boards, maps, images and spreadsheets are **grids**: rows and columns. In Python a grid is a list of rows, and `grid[r][c]` is row `r`, column `c`.

![A 3 by 4 grid with rows numbered 0 to 2 and columns 0 to 3. The cell at row 1, column 2 is highlighted, with arrows to its four neighbours: up (row 0), down (row 2), left (column 1) and right (column 3)](figures/grid-neighbours.svg)

```python
grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]
rows, cols = len(grid), len(grid[0])
print(rows, "rows,", cols, "columns")
print("row 1:", grid[1])
print("column 2:", [grid[r][2] for r in range(rows)])
print("cell (1, 2):", grid[1][2])
```

### The aliasing trap

```python
bad = [[0] * 3] * 2           # two references to the SAME row
bad[0][0] = 9
print(bad)                    # both rows changed!

good = [[0] * 3 for _ in range(2)]   # a new row each time
good[0][0] = 9
print(good)
```

`[row] * n` copies the **reference**, not the row. Always build grids with a comprehension.

### Neighbours with a direction list

Instead of four `if` blocks, loop over direction offsets and check the bounds once:

```python
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]     # up, down, left, right

def neighbours(grid, r, c):
    rows, cols = len(grid), len(grid[0])
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

grid = [[1, 2, 3], [4, 5, 6]]
print(list(neighbours(grid, 0, 0)))   # a corner has 2 neighbours
print(list(neighbours(grid, 1, 1)))
```

Add `(-1, -1), (-1, 1), (1, -1), (1, 1)` for 8 directions (diagonals). Grids are really graphs where each cell connects to its neighbours, and BFS/DFS on grids (Lesson 36) builds on this.

### Transpose and rotate

**Transposing** swaps rows and columns: `t[c][r] = grid[r][c]`. **Rotating 90° clockwise** is a transpose followed by reversing each row.

```python
grid = [[1, 2, 3],
        [4, 5, 6]]
transposed = [list(col) for col in zip(*grid)]
print(transposed)
rotated = [row[::-1] for row in transposed]
print(rotated)
```

`zip(*grid)` is a Python idiom: it passes each row as a separate argument, and `zip` groups their first items, their second items, and so on, which are the columns.

### Searching a sorted matrix in O(rows + cols)

If every row and every column is sorted, start at the **top-right** corner. If the value is too big, the whole column below is too big: move left. If too small, the whole row to the left is too small: move down. Each step discards a row or a column.

```python
def search_sorted_matrix(grid, target):
    r, c = 0, len(grid[0]) - 1
    while r < len(grid) and c >= 0:
        v = grid[r][c]
        if v == target:
            return (r, c)
        if v > target:
            c -= 1
        else:
            r += 1
    return None

m = [[1, 4, 7, 11],
     [2, 5, 8, 12],
     [3, 6, 9, 16],
     [10, 13, 14, 17]]
print(search_sorted_matrix(m, 9), search_sorted_matrix(m, 15))
```

:::exercise Rotate 90° clockwise
Write `rotate_90(grid)` that returns a **new** grid rotated 90° clockwise. The grid can be rectangular (R rows by C columns gives C rows by R columns) or empty (`[]` gives `[]`).
```python starter
def rotate_90(grid):
    pass
```
```python check
test("rotate_90", [
    ([[1, 2], [3, 4]], [[3, 1], [4, 2]], "a 2 × 2 grid"),
    ([[1, 2, 3], [4, 5, 6]], [[4, 1], [5, 2], [6, 3]], "a 2 × 3 grid"),
    ([[1, 2, 3]], [[1], [2], [3]], "one row"),
    ([[1], [2], [3]], [[3, 2, 1]], "one column"),
    ([], [], "an empty grid"),
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[7, 4, 1], [8, 5, 2], [9, 6, 3]], "a 3 × 3 grid"),
])
f = need("rotate_90")
g = [[1, 2], [3, 4]]
f(g)
if g != [[1, 2], [3, 4]]:
    raise AssertionError("rotate_90 changed the grid it was given. Return a new grid and leave the input alone.")
```
```python solution
def rotate_90(grid):
    if not grid:
        return []
    rows, cols = len(grid), len(grid[0])
    return [[grid[rows - 1 - r][c] for r in range(rows)] for c in range(cols)]
```
hint: Try it on paper with `[[1, 2, 3], [4, 5, 6]]`. The result has 3 rows of 2. Where does each new row come from?
hint: New row c is old column c, read from the bottom row up.
hint: `[[grid[rows - 1 - r][c] for r in range(rows)] for c in range(cols)]`, or transpose with `zip(*grid)` then reverse each row.
approach:
1. **Understand:** a new grid; R × C becomes C × R; empty → empty; don't change the input.
2. **Examples:** `[[1, 2], [3, 4]]` → `[[3, 1], [4, 2]]`. One row `[[1, 2, 3]]` → a column `[[1], [2], [3]]`.
3. **Brute force:** work out where each cell goes: (r, c) moves to (c, R − 1 − r).
4. **Pattern:** **index mapping**, or **transpose + reverse each row**.
5. **Plan:** for each old column c (top to bottom of the new grid), build a row from the old column read bottom-up.
6. **Code and test:** test a non-square grid; square-only code often breaks there.
walkthrough:
**Line by line**

- `if not grid: return []` avoids `grid[0]` failing on an empty grid.
- The outer comprehension makes one new row per old column `c`.
- The inner part reads that column from the **bottom** row up: `grid[rows - 1 - r][c]` for r = 0, 1, …

**Trace** on `[[1, 2, 3], [4, 5, 6]]` (rows = 2, cols = 3):

| new row (c) | reads grid[1][c], grid[0][c] | result |
|---|---|---|
| 0 | 4, 1 | [4, 1] |
| 1 | 5, 2 | [5, 2] |
| 2 | 6, 3 | [6, 3] |

**Alternative:** `[list(row)[::-1] for row in zip(*grid)]` (transpose, then reverse each row).

**Complexity:** O(R × C) time and space: every cell is copied once. (An in-place rotation is possible for **square** grids by rotating four cells at a time, still O(n²) for n × n.)
:::

:::exercise Spiral order
Write `spiral(grid)` that returns all values in **clockwise spiral order**, starting top-left: across the top row, down the right column, back along the bottom, up the left, then the next ring inwards. Handle rectangular and empty grids.
```python starter
def spiral(grid):
    pass
```
```python check
test("spiral", [
    ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3, 6, 9, 8, 7, 4, 5], "a 3 × 3 grid"),
    ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7], "a 3 × 4 grid"),
    ([[1, 2, 3]], [1, 2, 3], "one row"),
    ([[1], [2], [3]], [1, 2, 3], "one column"),
    ([], [], "an empty grid"),
    ([[1, 2], [3, 4], [5, 6]], [1, 2, 4, 6, 5, 3], "a 3 × 2 grid"),
])
```
```python solution
def spiral(grid):
    out = []
    if not grid:
        return out
    top, bottom = 0, len(grid) - 1
    left, right = 0, len(grid[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):          # top row, left to right
            out.append(grid[top][c])
        top += 1
        for r in range(top, bottom + 1):          # right column, top to bottom
            out.append(grid[r][right])
        right -= 1
        if top <= bottom:                         # bottom row, right to left
            for c in range(right, left - 1, -1):
                out.append(grid[bottom][c])
            bottom -= 1
        if left <= right:                         # left column, bottom to top
            for r in range(bottom, top - 1, -1):
                out.append(grid[r][left])
            left += 1
    return out
```
hint: Keep four boundaries, `top`, `bottom`, `left` and `right`, and shrink them as you finish each side.
hint: One lap: walk the top row and move `top` down; the right column and move `right` left; the bottom row (backwards) and move `bottom` up; the left column (upwards) and move `left` right.
hint: Before the bottom row and the left column, check `top <= bottom` and `left <= right` again, or a single leftover row or column gets added twice.
approach:
1. **Understand:** every value exactly once, in spiral order; rectangular grids allowed.
2. **Examples:** 3 × 3 → 1, 2, 3, 6, 9, 8, 7, 4, 5. A single row or column is just read in order.
3. **Brute force:** walk with a direction and turn when you hit the edge or a visited cell (needs a visited grid). Works, but more bookkeeping.
4. **Pattern:** **shrinking boundaries** (four pointers).
5. **Plan:** while the boundaries haven't crossed: four sides, shrinking one boundary after each.
6. **Code and test:** the 3 × 4 and 3 × 2 grids catch the double-counting bug.
walkthrough:
**Line by line**

- `top, bottom, left, right` describe the ring not yet visited.
- After the top row, `top += 1`: that row is done. Same for the others.
- `if top <= bottom:` before the bottom row: if the top row we just did **was** the last row, there's no separate bottom row left. The same idea with `left <= right` for the left column.

**Trace** on the 3 × 4 grid `[[1,2,3,4],[5,6,7,8],[9,10,11,12]]`:

| side | values | boundaries after |
|---|---|---|
| top | 1 2 3 4 | top = 1 |
| right | 8 12 | right = 2 |
| bottom | 11 10 9 | bottom = 1 |
| left | 5 | left = 1 |
| top (lap 2) | 6 7 | top = 2 |
| right | (none: top > bottom) | right = 1 |
| stop | | top > bottom |

**Complexity:** O(R × C) time (each value once), O(1) extra space besides the output.
:::

:::quiz
? What's wrong with `grid = [[0] * 3] * 2`?
+ Both rows are the same list, so changing one changes the other
- It creates a 3 × 2 grid
- Nothing
= Multiplying a list of lists copies references. Use a comprehension.
? How do you get the columns of a grid as tuples?
+ zip(*grid)
- grid.T
- reversed(grid)
= `*` unpacks the rows as separate arguments to zip.
? Rotating a grid 90° clockwise equals:
+ Transposing, then reversing each row
- Reversing the rows only
- Transposing twice
= Try it on a 2 × 2 example.
? Searching a matrix whose rows and columns are sorted, starting from the top-right corner, costs:
- O(rows × cols)
+ O(rows + cols)
- O(1)
= Each step removes a whole row or a whole column.
:::

@@@ lesson
id: strings
title: Working with strings
minutes: 17
summary: Immutability and efficient building with join, characters and their codes, counting letters, anagrams, reversing words and run-length encoding.
---
Strings are **sequences of characters**: indexing, slicing, `len`, `in` and loops work like lists. The big difference: strings are **immutable**. You can't change a character; every "change" creates a new string.

```python
s = "hello"
try:
    s[0] = "H"
except TypeError as e:
    print("TypeError:", e)
s = "H" + s[1:]           # build a new string instead
print(s)
```

### Building strings efficiently

Because each `+` makes a new string, building a long string piece by piece can cost O(n²) in the worst case. The reliable idiom: collect pieces in a list, `"".join(...)` once.

```python
words = ["data", "structures", "and", "algorithms"]
print(" ".join(words))
print("-".join(w.upper() for w in words))
chars = list("hello")
chars[0] = "j"                     # lists are mutable
print("".join(chars))
```

(CPython sometimes optimises `s += piece` in a loop, but other Pythons don't, and it's an implementation detail. In interviews, use `join`.)

### Characters are numbers underneath

`ord(ch)` gives a character's code number; `chr(n)` goes back. Letters are consecutive, so `ord(ch) - ord("a")` maps "a"–"z" to 0–25, handy for fixed-size count arrays.

```python
print(ord("a"), ord("b"), ord("z"), chr(97))
counts = [0] * 26
for ch in "banana":
    counts[ord(ch) - ord("a")] += 1
print({chr(i + ord("a")): n for i, n in enumerate(counts) if n})
```

### Anagrams: two ways

Two words are **anagrams** if they use the same letters the same number of times.

```python
from collections import Counter

def is_anagram_sort(a, b):          # O(n log n)
    return sorted(a) == sorted(b)

def is_anagram_count(a, b):         # O(n)
    return len(a) == len(b) and Counter(a) == Counter(b)

print(is_anagram_sort("listen", "silent"), is_anagram_count("rat", "car"))
```

### Useful built-ins

| Method | Example | Result |
|---|---|---|
| `split()` | `"  a b  c ".split()` | `['a', 'b', 'c']` (any whitespace) |
| `strip()` | `"  hi ".strip()` | `'hi'` |
| `lower()`, `upper()` | `"Hi".lower()` | `'hi'` |
| `isalnum()`, `isalpha()`, `isdigit()` | `"a1".isalnum()` | `True` |
| `startswith`, `endswith` | `"data".startswith("da")` | `True` |
| `find(sub)` | `"banana".find("an")` | `1` (−1 if missing) |
| `replace(a, b)` | `"a-b".replace("-", " ")` | `'a b'` |
| `s[::-1]` | `"abc"[::-1]` | `'cba'` |

All of these are O(n): they look at the whole string.

:::exercise Run-length encoding
Write `compress(s)` that replaces each run of the same character with the character followed by the run's length: `"aaabcc"` → `"a3b1c2"`. An empty string gives `""`. Build the result with a list and `join`.
```python starter
def compress(s):
    pass
```
```python check
test("compress", [
    ("aaabcc", "a3b1c2", '"aaabcc"'),
    ("", "", "an empty string"),
    ("a", "a1", "one character"),
    ("abc", "a1b1c1", "no repeats"),
    ("zzzzzzzzzzzz", "z12", "a run of 12 (two digits)"),
    ("aabaa", "a2b1a2", "the same letter in separate runs"),
])
```
```python solution
def compress(s):
    if not s:
        return ""
    parts = []
    run_char, run_len = s[0], 1
    for ch in s[1:]:
        if ch == run_char:
            run_len += 1
        else:
            parts.append(run_char + str(run_len))
            run_char, run_len = ch, 1
    parts.append(run_char + str(run_len))       # the last run
    return "".join(parts)
```
hint: Walk through the string keeping the current run's character and its length.
hint: When the character changes, the previous run is finished: add `char + str(length)` to a list and start a new run.
hint: Don't forget the **last** run after the loop ends. Then `return "".join(parts)`.
approach:
1. **Understand:** consecutive equal characters form a run; output char + count for each run, in order.
2. **Examples:** "aaabcc" → "a3b1c2"; "aabaa" → "a2b1a2" (runs, not totals); "zzzzzzzzzzzz" → "z12".
3. **Brute force:** this is already one pass; the care is in the bookkeeping.
4. **Pattern:** **run tracking**: compare each item with the current run.
5. **Plan:** start a run with s[0]; for the rest: same → count up; different → save the run, start a new one; after the loop save the last run.
6. **Code and test:** empty string and one character are the edge cases.
walkthrough:
**Line by line**

- `if not s: return ""` because `s[0]` would fail on an empty string.
- `run_char, run_len = s[0], 1` starts the first run.
- When `ch` differs, the run ended: save it with `str(run_len)` (numbers must become text before joining).
- The final `parts.append(...)` after the loop: the last run never meets a "different" character, so the loop never saves it. Forgetting it is the most common bug.

**Trace** on `"aaabcc"`:

| ch | same as run? | run | parts |
|---|---|---|---|
| (start) | | a×1 | [] |
| a | yes | a×2 | [] |
| a | yes | a×3 | [] |
| b | no | b×1 | [a3] |
| c | no | c×1 | [a3, b1] |
| c | yes | c×2 | [a3, b1] |
| end | | | [a3, b1, c2] |

**Complexity:** O(n) time and space.

**Python shortcut:** `"".join(ch + str(len(list(g))) for ch, g in itertools.groupby(s))`: `groupby` groups consecutive equal items.
:::

:::exercise Reverse the words
Write `reverse_words(s)` that returns the words of `s` in reverse order, separated by single spaces, with no leading or trailing spaces. Words are separated by one or more spaces.
```python starter
def reverse_words(s):
    pass
```
```python check
test("reverse_words", [
    ("the sky is blue", "blue is sky the", "a simple sentence"),
    ("  hello world  ", "world hello", "leading and trailing spaces"),
    ("a good   example", "example good a", "several spaces between words"),
    ("", "", "an empty string"),
    ("   ", "", "only spaces"),
    ("one", "one", "one word"),
])
```
```python solution
def reverse_words(s):
    return " ".join(reversed(s.split()))
```
hint: `split()` with no argument splits on any run of whitespace and ignores spaces at the ends.
hint: Reverse the list of words, then join them with single spaces.
hint: `return " ".join(reversed(s.split()))`.
approach:
1. **Understand:** words, not characters, are reversed; extra spaces disappear.
2. **Examples:** "  hello world  " → "world hello"; "   " → "".
3. **Brute force:** scan characters, collect words manually: fine, but long.
4. **Pattern:** **split → transform → join**, the standard Python string pipeline.
5. **Plan:** `split()`, reverse, `" ".join`.
6. **Code and test:** `split()` (no argument) is the key: `split(" ")` would produce empty strings between double spaces.
walkthrough:
**Line by line**

- `s.split()` with no argument splits on any whitespace and drops empty pieces: `"  a   b "` → `['a', 'b']`.
- `reversed(...)` walks the list backwards without copying.
- `" ".join(...)` puts exactly one space between words.

**Trace** on `"a good   example"`:

| step | value |
|---|---|
| split() | ['a', 'good', 'example'] |
| reversed | example, good, a |
| join | "example good a" |

**Common wrong approach:** `s.split(" ")`. For `"a  b"` it gives `['a', '', 'b']`, so the output gets double spaces.

**Complexity:** O(n) time and space.

**Interview follow-up:** "do it in place with O(1) extra space" (in languages with mutable strings): reverse the whole string, then reverse each word, the same three-reversal idea as rotating an array.
:::

:::quiz
? Why does `s[0] = "H"` fail for a string?
+ Strings are immutable
- Strings can't be indexed
- You must use s.set(0, "H")
= Build a new string instead, e.g. "H" + s[1:].
? What's the reliable way to build a long string from many parts?
+ Append the parts to a list and "".join(parts) once
- Use += in a loop
- Convert to an int
= join builds the result in one O(total length) pass.
? `ord(ch) - ord("a")` is useful because:
+ It maps "a"–"z" to 0–25, so a list of 26 counters can count letters
- It sorts letters
- It removes spaces
= Letters have consecutive codes.
? What does `"  a  b ".split()` return?
+ ['a', 'b']
- ['', '', 'a', '', 'b', '']
- ['a  b']
= split() with no argument splits on runs of whitespace and ignores the ends.
:::

@@@ lesson
id: string-matching
title: Pattern matching: naive, KMP and Rabin-Karp
minutes: 22
summary: Find a pattern inside a text. The O(n·m) naive method, KMP's failure table that never re-reads the text (O(n + m)), and Rabin-Karp's rolling hash.
---
"Does `pattern` occur in `text`, and where?" is behind search boxes, DNA analysis and plagiarism checks. Let n = length of the text and m = length of the pattern.

In everyday Python, `text.find(pattern)` and `pattern in text` are the right tools: they use a highly optimised C implementation. This lesson shows how such algorithms work, because the ideas (never repeating work, rolling hashes) appear in many other problems and interviews.

### 1. Naive: try every position, O(n·m)

```python
def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    hits = []
    for i in range(n - m + 1):              # every possible start
        if text[i:i + m] == pattern:        # compare up to m characters
            hits.append(i)
    return hits

print(naive_search("abracadabra", "abra"))
print(naive_search("aaaaa", "aa"))          # overlapping matches count
```

Worst case (text `"aaaa…ab"`, pattern `"aaab"`): almost every start compares nearly m characters, O(n·m).

### 2. KMP (Knuth–Morris–Pratt): O(n + m)

When the naive method fails partway through a match, it throws away everything it learned and restarts one position later. **KMP** precomputes, for the pattern, the **longest proper prefix that is also a suffix** (the "LPS" or failure table) of every prefix. After a mismatch, it knows how much of the pattern is **already matched** and continues from there, never moving backwards in the text.

![The LPS table for the pattern "ababaca": 0 0 1 2 3 0 1. Under it, a text being matched: after matching "ababa" and failing on the next character, KMP slides the pattern so that its prefix "aba" lines up with the "aba" it just read, instead of starting again from scratch](figures/kmp.svg)

```python
def build_lps(p):
    lps = [0] * len(p)
    length = 0                      # length of the current matching prefix-suffix
    i = 1
    while i < len(p):
        if p[i] == p[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]   # fall back to a shorter prefix-suffix
        else:
            lps[i] = 0
            i += 1
    return lps

def kmp_search(text, pattern):
    if not pattern:
        return list(range(len(text) + 1))
    lps, hits, j = build_lps(pattern), [], 0       # j = characters of the pattern matched
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = lps[j - 1]                         # reuse what's already matched
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            hits.append(i - j + 1)
            j = lps[j - 1]                         # keep going: allows overlaps
    return hits

print(build_lps("ababaca"))
print(kmp_search("abababacabababaca", "ababaca"))
print(kmp_search("aaaaa", "aa"))
```

Cost: building LPS is O(m), the search is O(n). The text pointer `i` never moves back, and `j` can only drop as many times as it has risen, so the total work is linear.

### 3. Rabin-Karp: compare hashes, with a rolling hash

Turn each length-m window of the text into a number (a **hash**) and compare numbers instead of strings. The trick is the **rolling hash**: sliding the window one step updates the hash in O(1) (remove the leaving character's contribution, shift, add the new one), like the sliding window of Lesson 8.

```python
def rabin_karp(text, pattern, base=256, mod=1_000_000_007):
    n, m = len(text), len(pattern)
    if m > n:
        return []
    high = pow(base, m - 1, mod)                    # weight of the leaving character
    hp = ht = 0
    for i in range(m):
        hp = (hp * base + ord(pattern[i])) % mod
        ht = (ht * base + ord(text[i])) % mod
    hits = []
    for i in range(n - m + 1):
        if ht == hp and text[i:i + m] == pattern:   # confirm: different strings can share a hash
            hits.append(i)
        if i + m < n:                                # roll: drop text[i], add text[i + m]
            ht = ((ht - ord(text[i]) * high) * base + ord(text[i + m])) % mod
    return hits

print(rabin_karp("abracadabra", "abra"))
```

Two different strings can have the same hash (a **collision**), so a hash match is double-checked by comparing the strings. With a good large modulus, collisions are rare: O(n + m) on average, O(n·m) in the (very unlikely) worst case. Rabin-Karp shines when searching for **many patterns** of the same length at once: store their hashes in a set.

### Which to use?

| Method | Time | Extra space | Use when |
|---|---|---|---|
| `in`, `str.find` | fast in practice | small | everyday Python |
| Naive | O(n·m) worst | O(1) | tiny inputs, interview warm-up |
| KMP | O(n + m) guaranteed | O(m) | long texts, worst-case guarantees, streaming text |
| Rabin-Karp | O(n + m) average | O(1) | many patterns, plagiarism or duplicate detection |

(Other famous ones: the **Z-algorithm**, similar to KMP; **Boyer–Moore**, which skips ahead using the pattern's last character, used in `grep`; and **Aho–Corasick** for searching many patterns at once.)

:::exercise All occurrences
Write `find_all(text, pattern)` returning a list of every start index where `pattern` occurs in `text`, including **overlapping** occurrences. Assume the pattern isn't empty. Use any method (naive is fine here).
```python starter
def find_all(text, pattern):
    pass
```
```python check
test("find_all", [
    (("abracadabra", "abra"), [0, 7], '"abra" in "abracadabra"'),
    (("aaaaa", "aa"), [0, 1, 2, 3], "overlapping matches"),
    (("hello", "xyz"), [], "no match"),
    (("ab", "abc"), [], "pattern longer than the text"),
    (("abc", "abc"), [0], "the whole text"),
    (("", "a"), [], "an empty text"),
])
```
```python solution
def find_all(text, pattern):
    hits = []
    start = text.find(pattern)
    while start != -1:
        hits.append(start)
        start = text.find(pattern, start + 1)     # +1 (not + len) so overlaps are found
    return hits
```
hint: Try every possible start position i, from 0 to `len(text) - len(pattern)`.
hint: Compare `text[i:i + len(pattern)] == pattern`. Or use `text.find(pattern, start)` repeatedly.
hint: With `find`: after a hit at `start`, search again from `start + 1` (not `start + len(pattern)`), so overlapping matches are found.
approach:
1. **Understand:** every start index, overlaps included; empty result when there's no match.
2. **Examples:** "aaaaa", "aa" → [0, 1, 2, 3].
3. **Brute force:** naive search: every start, compare a slice. O(n·m), fine for these sizes.
4. **Pattern:** a **scan**, or repeated `find` with a moving start.
5. **Plan:** loop over starts (or call find repeatedly), collecting hits.
6. **Code and test:** check the pattern longer than the text (no starts at all).
walkthrough:
**Line by line**

- `text.find(pattern)` returns the first index or −1.
- `text.find(pattern, start + 1)` searches again from just after the previous hit. Jumping by `len(pattern)` would skip overlapping matches like the second "aa" in "aaa".

**Trace** on `("aaaaa", "aa")`:

| search from | found at |
|---|---|
| 0 | 0 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | −1 → stop |

**Complexity:** each `find` is fast in practice; worst case O(n·m) overall. KMP gives a guaranteed O(n + m).
:::

:::exercise Build the KMP table
Write `build_lps(p)` that returns the LPS table: `lps[i]` is the length of the longest **proper** prefix of `p[:i + 1]` that is also a suffix of it ("proper" means not the whole string). For `"ababaca"` it's `[0, 0, 1, 2, 3, 0, 1]`. Aim for O(m).
```python starter
def build_lps(p):
    pass
```
```python check
test("build_lps", [
    ("ababaca", [0, 0, 1, 2, 3, 0, 1], '"ababaca"'),
    ("aaaa", [0, 1, 2, 3], '"aaaa"'),
    ("abcd", [0, 0, 0, 0], "no repeats"),
    ("a", [0], "one character"),
    ("", [], "an empty pattern"),
    ("aabaaab", [0, 1, 0, 1, 2, 2, 3], '"aabaaab" (needs the fall-back step)'),
])
def _ref(p):
    lps = [0] * len(p); k = 0
    for i in range(1, len(p)):
        while k and p[i] != p[k]: k = lps[k - 1]
        if p[i] == p[k]: k += 1
        lps[i] = k
    return lps
speed("build_lps", lambda n: "a" * n + "b", _ref, sizes=(500, 3_000, 100_000), what="characters",
      tip="Checking every prefix against every suffix is O(m²) or worse. Reuse the previous entry: extend the current prefix-suffix, or fall back with length = lps[length - 1].")
```
```python solution
def build_lps(p):
    lps = [0] * len(p)
    length = 0
    for i in range(1, len(p)):
        while length > 0 and p[i] != p[length]:
            length = lps[length - 1]
        if p[i] == p[length]:
            length += 1
        lps[i] = length
    return lps
```
```python slow
def build_lps(p):
    lps = []
    for i in range(len(p)):
        s = p[:i + 1]
        best = 0
        for k in range(1, len(s)):
            if s[:k] == s[-k:]:
                best = k
        lps.append(best)
    return lps
```
hint: `lps[0]` is always 0. Keep `length`, the size of the current matching prefix-suffix, as you move `i` forward.
hint: If `p[i] == p[length]`, the match grows: `length += 1`. If not, don't restart from 0: fall back to `length = lps[length - 1]` and try again.
hint: `for i in 1..m-1: while length and p[i] != p[length]: length = lps[length - 1]`; `if p[i] == p[length]: length += 1`; `lps[i] = length`.
approach:
1. **Understand:** for every prefix of p, the longest proper prefix that is also its suffix.
2. **Examples:** "aaaa" → [0, 1, 2, 3]; "abcd" → all 0; "aabaaab" → [0, 1, 0, 1, 2, 2, 3].
3. **Brute force:** for each i, try every k: O(m²) comparisons of length up to m, O(m³).
4. **Pattern:** **reuse previous answers** (a taste of dynamic programming): the next entry extends or falls back from the current one.
5. **Plan:** length = 0; for i from 1: fall back while mismatched; extend on a match; store.
6. **Code and test:** "aabaaab" tests the fall-back: at i = 5 the match of length 2 breaks and falls back to 1.
walkthrough:
**Line by line**

- `length` = length of the longest prefix of `p` that also ends at position `i - 1`.
- `while length > 0 and p[i] != p[length]: length = lps[length - 1]`: the current prefix-suffix can't be extended, so try the next-longest one, which is `lps[length - 1]`. This is the clever part: no restart from zero.
- `if p[i] == p[length]: length += 1` extends by one character.

**Trace** on `"aabaaab"`:

| i | p[i] | fall-backs | length | lps |
|---|---|---|---|---|
| 1 | a | | 1 | [0, 1] |
| 2 | b | 1 → lps[0] = 0 | 0 | [0, 1, 0] |
| 3 | a | | 1 | [0, 1, 0, 1] |
| 4 | a | | 2 | [0, 1, 0, 1, 2] |
| 5 | a | 2 → lps[1] = 1 | 2 | [0, 1, 0, 1, 2, 2] |
| 6 | b | | 3 | [0, 1, 0, 1, 2, 2, 3] |

**Complexity:** O(m) time: `length` goes up at most once per step and every fall-back lowers it, so the total number of fall-backs is at most m. O(m) space.
:::

:::quiz
? What is the naive pattern search's worst-case time?
- O(n + m)
+ O(n · m)
- O(log n)
= Every start position may compare almost the whole pattern.
? What does KMP's LPS table let it avoid?
+ Re-reading text characters after a mismatch
- Building any table
- Comparing characters
= It knows how much of the pattern is already matched and continues from there.
? Why does Rabin-Karp compare the strings when the hashes match?
+ Different strings can have the same hash (a collision)
- Hashes are always wrong
- To make it slower
= A hash match means "probably equal", so confirm it.
? For everyday Python code, which should you use to find a substring?
+ `pattern in text` or `text.find(pattern)`
- Your own KMP
- Rabin-Karp
= The built-ins are implemented in optimised C.
:::
