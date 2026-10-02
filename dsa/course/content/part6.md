@@@ part
id: 6
title: Searching and Sorting
level: Intermediate
blurb: Binary search and its many disguises (first and last positions, rotated arrays, searching on the answer), the simple and the efficient sorting algorithms with their trade-offs, quickselect, non-comparison sorts, and how to sort anything in Python.

@@@ lesson
id: binary-search
title: Binary search
minutes: 22
summary: Halve the search space at every step: the exact template, bisect, first and last occurrences, insert positions, rotated arrays and peaks, and how to avoid off-by-one bugs.
---
**Linear search** checks items one by one: O(n). If the data is **sorted**, you can do much better. Look at the middle item: if it's too small, the target can only be in the right half; if too big, only in the left half. Each step throws away half of what's left, so a million items need at most 20 steps: **O(log n)**.

![Searching for 23 in the sorted list 2, 5, 8, 12, 16, 23, 38, 56, 72, 91. Step 1: low = 0, high = 9, mid = 4 holds 16, too small, so low moves to 5. Step 2: mid = 7 holds 56, too big, so high moves to 6. Step 3: mid = 5 holds 23: found](figures/binary-search.svg)

### The template

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1          # the target, if present, is in nums[lo..hi]
    while lo <= hi:                     # the range isn't empty
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1                # discard mid and everything left of it
        else:
            hi = mid - 1                # discard mid and everything right of it
    return -1                           # the range became empty: not there

nums = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(nums, 23), binary_search(nums, 7))
```

Three details make or break it:

- **The invariant**: "if the target is anywhere, it's in `nums[lo..hi]`". Every update must keep that true.
- **`lo <= hi`**: with an inclusive range, a single item (lo == hi) must still be checked.
- **`mid + 1` and `mid - 1`**: mid has been checked, so exclude it, otherwise the range can stop shrinking and loop forever.

(In languages with fixed-size integers, `(lo + hi) // 2` can overflow, so people write `lo + (hi - lo) // 2`. Python's integers never overflow, but you'll see that form in other code.)

### Python's bisect module

`bisect_left(a, x)` returns the first position where x could be inserted while keeping `a` sorted, which is the index of the **first** item ≥ x. `bisect_right(a, x)` returns the position **after** the last item ≤ x. Both are binary searches written in C.

```python
from bisect import bisect_left, bisect_right, insort

scores = [10, 20, 20, 20, 30, 40]
print(bisect_left(scores, 20), bisect_right(scores, 20))   # first 20 is at 1; after the last 20 is 4
print("how many 20s:", bisect_right(scores, 20) - bisect_left(scores, 20))
print("items < 25:", bisect_left(scores, 25))

i = bisect_left(scores, 30)
print("30 present?", i < len(scores) and scores[i] == 30)

insort(scores, 25)            # insert keeping the order (O(n), because the list shifts)
print(scores)
```

Common uses: membership in a sorted list, counting items in a range (`bisect_right(a, hi) - bisect_left(a, lo)`), and mapping a value to a band, like a score to a grade:

```python
from bisect import bisect_right

def grade(score, cutoffs=(60, 70, 80, 90), letters="FDCBA"):
    return letters[bisect_right(cutoffs, score)]

print([grade(s) for s in [33, 60, 75, 89, 90, 100]])
```

### First and last occurrence (lower and upper bound)

With duplicates, "find 20" isn't enough: you often need the **first** or **last** 20. Don't stop when you find a match; record it and keep searching to the left (or right).

```python
def first_position(nums, target):
    lo, hi, answer = 0, len(nums) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] >= target:
            if nums[mid] == target:
                answer = mid            # a candidate; an earlier one may exist
            hi = mid - 1                # keep looking left
        else:
            lo = mid + 1
    return answer

print(first_position([10, 20, 20, 20, 30], 20), first_position([10, 30], 20))
```

### Rotated sorted arrays

A sorted list "rotated" at some point, like `[40, 50, 60, 10, 20, 30]`, isn't sorted, but at every mid **one half is**. Check which half is sorted and whether the target lies inside it:

```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                    # the left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                        # the right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

print(search_rotated([40, 50, 60, 10, 20, 30], 20), search_rotated([40, 50, 60, 10, 20, 30], 45))
```

### A peak without sorted data

A **peak** is an item bigger than its neighbours. Even in unsorted data, binary search finds one in O(log n): if `nums[mid] < nums[mid + 1]`, the numbers rise to the right, so a peak must exist on the right side; otherwise one exists at mid or to its left.

```python
def find_peak(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:                       # a half-open style: stop when one candidate remains
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1                 # rising: a peak is to the right
        else:
            hi = mid                     # falling (or flat): mid could be the peak
    return lo

print(find_peak([1, 3, 20, 4, 1, 0]), find_peak([5, 4, 3]), find_peak([1, 2, 3]))
```

The lesson: binary search doesn't need fully sorted data. It needs a test that tells you **which half to keep**.

### Binary search on 2-D sorted matrices

If every row is sorted and each row starts after the previous row ends, the matrix is one sorted list in disguise: index k is row `k // cols`, column `k % cols`.

```python
def search_matrix(matrix, target):
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target:
            return True
        if value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False

m = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
print(search_matrix(m, 16), search_matrix(m, 13))
```

O(log(rows × cols)).

:::exercise Binary search
Write `binary_search(nums, target)` returning the index of `target` in the **sorted** list `nums` (distinct values), or `-1` if it isn't there. Don't use `bisect`, `index` or `in`. It will be called 5,000 times on a list of a million numbers, so each call must be O(log n).
```python starter
def binary_search(nums, target):
    pass

print(binary_search([2, 5, 8, 12, 16, 23, 38], 23))   # 5
```
```python check
if uses("bisect") or uses(".index(") or uses(" in nums"):
    raise AssertionError("Write the halving yourself, without bisect, .index() or `in`.")
test("binary_search", [
    (([2, 5, 8, 12, 16, 23, 38], 23), 5, "the example"),
    (([2, 5, 8, 12, 16, 23, 38], 2), 0, "the first item"),
    (([2, 5, 8, 12, 16, 23, 38], 38), 6, "the last item"),
    (([2, 5, 8, 12, 16, 23, 38], 9), -1, "missing, in the middle"),
    (([2, 5, 8], 1), -1, "smaller than everything"),
    (([2, 5, 8], 99), -1, "bigger than everything"),
    (([7], 7), 0, "one item, found"),
    (([7], 3), -1, "one item, missing"),
    (([], 3), -1, "an empty list"),
])
fn = need("binary_search")
def _bs(nums, t):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == t: return mid
        if nums[mid] < t: lo = mid + 1
        else: hi = mid - 1
    return -1
def _many(nums, queries):
    return [fn(nums, q) for q in queries]
def _ref(nums, queries):
    return [_bs(nums, q) for q in queries]
speed(_many, lambda n: (list(range(0, 3 * n, 3)), [(i * 7919) % (3 * n) for i in range(5_000)]), _ref,
      sizes=(4_000, 1_000_000), what="numbers, searched 5,000 times", factor=10,
      tip="Checking items one by one is O(n) per search. Halve the range each step: compare with the middle item and keep only the half that can contain the target.")
```
```python solution
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1          # the target can only be to the right of mid
        else:
            hi = mid - 1          # the target can only be to the left of mid
    return -1

print(binary_search([2, 5, 8, 12, 16, 23, 38], 23))
```
```python slow
def binary_search(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
```
hint: The list is sorted. After comparing `target` with the middle item, which half can you ignore?
hint: Keep two indexes `lo` and `hi` for the range still possible. Loop while `lo <= hi`, compare with `nums[mid]`, and move `lo` or `hi` past `mid`.
hint: `mid = (lo + hi) // 2`; equal → return mid; `nums[mid] < target` → `lo = mid + 1`; else `hi = mid - 1`. After the loop, return -1.
approach:
1. **Understand:** sorted, distinct values; return an index or −1; many searches on a big list.
2. **Examples:** [2, 5, 8, 12, 16, 23, 38], 23 → 5; 9 → −1; [] → −1.
3. **Brute force:** scan the list: O(n) per search, billions of steps for 5,000 searches of a million items.
4. **Pattern:** sorted + "find" → **binary search**.
5. **Plan:** lo = 0, hi = n − 1; while lo ≤ hi: mid; equal → done; smaller → go right; bigger → go left; return −1.
6. **Code and test:** first item, last item, missing at both ends, one item, empty list.
walkthrough:
**Line by line**

- `lo, hi = 0, len(nums) - 1`: the whole list is possible at the start. For an empty list hi is −1, so the loop never runs and we return −1.
- `while lo <= hi`: the range `lo..hi` still contains at least one item.
- `mid + 1` / `mid - 1` exclude mid after checking it, so the range always shrinks; without that, `lo = mid` could loop forever when lo and hi are next to each other.

**Trace** searching 23 in [2, 5, 8, 12, 16, 23, 38]:

| lo | hi | mid | nums[mid] | action |
|---|---|---|---|---|
| 0 | 6 | 3 | 12 | 12 < 23 → lo = 4 |
| 4 | 6 | 5 | 23 | found → 5 |

Searching 9: lo 0, hi 6, mid 3 (12) → hi = 2; mid 1 (5) → lo = 2; mid 2 (8) → lo = 3 > hi → −1.

**Complexity:** O(log n) time, O(1) space.

**Common wrong approach:** `while lo < hi` with `hi = len(nums) - 1` skips checking the last remaining item, so a target sitting alone in the final range is reported missing.
:::

