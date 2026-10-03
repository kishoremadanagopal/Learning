# Data structures and algorithms glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **0-1 BFS** | A BFS with a deque for edge weights of 0 or 1; 0-cost neighbours go to the front. [36] |
| **0/1 knapsack** | Choose items, each at most once, to maximise value within a weight limit. [44] |
| **2-D DP** | A dynamic program whose state needs two indexes, dp[i][j]. [43] |
| **Activity selection** | Choosing the most non-overlapping intervals; solved by earliest end first. [45] |
| **Adaptive sort** | A sort that runs faster on input that is already partly sorted. [26] |
| **Adjacency list** | For each vertex, a list of its neighbours. [35] |
| **Adjacency matrix** | A V × V grid with a mark where two vertices are joined. [35] |
| **Admissible heuristic** | An estimate that never overestimates the true remaining cost. [38] |
| **Algorithm** | A precise, step-by-step recipe for solving a problem. [1] |
| **Aliasing** | Two names (or list slots) referring to the same object, so changing one changes the other. [10] |
| **Amortised analysis** | Bounding the total cost of many operations, so an occasional expensive step averages out. [18] |
| **Amortised cost** | The average cost per operation over a long sequence, when rare operations are expensive and most are cheap. [4] |
| **Anagram** | A word made by rearranging all the letters of another. [11] |
| **Array** | Items stored side by side in one contiguous block of memory, each reachable by its index in O(1). [6] |
| **Articulation point (cut vertex)** | A vertex whose removal disconnects the graph. [40] |
| **A\* search** | Dijkstra ordered by cost so far plus a heuristic estimate of the cost remaining. [38] |
| **Autocomplete** | Suggesting stored words that start with what has been typed. [33] |
| **Average case** | The expected work over typical inputs. [4] |
| **AVL tree** | A self-balancing BST where sibling subtree heights differ by at most 1. [31] |
| **Backtracking** | Building candidates one choice at a time and undoing choices that can't lead to a solution. [23] |
| **Backtracking a DP table** | Walking back from the answer cell to rebuild the actual solution. [43] |
| **Balanced tree** | A tree whose height stays O(log n). [29] |
| **Base case** | An input small enough to answer directly, which stops the recursion. [21, 41] |
| **Bellman-Ford** | Relaxes every edge V − 1 times; handles negative weights and detects negative cycles. [38] |
| **Best case** | The input that makes the algorithm do the least work. [4] |
| **Bidirectional BFS** | Searching from the start and the goal at once until the two searches meet. [36] |
| **Big-O notation** | Describes how the number of steps (or memory) grows as the input size n grows, ignoring constants. [3] |
| **Binary heap** | A complete binary tree where every parent is ≤ its children (min-heap) or ≥ them (max-heap). [32] |
| **Binary search** | Repeatedly halving a sorted range by comparing with its middle item. [24] |
| **Binary search on the answer** | Binary searching over the possible values of the answer, using a yes/no test. [25] |
| **Binary search tree (BST)** | A binary tree where every left subtree holds smaller values and every right subtree bigger ones. [31] |
| **Binary tree** | A tree where each node has at most two children, left and right. [29] |
| **Bipartite graph** | A graph whose vertices split into two sides with every edge between the sides. [40] |
| **bisect_left / bisect_right** | The first position where x could be inserted keeping the order (before / after equal items). [24] |
| **Bitmask DP** | DP whose state includes a set of items stored as the bits of an integer. [44] |
| **Bounds check** | Testing 0 <= r < rows and 0 <= c < cols before using a cell. [10] |
| **Breadth-first search (BFS)** | Visiting level by level, using a queue. [29] |
| **Bridge** | An edge whose removal disconnects the graph. [40] |
| **Brute force** | The simplest correct solution, usually trying every possibility; often slow but a good start. [2] |
| **B-tree** | A balanced search tree with many keys per node, used by databases and file systems. [31] |
| **Bubble sort** | Repeatedly swaps neighbouring items that are out of order. [26] |
| **Bucket** | A slot in a hash table's internal array where entries are stored. [13] |
| **Bucket sort** | Spreads evenly distributed values into buckets, sorts each bucket, and joins them. [28] |
| **Cache** | Fast storage that keeps recent or frequent results so they don't have to be recomputed or fetched again. [20] |
| **Cache hit / miss** | The item was in the cache / it wasn't. [20] |
| **Call stack** | The memory Python uses to remember function calls that haven't finished yet. [4, 17] |
| **Capacity** | The space a list has reserved; it grows by a factor when full. [4] |
| **Ceiling division** | Dividing and rounding up, `(a + b - 1) // b` for positive integers. [25] |
| **Circular linked list** | The last node points back to the first. [15] |
| **Circular (ring) buffer** | A fixed-size array used as a queue, with indexes that wrap around using `%`. [19] |
| **Clue words** | Phrases in a problem that point to a pattern, like "contiguous subarray" → sliding window. [2] |
| **cmp_to_key** | Turns an old-style comparison function into a key function. [28] |
| **Collision** | Two different keys landing in the same bucket. [13] |
| **Combination** | A selection where order doesn't matter; choosing k of n gives C(n, k). [23] |
| **Comparison sort** | A sort that learns about the data only by comparing pairs of items. [28] |
| **Complement** | The value needed to complete a pair, such as target − x. [14] |
| **Complete binary tree** | Every level full except possibly the last, which fills from the left. [29] |
| **Connected component** | A maximal group of vertices that can all reach each other. [35] |
| **Consecutive sequence** | Integers that follow each other without gaps, like 3, 4, 5. [14] |
| **Constraint** | A limit given in the problem, such as the input size or value range; it hints at the Big-O you need. [2] |
| **Contiguous** | Stored in one unbroken block, next to each other. [6] |
| **Coordinate compression** | Replacing values by their rank in sorted order, so they index a small array. [34] |
| **Counter** | A dict subclass from collections that counts items; missing keys count as 0. [14] |
| **Counting sort** | Counts how many times each small integer appears, then writes them out in order. [28] |
| **Critical path** | The longest chain of dependent tasks; it decides the earliest finishing time of a project. [37] |
| **Cut property** | The cheapest edge crossing any split of the vertices is safe to include in an MST. [39] |
| **Cycle** | A loop in the links, so following `next` never reaches None. [16] |
| **DAG (directed acyclic graph)** | A directed graph with no cycles; exactly the graphs with a topological order. [37] |
| **Data structure** | A way of organising data in memory so certain operations are fast, such as a list, dict or tree. [1] |
| **Decision tree** | The tree of all choices; backtracking explores it depth first. [23] |
| **defaultdict** | A dict that creates a default value (like an empty list) for missing keys. [14] |
| **Degenerate tree** | A tree where every node has one child, so it behaves like a linked list. [31] |
| **Degree** | The number of edges at a vertex; in-degree and out-degree for directed graphs. [35] |
| **Depth-first search (DFS)** | Exploring as deep as possible along a branch before backing up. [29] |
| **Depth / height** | Edges from the root down to a node / edges on the longest root-to-leaf path. [29] |
| **deque** | A double-ended queue from `collections` with O(1) adds and removals at both ends. [5, 19] |
| **Diameter** | The number of edges on the longest path between any two nodes. [30] |
| **Difference array** | Records where range updates start and stop; a prefix sum of it gives the final values. [9, 46] |
| **Dijkstra's algorithm** | Repeatedly settles the closest unsettled vertex; needs non-negative weights. [38] |
| **Directed / undirected graph** | Edges go one way / both ways. [35] |
| **Direction list** | Offsets like (−1, 0), (1, 0), (0, −1), (0, 1) used to visit neighbours in a loop. [10] |
| **Divide and conquer** | Split a problem into smaller independent subproblems, solve them recursively, combine the answers. [22] |
| **Dominant term** | The fastest-growing part of a step count, the only one Big-O keeps. [3] |
| **Doubling experiment** | Timing code at n, 2n, 4n to see how the time grows. [5] |
| **Doubly linked list** | Nodes point both forwards (`next`) and backwards (`prev`). [15] |
| **Dummy (sentinel) node** | A placeholder node before the head (or after the tail) that removes special cases. [15] |
| **Dutch national flag** | A one-pass, three-pointer partition into three groups. [26] |
| **Dynamic array** | An array that grows automatically by reserving spare room; Python's list. [6] |
| **Dynamic programming (DP)** | Solving a problem by combining stored answers to smaller versions of it, each computed once. [41] |
| **Edge case** | An unusual input at the boundaries, such as an empty list, one item, negatives or duplicates. [1] |
| **Edit (Levenshtein) distance** | The fewest insertions, deletions and substitutions turning one string into another. [43] |
| **"Ending at i" state** | A DP state describing the best answer that finishes exactly at position i. [42] |
| **End-of-word flag** | A marker on the node where a complete word ends. [33] |
| **Enqueue / dequeue** | Add at the back / remove from the front. [19] |
| **Eulerian path** | A path that uses every edge exactly once. [40] |
| **Event** | A point where something changes, such as +1 at a meeting's start and −1 at its end. [46] |
| **Eviction** | Removing an item from a full cache to make room. [20] |
| **Exchange argument** | A proof that swapping the greedy choice into an optimal solution keeps it optimal. [45] |
| **External sorting** | Sorting data too big for memory by sorting chunks and merging them. [27] |
| **Fast and slow pointers** | Two pointers moving at different speeds (usually 2 steps and 1 step) through a list. [16] |
| **Fast (binary) exponentiation** | Computing xⁿ by squaring, in O(log n) multiplications. [22] |
| **Feasibility check** | A function that answers "does this candidate value work?" [25] |
| **Fenwick tree (binary indexed tree)** | An array where position i stores the sum of a block ending at i, of length i & -i. [34] |
| **FIFO** | First in, first out. [19] |
| **Fixed-size window** | A window of exactly k items; one item joins and one leaves at each step. [8] |
| **Floor / ceiling** | The largest value ≤ x / the smallest value ≥ x. [31] |
| **Floyd's cycle detection** | The tortoise-and-hare method: if fast and slow ever meet, there's a cycle. [16] |
| **Floyd-Warshall** | All-pairs shortest paths by allowing each vertex in turn as a stopover. [38] |
| **Fractional knapsack** | A knapsack where items can be split; solved by value per weight. [45] |
| **Frequency count** | How many times each item appears, usually in a dict or Counter. [14] |
| **frozenset** | An immutable set, usable as a dict key. [13] |
| **Function** | A named block of code that takes inputs (arguments) and returns an output. [1] |
| **Graph** | A set of vertices joined by edges. [35] |
| **Greedy algorithm** | An algorithm that makes the locally best choice at each step and never reconsiders. [45] |
| **Greedy-choice property** | Some optimal solution begins with the greedy choice. [45] |
| **Grey vertex** | In DFS cycle detection, a vertex on the current path; reaching one again means a directed cycle. [37] |
| **Grid / matrix** | Values arranged in rows and columns; grid[r][c] is row r, column c. [10] |
| **Grouping key** | A normalised form shared by everything that belongs together, like sorted letters for anagrams. [14] |
| **Half-open interval [a, b)** | Includes a but not b, so [1, 3) and [3, 5) don't overlap. [46] |
| **Half-open template** | `while lo < hi` with `hi = mid` and `lo = mid + 1`; ends with lo == hi. [25] |
| **Hashable** | A value that can be a dict key or set item because it can't change, such as numbers, strings and tuples. [5] |
| **Hash collision** | Two different inputs with the same hash value. [12] |
| **Hash function** | Turns a key into a number (its hash); the same key always gives the same hash. [13] |
| **Hash randomisation** | Python changes string hashes each run, so attackers can't force collisions. [13] |
| **Hash table** | The structure behind dict and set; finds keys in O(1) on average. [5] |
| **Head** | The first node of a linked list; the list is reached through it. [15] |
| **Heapify** | Turning a whole list into a heap in O(n), by sifting down from the last parent to the root. [32] |
| **heapq** | Python's module that treats an ordinary list as a min-heap. [32] |
| **Heap sort** | Builds a max-heap in the array, then repeatedly moves the maximum to the end. [27] |
| **Height-balanced** | At every node, the left and right subtree heights differ by at most 1. [30] |
| **Held-Karp algorithm** | The O(2ⁿ · n²) bitmask DP for the travelling salesman problem. [44] |
| **Hidden test** | A test case the checker runs without showing it to you first, like on coding-interview sites. [1] |
| **Histogram** | A row of bars of different heights. [18] |
| **Huffman coding** | An optimal prefix code built by repeatedly merging the two least frequent symbols. [45] |
| **Immutable** | Can't be changed after it's created; "changing" a string makes a new one. [5, 11] |
| **Implicit graph** | A graph whose edges are computed on the fly, such as the cells of a grid. [35] |
| **Inclusion–exclusion** | Adding and subtracting overlapping areas so each is counted once; used by 2-D prefix sums. [9] |
| **In-degree** | The number of edges coming into a vertex, such as unmet prerequisites. [37] |
| **Index** | The position of an item, starting at 0. [6] |
| **Infix notation** | The usual way of writing expressions, like `3 + 4`. [17] |
| **Inorder successor** | The next value in sorted order; for a node with a right subtree, the leftmost node of that subtree. [31] |
| **In place** | Changing the input directly with only O(1) extra memory. [4] |
| **In-place** | Changing the existing structure instead of building a new one, using O(1) extra memory. [16] |
| **In-place sort** | A sort that rearranges the list itself with O(1) extra memory. [26] |
| **Insertion sort** | Grows a sorted prefix, sliding each new item left into position. [26] |
| **Interval** | A range from a start to an end, such as a meeting or a booking. [46] |
| **Interval DP** | DP over ranges i..j, splitting each range and combining the parts. [44] |
| **Introsort** | Quicksort that switches to heap sort when recursion gets too deep. [27] |
| **Invariant** | A statement that stays true on every loop pass, such as "if the target exists, it's in nums[lo..hi]". [24] |
| **Inversion** | A pair of positions i < j whose values are out of order (nums[i] > nums[j]). [22] |
| **itertools** | Python's module with fast permutations, combinations and product. [23] |
| **join** | `sep.join(parts)` glues a list of strings together with sep between them, in one pass. [11] |
| **Kadane's algorithm** | The O(n) maximum-subarray DP that tracks the best sum ending at each position. [42] |
| **Kahn's algorithm** | Repeatedly take a vertex with in-degree 0 and remove its outgoing edges. [37] |
| **Key function** | A function that gives the value to sort each item by, as in `sorted(items, key=len)`. [28] |
| **KMP (Knuth–Morris–Pratt)** | A search that uses a table of the pattern's prefix-suffixes so it never re-reads the text; O(n + m). [12] |
| **Kruskal / Prim** | Build an MST by cheapest edges overall with union-find / by growing one tree with a heap. [39] |
| **Lazy deletion** | Marking items as removed and skipping them when they reach the top. [32, 38] |
| **Lazy propagation** | Storing a pending range update at a node and passing it down only when needed. [34] |
| **Leap of faith** | Assuming the function already works on smaller inputs while writing it. [21] |
| **LFU (least frequently used)** | Evicts the item used the fewest times. [20] |
| **LIFO** | Last in, first out. [17] |
| **Linear search** | Checking items one by one until the target is found. [4, 24] |
| **Linked list** | A sequence of nodes where each node points to the next one. [15] |
| **Load factor** | Number of entries ÷ number of buckets; higher means more collisions. [13] |
| **Logarithm (log₂ n)** | How many times you can halve n before reaching 1. [3] |
| **Lomuto partition** | A partition scheme that sweeps left to right, swapping smaller items to the front. [27] |
| **Longest common subsequence (LCS)** | The longest sequence appearing in order, with gaps allowed, in two strings. [43] |
| **Longest increasing subsequence (LIS)** | The longest subsequence whose values strictly increase. [42] |
| **Longest prefix match** | Finding the longest stored word that is a prefix of a given text, as routers do. [33] |
| **Lower bound** | The least work any algorithm for a problem must do; Ω(n log n) for comparison sorts. [28] |
| **Lower bound / upper bound** | The first position with a value ≥ x / > x. [24] |
| **Lowest common ancestor (LCA)** | The deepest node that has both given nodes in its subtree. [30] |
| **Lowest set bit** | The rightmost 1 bit of a number; `i & -i` in Python. [34] |
| **Low-link value** | The earliest discovery time a DFS subtree can reach with one back edge. [40] |
| **LPS table** | For each prefix of the pattern, the length of its longest proper prefix that is also a suffix. [12] |
| **@lru_cache / @cache** | Python decorators that memoise a function (bounded with LRU eviction / unbounded). [20] |
| **LRU (least recently used)** | Evicts the item that hasn't been used for the longest time. [20] |
| **Master theorem** | A rule for solving recurrences of the form T(n) = a·T(n/b) + O(nᵈ). [22] |
| **Maximum flow** | The most that can be sent from a source to a sink through edges with capacities. [40] |
| **Memoisation** | Caching a function's results by its arguments. [20, 21] |
| **Memoisation (top-down)** | Recursion that caches each result the first time it's computed. [41] |
| **Merge** | Combining two sorted lists into one sorted list by repeatedly taking the smaller front item. [7, 16] |
| **Merge sort** | Sort each half recursively, then merge the sorted halves. [22] |
| **Minimum cut** | The cheapest set of edges whose removal separates source from sink; equals the maximum flow. [40] |
| **Minimum spanning tree (MST)** | A spanning tree with the smallest total weight. [39] |
| **Mirror (invert)** | Swapping every node's left and right children. [30] |
| **Modular arithmetic** | Working with remainders after division by a modulus, to keep numbers small. [22] |
| **Monotonic** | Never changing direction: once the test says yes, it says yes for every larger value. [25] |
| **Monotonic deque** | A deque kept in increasing or decreasing order, used for sliding-window maximums or minimums. [19] |
| **Monotonic rule** | A rule where growing an invalid window can never make it valid again; needed for variable windows. [8] |
| **Monotonic stack** | A stack whose values stay in increasing or decreasing order; new items pop the ones that break the order. [18] |
| **Multi-source BFS** | A BFS that starts with several vertices in the queue at distance 0. [36] |
| **n** | The size of the input, such as the length of a list. [3] |
| **Naive search** | Trying every start position and comparing character by character. [12] |
| **Negative cycle** | A cycle whose weights add up to less than zero, so costs can fall forever. [38] |
| **Next greater element** | For each item, the first item to its right that is larger. [18] |
| **Node** | One item of a linked list: a value plus a pointer to the next node (and the previous one, in a doubly linked list). [15] |
| **NP-hard** | A problem with no known polynomial-time algorithm, such as the travelling salesman problem. [40] |
| **N-Queens** | Placing n queens on an n × n board so none attack each other. [23] |
| **O(1), constant time** | The work doesn't depend on n. [3] |
| **O(2ⁿ), exponential time** | Doubles with every extra item, typical of trying every subset. [3] |
| **Off-by-one error** | A loop that runs one step too many or too few, usually from a wrong range bound. [6, 24] |
| **O(log n), logarithmic time** | The work grows by one step each time n doubles, typical when the problem is halved each step. [3] |
| **O(n), linear time** | The work grows in proportion to n, typically one loop. [3] |
| **O(n log n)** | Typical of efficient sorting. [3] |
| **O(n²), quadratic time** | Typical of a loop inside a loop. [3] |
| **Open addressing** | Handling collisions by probing other buckets until a free one is found; Python's dict does this. [13] |
| **Opposite-ends pointers** | One pointer starts at each end and they move towards each other. [7] |
| **Optimal substructure** | An optimal answer is built from optimal answers to subproblems. [41] |
| **ord / chr** | Convert a character to its code number and back. [11] |
| **OrderedDict** | A dict that remembers order and can move a key to either end in O(1). [20] |
| **Overlapping subproblems** | When the same subproblem is needed many times; a sign to use memoisation instead. [22, 41] |
| **Overlap test** | Two intervals overlap when each starts before the other ends. [46] |
| **Palindrome** | Text that reads the same forwards and backwards. [7, 43] |
| **Parent link** | The vertex from which another vertex was first reached; following parents rebuilds the path. [36] |
| **Partition** | Rearranging items into groups around a value, such as smaller / equal / bigger. [26] |
| **Path compression** | Pointing every node on a find path directly at the root. [39] |
| **Patience sorting** | The O(n log n) LIS method that keeps the smallest tail for each length. [42] |
| **Pattern** | A known technique that solves a family of problems, such as two pointers or a hash map. [2] |
| **Pattern matching** | Finding where a pattern string occurs inside a text. [12] |
| **Peak element** | An item larger than its neighbours. [24] |
| **perf_counter** | `time.perf_counter()`, a precise clock for timing code. [5] |
| **Permutation** | An ordering of items; n items have n! permutations. [23] |
| **Pivot** | The item a partition splits around. [27] |
| **Pivot index** | An index where the sum to the left equals the sum to the right. [9] |
| **Pointer (reference)** | A variable that refers to an object, such as `node.next`. [15] |
| **Point update** | Changing a single item of the list. [34] |
| **Precomputation** | Doing work once up front so that many later questions are cheap. [9] |
| **Prefix** | The beginning part of a string; "ca" is a prefix of "cat". [33, 43] |
| **Prefix code** | A set of codes where no code is the start of another, so decoding is unambiguous. [45] |
| **Prefix sum** | The running total of the first k items; prefix[0] = 0. [9] |
| **Prefix-sum count** | A dict from each prefix sum to how often it has appeared, used to count subarrays with a given sum. [14] |
| **Preorder / inorder / postorder** | Visiting the node before, between or after its two subtrees. [29] |
| **Previous greater element** | For each item, the nearest item to its left that is larger. [18] |
| **Priority queue** | A queue that always serves the smallest (or most urgent) item first. [19, 32] |
| **Producer / consumer** | One part of a program adds work to a queue while another takes it off. [19] |
| **Proper prefix** | A prefix that isn't the whole string. [12] |
| **Pruning** | Skipping a branch as soon as it can't lead to a valid answer. [23] |
| **Pseudocode** | The steps of an algorithm in plain words, before writing real code. [2] |
| **Pseudo-polynomial time** | Polynomial in a number's value (like W) rather than in the input's length. [44] |
| **Push / pop / peek** | Add to the top / remove the top / look at the top without removing it. [17] |
| **Query** | A question asked of the data, such as a range sum. [9] |
| **Queue** | A collection where items join at the back and leave from the front: first in, first out. [19] |
| **Quickselect** | Partition, then continue into only the side containing position k, to find the k-th smallest. [27] |
| **Quicksort** | Partition around a pivot, then sort each side recursively. [27] |
| **Rabin-Karp** | A search that compares hashes of windows, updated with a rolling hash. [12] |
| **Radix sort** | Sorts by one digit at a time, least significant first, with a stable sort per digit. [28] |
| **Radix tree** | A compressed trie whose edges hold whole strings instead of single characters. [33] |
| **Randomised pivot** | Choosing the pivot at random so no input is reliably bad. [27] |
| **Range query** | A question about a contiguous part of a list, such as its sum or minimum. [34] |
| **Range sum** | The sum of items from index i to j; prefix[j + 1] − prefix[i]. [9] |
| **Read/write pointers** | One pointer scans every item; the other marks where the next kept item goes. [7] |
| **Recurrence relation** | An equation for an algorithm's cost in terms of its cost on smaller inputs, like T(n) = 2T(n/2) + n. [22] |
| **Recursion** | A function solving a problem by calling itself on smaller versions of it. [21] |
| **Recursion depth** | How many calls are waiting on the stack at once; it decides the stack space. [21] |
| **RecursionError** | Python's error when the call stack goes deeper than its limit (about 1,000 by default). [21] |
| **Recursion tree** | A drawing of every call as a node, with its recursive calls as children. [21] |
| **Recursive case** | The part that breaks the problem down and makes the recursive calls. [21] |
| **Red-black tree** | A self-balancing BST using node colours; used by many standard libraries. [31] |
| **Reference** | A pointer to an object; a Python list stores references, not the objects themselves. [6] |
| **Relaxation** | Updating a vertex's distance if going through a neighbouring vertex is cheaper. [38] |
| **Resize (rehash)** | Moving every entry into a bigger table when the load factor gets too high. [13] |
| **Return value** | What a function gives back with `return`; tests check this, not what it prints. [1] |
| **Reverse Polish notation (RPN)** | Writing operators after their operands, like `3 4 +`; no brackets needed. [17] |
| **Rolling hash** | A hash of a sliding window updated in O(1) as it moves. [12] |
| **Root** | The element that names its group; it is its own parent. [39] |
| **Root / leaf** | The top node / a node with no children. [29] |
| **Rotated sorted array** | A sorted list cut at some point with the two parts swapped. [24] |
| **Rotation** | Shifting every item k places, wrapping around the end. [6, 31] |
| **Run-length encoding** | Replacing runs of a repeated character with the character and its count. [11] |
| **Running best** | A pattern that walks through data once, remembering the best value seen so far. [1] |
| **Running minimum** | The smallest value seen so far while scanning. [6] |
| **Search space** | The range of candidate answers, from the smallest possible to the largest. [25] |
| **Segment tree** | A binary tree where each node stores the combined value of a range of the list. [34] |
| **Selection sort** | Repeatedly selects the smallest remaining item and swaps it into place. [26] |
| **Self-balancing BST** | A BST that restructures itself to keep its height O(log n). [31] |
| **Sentinel** | A special value (like −1 or `#`) that signals "empty" or "invalid". [30] |
| **Separate chaining** | Handling collisions by keeping a small list of entries in each bucket. [13] |
| **Serialise / deserialise** | Turning a tree into a string / rebuilding the tree from it. [30] |
| **Shortest path (unweighted)** | A path with the fewest edges. [36] |
| **Shunting-yard algorithm** | Converts infix expressions to RPN using a stack of operators and precedence rules. [17] |
| **Sift up / sift down** | Swapping an item with its parent / smaller child until the heap property holds again. [32] |
| **Sliding window** | A contiguous range [left, right] that moves through the data and is updated instead of recomputed. [8] |
| **Sorted** | Arranged in increasing (or decreasing) order; what makes opposite-ends pointers work. [7] |
| **Space complexity** | How the extra memory an algorithm needs grows with the input size. [4] |
| **Spanning tree** | V − 1 edges that connect every vertex with no cycle. [39] |
| **Sparse table** | Precomputed minimums of every power-of-two block, for O(1) static range-minimum queries. [34] |
| **Spiral order** | Visiting a grid's values clockwise from the outside ring inwards. [10] |
| **Stable** | Keeping equal items in their original order. [16] |
| **Stable sort** | A sort that keeps equal items in their original relative order. [26] |
| **Stack** | A collection where you add and remove only at the top: last in, first out. [17] |
| **Stack frame** | The record of one function call: its local variables and where to return to. [17] |
| **State** | What one DP table entry means, such as "dp[i] = ways to reach step i". [41] |
| **State graph** | An implicit graph whose vertices are situations (words, lock combinations) and whose edges are moves. [36] |
| **Stock span** | The number of consecutive days, ending today, with a price at most today's. [18] |
| **Strongly connected component (SCC)** | A maximal set of vertices in a directed graph that can all reach each other. [40] |
| **Subarray** | A contiguous run of items in an array. [8] |
| **Subsequence** | Items kept in their original order, with gaps allowed. [42] |
| **Subset** | Any selection of items, including none and all; n items have 2ⁿ subsets. [23] |
| **Subset sum** | Deciding whether some subset of numbers adds up to a target. [44] |
| **Substring** | A contiguous run of characters in a string. [8] |
| **Sweep line** | Processing sorted events in order along a line while keeping a running state. [46] |
| **Tabulation (bottom-up)** | Filling a table of answers from the smallest cases upwards with loops. [41] |
| **Tail** | The last node; its `next` is None. [15] |
| **Tail call** | A recursive call that is the very last thing a function does; Python doesn't optimise these. [21] |
| **Test case** | One input together with the expected output, used to check a function. [1] |
| **Tie-breaker** | An extra value, such as a counter, that decides between equal priorities. [32] |
| **Time complexity** | How an algorithm's running time grows with the input size. [3] |
| **Timsort** | Python's sorting algorithm: finds sorted runs and merges them; stable and adaptive. [28] |
| **Top k** | Finding the k largest or smallest items, typically with a heap of size k. [32] |
| **Topological order** | An ordering of a directed graph's vertices where every edge points forward. [37] |
| **Trade-off** | Gaining one thing (like speed) by giving up another (like memory). [2] |
| **Transition (recurrence)** | The formula that computes a state from smaller states. [41] |
| **Transpose** | Swapping rows and columns. [10] |
| **Traversal** | Visiting every node by following `next` from the head. [15] |
| **Tree** | A hierarchy of nodes with one root, where every other node has exactly one parent. [29] |
| **Tree DP** | Computing each node's answer from its children's answers, usually in postorder. [44] |
| **Trie (prefix tree)** | A tree that stores strings one character per level, sharing common prefixes. [33] |
| **Two pointers** | Two indexes that move through the data by a rule, replacing a nested loop. [7] |
| **Unbounded knapsack** | A DP where each item (such as a coin value) may be used any number of times. [42, 44] |
| **Union by size (or rank)** | Hanging the smaller tree under the larger one. [39] |
| **Union-find (disjoint set union)** | A structure that keeps elements in merging groups and answers "same group?". [39] |
| **Variable-size window** | A window that grows on the right and shrinks on the left to keep a rule true. [8] |
| **Vertex (node) / edge** | A point in the graph / a connection between two vertices. [35] |
| **Weighted graph** | Each edge carries a number such as a distance or cost. [35] |
| **Whitespace** | Spaces, tabs and newlines. [11] |
| **Wildcard** | A pattern character, such as `.`, that matches any single character. [33] |
| **Window state** | What you keep about the window (a sum, counts, a set) so updates are O(1). [8] |
| **Worst case** | The input that makes it do the most work; the usual meaning of "the complexity". [4] |
