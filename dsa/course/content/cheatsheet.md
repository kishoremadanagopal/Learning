# Data structures and algorithms cheat sheet

The method, the costs and the patterns for the whole course in one place. The number in brackets is the lesson. The table of every concept with its approach and complexity is at the end.

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

Rules: drop constants; keep the fastest-growing term; nested loops multiply, sequential loops add; halving → log. Python does very roughly 10⁷ simple steps per second.

**What input size allows which complexity** [49]:

| n up to | Aim for | Typical techniques |
|---|---|---|
| 10 | O(n!) | permutations, backtracking |
| 20–25 | O(2ⁿ), O(2ⁿ · n) | subsets, bitmask DP |
| 500 | O(n³) | Floyd-Warshall, interval DP |
| 5,000 | O(n²) | 2-D DP, all pairs |
| 10⁶ | O(n log n) or O(n) | sorting, heaps, hashing, two pointers, sliding window |
| 10⁹ and more | O(log n) or O(1) | binary search on the answer, maths |

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

## Data structures: what each operation costs

| Structure | Fast at | Costs | Lessons |
|---|---|---|---|
| list (dynamic array) | index, append, pop at the end | O(1); insert / delete in the middle O(n) | 5, 6 |
| dict / set (hash table) | lookup, insert, delete by key | O(1) average | 13, 14 |
| linked list | insert / delete at a known node | O(1); search O(n) | 15, 16 |
| stack (list) | push, pop, peek | O(1) | 17, 18 |
| queue / deque | add and remove at both ends | O(1) | 19 |
| binary heap (heapq) | min (or max), push, pop | O(1) peek, O(log n) push/pop | 32 |
| balanced BST / SortedList | ordered search, insert, delete, floor/ceiling | O(log n) | 31 |
| trie | insert / search / prefix | O(length of the word) | 33 |
| Fenwick / segment tree | point update + range query | O(log n) | 34 |
| union-find | union, "same group?" | ~O(1) amortised | 39 |
| adjacency list (graph) | list a vertex's neighbours | O(degree); space O(V + E) | 35 |

## Clue words → pattern [49]

| The problem says… | Try | Typical cost |
|---|---|---|
| "sorted array", "pair", "palindrome", "in place" | two pointers [7] | O(n) |
| "contiguous subarray / substring", "longest / shortest window", "k consecutive" | sliding window [8] | O(n) |
| "sum of a range", many range queries | prefix sums [9] | O(n) build, O(1) query |
| "subarray sum equals k" with negatives | prefix sums + hash map [14] | O(n) |
| "seen before", "duplicate", "count", "frequency", "anagram", "pair sum" (unsorted) | hash map / set [14] | O(n) |
| "grid", "neighbours", "rotate", "spiral" | 2-D indexing with direction lists [10] | O(rows × cols) |
| "find a pattern in text" | `in` / `find`; KMP or Rabin-Karp [12] | O(n + m) |
| "matching brackets", "nested", "undo" | stack [17] | O(n) |
| "next greater / smaller", "span", "histogram" | monotonic stack [18] | O(n) |
| "maximum of every window" | monotonic deque [19] | O(n) |
| "least recently used", "evict" | dict + doubly linked list [20] | O(1) per operation |
| "all subsets / permutations / combinations", "place n queens" | backtracking [23] | exponential |
| "sorted", "find the position / first / last" | binary search [24] | O(log n) |
| "minimise the maximum", "smallest x such that…" | binary search on the answer [25] | O(log range × check) |
| "k-th largest", "top k", "k closest", "merge k sorted" | heap [32] | O(n log k) |
| "running median" | two heaps [32] | O(log n) per item |
| "prefix", "autocomplete", "word dictionary" | trie [33] | O(word length) |
| "range sum / min with updates" | Fenwick or segment tree [34] | O(log n) |
| "islands", "connected", "can reach" | DFS / BFS [35] | O(V + E) |
| "shortest path", "fewest steps" (unweighted) | BFS [36] | O(V + E) |
| "prerequisites", "order of tasks", "dependencies" | topological sort [37] | O(V + E) |
| "cheapest", "weighted shortest path" | Dijkstra [38] (Bellman-Ford if negative) | O((V + E) log V) |
| "merge groups", "redundant connection", "connect everything cheaply" | union-find, MST [39] | ~O(E log E) |
| "number of ways", "min cost", "is it possible", choices that affect later choices | dynamic programming [41–44] | states × transitions |
| "earliest end", "most non-overlapping", "always take the best now" (provably) | greedy [45] | O(n log n) |
| "intervals", "meetings", "overlap", "rooms" | sort + sweep, heap of ends [46] | O(n log n) |
| "appears once, others twice", "subsets of ≤ 20 items" | bit manipulation [47] | O(n), O(2ⁿ) |
| "modulo 10⁹ + 7", "primes", "gcd", "choose k" | number theory [48] | varies |

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

