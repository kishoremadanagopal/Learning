@@@ part
id: 9
title: Dynamic Programming and Greedy
level: Advanced
blurb: Solving problems by reusing answers to smaller ones: memoisation and tabulation, the classic 1-D and 2-D dynamic programs, knapsacks, interval and bitmask DP, greedy algorithms and how to tell when they work, and interval problems with sweep lines.

@@@ lesson
id: dp-intro
title: Dynamic programming foundations
minutes: 26
summary: What makes a problem a dynamic program (overlapping subproblems and optimal substructure), memoisation versus tabulation, the five-step DP recipe, shrinking the table to a few variables, and the first classics: climbing stairs, minimum-cost stairs and house robber.
---
**Dynamic programming (DP)** solves a problem by combining the answers to **smaller versions of the same problem**, solving each smaller version only **once** and storing the result. Lesson 21 showed the idea on Fibonacci: naive recursion made millions of calls because it solved fib(3) and fib(2) over and over; remembering answers made it O(n).

A problem suits DP when it has both:

- **Overlapping subproblems:** the same smaller problems come up again and again. (Merge sort's halves never overlap, which is why it's divide and conquer, not DP.)
- **Optimal substructure:** the best answer is built from the best answers to subproblems. The cheapest route to the top of the stairs ends with the cheapest route to one of the last steps.

### Two ways to write it: top-down and bottom-up

```python
from functools import cache

# Top-down (memoisation): write the recursion, cache the answers
@cache
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)

# Bottom-up (tabulation): fill a table from the smallest case upwards
def fib_table(n):
    if n < 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]      # every value it needs is already in the table
    return dp[n]

# Bottom-up with O(1) space: only the last two values are ever needed
def fib_two(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fib_memo(90), fib_table(90), fib_two(90))
print(len(str(fib_two(10_000))), "digits in fib(10,000)")
```

| | Top-down (memoisation) | Bottom-up (tabulation) |
|---|---|---|
| How | recursion + cache | loops filling a table |
| Computes | only the subproblems actually needed | every subproblem up to n |
| Easiest when | the recurrence is clear but the order isn't | the order of subproblems is simple |
| Limits | recursion depth (see below) | none from the stack |
| Space savings | hard | easy: keep only the rows or values still needed |

**Recursion depth:** a top-down solution for n = 5,000 needs about 5,000 nested calls. Desktop Python stops at about 1,000 (`RecursionError`); in this browser sandbox, recursion through `@cache` stops at about 500, because each call adds the cache's own frame. So memoise for small inputs or when only some subproblems matter, and **tabulate** when n is large.

### The DP recipe

1. **State:** define, in words, what one table entry means. "`dp[i]` = the number of ways to reach step i." Most of the difficulty is here.
2. **Transition (recurrence):** how an entry follows from smaller ones. "`dp[i] = dp[i − 1] + dp[i − 2]`."
3. **Base cases:** the smallest entries you know directly. "`dp[0] = 1`."
4. **Order:** compute entries so that everything an entry needs is already done (usually increasing i).
5. **Answer:** which entry, or which combination of entries, answers the question. "`dp[n]`."

Then ask whether you can **save space**: if `dp[i]` only looks back a fixed number of steps, keep just those values.

### Climbing stairs

You climb n steps, taking 1 or 2 at a time. In how many different ways can you reach the top? The **last** move was either a 1-step from step n − 1 or a 2-step from step n − 2, so `ways(n) = ways(n − 1) + ways(n − 2)`: Fibonacci in disguise.

![A row of steps 0 to 5 with the number of ways to reach each: 1, 1, 2, 3, 5, 8. Arrows into step 5 come from step 4 (one step) and step 3 (two steps), showing 8 = 5 + 3](figures/stairs-dp.svg)

```python
def climb(n):
    dp = [0] * (n + 1)
    dp[0] = 1                       # one way to stand at the bottom: do nothing
    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + (dp[i - 2] if i >= 2 else 0)
    return dp

print(climb(10))
```

### Minimum cost climbing stairs

`cost[i]` is the price of stepping on step i; you may start on step 0 or 1 and want to get past the last step as cheaply as possible, moving 1 or 2 steps at a time. State: `dp[i]` = the cheapest total to **arrive** at step i. You arrive from i − 1 or i − 2, paying for the step you left.

```python
def min_cost(cost):
    n = len(cost)
    dp = [0] * (n + 1)              # dp[0] = dp[1] = 0: you may start on either for free
    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
    return dp[n]                    # "past the end" is position n

print(min_cost([10, 15, 20]), min_cost([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]))
```

### House robber: take it or skip it

Houses in a row hold `nums[i]` money; you can't rob two neighbours. At each house there are two choices: **skip** it (keep the best up to the previous house) or **take** it (its money plus the best up to two houses back). That take-or-skip shape appears in countless DP problems. It's the first exercise.

### How to recognise a DP problem

- It asks for a **count** ("how many ways"), an **optimum** ("minimum cost", "longest", "maximum profit") or **feasibility** ("is it possible").
- Each decision **limits** future decisions, so a simple greedy choice might be wrong.
- Brute force would try every combination (2ⁿ subsets, every path), and the same partial situations repeat.
- Input sizes are moderate: n up to around 10⁴ for O(n²), or two sizes up to around 10³ for an O(n·m) table.

:::exercise Climbing stairs with any step sizes
Write `count_ways(n, steps)` returning how many different ordered sequences of moves reach exactly step `n`, where each move climbs one of the sizes in `steps` (a list of distinct positive integers). There's 1 way to reach step 0. It must handle n = 5,000 quickly: build a table with a loop (deep recursion won't fit).
```python starter
def count_ways(n, steps):
    pass

print(count_ways(4, [1, 2]))      # 5
print(count_ways(4, [1, 2, 3]))   # 7
```
```python check
fn = need("count_ways")
test(fn, cases=[
    ((4, [1, 2]), 5, "steps of 1 or 2"),
    ((4, [1, 2, 3]), 7, "steps of 1, 2 or 3"),
    ((0, [1, 2]), 1, "already at the top"),
    ((7, [2]), 0, "an odd height with only 2-steps"),
    ((10, [3, 5]), 1, "steps of 3 or 5: only 5 + 5 lands exactly on 10"),
    ((5, [1, 5]), 2, "a single 5-step or five 1-steps"),
    ((30, [1, 2]), 1346269, "a larger staircase"),
])
def _ref(n, steps):
    dp = [0] * (n + 1); dp[0] = 1
    for i in range(1, n + 1):
        dp[i] = sum(dp[i - s] for s in steps if s <= i)
    return dp[n]
speed(fn, lambda n: (n, [1, 2, 3]), _ref, sizes=(10, 23, 5_000), what="steps",
      tip="Plain recursion recomputes the same steps exponentially often, and even memoised recursion goes n calls deep. Fill a table bottom-up: ways[i] = sum of ways[i - s] for each step size s.")
```
```python solution
def count_ways(n, steps):
    ways = [0] * (n + 1)
    ways[0] = 1                          # one way to be at the bottom: make no moves
    for i in range(1, n + 1):
        for s in steps:
            if s <= i:
                ways[i] += ways[i - s]   # the last move was a step of size s
    return ways[n]

print(count_ways(4, [1, 2]))
print(count_ways(4, [1, 2, 3]))
```
```python slow
def count_ways(n, steps):
    if n == 0:
        return 1
    return sum(count_ways(n - s, steps) for s in steps if s <= n)
```
hint: Think about the **last** move. If it was a step of size s, where were you just before it?
hint: You were at step n − s. So the number of ways to reach n is the sum of the ways to reach n − s, over every step size s that fits.
hint: `ways = [0] * (n + 1); ways[0] = 1`; for i from 1 to n, add `ways[i - s]` for each `s <= i`. Return `ways[n]`.
approach:
1. **Understand:** ordered sequences (1 + 2 and 2 + 1 are different); exactly n; n = 0 → 1.
2. **Examples:** n = 4 with [1, 2] → 5: 1111, 112, 121, 211, 22.
3. **Brute force:** recursion over the first move: correct but exponential, since the same heights are recomputed.
4. **Pattern:** **1-D DP**: state `ways[i]`, transition = sum over the last move.
5. **Plan:** a table of size n + 1, base `ways[0] = 1`, fill upwards, return `ways[n]`.
6. **Code and test:** n = 0, impossible heights, a single big step.
walkthrough:
**Line by line**

- `ways[i]` means "the number of move sequences that end exactly at step i".
- `ways[0] = 1` is the empty sequence. Without it, every count would stay 0.
- For each i, every allowed last step s contributes all the ways of reaching i − s.
- Filling i in increasing order guarantees `ways[i - s]` is already final.

**Trace** for n = 4, steps [1, 2, 3]:

| i | from i−1 | from i−2 | from i−3 | ways[i] |
|---|---|---|---|---|
| 0 | | | | 1 |
| 1 | 1 | | | 1 |
| 2 | 1 | 1 | | 2 |
| 3 | 2 | 1 | 1 | 4 |
| 4 | 4 | 2 | 1 | **7** |

**Complexity:** O(n × k) time for k step sizes, O(n) space (O(max step) if you keep only a sliding window).

**Common wrong approach:** looping over step sizes in the **outer** loop and heights in the inner loop. That counts **combinations** (1 + 2 and 2 + 1 once) instead of ordered sequences; it's the right order for coin change "number of ways" (next lesson), not here.
:::

:::exercise House robber
Houses in a row contain `nums[i]` money (non-negative). You can't rob two **adjacent** houses. Write `rob(nums)` returning the most money you can take. It must handle 100,000 houses quickly.
```python starter
def rob(nums):
    pass

print(rob([1, 2, 3, 1]))       # 4: houses 0 and 2
print(rob([2, 7, 9, 3, 1]))    # 12: houses 0, 2 and 4
```
```python check
fn = need("rob")
test(fn, cases=[
    (([1, 2, 3, 1],), 4, "the first example"),
    (([2, 7, 9, 3, 1],), 12, "the second example"),
    (([],), 0, "no houses"),
    (([5],), 5, "one house"),
    (([2, 1, 1, 2],), 4, "skipping two houses in a row"),
    (([0, 0, 0],), 0, "all empty"),
    (([10, 1, 1, 10, 1, 1, 10],), 30, "big houses three apart"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    return ([rng.randint(0, 100) for _ in range(n)],)
def _ref(nums):
    a = b = 0
    for x in nums:
        a, b = b, max(b, a + x)
    return b
speed(fn, _make, _ref, sizes=(10, 31, 100_000), what="houses",
      tip="Trying both choices at every house recursively is exponential, and recursion can't go 100,000 deep anyway. Keep two running values: the best up to the previous house and the best up to the one before it.")
```
```python solution
def rob(nums):
    prev2 = 0          # best total up to two houses back
    prev1 = 0          # best total up to the previous house
    for money in nums:
        take = prev2 + money            # rob this house: can't have robbed the previous one
        skip = prev1                    # leave it: keep the best so far
        prev2, prev1 = prev1, max(take, skip)
    return prev1

print(rob([1, 2, 3, 1]))
print(rob([2, 7, 9, 3, 1]))
```
```python slow
def rob(nums, i=0):
    if i >= len(nums):
        return 0
    return max(rob(nums, i + 1), nums[i] + rob(nums, i + 2))
```
hint: At each house you have two choices. What are they, and what does each one allow at the previous house?
hint: Let `best[i]` be the most you can take from the first i + 1 houses. Either skip house i (`best[i − 1]`) or rob it (`best[i − 2] + nums[i]`); take the larger.
hint: You only ever look back two houses, so keep two variables `prev2` and `prev1`. For each house: `prev2, prev1 = prev1, max(prev1, prev2 + money)`. Return `prev1`.
approach:
1. **Understand:** no two neighbours; amounts ≥ 0; empty list → 0.
2. **Examples:** [2, 7, 9, 3, 1] → 2 + 9 + 1 = 12.
3. **Brute force:** recursion that tries rob/skip at every house: O(2ⁿ).
4. **Pattern:** **1-D DP, take or skip**: `best[i] = max(best[i−1], best[i−2] + nums[i])`.
5. **Plan:** two rolling variables instead of a whole table.
6. **Code and test:** empty, one house, the best plan skipping two houses in a row.
walkthrough:
**Line by line**

