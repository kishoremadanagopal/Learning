@@ linked-lists
topics: nodes and pointers, traversal, insert and delete, the dummy (sentinel) node, tail pointers, doubly and circular linked lists, linked list vs array
terms:
- **Linked list:** a sequence of nodes where each node points to the next one.
- **Node:** one item of a linked list: a value plus a pointer to the next node (and the previous one, in a doubly linked list).
- **Pointer (reference):** a variable that refers to an object, such as `node.next`.
- **Head:** the first node of a linked list; the list is reached through it.
- **Tail:** the last node; its `next` is None.
- **Traversal:** visiting every node by following `next` from the head.
- **Dummy (sentinel) node:** a placeholder node before the head (or after the tail) that removes special cases.
- **Doubly linked list:** nodes point both forwards (`next`) and backwards (`prev`).
- **Circular linked list:** the last node points back to the first.
mistakes:
- Losing the rest of the list by overwriting `node.next` before saving it.
- Forgetting the empty list (head is None) and one-node lists.
- Writing `while node.next:` when you need `while node:`, which skips the last node (or crashes on an empty list).
- Looping forever over a circular list with `while node:`.

glance:
- Traverse / search | follow next from the head | O(n) | O(1)
- Access item i | walk i steps | O(n) | O(1)
- Insert / delete at the front | new node points to the old head | O(1) | O(1)
- Append with a tail pointer | link after the tail, move the tail | O(1) | O(1)
- Delete by value | dummy + prev pointer; prev.next = prev.next.next | O(n) | O(1)
- Delete a node you hold (doubly linked) | reconnect its prev and next | O(1) | O(1)
- Insert into a sorted list | walk to the last smaller node, splice | O(n) | O(1)
- Josephus circle | circular list, unlink every k-th node | O(n·k) | O(n)

@@ linked-list-patterns
topics: reversing in place, recursion vs iteration, fast and slow pointers, the middle node, Floyd's cycle detection and cycle start, merging sorted lists, a gap of k, palindrome lists
terms:
- **In-place:** changing the existing structure instead of building a new one, using O(1) extra memory.
- **Fast and slow pointers:** two pointers moving at different speeds (usually 2 steps and 1 step) through a list.
- **Floyd's cycle detection:** the tortoise-and-hare method: if fast and slow ever meet, there's a cycle.
- **Cycle:** a loop in the links, so following `next` never reaches None.
- **Merge:** combining two sorted sequences into one sorted sequence.
- **Stable:** keeping equal items in their original order.
mistakes:
- Comparing node values (`==`) instead of node identity (`is`) when detecting cycles.
- Reversing recursively on long lists in Python, which hits the recursion limit.
- Forgetting to attach the leftover nodes after a merge loop.
- Checking `fast.next.next` without first checking `fast` and `fast.next`.

glance:
- Reverse a list | prev / cur / next, turn each arrow around | O(n) | O(1) (recursive: O(n) stack)
- Middle node | slow 1 step, fast 2 steps | O(n) | O(1)
- Detect a cycle (Floyd) | fast and slow meet if there's a loop | O(n) | O(1)
- Find the cycle's start | after meeting, restart one pointer at the head; step both by 1 | O(n) | O(1)
- Merge two sorted lists | dummy + tail; attach the smaller front | O(n + m) | O(1)
- Remove k-th from the end | lead k steps ahead, then move both | O(n) | O(1)
- Palindrome list | middle, reverse the second half, compare | O(n) | O(1)

@@ stacks
topics: last in first out, lists as stacks, matching brackets, a min stack, reverse Polish notation, shunting-yard, the call stack and recursion
terms:
- **Stack:** a collection where you add and remove only at the top: last in, first out.
- **LIFO:** last in, first out.
- **Push / pop / peek:** add to the top / remove the top / look at the top without removing it.
- **Reverse Polish notation (RPN):** writing operators after their operands, like `3 4 +`; no brackets needed.
- **Infix notation:** the usual way of writing expressions, like `3 + 4`.
- **Shunting-yard algorithm:** converts infix expressions to RPN using a stack of operators and precedence rules.
- **Call stack:** the stack of active function calls; each call pushes a frame, each return pops it.
- **Stack frame:** the record of one function call: its local variables and where to return to.
mistakes:
- Using `pop(0)` or `insert(0, x)`, which make a list-based stack O(n).
- Popping from an empty stack without checking first (IndexError).
- Popping operands in the wrong order for `-` and `/`.
- Checking bracket balance by counting, which ignores order and type.

glance:
- Push / pop / peek | list.append / list.pop() / list[-1] | O(1) | O(n) for n items
- Valid brackets | push openers; a closer must match the popped top | O(n) | O(n)
- Min stack | store (value, min so far) pairs | O(1) per operation | O(n)
- Evaluate RPN | push numbers; on an operator pop b, pop a, push a op b | O(n) | O(n)
- Infix → RPN (shunting-yard) | operator stack ordered by precedence | O(n) | O(n)
- Recursion → loop | replace the call stack with your own list | same as the recursion | O(depth)

