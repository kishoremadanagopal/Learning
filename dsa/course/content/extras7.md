@@ binary-trees
topics: tree vocabulary, full, complete and balanced trees, building a tree from a list, preorder, inorder and postorder, iterative traversals with a stack, level-order traversal with a queue, recursive "ask the children" thinking
terms:
- **Tree:** a hierarchy of nodes with one root, where every other node has exactly one parent.
- **Binary tree:** a tree where each node has at most two children, left and right.
- **Root / leaf:** the top node / a node with no children.
- **Depth / height:** edges from the root down to a node / edges on the longest root-to-leaf path.
- **Complete binary tree:** every level full except possibly the last, which fills from the left.
- **Balanced tree:** a tree whose height stays O(log n).
- **Depth-first search (DFS):** exploring as deep as possible along a branch before backing up.
- **Preorder / inorder / postorder:** visiting the node before, between or after its two subtrees.
- **Breadth-first search (BFS):** visiting level by level, using a queue.
mistakes:
- Forgetting the `None` base case, so the code crashes on `None.left`.
- Using `list.pop(0)` as the BFS queue instead of `deque.popleft()`.
- Not fixing `len(queue)` before the inner loop, which mixes levels together.
- Recursing on very deep (chain-like) trees past Python's recursion limit; use an explicit stack.

glance:
- Preorder / inorder / postorder (recursive) | visit node before / between / after the subtrees | O(n) | O(h)
- Iterative DFS | explicit stack; push right before left for preorder | O(n) | O(h)
- Level order (BFS) | queue; pop len(queue) nodes per level | O(n) | O(w), the widest level
- Max depth | 1 + max(depth(left), depth(right)) | O(n) | O(h)
- Count / sum of nodes | 1 + count(left) + count(right) | O(n) | O(h)
- Build from a level-order list | queue of nodes waiting for children | O(n) | O(n)

@@ tree-problems
topics: returning information from subtrees, diameter, checking balance, root-to-leaf path sums, inverting and checking symmetry, lowest common ancestor, serialising and deserialising, rebuilding a tree from preorder and inorder
terms:
- **Diameter:** the number of edges on the longest path between any two nodes.
- **Height-balanced:** at every node, the left and right subtree heights differ by at most 1.
- **Lowest common ancestor (LCA):** the deepest node that has both given nodes in its subtree.
- **Mirror (invert):** swapping every node's left and right children.
- **Serialise / deserialise:** turning a tree into a string / rebuilding the tree from it.
- **Sentinel:** a special value (like −1 or `#`) that signals "empty" or "invalid".
mistakes:
- Only checking the root for the diameter, when the longest path may lie inside a subtree.
- Recomputing heights at every node, which makes balance or diameter O(n²).
- Comparing node values instead of node identity in LCA when values can repeat.
- Saving `path` instead of `path[:]` when collecting root-to-leaf paths.

glance:
- Diameter | height helper; best = max(best, left + right) | O(n) | O(h)
- Is balanced | height helper returning −1 for "unbalanced" | O(n) | O(h)
- Root-to-leaf paths with a sum | DFS passing the remaining sum down; backtrack the path | O(n) per path copy, O(n²) worst | O(h)
- Invert a tree | swap children recursively | O(n) | O(h)
- Is symmetric | compare left.left with right.right and left.right with right.left | O(n) | O(h)
- Lowest common ancestor | return p/q/None from each side; both non-None → this node | O(n) | O(h)
- Serialise / deserialise | preorder with "#" for empty children | O(n) | O(n)
- Build from preorder + inorder | next preorder value is the root; dict of inorder positions splits | O(n) | O(n)