- `prev1` is the best total over the houses so far; `prev2` the best total excluding the most recent house.
- `take` adds this house to a plan that didn't use the previous house; `skip` keeps the best plan so far.
- The tuple assignment shifts the window forward by one house.
- Starting both at 0 handles the empty list and the first two houses without special cases.

**Trace** on [2, 7, 9, 3, 1]:

| money | take (prev2 + money) | skip (prev1) | prev2, prev1 after |
|---|---|---|---|
| 2 | 2 | 0 | 0, 2 |
| 7 | 7 | 2 | 2, 7 |
| 9 | 11 | 7 | 7, 11 |
| 3 | 10 | 11 | 11, 11 |
| 1 | 12 | 11 | 11, **12** |

**Complexity:** O(n) time, O(1) space.

**Common wrong approach:** summing the even-indexed or the odd-indexed houses and taking the larger; [2, 1, 1, 2] has a best of 4 using houses 0 and 3.
:::

:::quiz
? Which two properties make a problem suitable for dynamic programming?
+ Overlapping subproblems and optimal substructure
- Sorted input and small numbers
- Recursion and a hash table
= Subproblems repeat, and the best answer is built from the best answers to subproblems.
? What is the main practical risk of top-down (memoised) DP in Python for large n?
+ Exceeding the recursion depth limit
- It gives wrong answers
- It uses less memory than tabulation
= Each level is a nested call; bottom-up loops have no such limit.
? In the DP recipe, which step usually takes the most thought?
+ Defining the state: what one table entry means
- Choosing a variable name
- Printing the answer
= Once dp[i] has a precise meaning, the transition usually follows.
? House robber looks back two houses. How much memory does the optimised version need?
+ O(1): two variables
- O(n)
- O(n²)
= Keep only the values the transition still needs.
:::

@@@ lesson
id: dp-sequences
title: DP on sequences
minutes: 28
summary: The classic one-dimensional dynamic programs: fewest coins and number of ways to make change (and why loop order matters), maximum subarray with Kadane's algorithm, longest increasing subsequence in O(n²) and O(n log n), word break and decode ways.
---
Many DP problems walk along a sequence (amounts, positions in a list, characters in a string) where `dp[i]` summarises everything about the first i items or the amount i. This lesson collects the patterns you'll meet most.

### Coin change: the fewest coins

Given coin values (with unlimited coins of each) and an amount, find the fewest coins that add up to it. State: `dp[a]` = fewest coins for amount a. The last coin used was some c, so `dp[a] = 1 + min(dp[a − c])` over the coins that fit.

```python
def fewest_coins(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount               # dp[0] = 0: no coins needed for 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1

print(fewest_coins([1, 3, 4], 6))      # 3 + 3
print(fewest_coins([2], 3))            # impossible
print(fewest_coins([1, 5, 10, 25], 63))
```

Why not just take the biggest coin each time? That **greedy** approach works for coin systems like 1, 5, 10, 25 but fails in general: with coins 1, 3, 4 and amount 6, greedy picks 4 + 1 + 1 (3 coins) while 3 + 3 uses 2. DP checks every last coin, so it's always right. (Lesson 45 shows when greedy is safe.)

### Coin change: the number of ways, and why loop order matters

"How many ways to make amount a?" counts **combinations** (2 + 1 and 1 + 2 are the same way) if you loop over **coins on the outside**: each coin is added to the counts only after the previous coins are finished, so coins always appear in one fixed order. Swap the loops and you count **ordered sequences** instead (like the stairs exercise).

```python
def ways_combinations(coins, amount):
    dp = [1] + [0] * amount
    for c in coins:                         # coins outside: each combination counted once
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]

def ways_sequences(coins, amount):
    dp = [1] + [0] * amount
    for a in range(1, amount + 1):          # amounts outside: every order counted
        for c in coins:
            if c <= a:
                dp[a] += dp[a - c]
    return dp[amount]

print(ways_combinations([1, 2, 5], 5), ways_sequences([1, 2, 5], 5))
```

### Maximum subarray: Kadane's algorithm

The largest sum of a **contiguous** run of numbers. State: `best_here` = the largest sum of a subarray **ending at** the current position. Either extend the previous run or start fresh at this number: `best_here = max(x, best_here + x)`. The answer is the largest `best_here` seen.

```python
def max_subarray(nums):
    best_here = best = nums[0]
    for x in nums[1:]:
        best_here = max(x, best_here + x)   # a negative running sum is worth dropping
        best = max(best, best_here)
    return best

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))   # 4 - 1 + 2 + 1
print(max_subarray([-3, -1, -2]))                      # all negative: the largest single number
```

"Ending at i" is one of the most useful state definitions: it turns "best subarray anywhere" into a simple left-to-right pass. For the maximum **product**, track both the largest and the smallest product ending here, because a negative number turns the smallest into the largest.

### Longest increasing subsequence (LIS)

A **subsequence** keeps the original order but may skip items: [3, 10, 2, 1, 20] contains the increasing subsequence 3, 10, 20 of length 3.

**O(n²) DP:** `dp[i]` = length of the longest increasing subsequence **ending at** i = 1 + the best `dp[j]` over earlier j with a smaller value.

```python
def lis_quadratic(nums):
    n = len(nums)
    dp, parent = [1] * n, [-1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i], parent[i] = dp[j] + 1, j
    end = max(range(n), key=dp.__getitem__)
    seq = []
    while end != -1:                        # follow parents to rebuild one LIS
        seq.append(nums[end])
        end = parent[end]
    return len(seq), seq[::-1]

print(lis_quadratic([10, 9, 2, 5, 3, 7, 101, 18]))
```

**O(n log n) with patience sorting:** keep a list `tails` where `tails[k]` is the **smallest possible last value** of an increasing subsequence of length k + 1. It's always sorted, so each new number finds its place by binary search: replace the first tail ≥ it, or append if it's bigger than all of them. The answer is `len(tails)`.

![Processing 10, 9, 2, 5, 3, 7, 101, 18. The tails list changes: [10], [9], [2], [2, 5], [2, 3], [2, 3, 7], [2, 3, 7, 101], [2, 3, 7, 18]. Its final length 4 is the LIS length](figures/lis-tails.svg)

```python
from bisect import bisect_left

def lis_length(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)           # the first tail >= x
        if i == len(tails):
            tails.append(x)                 # x extends the longest subsequence so far
        else:
            tails[i] = x                    # x is a smaller ending for length i + 1
        print(f"{x:>4}: {tails}")
    return len(tails)

print("length:", lis_length([10, 9, 2, 5, 3, 7, 101, 18]))
```

`tails` is **not** itself an increasing subsequence of the input (its values may come from different subsequences); only its length is the answer. For **non-decreasing** subsequences, use `bisect_right`.

### Word break

Can a string be split into dictionary words? State: `ok[i]` = the first i characters can be split. `ok[i]` is true if some earlier split point j has `ok[j]` true and `s[j:i]` is a word.

```python
def word_break(s, words):
    words = set(words)
    longest = max(map(len, words), default=0)
    ok = [True] + [False] * len(s)              # the empty prefix can always be split
    for i in range(1, len(s) + 1):
        for j in range(max(0, i - longest), i): # only look back as far as the longest word
            if ok[j] and s[j:i] in words:
                ok[i] = True
                break
    return ok[len(s)]

print(word_break("applepenapple", ["apple", "pen"]), word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))
```

### Decode ways

Letters are encoded A = 1, …, Z = 26. How many ways can a digit string be decoded? "226" is BZ, VF or BBF. State: `dp[i]` = ways to decode the first i digits. The last letter used either one digit (1–9) or two digits (10–26).

```python
def decode_ways(s):
    dp = [1] + [0] * len(s)
    for i in range(1, len(s) + 1):
        if s[i - 1] != "0":
            dp[i] += dp[i - 1]                       # last letter from one digit
        if i >= 2 and "10" <= s[i - 2:i] <= "26":
            dp[i] += dp[i - 2]                       # last letter from two digits
    return dp[len(s)]

print(decode_ways("226"), decode_ways("12"), decode_ways("06"), decode_ways("11106"))
```

(The string comparison `"10" <= s[i-2:i] <= "26"` works because both sides are two-digit strings.)

:::exercise Coin change
Write `coin_change(coins, amount)` returning the **fewest** coins that add up to `amount` (unlimited coins of each value), or `-1` if it can't be done. It must handle amount = 10,000 quickly.
```python starter
def coin_change(coins, amount):
    pass

print(coin_change([1, 2, 5], 11))   # 3: 5 + 5 + 1
print(coin_change([2], 3))          # -1
```
```python check
fn = need("coin_change")
test(fn, cases=[
    (([1, 2, 5], 11), 3, "the example"),
    (([2], 3), -1, "impossible"),
    (([1], 0), 0, "amount zero"),
    (([1, 3, 4], 6), 2, "greedy would use 3 coins"),
    (([25, 10, 1], 30), 3, "10 + 10 + 10 beats 25 + five 1s"),
    (([5, 7], 1), -1, "every coin is too big"),
    (([2, 5, 10, 1], 27), 4, "unsorted coins"),
])
def _ref(coins, amount):
    INF = float("inf"); dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]: dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1
speed(fn, lambda n: ([1, 3, 4], n), _ref, sizes=(10, 29, 10_000), what="as the amount",
      tip="Trying every first coin recursively is exponential. Build dp[a] = fewest coins for amount a, from 0 up to the target: dp[a] = 1 + min(dp[a - c]).")
```
```python solution
def coin_change(coins, amount):
    INF = float("inf")
    fewest = [0] + [INF] * amount            # fewest[a]: fewest coins that make amount a
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and fewest[a - c] + 1 < fewest[a]:
                fewest[a] = fewest[a - c] + 1    # use c as the last coin
    return fewest[amount] if fewest[amount] != INF else -1

print(coin_change([1, 2, 5], 11))
print(coin_change([2], 3))
```
```python slow
def coin_change(coins, amount):
    if amount == 0:
        return 0
    best = -1
    for c in coins:
        if c <= amount:
            rest = coin_change(coins, amount - c)
            if rest != -1 and (best == -1 or rest + 1 < best):
                best = rest + 1
    return best
```
hint: Suppose you knew the fewest coins for every smaller amount. Which coin might be the **last** one used for `amount`?
hint: Any coin c that fits. Then the count is 1 + the fewest coins for `amount − c`. Take the smallest over all coins.
hint: `fewest = [0] + [inf] * amount`; for each a from 1 up, for each coin c ≤ a, update `fewest[a] = min(fewest[a], fewest[a - c] + 1)`. Return −1 if it's still infinity.
approach:
1. **Understand:** unlimited coins; fewest count; amount 0 → 0; impossible → −1.
2. **Examples:** [1, 2, 5], 11 → 3; [1, 3, 4], 6 → 2 (not 3, as greedy would say).
3. **Brute force:** recursion over the last coin: exponential, recomputing the same amounts.
4. **Pattern:** **1-D DP over amounts** (unbounded knapsack, minimum version).
5. **Plan:** table of size amount + 1 with infinity; fill upwards; translate infinity to −1.
6. **Code and test:** 0, impossible, greedy traps, unsorted coins.
walkthrough:
**Line by line**

- `fewest[0] = 0` is the base case; every other amount starts as "impossible" (infinity).
- For amount a, each coin c ≤ a offers the candidate `fewest[a - c] + 1`; if a − c is impossible, infinity + 1 is still infinity, so it never wins.
- Amounts are filled in increasing order, so `fewest[a - c]` is final when used.
- The final translation turns "still infinity" into −1.

**Trace** for coins [1, 3, 4], amount 6:

