@@ arrays
topics: contiguous memory, why indexing is O(1), dynamic arrays, the cost of inserting and deleting, loop patterns, off-by-one errors, running minimum, rotating with three reversals
terms:
- **Array:** items stored side by side in one contiguous block of memory, each reachable by its index in O(1).
- **Contiguous:** stored in one unbroken block, next to each other.
- **Index:** the position of an item, starting at 0.
- **Dynamic array:** an array that grows automatically by reserving spare room; Python's list.
- **Reference:** a pointer to an object; a Python list stores references, not the objects themselves.
- **Off-by-one error:** a loop that runs one step too many or too few, usually from a wrong range bound.
- **Rotation:** shifting every item k places, wrapping around the end.
- **Running minimum:** the smallest value seen so far while scanning.
mistakes:
- Using `nums[i + 1]` in a loop that runs to `len(nums)`, which reads past the end.
- Forgetting `k %= n` when rotating, so k larger than the length breaks the code.
- Using `max(prices) - min(prices)` when order matters (buy before sell).

@@ two-pointers
topics: opposite-ends pointers, pair sum in a sorted array, palindromes, read/write pointers, removing duplicates and zeros in place, merging sorted lists, why each move is safe
terms:
- **Two pointers:** two indexes that move through the data by a rule, replacing a nested loop.
- **Opposite-ends pointers:** one pointer starts at each end and they move towards each other.
- **Read/write pointers:** one pointer scans every item; the other marks where the next kept item goes.
- **Palindrome:** text that reads the same forwards and backwards.
- **Merge:** combining two sorted lists into one sorted list by repeatedly taking the smaller front item.
- **Sorted:** arranged in increasing (or decreasing) order; what makes opposite-ends pointers work.
mistakes:
- Using opposite-ends pointers on unsorted data.
- Letting the two pointers meet and pairing an item with itself (`while left <= right` instead of `<`).
- Comparing with the previous item instead of the last kept item when removing duplicates.
- Forgetting to add the leftovers after one list runs out while merging.

@@ sliding-window
topics: fixed-size windows, variable windows that grow and shrink, the template, why it's O(n), longest substring without repeats, shortest subarray with a target sum, when windows don't work
terms:
- **Sliding window:** a contiguous range [left, right] that moves through the data and is updated instead of recomputed.
- **Fixed-size window:** a window of exactly k items; one item joins and one leaves at each step.
- **Variable-size window:** a window that grows on the right and shrinks on the left to keep a rule true.
- **Substring:** a contiguous run of characters in a string.
- **Subarray:** a contiguous run of items in an array.
- **Window state:** what you keep about the window (a sum, counts, a set) so updates are O(1).
- **Monotonic rule:** a rule where growing an invalid window can never make it valid again; needed for variable windows.
mistakes:
- Recomputing the whole window at every step, which makes it O(n·k).
- Starting the best value at 0 when all values could be negative.
- Moving the left pointer backwards (the "abba" bug).
- Using a sliding window with negative numbers for "sum at least target"; use prefix sums instead.

@@ prefix-sums
topics: prefix-sum arrays, O(1) range sums, the leading zero, running left sums, pivot index, difference arrays for range updates, 2-D prefix sums
terms:
- **Prefix sum:** the running total of the first k items; prefix[0] = 0.
- **Range sum:** the sum of items from index i to j; prefix[j + 1] − prefix[i].
- **Query:** a question asked of the data, such as a range sum.
- **Precomputation:** doing work once up front so that many later questions are cheap.
- **Pivot index:** an index where the sum to the left equals the sum to the right.
- **Difference array:** records where range updates start and stop; a prefix sum of it gives the final values.
- **Inclusion–exclusion:** adding and subtracting overlapping areas so each is counted once; used by 2-D prefix sums.
mistakes:
- Off-by-one errors from leaving out the leading 0, or using prefix[j] instead of prefix[j + 1].
- Rebuilding the prefix array for every query.
- Comparing the pivot after adding the current number to the left sum.

@@ matrices
topics: grids as lists of lists, rows and columns, the aliasing trap, direction lists and bounds checks, transpose and rotate, zip(*grid), spiral order, searching a sorted matrix
terms:
- **Grid / matrix:** values arranged in rows and columns; grid[r][c] is row r, column c.
- **Aliasing:** two names (or list slots) referring to the same object, so changing one changes the other.
- **Direction list:** offsets like (−1, 0), (1, 0), (0, −1), (0, 1) used to visit neighbours in a loop.
- **Bounds check:** testing 0 <= r < rows and 0 <= c < cols before using a cell.
- **Transpose:** swapping rows and columns.
- **Spiral order:** visiting a grid's values clockwise from the outside ring inwards.
mistakes:
- Creating grids with `[[0] * cols] * rows`, which repeats one row object.
- Mixing up rows and columns (grid[c][r]) or the lengths (len(grid) is the number of rows).
- Code that only works for square grids.
- Forgetting the bounds check when visiting neighbours.

@@ strings
topics: immutability, building strings with join, characters and ord/chr, counting letters, anagrams by sorting or counting, split and join, run-length encoding, reversing words
terms:
- **Immutable:** can't be changed after creation; strings must be rebuilt instead.
- **join:** `sep.join(parts)` glues a list of strings together with sep between them, in one pass.
- **ord / chr:** convert a character to its code number and back.
- **Anagram:** a word made by rearranging all the letters of another.
- **Run-length encoding:** replacing runs of a repeated character with the character and its count.
- **Whitespace:** spaces, tabs and newlines.
mistakes:
- Trying to assign to a character, like `s[0] = "x"`.
- Building a big string with + in a loop instead of collecting parts and joining.
- Using `split(" ")`, which keeps empty strings between double spaces; `split()` handles any whitespace.
- Forgetting to output the last run when encoding runs.

@@ string-matching
topics: substring search, naive O(n·m) matching, KMP and the LPS failure table, Rabin-Karp and rolling hashes, collisions, choosing a method, other algorithms
terms:
- **Pattern matching:** finding where a pattern string occurs inside a text.
- **Naive search:** trying every start position and comparing character by character.
- **KMP (Knuth–Morris–Pratt):** a search that uses a table of the pattern's prefix-suffixes so it never re-reads the text; O(n + m).
- **LPS table:** for each prefix of the pattern, the length of its longest proper prefix that is also a suffix.
- **Proper prefix:** a prefix that isn't the whole string.
- **Rabin-Karp:** a search that compares hashes of windows, updated with a rolling hash.
- **Rolling hash:** a hash of a sliding window updated in O(1) as it moves.
- **Hash collision:** two different inputs with the same hash value.
mistakes:
- Skipping overlapping matches by jumping ahead by the pattern length after a hit.
- Trusting a Rabin-Karp hash match without comparing the strings.
- Restarting the LPS length at 0 after a mismatch instead of falling back to lps[length − 1].
- Writing your own search in production code when `in` and `find` already do it fast.
