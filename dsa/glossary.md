# Data structures and algorithms glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **Algorithm** | A precise, step-by-step recipe for solving a problem. [1] |
| **Aliasing** | Two names (or list slots) referring to the same object, so changing one changes the other. [10] |
| **Amortised cost** | The average cost per operation over a long sequence, when rare operations are expensive and most are cheap. [4] |
| **Anagram** | A word made by rearranging all the letters of another. [11] |
| **Array** | Items stored side by side in one contiguous block of memory, each reachable by its index in O(1). [6] |
| **Average case** | The expected work over typical inputs. [4] |
| **Best case** | The input that makes the algorithm do the least work. [4] |
| **Big-O notation** | Describes how the number of steps (or memory) grows as the input size n grows, ignoring constants. [3] |
| **Bounds check** | Testing 0 <= r < rows and 0 <= c < cols before using a cell. [10] |
| **Brute force** | The simplest correct solution, usually trying every possibility; often slow but a good start. [2] |
| **Bucket** | A slot in a hash table's internal array where entries are stored. [13] |
| **Call stack** | The memory Python uses to remember function calls that haven't finished yet. [4] |
| **Capacity** | The space a list has reserved; it grows by a factor when full. [4] |
| **Clue words** | Phrases in a problem that point to a pattern, like "contiguous subarray" → sliding window. [2] |
| **Collision** | Two different keys landing in the same bucket. [13] |
| **Complement** | The value needed to complete a pair, such as target − x. [14] |
| **Consecutive sequence** | Integers that follow each other without gaps, like 3, 4, 5. [14] |
| **Constraint** | A limit given in the problem, such as the input size or value range; it hints at the Big-O you need. [2] |
| **Contiguous** | Stored in one unbroken block, next to each other. [6] |
| **Counter** | A dict subclass from collections that counts items; missing keys count as 0. [14] |
| **Data structure** | A way of organising data in memory so certain operations are fast, such as a list, dict or tree. [1] |
| **defaultdict** | A dict that creates a default value (like an empty list) for missing keys. [14] |
| **deque** | A double-ended queue from `collections` with O(1) adds and removals at both ends. [5] |
| **Difference array** | Records where range updates start and stop; a prefix sum of it gives the final values. [9] |
| **Direction list** | Offsets like (−1, 0), (1, 0), (0, −1), (0, 1) used to visit neighbours in a loop. [10] |
| **Dominant term** | The fastest-growing part of a step count, the only one Big-O keeps. [3] |
| **Doubling experiment** | Timing code at n, 2n, 4n to see how the time grows. [5] |
| **Dynamic array** | An array that grows automatically by reserving spare room; Python's list. [6] |
| **Edge case** | An unusual input at the boundaries, such as an empty list, one item, negatives or duplicates. [1] |
| **Fixed-size window** | A window of exactly k items; one item joins and one leaves at each step. [8] |
| **Frequency count** | How many times each item appears, usually in a dict or Counter. [14] |
| **frozenset** | An immutable set, usable as a dict key. [13] |
| **Function** | A named block of code that takes inputs (arguments) and returns an output. [1] |
| **Grid / matrix** | Values arranged in rows and columns; grid[r][c] is row r, column c. [10] |
| **Grouping key** | A normalised form shared by everything that belongs together, like sorted letters for anagrams. [14] |
| **Hashable** | A value that can be a dict key or set item because it can't change, such as numbers, strings and tuples. [5] |
| **Hash collision** | Two different inputs with the same hash value. [12] |
| **Hash function** | Turns a key into a number (its hash); the same key always gives the same hash. [13] |
| **Hash randomisation** | Python changes string hashes each run, so attackers can't force collisions. [13] |
| **Hash table** | The structure behind dict and set; finds keys in O(1) on average. [5] |
| **Hidden test** | A test case the checker runs without showing it to you first, like on coding-interview sites. [1] |
| **Immutable** | Can't be changed after it's created; "changing" a string makes a new one. [5, 11] |
| **Inclusion–exclusion** | Adding and subtracting overlapping areas so each is counted once; used by 2-D prefix sums. [9] |
| **Index** | The position of an item, starting at 0. [6] |
| **In place** | Changing the input directly with only O(1) extra memory. [4] |
| **join** | `sep.join(parts)` glues a list of strings together with sep between them, in one pass. [11] |
| **KMP (Knuth–Morris–Pratt)** | A search that uses a table of the pattern's prefix-suffixes so it never re-reads the text; O(n + m). [12] |
| **Linear search** | Checking items one by one until the target is found. [4] |
| **Load factor** | Number of entries ÷ number of buckets; higher means more collisions. [13] |
| **Logarithm (log₂ n)** | How many times you can halve n before reaching 1. [3] |
| **LPS table** | For each prefix of the pattern, the length of its longest proper prefix that is also a suffix. [12] |
| **Merge** | Combining two sorted lists into one sorted list by repeatedly taking the smaller front item. [7] |
| **Monotonic rule** | A rule where growing an invalid window can never make it valid again; needed for variable windows. [8] |
| **n** | The size of the input, such as the length of a list. [3] |
| **Naive search** | Trying every start position and comparing character by character. [12] |
| **O(1), constant time** | The work doesn't depend on n. [3] |
| **O(2ⁿ), exponential time** | Doubles with every extra item, typical of trying every subset. [3] |
| **Off-by-one error** | A loop that runs one step too many or too few, usually from a wrong range bound. [6] |
| **O(log n), logarithmic time** | The work grows by one step each time n doubles, typical when the problem is halved each step. [3] |
| **O(n), linear time** | The work grows in proportion to n, typically one loop. [3] |
| **O(n log n)** | Typical of efficient sorting. [3] |
| **O(n²), quadratic time** | Typical of a loop inside a loop. [3] |
| **Open addressing** | Handling collisions by probing other buckets until a free one is found; Python's dict does this. [13] |
| **Opposite-ends pointers** | One pointer starts at each end and they move towards each other. [7] |
| **ord / chr** | Convert a character to its code number and back. [11] |
| **Palindrome** | Text that reads the same forwards and backwards. [7] |
| **Pattern** | A known technique that solves a family of problems, such as two pointers or a hash map. [2] |
| **Pattern matching** | Finding where a pattern string occurs inside a text. [12] |
| **perf_counter** | `time.perf_counter()`, a precise clock for timing code. [5] |
| **Pivot index** | An index where the sum to the left equals the sum to the right. [9] |
| **Precomputation** | Doing work once up front so that many later questions are cheap. [9] |
| **Prefix sum** | The running total of the first k items; prefix[0] = 0. [9] |
| **Prefix-sum count** | A dict from each prefix sum to how often it has appeared, used to count subarrays with a given sum. [14] |
| **Proper prefix** | A prefix that isn't the whole string. [12] |
| **Pseudocode** | The steps of an algorithm in plain words, before writing real code. [2] |
| **Query** | A question asked of the data, such as a range sum. [9] |
| **Rabin-Karp** | A search that compares hashes of windows, updated with a rolling hash. [12] |
| **Range sum** | The sum of items from index i to j; prefix[j + 1] − prefix[i]. [9] |
| **Read/write pointers** | One pointer scans every item; the other marks where the next kept item goes. [7] |
| **Reference** | A pointer to an object; a Python list stores references, not the objects themselves. [6] |
| **Resize (rehash)** | Moving every entry into a bigger table when the load factor gets too high. [13] |
| **Return value** | What a function gives back with `return`; tests check this, not what it prints. [1] |
| **Rolling hash** | A hash of a sliding window updated in O(1) as it moves. [12] |
| **Rotation** | Shifting every item k places, wrapping around the end. [6] |
| **Run-length encoding** | Replacing runs of a repeated character with the character and its count. [11] |
| **Running best** | A pattern that walks through data once, remembering the best value seen so far. [1] |
| **Running minimum** | The smallest value seen so far while scanning. [6] |
| **Separate chaining** | Handling collisions by keeping a small list of entries in each bucket. [13] |
| **Sliding window** | A contiguous range [left, right] that moves through the data and is updated instead of recomputed. [8] |
| **Sorted** | Arranged in increasing (or decreasing) order; what makes opposite-ends pointers work. [7] |
| **Space complexity** | How the extra memory an algorithm needs grows with the input size. [4] |
| **Spiral order** | Visiting a grid's values clockwise from the outside ring inwards. [10] |
| **Subarray** | A contiguous run of items in an array. [8] |
| **Substring** | A contiguous run of characters in a string. [8] |
| **Test case** | One input together with the expected output, used to check a function. [1] |
| **Time complexity** | How an algorithm's running time grows with the input size. [3] |
| **Trade-off** | Gaining one thing (like speed) by giving up another (like memory). [2] |
| **Transpose** | Swapping rows and columns. [10] |
| **Two pointers** | Two indexes that move through the data by a rule, replacing a nested loop. [7] |
| **Variable-size window** | A window that grows on the right and shrinks on the left to keep a rule true. [8] |
| **Whitespace** | Spaces, tabs and newlines. [11] |
| **Window state** | What you keep about the window (a sum, counts, a set) so updates are O(1). [8] |
| **Worst case** | The input that makes it do the most work; the usual meaning of "the complexity". [4] |
