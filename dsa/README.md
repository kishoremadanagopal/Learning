# Data Structures and Algorithms in Python

A hands-on DSA course for complete beginners: 23 lessons on how to think about a problem, how fast code really is (Big-O), and the data structures and algorithm patterns behind coding interviews: arrays and hashing, two pointers, sliding windows, stacks, queues, linked lists, recursion, binary search, sorting, trees, heaps, graphs, dynamic programming, greedy and backtracking.

Every exercise is checked like a coding-interview site: **hidden test cases** (including the tricky edge cases) and a **speed check** that tells you when a correct answer is too slow. When you're stuck, a help ladder takes you from a **step-by-step approach**, through **three hints**, to a full **walkthrough** with a trace table that shows the code running.

Data structures and algorithms are part of the shared core for both the **AI engineer** and the **data / AI analyst** paths: they're how technical interviews test problem solving, and they decide whether your code takes a second or an hour on real data.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/learning/dsa/)

The sandbox runs real Python 3.14 inside your browser (via [Pyodide](https://pyodide.org)), with the whole standard library: `collections`, `heapq`, `bisect`, `functools` and more. Nothing to install, no sign-up.

- every lesson, with **98 examples** you can run and change
- **49 exercises** with hidden tests and speed checks, each with an approach, hints and a walkthrough
- **92 quiz questions**, with explanations
- a diagram for every data structure and pattern
- your progress and code saved in your own browser

**Before you start:** you should be comfortable with Python basics: lists, dictionaries, loops and functions. If not, do [Learn Python from scratch](../python/) first (Parts 1 to 4 are enough). No maths beyond school arithmetic is needed.

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 23 lessons, each with key terms, examples, common mistakes, exercises, walkthroughs and a quiz |
| 📖 [Glossary](glossary.md) | every DSA term used in the course, defined in plain English |
| 🧾 [Cheat sheet](cheatsheet.md) | Big-O of every operation, the 6-step problem-solving method, and a "clue words → pattern" table |

## How to use this course

1. Read a lesson, here on GitHub or in the sandbox. Start with its **Key terms**.
2. Run the examples in the sandbox and change them to see what happens.
3. For each exercise, work through the **6 steps** (understand, examples, brute force, pattern, plan, code) before typing, then press **Check**.
4. Stuck? Open **How to approach it**, then the hints one at a time. Open the **walkthrough** only after a real attempt, and then solve it again without looking.

## Lessons

### Part 1: Foundations (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 1 | [What data structures and algorithms are](lessons/01-what-is-dsa.md) | data structures vs algorithms, the structures in this course, why the right choice matters, how exercises and the help ladder work | 1–2 |
| 2 | [How to approach any problem: the 6-step method](lessons/02-problem-solving.md) | the 6-step method, understanding the problem, examples and edge cases, brute force first, spotting the pattern, planning in pseudocode, testing, clue words | 3–4 |
| 3 | [Big-O: how running time grows](lessons/03-big-o.md) | Big-O notation, counting steps, dropping constants and lower terms, O(1) O(log n) O(n) O(n log n) O(n²) O(2ⁿ), loops that add vs multiply, halving, hidden loops | 5–6 |
| 4 | [Space, best and worst cases, amortised cost](lessons/04-space-and-cases.md) | space complexity, extra vs input memory, in-place algorithms, the call stack, best/average/worst case, amortised analysis, list growth | 7–8 |
| 5 | [The real cost of Python's built-ins](lessons/05-python-costs.md) | cost of list, dict, set and string operations, insert/pop at the front, slicing copies, hashable keys, deque, timing with perf_counter, doubling experiments | 9–10 |

### Part 2: Arrays and Strings (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 6 | [Arrays and Python lists](lessons/06-arrays.md) | contiguous memory, why indexing is O(1), dynamic arrays, the cost of inserting and deleting, loop patterns, off-by-one errors, running minimum, rotating with three reversals | 11–12 |
| 7 | [Two pointers](lessons/07-two-pointers.md) | opposite-ends pointers, pair sum in a sorted array, palindromes, read/write pointers, removing duplicates and zeros in place, merging sorted lists, why each move is safe | 13–14 |
| 8 | [Sliding window](lessons/08-sliding-window.md) | fixed-size windows, variable windows that grow and shrink, the template, why it's O(n), longest substring without repeats, shortest subarray with a target sum, when windows don't work | 15–16 |
| 9 | [Prefix sums and difference arrays](lessons/09-prefix-sums.md) | prefix-sum arrays, O(1) range sums, the leading zero, running left sums, pivot index, difference arrays for range updates, 2-D prefix sums | 17–18 |
| 10 | [2-D grids and matrices](lessons/10-matrices.md) | grids as lists of lists, rows and columns, the aliasing trap, direction lists and bounds checks, transpose and rotate, zip(*grid), spiral order, searching a sorted matrix | 19–20 |
| 11 | [Working with strings](lessons/11-strings.md) | immutability, building strings with join, characters and ord/chr, counting letters, anagrams by sorting or counting, split and join, run-length encoding, reversing words | 21–22 |
| 12 | [Pattern matching: naive, KMP and Rabin-Karp](lessons/12-string-matching.md) | substring search, naive O(n·m) matching, KMP and the LPS failure table, Rabin-Karp and rolling hashes, collisions, choosing a method, other algorithms | 23–24 |

### Part 3: Hashing (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 13 | [How hash tables work](lessons/13-hash-tables.md) | hash functions, buckets, collisions, separate chaining vs open addressing, load factor and resizing, average O(1) vs worst O(n), hash randomisation, hashable keys, building a hash map | 25 |
| 14 | [Hashing patterns: counting, Two Sum, grouping](lessons/14-hashing-patterns.md) | counting with Counter and dict.get, first unique character, Two Sum with complements, grouping with defaultdict, choosing a key, prefix sums with a hash map, longest consecutive sequence, pattern summary | 26–28 |

### Part 4: Linked Lists, Stacks and Queues (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 15 | [Linked lists](lessons/15-linked-lists.md) | nodes and pointers, traversal, insert and delete, the dummy (sentinel) node, tail pointers, doubly and circular linked lists, linked list vs array | 29–30 |
| 16 | [Linked list patterns: reverse, fast and slow pointers, merge](lessons/16-linked-list-patterns.md) | reversing in place, recursion vs iteration, fast and slow pointers, the middle node, Floyd's cycle detection and cycle start, merging sorted lists, a gap of k, palindrome lists | 31–33 |
| 17 | [Stacks](lessons/17-stacks.md) | last in first out, lists as stacks, matching brackets, a min stack, reverse Polish notation, shunting-yard, the call stack and recursion | 34–36 |
| 18 | [Monotonic stacks: next greater element](lessons/18-monotonic-stack.md) | monotonic stacks, next greater and next smaller element, previous greater (stock span), largest rectangle in a histogram, trapping rain water, amortised O(n) | 37–38 |
| 19 | [Queues, circular buffers and deques](lessons/19-queues-deques.md) | first in first out, collections.deque, why not list.pop(0), bounded deques, circular buffers, a queue from two stacks, amortised O(1), the monotonic deque, other kinds of queue | 39–40 |
| 20 | [Designing a data structure: the LRU cache](lessons/20-lru-cache.md) | caches and eviction, LRU design with a hash map and a doubly linked list, OrderedDict, functools.lru_cache and cache, LFU caches, how to approach design questions | 41 |

### Part 5: Recursion (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 21 | [Recursion and recursion trees](lessons/21-recursion.md) | base and recursive cases, the call stack, the leap of faith, recursion on nested data, recursion trees, memoisation, recursion limits and when to use a loop, the Tower of Hanoi | 42–43 |
| 22 | [Divide and conquer](lessons/22-divide-and-conquer.md) | divide, conquer and combine, fast exponentiation, modular power, merge sort, counting inversions, maximum subarray by halves, the master theorem, when divide and conquer fits | 44–45 |
| 23 | [Backtracking: subsets, permutations, N-Queens](lessons/23-backtracking.md) | the choose-explore-unchoose template, subsets, permutations, combinations, itertools, N-Queens with sets, a Sudoku solver, word search, pruning, recognising backtracking problems | 46–49 |

## Running it on your own computer

Everything in the course works in any Python 3.10 or newer, with no extra packages. Copy a function into a file or notebook and call it with your own inputs.

## Editing the course

Lessons are generated from the Markdown sources in [`course/`](course/). See [course/README.md](course/README.md).
