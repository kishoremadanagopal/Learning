@@ what-is-dsa
topics: data structures vs algorithms, the structures in this course, why the right choice matters, how exercises and the help ladder work
terms:
- **Data structure:** a way of organising data in memory so certain operations are fast, such as a list, dict or tree.
- **Algorithm:** a precise, step-by-step recipe for solving a problem.
- **Function:** a named block of code that takes inputs (arguments) and returns an output.
- **Return value:** what a function gives back with `return`; tests check this, not what it prints.
- **Test case:** one input together with the expected output, used to check a function.
- **Hidden test:** a test case the checker runs without showing it to you first, like on coding-interview sites.
- **Edge case:** an unusual input at the boundaries, such as an empty list, one item, negatives or duplicates.
- **Running best:** a pattern that walks through data once, remembering the best value seen so far.
mistakes:
- Printing the answer instead of returning it. Tests see None.
- Starting a "smallest so far" at 0 instead of the first item, which breaks on lists without 0.
- Testing only the example in the question and forgetting edge cases like an empty list.
glance:
- Data structure | a way to organise data so the operations you need are fast | depends on the structure | O(n) to store n items
- Algorithm | exact steps that turn an input into the right output | measured with Big-O | extra memory it needs
- Smallest number | one pass, remembering the smallest so far | O(n) | O(1)
- Duplicate check (brute force vs set) | compare every pair, or remember seen items in a set | O(n²) vs O(n) | O(1) vs O(n)

@@ problem-solving
topics: the 6-step method, understanding the problem, examples and edge cases, brute force first, spotting the pattern, planning in pseudocode, testing, clue words
terms:
- **Brute force:** the simplest correct solution, usually trying every possibility; often slow but a good start.
- **Pseudocode:** the steps of an algorithm in plain words, before writing real code.
- **Pattern:** a known technique that solves a family of problems, such as two pointers or a hash map.
- **Trade-off:** gaining one thing (like speed) by giving up another (like memory).
- **Constraint:** a limit given in the problem, such as the input size or value range; it hints at the Big-O you need.
- **Clue words:** phrases in a problem that point to a pattern, like "contiguous subarray" → sliding window.
mistakes:
- Typing code before understanding the problem and working an example by hand.
- Skipping the brute force and getting stuck chasing a clever solution.
- Not stating the time and space cost at the end; interviewers expect it.
- Staying silent in an interview. Say your reasoning out loud.
glance:
- 6-step method | understand → examples → brute force → pattern → plan → code and test | (thinking, not running) | —
- Contains duplicate | add to a set; stop when an item is already in it | O(n) | O(n)
- Contains duplicate (low memory) | sort, then compare neighbours | O(n log n) | O(1) extra (in place)
- Second largest | one pass tracking the largest and second largest distinct values | O(n) | O(1)

@@ big-o
topics: Big-O notation, counting steps, dropping constants and lower terms, O(1) O(log n) O(n) O(n log n) O(n²) O(2ⁿ), loops that add vs multiply, halving, hidden loops
terms:
- **Big-O notation:** describes how the number of steps (or memory) grows as the input size n grows, ignoring constants.
- **Time complexity:** how an algorithm's running time grows with the input size.
- **n:** the size of the input, such as the length of a list.
- **O(1), constant time:** the work doesn't depend on n.
- **O(log n), logarithmic time:** the work grows by one step each time n doubles, typical when the problem is halved each step.
- **O(n), linear time:** the work grows in proportion to n, typically one loop.
- **O(n log n):** typical of efficient sorting.
- **O(n²), quadratic time:** typical of a loop inside a loop.
- **O(2ⁿ), exponential time:** doubles with every extra item, typical of trying every subset.
- **Dominant term:** the fastest-growing part of a step count, the only one Big-O keeps.
- **Logarithm (log₂ n):** how many times you can halve n before reaching 1.
mistakes:
- Keeping constants or smaller terms, like writing O(2n) or O(n² + n).
- Calling two loops one after the other O(n²). Only nested loops multiply.
- Missing hidden loops such as `in`, `index`, `min`, slicing or sorting inside a loop.
glance:
- O(1) constant | same work whatever the size: indexing, dict lookup | O(1) | —
- O(log n) logarithmic | halve the problem each step: binary search | O(log n) | —
- O(n) linear | touch each item once: one loop | O(n) | —
- O(n log n) | sort, or split in halves and do linear work per level | O(n log n) | —
- O(n²) quadratic | a loop inside a loop over the same data | O(n²) | —
- O(2ⁿ), O(n!) | try every subset or every ordering | O(2ⁿ), O(n!) | —
- Sum 1..n | formula n(n+1)/2 instead of a loop | O(1) | O(1)