@@ bst
topics: the BST ordering rule, search and insert, minimum and maximum, floor and ceiling, k-th smallest, deleting a node, validating with bounds, LCA in a BST, degenerate trees, rotations, AVL and red-black trees, B-trees, sorted collections in Python
terms:
- **Binary search tree (BST):** a binary tree where every left subtree holds smaller values and every right subtree bigger ones.
- **Inorder successor:** the next value in sorted order; for a node with a right subtree, the leftmost node of that subtree.
- **Floor / ceiling:** the largest value ≤ x / the smallest value ≥ x.
- **Degenerate tree:** a tree where every node has one child, so it behaves like a linked list.
- **Self-balancing BST:** a BST that restructures itself to keep its height O(log n).
- **Rotation:** an O(1) restructuring that lifts a child above its parent while keeping the sorted order.
- **AVL tree:** a self-balancing BST where sibling subtree heights differ by at most 1.
- **Red-black tree:** a self-balancing BST using node colours; used by many standard libraries.
- **B-tree:** a balanced search tree with many keys per node, used by databases and file systems.
mistakes:
- Validating a BST by comparing each node only with its children.
- Forgetting to assign the result of a recursive delete or insert back to `node.left` / `node.right`.
- Assuming BST operations are always O(log n): a plain BST built from sorted data is O(n).
- Allowing duplicates without deciding which side they go to.

glance:
- Search / insert | go left if smaller, right if bigger | O(h): O(log n) balanced, O(n) worst | O(1) iterative
- Min / max | go left / right until you can't | O(h) | O(1)
- Floor / ceiling | search, remembering the best candidate | O(h) | O(1)
- K-th smallest | iterative inorder, stop after k | O(h + k) | O(h)
- Delete | 0 or 1 child: return the other child; 2 children: copy the successor, delete it | O(h) | O(h)
- Validate | pass (low, high) bounds down | O(n) | O(h)
- LCA in a BST | go left while both are smaller, right while both are bigger | O(h) | O(1)
- AVL / red-black insert and delete | BST operation + rotations | O(log n) | O(log n)
- Sorted list + bisect | binary search; insort shifts items | O(log n) search, O(n) insert | O(n)

@@ heaps
topics: priority queues, the heap property, storing a complete tree in a list, sift up and sift down, heapify in O(n), heapq and its max-heap functions in Python 3.14, priorities and tie-breakers, top k, merging k sorted lists, the two-heap running median, lazy deletion
terms:
- **Priority queue:** a collection that always hands back the highest-priority item next.
- **Binary heap:** a complete binary tree where every parent is ≤ its children (min-heap) or ≥ them (max-heap).
- **Sift up / sift down:** swapping an item with its parent / smaller child until the heap property holds again.
- **Heapify:** turning a whole list into a heap in O(n), by sifting down from the last parent to the root.
- **heapq:** Python's module that treats an ordinary list as a min-heap.
- **Tie-breaker:** an extra value, such as a counter, that decides between equal priorities.
- **Top k:** finding the k largest or smallest items, typically with a heap of size k.
- **Lazy deletion:** marking items as removed and skipping them when they reach the top.
mistakes:
- Expecting a heap list to be sorted; only `heap[0]` is guaranteed to be the minimum.
- Forgetting that heapq is a min-heap (negate keys, or use the 3.14 `_max` functions, for a max-heap).
- Pushing `(priority, item)` where equal priorities make Python compare uncomparable items.
- Using a max-heap of all n items for "k largest" instead of a min-heap of size k.

glance:
- Push / pop | append + sift up / move last to root + sift down | O(log n) | O(1)
- Peek at the minimum | heap[0] | O(1) | O(1)
- Heapify a list | sift down from the last parent to the root | O(n) | O(1)
- Heap sort | heapify, then pop n times | O(n log n) | O(1) in place
- K largest / k closest | min-heap (or negated max-heap) of size k | O(n log k) | O(k)
- K-th largest | root of a size-k min-heap | O(n log k) | O(k)
- Merge k sorted lists | heap of (value, list, index) | O(N log k) | O(k)
- Running median | max-heap of the lower half + min-heap of the upper half | O(log n) add, O(1) median | O(n)

