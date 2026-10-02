@@ binary-search
topics: linear vs binary search, the exact template and its invariant, off-by-one errors, bisect, first and last occurrence, rotated arrays, peaks, sorted matrices
terms:
- **Linear search:** checking items one by one until the target is found.
- **Binary search:** repeatedly halving a sorted range by comparing with its middle item.
- **Invariant:** a statement that stays true on every loop pass, such as "if the target exists, it's in nums[lo..hi]".
- **Off-by-one error:** a bug where a loop or index is one step too far or too short.
- **bisect_left / bisect_right:** the first position where x could be inserted keeping the order (before / after equal items).
- **Lower bound / upper bound:** the first position with a value ≥ x / > x.
- **Rotated sorted array:** a sorted list cut at some point with the two parts swapped.
- **Peak element:** an item larger than its neighbours.
mistakes:
- Using `while lo < hi` with an inclusive `hi`, which skips the last candidate.
- Writing `lo = mid` or `hi = mid` with the inclusive template, which can loop forever.
- Running binary search on unsorted data.
- Stopping at the first match when the question asks for the first or last occurrence.

glance:
- Linear search | check each item | O(n) | O(1)
- Binary search | compare with the middle; keep one half | O(log n) | O(1)
- bisect_left / bisect_right | C-coded binary search for insertion points | O(log n) | O(1)
- Count items in a range of a sorted list | bisect_right(hi) − bisect_left(lo) | O(log n) | O(1)
- First / last occurrence | on a match, record it and keep searching left / right | O(log n) | O(1)
- Search a rotated sorted array | one half is always sorted; check if the target is inside it | O(log n) | O(1)
- Find a peak | move towards the bigger neighbour | O(log n) | O(1)
- Search a sorted matrix (rows continue) | treat it as one list: row k // cols, column k % cols | O(log(r·c)) | O(1)

@@ binary-search-answer
topics: monotonic yes/no tests, searching for the first yes or last yes, rounding mid, integer square root, minimum ship capacity, eating speed, minimum of a rotated array, real-valued binary search
terms:
- **Binary search on the answer:** binary searching over the possible values of the answer, using a yes/no test.
- **Monotonic:** never changing direction: once the test says yes, it says yes for every larger value.
- **Feasibility check:** a function that answers "does this candidate value work?"
- **Search space:** the range of candidate answers, from the smallest possible to the largest.
- **Half-open template:** `while lo < hi` with `hi = mid` and `lo = mid + 1`; ends with lo == hi.
- **Ceiling division:** dividing and rounding up, `(a + b - 1) // b` for positive integers.
mistakes:
- Searching a range that doesn't contain the answer (bounds too tight or too loose).
- Using `mid = (lo + hi) // 2` together with `lo = mid`, which never terminates.
- A feasibility check that isn't actually monotonic.
- Using float square roots for huge integers, which can be off by one.

glance:
- First value that works | while lo < hi: mid; works → hi = mid, else lo = mid + 1 | O(log(range) × check) | O(1)
- Last value that works | mid rounded up; works → lo = mid, else hi = mid − 1 | O(log(range) × check) | O(1)
- Integer square root | last x with x·x ≤ n | O(log n) | O(1)
- Minimum ship capacity | search max(w)..sum(w); greedy day count | O(n log(sum)) | O(1)
- Minimum eating speed | search 1..max(pile); total hours with ceiling division | O(n log(max)) | O(1)
- Minimum of a rotated array | compare nums[mid] with nums[hi] | O(log n) | O(1)
- Real-valued answer | fixed number of halvings (e.g. 100) | O(iterations × check) | O(1)

