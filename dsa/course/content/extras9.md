@@ dp-intro
topics: overlapping subproblems and optimal substructure, memoisation and tabulation, recursion depth limits, the five-step DP recipe, space optimisation, climbing stairs, minimum-cost stairs, house robber, recognising DP problems
terms:
- **Dynamic programming (DP):** solving a problem by combining stored answers to smaller versions of it, each computed once.
- **Overlapping subproblems:** the same smaller problems are needed many times.
- **Optimal substructure:** an optimal answer is built from optimal answers to subproblems.
- **Memoisation (top-down):** recursion that caches each result the first time it's computed.
- **Tabulation (bottom-up):** filling a table of answers from the smallest cases upwards with loops.
- **State:** what one DP table entry means, such as "dp[i] = ways to reach step i".
- **Transition (recurrence):** the formula that computes a state from smaller states.
- **Base case:** a state whose answer is known directly, such as dp[0] = 1.
mistakes:
- Starting to code before defining in words what dp[i] means.
- Forgetting or mis-setting the base case (dp[0] = 0 where it should be 1).
- Filling the table in an order where some needed entry isn't computed yet.
- Memoised recursion on large n, which exceeds the recursion limit; tabulate instead.

glance:
- Fibonacci / climbing stairs (1 or 2) | dp[i] = dp[i − 1] + dp[i − 2] | O(n) | O(1) with two variables
- Climbing with any step sizes | ways[i] = Σ ways[i − s] | O(n · k) | O(n)
- Minimum cost stairs | dp[i] = min(dp[i − 1] + cost[i − 1], dp[i − 2] + cost[i − 2]) | O(n) | O(1)
- House robber | best = max(skip: prev1, take: prev2 + x) | O(n) | O(1)
- Memoise any recursive function | @cache | O(states × work per state) | O(states) + recursion depth

@@ dp-sequences
topics: fewest coins, counting combinations versus ordered sequences, why greedy coin change fails, Kadane's maximum subarray, maximum product subarray, longest increasing subsequence in O(n²) and O(n log n), rebuilding a subsequence, word break, decode ways
terms:
- **Unbounded knapsack:** a DP where each item (such as a coin value) may be used any number of times.
- **Kadane's algorithm:** the O(n) maximum-subarray DP that tracks the best sum ending at each position.
- **Subsequence:** items kept in their original order, with gaps allowed.
- **Longest increasing subsequence (LIS):** the longest subsequence whose values strictly increase.
- **Patience sorting:** the O(n log n) LIS method that keeps the smallest tail for each length.
- **"Ending at i" state:** a DP state describing the best answer that finishes exactly at position i.
mistakes:
- Using greedy coin change for an arbitrary coin system.
- Putting the loops in the wrong order and counting sequences instead of combinations (or the reverse).
- Using `bisect_right` for a strictly increasing LIS.
- Treating the `tails` list as an actual longest increasing subsequence.

glance:
- Fewest coins | dp[a] = 1 + min(dp[a − c]) | O(amount · coins) | O(amount)
- Number of coin combinations | coins in the outer loop: dp[a] += dp[a − c] | O(amount · coins) | O(amount)
- Maximum subarray (Kadane) | here = max(x, here + x); best = max(best, here) | O(n) | O(1)
- LIS (simple) | dp[i] = 1 + max(dp[j]) for j < i with nums[j] < nums[i] | O(n²) | O(n)
- LIS (fast) | tails + bisect_left | O(n log n) | O(n)
- Word break | ok[i] = any(ok[j] and s[j:i] in words) | O(n · L) checks | O(n)
- Decode ways | dp[i] = dp[i − 1] (valid 1 digit) + dp[i − 2] (10–26) | O(n) | O(n), or O(1)

@@ dp-grids-strings
topics: unique paths and obstacles, minimum path sum, one-row space saving, longest common subsequence and rebuilding it, edit distance and its uses, longest palindromic subsequence and substring, two-sequence DP patterns
terms:
- **2-D DP:** a dynamic program whose state needs two indexes, dp[i][j].
- **Longest common subsequence (LCS):** the longest sequence appearing in order, with gaps allowed, in two strings.
- **Edit (Levenshtein) distance:** the fewest insertions, deletions and substitutions turning one string into another.
- **Prefix:** the first i characters of a string; two-string DP compares prefixes.
- **Backtracking a DP table:** walking back from the answer cell to rebuild the actual solution.
- **Palindrome:** a string that reads the same forwards and backwards.
mistakes:
- Off-by-one errors between table indexes (i) and string indexes (i − 1).
- Forgetting the base row and column (empty prefixes).
- Treating edit distance as counting differing positions (Hamming distance).
- Overwriting a one-row table in an order that destroys values still needed.

glance:
- Unique paths (right/down) | paths[r][c] = above + left; or C(m + n − 2, m − 1) | O(m · n) | O(n)
- Minimum path sum | cost[r][c] = grid[r][c] + min(above, left) | O(m · n) | O(n) with one row
- Longest common subsequence | match: diagonal + 1; else max(above, left) | O(m · n) | O(m · n), O(n) for the length only
- Edit distance | match: diagonal; else 1 + min(diagonal, above, left) | O(m · n) | O(n) with two rows
- Longest palindromic subsequence | LCS(s, reversed s) | O(n²) | O(n)
- Longest palindromic substring | expand around 2n − 1 centres | O(n²) | O(1)