@@ monotonic-stack
topics: monotonic stacks, next greater and next smaller element, previous greater (stock span), largest rectangle in a histogram, trapping rain water, amortised O(n)
terms:
- **Monotonic stack:** a stack whose values stay in increasing or decreasing order; new items pop the ones that break the order.
- **Next greater element:** for each item, the first item to its right that is larger.
- **Previous greater element:** for each item, the nearest item to its left that is larger.
- **Stock span:** the number of consecutive days, ending today, with a price at most today's.
- **Histogram:** a row of bars of different heights.
- **Amortised analysis:** bounding the total cost of many operations, so an occasional expensive step averages out.
mistakes:
- Pushing values instead of indexes when you need distances or widths.
- Using `<=` where `<` is needed (or the reverse), which mishandles equal values.
- Forgetting to flush the stack at the end (a sentinel 0 bar), so some items never get an answer.
- Thinking the nested while loop makes it O(n²); count total pushes and pops instead.

glance:
- Next greater element | decreasing stack of indexes; a bigger value pops and answers them | O(n) | O(n)
- Daily temperatures | next greater, answer = index distance | O(n) | O(n)
- Stock span (previous greater) | pop smaller or equal, distance to the new top | O(n) | O(n)
- Largest rectangle in a histogram | increasing stack; a popped bar's width runs from the bar below it to i | O(n) | O(n)
- Trapping rain water | two pointers, move the lower wall | O(n) | O(1)

@@ queues-deques
topics: first in first out, collections.deque, why not list.pop(0), bounded deques, circular buffers, a queue from two stacks, amortised O(1), the monotonic deque, other kinds of queue
terms:
- **Queue:** a collection where items join at the back and leave from the front: first in, first out.
- **FIFO:** first in, first out.
- **Enqueue / dequeue:** add at the back / remove from the front.
- **Deque:** a double-ended queue: O(1) adds and removes at both ends (`collections.deque`).
- **Circular (ring) buffer:** a fixed-size array used as a queue, with indexes that wrap around using `%`.
- **Monotonic deque:** a deque kept in increasing or decreasing order, used for sliding-window maximums or minimums.
- **Priority queue:** a queue that always serves the smallest (or most urgent) item first.
- **Producer / consumer:** one part of a program adds work to a queue while another takes it off.
mistakes:
- Using `list.pop(0)` as dequeue: O(n) per call.
- Indexing into the middle of a deque in a loop: `q[i]` is O(n) for a deque.
- Pouring a two-stack queue back and forth on every operation.
- Storing values instead of indexes in a sliding-window deque, so expired items can't be detected.

glance:
- Enqueue / dequeue | deque.append / deque.popleft | O(1) | O(n)
- Keep only the last k items | deque(maxlen=k) | O(1) per append | O(k)
- Circular buffer | array + head + size, indexes wrap with % | O(1) per operation | O(capacity)
- Queue from two stacks | push to inbox; pour into outbox only when it's empty | amortised O(1) | O(n)
- Sliding window maximum | deque of indexes with decreasing values | O(n) | O(k)

@@ lru-cache
topics: caches and eviction, LRU design with a hash map and a doubly linked list, OrderedDict, functools.lru_cache and cache, LFU caches, how to approach design questions
terms:
- **Cache:** fast storage that keeps recent or frequent results so they don't have to be recomputed or fetched again.
- **Eviction:** removing an item from a full cache to make room.
- **LRU (least recently used):** evicts the item that hasn't been used for the longest time.
- **LFU (least frequently used):** evicts the item used the fewest times.
- **Cache hit / miss:** the item was in the cache / it wasn't.
- **OrderedDict:** a dict that remembers order and can move a key to either end in O(1).
- **Memoisation:** caching a function's results by its arguments.
- **@lru_cache / @cache:** Python decorators that memoise a function (bounded with LRU eviction / unbounded).
mistakes:
- Forgetting to remove the evicted key from the dict.
- Not treating `get` as a use, so recently read items get evicted.
- Creating a second node when updating an existing key instead of moving the existing one.
- Using @lru_cache on functions with list arguments (they aren't hashable).

glance:
- LRU get / put | dict of key → node + doubly linked list in recency order | O(1) | O(capacity)
- LRU with OrderedDict | move_to_end and popitem(last=False) | O(1) | O(capacity)
- Memoise a function | @lru_cache(maxsize) or @cache | O(1) per repeated call | O(distinct arguments)
- LFU get / put | count per key + OrderedDict per count + minimum count | O(1) | O(capacity)