@@ simple-sorts
topics: in-place and stable sorting, bubble sort with early exit, selection sort, insertion sort and nearly sorted data, comparing the simple sorts, the Dutch national flag partition
terms:
- **In-place sort:** a sort that rearranges the list itself with O(1) extra memory.
- **Stable sort:** a sort that keeps equal items in their original relative order.
- **Bubble sort:** repeatedly swaps neighbouring items that are out of order.
- **Selection sort:** repeatedly selects the smallest remaining item and swaps it into place.
- **Insertion sort:** grows a sorted prefix, sliding each new item left into position.
- **Adaptive sort:** a sort that runs faster on input that is already partly sorted.
- **Partition:** rearranging items into groups around a value, such as smaller / equal / bigger.
- **Dutch national flag:** a one-pass, three-pointer partition into three groups.
mistakes:
- Writing insertion sort without the early stop, losing its O(n) best case.
- Forgetting bubble sort's "no swaps → stop" check.
- Assuming every sort is stable (selection sort and quicksort aren't).
- Advancing `mid` after swapping with `high` in the Dutch flag partition.

glance:
- Bubble sort | swap out-of-order neighbours; stop when a pass makes no swaps | O(n²), best O(n) | O(1)
- Selection sort | swap the minimum of the rest into place | O(n²) always | O(1)
- Insertion sort | shift bigger items right, drop the item in the gap | O(n²), best O(n) | O(1)
- Dutch national flag (sort 0/1/2) | three pointers low / mid / high | O(n) | O(1)

@@ efficient-sorts
topics: merge sort's trade-offs, quicksort with Lomuto partition and random pivots, the quicksort worst case, heap sort, introsort, quickselect, choosing an O(n log n) sort
terms:
- **Quicksort:** partition around a pivot, then sort each side recursively.
- **Pivot:** the item a partition splits around.
- **Lomuto partition:** a partition scheme that sweeps left to right, swapping smaller items to the front.
- **Randomised pivot:** choosing the pivot at random so no input is reliably bad.
- **Heap sort:** builds a max-heap in the array, then repeatedly moves the maximum to the end.
- **Introsort:** quicksort that switches to heap sort when recursion gets too deep.
- **Quickselect:** partition, then continue into only the side containing position k, to find the k-th smallest.
- **External sorting:** sorting data too big for memory by sorting chunks and merging them.
mistakes:
- Always using the first or last item as the pivot, which is O(n²) on sorted input.
- Recursing into both sides in quickselect (that's just quicksort).
- Forgetting that quicksort and heap sort aren't stable.
- Deep recursion in Python: recurse on the smaller side and loop on the larger one.

glance:
- Merge sort | split, sort halves, merge | O(n log n) always | O(n)
- Quicksort | random pivot, partition, recurse both sides | O(n log n) average, O(n²) worst | O(log n)
- Heap sort | build a max-heap, swap the max to the end, sift down | O(n log n) always | O(1)
- Quickselect (k-th smallest) | partition, keep only the side holding k | O(n) average, O(n²) worst | O(1)
- 3-way quicksort (many duplicates) | Dutch-flag partition around the pivot | O(n log n), O(n) if all equal | O(log n)

@@ sorting-in-practice
topics: the n log n lower bound for comparison sorts, counting sort, radix sort, bucket sort, Timsort, sorted and list.sort, key functions and multi-key sorting, stability tricks, cmp_to_key, choosing a sort
terms:
- **Comparison sort:** a sort that learns about the data only by comparing pairs of items.
- **Lower bound:** the least work any algorithm for a problem must do; Ω(n log n) for comparison sorts.
- **Counting sort:** counts how many times each small integer appears, then writes them out in order.
- **Radix sort:** sorts by one digit at a time, least significant first, with a stable sort per digit.
- **Bucket sort:** spreads evenly distributed values into buckets, sorts each bucket, and joins them.
- **Timsort:** Python's sorting algorithm: finds sorted runs and merges them; stable and adaptive.
- **Key function:** a function that gives the value to sort each item by, as in `sorted(items, key=len)`.
- **cmp_to_key:** turns an old-style comparison function into a key function.
mistakes:
- Calling `.sort()` and using its return value (it's None).
- Using counting sort on a huge value range.
- Sorting with `reverse=True` when only one of several keys should be descending.
- Comparing numbers as strings by accident ("10" < "9").

glance:
- Counting sort | count each value, write values in order | O(n + k) | O(n + k)
- Radix sort (LSD) | stable bucket pass per digit, least significant first | O(d · (n + b)) | O(n + b)
- Bucket sort | bucket by value, sort buckets, concatenate | O(n) average, O(n²) worst | O(n)
- sorted() / list.sort() (Timsort) | merge natural runs; insertion sort for short runs | O(n log n), O(n) if nearly sorted | O(n)
- Multi-key sort | key returns a tuple; negate numbers to reverse one key | O(n log n) | O(n)
- Largest number from digits | sort strings with cmp: a + b vs b + a | O(L · n log n) | O(n · L)
- Top k items | heapq.nlargest(k, items) | O(n log k) | O(k)