| a | via 1 | via 3 | via 4 | fewest[a] |
|---|---|---|---|---|
| 1 | 1 | — | — | 1 |
| 2 | 2 | — | — | 2 |
| 3 | 3 | 1 | — | 1 |
| 4 | 2 | 2 | 1 | 1 |
| 5 | 2 | 3 | 2 | 2 |
| 6 | 3 | **2** | 3 | 2 |

**Complexity:** O(amount × number of coins) time, O(amount) space.

**Common wrong approach:** greedy (largest coin first), which fails on [1, 3, 4] with amount 6.
:::

:::exercise Longest increasing subsequence
Write `length_of_lis(nums)` returning the length of the longest **strictly** increasing subsequence. It must be O(n log n): 100,000 numbers in well under a second.
```python starter
from bisect import bisect_left

def length_of_lis(nums):
    pass

print(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]))   # 4: 2, 3, 7, 101
```
```python check
fn = need("length_of_lis")
test(fn, cases=[
    (([10, 9, 2, 5, 3, 7, 101, 18],), 4, "the example"),
    (([0, 1, 0, 3, 2, 3],), 4, "0, 1, 2, 3"),
    (([7, 7, 7, 7],), 1, "equal numbers don't count as increasing"),
    (([],), 0, "an empty list"),
    (([5],), 1, "one number"),
    (([5, 4, 3, 2, 1],), 1, "decreasing"),
    (([1, 3, 6, 7, 9, 4, 10, 5, 6],), 6, "a dip in the middle"),
    (([-2, -1, -5, 0, -3, 1],), 4, "negative numbers"),
])
import random as _random
from bisect import bisect_left as _bl
def _make(n):
    rng = _random.Random(n)
    return ([rng.randint(0, 10**6) for _ in range(n)],)
def _ref(nums):
    t = []
    for x in nums:
        i = _bl(t, x)
        if i == len(t): t.append(x)
        else: t[i] = x
    return len(t)
speed(fn, _make, _ref, sizes=(1_000, 5_000, 100_000), what="numbers",
      tip="Comparing every pair is O(n^2). Keep tails[k] = the smallest last value of an increasing subsequence of length k + 1, and place each number with bisect_left.")
```
```python solution
from bisect import bisect_left

def length_of_lis(nums):
    tails = []                        # tails[k]: smallest ending of an increasing subsequence of length k + 1
    for x in nums:
        i = bisect_left(tails, x)     # first position whose tail is >= x
        if i == len(tails):
            tails.append(x)           # longer than every subsequence so far
        else:
            tails[i] = x              # a smaller ending for subsequences of length i + 1
    return len(tails)

print(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]))
```
```python slow
def length_of_lis(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)
```
hint: The O(n²) DP sets `dp[i]` = 1 + the best `dp[j]` for earlier, smaller `nums[j]`. To go faster, what do you really need to remember about the subsequences so far?
hint: For each possible length, only the **smallest ending value** matters: a smaller ending is easier to extend. Those smallest endings (`tails`) are always sorted.
hint: For each x: `i = bisect_left(tails, x)`. If `i == len(tails)` append x, otherwise set `tails[i] = x`. Return `len(tails)`.
approach:
1. **Understand:** subsequence (gaps allowed, order kept); strictly increasing; only the length is needed.
2. **Examples:** [0, 1, 0, 3, 2, 3] → 4; [7, 7, 7] → 1.
3. **Brute force:** all 2ⁿ subsequences; the O(n²) DP is the standard improvement.
4. **Pattern:** **patience sorting**: a sorted `tails` list with binary search.
5. **Plan:** one pass, bisect_left, replace or append, return the length.
6. **Code and test:** equal values (need `bisect_left`), empty input, decreasing input.
walkthrough:
**Line by line**

- `tails[k]` is the smallest value that can end an increasing subsequence of length k + 1 among the numbers seen so far. These values increase with k, so the list is sorted.
- `bisect_left` finds the first tail ≥ x. If none exists, x extends the longest subsequence: append.
- Otherwise x becomes a smaller (better) ending for that length. The length of `tails` never shrinks, and only grows when a longer subsequence really exists.
- `bisect_left` (not `bisect_right`) makes an equal value replace its twin rather than extend, which enforces **strictly** increasing.

**Trace** on [0, 1, 0, 3, 2, 3]:

| x | position | tails |
|---|---|---|
| 0 | append | [0] |
| 1 | append | [0, 1] |
| 0 | replace 0 | [0, 1] |
| 3 | append | [0, 1, 3] |
| 2 | replace 3 | [0, 1, 2] |
| 3 | append | [0, 1, 2, 3] → **4** |

**Complexity:** O(n log n) time, O(n) space.

**Common wrong approach:** returning `tails` as the subsequence itself. Its values can come from different subsequences; rebuilding an actual LIS needs extra parent pointers.
:::