**Binary search, first position where `ok` is true [24, 25]**
```python
lo, hi = 0, len(a)                           # or the range of possible answers
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid): hi = mid
    else: lo = mid + 1
return lo
```

**Monotonic stack: next greater element [18]**
```python
result, stack = [-1] * len(a), []            # stack holds indexes still waiting for an answer
for i, x in enumerate(a):
    while stack and a[stack[-1]] < x:
        result[stack.pop()] = x
    stack.append(i)
```

**Backtracking [23]**
```python
def backtrack(path, choices):
    if is_complete(path): results.append(path[:]); return
    for c in choices:
        if allowed(c):
            path.append(c)                   # choose
            backtrack(path, next_choices)    # explore
            path.pop()                       # un-choose
```

**Tree recursion: ask the children, combine [29, 30]**
```python
def solve(node):
    if node is None: return base_value
    left, right = solve(node.left), solve(node.right)
    return combine(node.val, left, right)
```

**Heap: top k [32]**
```python
heap = []
for x in data:
    heapq.heappush(heap, x)
    if len(heap) > k: heapq.heappop(heap)    # drop the smallest: the k largest remain
```

**BFS (shortest steps) [35, 36]**
```python
dist, queue = {start: 0}, deque([start])
while queue:
    u = queue.popleft()
    for v in neighbours(u):
        if v not in dist:                    # mark when queued
            dist[v] = dist[u] + 1; queue.append(v)
```

**Iterative DFS / flood fill [35]**
```python
seen, stack = {start}, [start]
while stack:
    u = stack.pop()
    for v in neighbours(u):
        if v not in seen: seen.add(v); stack.append(v)
```

**Topological sort, Kahn [37]**
```python
ready = deque(v for v in range(n) if indegree[v] == 0); order = []
while ready:
    u = ready.popleft(); order.append(u)
    for v in graph[u]:
        indegree[v] -= 1
        if indegree[v] == 0: ready.append(v)
# len(order) < n means a cycle
```

**Dijkstra [38]**
```python
dist, heap = {s: 0}, [(0, s)]
while heap:
    d, u = heapq.heappop(heap)
    if d > dist.get(u, inf): continue       # stale entry
    for v, w in graph[u]:
        if d + w < dist.get(v, inf):
            dist[v] = d + w; heapq.heappush(heap, (d + w, v))
```

**Union-find [39]**
```python
parent = list(range(n))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]   # path halving
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: return False                # already connected (a cycle, if adding edges)
    parent[ra] = rb; return True
```

**Dynamic programming [41–44]**
```python
dp = [base] * (n + 1)                        # 1. state: what dp[i] means, in words
dp[0] = ...                                  # 3. base cases
for i in range(1, n + 1):                    # 4. an order where dependencies are ready
    dp[i] = best_of(dp[i - 1], dp[i - 2] + cost[i])   # 2. transition
return dp[n]                                 # 5. answer

for wt, val in items:                        # 0/1 knapsack: capacities DOWNWARDS
    for w in range(W, wt - 1, -1):
        dp[w] = max(dp[w], dp[w - wt] + val)
```

**Intervals [46]**
```python
merged = []
for s, e in sorted(intervals):
    if merged and s <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], e)
    else: merged.append([s, e])
```

## Sorting algorithms [26–28]

| Algorithm | Best | Average | Worst | Space | Stable |
|---|---|---|---|---|---|
| Bubble / insertion | O(n) | O(n²) | O(n²) | O(1) | yes |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | no |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | yes |
| Quicksort (random pivot) | O(n log n) | O(n log n) | O(n²) | O(log n) | no |
| Heap sort | O(n log n) | O(n log n) | O(n log n) | O(1) | no |
| Counting / radix | O(n + k) | O(n + k) | O(n + k) | O(n + k) | yes |
| Python's `sorted` (Timsort) | O(n) | O(n log n) | O(n log n) | O(n) | yes |

## Graph algorithms [35–40]

| Task | Algorithm | Time |
|---|---|---|
| Reachability, components | DFS / BFS | O(V + E) |
| Shortest path, unweighted / 0-1 weights | BFS / 0-1 BFS | O(V + E) |
| Shortest path, non-negative weights | Dijkstra | O((V + E) log V) |
| Shortest path, negative weights | Bellman-Ford | O(V · E) |
| All pairs | Floyd-Warshall | O(V³) |
| Order with dependencies | topological sort | O(V + E) |
| Minimum spanning tree | Kruskal / Prim | O(E log E) |
| Strongly connected components | Kosaraju / Tarjan | O(V + E) |
| Bridges, articulation points | Tarjan low-link | O(V + E) |
| Maximum flow | Edmonds-Karp | O(V · E²) |

## Edge cases to always test

Empty input · one item · two items · all the same · already sorted / reverse sorted · negatives and zero · duplicates · the answer at the very start or end · no valid answer · very large input (speed).