@@ knapsack-and-more
topics: 0/1 knapsack in 2-D and 1-D, loop direction, unbounded knapsack, rebuilding the chosen items, pseudo-polynomial time, subset sum and equal partition, the big-integer bitset trick, interval DP and matrix-chain order, bitmask DP and the travelling salesman problem, DP on trees, choosing a DP shape
terms:
- **0/1 knapsack:** choose items, each at most once, to maximise value within a weight limit.
- **Unbounded knapsack:** the same, but each item can be used any number of times.
- **Subset sum:** deciding whether some subset of numbers adds up to a target.
- **Pseudo-polynomial time:** polynomial in a number's value (like W) rather than in the input's length.
- **Interval DP:** DP over ranges i..j, splitting each range and combining the parts.
- **Bitmask DP:** DP whose state includes a set of items stored as the bits of an integer.
- **Held-Karp algorithm:** the O(2ⁿ · n²) bitmask DP for the travelling salesman problem.
- **Tree DP:** computing each node's answer from its children's answers, usually in postorder.
mistakes:
- Looping capacities upwards in a 0/1 knapsack, which reuses items.
- Forgetting to reject an odd total in the equal-partition problem.
- Filling an interval table by start position instead of by interval length.
- Using a value-per-weight greedy for the 0/1 knapsack.

glance:
- 0/1 knapsack | dp[w] = max(dp[w], dp[w − wt] + val), w downwards | O(n · W) | O(W)
- Unbounded knapsack | the same with w upwards | O(n · W) | O(W)
- Subset sum / equal partition | can[s] = can[s] or can[s − x], s downwards; or a big-integer bitset shifted by x | O(n · S) | O(S)
- Matrix-chain order (interval DP) | dp[i][j] = min over k of dp[i][k] + dp[k+1][j] + cost | O(n³) | O(n²)
- Travelling salesman (Held-Karp) | dp[mask][j] over subsets | O(2ⁿ · n²) | O(2ⁿ · n)
- House robber on a tree | each node returns (take, skip) | O(n) | O(h)

@@ greedy
topics: the greedy-choice property, exchange arguments, activity selection, greedy counterexamples, fractional knapsack, jump games, the gas station, Huffman coding, two-pointer pairing, testing greedy rules against brute force
terms:
- **Greedy algorithm:** an algorithm that makes the locally best choice at each step and never reconsiders.
- **Greedy-choice property:** some optimal solution begins with the greedy choice.
- **Exchange argument:** a proof that swapping the greedy choice into an optimal solution keeps it optimal.
- **Activity selection:** choosing the most non-overlapping intervals; solved by earliest end first.
- **Fractional knapsack:** a knapsack where items can be split; solved by value per weight.
- **Huffman coding:** an optimal prefix code built by repeatedly merging the two least frequent symbols.
- **Prefix code:** a set of codes where no code is the start of another, so decoding is unambiguous.
mistakes:
- Trusting a greedy rule because it works on the examples given.
- Sorting by the wrong key (start time or length instead of end time).
- Using ratio greedy for the 0/1 knapsack or largest-coin greedy for arbitrary coins.
- Forgetting to test against brute force on small random inputs.

glance:
- Activity selection | sort by end; take each interval starting after the last end | O(n log n) | O(1) extra
- Fractional knapsack | sort by value / weight; take greedily, cut the last item | O(n log n) | O(1) extra
- Can reach the end | track the farthest reachable index | O(n) | O(1)
- Fewest jumps | BFS levels: count a jump when the current range ends | O(n) | O(1)
- Gas station | impossible if total < 0; restart after each negative tank | O(n) | O(1)
- Huffman coding / cheapest rope joining | heap: merge the two smallest | O(n log n) | O(n)
- Boats (pairs under a limit) | sort; heaviest with lightest if they fit | O(n log n) | O(1) extra

@@ intervals-sweep
topics: closed and half-open intervals, the overlap test, merging intervals, inserting an interval, intersecting two interval lists, fewest removals, meeting rooms with a heap or a sweep line, event sorting, difference arrays
terms:
- **Interval:** a range from a start to an end, such as a meeting or a booking.
- **Half-open interval [a, b):** includes a but not b, so [1, 3) and [3, 5) don't overlap.
- **Overlap test:** two intervals overlap when each starts before the other ends.
- **Sweep line:** processing sorted events in order along a line while keeping a running state.
- **Event:** a point where something changes, such as +1 at a meeting's start and −1 at its end.
- **Difference array:** an array of changes (+k at l, −k at r + 1) whose prefix sums give the final values.
mistakes:
- Mixing up closed and half-open intervals at shared endpoints.
- Forgetting `max` when extending a merged interval that contains the next one.
- Sorting by start when a scheduling problem needs sorting by end (or the reverse).
- Processing starts before ends at the same time in a half-open sweep.

glance:
- Overlap test | a.start ≤ b.end and b.start ≤ a.end (strict for half-open) | O(1) | O(1)
- Merge intervals | sort by start; extend the last or append | O(n log n) | O(n)
- Insert into sorted intervals | copy before, absorb overlapping, copy after | O(n) | O(n)
- Intersect two sorted lists | two pointers; advance the earlier end | O(m + n) | O(m + n)
- Fewest removals for no overlap | n − (activity selection by end) | O(n log n) | O(1) extra
- Meeting rooms / maximum overlap | heap of end times, or sorted ±1 events | O(n log n) | O(n)
- Many range additions | difference array + one prefix sum | O(n + updates) | O(n)
