# Data structures and algorithms cheat sheet

The method, the costs and the patterns on one page. The number in brackets is the lesson. This sheet grows as new parts of the course are added.

## The 6-step method [2]

1. **Understand:** inputs, outputs, limits (size, empty, negatives, duplicates).
2. **Examples:** 2–3 by hand, including an edge case.
3. **Brute force:** the simplest correct solution, and its Big-O.
4. **Spot the pattern:** clue words (table below); where does the brute force repeat work?
5. **Plan:** steps in plain words; check them on your examples.
6. **Code and test:** run the examples and edge cases; state the time and space cost.

In interviews, say every step out loud.

## Big-O at a glance [3, 4]

| Big-O | Name | Typical code | n = 10⁶ |
|---|---|---|---|
| O(1) | constant | index, dict/set lookup | 1 |
| O(log n) | logarithmic | halving (binary search) | ~20 |
| O(n) | linear | one loop | 10⁶ |
| O(n log n) | linearithmic | sorting | ~2 × 10⁷ |
| O(n²) | quadratic | loop inside a loop | 10¹² (too slow) |
| O(2ⁿ) | exponential | all subsets | impossible |

Rules: drop constants; keep the fastest-growing term; nested loops multiply, sequential loops add; halving → log. Python does roughly 10⁷–10⁸ simple steps per second.

**What input size allows which complexity** (rough guide for interview constraints):

| n up to | Aim for |
|---|---|
| 10–20 | O(2ⁿ), O(n!) (backtracking) |
| 500 | O(n³) |
| 5,000 | O(n²) |
| 10⁶ | O(n log n) or O(n) |
| 10⁹ and more | O(log n) or O(1) |

## Cost of Python's built-ins [5]

| list | cost | | dict / set | average cost |
|---|---|---|---|---|
| `a[i]`, `a[i] = x`, `len(a)` | O(1) | | `d[k]`, `d[k] = v`, `del d[k]` | O(1) |
| `append`, `pop()` | O(1) amortised | | `k in d`, `x in s`, `s.add(x)` | O(1) |
| `insert(i, x)`, `pop(i)`, `del a[i]` | O(n) | | iterate | O(n) |
| `x in a`, `index`, `count`, `remove` | O(n) | | `s & t` | O(min(len(s), len(t))) |
| slice `a[i:j]`, copy | O(j − i), O(n) | | `s | t` | O(len(s) + len(t)) |
| `min`, `max`, `sum` | O(n) | | **deque** `append`/`appendleft`/`pop`/`popleft` | O(1) |
| `sort`, `sorted` | O(n log n) | | **string** `+`, slice, `in`, `replace`, `join` | O(n) |

## Clue words → pattern [2]

| The problem says… | Try | Typical cost |
|---|---|---|
| "sorted array", "pair", "palindrome", "in place" | two pointers [7] | O(n) |
| "contiguous subarray / substring", "longest / shortest window", "k consecutive" | sliding window [8] | O(n) |
| "sum of a range", many range queries | prefix sums [9] | O(n) build, O(1) query |
| "subarray sum equals k" with negatives | prefix sums + hash map [14] | O(n) |
| "seen before", "duplicate", "count", "frequency", "anagram", "pair sum" (unsorted) | hash map / set [14] | O(n) |
| "grid", "neighbours", "rotate", "spiral" | 2-D indexing with direction lists [10] | O(rows × cols) |
| "find a pattern in text" | `in` / `find`; KMP or Rabin-Karp [12] | O(n + m) |
| "matching brackets", "next greater", "undo" | stack | (Part 4) |
| "top k", "k-th largest" | heap | (Part 6) |
| "shortest path", "fewest steps" | BFS | (Part 7) |
| "all combinations / subsets / permutations" | backtracking | (Part 5) |
| "number of ways", "min cost", choices that overlap | dynamic programming | (Part 8) |

## Pattern templates

**Running best [1, 6]**
```python
best = first_value            # or float("inf") / float("-inf")
for x in data:
    best = better_of(best, x)
```

**Two pointers, opposite ends [7]**
```python
left, right = 0, len(a) - 1
while left < right:
    if good(a[left], a[right]): return ...
    elif need_bigger: left += 1
    else: right -= 1
```

**Read / write pointers [7]**
```python
write = 0
for read in range(len(a)):
    if keep(a[read]):
        a[write] = a[read]; write += 1
return write
```

**Sliding window [8]**
```python
left = 0
for right, x in enumerate(a):
    add x to window state
    while window is invalid:
        remove a[left] from state; left += 1
    best = max(best, right - left + 1)
```

**Prefix sums [9]**
```python
prefix = [0]
for x in a: prefix.append(prefix[-1] + x)
range_sum = prefix[j + 1] - prefix[i]       # a[i..j] inclusive
```

**Hash map patterns [14]**
```python
seen = {}                                    # Two Sum: value -> index
for i, x in enumerate(a):
    if target - x in seen: return [seen[target - x], i]
    seen[x] = i

counts = {0: 1}; cur = ans = 0               # subarrays with sum k
for x in a:
    cur += x; ans += counts.get(cur - k, 0); counts[cur] = counts.get(cur, 0) + 1

groups = defaultdict(list)                   # group by a normalised key
for w in words: groups["".join(sorted(w))].append(w)
```

**Grid neighbours [10]**
```python
for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols: ...
```

## Algorithms so far

| Algorithm | Time | Space | Notes |
|---|---|---|---|
| Linear search [4] | O(n) | O(1) | any list |
| Reverse / rotate in place [4, 6] | O(n) | O(1) | three reversals |
| Kadane-style running best, buy/sell stock [6] | O(n) | O(1) | running minimum |
| Merge two sorted lists [7] | O(n + m) | O(n + m) | two pointers |
| Fixed / variable sliding window [8] | O(n) | O(1) or O(k) | each pointer moves ≤ n times |
| Prefix sums, difference array [9] | O(n) build | O(n) | O(1) per query / update |
| Spiral, rotate a grid [10] | O(R·C) | O(1) / O(R·C) | |
| Naive string search [12] | O(n·m) | O(1) | |
| KMP [12] | O(n + m) | O(m) | LPS table |
| Rabin-Karp [12] | O(n + m) average | O(1) | rolling hash, check matches |
| Hash map insert / lookup [13] | O(1) average, O(n) worst | O(n) | keys must be hashable |

## Edge cases to always test

Empty input · one item · two items · all the same · already sorted / reverse sorted · negatives and zero · duplicates · the answer at the very start or end · no valid answer · very large input (speed).