:::quiz
? With coins [1, 3, 4] and amount 6, what does always taking the largest coin give?
+ 3 coins (4 + 1 + 1), while the best is 2 (3 + 3)
- 2 coins, the best answer
- No answer
= Greedy isn't safe for every coin system; DP checks every last coin.
? To count coin combinations (order doesn't matter), which loop goes outside?
+ The loop over coin values
- The loop over amounts
- It makes no difference
= With amounts outside, 1 + 2 and 2 + 1 are counted separately.
? In Kadane's algorithm, what does best_here represent?
+ The largest sum of a subarray ending at the current position
- The largest sum seen anywhere so far
- The sum of all positive numbers
= Each step either extends the previous run or starts again at x.
? In the O(n log n) LIS method, what does tails[k] hold?
+ The smallest last value of an increasing subsequence of length k + 1
- The k-th number of the longest subsequence
- The count of subsequences of length k
= Smaller endings are easier to extend, and the list stays sorted.
:::

@@@ lesson
id: dp-grids-strings
title: DP on grids and strings
minutes: 28
summary: Two-dimensional dynamic programs: counting and costing paths through a grid, saving memory with one row, the longest common subsequence and rebuilding it, edit distance (Levenshtein) and where it's used, and palindromic subsequences and substrings.
---
When the state needs **two** numbers (a row and a column, or a position in each of two strings), the table becomes 2-D: `dp[i][j]`. The recipe is the same; the extra work is choosing the order so every cell's neighbours are ready.

### Paths through a grid

A robot starts at the top-left of an m × n grid and moves only **right** or **down**. How many different paths reach the bottom-right? Every cell is entered from above or from the left, so `paths[r][c] = paths[r − 1][c] + paths[r][c − 1]`.

```python
from math import comb

def unique_paths(m, n, blocked=()):
    paths = [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if (r, c) in blocked:
                continue                         # no path goes through an obstacle
            if r == 0 and c == 0:
                paths[r][c] = 1
            else:
                paths[r][c] = (paths[r - 1][c] if r else 0) + (paths[r][c - 1] if c else 0)
    return paths[m - 1][n - 1]

print(unique_paths(3, 7), comb(3 + 7 - 2, 3 - 1))    # with no obstacles it's a binomial coefficient
print(unique_paths(3, 3, blocked={(1, 1)}))
```

Without obstacles there's a formula: choose which m − 1 of the m + n − 2 moves go down. With obstacles, or costs, you need the DP.

**Minimum path sum:** each cell has a cost, and you want the cheapest right/down path. Same shape, with `min` instead of `+`: `cost[r][c] = grid[r][c] + min(from above, from the left)`. That's the first exercise. Rows only depend on the row above, so **one row of memory** is enough: overwrite it left to right.

```python
def min_path_one_row(grid):
    cols = len(grid[0])
    row = [float("inf")] * cols
    row[0] = 0
    for r in range(len(grid)):
        for c in range(cols):
            left = row[c - 1] if c else float("inf")
            row[c] = grid[r][c] + min(row[c], left)   # row[c] still holds the value from the row above
    return row[-1]

print(min_path_one_row([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))   # 1 → 3 → 1 → 1 → 1
```

### Longest common subsequence (LCS)

The longest sequence of characters appearing **in order** (gaps allowed) in both strings: "ABCBDAB" and "BDCABA" share "BCBA", length 4. State: `dp[i][j]` = LCS length of the first i characters of a and the first j characters of b.

- If `a[i−1] == b[j−1]`, that character extends the LCS of the shorter prefixes: `dp[i][j] = dp[i−1][j−1] + 1`.
- Otherwise drop the last character of one string or the other: `dp[i][j] = max(dp[i−1][j], dp[i][j−1])`.

![The LCS table for "ABCB" (rows) and "BDCB" (columns), with an extra row and column of zeros. Matching characters take the diagonal value plus one; others take the larger of the cell above and the cell to the left. The bottom-right cell is 3, and the highlighted path back through the matches spells "BCB"](figures/lcs-table.svg)

```python
def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]       # row 0 and column 0: empty prefixes
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    out, i, j = [], m, n                              # walk back from the corner to rebuild one LCS
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[m][n], "".join(reversed(out))

print(lcs("ABCBDAB", "BDCABA"))
print(lcs("kitten", "sitting"))
```

The **diff** tools in Git compare files line by line with algorithms based on this idea, and the same DP aligns DNA sequences in bioinformatics.

### Edit distance (Levenshtein distance)

The fewest **insertions, deletions and substitutions** that turn one string into another: "kitten" → "sitting" takes 3 (k→s, e→i, insert g). State: `dp[i][j]` = edits to turn the first i characters of a into the first j characters of b.

- Base cases: `dp[i][0] = i` (delete everything), `dp[0][j] = j` (insert everything).
- If the last characters match, no edit is needed: `dp[i][j] = dp[i−1][j−1]`.
- Otherwise 1 + the best of: **replace** (`dp[i−1][j−1]`), **delete** from a (`dp[i−1][j]`), **insert** into a (`dp[i][j−1]`).

It's the second exercise. Edit distance powers spell checkers ("did you mean…?"), fuzzy search, record de-duplication, and the **word error rate** used to score speech recognition and translation systems (edit distance counted in words instead of characters).

### Palindromes

The **longest palindromic subsequence** of s is the LCS of s and s reversed. The longest palindromic **substring** (contiguous) is easier without a table: expand outwards from each of the 2n − 1 possible centres, O(n²) time and O(1) space.

```python
def longest_palindrome_substring(s):
    best = ""
    for centre in range(2 * len(s) - 1):
        lo, hi = centre // 2, (centre + 1) // 2      # odd centres (a letter) and even centres (between letters)
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
            lo, hi = lo - 1, hi + 1
        if hi - lo - 1 > len(best):
            best = s[lo + 1:hi]
    return best

def lcs_length(a, b):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]

s = "character"
print(longest_palindrome_substring("babad"), longest_palindrome_substring("cbbd"))
print("longest palindromic subsequence of", s, "=", lcs_length(s, s[::-1]))   # "carac"
```

### Two-sequence DP in general

| Problem | dp[i][j] means | Match | No match |
|---|---|---|---|
| LCS | LCS of prefixes | dp[i−1][j−1] + 1 | max(dp[i−1][j], dp[i][j−1]) |
| Edit distance | edits between prefixes | dp[i−1][j−1] | 1 + min(three neighbours) |
| Distinct subsequences | ways b's prefix appears in a's prefix | dp[i−1][j−1] + dp[i−1][j] | dp[i−1][j] |
| Wildcard / regex match | does a's prefix match the pattern prefix | dp[i−1][j−1] | depends on `*` / `?` |

All are O(m × n) time; since each row only needs the previous one, space can drop to O(min(m, n)).

:::exercise Minimum path sum
`grid` is an m × n list of lists of non-negative integers. Starting at the top-left cell and moving only **right** or **down**, reach the bottom-right cell. Write `min_path_sum(grid)` returning the smallest possible sum of the cells on the path (including the first and last). It must handle a 300 × 300 grid quickly.
```python starter
def min_path_sum(grid):
    pass

print(min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))   # 7
```
```python check
fn = need("min_path_sum")
test(fn, cases=[
    (([[1, 3, 1], [1, 5, 1], [4, 2, 1]],), 7, "the example"),
    (([[1, 2, 3], [4, 5, 6]],), 12, "two rows"),
    (([[5]],), 5, "one cell"),
    (([[1, 2, 3, 4]],), 10, "one row"),
    (([[1], [2], [3]],), 6, "one column"),
    (([[0, 9, 0], [0, 9, 0], [0, 0, 0]],), 0, "a free route around the expensive middle"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    return ([[rng.randint(0, 9) for _ in range(n)] for _ in range(n)],)
def _ref(grid):
    row = [float("inf")] * len(grid[0]); row[0] = 0
    for r in grid:
        for c, v in enumerate(r):
            row[c] = v + min(row[c], row[c - 1] if c else float("inf"))
    return row[-1]
speed(fn, _make, _ref, sizes=(5, 12, 300), what="rows and columns",
      tip="Trying every right/down path recursively is exponential. Fill a table: cost[r][c] = grid[r][c] + min(cost above, cost to the left).")
```
```python solution
def min_path_sum(grid):
    rows, cols = len(grid), len(grid[0])
    cost = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                cost[r][c] = grid[0][0]
            elif r == 0:
                cost[r][c] = cost[r][c - 1] + grid[r][c]      # first row: only from the left
            elif c == 0:
                cost[r][c] = cost[r - 1][c] + grid[r][c]      # first column: only from above
            else:
                cost[r][c] = grid[r][c] + min(cost[r - 1][c], cost[r][c - 1])
    return cost[-1][-1]

print(min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))
```
```python slow
def min_path_sum(grid, r=0, c=0):
    rows, cols = len(grid), len(grid[0])
    if r == rows - 1 and c == cols - 1:
        return grid[r][c]
    best = float("inf")
    if r + 1 < rows:
        best = min(best, min_path_sum(grid, r + 1, c))
    if c + 1 < cols:
        best = min(best, min_path_sum(grid, r, c + 1))
    return grid[r][c] + best
```
hint: The last move into a cell came either from above or from the left. If you knew the cheapest cost to reach those two cells, what's the cheapest cost to reach this one?
hint: `cost[r][c] = grid[r][c] + min(cost[r−1][c], cost[r][c−1])`, filled row by row from the top-left. The first row and column have only one way in.
hint: Make a `cost` table the size of the grid. Handle (0, 0), the first row (from the left only) and the first column (from above only), then apply the formula everywhere else. Return the bottom-right entry.
approach:
1. **Understand:** right/down only; both end cells count; costs ≥ 0.
2. **Examples:** the example's best path 1 → 3 → 1 → 1 → 1 = 7.
3. **Brute force:** recursion over every path: C(m + n − 2, m − 1) paths, exponential.
4. **Pattern:** **2-D grid DP**: each cell from its top and left neighbours.
5. **Plan:** a cost table filled row by row; edges get one neighbour.
6. **Code and test:** one cell, one row, one column, a route around expensive cells.
walkthrough:
**Line by line**

- `cost[r][c]` means "the cheapest sum of a path from the top-left to (r, c), including both".
- Filling row by row, left to right, guarantees the cells above and to the left are already final.
- The first row can only be reached from the left, and the first column only from above, so they're running sums.
- The answer is the bottom-right entry.

**Trace** on [[1, 3, 1], [1, 5, 1], [4, 2, 1]]:

| | col 0 | col 1 | col 2 |
|---|---|---|---|
| row 0 | 1 | 4 | 5 |
| row 1 | 2 | 7 | 6 |
| row 2 | 6 | 8 | **7** |

**Complexity:** O(m × n) time; O(m × n) space as written, O(n) with a single row.

**Common wrong approach:** greedy, always stepping to the cheaper of the two next cells; a cheap step now can lead into an expensive region.
:::

:::exercise Edit distance
Write `edit_distance(a, b)` returning the fewest single-character **insertions, deletions or substitutions** needed to turn string `a` into string `b`. Two strings of 800 characters must take well under a second.
```python starter
def edit_distance(a, b):
    pass

print(edit_distance("horse", "ros"))              # 3
print(edit_distance("intention", "execution"))    # 5
```
```python check
fn = need("edit_distance")
test(fn, cases=[
    (("horse", "ros"), 3, "the first example"),
    (("intention", "execution"), 5, "the second example"),
    (("", "abc"), 3, "from empty: insert everything"),
    (("abc", ""), 3, "to empty: delete everything"),
    (("same", "same"), 0, "identical strings"),
    (("kitten", "sitting"), 3, "the classic example"),
    (("ab", "ba"), 2, "a swap costs two edits"),
    (("a", "b"), 1, "one substitution"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    return ("".join(rng.choice("abcd") for _ in range(n)), "".join(rng.choice("abcd") for _ in range(n)))
def _ref(a, b):
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] if a[i - 1] == b[j - 1] else 1 + min(prev[j], cur[j - 1], prev[j - 1])
        prev = cur
    return prev[-1]
speed(fn, _make, _ref, sizes=(6, 13, 800), what="characters in each string",
      tip="Trying all three edits recursively is exponential. Fill a (len(a) + 1) x (len(b) + 1) table: dp[i][j] = edits between the first i characters of a and the first j of b.")
```
```python solution
def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                      # delete all i characters
    for j in range(n + 1):
        dp[0][j] = j                      # insert all j characters
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]          # last characters match: free
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], # replace a's last character
                                   dp[i - 1][j],     # delete a's last character
                                   dp[i][j - 1])     # insert b's last character
    return dp[m][n]

print(edit_distance("horse", "ros"))
print(edit_distance("intention", "execution"))
```
```python slow
def edit_distance(a, b):
    if not a:
        return len(b)
    if not b:
        return len(a)
    if a[0] == b[0]:
        return edit_distance(a[1:], b[1:])
    return 1 + min(edit_distance(a[1:], b), edit_distance(a, b[1:]), edit_distance(a[1:], b[1:]))
```
hint: Look at the **last** characters of the two prefixes. If they're equal, what's the cost? If not, what are the three possible last edits?
hint: Let `dp[i][j]` be the edits between `a[:i]` and `b[:j]`. Equal last characters: `dp[i−1][j−1]`. Otherwise 1 + the minimum of replace `dp[i−1][j−1]`, delete `dp[i−1][j]` and insert `dp[i][j−1]`.
hint: The table is (m + 1) × (n + 1). Fill row 0 with 0..n and column 0 with 0..m, then fill the rest row by row and return `dp[m][n]`.
approach:
1. **Understand:** three operations, each costing 1; either string may be empty.
2. **Examples:** horse → ros: replace h with r, delete r, delete e = 3.
3. **Brute force:** recursion trying all three edits: exponential.
4. **Pattern:** **two-sequence DP** over prefixes.
5. **Plan:** base row and column, the match / three-way minimum rule, answer in the corner.
6. **Code and test:** empty strings, identical strings, a swap.
walkthrough:
**Line by line**

- `dp[i][0] = i` and `dp[0][j] = j` cover turning a prefix into nothing and nothing into a prefix.
- Equal last characters can be kept, so the cost is that of the shorter prefixes.
- Otherwise the last operation was a replace (both prefixes shrink), a delete (a's prefix shrinks) or an insert (b's prefix shrinks); add 1 to the cheapest.
- Row by row, left to right, makes the three neighbours ready.

**Trace** on "ab" → "ba" (rows: "", a, ab; columns: "", b, ba):

| | "" | b | ba |
|---|---|---|---|
| "" | 0 | 1 | 2 |
| a | 1 | 1 | 1 |
| ab | 2 | 1 | **2** |

**Complexity:** O(m × n) time; O(m × n) space, or O(n) keeping two rows.

**Common wrong approach:** counting the positions where the characters differ (Hamming distance). That ignores insertions and deletions: "abc" → "bc" is 1 edit, not 3.
:::

:::quiz
? In the grid "unique paths" DP, where does each cell's value come from?
+ The cell above plus the cell to the left
- The cell below plus the cell to the right
- Only the diagonal neighbour
= Moves are right or down, so each cell is entered from above or from the left.
? In the LCS table, what happens when a[i−1] == b[j−1]?
+ dp[i][j] = dp[i−1][j−1] + 1
- dp[i][j] = max(dp[i−1][j], dp[i][j−1])
- dp[i][j] = 0
= A shared last character extends the LCS of the shorter prefixes.
? Which three neighbours does edit distance compare when the last characters differ?
+ Replace (diagonal), delete (above) and insert (left)
- Only the diagonal
- The cells two steps away
= Each corresponds to the last edit made.
? Two-string DP tables need O(m × n) memory. How can you usually reduce that?
+ Keep only the previous row (and the current one)
- Sort the strings first
- Use recursion instead
= Each row depends only on the row above it.
:::

@@@ lesson
id: knapsack-and-more
title: Knapsacks, intervals, bitmasks and trees
minutes: 30
summary: The 0/1 and unbounded knapsack (and why the loop direction matters), subset sum and equal partition (with a big-integer bitset trick), pseudo-polynomial time, interval DP (matrix-chain order), bitmask DP for the travelling salesman problem, and DP on trees.
---
This lesson covers the DP families you'll meet after the sequence and grid classics. Each has a recognisable shape; once you know the shape, the code follows.

### 0/1 knapsack

Each item has a weight and a value, and the bag holds at most W. Each item can be taken **once or not at all** (hence 0/1). Maximise the total value. State: `dp[i][w]` = the best value using the first i items with capacity w. Item i is either skipped (`dp[i−1][w]`) or taken (`dp[i−1][w − weight] + value`).

```python
def knapsack_table(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = weights[i - 1], values[i - 1]
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]                                   # skip item i
            if wt <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wt] + val)     # take item i
    chosen, w = [], W                                                 # walk back to see which items were taken
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(i - 1)
            w -= weights[i - 1]
    return dp[n][W], sorted(chosen)

print(knapsack_table([1, 3, 4, 5], [1, 4, 5, 7], 7))      # items 1 and 2: weight 7, value 9
```

**One row is enough**, but you must loop capacities **downwards**. Going down, `dp[w − wt]` still holds the value from the previous item, so each item is used at most once. Going **upwards** would let the same item be added again and again, which is exactly the **unbounded** knapsack (and coin change).

```python
def knapsack_01(weights, values, W):
    dp = [0] * (W + 1)
    for wt, val in zip(weights, values):
        for w in range(W, wt - 1, -1):          # downwards: each item at most once
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[W]

def knapsack_unbounded(weights, values, W):
    dp = [0] * (W + 1)
    for wt, val in zip(weights, values):
        for w in range(wt, W + 1):              # upwards: an item can be reused
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[W]

print(knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7), knapsack_unbounded([1, 3, 4, 5], [1, 4, 5, 7], 7))
```

![Two one-row knapsack tables after adding an item of weight 2 and value 3 to an empty bag with capacity 6. Looping capacities downwards gives 0, 0, 3, 3, 3, 3, 3: the item is used once. Looping upwards gives 0, 0, 3, 3, 6, 6, 9: the item was reused because dp[w − 2] had already been updated](figures/knapsack-direction.svg)

**Pseudo-polynomial time:** O(n × W) looks polynomial, but W is a **number**, not a length: doubling the number of digits in W squares the work. That's why knapsack is NP-hard in general yet easy when capacities are moderate (up to around 10⁶).

### Subset sum and equal partition

"Can some of these numbers add up to exactly T?" is a knapsack where weight = value and only feasibility matters: `can[s]` = some subset sums to s, updated downwards for each number. "Can the list be split into two halves with equal sums?" is subset sum with T = total / 2 (and impossible if the total is odd).

Python's unlimited-size integers give a neat speed-up: store the reachable sums as **bits** of one integer. Adding a number x to every reachable sum is a single shift-and-OR, done by fast C code on whole machine words at a time:

```python
def subset_sums(nums):
    reach = 1                       # bit s is 1 if sum s is reachable; only 0 at first
    for x in nums:
        reach |= reach << x         # every old sum, plus the same sums with x added
    return reach

reach = subset_sums([3, 34, 4, 12, 5, 2])
print([s for s in range(15) if reach >> s & 1])
print("9 reachable?", bool(reach >> 9 & 1), "| 30 reachable?", bool(reach >> 30 & 1))
```

### Interval DP

When the answer for a range i..j comes from **splitting** it at some k and combining the two sides, the state is the interval: `dp[i][j]`. Compute **short intervals first**, so both sides of every split are ready.

The classic is **matrix-chain multiplication**: multiplying A (10 × 30), B (30 × 5) and C (5 × 60) costs 4,500 scalar multiplications as (AB)C but 27,000 as A(BC). Which order is cheapest for a long chain?

```python
def matrix_chain(dims):                      # matrix i has shape dims[i] x dims[i + 1]
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]         # dp[i][j]: cheapest cost to multiply matrices i..j
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):           # short intervals first
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):            # last multiplication: (i..k) times (k+1..j)
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if cost < dp[i][j]:
                    dp[i][j], split[i][j] = cost, k

    def brackets(i, j):
        if i == j:
            return "ABCDEFGH"[i]
        k = split[i][j]
        return f"({brackets(i, k)}{brackets(k + 1, j)})"
    return dp[0][n - 1], brackets(0, n - 1)

print(matrix_chain([10, 30, 5, 60]))
print(matrix_chain([40, 20, 30, 10, 30]))
```

O(n³) time, O(n²) space. The same shape solves bursting balloons, merging stones, optimal binary search trees and cutting a stick at chosen points.

### Bitmask DP: the travelling salesman

The **travelling salesman problem (TSP)**: the shortest tour visiting every city once and returning home. Trying all (n − 1)! orders is hopeless beyond about 11 cities. The **Held-Karp** DP stores, for each **set** of visited cities and each current city, the shortest path: `dp[mask][j]`. A set of cities fits in an integer's bits (bit j set means city j has been visited), so there are 2ⁿ × n states.

```python
def tsp(dist):
    n = len(dist)
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0                                     # start at city 0; only city 0 visited
    for mask in range(1 << n):
        for j in range(n):
            if dp[mask][j] == INF or not mask >> j & 1:
                continue
            for k in range(n):
                if mask >> k & 1:
                    continue                         # k already visited
                new = mask | 1 << k
                if dp[mask][j] + dist[j][k] < dp[new][k]:
                    dp[new][k] = dp[mask][j] + dist[j][k]
    full = (1 << n) - 1
    return min(dp[full][j] + dist[j][0] for j in range(1, n))   # return home

dist = [[0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]]
print(tsp(dist))                                     # 0 -> 1 -> 3 -> 2 -> 0
```

O(2ⁿ × n²): about 400 million steps for n = 20, versus 19! ≈ 10¹⁷ orders. Bitmask DP fits any problem with a small set of items where **which** items are used matters but their order doesn't (assigning n ≤ 20 tasks to people, covering a set of requirements). The bit tricks themselves are in Lesson 47.

### DP on trees

On a tree, compute each node's answer from its children's answers in **postorder** (Lesson 30's "return information from children"). Often a node returns **two** numbers: the best with the node used, and the best with it unused. House robber on a tree ("you can't rob a parent and its child"):

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def rob_tree(root):
    def best(node):                          # returns (best if node is robbed, best if not)
        if node is None:
            return 0, 0
        l_take, l_skip = best(node.left)
        r_take, r_skip = best(node.right)
        take = node.val + l_skip + r_skip    # robbing it forbids robbing its children
        skip = max(l_take, l_skip) + max(r_take, r_skip)
        return take, skip
    return max(best(root))

root = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(3)), TreeNode(5, None, TreeNode(1)))
print(rob_tree(root))                        # 4 + 5
```

### Which DP shape is it?

| Clue in the problem | Shape | State |
|---|---|---|
| choose items under a weight/budget limit, each once | 0/1 knapsack | dp[capacity], capacities downwards |
| items can be reused | unbounded knapsack | dp[capacity], capacities upwards |
| reach an exact sum / split into equal halves | subset sum | can[sum] (or a bitset) |
| best way to split or merge a range | interval DP | dp[i][j], short intervals first |
| small set (n ≤ 20), which items are used matters | bitmask DP | dp[mask][last] |
| answer depends on children in a tree | tree DP | return a tuple from each subtree |
| count numbers up to N with a digit property | digit DP | dp[position][tight][state] |

:::exercise Partition into equal sums
Write `can_partition(nums)` returning `True` if the list of positive integers can be split into two groups with equal sums. It must handle 100 numbers up to 50 quickly.
```python starter
def can_partition(nums):
    pass