:::exercise First and last position
Write `search_range(nums, target)` returning `[first, last]`, the first and last indexes of `target` in the sorted list `nums` (which may contain duplicates), or `[-1, -1]` if it's absent. Use two binary searches: O(log n), even when the target appears a million times.
```python starter
def search_range(nums, target):
    pass

print(search_range([5, 7, 7, 8, 8, 10], 8))   # [3, 4]
```
```python check
test("search_range", [
    (([5, 7, 7, 8, 8, 10], 8), [3, 4], "the example"),
    (([5, 7, 7, 8, 8, 10], 6), [-1, -1], "absent"),
    (([], 0), [-1, -1], "an empty list"),
    (([1], 1), [0, 0], "one item"),
    (([2, 2, 2, 2], 2), [0, 3], "every item matches"),
    (([1, 2, 3], 3), [2, 2], "the last item once"),
    (([1, 1, 2], 1), [0, 1], "at the start"),
])
from bisect import bisect_left as _bl, bisect_right as _br
def _ref(nums, t):
    a = _bl(nums, t)
    return [a, _br(nums, t) - 1] if a < len(nums) and nums[a] == t else [-1, -1]
speed("search_range", lambda n: ([0] + [5] * n + [9], 5), _ref, sizes=(1_000, 1_000_000), what="copies of the target", floor=0.05,
      tip="Finding one match and walking left and right is O(n) when the target repeats. Run two binary searches: one that keeps going left after a match, one that keeps going right.")
```
```python solution
def search_range(nums, target):
    def boundary(go_left):
        lo, hi, found = 0, len(nums) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                found = mid                     # record it, then keep searching one side
                if go_left:
                    hi = mid - 1
                else:
                    lo = mid + 1
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return found

    return [boundary(True), boundary(False)]

print(search_range([5, 7, 7, 8, 8, 10], 8))
```
```python slow
def search_range(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            first = last = mid
            while first > 0 and nums[first - 1] == target:
                first -= 1
            while last < len(nums) - 1 and nums[last + 1] == target:
                last += 1
            return [first, last]
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return [-1, -1]
```
hint: A normal binary search stops at **some** match. How could it keep going to find the first one?
hint: When `nums[mid] == target`, record `mid` as a candidate and continue searching the **left** half (`hi = mid - 1`). Do the mirror image for the last position.
hint: Write one helper `boundary(go_left)` that records matches and moves `hi` (for first) or `lo` (for last) past them; return `[boundary(True), boundary(False)]`.
approach:
1. **Understand:** sorted with duplicates; first and last index; [−1, −1] if absent; O(log n) even with huge runs of the target.
2. **Examples:** [5, 7, 7, 8, 8, 10], 8 → [3, 4]; [2, 2, 2, 2], 2 → [0, 3].
3. **Brute force:** find one match and walk outwards: O(n) when the target fills the list.
4. **Pattern:** **lower bound / upper bound** binary search (don't stop at the first match).
5. **Plan:** a helper that, on a match, records it and keeps searching left (or right); call it twice.
6. **Code and test:** absent target, all equal, single item, empty list.
walkthrough:
**Line by line**

- `found` remembers the best match so far; it stays −1 if the target never appears.
- On a match, searching left (`hi = mid - 1`) looks for an earlier copy. If there is none, the loop ends with `found` holding the first index.
- For the last position, the same happens to the right (`lo = mid + 1`).
- Each search halves the range every step: two searches are still O(log n).

**Trace** of the "first" search for 8 in [5, 7, 7, 8, 8, 10]:

| lo | hi | mid | nums[mid] | action | found |
|---|---|---|---|---|---|
| 0 | 5 | 2 | 7 | 7 < 8 → lo = 3 | −1 |
| 3 | 5 | 4 | 8 | match → hi = 3 | 4 |
| 3 | 3 | 3 | 8 | match → hi = 2 | **3** |

**Complexity:** O(log n) time, O(1) space.

**Common wrong approach:** stopping at the first match found and walking outwards one item at a time, which is O(n) for a list full of the target.
:::

:::exercise Search a rotated sorted list
Write `search_rotated(nums, target)` for a list that was sorted (distinct values) and then rotated at some unknown point, like `[4, 5, 6, 7, 0, 1, 2]`. Return the index of `target` or `-1`, in O(log n).
```python starter
def search_rotated(nums, target):
    pass

print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0))   # 4
```
```python check
if uses(".index(") or uses(" in nums"):
    raise AssertionError("Use binary search, not .index() or `in` (they scan the whole list).")
test("search_rotated", [
    (([4, 5, 6, 7, 0, 1, 2], 0), 4, "the example"),
    (([4, 5, 6, 7, 0, 1, 2], 3), -1, "absent"),
    (([4, 5, 6, 7, 0, 1, 2], 4), 0, "the first item"),
    (([4, 5, 6, 7, 0, 1, 2], 2), 6, "the last item"),
    (([1], 0), -1, "one item, absent"),
    (([1], 1), 0, "one item, present"),
    (([1, 2, 3, 4, 5], 4), 3, "not rotated at all"),
    (([5, 1, 3], 5), 0, "rotated by one"),
    (([3, 1], 1), 1, "two items"),
    (([], 1), -1, "an empty list"),
])
fn = need("search_rotated")
def _many(nums, qs):
    return [fn(nums, q) for q in qs]
def _rot(nums, t):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == t: return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= t < nums[mid]: hi = mid - 1
            else: lo = mid + 1
        else:
            if nums[mid] < t <= nums[hi]: lo = mid + 1
            else: hi = mid - 1
    return -1
def _ref(nums, qs):
    return [_rot(nums, q) for q in qs]
speed(_many, lambda n: (list(range(n // 3, n)) + list(range(n // 3)), [(i * 7919) % (n + 5) for i in range(5_000)]), _ref,
      sizes=(4_000, 1_000_000), what="numbers, searched 5,000 times", factor=10,
      tip="Scanning is O(n) per search. At each mid, one half is sorted: check whether the target lies inside that half's range, and keep only the half that can contain it.")
```
```python solution
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                 # left half nums[lo..mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1                      # the target is inside it
            else:
                lo = mid + 1
        else:                                     # right half nums[mid..hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0))
```
```python slow
def search_rotated(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
```
hint: Pick the middle item. Even in a rotated list, at least one of the two halves around it is in sorted order. How can you tell which?
hint: If `nums[lo] <= nums[mid]`, the left half is sorted; otherwise the right half is. In the sorted half you can check with two comparisons whether the target lies inside it.
hint: Left sorted: if `nums[lo] <= target < nums[mid]`, go left (`hi = mid - 1`), else go right. Right sorted: if `nums[mid] < target <= nums[hi]`, go right, else go left.
approach:
1. **Understand:** a rotation of a sorted list; distinct values; O(log n); it might not be rotated at all.
2. **Examples:** [4, 5, 6, 7, 0, 1, 2], 0 → 4; 3 → −1; [1, 2, 3, 4, 5], 4 → 3.
3. **Brute force:** linear scan: O(n).
4. **Pattern:** **modified binary search**: decide which half to keep using the sorted half.
5. **Plan:** loop with lo/hi/mid; return on a match; find the sorted half; keep it if the target's inside its range, else keep the other half.
6. **Code and test:** unrotated input, rotated by one, two items, targets at the ends.
walkthrough:
**Line by line**

- A rotated sorted list consists of two sorted runs. Whatever `mid` is, the half from `lo` to `mid` or the half from `mid` to `hi` lies entirely within one run, so it's sorted.
- `nums[lo] <= nums[mid]` means no "drop" between lo and mid: the left half is sorted. `<=` matters when lo == mid.
- In a sorted half we know the smallest and largest values, so "is the target inside?" is a range check. If yes, keep that half; if not, it must be in the other half.

**Trace** searching 0 in [4, 5, 6, 7, 0, 1, 2]:

| lo | hi | mid | nums[mid] | sorted half | target inside? | action |
|---|---|---|---|---|---|---|
| 0 | 6 | 3 | 7 | left (4..7) | no | lo = 4 |
| 4 | 6 | 5 | 1 | left (0..1) | yes (0 ≤ 0 < 1) | hi = 4 |
| 4 | 4 | 4 | 0 | — | match | return 4 |

**Complexity:** O(log n) time, O(1) space.

**Common wrong approach:** finding the rotation point first with a linear scan and then binary-searching, which is O(n) overall.
:::

:::quiz
? Binary search needs at most how many comparisons for a million sorted items?
- About 1,000
+ About 20
- About 500,000
= Each comparison halves the range: 2^20 is about a million.
? Why must the template use `lo = mid + 1` rather than `lo = mid`?
+ mid has already been checked; excluding it guarantees the range shrinks, otherwise the loop can run forever
- It makes the answer one bigger
- Python indexes start at 1
= With lo = mid, when lo and hi are neighbours, mid equals lo and nothing changes.
? bisect_left([10, 20, 20, 30], 20) returns:
+ 1, the index of the first 20
- 2
- 3
= bisect_left gives the leftmost insertion point, which is the first item >= 20.
? What does binary search really need to work?
+ A test that tells you which half can be thrown away
- Data that is fully sorted, always
- Numbers only
= Rotated arrays and peaks work without full sorting, because each step can still discard half.
:::

@@@ lesson
id: binary-search-answer
title: Binary search on the answer
minutes: 20
summary: When the answer is a number and "is x big enough?" flips from no to yes exactly once, binary search over the possible answers: integer square roots, minimum capacities, eating speeds and real-valued answers.
---
Some problems ask for the **smallest** (or largest) number that satisfies a condition: the smallest ship capacity that delivers everything in 5 days, the slowest eating speed that finishes in time, the biggest number whose square is at most n. There's no sorted list to search, but there is a sorted **range of possible answers**, and a yes/no test that's **monotonic**: once the answer is "yes" for some x, it stays "yes" for every bigger x.

![A number line of possible answers from low to high, coloured by the yes/no test: a run of "no" (too small) followed by a run of "yes". Binary search finds the boundary: the first yes is the answer](figures/answer-search.svg)

Binary search for the **first yes** on that line:

```py-static
lo, hi = smallest_possible, largest_possible
while lo < hi:
    mid = (lo + hi) // 2
    if works(mid):
        hi = mid          # mid works: the answer is mid or smaller
    else:
        lo = mid + 1      # mid fails: the answer is bigger
return lo                 # lo == hi: the first value that works
```

This uses the **half-open** style: `while lo < hi`, `hi = mid` (mid might be the answer, so keep it) and `lo = mid + 1`. When the loop ends, `lo == hi` is the answer. The total cost is O(log(range) × cost of `works`).

### Integer square root

The largest x with x·x ≤ n. Here the test flips from yes to no, so search for the **last yes**, rounding mid **up** so the range always shrinks:

```python
def isqrt(n):
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2      # round up, because we set lo = mid below
        if mid * mid <= n:
            lo = mid                  # mid works: the answer is mid or bigger
        else:
            hi = mid - 1
    return lo

import math
print(isqrt(0), isqrt(15), isqrt(16), isqrt(10**18), math.isqrt(10**18))
```

Rounding: if you write `lo = mid`, use `mid = (lo + hi + 1) // 2`; if you write `hi = mid`, use `mid = (lo + hi) // 2`. Mixing them up loops forever when lo and hi are neighbours.

### Minimum ship capacity

Packages with weights must ship **in order**, within D days. Each day the ship carries packages up to its capacity. What's the smallest capacity that works? A capacity of `max(weights)` is the least that can ever work (the heaviest package must fit); `sum(weights)` always works (everything in one day). Test a capacity by simulating the days greedily:

```python
def days_needed(weights, capacity):
    days, load = 1, 0
    for w in weights:
        if load + w > capacity:       # doesn't fit today: start a new day
            days += 1
            load = 0
        load += w
    return days

def ship_within(weights, days):
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(weights, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo

print(ship_within([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))   # 15
```

O(n · log(sum of weights)). Trying every capacity from max to sum would be O(n · sum).

### Eating bananas at the slowest speed

Piles of bananas; eating at speed k per hour, a pile of p takes ⌈p / k⌉ hours. Find the smallest k that finishes all piles within h hours. Same shape:

```python
def min_eating_speed(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        k = (lo + hi) // 2
        hours = sum((p + k - 1) // k for p in piles)   # ceiling division without floats
        if hours <= h:
            hi = k
        else:
            lo = k + 1
    return lo

print(min_eating_speed([3, 6, 7, 11], 8), min_eating_speed([30, 11, 23, 4, 20], 5))
```

### Minimum of a rotated sorted list

The same "first yes" idea with the test `nums[mid] <= nums[-1]` (mid is in the rotated-to-the-front part, which holds the minimum):

```python
def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1         # the drop (and the minimum) is right of mid
        else:
            hi = mid             # mid could be the minimum
    return nums[lo]

print(find_min([4, 5, 6, 7, 0, 1, 2]), find_min([1, 2, 3]))
```

### Real-valued answers

For an answer that's a real number (a cube root, a time, a rate), repeat a fixed number of times instead of comparing integers: each round halves the error, so 100 rounds shrink even a range of 10¹⁸ to below 10⁻¹².

```python
def cube_root(x):
    lo, hi = 0.0, max(1.0, x)
    for _ in range(100):           # each round halves the interval
        mid = (lo + hi) / 2
        if mid ** 3 < x:
            lo = mid
        else:
            hi = mid
    return lo

print(round(cube_root(27), 9), round(cube_root(2), 9))
```

### Spotting "binary search on the answer"

- The question asks for a **minimum** or **maximum** value (capacity, speed, time, distance, size).
- Checking one candidate value is easy (often a greedy simulation).
- Bigger values are "always at least as good" (monotonic).
- Clue phrases: "minimum largest…", "maximum minimum…", "smallest capacity / speed / time such that…", "within D days".

:::exercise Integer square root
Write `int_sqrt(n)` returning the largest integer x with x · x ≤ n, for 0 ≤ n ≤ 10¹⁸. Don't use `math.sqrt`, `math.isqrt`, `** 0.5` or `pow`: use binary search.
```python starter
def int_sqrt(n):
    pass

print(int_sqrt(15), int_sqrt(16))   # 3 4
```
```python check
import re as _re, math as _math
_code = "\n".join(ln.split("#")[0] for ln in __source__.splitlines())
if _re.search(r"isqrt|(?<![\w])sqrt\s*\(|\*\*|(?<![\w.])pow\s*\(", _code):
    raise AssertionError("Use binary search, without math.sqrt, isqrt, ** or pow.")
test("int_sqrt", [
    (0, 0, "zero"),
    (1, 1, "one"),
    (15, 3, "just below a square"),
    (16, 4, "a perfect square"),
    (17, 4, "just above a square"),
    (2, 1, "two"),
    (99_980_001, 9_999, "eight digits"),
    (10**8, 10**4, "a perfect square, 10^8"),
])
speed("int_sqrt", lambda n: n, lambda n: _math.isqrt(n), sizes=(10**6, 10**14, 10**18 - 1, 10**18), what="as the input", floor=0.2,
      tip="Counting up from 1 takes sqrt(n) steps: a billion for 10^18. Binary search between 0 and n for the last x with x*x <= n.")
```
```python solution
def int_sqrt(n):
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2      # round up because we set lo = mid
        if mid * mid <= n:
            lo = mid                  # mid works; the answer is mid or bigger
        else:
            hi = mid - 1              # mid is too big
    return lo

print(int_sqrt(15), int_sqrt(16))
```
```python slow
def int_sqrt(n):
    x = 0
    while (x + 1) * (x + 1) <= n:
        x += 1
    return x
```
hint: Think of the candidates 0, 1, 2, …, n. For which of them is x · x ≤ n true? Is there a pattern?
hint: It's true for 0 up to the answer, then false for everything bigger: one boundary. Binary search for the **last** true value.
hint: `lo, hi = 0, n`; while `lo < hi`: `mid = (lo + hi + 1) // 2`; if `mid * mid <= n`: `lo = mid` else `hi = mid - 1`. Return `lo`.
approach:
1. **Understand:** floor of the square root; inputs up to 10¹⁸; exact integer arithmetic.
2. **Examples:** 15 → 3, 16 → 4, 0 → 0, 10¹⁸ → 10⁹.
3. **Brute force:** count x upward until (x + 1)² > n: O(√n), a billion steps for 10¹⁸.
4. **Pattern:** **binary search on the answer** with the monotonic test x² ≤ n.
5. **Plan:** search [0, n] for the last x with x² ≤ n, rounding mid up.
6. **Code and test:** 0, 1, perfect squares and their neighbours.
walkthrough:
**Line by line**

- The range `[lo, hi]` always contains the answer: 0 always satisfies 0² ≤ n, and nothing above n can (for n ≥ 1).
- When `mid * mid <= n`, mid is a valid answer, and something bigger might be too, so keep mid: `lo = mid`.
- Otherwise mid is too big: `hi = mid - 1`.
- Rounding mid **up** matters: with lo = 3, hi = 4, rounding down gives mid = 3, and `lo = mid` changes nothing: an infinite loop.
- Python's integers are exact, so `mid * mid` never loses precision, unlike floats (`int(n ** 0.5)` can be off by one for huge n).

**Trace** for n = 15:

| lo | hi | mid | mid² ≤ 15? | action |
|---|---|---|---|---|
| 0 | 15 | 8 | 64: no | hi = 7 |
| 0 | 7 | 4 | 16: no | hi = 3 |
| 0 | 3 | 2 | 4: yes | lo = 2 |
| 2 | 3 | 3 | 9: yes | lo = 3 |
| 3 | 3 | — | — | return 3 |

**Complexity:** O(log n) time (about 60 steps for 10¹⁸), O(1) space.

**Common wrong approach:** `mid = (lo + hi) // 2` together with `lo = mid` loops forever once lo and hi are neighbours.
:::

:::exercise Minimum ship capacity
Write `ship_capacity(weights, days)` returning the smallest ship capacity that delivers every package **in the given order** within `days` days (each day the ship carries a run of consecutive packages whose total weight is at most the capacity). Must be fast when the weights add up to billions.
```python starter
def ship_capacity(weights, days):
    pass

print(ship_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))   # 15
```
```python check
test("ship_capacity", [
    (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15, "the example"),
    (([3, 2, 2, 4, 1, 4], 3), 6, "three days"),
    (([1, 2, 3, 1, 1], 4), 3, "four days"),
    (([10], 1), 10, "one package"),
    (([5, 5, 5], 3), 5, "one package per day"),
    (([5, 5, 5], 1), 15, "everything in one day"),
    (([7, 2, 5, 10, 8], 2), 18, "two days"),
])
def _ref(w, d):
    lo, hi = max(w), sum(w)
    while lo < hi:
        mid = (lo + hi) // 2
        days, load = 1, 0
        for x in w:
            if load + x > mid: days += 1; load = 0
            load += x
        if days <= d: hi = mid
        else: lo = mid + 1
    return lo
speed("ship_capacity", lambda n: ([(i * 7919) % 1_000 + 1 for i in range(2_000)], n), _ref, sizes=(1_000, 250, 2),
      what="days for 2,000 packages",
      tip="Trying capacities one by one is far too slow when weights are large. If a capacity works, every bigger one works too: binary search between max(weights) and sum(weights), testing each candidate with a greedy simulation.")
```
```python solution
def ship_capacity(weights, days):
    def fits(capacity):
        needed, load = 1, 0
        for w in weights:
            if load + w > capacity:      # start a new day
                needed += 1
                load = 0
            load += w
        return needed <= days

    lo, hi = max(weights), sum(weights)  # the answer is somewhere in here
    while lo < hi:
        mid = (lo + hi) // 2
        if fits(mid):
            hi = mid                     # works: try smaller
        else:
            lo = mid + 1                 # too small
    return lo

print(ship_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))
```
```python slow
def ship_capacity(weights, days):
    capacity = max(weights)
    while True:
        needed, load = 1, 0
        for w in weights:
            if load + w > capacity:
                needed += 1
                load = 0
            load += w
        if needed <= days:
            return capacity
        capacity += 1
```
hint: For a given capacity, can you check quickly whether it's enough? And if capacity c is enough, what about c + 1?
hint: Check with a greedy simulation (fill each day until the next package won't fit). Bigger capacities never need more days, so the "enough?" answer flips from no to yes once: binary search for the first yes.
hint: Search between `max(weights)` (the heaviest package must fit) and `sum(weights)` (one day). `while lo < hi: mid; if fits(mid): hi = mid else: lo = mid + 1`.
approach:
1. **Understand:** order is fixed; whole packages only; the smallest capacity that needs at most `days` days.
2. **Examples:** [1..10], 5 days → 15: days [1-5], [6, 7], [8], [9], [10].
3. **Brute force:** try capacities upward from max(weights): O(n × range), hopeless when weights are in the millions.
4. **Pattern:** "smallest X such that it's possible" → **binary search on the answer** + greedy check.
5. **Plan:** `fits(c)` simulates days greedily; binary search the first c in [max, sum] that fits.
6. **Code and test:** one day, one package per day, a single package.
walkthrough:
**Line by line**

- `fits(capacity)` fills each day greedily: putting as much as possible on today never makes a later day worse, so the greedy count is the true minimum number of days for that capacity.
- `lo = max(weights)`: smaller capacities can't carry the heaviest package. `hi = sum(weights)`: everything in one day, always enough.
- Monotonic: if capacity c fits, c + 1 fits too. So "fits" looks like no, no, …, no, yes, yes, …, and we want the first yes.
- `hi = mid` keeps mid (it works and might be the answer); `lo = mid + 1` discards a failing mid.

**Trace** for [1..10], 5 days (lo = 10, hi = 55):

| lo | hi | mid | days needed | fits? |
|---|---|---|---|---|
| 10 | 55 | 32 | 2 | yes → hi = 32 |
| 10 | 32 | 21 | 3 | yes → hi = 21 |
| 10 | 21 | 15 | 5 | yes → hi = 15 |
| 10 | 15 | 12 | 6 | no → lo = 13 |
| 13 | 15 | 14 | 6 | no → lo = 15 → answer 15 |

**Complexity:** O(n · log(sum of weights)) time, O(1) space.

**Common wrong approach:** starting the search at 1 or 0, so the check meets a package heavier than the capacity; the greedy loop then "fits" it anyway and gives a wrong answer.
:::

:::quiz
? Binary search on the answer requires the yes/no test to be:
+ Monotonic: once it's yes for some value, it's yes for every bigger value (or the reverse)
- Fast, but it can flip back and forth
- Based on a sorted list
= A single boundary between no and yes is what binary search finds.
? In the ship problem, why is the lower bound max(weights)?
+ Any smaller capacity can't carry the heaviest package at all
- It's the average weight
- Because binary search must start at the largest item
= The search range must contain the answer and only sensible candidates.
? You write `lo = mid` in your loop. How should mid be computed?
+ (lo + hi + 1) // 2, rounding up
- (lo + hi) // 2, rounding down
- It doesn't matter
= Rounding down with lo = mid can leave the range unchanged forever when lo and hi are neighbours.
? Which question suggests binary search on the answer?
+ "What is the minimum speed that finishes all the work within 8 hours?"
- "Print every permutation of a string"
- "Count the words in a sentence"
= A minimum or maximum value with an easy feasibility check is the classic signal.
:::
EOF
echo ok
@@@ lesson
id: simple-sorts
title: "Simple sorts: bubble, selection, insertion"
minutes: 20
summary: The three O(n²) sorts every programmer should be able to write and explain, what "stable" and "in place" mean, why insertion sort still matters, and the Dutch national flag partition.
---
Python's `sorted()` is all you'll use in practice, but the classic sorting algorithms are where the ideas behind most of DSA come from: invariants, swaps, partitions, divide and conquer, and best versus worst cases. Interviews ask you to write them and, more often, to **compare** them.

Two words describe every sort:

- **In place:** it rearranges the list itself using only O(1) extra memory.
- **Stable:** items that compare equal keep their original order. This matters when you sort records by one field after another (sort by name, then stably by department, and each department stays alphabetical).

### Bubble sort

Walk through the list swapping neighbours that are out of order. After each pass, the largest remaining item has "bubbled" to the end. Stop early if a pass makes no swaps.

```python
def bubble_sort(nums):
    n = len(nums)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                swapped = True
        if not swapped:          # no swaps: already sorted, stop early
            break
    return nums

print(bubble_sort([5, 1, 4, 2, 8]))
```

O(n²) comparisons in the worst case; O(n) on an already sorted list thanks to the early exit. Stable and in place, but slow: mostly a teaching tool.

### Selection sort

Find the smallest remaining item and swap it into the next position.

```python
def selection_sort(nums):
    for i in range(len(nums)):
        smallest = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[smallest]:
                smallest = j
        nums[i], nums[smallest] = nums[smallest], nums[i]
    return nums

print(selection_sort([64, 25, 12, 22, 11]))
```

Always O(n²) comparisons, even on sorted input, but only O(n) **swaps**, which helps when writing is expensive (like flash memory). **Not stable**: the long-distance swap can jump an item over an equal one.

### Insertion sort

Grow a sorted section on the left. Take the next item and slide it left past every bigger item, like sorting a hand of cards.

![Insertion sort on 5, 2, 4, 6, 1, 3. Each row shows one step: the sorted part on the left grows by one item; the new item (orange) slides left past bigger items until it reaches its place](figures/insertion-sort.svg)

```python
def insertion_sort(nums):
    for i in range(1, len(nums)):
        item = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > item:   # shift bigger items one place right
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = item                 # drop the item into the gap
    return nums

print(insertion_sort([5, 2, 4, 6, 1, 3]))
```

O(n²) in the worst case (reverse order), but **O(n) on nearly sorted data**, because each item moves only a few places. It's stable, in place and has tiny overhead, so real-world sorts (Python's Timsort, C++'s introsort) switch to insertion sort for small pieces.

### Comparing them

| Sort | Best | Average | Worst | Extra space | Stable? | Good for |
|---|---|---|---|---|---|---|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | yes | teaching |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | no | few writes |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | yes | small or nearly sorted data |

You can see "nearly sorted" pay off:

```python
import random, time

def insertion_sort(nums):
    for i in range(1, len(nums)):
        item, j = nums[i], i - 1
        while j >= 0 and nums[j] > item:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = item
    return nums

n = 3000
random.seed(1)
shuffled = random.sample(range(n), n)
nearly = list(range(n))
for _ in range(10):                          # swap 10 random neighbours
    i = random.randrange(n - 1)
    nearly[i], nearly[i + 1] = nearly[i + 1], nearly[i]

for name, data in [("shuffled", shuffled), ("nearly sorted", nearly)]:
    t = time.perf_counter()
    insertion_sort(data[:])
    print(f"{name:>14}: {time.perf_counter() - t:.4f} s")
```

### The Dutch national flag: partitioning in one pass

Sorting a list that holds only three values (say 0, 1 and 2) doesn't need a general sort. Edsger Dijkstra's **three-way partition** keeps three regions, 0s at the front, 2s at the back, 1s in the middle, and sorts in one pass with O(1) space. The same partition is the heart of quicksort (next lesson).

```python
def sort_colours(nums):
    low, mid, high = 0, 0, len(nums) - 1     # [0, low) = 0s, [low, mid) = 1s, (high, end] = 2s
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                         # don't move mid: the swapped-in item is unchecked
    return nums

print(sort_colours([2, 0, 2, 1, 1, 0]))
```

:::exercise Insertion sort
Write `insertion_sort(nums)` that sorts the list **in place** using insertion sort and returns it. Don't use `sorted()` or `.sort()`. It must finish quickly on a nearly sorted list of 50,000 numbers (insertion sort's best case).
```python starter
def insertion_sort(nums):
    pass

print(insertion_sort([5, 2, 4, 6, 1, 3]))
```
```python check
if uses("sorted(") or uses(".sort("):
    raise AssertionError("Write the insertion sort yourself, without sorted() or .sort().")
fn = need("insertion_sort")
data = [3, 1, 2]
out = fn(data)
if data != [1, 2, 3]:
    raise AssertionError("Sort the list in place (change `nums` itself), then return it.")
test("insertion_sort", [
    ([5, 2, 4, 6, 1, 3], [1, 2, 3, 4, 5, 6], "the example"),
    ([], [], "an empty list"),
    ([1], [1], "one item"),
    ([1, 2, 3], [1, 2, 3], "already sorted"),
    ([3, 2, 1], [1, 2, 3], "reversed"),
    ([2, 3, 2, 1, 3], [1, 2, 2, 3, 3], "duplicates"),
    ([-1, 5, -10, 0], [-10, -1, 0, 5], "negatives"),
])
def _nearly(n):
    a = list(range(n))
    for i in range(0, n - 1, 97):
        a[i], a[i + 1] = a[i + 1], a[i]
    return a
speed("insertion_sort", _nearly, sorted, sizes=(1_000, 7_000, 50_000), what="nearly sorted numbers", factor=200, floor=0.4,
      tip="On nearly sorted data, insertion sort should do almost no work: shift an item left only while the item before it is bigger, and stop as soon as it isn't.")
```
```python solution
def insertion_sort(nums):
    for i in range(1, len(nums)):
        item = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > item:   # strictly greater: equal items stay in order (stable)
            nums[j + 1] = nums[j]          # shift right to make room
            j -= 1
        nums[j + 1] = item
    return nums

print(insertion_sort([5, 2, 4, 6, 1, 3]))
```
```python slow
def insertion_sort(nums):
    for i in range(1, len(nums)):
        for j in range(i, 0, -1):          # always walks all the way back, even when sorted
            if nums[j - 1] > nums[j]:
                nums[j - 1], nums[j] = nums[j], nums[j - 1]
    return nums
```
hint: Imagine the left part of the list is already sorted. Where does the next item belong?
hint: Remember the item, then shift bigger items one place right until you find a smaller (or equal) one, and drop the item into the gap.
hint: For i from 1: `item = nums[i]; j = i - 1; while j >= 0 and nums[j] > item: nums[j + 1] = nums[j]; j -= 1`; then `nums[j + 1] = item`.
approach:
1. **Understand:** in place, return the list; must be fast on nearly sorted data (so stop shifting early).
2. **Examples:** [5, 2, 4, 6, 1, 3] → [1, 2, 3, 4, 5, 6]; sorted input needs no shifts.
3. **Brute force:** compare every pair: O(n²) always.
4. **Pattern:** **insertion sort**: grow a sorted prefix; shift while bigger.
5. **Plan:** for each i ≥ 1, hold nums[i], shift bigger items right, place it.
6. **Code and test:** empty, one item, reversed, duplicates.
walkthrough:
**Line by line**

- Invariant: before step i, `nums[0..i-1]` is sorted.
- `item = nums[i]` is saved because shifting will overwrite that slot.
- The `while` stops at the first item that isn't bigger; on nearly sorted data that's immediately, so each step costs O(1): O(n) overall.
- `nums[j + 1] = item` puts it right after the first smaller-or-equal item, which keeps equal items in their original order (stable).

**Trace** on [5, 2, 4]:

| i | item | shifts | list after |
|---|---|---|---|
| 1 | 2 | 5 → right | [2, 5, 4] |
| 2 | 4 | 5 → right; stop at 2 | [2, 4, 5] |

**Complexity:** O(n²) worst case (reversed input), O(n) best case (sorted or nearly sorted), O(1) extra space.

**Common wrong approach:** an inner loop that always runs back to index 0 (the "slow" version) loses the early stop, so even sorted input takes O(n²).
:::

:::exercise Sort the colours
Write `sort_colours(nums)` for a list containing only `0`, `1` and `2`. Sort it **in place in one pass** with O(1) extra space (no counting and rewriting, no `sorted`), and return it.
```python starter
def sort_colours(nums):
    pass

print(sort_colours([2, 0, 2, 1, 1, 0]))   # [0, 0, 1, 1, 2, 2]
```
```python check
if uses("sorted(") or uses(".sort(") or uses(".count("):
    raise AssertionError("Do it in one pass with three pointers, without sorting or counting.")
fn = need("sort_colours")
data = [2, 1, 0]
fn(data)
if data != [0, 1, 2]:
    raise AssertionError("Sort `nums` in place (swap inside the list), then return it.")
test("sort_colours", [
    ([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2], "the example"),
    ([2, 0, 1], [0, 1, 2], "one of each"),
    ([0], [0], "one item"),
    ([], [], "empty"),
    ([2, 2, 2], [2, 2, 2], "all twos"),
    ([1, 0], [0, 1], "two items"),
    ([2, 0, 0, 2, 1, 2, 0], [0, 0, 0, 1, 2, 2, 2], "mixed"),
])
```
```python solution
def sort_colours(nums):
    low, mid, high = 0, 0, len(nums) - 1
    # nums[:low] are 0s, nums[low:mid] are 1s, nums[high+1:] are 2s, nums[mid:high+1] unknown
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                 # the item swapped in from high hasn't been checked yet
    return nums

print(sort_colours([2, 0, 2, 1, 1, 0]))
```
hint: Keep three regions: 0s at the front, 2s at the back, 1s in between, and an unknown middle part that shrinks.
hint: Use three pointers: `low` (next place for a 0), `mid` (the item being checked) and `high` (next place for a 2).
hint: While `mid <= high`: a 0 → swap with `low`, move both low and mid; a 1 → move mid; a 2 → swap with `high`, move high only (re-check the new item at mid).
approach:
1. **Understand:** only 0, 1, 2; in place; one pass; O(1) space.
2. **Examples:** [2, 0, 2, 1, 1, 0] → [0, 0, 1, 1, 2, 2].
3. **Brute force:** count each value and rewrite the list: two passes (allowed in real life, banned here), or sort: O(n log n).
4. **Pattern:** **three-way partition** with three pointers (Dutch national flag).
5. **Plan:** low/mid/high; inspect nums[mid]; swap 0s to the front and 2s to the back.
6. **Code and test:** all equal, two items, empty.
walkthrough:
**Line by line**

- The invariant is in the comment: four regions, and the unknown one (`mid..high`) shrinks every step.
- A 0 at `mid` swaps with `low`. The item coming back from `low` is a 1 (or it's the same slot), so `mid` can move on safely.
- A 2 swaps with `high`, but the item that comes from `high` hasn't been looked at, so `mid` stays to check it next.
- The loop ends when the unknown region is empty (`mid > high`).

**Trace** on [2, 0, 1]:

| low | mid | high | nums | action |
|---|---|---|---|---|
| 0 | 0 | 2 | [2, 0, 1] | 2: swap with high → [1, 0, 2], high = 1 |
| 0 | 0 | 1 | [1, 0, 2] | 1: mid = 1 |
| 0 | 1 | 1 | [1, 0, 2] | 0: swap with low → [0, 1, 2], low = 1, mid = 2 |

**Complexity:** O(n) time, one pass; O(1) space.

**Common wrong approach:** moving `mid` forward after swapping with `high`, which leaves an unchecked 0 or 2 in the middle.
:::

:::quiz
? Which sort is fastest on a nearly sorted list?
+ Insertion sort: each item only moves a few places, so it's close to O(n)
- Selection sort
- They're all O(n²) on any input
= Insertion sort stops shifting as soon as the item is in place.
? What does "stable" mean for a sorting algorithm?
+ Items that compare equal keep their original relative order
- It never crashes
- It uses O(1) extra memory
= Stability matters when sorting records by one key after another.
? Why isn't selection sort stable?
+ Its long-distance swap can move an item past another item equal to it
- It sorts in reverse
- It uses recursion
= For example [2a, 2b, 1]: swapping 1 with 2a puts 2a after 2b.
? In the Dutch flag partition, why doesn't mid move after swapping with high?
+ The item swapped in from the end hasn't been checked yet
- Because mid always stays at 0
- It would skip a 1
= It could be a 0 or a 2 and still needs to be placed.
:::

@@@ lesson
id: efficient-sorts
title: "Efficient sorts: merge, quick and heap sort, quickselect"
minutes: 24
summary: The O(n log n) sorts and their trade-offs: merge sort (stable, extra memory), quicksort (in place, fast, bad pivots), heap sort (guaranteed, in place), and quickselect for the k-th smallest in O(n) on average.
---
The simple sorts compare each item with many others: O(n²). The efficient sorts use divide and conquer, or a heap, to get down to **O(n log n)**: for a million items that's about 20 million steps instead of a trillion.

### Merge sort (recap)

You wrote it in Lesson 22: split in halves, sort each recursively, merge. Its strengths and weaknesses:

- **Always O(n log n)**, whatever the input.
- **Stable**, which is why Python's `sorted()` (Timsort) is built from merges.
- Needs **O(n) extra memory** for merging.
- Works well on data that doesn't fit in memory (**external sorting**: sort chunks, then merge the sorted chunk files), and on linked lists, where merging needs no extra array.

### Quicksort

Pick a **pivot**, **partition** the list so smaller items are on its left and bigger ones on its right (the pivot is then in its final place), and sort the two sides recursively. No merge step is needed.

![Partitioning [7, 2, 1, 8, 6, 3, 5, 4] around the pivot 4 (Lomuto scheme). The pointer i marks the end of the "smaller than the pivot" region; j scans left to right, swapping smaller items into that region. Finally the pivot swaps into position 3, with 2, 1, 3 on its left and 8, 6, 7, 5 on its right](figures/quick-partition.svg)

```python
import random

def quicksort(nums, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo >= hi:
        return nums
    p = random.randint(lo, hi)                 # a random pivot avoids the worst case on sorted input
    nums[p], nums[hi] = nums[hi], nums[p]
    pivot, i = nums[hi], lo
    for j in range(lo, hi):                    # Lomuto partition
        if nums[j] < pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    nums[i], nums[hi] = nums[hi], nums[i]      # the pivot lands in its final position i
    quicksort(nums, lo, i - 1)
    quicksort(nums, i + 1, hi)
    return nums

random.seed(0)
print(quicksort([7, 2, 1, 8, 6, 3, 5, 4]))
```

- **Average O(n log n)**, and in practice often the fastest comparison sort: it works in place and moves through memory in order, which CPUs like.
- **Worst case O(n²)**: if the pivot is always the smallest or largest item (for example, always taking the first item of an already sorted list), each partition removes just one item. A **random pivot** (or "median of three") makes that astronomically unlikely.
- **In place**: O(log n) extra space for the recursion on average.
- **Not stable**.
- Many equal keys? A three-way partition (the Dutch flag from last lesson) groups all items equal to the pivot in one pass, so lists full of duplicates stay fast.

### Heap sort

Build a **max-heap** (Lesson 32) inside the list, then repeatedly swap the largest item to the end and restore the heap on the rest.

```python
def heap_sort(nums):
    n = len(nums)

    def sift_down(start, end):            # push nums[start] down until both children are smaller
        root = start
        while 2 * root + 1 < end:
            child = 2 * root + 1
            if child + 1 < end and nums[child + 1] > nums[child]:
                child += 1                # the bigger child
            if nums[root] >= nums[child]:
                return
            nums[root], nums[child] = nums[child], nums[root]
            root = child

    for start in range(n // 2 - 1, -1, -1):   # build the max-heap: O(n)
        sift_down(start, n)
    for end in range(n - 1, 0, -1):           # move the max to the end, shrink the heap
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(0, end)
    return nums

print(heap_sort([12, 11, 13, 5, 6, 7]))
```

**Guaranteed O(n log n)** and **in place** (O(1) extra space), but not stable and usually slower than quicksort in practice because it jumps around memory. Introsort (C++'s `std::sort`) starts with quicksort and switches to heap sort if the recursion gets suspiciously deep, getting quicksort's speed with heap sort's guarantee.

### Quickselect: the k-th smallest without sorting

To find the median or the k-th smallest item you don't need everything sorted. Partition once: if the pivot lands at position k, done; otherwise recurse into **only the side** that contains position k. On average the sizes go n + n/2 + n/4 + … = 2n: **O(n)** average (O(n²) worst case, made unlikely by a random pivot).

```python
import random

def kth_smallest(nums, k):                 # k is 1-based: k = 1 is the minimum
    nums = list(nums)
    target = k - 1
    lo, hi = 0, len(nums) - 1
    while True:
        p = random.randint(lo, hi)
        nums[p], nums[hi] = nums[hi], nums[p]
        pivot, i = nums[hi], lo
        for j in range(lo, hi):
            if nums[j] < pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        if i == target:
            return nums[i]
        if i < target:
            lo = i + 1                     # the answer is on the right
        else:
            hi = i - 1                     # the answer is on the left

random.seed(2)
print(kth_smallest([7, 10, 4, 3, 20, 15], 3), kth_smallest([7, 10, 4, 3, 20, 15], 1))
```

`heapq.nsmallest(k, nums)` and `heapq.nlargest(k, nums)` give the k smallest or largest in O(n log k), often the simplest choice (Lesson 32).

### Choosing an O(n log n) sort

| | Merge sort | Quicksort | Heap sort |
|---|---|---|---|
| Average | O(n log n) | O(n log n) | O(n log n) |
| Worst | O(n log n) | O(n²) (rare with a random pivot) | O(n log n) |
| Extra space | O(n) | O(log n) | O(1) |
| Stable | yes | no | no |
| In practice | linked lists, external sorting, Timsort | fastest general in-memory sort | guaranteed bound, little memory |

:::exercise Quicksort
Write `quick_sort(nums)` that sorts the list **in place** with quicksort (partition around a pivot, recurse on both sides) and returns it. Don't use `sorted()`, `.sort()` or `heapq`. It must handle 50,000 numbers that are **already sorted**, where a "first item" pivot breaks down.
```python starter
import random

def quick_sort(nums):
    pass

print(quick_sort([7, 2, 1, 8, 6, 3, 5, 4]))
```
```python check
if uses("sorted(") or uses(".sort(") or uses("heapq"):
    raise AssertionError("Write quicksort yourself, without sorted(), .sort() or heapq.")
fn = need("quick_sort")
data = [3, 1, 2]
fn(data)
if data != [1, 2, 3]:
    raise AssertionError("Sort `nums` in place (rearrange the list itself), then return it.")
test("quick_sort", [
    ([7, 2, 1, 8, 6, 3, 5, 4], [1, 2, 3, 4, 5, 6, 7, 8], "the example"),
    ([], [], "empty"),
    ([1], [1], "one item"),
    ([2, 1], [1, 2], "two items"),
    ([5, 5, 5, 5], [5, 5, 5, 5], "all equal"),
    ([3, -1, 3, 0, -1], [-1, -1, 0, 3, 3], "duplicates and negatives"),
    (list(range(20, 0, -1)), list(range(1, 21)), "reversed"),
])
speed("quick_sort", lambda n: list(range(n)), sorted, sizes=(1_000, 50_000), what="already sorted numbers", factor=400, floor=0.8,
      tip="With the first (or last) item as the pivot, sorted input splits into sizes 0 and n - 1 every time: O(n^2) and very deep recursion. Pick a random pivot (swap it to the end first).")
```
```python solution
import random

def quick_sort(nums):
    def sort(lo, hi):
        while lo < hi:
            p = random.randint(lo, hi)              # random pivot, moved to the end
            nums[p], nums[hi] = nums[hi], nums[p]
            pivot, i = nums[hi], lo
            for j in range(lo, hi):
                if nums[j] < pivot:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
            nums[i], nums[hi] = nums[hi], nums[i]   # pivot in its final place
            if i - lo < hi - i:                     # recurse on the smaller side,
                sort(lo, i - 1)                     # loop on the bigger one: depth O(log n)
                lo = i + 1
            else:
                sort(i + 1, hi)
                hi = i - 1

    sort(0, len(nums) - 1)
    return nums

print(quick_sort([7, 2, 1, 8, 6, 3, 5, 4]))
```
```python slow
def quick_sort(nums):
    def sort(lo, hi):
        if lo >= hi:
            return
        pivot, i = nums[hi], lo              # always the last item: sorted input is the worst case
        for j in range(lo, hi):
            if nums[j] < pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        sort(lo, i - 1)
        sort(i + 1, hi)

    sort(0, len(nums) - 1)
    return nums
```
hint: Partition: choose a pivot, move smaller items to its left and bigger ones to its right. Then the two sides are independent, smaller problems.
hint: Lomuto partition: put the pivot at `hi`; keep `i` as the next slot for a smaller item; for each j in `lo..hi-1`, if `nums[j] < pivot`, swap it to `i` and move `i`. Finally swap the pivot into `i`.
hint: Use `random.randint(lo, hi)` for the pivot and swap it to `hi` first. To keep recursion shallow, recurse on the smaller side and loop on the bigger one.
approach:
1. **Understand:** in place; return the list; must survive sorted input of 50,000 items.
2. **Examples:** [7, 2, 1, 8, 6, 3, 5, 4] → [1..8]; [5, 5, 5, 5] stays.
3. **Brute force:** a simple O(n²) sort is far too slow for 50,000 items.
4. **Pattern:** **divide and conquer by partitioning**, with a **random pivot**.
5. **Plan:** helper sort(lo, hi); random pivot to hi; Lomuto partition; recurse on both sides.
6. **Code and test:** empty, duplicates, already sorted, reversed.
walkthrough:
**Line by line**

- A random pivot makes the "always the smallest" split astronomically unlikely, whatever order the input is in.
- After the partition loop, `nums[lo:i]` are smaller than the pivot and `nums[i:hi]` are not; swapping the pivot into `i` puts it exactly where it belongs in the sorted list. It never moves again.
- Recursing on the smaller side and looping on the bigger one (a manual tail-call) keeps the recursion depth O(log n), so Python's recursion limit is never a problem, even with unlucky pivots.

**Trace** of one partition on [7, 2, 1, 8, 6, 3, 5, 4] with pivot 4 at the end:

| j | nums[j] | < 4? | i after | list |
|---|---|---|---|---|
| 0 | 7 | no | 0 | |
| 1 | 2 | yes, swap with 7 | 1 | [2, 7, 1, …] |
| 2 | 1 | yes, swap with 7 | 2 | [2, 1, 7, …] |
| 3–4 | 8, 6 | no | 2 | |
| 5 | 3 | yes, swap with 7 | 3 | [2, 1, 3, 8, 6, 7, 5, 4] |
| 6 | 5 | no | 3 | |
| end | | pivot ↔ position 3 | | [2, 1, 3, **4**, 6, 7, 5, 8] |

**Complexity:** O(n log n) average time, O(n²) worst case (very unlikely with random pivots); O(log n) stack space.

**Common wrong approach:** always taking the first or last item as the pivot. On sorted input every partition is lopsided, so it's O(n²) and the recursion goes n levels deep (a RecursionError in Python).
:::

:::exercise K-th smallest with quickselect
Write `kth_smallest(nums, k)` returning the k-th smallest number (k = 1 is the minimum) using **quickselect**: partition, then continue on one side only. Don't sort (no `sorted`, `.sort` or `heapq`). Must handle 300,000 numbers.
```python starter
import random

def kth_smallest(nums, k):
    pass

print(kth_smallest([7, 10, 4, 3, 20, 15], 3))   # 7
```
```python check
if uses("sorted(") or uses(".sort(") or uses("heapq"):
    raise AssertionError("Use quickselect (partition and keep one side), without sorting or heapq.")
test("kth_smallest", [
    (([7, 10, 4, 3, 20, 15], 3), 7, "the example"),
    (([7, 10, 4, 3, 20, 15], 1), 3, "the minimum"),
    (([7, 10, 4, 3, 20, 15], 6), 20, "the maximum"),
    (([5], 1), 5, "one number"),
    (([2, 1, 2, 1, 2], 3), 2, "duplicates"),
    (([-5, -1, -9], 2), -5, "negatives"),
    ((list(range(100, 0, -1)), 50), 50, "reversed"),
])
speed("kth_smallest", lambda n: ([(i * 7919) % 1_000_003 for i in range(n)], n // 2), lambda a, k: sorted(a)[k - 1],
      sizes=(1_000, 10_000, 300_000), what="numbers", factor=60, floor=0.3,
      tip="Partition around a random pivot, then continue only into the side that contains position k - 1 (a loop with lo and hi works well). Repeatedly finding and removing the minimum is O(n * k).")
```
```python solution
import random

def kth_smallest(nums, k):
    nums = list(nums)                       # work on a copy
    target = k - 1                          # 0-based position we want
    lo, hi = 0, len(nums) - 1
    while True:
        p = random.randint(lo, hi)
        nums[p], nums[hi] = nums[hi], nums[p]
        pivot, i = nums[hi], lo
        for j in range(lo, hi):
            if nums[j] < pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        if i == target:
            return nums[i]
        if i < target:
            lo = i + 1                      # only the right side can contain it
        else:
            hi = i - 1                      # only the left side can contain it

print(kth_smallest([7, 10, 4, 3, 20, 15], 3))
```
```python slow
def kth_smallest(nums, k):
    nums = list(nums)
    for _ in range(k - 1):
        nums.remove(min(nums))
    return min(nums)
```
hint: After one partition, the pivot sits at its final sorted position i. Compare i with k − 1: what does that tell you?
hint: If i == k − 1, the pivot is the answer. If i < k − 1, the answer is to the right; otherwise to the left. You never need the other side.
hint: Loop with `lo` and `hi`: random pivot to `hi`, Lomuto partition, then return `nums[i]` or move `lo = i + 1` / `hi = i - 1`. Copy the list first if you don't want to change the caller's list.
approach:
1. **Understand:** 1-based k; duplicates allowed; O(n) average required for 300,000 numbers.
2. **Examples:** [7, 10, 4, 3, 20, 15], k = 3 → 7 (sorted: 3, 4, 7, 10, 15, 20).
3. **Brute force:** sort and index: O(n log n) (fine in real life, but banned here); removing the minimum k times: O(n·k).
4. **Pattern:** **quickselect**: quicksort's partition, but recurse into one side only.
5. **Plan:** loop: random pivot, partition, compare its position with k − 1, shrink to one side.
6. **Code and test:** k = 1, k = n, duplicates.
walkthrough:
**Line by line**

- The partition is identical to quicksort's: the pivot ends at index `i`, with smaller items before it.
- So the pivot is the (i + 1)-th smallest. If that's what we want, we're done.
- Otherwise, only one side can contain the answer, and the other side is dropped entirely. That's the difference from quicksort, which recurses into both sides.
- On average each round keeps about half, so the work is n + n/2 + n/4 + … ≈ 2n: O(n).
- Duplicates are fine: items equal to the pivot go to the right side, and the position checks still hold.

**Trace** for [7, 10, 4, 3, 20, 15], k = 3 (target index 2), supposing the pivot chosen is 10:

| step | partition result | pivot index | action |
|---|---|---|---|
| 1 | [7, 4, 3, **10**, 20, 15] | 3 | 3 > 2 → keep the left side 0..2 |
| 2 | pivot 4: [3, **4**, 7] | 1 | 1 < 2 → keep the right side 2..2 |
| 3 | pivot 7 | 2 | found: 7 |

**Complexity:** O(n) average, O(n²) worst case (unlikely with a random pivot), O(1) extra space besides the copy.

**Common wrong approach:** recursing into both sides, which turns it back into a full O(n log n) quicksort.
:::

:::quiz
? Which sort is stable and always O(n log n), but needs O(n) extra memory?
+ Merge sort
- Quicksort
- Heap sort
= Merging needs a temporary array; in exchange, it never degrades and keeps equal items in order.
? When does quicksort with "first item as pivot" hit O(n²)?
+ On already sorted (or reversed) input, where each partition removes only one item
- On random input
- When the list has negative numbers
= A random pivot avoids this pattern.
? Quickselect is faster on average than sorting because:
+ After each partition it continues into only one side
- It doesn't compare numbers
- It uses a heap
= n + n/2 + n/4 + ... adds up to about 2n.
? Which O(n log n) sort uses O(1) extra space and has no bad worst case?
+ Heap sort
- Merge sort
- Quicksort
= It sorts inside the array using a heap, guaranteed O(n log n).
:::

@@@ lesson
id: sorting-in-practice
title: "Non-comparison sorts and sorting in practice"
minutes: 20
summary: Counting, radix and bucket sort beat O(n log n) by not comparing; why comparison sorts can't; and how to sort anything in Python with sorted, key functions, multiple keys and cmp_to_key.
---
### Why comparison sorts can't beat n log n

A sort that only learns about the data by comparing pairs ("is a < b?") is like a game of twenty questions: each comparison has two outcomes, and it must tell apart all n! possible orderings of the input. With k comparisons you can distinguish at most 2ᵏ cases, so you need 2ᵏ ≥ n!, which works out to k ≥ log₂(n!) ≈ n log₂ n. So **every comparison sort needs Ω(n log n) comparisons** in the worst case. Merge sort and heap sort are optimal.

To go faster, you must use more than comparisons: the **values themselves**.

### Counting sort

If the values are small integers (ages, grades, digits), count how many times each value appears, then write them back in order. O(n + k) for values from 0 to k − 1.

![Counting sort on [4, 2, 2, 8, 3, 3, 1]: a count array indexed 0 to 8 holds how many times each value appears (1 → 1, 2 → 2, 3 → 2, 4 → 1, 8 → 1); reading the counts in order writes 1, 2, 2, 3, 3, 4, 8](figures/counting-sort.svg)

```python
def counting_sort(nums, max_value):
    counts = [0] * (max_value + 1)
    for x in nums:
        counts[x] += 1
    out = []
    for value, c in enumerate(counts):
        out.extend([value] * c)
    return out

print(counting_sort([4, 2, 2, 8, 3, 3, 1], 8))
```

It's only worth it when the range k isn't much bigger than n: sorting 10 numbers between 0 and a billion would need a billion counters. To sort **records** by a small key stably, turn the counts into starting positions (prefix sums) and place each record there; that stable version is what radix sort uses.

### Radix sort

Sort numbers digit by digit, from the **least significant** digit, using a stable sort for each digit. After processing the last digit, everything is in order. O(d · (n + b)) for d digits in base b: for fixed-size integers (like 32-bit IDs) that's linear in n.

```python
def radix_sort(nums):
    if not nums:
        return []
    place = 1
    while max(nums) // place > 0:
        buckets = [[] for _ in range(10)]      # one bucket per digit 0..9
        for x in nums:
            buckets[(x // place) % 10].append(x)   # appending keeps it stable
        nums = [x for b in buckets for x in b]
        place *= 10
    return nums

print(radix_sort([170, 45, 75, 90, 802, 24, 2, 66]))
```

### Bucket sort

For values spread evenly over a range (like random decimals between 0 and 1), drop each into one of n buckets by value, sort each small bucket, and concatenate: O(n) on average, O(n²) if everything lands in one bucket.

```python
def bucket_sort(values):
    n = len(values)
    buckets = [[] for _ in range(n)]
    for v in values:                       # 0 <= v < 1
        buckets[int(v * n)].append(v)
    return [v for b in buckets for v in sorted(b)]

print(bucket_sort([0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]))
```

### How Python sorts: Timsort

`sorted()` and `list.sort()` use **Timsort** (since Python 3.11, with an improved "powersort" merge policy). It finds runs that are already in order, extends short runs with insertion sort, and merges runs like merge sort. Result: O(n log n) worst case, **O(n) on already sorted or nearly sorted data**, and **stable**. It's written in C, so a hand-written sort in Python is never faster for real work.

```python
words = ["banana", "Apple", "cherry", "apple"]
print(sorted(words))                      # by Unicode: capitals come first
print(sorted(words, key=str.lower))       # case-insensitive
print(sorted(words, key=len, reverse=True))

nums = [3, 1, 2]
nums.sort()                               # sorts in place, returns None
print(nums)
```

### Sorting by several keys

A `key` function can return a **tuple**: Python compares tuples item by item, so the first item is the main key and later items break ties. To reverse just one numeric key, negate it.

```python
people = [("Ana", "Sales", 52_000), ("Ben", "IT", 61_000), ("Cy", "Sales", 61_000), ("Dee", "IT", 58_000)]

by_dept_then_salary_desc = sorted(people, key=lambda p: (p[1], -p[2]))
for p in by_dept_then_salary_desc:
    print(p)
```

For keys you can't negate (like strings descending), use **stability**: sort by the secondary key first, then stably by the primary key.

```python
people = [("Ana", "Sales"), ("Ben", "IT"), ("Cy", "Sales"), ("Dee", "IT")]
step1 = sorted(people, key=lambda p: p[0], reverse=True)   # secondary: name, Z to A
step2 = sorted(step1, key=lambda p: p[1])                  # primary: department; ties keep step 1's order
print(step2)
```

### Custom comparisons: cmp_to_key

Sometimes the order is defined by comparing two items directly. The classic: arrange numbers to form the **largest number** ([3, 30, 34, 5, 9] → "9534330"). Put a before b if the string `a + b` beats `b + a`.

```python
from functools import cmp_to_key

def compare(a, b):
    if a + b > b + a:
        return -1          # a should come first
    if a + b < b + a:
        return 1
    return 0

nums = [3, 30, 34, 5, 9]
parts = sorted(map(str, nums), key=cmp_to_key(compare))
print("".join(parts))
```

A comparison function returns a negative number if a comes first, positive if b comes first, 0 if equal.

### Choosing a sort

| Situation | Use |
|---|---|
| Anything in Python | `sorted()` / `list.sort()` with a `key` |
| Small integer range (ages, scores 0–100) | counting sort, O(n + k) |
| Fixed-length integers or strings, huge n | radix sort, O(d · n) |
| Only the top k items | `heapq.nlargest(k, …)`, O(n log k) |
| The k-th item or the median | quickselect, O(n) average |
| Data bigger than memory | external merge sort |
| Need a guaranteed bound with O(1) memory | heap sort |

:::exercise Counting sort
Write `counting_sort(nums, max_value)` returning a new sorted list of the integers in `nums`, all between 0 and `max_value`, using counting sort in O(n + max_value). Don't use `sorted()` or `.sort()`. Must handle a million numbers.
```python starter
def counting_sort(nums, max_value):
    pass

print(counting_sort([4, 2, 2, 8, 3, 3, 1], 8))
```
```python check
if uses("sorted(") or uses(".sort("):
    raise AssertionError("Count the values instead of using sorted() or .sort().")
test("counting_sort", [
    (([4, 2, 2, 8, 3, 3, 1], 8), [1, 2, 2, 3, 3, 4, 8], "the example"),
    (([], 5), [], "empty"),
    (([0, 0, 0], 0), [0, 0, 0], "all zeros, max 0"),
    (([5], 9), [5], "one number"),
    (([9, 0, 9, 0], 9), [0, 0, 9, 9], "the extremes"),
    (([3, 1, 2], 100), [1, 2, 3], "a range much larger than the data"),
])
speed("counting_sort", lambda n: ([(i * 7919) % 101 for i in range(n)], 100), lambda a, m: sorted(a),
      sizes=(1_000, 10_000, 1_000_000), what="scores between 0 and 100", factor=40, floor=0.3,
      tip="Make one counter per possible value (a list of max_value + 1 zeros), count in one pass, then write each value out as many times as it was counted.")
```
```python solution
def counting_sort(nums, max_value):
    counts = [0] * (max_value + 1)      # one counter per possible value
    for x in nums:
        counts[x] += 1
    out = []
    for value in range(max_value + 1):
        out.extend([value] * counts[value])
    return out

print(counting_sort([4, 2, 2, 8, 3, 3, 1], 8))
```
```python slow
def counting_sort(nums, max_value):
    out = []
    for value in range(max_value + 1):
        out.extend([value] * nums.count(value))   # scans the whole list for every value
    out_sorted = []
    remaining = list(nums)
    while remaining:                              # and a selection sort on top
        m = min(remaining)
        remaining.remove(m)
        out_sorted.append(m)
    return out_sorted
```
hint: The values are small integers. Instead of comparing them, what could you count?
hint: Make a list `counts` with one slot per possible value (0 to max_value). One pass fills it; then read it from 0 upward.
hint: `counts = [0] * (max_value + 1)`; `for x in nums: counts[x] += 1`; then for each value, `out.extend([value] * counts[value])`.
approach:
1. **Understand:** integers in 0..max_value; return a new list; linear time.
2. **Examples:** [4, 2, 2, 8, 3, 3, 1], 8 → [1, 2, 2, 3, 3, 4, 8].
3. **Brute force:** a comparison sort: O(n log n) at best, O(n²) for the simple ones.
4. **Pattern:** small integer range → **counting sort** (no comparisons).
5. **Plan:** count each value; output values in order, repeated by their counts.
6. **Code and test:** empty input, max_value 0, a large range with few numbers.
walkthrough:
**Line by line**

- `counts[x]` is the number of times value `x` appears; the list index **is** the value, which is why no comparisons are needed.
- Reading `counts` from 0 to max_value visits the values in increasing order.
- `out.extend([value] * counts[value])` writes each value the right number of times.

**Trace** on [2, 0, 2, 1] with max_value 2:

| step | counts (for 0, 1, 2) | out |
|---|---|---|
| count | [1, 1, 2] | |
| value 0 | | [0] |
| value 1 | | [0, 1] |
| value 2 | | [0, 1, 2, 2] |

**Complexity:** O(n + k) time and O(n + k) space, where k = max_value + 1.

**Common wrong approach:** calling `nums.count(value)` for each value: that rescans the whole list every time, O(n · k).
:::

:::exercise Largest number
Write `largest_number(nums)` that arranges a list of non-negative integers so that, written side by side, they form the largest possible number, returned as a string. If the result is all zeros, return `"0"`.
```python starter
from functools import cmp_to_key

def largest_number(nums):
    pass

print(largest_number([3, 30, 34, 5, 9]))   # "9534330"
```
```python check
test("largest_number", [
    (([10, 2],), "210", "the classic"),
    (([3, 30, 34, 5, 9],), "9534330", "the example"),
    (([0, 0],), "0", "all zeros"),
    (([1],), "1", "one number"),
    (([121, 12],), "12121", "a tricky prefix"),
    (([8308, 8308, 830],), "83088308830", "repeated numbers"),
    (([0, 9, 8, 7, 6, 5, 4, 3, 2, 1],), "9876543210", "digits"),
])
```
```python solution
from functools import cmp_to_key

def largest_number(nums):
    def compare(a, b):
        if a + b > b + a:
            return -1        # a first makes a bigger number
        if a + b < b + a:
            return 1
        return 0

    parts = sorted(map(str, nums), key=cmp_to_key(compare))
    result = "".join(parts)
    return "0" if result[0] == "0" else result   # "00" -> "0"

print(largest_number([3, 30, 34, 5, 9]))
```
hint: Sorting the numbers in descending numeric order fails for [3, 30] ("303" < "330"). What should decide whether a goes before b?
hint: Compare the two possible joins: put a first if the string `a + b` is bigger than `b + a`. Use `functools.cmp_to_key` to sort with that rule.
hint: Convert to strings, sort with `key=cmp_to_key(compare)` where compare returns −1 if `a + b > b + a`, 1 if smaller, 0 if equal. Join, and turn a leading "0" result into "0".
approach:
1. **Understand:** order the numbers to maximise the concatenated string; return a string; all zeros → "0".
2. **Examples:** [10, 2] → "210"; [3, 30, 34, 5, 9] → "9534330"; [0, 0] → "0".
3. **Brute force:** try all n! orderings: hopeless beyond about 10 numbers.
4. **Pattern:** a **custom comparison sort** (the right order is defined pairwise).
5. **Plan:** strings; compare by a+b vs b+a; sort; join; fix the all-zeros case.
6. **Code and test:** prefixes like 121 and 12, zeros, a single number.
walkthrough:
**Line by line**

- Working with strings makes `a + b` concatenation, and comparing equal-length strings compares them as numbers.
- `compare(a, b)` returns −1 when a should come first: joining a then b gives the bigger result.
- This pairwise rule is transitive, so sorting with it produces the best overall order.
- If the biggest piece is "0", every piece is "0", so return "0" instead of "000".

**Trace** comparing pairs from [3, 30, 34]:

| a | b | a+b | b+a | order |
|---|---|---|---|---|
| "3" | "30" | "330" | "303" | 3 before 30 |
| "34" | "3" | "343" | "334" | 34 before 3 |
| → sorted | | | | 34, 3, 30 → "34330" |

**Complexity:** O(n log n) comparisons, each O(L) for numbers with up to L digits: O(L · n log n). O(n · L) space.

**Common wrong approach:** sorting by numeric value descending, which puts 30 before 3 and gives "303" instead of "330".
:::

:::quiz
? Why can't any comparison sort beat O(n log n) in the worst case?
+ It must distinguish n! orderings, and k yes/no comparisons distinguish at most 2^k of them
- Because computers are too slow
- Because Python limits sorting
= 2^k >= n! requires k >= log2(n!), which is about n log n.
? When is counting sort a good choice?
+ When the values are integers in a small range compared with n
- When the values are long strings
- When memory is extremely limited and values span billions
= Its cost is O(n + k); a huge range k makes it wasteful.
? Python's sorted() on a list that's already sorted takes:
+ About O(n), because Timsort detects existing runs
- O(n log n) always
- O(n²)
= Timsort is adaptive: sorted or nearly sorted input is fast.
? How do you sort by department ascending, then salary descending?
+ sorted(people, key=lambda p: (p.dept, -p.salary))
- sorted(people, key=lambda p: (p.dept, p.salary), reverse=True)
- Sort twice by salary
= Tuples compare item by item; negating the number reverses just that key.
:::