@@ space-and-cases
topics: space complexity, extra vs input memory, in-place algorithms, the call stack, best/average/worst case, amortised analysis, list growth
terms:
- **Space complexity:** how the extra memory an algorithm needs grows with the input size.
- **In place:** changing the input directly with only O(1) extra memory.
- **Best case:** the input that makes the algorithm do the least work.
- **Worst case:** the input that makes it do the most work; the usual meaning of "the complexity".
- **Average case:** the expected work over typical inputs.
- **Amortised cost:** the average cost per operation over a long sequence, when rare operations are expensive and most are cheap.
- **Capacity:** the space a list has reserved; it grows by a factor when full.
- **Linear search:** checking items one by one until the target is found.
- **Call stack:** the memory Python uses to remember function calls that haven't finished yet.
mistakes:
- Forgetting that building a new list, set or dict costs O(n) extra space.
- Assigning `nums = ...` inside a function and expecting the caller's list to change.
- Quoting only the best case. Give the worst case unless asked otherwise.
glance:
- Space complexity | count the extra memory that grows with the input | — | O(1), O(n)…
- Best / average / worst case | analyse the input that is fastest, typical and slowest | e.g. linear search O(1) / O(n) / O(n) | —
- Amortised cost | average over a long run of operations (list append) | amortised O(1) per append | O(n) total
- Reverse in place | swap the ends and move two pointers inwards | O(n) | O(1)
- Linear search | check each item until found | O(n) worst, O(1) best | O(1)

@@ python-costs
topics: cost of list, dict, set and string operations, insert/pop at the front, slicing copies, hashable keys, deque, timing with perf_counter, doubling experiments
terms:
- **Hash table:** the structure behind dict and set; finds keys in O(1) on average.
- **Hashable:** a value that can be a dict key or set item because it can't change, such as numbers, strings and tuples.
- **Immutable:** can't be changed after it's created; "changing" a string makes a new one.
- **deque:** a double-ended queue from `collections` with O(1) adds and removals at both ends.
- **perf_counter:** `time.perf_counter()`, a precise clock for timing code.
- **Doubling experiment:** timing code at n, 2n, 4n to see how the time grows.
mistakes:
- Using `pop(0)` or `insert(0, x)` on a big list in a loop. Use a deque.
- Checking `x in some_list` inside a loop instead of using a set.
- Deleting items from a list one by one in a loop instead of building a filtered list.
- Building a big string with + in a loop instead of collecting parts and joining.
glance:
- list index, append, pop() | direct access at the end | O(1) (append amortised) | —
- list insert(0), pop(0), `in`, remove | shift items or scan | O(n) | —
- dict / set lookup, insert, delete | hash table | O(1) average, O(n) worst | O(n)
- String concatenation in a loop | build a list and `''.join` it once | O(n) with join, O(n²) with += | O(n)
- deque appendleft / popleft | double-ended queue | O(1) | O(n)
- sorted(), list.sort() | Timsort | O(n log n) | O(n)
- Items in both lists | turn one list into a set, then filter the other | O(n + m) | O(n)
