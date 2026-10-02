@@ recursion
topics: base and recursive cases, the call stack, the leap of faith, recursion on nested data, recursion trees, memoisation, recursion limits and when to use a loop, the Tower of Hanoi
terms:
- **Recursion:** a function solving a problem by calling itself on smaller versions of it.
- **Base case:** an input small enough to answer directly, which stops the recursion.
- **Recursive case:** the part that breaks the problem down and makes the recursive calls.
- **Leap of faith:** assuming the function already works on smaller inputs while writing it.
- **Recursion tree:** a drawing of every call as a node, with its recursive calls as children.
- **Recursion depth:** how many calls are waiting on the stack at once; it decides the stack space.
- **Memoisation:** storing each result the first time it's computed and reusing it.
- **Tail call:** a recursive call that is the very last thing a function does; Python doesn't optimise these.
- **RecursionError:** Python's error when the call stack goes deeper than its limit (about 1,000 by default).
mistakes:
- A base case that some inputs never reach (for example, n going negative).
- Forgetting to `return` the recursive result.
- Recursing on very long linked lists or big counts, past Python's recursion limit.
- Slicing lists or strings at every level without realising it adds O(n) work per call.

glance:
- Factorial | n × factorial(n − 1), base case n ≤ 1 | O(n) | O(n) stack
- Sum / reverse / palindrome by recursion | handle one item, recurse on the rest | O(n) with indexes (O(n²) with slicing) | O(n) stack
- Nested data (folders, nested lists) | recurse into each sub-container | O(total items) | O(depth)
- Naive Fibonacci | fib(n − 1) + fib(n − 2) | O(2ⁿ) (about 1.6ⁿ) | O(n)
- Memoised Fibonacci | cache each fib(k) | O(n) | O(n)
- Tower of Hanoi | move n − 1, move 1, move n − 1 | O(2ⁿ) moves | O(n) stack
- Flatten a nested list | extend with flatten(sub-list), append numbers | O(n) | O(depth)

@@ divide-and-conquer
topics: divide, conquer and combine, fast exponentiation, modular power, merge sort, counting inversions, maximum subarray by halves, the master theorem, when divide and conquer fits
terms:
- **Divide and conquer:** split a problem into smaller independent subproblems, solve them recursively, combine the answers.
- **Fast (binary) exponentiation:** computing xⁿ by squaring, in O(log n) multiplications.
- **Modular arithmetic:** working with remainders after division by a modulus, to keep numbers small.
- **Merge sort:** sort each half recursively, then merge the sorted halves.
- **Inversion:** a pair of positions i < j whose values are out of order (nums[i] > nums[j]).
- **Recurrence relation:** an equation for an algorithm's cost in terms of its cost on smaller inputs, like T(n) = 2T(n/2) + n.
- **Master theorem:** a rule for solving recurrences of the form T(n) = a·T(n/b) + O(nᵈ).
- **Overlapping subproblems:** when the same subproblem is needed many times; a sign to use memoisation instead.
mistakes:
- Calling the recursive half twice (`f(n // 2) * f(n // 2)`), which throws away the speed-up.
- Forgetting the "crossing the middle" case when combining halves.
- Using divide and conquer on overlapping subproblems (like Fibonacci) without memoisation.
- Not taking the modulus after every multiplication, so numbers grow huge.

glance:
- Fast power xⁿ | square the half-power; multiply in x when n is odd | O(log n) | O(1) loop / O(log n) recursive
- Merge sort | sort halves recursively, merge | O(n log n) | O(n)
- Count inversions | count during merge sort's merge: add len(left) − i | O(n log n) | O(n)
- Maximum subarray (D&C) | best of left, right, and crossing the middle | O(n log n) | O(log n)
- Master theorem | compare a with bᵈ: same → nᵈ log n; smaller → nᵈ; larger → n^(log_b a) | — | —

@@ backtracking
topics: the choose-explore-unchoose template, subsets, permutations, combinations, itertools, N-Queens with sets, a Sudoku solver, word search, pruning, recognising backtracking problems
terms:
- **Backtracking:** building candidates one choice at a time and undoing choices that can't lead to a solution.
- **Decision tree:** the tree of all choices; backtracking explores it depth first.
- **Pruning:** skipping a branch as soon as it can't lead to a valid answer.
- **Subset:** any selection of items, including none and all; n items have 2ⁿ subsets.
- **Permutation:** an ordering of items; n items have n! permutations.
- **Combination:** a selection where order doesn't matter; choosing k of n gives C(n, k).
- **N-Queens:** placing n queens on an n × n board so none attack each other.
- **itertools:** Python's module with fast permutations, combinations and product.
mistakes:
- Saving `path` instead of a copy `path[:]`.
- Forgetting to undo a choice (pop, unmark) after the recursive call.
- Looping from 0 in combination problems, which produces the same combination in different orders.
- Trying backtracking on large inputs where an exponential search can't finish.

glance:
- Subsets | include or skip each item | O(n · 2ⁿ) | O(n) + output
- Permutations | at each position try every unused item | O(n · n!) | O(n) + output
- Combinations (k of n) | loop forward from a start index; prune when too few remain | O(k · C(n, k)) | O(k) + output
- Combination sum (reuse allowed) | sorted candidates, recurse with the same index, break when too big | exponential | O(target / smallest)
- N-Queens | one queen per row; sets of columns, row − col, row + col | O(n!) worst, heavily pruned | O(n)
- Sudoku | fill an empty cell with each valid digit, undo on dead ends | exponential worst | O(81)
- Word search | DFS from each cell, mark used cells, unmark after | O(r · c · 4ᴸ) | O(L)
