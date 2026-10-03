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

## Every concept at a glance

Generated from the **At a glance** table at the end of each lesson. The number in brackets links to the lesson.

| Concept | Approach | Time | Space | Lesson |
|---|---|---|---|---|
| Data structure | a way to organise data so the operations you need are fast | depends on the structure | O(n) to store n items | [1](lessons/01-what-is-dsa.md) |
| Algorithm | exact steps that turn an input into the right output | measured with Big-O | extra memory it needs | [1](lessons/01-what-is-dsa.md) |
| Smallest number | one pass, remembering the smallest so far | O(n) | O(1) | [1](lessons/01-what-is-dsa.md) |
| Duplicate check (brute force vs set) | compare every pair, or remember seen items in a set | O(n²) vs O(n) | O(1) vs O(n) | [1](lessons/01-what-is-dsa.md) |
| 6-step method | understand → examples → brute force → pattern → plan → code and test | (thinking, not running) | — | [2](lessons/02-problem-solving.md) |
| Contains duplicate | add to a set; stop when an item is already in it | O(n) | O(n) | [2](lessons/02-problem-solving.md) |
| Contains duplicate (low memory) | sort, then compare neighbours | O(n log n) | O(1) extra (in place) | [2](lessons/02-problem-solving.md) |
| Second largest | one pass tracking the largest and second largest distinct values | O(n) | O(1) | [2](lessons/02-problem-solving.md) |
| O(1) constant | same work whatever the size: indexing, dict lookup | O(1) | — | [3](lessons/03-big-o.md) |
| O(log n) logarithmic | halve the problem each step: binary search | O(log n) | — | [3](lessons/03-big-o.md) |
| O(n) linear | touch each item once: one loop | O(n) | — | [3](lessons/03-big-o.md) |
| O(n log n) | sort, or split in halves and do linear work per level | O(n log n) | — | [3](lessons/03-big-o.md) |
| O(n²) quadratic | a loop inside a loop over the same data | O(n²) | — | [3](lessons/03-big-o.md) |
| O(2ⁿ), O(n!) | try every subset or every ordering | O(2ⁿ), O(n!) | — | [3](lessons/03-big-o.md) |
| Sum 1..n | formula n(n+1)/2 instead of a loop | O(1) | O(1) | [3](lessons/03-big-o.md) |
| Space complexity | count the extra memory that grows with the input | — | O(1), O(n)… | [4](lessons/04-space-and-cases.md) |
| Best / average / worst case | analyse the input that is fastest, typical and slowest | e.g. linear search O(1) / O(n) / O(n) | — | [4](lessons/04-space-and-cases.md) |
| Amortised cost | average over a long run of operations (list append) | amortised O(1) per append | O(n) total | [4](lessons/04-space-and-cases.md) |
| Reverse in place | swap the ends and move two pointers inwards | O(n) | O(1) | [4](lessons/04-space-and-cases.md) |
| Linear search | check each item until found | O(n) worst, O(1) best | O(1) | [4](lessons/04-space-and-cases.md) |
| list index, append, pop() | direct access at the end | O(1) (append amortised) | — | [5](lessons/05-python-costs.md) |
| list insert(0), pop(0), `in`, remove | shift items or scan | O(n) | — | [5](lessons/05-python-costs.md) |
| dict / set lookup, insert, delete | hash table | O(1) average, O(n) worst | O(n) | [5](lessons/05-python-costs.md) |
| String concatenation in a loop | build a list and `''.join` it once | O(n) with join, O(n²) with += | O(n) | [5](lessons/05-python-costs.md) |
| deque appendleft / popleft | double-ended queue | O(1) | O(n) | [5](lessons/05-python-costs.md) |
| sorted(), list.sort() | Timsort | O(n log n) | O(n) | [5](lessons/05-python-costs.md) |
| Items in both lists | turn one list into a set, then filter the other | O(n + m) | O(n) | [5](lessons/05-python-costs.md) |
| Index access | address = start + index × size | O(1) | — | [6](lessons/06-arrays.md) |
| Insert / delete in the middle | shift the items after it | O(n) | O(1) | [6](lessons/06-arrays.md) |
| Best time to buy and sell | track the cheapest price so far and today's profit | O(n) | O(1) | [6](lessons/06-arrays.md) |
| Rotate by k in place | reverse all, then reverse the first k and the rest | O(n) | O(1) | [6](lessons/06-arrays.md) |
| Pair sum in a sorted array | pointers at both ends; move the one that fixes the sum | O(n) | O(1) | [7](lessons/07-two-pointers.md) |
| Palindrome check | compare from both ends towards the middle | O(n) | O(1) | [7](lessons/07-two-pointers.md) |
| Remove duplicates in place | write pointer + read pointer | O(n) | O(1) | [7](lessons/07-two-pointers.md) |
| Merge two sorted lists | one pointer per list, take the smaller | O(n + m) | O(n + m) for the result | [7](lessons/07-two-pointers.md) |
| Fixed-size window (best k in a row) | add the new item, subtract the one leaving | O(n) | O(1) | [8](lessons/08-sliding-window.md) |
| Variable window (longest substring without repeats) | grow the right edge; shrink the left until valid | O(n) | O(k) distinct items | [8](lessons/08-sliding-window.md) |
| Window template | expand → while invalid: shrink → record answer | O(n) (each item enters and leaves once) | depends on the window state | [8](lessons/08-sliding-window.md) |
| Prefix sums | prefix[i] = sum of the first i items; a range sum is a difference | O(n) build, O(1) per query | O(n) | [9](lessons/09-prefix-sums.md) |
| Pivot index | left sum vs total − left − current | O(n) | O(1) | [9](lessons/09-prefix-sums.md) |
| Difference array | +v at start, −v after end; prefix-sum once at the end | O(1) per update, O(n) to finish | O(n) | [9](lessons/09-prefix-sums.md) |
| 2-D prefix sums | inclusion–exclusion on a grid | O(r·c) build, O(1) per query | O(r·c) | [9](lessons/09-prefix-sums.md) |
| Grid neighbours | loop over a list of (dr, dc) directions with bounds checks | O(1) per cell | O(1) | [10](lessons/10-matrices.md) |
| Transpose | swap m[r][c] with m[c][r] above the diagonal | O(n²) | O(1) in place | [10](lessons/10-matrices.md) |
| Rotate 90° clockwise | transpose, then reverse each row | O(n²) | O(1) in place | [10](lessons/10-matrices.md) |
| Spiral order | shrink four boundaries: top, right, bottom, left | O(r·c) | O(1) extra | [10](lessons/10-matrices.md) |
| Search a sorted matrix | start top-right; go left or down | O(r + c) | O(1) | [10](lessons/10-matrices.md) |
| Build a string | append pieces to a list, `''.join` once | O(n) | O(n) | [11](lessons/11-strings.md) |
| Characters as numbers | `ord`/`chr`, counts in an array of 26 | O(1) per char | O(1) for a fixed alphabet | [11](lessons/11-strings.md) |
| Anagram check | sort both, or compare Counters | O(n log n) or O(n) | O(n) | [11](lessons/11-strings.md) |
| Run-length encoding | count runs of equal characters in one pass | O(n) | O(n) | [11](lessons/11-strings.md) |
| Reverse the words | split, reverse the list, join | O(n) | O(n) | [11](lessons/11-strings.md) |
| Naive matching | try the pattern at every position | O(n·m) | O(1) | [12](lessons/12-string-matching.md) |
| KMP | prefix (failure) table lets the scan never move backwards | O(n + m) | O(m) | [12](lessons/12-string-matching.md) |
| Rabin-Karp | rolling hash of each window; compare text only when hashes match | O(n + m) average, O(n·m) worst | O(1) | [12](lessons/12-string-matching.md) |
| Python `in` / `str.find` | optimised built-in search | about O(n) in practice | O(1) | [12](lessons/12-string-matching.md) |
| Hash table | hash(key) % size picks a bucket | O(1) average per operation | O(n) | [13](lessons/13-hash-tables.md) |
| Collisions (chaining) | each bucket holds a small list of pairs | O(1) average, O(n) worst | O(n) | [13](lessons/13-hash-tables.md) |
| Resizing | grow and re-insert when the load factor is high | O(n) per resize, amortised O(1) | O(n) | [13](lessons/13-hash-tables.md) |
| Your own hash map | buckets of [key, value] pairs with put / get / remove | O(1) average | O(n) | [13](lessons/13-hash-tables.md) |
| Counting | Counter or dict.get(x, 0) + 1 | O(n) | O(k) distinct items | [14](lessons/14-hashing-patterns.md) |
| Two Sum | for each x, look up target − x among numbers already seen | O(n) | O(n) | [14](lessons/14-hashing-patterns.md) |
| Group anagrams | key = sorted letters; dict of lists | O(n·k log k) | O(n·k) | [14](lessons/14-hashing-patterns.md) |
| Subarray sum equals k | count earlier prefix sums equal to current − k | O(n) | O(n) | [14](lessons/14-hashing-patterns.md) |
| Longest consecutive sequence | set; start counting only at numbers whose x − 1 is missing | O(n) | O(n) | [14](lessons/14-hashing-patterns.md) |
| Traverse / search | follow next from the head | O(n) | O(1) | [15](lessons/15-linked-lists.md) |
| Access item i | walk i steps | O(n) | O(1) | [15](lessons/15-linked-lists.md) |
| Insert / delete at the front | new node points to the old head | O(1) | O(1) | [15](lessons/15-linked-lists.md) |
| Append with a tail pointer | link after the tail, move the tail | O(1) | O(1) | [15](lessons/15-linked-lists.md) |
| Delete by value | dummy + prev pointer; prev.next = prev.next.next | O(n) | O(1) | [15](lessons/15-linked-lists.md) |
| Delete a node you hold (doubly linked) | reconnect its prev and next | O(1) | O(1) | [15](lessons/15-linked-lists.md) |
| Insert into a sorted list | walk to the last smaller node, splice | O(n) | O(1) | [15](lessons/15-linked-lists.md) |
| Josephus circle | circular list, unlink every k-th node | O(n·k) | O(n) | [15](lessons/15-linked-lists.md) |
| Reverse a list | prev / cur / next, turn each arrow around | O(n) | O(1) (recursive: O(n) stack) | [16](lessons/16-linked-list-patterns.md) |
| Middle node | slow 1 step, fast 2 steps | O(n) | O(1) | [16](lessons/16-linked-list-patterns.md) |
| Detect a cycle (Floyd) | fast and slow meet if there's a loop | O(n) | O(1) | [16](lessons/16-linked-list-patterns.md) |
| Find the cycle's start | after meeting, restart one pointer at the head; step both by 1 | O(n) | O(1) | [16](lessons/16-linked-list-patterns.md) |
| Merge two sorted lists | dummy + tail; attach the smaller front | O(n + m) | O(1) | [16](lessons/16-linked-list-patterns.md) |
| Remove k-th from the end | lead k steps ahead, then move both | O(n) | O(1) | [16](lessons/16-linked-list-patterns.md) |
| Palindrome list | middle, reverse the second half, compare | O(n) | O(1) | [16](lessons/16-linked-list-patterns.md) |
| Push / pop / peek | list.append / list.pop() / list[-1] | O(1) | O(n) for n items | [17](lessons/17-stacks.md) |
| Valid brackets | push openers; a closer must match the popped top | O(n) | O(n) | [17](lessons/17-stacks.md) |
| Min stack | store (value, min so far) pairs | O(1) per operation | O(n) | [17](lessons/17-stacks.md) |
| Evaluate RPN | push numbers; on an operator pop b, pop a, push a op b | O(n) | O(n) | [17](lessons/17-stacks.md) |
| Infix → RPN (shunting-yard) | operator stack ordered by precedence | O(n) | O(n) | [17](lessons/17-stacks.md) |
| Recursion → loop | replace the call stack with your own list | same as the recursion | O(depth) | [17](lessons/17-stacks.md) |
| Next greater element | decreasing stack of indexes; a bigger value pops and answers them | O(n) | O(n) | [18](lessons/18-monotonic-stack.md) |
| Daily temperatures | next greater, answer = index distance | O(n) | O(n) | [18](lessons/18-monotonic-stack.md) |
| Stock span (previous greater) | pop smaller or equal, distance to the new top | O(n) | O(n) | [18](lessons/18-monotonic-stack.md) |
| Largest rectangle in a histogram | increasing stack; a popped bar's width runs from the bar below it to i | O(n) | O(n) | [18](lessons/18-monotonic-stack.md) |
| Trapping rain water | two pointers, move the lower wall | O(n) | O(1) | [18](lessons/18-monotonic-stack.md) |
| Enqueue / dequeue | deque.append / deque.popleft | O(1) | O(n) | [19](lessons/19-queues-deques.md) |
| Keep only the last k items | deque(maxlen=k) | O(1) per append | O(k) | [19](lessons/19-queues-deques.md) |
| Circular buffer | array + head + size, indexes wrap with % | O(1) per operation | O(capacity) | [19](lessons/19-queues-deques.md) |
| Queue from two stacks | push to inbox; pour into outbox only when it's empty | amortised O(1) | O(n) | [19](lessons/19-queues-deques.md) |
| Sliding window maximum | deque of indexes with decreasing values | O(n) | O(k) | [19](lessons/19-queues-deques.md) |
| LRU get / put | dict of key → node + doubly linked list in recency order | O(1) | O(capacity) | [20](lessons/20-lru-cache.md) |
| LRU with OrderedDict | move_to_end and popitem(last=False) | O(1) | O(capacity) | [20](lessons/20-lru-cache.md) |
| Memoise a function | @lru_cache(maxsize) or @cache | O(1) per repeated call | O(distinct arguments) | [20](lessons/20-lru-cache.md) |
| LFU get / put | count per key + OrderedDict per count + minimum count | O(1) | O(capacity) | [20](lessons/20-lru-cache.md) |
| Factorial | n × factorial(n − 1), base case n ≤ 1 | O(n) | O(n) stack | [21](lessons/21-recursion.md) |
| Sum / reverse / palindrome by recursion | handle one item, recurse on the rest | O(n) with indexes (O(n²) with slicing) | O(n) stack | [21](lessons/21-recursion.md) |
| Nested data (folders, nested lists) | recurse into each sub-container | O(total items) | O(depth) | [21](lessons/21-recursion.md) |
| Naive Fibonacci | fib(n − 1) + fib(n − 2) | O(2ⁿ) (about 1.6ⁿ) | O(n) | [21](lessons/21-recursion.md) |
| Memoised Fibonacci | cache each fib(k) | O(n) | O(n) | [21](lessons/21-recursion.md) |
| Tower of Hanoi | move n − 1, move 1, move n − 1 | O(2ⁿ) moves | O(n) stack | [21](lessons/21-recursion.md) |
| Flatten a nested list | extend with flatten(sub-list), append numbers | O(n) | O(depth) | [21](lessons/21-recursion.md) |
| Fast power xⁿ | square the half-power; multiply in x when n is odd | O(log n) | O(1) loop / O(log n) recursive | [22](lessons/22-divide-and-conquer.md) |
| Merge sort | sort halves recursively, merge | O(n log n) | O(n) | [22](lessons/22-divide-and-conquer.md) |
| Count inversions | count during merge sort's merge: add len(left) − i | O(n log n) | O(n) | [22](lessons/22-divide-and-conquer.md) |
| Maximum subarray (D&C) | best of left, right, and crossing the middle | O(n log n) | O(log n) | [22](lessons/22-divide-and-conquer.md) |
| Master theorem | compare a with bᵈ: same → nᵈ log n; smaller → nᵈ; larger → n^(log_b a) | — | — | [22](lessons/22-divide-and-conquer.md) |
| Subsets | include or skip each item | O(n · 2ⁿ) | O(n) + output | [23](lessons/23-backtracking.md) |
| Permutations | at each position try every unused item | O(n · n!) | O(n) + output | [23](lessons/23-backtracking.md) |
| Combinations (k of n) | loop forward from a start index; prune when too few remain | O(k · C(n, k)) | O(k) + output | [23](lessons/23-backtracking.md) |
| Combination sum (reuse allowed) | sorted candidates, recurse with the same index, break when too big | exponential | O(target / smallest) | [23](lessons/23-backtracking.md) |
| N-Queens | one queen per row; sets of columns, row − col, row + col | O(n!) worst, heavily pruned | O(n) | [23](lessons/23-backtracking.md) |
| Sudoku | fill an empty cell with each valid digit, undo on dead ends | exponential worst | O(81) | [23](lessons/23-backtracking.md) |
| Word search | DFS from each cell, mark used cells, unmark after | O(r · c · 4ᴸ) | O(L) | [23](lessons/23-backtracking.md) |
| Linear search | check each item | O(n) | O(1) | [24](lessons/24-binary-search.md) |
| Binary search | compare with the middle; keep one half | O(log n) | O(1) | [24](lessons/24-binary-search.md) |
| bisect_left / bisect_right | C-coded binary search for insertion points | O(log n) | O(1) | [24](lessons/24-binary-search.md) |
| Count items in a range of a sorted list | bisect_right(hi) − bisect_left(lo) | O(log n) | O(1) | [24](lessons/24-binary-search.md) |
| First / last occurrence | on a match, record it and keep searching left / right | O(log n) | O(1) | [24](lessons/24-binary-search.md) |
| Search a rotated sorted array | one half is always sorted; check if the target is inside it | O(log n) | O(1) | [24](lessons/24-binary-search.md) |
| Find a peak | move towards the bigger neighbour | O(log n) | O(1) | [24](lessons/24-binary-search.md) |
| Search a sorted matrix (rows continue) | treat it as one list: row k // cols, column k % cols | O(log(r·c)) | O(1) | [24](lessons/24-binary-search.md) |
| First value that works | while lo < hi: mid; works → hi = mid, else lo = mid + 1 | O(log(range) × check) | O(1) | [25](lessons/25-binary-search-answer.md) |
| Last value that works | mid rounded up; works → lo = mid, else hi = mid − 1 | O(log(range) × check) | O(1) | [25](lessons/25-binary-search-answer.md) |
| Integer square root | last x with x·x ≤ n | O(log n) | O(1) | [25](lessons/25-binary-search-answer.md) |
| Minimum ship capacity | search max(w)..sum(w); greedy day count | O(n log(sum)) | O(1) | [25](lessons/25-binary-search-answer.md) |
| Minimum eating speed | search 1..max(pile); total hours with ceiling division | O(n log(max)) | O(1) | [25](lessons/25-binary-search-answer.md) |
| Minimum of a rotated array | compare nums[mid] with nums[hi] | O(log n) | O(1) | [25](lessons/25-binary-search-answer.md) |
| Real-valued answer | fixed number of halvings (e.g. 100) | O(iterations × check) | O(1) | [25](lessons/25-binary-search-answer.md) |
| Bubble sort | swap out-of-order neighbours; stop when a pass makes no swaps | O(n²), best O(n) | O(1) | [26](lessons/26-simple-sorts.md) |
| Selection sort | swap the minimum of the rest into place | O(n²) always | O(1) | [26](lessons/26-simple-sorts.md) |
| Insertion sort | shift bigger items right, drop the item in the gap | O(n²), best O(n) | O(1) | [26](lessons/26-simple-sorts.md) |
| Dutch national flag (sort 0/1/2) | three pointers low / mid / high | O(n) | O(1) | [26](lessons/26-simple-sorts.md) |
| Merge sort | split, sort halves, merge | O(n log n) always | O(n) | [27](lessons/27-efficient-sorts.md) |
| Quicksort | random pivot, partition, recurse both sides | O(n log n) average, O(n²) worst | O(log n) | [27](lessons/27-efficient-sorts.md) |
| Heap sort | build a max-heap, swap the max to the end, sift down | O(n log n) always | O(1) | [27](lessons/27-efficient-sorts.md) |
| Quickselect (k-th smallest) | partition, keep only the side holding k | O(n) average, O(n²) worst | O(1) | [27](lessons/27-efficient-sorts.md) |
| 3-way quicksort (many duplicates) | Dutch-flag partition around the pivot | O(n log n), O(n) if all equal | O(log n) | [27](lessons/27-efficient-sorts.md) |
| Counting sort | count each value, write values in order | O(n + k) | O(n + k) | [28](lessons/28-sorting-in-practice.md) |
| Radix sort (LSD) | stable bucket pass per digit, least significant first | O(d · (n + b)) | O(n + b) | [28](lessons/28-sorting-in-practice.md) |
| Bucket sort | bucket by value, sort buckets, concatenate | O(n) average, O(n²) worst | O(n) | [28](lessons/28-sorting-in-practice.md) |
| sorted() / list.sort() (Timsort) | merge natural runs; insertion sort for short runs | O(n log n), O(n) if nearly sorted | O(n) | [28](lessons/28-sorting-in-practice.md) |
| Multi-key sort | key returns a tuple; negate numbers to reverse one key | O(n log n) | O(n) | [28](lessons/28-sorting-in-practice.md) |
| Largest number from digits | sort strings with cmp: a + b vs b + a | O(L · n log n) | O(n · L) | [28](lessons/28-sorting-in-practice.md) |
| Top k items | heapq.nlargest(k, items) | O(n log k) | O(k) | [28](lessons/28-sorting-in-practice.md) |
| Preorder / inorder / postorder (recursive) | visit node before / between / after the subtrees | O(n) | O(h) | [29](lessons/29-binary-trees.md) |
| Iterative DFS | explicit stack; push right before left for preorder | O(n) | O(h) | [29](lessons/29-binary-trees.md) |
| Level order (BFS) | queue; pop len(queue) nodes per level | O(n) | O(w), the widest level | [29](lessons/29-binary-trees.md) |
| Max depth | 1 + max(depth(left), depth(right)) | O(n) | O(h) | [29](lessons/29-binary-trees.md) |
| Count / sum of nodes | 1 + count(left) + count(right) | O(n) | O(h) | [29](lessons/29-binary-trees.md) |
| Build from a level-order list | queue of nodes waiting for children | O(n) | O(n) | [29](lessons/29-binary-trees.md) |
| Diameter | height helper; best = max(best, left + right) | O(n) | O(h) | [30](lessons/30-tree-problems.md) |
| Is balanced | height helper returning −1 for "unbalanced" | O(n) | O(h) | [30](lessons/30-tree-problems.md) |
| Root-to-leaf paths with a sum | DFS passing the remaining sum down; backtrack the path | O(n) per path copy, O(n²) worst | O(h) | [30](lessons/30-tree-problems.md) |
| Invert a tree | swap children recursively | O(n) | O(h) | [30](lessons/30-tree-problems.md) |
| Is symmetric | compare left.left with right.right and left.right with right.left | O(n) | O(h) | [30](lessons/30-tree-problems.md) |
| Lowest common ancestor | return p/q/None from each side; both non-None → this node | O(n) | O(h) | [30](lessons/30-tree-problems.md) |
| Serialise / deserialise | preorder with "#" for empty children | O(n) | O(n) | [30](lessons/30-tree-problems.md) |
| Build from preorder + inorder | next preorder value is the root; dict of inorder positions splits | O(n) | O(n) | [30](lessons/30-tree-problems.md) |
| Search / insert | go left if smaller, right if bigger | O(h): O(log n) balanced, O(n) worst | O(1) iterative | [31](lessons/31-bst.md) |
| Min / max | go left / right until you can't | O(h) | O(1) | [31](lessons/31-bst.md) |
| Floor / ceiling | search, remembering the best candidate | O(h) | O(1) | [31](lessons/31-bst.md) |
| K-th smallest | iterative inorder, stop after k | O(h + k) | O(h) | [31](lessons/31-bst.md) |
| Delete | 0 or 1 child: return the other child; 2 children: copy the successor, delete it | O(h) | O(h) | [31](lessons/31-bst.md) |
| Validate | pass (low, high) bounds down | O(n) | O(h) | [31](lessons/31-bst.md) |
| LCA in a BST | go left while both are smaller, right while both are bigger | O(h) | O(1) | [31](lessons/31-bst.md) |
| AVL / red-black insert and delete | BST operation + rotations | O(log n) | O(log n) | [31](lessons/31-bst.md) |
| Sorted list + bisect | binary search; insort shifts items | O(log n) search, O(n) insert | O(n) | [31](lessons/31-bst.md) |
| Push / pop | append + sift up / move last to root + sift down | O(log n) | O(1) | [32](lessons/32-heaps.md) |
| Peek at the minimum | heap[0] | O(1) | O(1) | [32](lessons/32-heaps.md) |
| Heapify a list | sift down from the last parent to the root | O(n) | O(1) | [32](lessons/32-heaps.md) |
| Heap sort | heapify, then pop n times | O(n log n) | O(1) in place | [32](lessons/32-heaps.md) |
| K largest / k closest | min-heap (or negated max-heap) of size k | O(n log k) | O(k) | [32](lessons/32-heaps.md) |
| K-th largest | root of a size-k min-heap | O(n log k) | O(k) | [32](lessons/32-heaps.md) |
| Merge k sorted lists | heap of (value, list, index) | O(N log k) | O(k) | [32](lessons/32-heaps.md) |
| Running median | max-heap of the lower half + min-heap of the upper half | O(log n) add, O(1) median | O(n) | [32](lessons/32-heaps.md) |
| Insert / search / starts_with | walk one character per level, creating nodes on insert | O(L) | O(L) per new word | [33](lessons/33-tries.md) |
| Autocomplete (first k words) | walk the prefix, then DFS in alphabetical order, stop at k | O(L + nodes visited) | O(L) | [33](lessons/33-tries.md) |
| Count words with a prefix | store a pass-through count in each node | O(L) | O(1) extra per node | [33](lessons/33-tries.md) |
| Delete a word | decrement counts along the path; prune empty branches | O(L) | O(1) | [33](lessons/33-tries.md) |
| Wildcard search | at ".", try every child | O(26^dots × L) worst | O(L) | [33](lessons/33-tries.md) |
| Longest prefix match | walk the text, remember the last word end | O(L) | O(1) | [33](lessons/33-tries.md) |
| Prefix range with a sorted list | bisect_left(words, prefix), read forwards | O(L log n) | O(n) | [33](lessons/33-tries.md) |
| Fenwick: point add / prefix sum | climb with i += i & −i / descend with i −= i & −i | O(log n) each | O(n) | [34](lessons/34-segment-fenwick.md) |
| Fenwick: range sum | prefix(r + 1) − prefix(l) | O(log n) | O(n) | [34](lessons/34-segment-fenwick.md) |
| Segment tree (iterative, 2n list) | leaves at n..2n−1; combine pairs going up | O(log n) update and query | O(n) | [34](lessons/34-segment-fenwick.md) |
| Segment tree with lazy propagation | stop at covering nodes, store a pending update | O(log n) range update and query | O(n) | [34](lessons/34-segment-fenwick.md) |
| Sparse table (static min / max) | two overlapping power-of-two blocks | O(n log n) build, O(1) query | O(n log n) | [34](lessons/34-segment-fenwick.md) |
| Square-root decomposition | blocks of √n items with stored totals | O(1) update, O(√n) query | O(n) | [34](lessons/34-segment-fenwick.md) |
| Count smaller to the right / inversions | Fenwick tree over ranks, scanning right to left | O(n log n) | O(n) | [34](lessons/34-segment-fenwick.md) |
| Build an adjacency list | append (u, v) and (v, u) for undirected edges | O(V + E) | O(V + E) | [35](lessons/35-graphs.md) |
| DFS (iterative) | stack + visited set | O(V + E) | O(V) | [35](lessons/35-graphs.md) |
| BFS | queue (deque) + visited set, mark when queued | O(V + E) | O(V) | [35](lessons/35-graphs.md) |
| Connected components | one search from every unvisited vertex | O(V + E) | O(V) | [35](lessons/35-graphs.md) |
| Count islands in a grid | flood fill from each unvisited land cell | O(R · C) | O(R · C) | [35](lessons/35-graphs.md) |
| Edge check with an adjacency matrix | matrix[u][v] | O(1) | O(V²) | [35](lessons/35-graphs.md) |
| Shortest path, unweighted | BFS from the start; distance of first visit | O(V + E) | O(V) | [36](lessons/36-bfs-shortest.md) |
| Rebuild the path | store parents; walk back from the goal; reverse | O(path length) | O(V) | [36](lessons/36-bfs-shortest.md) |
| Grid shortest path | BFS over cells with 4 or 8 neighbours | O(R · C) | O(R · C) | [36](lessons/36-bfs-shortest.md) |
| Distance to the nearest of many sources | multi-source BFS | O(V + E) | O(V) | [36](lessons/36-bfs-shortest.md) |
| Weights 0 or 1 | 0-1 BFS with a deque | O(V + E) | O(V) | [36](lessons/36-bfs-shortest.md) |
| Word ladder | BFS over words; wildcard buckets find neighbours | O(N · L²) | O(N · L) | [36](lessons/36-bfs-shortest.md) |
| Bidirectional BFS | grow the smaller frontier until the two meet | about O(b^(d/2)) | O(b^(d/2)) | [36](lessons/36-bfs-shortest.md) |
| Topological sort (Kahn) | queue of in-degree-0 vertices; decrement neighbours | O(V + E) | O(V + E) | [37](lessons/37-topological-sort.md) |
| Topological sort (DFS) | reverse of the finishing order | O(V + E) | O(V) | [37](lessons/37-topological-sort.md) |
| Directed cycle check | Kahn leaves vertices out, or DFS meets a grey vertex | O(V + E) | O(V) | [37](lessons/37-topological-sort.md) |
| Smallest topological order | Kahn with a heap instead of a queue | O((V + E) log V) | O(V + E) | [37](lessons/37-topological-sort.md) |
| Earliest finish (critical path) | DP in topological order: start[v] = max(start[u] + time[u]) | O(V + E) | O(V) | [37](lessons/37-topological-sort.md) |
| Shortest path in a DAG (any weights) | relax edges in topological order | O(V + E) | O(V) | [37](lessons/37-topological-sort.md) |
| Dijkstra (heap) | pop the closest vertex, relax its edges, skip stale entries | O((V + E) log V) | O(V + E) | [38](lessons/38-shortest-paths.md) |
| Dijkstra (array scan, dense graphs) | pick the closest unsettled vertex by scanning | O(V²) | O(V) | [38](lessons/38-shortest-paths.md) |
| Bellman-Ford | relax every edge V − 1 times; an extra round finds negative cycles | O(V · E) | O(V) | [38](lessons/38-shortest-paths.md) |
| Cheapest with at most k edges | k rounds of Bellman-Ford from a copy | O(k · E) | O(V) | [38](lessons/38-shortest-paths.md) |
| Floyd-Warshall | for k, i, j: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) | O(V³) | O(V²) | [38](lessons/38-shortest-paths.md) |
| A* | heap ordered by g + h with an admissible h | ≤ Dijkstra in practice | O(V) | [38](lessons/38-shortest-paths.md) |
| Find / union | path compression + union by size | O(α(n)) amortised, effectively O(1) | O(n) | [39](lessons/39-union-find-mst.md) |
| Count components as edges arrive | start at n; each successful union subtracts 1 | O(E · α(V)) | O(V) | [39](lessons/39-union-find-mst.md) |
| Undirected cycle (redundant edge) | union fails because both ends share a root | O(E · α(V)) | O(V) | [39](lessons/39-union-find-mst.md) |
| Kruskal's MST | sort edges; add those joining different groups | O(E log E) | O(V + E) | [39](lessons/39-union-find-mst.md) |
| Prim's MST (heap) | grow one tree; take the cheapest edge to a new vertex | O(E log V) | O(V + E) | [39](lessons/39-union-find-mst.md) |
| Prim's MST (dense, array) | keep each outside vertex's cheapest link; scan for the minimum | O(V²) | O(V) | [39](lessons/39-union-find-mst.md) |
| Single-linkage clustering into k groups | Kruskal, stopping at k groups | O(E log E) | O(V + E) | [39](lessons/39-union-find-mst.md) |
| Bipartite check | BFS two-colouring; a same-colour edge means an odd cycle | O(V + E) | O(V) | [40](lessons/40-advanced-graphs.md) |
| Undirected cycle check | DFS ignoring the parent edge, or union-find | O(V + E) | O(V) | [40](lessons/40-advanced-graphs.md) |
| Strongly connected components | Kosaraju: finishing order, then DFS on reversed edges | O(V + E) | O(V + E) | [40](lessons/40-advanced-graphs.md) |
| Bridges / articulation points | Tarjan: low[v] > disc[u] / low[v] ≥ disc[u] | O(V + E) | O(V) | [40](lessons/40-advanced-graphs.md) |
| Eulerian path | Hierholzer: walk unused edges, add vertices when stuck | O(E) | O(E) | [40](lessons/40-advanced-graphs.md) |
| Maximum flow | Edmonds-Karp: BFS augmenting paths with reverse capacities | O(V · E²) | O(V²) with a matrix | [40](lessons/40-advanced-graphs.md) |
| Travelling salesman (exact) | bitmask DP over subsets | O(2ⁿ · n²) | O(2ⁿ · n) | [40](lessons/40-advanced-graphs.md) |