print(can_partition([1, 5, 11, 5]))   # True: [1, 5, 5] and [11]
print(can_partition([1, 2, 3, 5]))    # False
```
```python check
fn = need("can_partition")
test(fn, cases=[
    (([1, 5, 11, 5],), True, "the first example"),
    (([1, 2, 3, 5],), False, "the second example"),
    (([1, 1],), True, "two equal numbers"),
    (([1],), False, "a single number"),
    (([2, 2, 3, 5],), False, "an even total that still can't be split"),
    (([3, 3, 3, 4, 5],), True, "3 + 3 + 3 = 4 + 5"),
    (([100, 1, 1, 1, 1],), False, "one number bigger than the rest"),
    (([1, 2, 5],), False, "an even total with no subset"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    rest = [rng.randint(1, 50) for _ in range(n - 1)]
    return (rest + [sum(rest) + 2],)
def _ref(nums):
    t = sum(nums)
    if t % 2: return False
    reach = 1
    for x in nums: reach |= reach << x
    return bool(reach >> (t // 2) & 1)
speed(fn, _make, _ref, sizes=(10, 22, 100), what="numbers",
      tip="Trying every subset is O(2^n). Track which sums are reachable: can[s] for s up to total // 2, updated downwards for each number (a 0/1 knapsack).")
```
```python solution
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False                      # an odd total can't be split evenly
    target = total // 2
    can = [True] + [False] * target       # can[s]: some subset adds up to s
    for x in nums:
        for s in range(target, x - 1, -1):    # downwards, so each number is used once
            if can[s - x]:
                can[s] = True
    return can[target]

print(can_partition([1, 5, 11, 5]))
print(can_partition([1, 2, 3, 5]))
```
```python slow
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False

    def pick(i, remaining):
        if remaining == 0:
            return True
        if i == len(nums) or remaining < 0:
            return False
        return pick(i + 1, remaining - nums[i]) or pick(i + 1, remaining)

    return pick(0, total // 2)
```
hint: If the total is odd, it's impossible. If it's even, what single question decides the answer?
hint: "Is there a subset that adds up to exactly total / 2?" The other numbers then make up the other half. That's subset sum, a 0/1 knapsack.
hint: `can = [True] + [False] * target`. For each number x, loop s from `target` **down** to x and set `can[s] = True` if `can[s - x]`. Return `can[target]`.
approach:
1. **Understand:** two groups, every number used, equal sums; positive integers.
2. **Examples:** [1, 5, 11, 5] → 11 = 1 + 5 + 5; [1, 2, 3, 5] (total 11) → False.
3. **Brute force:** try all 2ⁿ subsets.
4. **Pattern:** **subset sum** (0/1 knapsack with booleans).
5. **Plan:** odd-total check; boolean table up to total // 2; update downwards per number.
6. **Code and test:** a single number, an even total with no split, one dominant number.
walkthrough:
**Line by line**

- An odd total can't be split into two equal integers, so return False at once.
- `can[s]` records whether some subset of the numbers seen so far sums to s; the empty subset makes `can[0]` True.
- For each number x, a sum s becomes reachable if s − x was reachable **before** x was considered. Looping s downwards guarantees `can[s - x]` hasn't already been updated with x.
- The answer is whether half the total is reachable.

**Trace** on [1, 5, 11, 5] (target 11), listing the reachable sums:

| number | reachable sums ≤ 11 |
|---|---|
| start | 0 |
| 1 | 0, 1 |
| 5 | 0, 1, 5, 6 |
| 11 | 0, 1, 5, 6, **11** |
| 5 | 0, 1, 5, 6, 10, 11 |

**Complexity:** O(n × total) time, O(total) space; the bitset version runs the same idea on whole machine words.

**Common wrong approach:** looping s **upwards**, which lets one number be used several times: [2, 3] would wrongly reach 4 as 2 + 2.
:::

:::exercise 0/1 knapsack
Write `knapsack(weights, values, capacity)` returning the largest total value of items that fit in the bag, with each item taken at most once. It must handle 200 items and a capacity of 1,000 quickly.
```python starter
def knapsack(weights, values, capacity):
    pass

print(knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7))   # 9: weights 3 + 4
```
```python check
fn = need("knapsack")
test(fn, cases=[
    (([1, 3, 4, 5], [1, 4, 5, 7], 7), 9, "the example"),
    (([10], [100], 5), 0, "nothing fits"),
    (([], [], 10), 0, "no items"),
    (([1, 1, 1], [10, 20, 30], 2), 50, "take the two most valuable"),
    (([5, 4, 6, 3], [10, 40, 30, 50], 10), 90, "the classic textbook case"),
    (([2, 2], [3, 3], 6), 6, "each item only once, even with room left"),
    (([3, 4, 2], [30, 50, 15], 0), 0, "zero capacity"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    return ([rng.randint(20, 200) for _ in range(n)], [rng.randint(1, 100) for _ in range(n)], 1_000)
def _ref(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for wt, val in zip(weights, values):
        for w in range(capacity, wt - 1, -1):
            if dp[w - wt] + val > dp[w]: dp[w] = dp[w - wt] + val
    return dp[capacity]
speed(fn, _make, _ref, sizes=(10, 26, 200), what="items",
      tip="Trying every take/skip combination is O(2^n). Keep dp[w] = best value with capacity w, and for each item loop w downwards: dp[w] = max(dp[w], dp[w - weight] + value).")
```
```python solution
def knapsack(weights, values, capacity):
    best = [0] * (capacity + 1)                 # best[w]: most value within capacity w
    for wt, val in zip(weights, values):
        for w in range(capacity, wt - 1, -1):   # downwards: this item can't be counted twice
            if best[w - wt] + val > best[w]:
                best[w] = best[w - wt] + val    # take the item
    return best[capacity]

print(knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7))
```
```python slow
def knapsack(weights, values, capacity, i=0):
    if i == len(weights):
        return 0
    best = knapsack(weights, values, capacity, i + 1)                  # skip item i
    if weights[i] <= capacity:
        best = max(best, values[i] + knapsack(weights, values, capacity - weights[i], i + 1))
    return best
```
hint: For each item there are two choices. What's the state that captures everything that matters about the choices made so far?
hint: Only the remaining capacity matters. Let `best[w]` be the most value achievable with capacity w using the items processed so far.
hint: For each item, loop w from `capacity` down to its weight: `best[w] = max(best[w], best[w - wt] + val)`. Return `best[capacity]`.
approach:
1. **Understand:** each item at most once; total weight ≤ capacity; maximise value.
2. **Examples:** weights [1, 3, 4, 5], values [1, 4, 5, 7], capacity 7 → 9 (items of weight 3 and 4).
3. **Brute force:** all 2ⁿ subsets, or the take/skip recursion.
4. **Pattern:** **0/1 knapsack**, one row, capacities downwards.
5. **Plan:** `best` of size capacity + 1; process items one by one.
6. **Code and test:** nothing fits, zero capacity, two identical items.
walkthrough:
**Line by line**

- Before any items, every capacity has value 0.
- For an item (wt, val), the new best for capacity w is the old best (skip) or `best[w - wt] + val` (take), where `best[w - wt]` must be the value **without** this item.
- Looping w downwards means `best[w - wt]` (a smaller index) hasn't been updated for this item yet.
- After all items, `best[capacity]` is the answer.

**Trace** on the example (capacities 0 to 7):

| after item | best[0..7] |
|---|---|
| (1, 1) | 0 1 1 1 1 1 1 1 |
| (3, 4) | 0 1 1 4 5 5 5 5 |
| (4, 5) | 0 1 1 4 5 6 6 9 |
| (5, 7) | 0 1 1 4 5 7 8 **9** |

**Complexity:** O(n × capacity) time, O(capacity) space.

**Common wrong approach:** a greedy by value-per-weight. It's right for the **fractional** knapsack (Lesson 45) but not here: weights [10, 20, 30], values [60, 100, 120], capacity 50 → greedy takes 160, the best is 220.
:::

:::quiz
? In a one-row 0/1 knapsack, why must capacities be looped downwards?
+ So dp[w − weight] still holds the value from before this item, and the item is used at most once
- To save memory
- Because larger capacities are more important
= Looping upwards allows reuse, which gives the unbounded knapsack.
? Why is knapsack's O(n × W) called pseudo-polynomial?
+ W is a numeric value, so the time grows exponentially in the number of digits of W
- Because it uses recursion
- Because n is always small
= Knapsack is NP-hard in general; the DP is fast only when W is moderate.
? In interval DP like matrix-chain order, which intervals are computed first?
+ The shortest ones
- The longest ones
- Those that start at 0
= Every split of a range needs both shorter sides to be done already.
? What does dp[mask][j] mean in the Held-Karp TSP algorithm?
+ The shortest path that visits exactly the cities in mask and ends at city j
- The distance between cities mask and j
- The number of tours through j
= Sets of visited cities are stored as the bits of mask.
:::

@@@ lesson
id: greedy
title: Greedy algorithms
minutes: 26
summary: Making the best-looking choice at each step: when that is provably right (the exchange argument) and when it fails, activity selection, fractional knapsack, jump games, the gas station, Huffman coding, pairing with two pointers, and testing a greedy idea against brute force.
---
A **greedy algorithm** builds its answer one step at a time, always taking the choice that looks best **right now**, and never reconsidering. When it works, it's usually the simplest and fastest solution, often just a sort and a loop. The catch: it doesn't always work, and a wrong greedy looks just as convincing as a right one.

A greedy approach is correct when the problem has:

- **The greedy-choice property:** some optimal solution starts with the greedy choice.
- **Optimal substructure:** after making that choice, what's left is a smaller instance of the same problem.

The usual proof is an **exchange argument**: take any optimal solution that doesn't start with the greedy choice, swap the greedy choice in, and show the result is no worse. If you can't make that argument, suspect DP.

### Activity selection: the most non-overlapping meetings

Given meetings as (start, end), attend as many as possible with no two overlapping. The greedy rule that works: **always pick the meeting that ends first**, then the next one that starts after it ends, and so on.

![Meetings drawn as bars on a timeline from 0 to 10. Sorted by end time, the greedy picks the bar ending at 3, skips two that overlap it, picks the one from 3 to 5, skips another, and picks the one from 6 to 9: three meetings. Picking the longest or the earliest-starting meeting first would leave room for fewer](figures/activity-selection.svg)

```python
def max_meetings(meetings):
    chosen, free_from = [], float("-inf")
    for start, end in sorted(meetings, key=lambda m: m[1]):   # earliest end first
        if start >= free_from:
            chosen.append((start, end))
            free_from = end
    return chosen

meetings = [(1, 3), (2, 5), (0, 4), (3, 5), (4, 7), (6, 9), (5, 9)]
print(max_meetings(meetings))
```

**Why it's right (exchange argument):** suppose an optimal schedule starts with some meeting M instead of the earliest-ending meeting G. G ends no later than M, so swapping M for G can't overlap anything that came after M. The new schedule is just as large and starts with G. Repeat for the rest.

Other rules sound sensible but fail: "shortest meeting first" (a short meeting can overlap two others that don't overlap each other) and "earliest start first" (one long meeting can block everything).

### When greedy fails

| Problem | Tempting greedy | Counterexample | Use instead |
|---|---|---|---|
| Fewest coins | biggest coin first | coins 1, 3, 4, amount 6: 4 + 1 + 1 vs 3 + 3 | DP (Lesson 42) |
| 0/1 knapsack | best value per weight first | capacity 50, items (10, $60), (20, $100), (30, $120): greedy $160, best $220 | DP (Lesson 44) |
| Longest path, TSP | nearest unvisited city | easily misled by one cheap edge | DP / search |

### Fractional knapsack: where the ratio greedy works

If you may take **part** of an item (gold dust rather than gold bars), greedy by value per weight is optimal: the last item can be cut to fill the bag exactly, so no capacity is ever wasted.

```python
def fractional_knapsack(items, capacity):           # items: (weight, value)
    total = 0.0
    for weight, value in sorted(items, key=lambda it: it[1] / it[0], reverse=True):
        take = min(weight, capacity)
        total += value * take / weight
        capacity -= take
        if capacity == 0:
            break
    return total

print(fractional_knapsack([(10, 60), (20, 100), (30, 120)], 50))    # all of the first two, 2/3 of the third
```

### Jump game

`nums[i]` is the farthest you can jump forward from position i. **Can you reach the end?** Track the farthest position reachable so far; if you ever stand beyond it, you're stuck. O(n), no DP needed.

```python
def can_reach_end(nums):
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False                 # this position can't be reached
        farthest = max(farthest, i + jump)
    return True

print(can_reach_end([2, 3, 1, 1, 4]), can_reach_end([3, 2, 1, 0, 4]))
```

The harder version, the **fewest** jumps, is greedy too: think of it as BFS levels, where each jump's range is the next level. That's the first exercise.

### Gas station

Stations on a circular road have `gas[i]` fuel and it costs `cost[i]` to drive to the next one. From which station can you complete the loop (or −1)? Two facts make it O(n): if total gas < total cost, it's impossible; otherwise, whenever the tank goes negative starting from s, no station between s and the failure point can work either, so restart just after it.

```python
def gas_station(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start, tank = 0, 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                     # can't get past i from start: try starting after i
            start, tank = i + 1, 0
    return start

print(gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), gas_station([2, 3, 4], [3, 4, 3]))
```

### Huffman coding

To compress text, give frequent characters **short** codes and rare characters long ones, with no code being a prefix of another (so the bits can be decoded unambiguously). **Huffman's algorithm** is greedy: repeatedly merge the two **least frequent** symbols (or subtrees) into one, using a heap. The resulting tree's left/right branches spell each character's code, and the total length is provably the smallest possible for a prefix code.

![A Huffman tree for frequencies a: 45, b: 13, c: 12, d: 16, e: 9, f: 5. The two smallest (f: 5 and e: 9) merge into 14; then c and b into 25; then 14 and d into 30; then 25 and 30 into 55; finally a and 55 into 100. Reading 0 for left and 1 for right gives a = 0, and longer codes for the rarer letters](figures/huffman.svg)

```python
import heapq
from collections import Counter
from itertools import count

def huffman_codes(text):
    tie = count()                                     # breaks ties so subtrees are never compared
    heap = [(freq, next(tie), ch) for ch, freq in Counter(text).items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)             # the two least frequent
        f2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, next(tie), (left, right)))
    codes = {}
    def walk(node, code):
        if isinstance(node, str):
            codes[node] = code or "0"                 # a one-letter text still needs one bit
        else:
            walk(node[0], code + "0")
            walk(node[1], code + "1")
    walk(heap[0][2], "")
    return codes

text = "abracadabra"
codes = huffman_codes(text)
print(codes)
bits = sum(len(codes[ch]) for ch in text)
print(f"{bits} bits instead of {8 * len(text)} with 8-bit characters")
```

Huffman coding is part of ZIP, gzip, PNG and JPEG.

### Two pointers as a greedy

**Boats:** each boat carries at most two people and a weight limit. Fewest boats? Sort; pair the **heaviest** person with the **lightest** if they fit, otherwise the heaviest goes alone. The heaviest person needs a boat anyway, and the lightest is the best possible partner.

```python
def boats(weights, limit):
    weights = sorted(weights)
    lo, hi, count = 0, len(weights) - 1, 0
    while lo <= hi:
        if weights[lo] + weights[hi] <= limit:
            lo += 1                       # the lightest rides with the heaviest
        hi -= 1                           # the heaviest always leaves on this boat
        count += 1
    return count

print(boats([3, 2, 2, 1], 3), boats([3, 5, 3, 4], 5))
```

### Testing a greedy idea

Before trusting a greedy rule, compare it with a brute-force (or DP) solution on **many small random inputs**. A counterexample usually turns up within seconds if one exists:

```python
import random
from itertools import product

def greedy_coins(coins, amount):
    n = 0
    for c in sorted(coins, reverse=True):
        n += amount // c
        amount %= c
    return n if amount == 0 else None

def best_coins(coins, amount):
    dp = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        dp[a] = min((dp[a - c] + 1 for c in coins if c <= a), default=float("inf"))
    return dp[amount]

random.seed(4)
for _ in range(1000):
    coins = [1] + random.sample(range(2, 12), 2)
    amount = random.randint(1, 30)
    if greedy_coins(coins, amount) != best_coins(coins, amount):
        print("counterexample:", sorted(coins), amount, "greedy", greedy_coins(coins, amount), "best", best_coins(coins, amount))
        break
```

### Greedy at a glance

| Problem | Greedy rule | Time |
|---|---|---|
| Most non-overlapping intervals | earliest end first | O(n log n) |
| Fractional knapsack | best value per weight first | O(n log n) |
| Reach the end / fewest jumps | track the farthest reach / BFS levels | O(n) |
| Gas station | restart after each failure | O(n) |
| Huffman coding, cheapest merging | merge the two smallest (heap) | O(n log n) |
| Boats, pairing | heaviest with lightest (two pointers) | O(n log n) |
| Minimise total waiting time | shortest job first | O(n log n) |
| Minimise maximum lateness | earliest deadline first | O(n log n) |

:::exercise Fewest jumps
`nums[i]` is the farthest you can jump forward from position i (you may jump any distance up to it). Starting at position 0, write `min_jumps(nums)` returning the fewest jumps needed to reach the last position. The end is always reachable. It must be O(n): 100,000 positions in well under a second.
```python starter
def min_jumps(nums):
    pass

print(min_jumps([2, 3, 1, 1, 4]))   # 2: 0 -> 1 -> 4
```
```python check
fn = need("min_jumps")
test(fn, cases=[
    (([2, 3, 1, 1, 4],), 2, "the example"),
    (([2, 3, 0, 1, 4],), 2, "a zero along the way"),
    (([0],), 0, "already at the end"),
    (([1, 1, 1, 1],), 3, "one step at a time"),
    (([10, 1, 1, 1],), 1, "one big jump"),
    (([1, 2, 1, 1, 1],), 3, "a longer jump in the middle"),
    (([3, 1, 4, 1, 1, 1, 1],), 2, "the farthest first jump isn't the best one"),
    (([2, 1],), 1, "two positions"),
])
def _ref(nums):
    jumps, end, far = 0, 0, 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1; end = far
    return jumps
speed(fn, lambda n: ([1] * n,), _ref, sizes=(1_000, 5_000, 100_000), what="positions",
      tip="Checking every earlier position for every position is O(n^2). Treat it like BFS: track where the current jump's range ends and the farthest point reachable; when you reach the end of the range, take one more jump.")
```
```python solution
def min_jumps(nums):
    jumps = 0
    current_end = 0          # the farthest position reachable with `jumps` jumps
    farthest = 0             # the farthest reachable with one more jump
    for i in range(len(nums) - 1):          # no jump is needed from the last position
        farthest = max(farthest, i + nums[i])
        if i == current_end:                # we've used up this jump's range
            jumps += 1
            current_end = farthest
    return jumps

print(min_jumps([2, 3, 1, 1, 4]))
```
```python slow
def min_jumps(nums):
    n = len(nums)
    best = [0] + [float("inf")] * (n - 1)
    for i in range(1, n):
        for j in range(i):
            if j + nums[j] >= i and best[j] + 1 < best[i]:
                best[i] = best[j] + 1
    return best[-1]
```
hint: Think of BFS: the positions reachable with 0 jumps, with 1 jump, with 2 jumps… form consecutive ranges. How do you find the next range from the current one?
hint: The next range ends at the farthest `i + nums[i]` over all positions i in the current range. Scan left to right, tracking that farthest point.
hint: Keep `current_end` and `farthest`. For i from 0 to n − 2: update `farthest`; when `i == current_end`, add a jump and set `current_end = farthest`. Return the jump count.
approach:
1. **Understand:** the minimum number of jumps; the end is reachable; a single position needs 0 jumps.
2. **Examples:** [2, 3, 1, 1, 4] → 0 → 1 → 4: 2 jumps.
3. **Brute force:** DP: best[i] = 1 + min best[j] over j that can reach i: O(n²).
4. **Pattern:** **greedy BFS by levels**: each jump extends the range as far as possible.
5. **Plan:** one pass, counting a jump every time the current range is used up.
6. **Code and test:** a single element, one huge first jump, all ones.
walkthrough:
**Line by line**

- Positions 0..`current_end` can be reached with `jumps` jumps; `farthest` is how far one more jump can take you from any of them.
- When i reaches `current_end`, every position in the current range has been examined, so one more jump is needed and the new range ends at `farthest`.
- The loop stops before the last index: once you can stand there, no further jump is needed.

**Trace** on [2, 3, 1, 1, 4]:

| i | farthest | i == current_end? | jumps | current_end |
|---|---|---|---|---|
| 0 | 2 | yes | 1 | 2 |
| 1 | 4 | no | 1 | 2 |
| 2 | 4 | yes | 2 | 4 |
| 3 | 4 | no | 2 | 4 |

**Complexity:** O(n) time, O(1) space.

**Common wrong approach:** always jumping as far as possible from the current position. In [2, 3, 1, 1, 4], jumping straight to index 2 (value 1) needs 3 jumps in total; stopping at index 1, whose own reach is 4, needs only 2.
:::

:::exercise Cheapest way to join ropes
You have ropes of the given `lengths`. Joining two ropes of lengths a and b costs a + b and gives one rope of length a + b. Write `join_cost(lengths)` returning the minimum total cost to join all the ropes into one (0 for zero or one rope). It must handle 200,000 ropes quickly.
```python starter
import heapq

def join_cost(lengths):
    pass

print(join_cost([4, 3, 2, 6]))   # 29: (2+3)=5, (4+5)=9, (6+9)=15 -> 5 + 9 + 15
```
```python check
import heapq as _hq
fn = need("join_cost")
test(fn, cases=[
    (([4, 3, 2, 6],), 29, "the example"),
    (([5],), 0, "one rope"),
    (([],), 0, "no ropes"),
    (([1, 1],), 2, "two ropes"),
    (([1, 2, 3, 4, 5],), 33, "five ropes"),
    (([10, 10, 10, 10],), 80, "equal lengths"),
    (([1, 8, 3, 5],), 30, "unsorted input"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    return ([rng.randint(1, 1000) for _ in range(n)],)
def _ref(lengths):
    h = list(lengths); _hq.heapify(h); c = 0
    while len(h) > 1:
        x = _hq.heappop(h) + _hq.heappop(h); c += x; _hq.heappush(h, x)
    return c
speed(fn, _make, _ref, sizes=(1_000, 6_000, 200_000), what="ropes",
      tip="Finding the two shortest ropes by scanning (or re-sorting) every time is O(n^2). Keep the ropes in a heapq min-heap: pop two, push their sum.")
```
```python solution
import heapq

def join_cost(lengths):
    heap = list(lengths)
    heapq.heapify(heap)                  # O(n)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)          # the two shortest ropes
        b = heapq.heappop(heap)
        total += a + b
        heapq.heappush(heap, a + b)      # the joined rope goes back in
    return total

print(join_cost([4, 3, 2, 6]))
```
```python slow
def join_cost(lengths):
    ropes = list(lengths)
    total = 0
    while len(ropes) > 1:
        a = min(ropes); ropes.remove(a)
        b = min(ropes); ropes.remove(b)
        total += a + b
        ropes.append(a + b)
    return total
```
hint: Each rope's length is paid again every time the rope it's part of is joined. Which ropes should be joined first, so their lengths are paid many times?
hint: Always join the two **shortest** ropes (Huffman's rule): long ropes then get joined fewer times. You need the two smallest values over and over.
hint: Put the lengths in a heap (`heapq.heapify`). While more than one rope remains: pop two, add their sum to the total, push the sum back.
approach:
1. **Understand:** each join costs the new rope's length; minimise the total; 0 or 1 rope costs 0.
2. **Examples:** [4, 3, 2, 6] → 5 + 9 + 15 = 29.
3. **Brute force:** try every order of joins: exponential; or the greedy with a linear scan each time: O(n²).
4. **Pattern:** **Huffman's greedy** with a **min-heap**.
5. **Plan:** heapify; repeatedly pop two, add, push.
6. **Code and test:** empty, one rope, equal lengths, unsorted input.
walkthrough:
**Line by line**

- `heapify` arranges the lengths so the shortest is always at the front, in O(n).
- Each round removes the two shortest ropes, pays their combined length, and puts the new rope back to be joined later.
- With n ropes there are n − 1 joins; the loop stops when one rope is left (or none was given).

**Trace** on [4, 3, 2, 6]:

| heap before | joined | cost so far |
|---|---|---|
| 2, 3, 4, 6 | 2 + 3 = 5 | 5 |
| 4, 5, 6 | 4 + 5 = 9 | 14 |
| 6, 9 | 6 + 9 = 15 | **29** |

**Complexity:** O(n log n) time, O(n) space.

**Common wrong approach:** sorting once and joining left to right (2 + 3, then + 4, then + 6). That ignores that a joined rope may become longer than an unjoined one: [1, 1, 1, 1] costs 8 the Huffman way, but 9 left to right.
:::

:::quiz
? What is the usual way to prove a greedy algorithm correct?
+ An exchange argument: swapping the greedy choice into an optimal solution doesn't make it worse
- Running it on one example
- Showing it's faster than DP
= If no exchange argument works, look for a counterexample, or use DP.
? For selecting the most non-overlapping meetings, which meeting should be chosen first?
+ The one that ends earliest
- The shortest one
- The one that starts earliest
= Ending early leaves the most room for the rest.
? Why does greedy by value per weight work for the fractional knapsack but not the 0/1 knapsack?
+ With fractions, the last item can be cut to fill the bag exactly, so no capacity is wasted
- Fractional values are smaller
- Sorting doesn't work for 0/1
= In 0/1, a high-ratio item can leave unusable leftover space.
? Huffman's algorithm repeatedly:
+ Merges the two least frequent symbols or subtrees
- Gives the most frequent symbol the longest code
- Sorts the symbols alphabetically
= Rare symbols end up deep in the tree with long codes; frequent ones get short codes.
:::

@@@ lesson
id: intervals-sweep
title: Intervals and sweep lines
minutes: 26
summary: Working with ranges: testing overlap, merging and inserting intervals, intersecting two schedules, the fewest removals to avoid overlap, how many rooms meetings need (heap or sweep line), events sorted along a line, and difference arrays for many range updates.
---
Calendars, bookings, IP ranges, gene positions, video timestamps: **intervals** `[start, end]` are everywhere, and nearly every interval problem starts the same way: **sort them**, usually by start (or by end for scheduling problems), then make one pass.

### Do two intervals overlap?

Two intervals overlap exactly when **each starts before the other ends**. It's easier to check that than all the ways they can overlap.

```python
def overlaps(a, b):                       # closed intervals: [1, 3] and [3, 5] share the point 3
    return a[0] <= b[1] and b[0] <= a[1]

def overlaps_half_open(a, b):             # half-open [start, end): a meeting ending at 3 and one starting at 3 don't clash
    return a[0] < b[1] and b[0] < a[1]

print(overlaps([1, 3], [3, 5]), overlaps_half_open([1, 3], [3, 5]), overlaps([1, 2], [4, 6]))
```

Decide which convention the problem uses. Meetings and bookings are usually **half-open** (one can end at 3 and the next start at 3); "merge intervals" problems usually treat touching intervals as overlapping.

### Merging overlapping intervals

Sort by start. Walk through, and either **extend** the last merged interval (if the current one starts before it ends) or start a new one. That's the first exercise.

![Intervals [1, 3], [2, 6], [8, 10], [9, 12] and [15, 18] drawn on a number line, sorted by start. [1, 3] and [2, 6] overlap and merge into [1, 6]; [8, 10] and [9, 12] merge into [8, 12]; [15, 18] stays alone](figures/merge-intervals.svg)

### Inserting into a sorted list of intervals

Given non-overlapping intervals sorted by start, insert a new one, merging where needed. Three phases in one pass: copy the intervals that end **before** it, absorb those that overlap it, copy the rest. O(n).

```python
def insert_interval(intervals, new):
    out, i, n = [], 0, len(intervals)
    start, end = new
    while i < n and intervals[i][1] < start:       # entirely before the new one
        out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= end:        # overlapping: grow the new interval
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    out.append([start, end])
    out.extend(intervals[i:])                      # entirely after
    return out

print(insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]))
```

### Intersecting two schedules

When are two people both free (or both busy)? With two sorted lists of non-overlapping intervals, use **two pointers**: the overlap of the current pair is `[max(starts), min(ends)]` if that's non-empty, then advance whichever interval ends first.

```python
def intersect(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo <= hi:
            out.append([lo, hi])
        if a[i][1] < b[j][1]:                      # the one that ends first can't overlap anything else
            i += 1
        else:
            j += 1
    return out

print(intersect([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]))
```

### Fewest removals so nothing overlaps

Removing the fewest intervals is the same as **keeping the most** non-overlapping ones: activity selection from Lesson 45. Sort by **end**, keep each interval that starts at or after the last kept end, and count the rest.

```python
def min_removals(intervals):
    kept, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if start >= last_end:
            kept += 1
            last_end = end
    return len(intervals) - kept

print(min_removals([[1, 2], [2, 3], [3, 4], [1, 3]]), min_removals([[1, 2], [1, 2], [1, 2]]))
```

### How many meeting rooms? Two ways

The fewest rooms needed equals the **largest number of meetings happening at the same moment**.

**Heap of end times:** process meetings by start time; the heap holds the end times of rooms in use. If the earliest-ending room is free by the time the next meeting starts, reuse it (pop); then push this meeting's end. The heap's largest size is the answer.

**Sweep line:** turn each meeting into two **events**, +1 at its start and −1 at its end, sort them, and sweep left to right keeping a running count. With half-open meetings, an end and a start at the same time must process the **end first**; sorting `(time, change)` does that automatically, because −1 sorts before +1.

![A timeline with meetings [0, 30], [5, 10] and [15, 20]. Below it, the running count of meetings in progress steps up and down at each start and end: 1, then 2 at time 5, back to 1 at 10, 2 again at 15, and 1 at 20. Its peak of 2 is the number of rooms needed](figures/sweep-line.svg)

```python
import heapq

def rooms_heap(meetings):
    ends = []                                       # end times of rooms currently in use
    for start, end in sorted(meetings):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)            # the earliest-ending room is free: reuse it
        else:
            heapq.heappush(ends, end)               # every room is busy: open another
    return len(ends)

def rooms_sweep(meetings):
    events = [(s, +1) for s, e in meetings] + [(e, -1) for s, e in meetings]
    in_use = peak = 0
    for time, change in sorted(events):             # at equal times, -1 (an end) sorts first
        in_use += change
        peak = max(peak, in_use)
    return peak

meetings = [[0, 30], [5, 10], [15, 20]]
print(rooms_heap(meetings), rooms_sweep(meetings), rooms_sweep([[1, 5], [5, 10]]))
```

The sweep line generalises: sort events along a line and keep running state. It finds the busiest moment of a server, the maximum number of overlapping bookings, the total length covered by a set of intervals, and (with a heap of heights) the city **skyline** outline.

### Difference arrays: many range updates at once

"Add k to every position from l to r", repeated many times, then read the final values. Updating each range directly is O(length) per update. A **difference array** records only the **changes**: `diff[l] += k` and `diff[r + 1] -= k`. A single prefix sum at the end turns the changes back into values: O(1) per update plus O(n) once.

```python
from itertools import accumulate

def car_pooling(trips, capacity):            # trips: (passengers, from, to); passengers leave at `to`
    last = max(to for _, _, to in trips)
    diff = [0] * (last + 1)
    for people, start, end in trips:
        diff[start] += people                 # they get in here
        diff[end] -= people                   # and out here
    load = list(accumulate(diff))             # prefix sums: passengers on board at each stop
    return max(load) <= capacity, load

print(car_pooling([(2, 1, 5), (3, 3, 7)], 4))
print(car_pooling([(2, 1, 5), (3, 5, 7)], 3))
```

It's the reverse of Lesson 9's prefix sums: prefix sums answer many range **queries** on fixed data; difference arrays apply many range **updates** before one read. (When updates and queries are mixed, use a Fenwick or segment tree with lazy propagation, Lesson 34.)

### Interval patterns at a glance

| Question | Sort by | Then |
|---|---|---|
| Merge overlapping intervals | start | extend the last merged interval or start a new one |
| Insert one interval | (already sorted) | before / overlapping / after, in one pass |
| Intersections of two lists | (already sorted) | two pointers, advance the earlier end |
| Most non-overlapping / fewest removals | end | greedy activity selection |
| Rooms needed / maximum overlap | start, or events | heap of end times, or sweep line |
| Many range additions, then read | — | difference array + prefix sum |

:::exercise Merge intervals
Write `merge(intervals)` that merges all overlapping intervals (lists `[start, end]`, in any order; intervals that touch, like [1, 4] and [4, 5], count as overlapping) and returns the merged intervals sorted by start. Don't change the input list. It must handle 100,000 intervals quickly.
```python starter
def merge(intervals):
    pass

print(merge([[1, 3], [2, 6], [8, 10], [15, 18]]))   # [[1, 6], [8, 10], [15, 18]]
print(merge([[1, 4], [4, 5]]))                      # [[1, 5]]
```
```python check
fn = need("merge")
_orig = [[8, 10], [1, 3], [2, 6]]
_copy = [iv[:] for iv in _orig]
fn(_copy)
if _copy != _orig:
    raise AssertionError("Don't change the input: sort a copy (sorted(intervals)) instead of intervals.sort().")
_norm = lambda r: [list(iv) for iv in r] if isinstance(r, (list, tuple)) else r
test(fn, key=_norm, cases=[
    (([[1, 3], [2, 6], [8, 10], [15, 18]],), [[1, 6], [8, 10], [15, 18]], "the example"),
    (([[1, 4], [4, 5]],), [[1, 5]], "touching intervals"),
    (([[1, 4], [2, 3]],), [[1, 4]], "one inside another"),
    (([[8, 10], [1, 3], [2, 6]],), [[1, 6], [8, 10]], "unsorted input"),
    (([[5, 7]],), [[5, 7]], "a single interval"),
    (([],), [], "no intervals"),
    (([[1, 10], [2, 3], [4, 5], [11, 12]],), [[1, 10], [11, 12]], "a long interval swallowing others"),
    (([[6, 8], [1, 9], [2, 4], [4, 7]],), [[1, 9]], "everything merges"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    starts = rng.sample(range(0, 10 * n, 10), n)
    return ([[s, s + 5] for s in starts],)
def _ref(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]: out[-1][1] = max(out[-1][1], e)
        else: out.append([s, e])
    return out
speed(fn, _make, _ref, sizes=(1_000, 3_000, 100_000), what="intervals", key=_norm,
      tip="Comparing every interval with every merged one is O(n^2). Sort by start once; then each interval either extends the last merged interval or starts a new one.")
```
```python solution
def merge(intervals):
    merged = []
    for start, end in sorted(intervals):          # sorted() copies, so the input is unchanged
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)   # overlaps the last one: extend it
        else:
            merged.append([start, end])           # a gap: start a new merged interval
    return merged

print(merge([[1, 3], [2, 6], [8, 10], [15, 18]]))
print(merge([[1, 4], [4, 5]]))
```
```python slow
def merge(intervals):
    result = []
    for start, end in intervals:
        i = 0
        while i < len(result):                    # absorb every merged interval that overlaps
            s, e = result[i]
            if start <= e and s <= end:
                start, end = min(start, s), max(end, e)
                result.pop(i)
            else:
                i += 1
        result.append([start, end])
    return sorted(result)
```
hint: If the intervals were sorted by start, which merged interval could the next one possibly overlap?
hint: Only the **last** merged interval. So: sort by start, then for each interval either extend the last merged one (if `start <= last_end`) or append a new one.
hint: `for start, end in sorted(intervals):` if `merged` is non-empty and `start <= merged[-1][1]`, set `merged[-1][1] = max(merged[-1][1], end)`; otherwise append `[start, end]`.
approach:
1. **Understand:** any input order; touching counts as overlapping; output sorted; input unchanged.
2. **Examples:** [[1, 3], [2, 6]] → [[1, 6]]; [[1, 4], [2, 3]] → [[1, 4]] (contained).
3. **Brute force:** repeatedly merge any overlapping pair until none remain: O(n²) or worse.
4. **Pattern:** **sort by start, then a single sweep**.
5. **Plan:** sorted copy; extend or append; use `max` for the end because of contained intervals.
6. **Code and test:** touching, contained, unsorted, empty input.
walkthrough:
**Line by line**

- `sorted(intervals)` returns a new list ordered by start (then end), leaving the caller's list alone.
- After sorting, an interval can only overlap the most recent merged interval: everything earlier ended before that one began, or was merged into it.
- `max(merged[-1][1], end)` matters when the new interval lies inside the last one, like [2, 3] inside [1, 4].
- Appending `[start, end]` (a new list) means later extensions never change the input's lists.

**Trace** on [[1, 3], [2, 6], [8, 10], [15, 18]]:

| interval | last merged | action | merged |
|---|---|---|---|
| [1, 3] | — | append | [[1, 3]] |
| [2, 6] | [1, 3] | 2 ≤ 3: extend to 6 | [[1, 6]] |
| [8, 10] | [1, 6] | 8 > 6: append | [[1, 6], [8, 10]] |
| [15, 18] | [8, 10] | append | [[1, 6], [8, 10], [15, 18]] |

**Complexity:** O(n log n) time for the sort, O(n) for the output.

**Common wrong approach:** setting `merged[-1][1] = end` instead of the maximum, which shrinks [1, 4] to [1, 3] when [2, 3] follows.
:::

:::exercise Meeting rooms
Each meeting is `[start, end]` and occupies a room from `start` up to (but not including) `end`, so a meeting ending at 10 and one starting at 10 can share a room. Write `min_rooms(meetings)` returning the fewest rooms needed. It must handle 100,000 meetings quickly.
```python starter
import heapq

def min_rooms(meetings):
    pass

print(min_rooms([[0, 30], [5, 10], [15, 20]]))   # 2
print(min_rooms([[7, 10], [2, 4]]))              # 1
```
```python check
fn = need("min_rooms")
test(fn, cases=[
    (([[0, 30], [5, 10], [15, 20]],), 2, "the example"),
    (([[7, 10], [2, 4]],), 1, "no overlap"),
    (([],), 0, "no meetings"),
    (([[1, 5], [5, 10]],), 1, "one ends exactly when the next starts"),
    (([[1, 10], [2, 9], [3, 8], [4, 7]],), 4, "all nested"),
    (([[1, 3], [2, 4], [3, 5], [4, 6]],), 2, "a chain of overlaps"),
    (([[9, 10], [4, 9], [4, 17]],), 2, "unsorted with a shared start"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    out = []
    for _ in range(n):
        s = rng.randint(0, 10 * n)
        out.append([s, s + rng.randint(1, 50)])
    return (out,)
def _ref(meetings):
    ev = sorted([(s, 1) for s, e in meetings] + [(e, -1) for s, e in meetings])
    cur = best = 0
    for _, c in ev:
        cur += c; best = max(best, cur)
    return best
speed(fn, _make, _ref, sizes=(1_000, 4_000, 100_000), what="meetings",
      tip="Counting, for every meeting, how many others overlap it is O(n^2). Sort by start and keep a heap of end times (or sweep sorted +1/-1 events).")
```
```python solution
import heapq

def min_rooms(meetings):
    ends = []                                   # end times of the rooms in use
    for start, end in sorted(meetings):         # by start time
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)        # the room that frees up first is free: reuse it
        else:
            heapq.heappush(ends, end)           # all rooms busy: open a new one
    return len(ends)                            # rooms are never closed, so this is the most ever needed

print(min_rooms([[0, 30], [5, 10], [15, 20]]))
print(min_rooms([[7, 10], [2, 4]]))
```
```python slow
def min_rooms(meetings):
    best = 0
    for s, _ in meetings:                       # how many meetings are running at each start time?
        running = sum(1 for a, b in meetings if a <= s < b)
        best = max(best, running)
    return best
```
hint: The number of rooms needed is the largest number of meetings in progress at the same moment. How can you track the meetings in progress as time moves forward?
hint: Process meetings in order of start time. Keep the end times of rooms in use in a min-heap: the smallest is the room that frees up first.
hint: For each meeting (sorted by start): if the heap's smallest end ≤ start, `heapreplace` it with this end (reuse the room); otherwise `heappush` the end (new room). Return the heap's size.
approach:
1. **Understand:** half-open meetings; an end at t frees the room for a start at t; empty → 0.
2. **Examples:** [[0, 30], [5, 10], [15, 20]] → 2.
3. **Brute force:** count the meetings running at each start time: O(n²).
4. **Pattern:** **sort by start + min-heap of end times** (or a sweep line of events).
5. **Plan:** reuse the earliest-freeing room when possible; otherwise add a room.
6. **Code and test:** back-to-back meetings, fully nested meetings, unsorted input.
walkthrough:
**Line by line**

- Sorting by start processes meetings in the order they begin.
- `ends[0]` is the earliest time any room becomes free. If it's free by this meeting's start (`<=`, because meetings are half-open), this meeting takes that room: `heapreplace` swaps in the new end time.
- Otherwise no room is free and a new one is opened.
- Rooms are never removed, so the heap size only grows when more rooms are needed at once: its final size is the peak.

**Trace** on [[0, 30], [5, 10], [15, 20]]:

| meeting | ends before | earliest free ≤ start? | ends after |
|---|---|---|---|
| [0, 30] | — | — | 30 |
| [5, 10] | 30 | no | 10, 30 |
| [15, 20] | 10, 30 | 10 ≤ 15: reuse | 20, 30 |

Two rooms.

**Complexity:** O(n log n) time, O(n) space.

**Common wrong approach:** comparing each meeting only with the previous one in sorted order, which misses a long meeting overlapping several later ones ([[1, 10], [2, 3], [4, 5]] needs 2 rooms, not 1, and nested meetings need more).
:::

:::quiz
? When do the closed intervals [a1, b1] and [a2, b2] overlap?
+ When a1 ≤ b2 and a2 ≤ b1
- When a1 == a2
- When b1 < a2
= Each must start before (or when) the other ends.
? After sorting intervals by start, which merged interval can the next one overlap?
+ Only the last merged interval
- Any of them
- Only the first
= Everything earlier ended before the last merged interval began.
? In a sweep line for meeting rooms, why must an end event come before a start event at the same time?
+ So a room freed at time t can be reused by a meeting starting at t
- To keep the list sorted
- Because ends are more important
= Sorting (time, change) with −1 for ends puts them first automatically.
? What does a difference array make cheap?
+ Applying many range additions before reading the values once
- Answering many range-sum queries on fixed data
- Sorting intervals
= Each update touches two cells; one prefix-sum pass rebuilds the values.
:::
