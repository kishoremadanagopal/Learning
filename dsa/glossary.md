# Data structures and algorithms glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **Adaptive sort** | A sort that runs faster on input that is already partly sorted. [26] |
| **Algorithm** | A precise, step-by-step recipe for solving a problem. [1] |
| **Aliasing** | Two names (or list slots) referring to the same object, so changing one changes the other. [10] |
| **Amortised analysis** | Bounding the total cost of many operations, so an occasional expensive step averages out. [18] |
| **Amortised cost** | The average cost per operation over a long sequence, when rare operations are expensive and most are cheap. [4] |
| **Anagram** | A word made by rearranging all the letters of another. [11] |
| **Array** | Items stored side by side in one contiguous block of memory, each reachable by its index in O(1). [6] |
| **Average case** | The expected work over typical inputs. [4] |
| **Backtracking** | Building candidates one choice at a time and undoing choices that can't lead to a solution. [23] |
| **Base case** | An input small enough to answer directly, which stops the recursion. [21] |
| **Best case** | The input that makes the algorithm do the least work. [4] |
| **Big-O notation** | Describes how the number of steps (or memory) grows as the input size n grows, ignoring constants. [3] |
| **Binary search** | Repeatedly halving a sorted range by comparing with its middle item. [24] |
| **Binary search on the answer** | Binary searching over the possible values of the answer, using a yes/no test. [25] |
| **bisect_left / bisect_right** | The first position where x could be inserted keeping the order (before / after equal items). [24] |
| **Bounds check** | Testing 0 <= r < rows and 0 <= c < cols before using a cell. [10] |
| **Brute force** | The simplest correct solution, usually trying every possibility; often slow but a good start. [2] |
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
| **Consecutive sequence** | Integers that follow each other without gaps, like 3, 4, 5. [14] |
| **Constraint** | A limit given in the problem, such as the input size or value range; it hints at the Big-O you need. [2] |
| **Contiguous** | Stored in one unbroken block, next to each other. [6] |
| **Counter** | A dict subclass from collections that counts items; missing keys count as 0. [14] |
| **Counting sort** | Counts how many times each small integer appears, then writes them out in order. [28] |
| **Cycle** | A loop in the links, so following `next` never reaches None. [16] |
| **Data structure** | A way of organising data in memory so certain operations are fast, such as a list, dict or tree. [1] |
| **Decision tree** | The tree of all choices; backtracking explores it depth first. [23] |
| **defaultdict** | A dict that creates a default value (like an empty list) for missing keys. [14] |
| **deque** | A double-ended queue from `collections` with O(1) adds and removals at both ends. [5, 19] |
| **Difference array** | Records where range updates start and stop; a prefix sum of it gives the final values. [9] |
| **Direction list** | Offsets like (−1, 0), (1, 0), (0, −1), (0, 1) used to visit neighbours in a loop. [10] |
| **Divide and conquer** | Split a problem into smaller independent subproblems, solve them recursively, combine the answers. [22] |
| **Dominant term** | The fastest-growing part of a step count, the only one Big-O keeps. [3] |
| **Doubling experiment** | Timing code at n, 2n, 4n to see how the time grows. [5] |
| **Doubly linked list** | Nodes point both forwards (`next`) and backwards (`prev`). [15] |
| **Dummy (sentinel) node** | A placeholder node before the head (or after the tail) that removes special cases. [15] |
| **Dutch national flag** | A one-pass, three-pointer partition into three groups. [26] |
| **Dynamic array** | An array that grows automatically by reserving spare room; Python's list. [6] |
| **Edge case** | An unusual input at the boundaries, such as an empty list, one item, negatives or duplicates. [1] |
| **Enqueue / dequeue** | Add at the back / remove from the front. [19] |
| **Eviction** | Removing an item from a full cache to make room. [20] |
| **External sorting** | Sorting data too big for memory by sorting chunks and merging them. [27] |
| **Fast and slow pointers** | Two pointers moving at different speeds (usually 2 steps and 1 step) through a list. [16] |
| **Fast (binary) exponentiation** | Computing xⁿ by squaring, in O(log n) multiplications. [22] |
| **Feasibility check** | A function that answers "does this candidate value work?" [25] |
| **FIFO** | First in, first out. [19] |
| **Fixed-size window** | A window of exactly k items; one item joins and one leaves at each step. [8] |
| **Floyd's cycle detection** | The tortoise-and-hare method: if fast and slow ever meet, there's a cycle. [16] |
| **Frequency count** | How many times each item appears, usually in a dict or Counter. [14] |
| **frozenset** | An immutable set, usable as a dict key. [13] |
| **Function** | A named block of code that takes inputs (arguments) and returns an output. [1] |
| **Grid / matrix** | Values arranged in rows and columns; grid[r][c] is row r, column c. [10] |
| **Grouping key** | A normalised form shared by everything that belongs together, like sorted letters for anagrams. [14] |
| **Half-open template** | `while lo < hi` with `hi = mid` and `lo = mid + 1`; ends with lo == hi. [25] |
| **Hashable** | A value that can be a dict key or set item because it can't change, such as numbers, strings and tuples. [5] |
| **Hash collision** | Two different inputs with the same hash value. [12] |
| **Hash function** | Turns a key into a number (its hash); the same key always gives the same hash. [13] |
| **Hash randomisation** | Python changes string hashes each run, so attackers can't force collisions. [13] |
| **Hash table** | The structure behind dict and set; finds keys in O(1) on average. [5] |
| **Head** | The first node of a linked list; the list is reached through it. [15] |
| **Heap sort** | Builds a max-heap in the array, then repeatedly moves the maximum to the end. [27] |
| **Hidden test** | A test case the checker runs without showing it to you first, like on coding-interview sites. [1] |
| **Histogram** | A row of bars of different heights. [18] |
| **Immutable** | Can't be changed after it's created; "changing" a string makes a new one. [5, 11] |
| **Inclusion–exclusion** | Adding and subtracting overlapping areas so each is counted once; used by 2-D prefix sums. [9] |
| **Index** | The position of an item, starting at 0. [6] |
| **Infix notation** | The usual way of writing expressions, like `3 + 4`. [17] |
| **In place** | Changing the input directly with only O(1) extra memory. [4] |
| **In-place** | Changing the existing structure instead of building a new one, using O(1) extra memory. [16] |
| **In-place sort** | A sort that rearranges the list itself with O(1) extra memory. [26] |
| **Insertion sort** | Grows a sorted prefix, sliding each new item left into position. [26] |
| **Introsort** | Quicksort that switches to heap sort when recursion gets too deep. [27] |
| **Invariant** | A statement that stays true on every loop pass, such as "if the target exists, it's in nums[lo..hi]". [24] |
| **Inversion** | A pair of positions i < j whose values are out of order (nums[i] > nums[j]). [22] |
| **itertools** | Python's module with fast permutations, combinations and product. [23] |
| **join** | `sep.join(parts)` glues a list of strings together with sep between them, in one pass. [11] |
| **Key function** | A function that gives the value to sort each item by, as in `sorted(items, key=len)`. [28] |
| **KMP (Knuth–Morris–Pratt)** | A search that uses a table of the pattern's prefix-suffixes so it never re-reads the text; O(n + m). [12] |
| **Leap of faith** | Assuming the function already works on smaller inputs while writing it. [21] |
| **LFU (least frequently used)** | Evicts the item used the fewest times. [20] |
| **LIFO** | Last in, first out. [17] |
| **Linear search** | Checking items one by one until the target is found. [4, 24] |
| **Linked list** | A sequence of nodes where each node points to the next one. [15] |
| **Load factor** | Number of entries ÷ number of buckets; higher means more collisions. [13] |
| **Logarithm (log₂ n)** | How many times you can halve n before reaching 1. [3] |
| **Lomuto partition** | A partition scheme that sweeps left to right, swapping smaller items to the front. [27] |
| **Lower bound** | The least work any algorithm for a problem must do; Ω(n log n) for comparison sorts. [28] |
| **Lower bound / upper bound** | The first position with a value ≥ x / > x. [24] |
| **LPS table** | For each prefix of the pattern, the length of its longest proper prefix that is also a suffix. [12] |
| **@lru_cache / @cache** | Python decorators that memoise a function (bounded with LRU eviction / unbounded). [20] |
| **LRU (least recently used)** | Evicts the item that hasn't been used for the longest time. [20] |
| **Master theorem** | A rule for solving recurrences of the form T(n) = a·T(n/b) + O(nᵈ). [22] |
| **Memoisation** | Caching a function's results by its arguments. [20, 21] |
| **Merge** | Combining two sorted lists into one sorted list by repeatedly taking the smaller front item. [7, 16] |
| **Merge sort** | Sort each half recursively, then merge the sorted halves. [22] |
| **Modular arithmetic** | Working with remainders after division by a modulus, to keep numbers small. [22] |
| **Monotonic** | Never changing direction: once the test says yes, it says yes for every larger value. [25] |
| **Monotonic deque** | A deque kept in increasing or decreasing order, used for sliding-window maximums or minimums. [19] |
| **Monotonic rule** | A rule where growing an invalid window can never make it valid again; needed for variable windows. [8] |
| **Monotonic stack** | A stack whose values stay in increasing or decreasing order; new items pop the ones that break the order. [18] |
| **n** | The size of the input, such as the length of a list. [3] |
| **Naive search** | Trying every start position and comparing character by character. [12] |
| **Next greater element** | For each item, the first item to its right that is larger. [18] |
| **Node** | One item of a linked list: a value plus a pointer to the next node (and the previous one, in a doubly linked list). [15] |
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
| **ord / chr** | Convert a character to its code number and back. [11] |
| **OrderedDict** | A dict that remembers order and can move a key to either end in O(1). [20] |
| **Overlapping subproblems** | When the same subproblem is needed many times; a sign to use memoisation instead. [22] |
| **Palindrome** | Text that reads the same forwards and backwards. [7] |
| **Partition** | Rearranging items into groups around a value, such as smaller / equal / bigger. [26] |
| **Pattern** | A known technique that solves a family of problems, such as two pointers or a hash map. [2] |
| **Pattern matching** | Finding where a pattern string occurs inside a text. [12] |
| **Peak element** | An item larger than its neighbours. [24] |
| **perf_counter** | `time.perf_counter()`, a precise clock for timing code. [5] |
| **Permutation** | An ordering of items; n items have n! permutations. [23] |
| **Pivot** | The item a partition splits around. [27] |
| **Pivot index** | An index where the sum to the left equals the sum to the right. [9] |
| **Pointer (reference)** | A variable that refers to an object, such as `node.next`. [15] |
| **Precomputation** | Doing work once up front so that many later questions are cheap. [9] |
| **Prefix sum** | The running total of the first k items; prefix[0] = 0. [9] |
| **Prefix-sum count** | A dict from each prefix sum to how often it has appeared, used to count subarrays with a given sum. [14] |
| **Previous greater element** | For each item, the nearest item to its left that is larger. [18] |
| **Priority queue** | A queue that always serves the smallest (or most urgent) item first. [19] |
| **Producer / consumer** | One part of a program adds work to a queue while another takes it off. [19] |
| **Proper prefix** | A prefix that isn't the whole string. [12] |
| **Pruning** | Skipping a branch as soon as it can't lead to a valid answer. [23] |
| **Pseudocode** | The steps of an algorithm in plain words, before writing real code. [2] |
| **Push / pop / peek** | Add to the top / remove the top / look at the top without removing it. [17] |
| **Query** | A question asked of the data, such as a range sum. [9] |
| **Queue** | A collection where items join at the back and leave from the front: first in, first out. [19] |
| **Quickselect** | Partition, then continue into only the side containing position k, to find the k-th smallest. [27] |
| **Quicksort** | Partition around a pivot, then sort each side recursively. [27] |
| **Rabin-Karp** | A search that compares hashes of windows, updated with a rolling hash. [12] |
| **Radix sort** | Sorts by one digit at a time, least significant first, with a stable sort per digit. [28] |
| **Randomised pivot** | Choosing the pivot at random so no input is reliably bad. [27] |
| **Range sum** | The sum of items from index i to j; prefix[j + 1] − prefix[i]. [9] |
| **Read/write pointers** | One pointer scans every item; the other marks where the next kept item goes. [7] |
| **Recurrence relation** | An equation for an algorithm's cost in terms of its cost on smaller inputs, like T(n) = 2T(n/2) + n. [22] |
| **Recursion** | A function solving a problem by calling itself on smaller versions of it. [21] |
| **Recursion depth** | How many calls are waiting on the stack at once; it decides the stack space. [21] |
| **RecursionError** | Python's error when the call stack goes deeper than its limit (about 1,000 by default). [21] |
| **Recursion tree** | A drawing of every call as a node, with its recursive calls as children. [21] |
| **Recursive case** | The part that breaks the problem down and makes the recursive calls. [21] |
| **Reference** | A pointer to an object; a Python list stores references, not the objects themselves. [6] |
| **Resize (rehash)** | Moving every entry into a bigger table when the load factor gets too high. [13] |
| **Return value** | What a function gives back with `return`; tests check this, not what it prints. [1] |
| **Reverse Polish notation (RPN)** | Writing operators after their operands, like `3 4 +`; no brackets needed. [17] |
| **Rolling hash** | A hash of a sliding window updated in O(1) as it moves. [12] |
| **Rotated sorted array** | A sorted list cut at some point with the two parts swapped. [24] |
| **Rotation** | Shifting every item k places, wrapping around the end. [6] |
| **Run-length encoding** | Replacing runs of a repeated character with the character and its count. [11] |
| **Running best** | A pattern that walks through data once, remembering the best value seen so far. [1] |
| **Running minimum** | The smallest value seen so far while scanning. [6] |
| **Search space** | The range of candidate answers, from the smallest possible to the largest. [25] |
| **Selection sort** | Repeatedly selects the smallest remaining item and swaps it into place. [26] |
| **Separate chaining** | Handling collisions by keeping a small list of entries in each bucket. [13] |
| **Shunting-yard algorithm** | Converts infix expressions to RPN using a stack of operators and precedence rules. [17] |
| **Sliding window** | A contiguous range [left, right] that moves through the data and is updated instead of recomputed. [8] |
| **Sorted** | Arranged in increasing (or decreasing) order; what makes opposite-ends pointers work. [7] |
| **Space complexity** | How the extra memory an algorithm needs grows with the input size. [4] |
| **Spiral order** | Visiting a grid's values clockwise from the outside ring inwards. [10] |
| **Stable** | Keeping equal items in their original order. [16] |
| **Stable sort** | A sort that keeps equal items in their original relative order. [26] |
| **Stack** | A collection where you add and remove only at the top: last in, first out. [17] |
| **Stack frame** | The record of one function call: its local variables and where to return to. [17] |
| **Stock span** | The number of consecutive days, ending today, with a price at most today's. [18] |
| **Subarray** | A contiguous run of items in an array. [8] |
| **Subset** | Any selection of items, including none and all; n items have 2ⁿ subsets. [23] |
| **Substring** | A contiguous run of characters in a string. [8] |
| **Tail** | The last node; its `next` is None. [15] |
| **Tail call** | A recursive call that is the very last thing a function does; Python doesn't optimise these. [21] |
| **Test case** | One input together with the expected output, used to check a function. [1] |
| **Time complexity** | How an algorithm's running time grows with the input size. [3] |
| **Timsort** | Python's sorting algorithm: finds sorted runs and merges them; stable and adaptive. [28] |
| **Trade-off** | Gaining one thing (like speed) by giving up another (like memory). [2] |
| **Transpose** | Swapping rows and columns. [10] |
| **Traversal** | Visiting every node by following `next` from the head. [15] |
| **Two pointers** | Two indexes that move through the data by a rule, replacing a nested loop. [7] |
| **Variable-size window** | A window that grows on the right and shrinks on the left to keep a rule true. [8] |
| **Whitespace** | Spaces, tabs and newlines. [11] |
| **Window state** | What you keep about the window (a sum, counts, a set) so updates are O(1). [8] |
| **Worst case** | The input that makes it do the most work; the usual meaning of "the complexity". [4] |