@@ tries
topics: prefix trees, nodes with children and an end flag, insert, search and starts_with, the dict-of-dicts trie, autocomplete, counting and deleting words, wildcard search, longest-prefix matching, radix trees, when to use a set or a sorted list instead
terms:
- **Trie (prefix tree):** a tree that stores strings one character per level, sharing common prefixes.
- **End-of-word flag:** a marker on the node where a complete word ends.
- **Prefix:** the beginning part of a string; "ca" is a prefix of "cat".
- **Autocomplete:** suggesting stored words that start with what has been typed.
- **Wildcard:** a pattern character, such as `.`, that matches any single character.
- **Longest prefix match:** finding the longest stored word that is a prefix of a given text, as routers do.
- **Radix tree:** a compressed trie whose edges hold whole strings instead of single characters.
mistakes:
- Forgetting the end-of-word flag, so every prefix of a word counts as a word.
- Rebuilding the trie for every query instead of once.
- Collecting every word under a prefix and sorting, when an ordered DFS can stop early.
- Using a trie where a set (exact lookups) or a sorted list with bisect (simple prefix ranges) would do.

glance:
- Insert / search / starts_with | walk one character per level, creating nodes on insert | O(L) | O(L) per new word
- Autocomplete (first k words) | walk the prefix, then DFS in alphabetical order, stop at k | O(L + nodes visited) | O(L)
- Count words with a prefix | store a pass-through count in each node | O(L) | O(1) extra per node
- Delete a word | decrement counts along the path; prune empty branches | O(L) | O(1)
- Wildcard search | at ".", try every child | O(26^dots × L) worst | O(L)
- Longest prefix match | walk the text, remember the last word end | O(L) | O(1)
- Prefix range with a sorted list | bisect_left(words, prefix), read forwards | O(L log n) | O(n)

@@ segment-fenwick
topics: range queries with updates, square-root decomposition, Fenwick trees and the lowest set bit, segment trees for sums, minimums and gcds, lazy propagation for range updates, sparse tables for static minimums, coordinate compression, counting smaller elements
terms:
- **Range query:** a question about a contiguous part of a list, such as its sum or minimum.
- **Point update:** changing a single item of the list.
- **Fenwick tree (binary indexed tree):** an array where position i stores the sum of a block ending at i, of length i & -i.
- **Lowest set bit:** the rightmost 1 bit of a number; `i & -i` in Python.
- **Segment tree:** a binary tree where each node stores the combined value of a range of the list.
- **Lazy propagation:** storing a pending range update at a node and passing it down only when needed.
- **Sparse table:** precomputed minimums of every power-of-two block, for O(1) static range-minimum queries.
- **Coordinate compression:** replacing values by their rank in sorted order, so they index a small array.
mistakes:
- Mixing 0-based list indexes with the Fenwick tree's 1-based positions.
- Treating "set nums[i] = val" as "add val" in a Fenwick tree (add the difference instead).
- Trying to answer range minimums with a Fenwick tree (minimum has no inverse).
- Sizing a recursive segment tree at 2n instead of 4n.

glance:
- Fenwick: point add / prefix sum | climb with i += i & −i / descend with i −= i & −i | O(log n) each | O(n)
- Fenwick: range sum | prefix(r + 1) − prefix(l) | O(log n) | O(n)
- Segment tree (iterative, 2n list) | leaves at n..2n−1; combine pairs going up | O(log n) update and query | O(n)
- Segment tree with lazy propagation | stop at covering nodes, store a pending update | O(log n) range update and query | O(n)
- Sparse table (static min / max) | two overlapping power-of-two blocks | O(n log n) build, O(1) query | O(n log n)
- Square-root decomposition | blocks of √n items with stored totals | O(1) update, O(√n) query | O(n)
- Count smaller to the right / inversions | Fenwick tree over ranks, scanning right to left | O(n log n) | O(n)
