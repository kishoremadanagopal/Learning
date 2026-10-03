@@@ part
id: 7
title: Trees and Heaps
level: Intermediate
blurb: Hierarchical data: binary trees and every traversal, the classic tree problems, binary search trees and balancing, heaps and priority queues, tries for prefixes, and segment and Fenwick trees for fast range queries.

@@@ lesson
id: binary-trees
title: Binary trees and traversals
minutes: 24
summary: Tree vocabulary, building a tree from a list, depth-first traversals (preorder, inorder, postorder) recursively and with a stack, and breadth-first level-order traversal with a queue.
---
A **tree** is a hierarchy: one **root** at the top, and every other node has exactly one **parent**. A **binary tree** limits each node to at most two **children**, a left and a right. Trees are everywhere: folders on a disk, the HTML of a web page, an organisation chart, a decision tree in machine learning, and the parse tree a compiler builds from your code.

![A binary tree with root 1. Node 1 has children 2 and 3; node 2 has children 4 and 5; node 3 has a right child 6. Labels show the root, a parent and child, leaves (4, 5, 6), the depth of each level (0, 1, 2) and that the tree's height is 2](figures/binary-tree.svg)

| Term | Meaning |
|---|---|
| **root** | the top node (no parent) |
| **leaf** | a node with no children |
| **depth** of a node | edges from the root down to it (the root has depth 0) |
| **height** of a tree | edges on the longest root-to-leaf path |
| **subtree** | a node together with everything below it |
| **full** binary tree | every node has 0 or 2 children |
| **complete** binary tree | every level full, except possibly the last, which fills from the left (heaps are complete) |
| **balanced** | heights of left and right subtrees differ by at most 1 everywhere: height O(log n) |

A tree with n nodes has n − 1 edges. A balanced tree's height is about log₂ n; a "degenerate" tree where each node has one child is just a linked list, with height n − 1.

### Nodes, and building a tree from a list

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build(values):
    """Build a tree from level-order values, with None for missing children (LeetCode style)."""
    if not values or values[0] is None:
        return None
    from collections import deque
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

root = build([1, 2, 3, 4, 5, None, 6])
print(root.val, root.left.val, root.right.val, root.left.left.val, root.right.right.val)
```

### Depth-first traversals

**Depth-first search (DFS)** goes as deep as possible down one branch before backing up. The three orders differ only in **when** you visit the node relative to its subtrees:

| Order | Visit | For the tree above | Typical use |
|---|---|---|---|
| **Preorder** | node, left, right | 1 2 4 5 3 6 | copying or serialising a tree |
| **Inorder** | left, node, right | 4 2 5 1 3 6 | sorted order in a binary search tree |
| **Postorder** | left, right, node | 4 5 2 6 3 1 | deleting a tree, computing sizes or heights (children first) |

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, None, TreeNode(6)))

def preorder(node, out):
    if node:
        out.append(node.val)
        preorder(node.left, out)
        preorder(node.right, out)
    return out

def inorder(node, out):
    if node:
        inorder(node.left, out)
        out.append(node.val)
        inorder(node.right, out)
    return out

def postorder(node, out):
    if node:
        postorder(node.left, out)
        postorder(node.right, out)
        out.append(node.val)
    return out

print("pre: ", preorder(root, []))
print("in:  ", inorder(root, []))
print("post:", postorder(root, []))
```

Each visits every node once: **O(n) time**, and **O(h) space** for the recursion, where h is the height (O(log n) balanced, O(n) for a degenerate tree).

### The same traversals with an explicit stack

For very deep trees, Python's recursion limit bites. Any recursion can use your own stack instead:

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, None, TreeNode(6)))

def preorder_iter(root):
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right: stack.append(node.right)   # push right first, so left is popped first
        if node.left: stack.append(node.left)
    return out

def inorder_iter(root):
    out, stack, node = [], [], root
    while stack or node:
        while node:                     # go as far left as possible
            stack.append(node)
            node = node.left
        node = stack.pop()              # the leftmost unvisited node
        out.append(node.val)
        node = node.right               # then its right subtree
    return out

print(preorder_iter(root), inorder_iter(root))
```

### Breadth-first (level-order) traversal

**Breadth-first search (BFS)** visits the tree level by level, using a **queue**: take a node from the front, add its children to the back. Processing `len(queue)` nodes at a time separates the levels.

```python
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, None, TreeNode(6)))

def level_order(root):
    if not root:
        return []
    levels, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):        # exactly the nodes of this level
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        levels.append(level)
    return levels

print(level_order(root))
```

O(n) time, O(w) space where w is the widest level (up to about n/2 for the last level of a full tree). BFS finds things **closest to the root first**, such as the minimum depth or the first node with some property; DFS goes deep first and uses less memory on wide, shallow trees.

### Solving tree problems recursively

Most tree questions are answered by the same move: **ask each subtree, then combine**. The height of a tree is 1 + the larger height of its two subtrees; the number of nodes is 1 + left count + right count. That's postorder thinking: children first.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, None, TreeNode(6)))

def count(node):
    return 0 if node is None else 1 + count(node.left) + count(node.right)

def total(node):
    return 0 if node is None else node.val + total(node.left) + total(node.right)

def leaves(node):
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    return leaves(node.left) + leaves(node.right)

print(count(root), total(root), leaves(root))
```

:::exercise Maximum depth
Write `max_depth(root)` returning the number of nodes on the longest path from the root down to a leaf (an empty tree has depth 0, a single node has depth 1). `TreeNode` and `build` are in the starter.
```python starter
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def max_depth(root):
    pass

print(max_depth(build([3, 9, 20, None, None, 15, 7])))   # 3
```
```python check
fn = need("max_depth")
test(lambda v: fn(build(v)), show="max_depth(build({0}))", cases=[
    ([3, 9, 20, None, None, 15, 7], 3, "the example"),
    ([1, None, 2], 2, "only a right child"),
    ([], 0, "an empty tree"),
    ([1], 1, "a single node"),
    ([1, 2, None, 3, None, 4, None, 5], 5, "a long left chain"),
    ([1, 2, 3, 4, 5, 6, 7], 3, "a perfect tree"),
])
```
```python solution
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def max_depth(root):
    if root is None:
        return 0                                     # an empty tree has depth 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

print(max_depth(build([3, 9, 20, None, None, 15, 7])))
```
hint: If you knew the depths of the left and right subtrees, how would you get the depth of the whole tree?
hint: It's 1 (for the root) plus the bigger of the two subtree depths. An empty tree (None) has depth 0: that's the base case.
hint: `if root is None: return 0`, then `return 1 + max(max_depth(root.left), max_depth(root.right))`.
approach:
1. **Understand:** count nodes (not edges) on the longest root-to-leaf path; None → 0.
2. **Examples:** [3, 9, 20, None, None, 15, 7] → 3 (3 → 20 → 15); [1] → 1.
3. **Brute force:** list every root-to-leaf path and take the longest: works, but more code and memory.
4. **Pattern:** **ask both subtrees, combine** (postorder recursion).
5. **Plan:** base case None → 0; otherwise 1 + max of the two recursive answers.
6. **Code and test:** empty tree, single node, a one-sided chain.
walkthrough:
**Line by line**

- The base case makes `None` children count as depth 0, so leaves get 1 + max(0, 0) = 1 with no special case.
- Leap of faith: `max_depth(root.left)` is the depth of the left subtree; the same for the right.
- The root adds one more level on top of the deeper subtree.

**Trace** on [3, 9, 20, None, None, 15, 7]:

| call | left | right | returns |
|---|---|---|---|
| 9 | 0 | 0 | 1 |
| 15, 7 | 0 | 0 | 1 each |
| 20 | 1 | 1 | 2 |
| 3 | 1 (from 9) | 2 (from 20) | **3** |

**Complexity:** O(n) time, O(h) recursion space.

**Common wrong approach:** returning `max(...)` without the `1 +`, so every tree reports depth 0.
:::

:::exercise Level order traversal
Write `level_order(root)` returning the values level by level, as a list of lists from the top level down (left to right within a level). An empty tree gives `[]`.
```python starter
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def level_order(root):
    pass

print(level_order(build([3, 9, 20, None, None, 15, 7])))   # [[3], [9, 20], [15, 7]]
```
```python check
fn = need("level_order")
test(lambda v: fn(build(v)), show="level_order(build({0}))", cases=[
    ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]], "the example"),
    ([1], [[1]], "a single node"),
    ([], [], "an empty tree"),
    ([1, 2, 3, 4, 5, 6, 7], [[1], [2, 3], [4, 5, 6, 7]], "a perfect tree"),
    ([1, 2, None, 3, None, 4], [[1], [2], [3], [4]], "a left chain"),
    ([1, None, 2, None, 3], [[1], [2], [3]], "a right chain"),
])
```
```python solution
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def level_order(root):
    if root is None:
        return []
    levels, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):        # the queue holds exactly one level right now
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels

print(level_order(build([3, 9, 20, None, None, 15, 7])))
```
hint: Which data structure gives you nodes in the order "all of level 0, then all of level 1, …"?
hint: A queue (`collections.deque`). Take a node from the front and put its children at the back.
hint: To group by level, at the start of each round note `len(queue)`: exactly that many nodes belong to the current level. Pop that many, collecting their values and pushing their children.
approach:
1. **Understand:** one list per level, top to bottom, left to right; empty tree → [].
2. **Examples:** [3, 9, 20, None, None, 15, 7] → [[3], [9, 20], [15, 7]].
3. **Brute force:** DFS with a depth parameter, appending to `levels[depth]`: also O(n) and a fine alternative.
4. **Pattern:** **BFS with a queue**, processing one level per round.
5. **Plan:** queue starts with the root; each round pops `len(queue)` nodes into a list and enqueues their children.
6. **Code and test:** empty, one node, chains on each side.
walkthrough:
**Line by line**

- The queue always contains nodes in level order, because children are added at the back after all nodes of the current level.
- At the start of a round, the queue holds exactly the next level, so `range(len(queue))` pops precisely that level even while children are being appended behind it.
- `level` collects the values; `levels.append(level)` stores the finished level.

**Trace** on [3, 9, 20, None, None, 15, 7]:

| round | queue at start | level | queue at end |
|---|---|---|---|
| 1 | 3 | [3] | 9, 20 |
| 2 | 9, 20 | [9, 20] | 15, 7 |
| 3 | 15, 7 | [15, 7] | — |

**Complexity:** O(n) time, O(w) space for the widest level.

**Common wrong approach:** using a list with `pop(0)` as the queue (O(n) per pop), or not fixing the level size before the inner loop, which mixes levels together.
:::

:::quiz
? Which traversal of a tree visits the node between its left and right subtrees?
+ Inorder
- Preorder
- Postorder
= In, as in "in between": left, node, right.
? What data structure does breadth-first (level-order) traversal use?
+ A queue
- A stack
- A hash set
= First in, first out keeps the nodes in level order. DFS uses a stack (or recursion).
? What is the recursion space of a DFS traversal?
+ O(h), the height of the tree
- O(1)
- O(n²)
= One frame per level on the current path: O(log n) when balanced, O(n) for a chain.
? A binary tree where every level is full except the last, which fills from the left, is called:
+ Complete
- Full
- Degenerate
= Heaps are complete binary trees, which is why they fit neatly in an array.
:::

@@@ lesson
id: tree-problems
title: Classic tree problems
minutes: 24
summary: Diameter, balance, path sums, inverting and mirroring, lowest common ancestor, serialising a tree, and rebuilding a tree from its traversals, each with the "return information from children" pattern.
---
Most tree problems follow one recursive shape: a helper that returns some **information about a subtree** (its height, its sum, whether it's balanced), and the parent **combines** its children's information. Sometimes the helper also updates a best-so-far answer on the side.

### Diameter: the longest path between any two nodes

The longest path might not pass through the root. For every node, the longest path **through** it is (height of left subtree) + (height of right subtree), counted in edges. One postorder pass computes heights and tracks the best sum.

![A tree whose longest path is 6 → 4 → 2 → 5 → 7, the diameter of 4 edges. It turns at node 2, the root's left child, and doesn't pass through the root 1, where the longest path has only 3 edges](figures/tree-diameter.svg)

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def diameter(root):
    best = 0
    def height(node):                    # returns the height in nodes; updates best on the side
        nonlocal best
        if node is None:
            return 0
        left, right = height(node.left), height(node.right)
        best = max(best, left + right)   # edges on the longest path through this node
        return 1 + max(left, right)
    height(root)
    return best

root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
print(diameter(root))      # 4 -> 2 -> 1 -> 3: 3 edges
```

### Is it balanced?

Balanced means every node's subtrees differ in height by at most 1. Checking heights at every node separately is O(n²); returning −1 as a "not balanced" signal keeps it to one O(n) pass.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def is_balanced(root):
    def height(node):                    # -1 means "unbalanced somewhere below"
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)
    return height(root) != -1

balanced = TreeNode(1, TreeNode(2, TreeNode(4)), TreeNode(3))
chain = TreeNode(1, TreeNode(2, TreeNode(3)))
print(is_balanced(balanced), is_balanced(chain))
```

### Root-to-leaf path sums: passing information down

Some problems pass information **down** instead (preorder style): the sum so far on the way to each leaf.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def paths_with_sum(root, target):
    found = []
    def walk(node, path, remaining):
        if node is None:
            return
        path.append(node.val)
        remaining -= node.val
        if node.left is None and node.right is None and remaining == 0:
            found.append(path[:])
        walk(node.left, path, remaining)
        walk(node.right, path, remaining)
        path.pop()                       # backtrack
    walk(root, [], target)
    return found

root = TreeNode(5, TreeNode(4, TreeNode(11, TreeNode(7), TreeNode(2))), TreeNode(8, TreeNode(13), TreeNode(4, TreeNode(5), TreeNode(1))))
print(paths_with_sum(root, 22))
```

### Invert (mirror) a tree, and check symmetry

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def invert(node):
    if node:
        node.left, node.right = invert(node.right), invert(node.left)
    return node

def is_mirror(a, b):
    if a is None or b is None:
        return a is b                          # both empty is a match; one empty is not
    return a.val == b.val and is_mirror(a.left, b.right) and is_mirror(a.right, b.left)

def is_symmetric(root):
    return root is None or is_mirror(root.left, root.right)

def preorder(node):
    return [] if node is None else [node.val] + preorder(node.left) + preorder(node.right)

t = TreeNode(1, TreeNode(2, TreeNode(3)), TreeNode(4))
print(preorder(invert(t)))
sym = TreeNode(1, TreeNode(2, TreeNode(3), TreeNode(4)), TreeNode(2, TreeNode(4), TreeNode(3)))
print(is_symmetric(sym))
```

### Lowest common ancestor (LCA)

The **lowest common ancestor** of two nodes is the deepest node that has both of them in its subtree (a node counts as its own ancestor). Ask each subtree "did you find p or q?": the first node where **both** sides answer yes, or that is p or q itself with the other below it, is the LCA.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def lca(root, p, q):
    if root is None or root is p or root is q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root                    # p and q are on different sides: root is the split point
    return left or right               # both on one side (or only one found so far)

n6, n0, n8, n7, n4 = TreeNode(6), TreeNode(0), TreeNode(8), TreeNode(7), TreeNode(4)
n5 = TreeNode(5, n6, TreeNode(2, n7, n4)); n1 = TreeNode(1, n0, n8)
root = TreeNode(3, n5, n1)
print(lca(root, n5, n1).val, lca(root, n6, n4).val, lca(root, n5, n4).val)
```

O(n) time, O(h) space. (For a binary search tree there's a faster O(h) method in the next lesson.)

### Serialise and deserialise

To save a tree to a file or send it over a network, turn it into a string (**serialise**) and back (**deserialise**). Preorder with a marker for empty children is enough to rebuild it exactly.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def serialise(node):
    if node is None:
        return "#"
    return f"{node.val},{serialise(node.left)},{serialise(node.right)}"

def deserialise(text):
    tokens = iter(text.split(","))
    def read():
        tok = next(tokens)
        if tok == "#":
            return None
        node = TreeNode(int(tok))
        node.left = read()
        node.right = read()
        return node
    return read()

t = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
s = serialise(t)
print(s)
print(serialise(deserialise(s)) == s)
```

### Rebuild a tree from preorder and inorder

Preorder's first value is the root; its position in the inorder list splits the left and right subtrees. A dict from value to inorder index makes each split O(1), so the whole rebuild is O(n).

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(preorder, inorder):
    where = {v: i for i, v in enumerate(inorder)}
    pre = iter(preorder)
    def make(lo, hi):                    # build from inorder[lo..hi]
        if lo > hi:
            return None
        val = next(pre)                  # the next preorder value is this subtree's root
        node = TreeNode(val)
        node.left = make(lo, where[val] - 1)
        node.right = make(where[val] + 1, hi)
        return node
    return make(0, len(inorder) - 1)

def postorder(n):
    return [] if n is None else postorder(n.left) + postorder(n.right) + [n.val]

print(postorder(build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])))
```

:::exercise Diameter of a binary tree
Write `diameter(root)` returning the number of **edges** on the longest path between any two nodes. One pass: O(n).
```python starter
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def diameter(root):
    pass

print(diameter(build([1, 2, 3, 4, 5])))   # 3
```
```python check
fn = need("diameter")
test(lambda v: fn(build(v)), show="diameter(build({0}))", cases=[
    ([1, 2, 3, 4, 5], 3, "the example"),
    ([1, 2], 1, "two nodes"),
    ([1], 0, "one node"),
    ([], 0, "an empty tree"),
    ([1, 2, None, 3, 4, 5, None, None, 6, 7, None, None, 8], 6, "the longest path avoids the root"),
    ([1, 2, 3, 4, 5, 6, 7], 4, "a perfect tree"),
])
def _ref_tree(n):
    root = TreeNode(0)
    node = root
    for i in range(1, n):
        node.left = TreeNode(i)
        node.right = TreeNode(-i)
        node = node.left if i % 2 else node.right
    return root
def _d(root):
    best = 0
    def h(node):
        nonlocal best
        if node is None: return 0
        a, b = h(node.left), h(node.right)
        best = max(best, a + b)
        return 1 + max(a, b)
    h(root)
    return best
speed(lambda trees: [fn(t) for t in trees], lambda n: ([_ref_tree(n) for _ in range(100)],),
      lambda trees: [_d(t) for t in trees], sizes=(50, 300), what="levels (100 trees each)",
      tip="Computing the height separately at every node repeats work (O(n^2)). Let one recursive helper return each subtree's height and update the best diameter as it goes.")
```
```python solution
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def diameter(root):
    best = 0

    def height(node):
        nonlocal best
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)      # longest path that turns at this node
        return 1 + max(left, right)

    height(root)
    return best

print(diameter(build([1, 2, 3, 4, 5])))
```
```python slow
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def height(node):
    return 0 if node is None else 1 + max(height(node.left), height(node.right))

def diameter(root):
    if root is None:
        return 0
    through_root = height(root.left) + height(root.right)
    return max(through_root, diameter(root.left), diameter(root.right))
```
hint: Every path has a highest node where it "turns". How long is the longest path that turns at a given node?
hint: Height of its left subtree + height of its right subtree (in edges, that's the number of nodes on each side's longest downward path). The answer is the best of these over all nodes.
hint: Write `height(node)` returning `1 + max(left, right)` (0 for None), and inside it update a `nonlocal best = max(best, left + right)`. Return `best`.
approach:
1. **Understand:** count edges; the path may skip the root; empty or single node → 0.
2. **Examples:** [1, 2, 3, 4, 5] → 3 (4 → 2 → 1 → 3).
3. **Brute force:** at every node, compute both heights from scratch: O(n²) on a long tree.
4. **Pattern:** **return info from children + track a global best** (postorder).
5. **Plan:** height helper; at each node, left + right is a candidate; return 1 + the larger.
6. **Code and test:** a path that avoids the root, a single node.
walkthrough:
**Line by line**

- `height(node)` returns the number of nodes on the longest downward path from `node`, and 0 for `None`.
- At each node, `left + right` counts the edges on the longest path that goes down both sides from here: left edges plus right edges.
- `best` remembers the largest such value over all nodes, because the longest path can turn at any node, not only the root.
- Every node is visited once.

**Trace** on [1, 2, 3, 4, 5]:

| node | left height | right height | left + right | returns |
|---|---|---|---|---|
| 4, 5, 3 | 0 | 0 | 0 | 1 |
| 2 | 1 | 1 | 2 | 2 |
| 1 | 2 | 1 | **3** | 3 |

**Complexity:** O(n) time, O(h) space.

**Common wrong approach:** returning `height(root.left) + height(root.right)` only for the root: a tree whose longest path lives inside one subtree gets the wrong answer.
:::

:::exercise Lowest common ancestor
Write `lowest_common_ancestor(root, p, q)` returning the **node** that is the deepest ancestor of both `p` and `q` (nodes of the tree; a node is an ancestor of itself). Both are guaranteed to be in the tree.
```python starter
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def find(root, val):
    if root is None or root.val == val:
        return root
    return find(root.left, val) or find(root.right, val)

def lowest_common_ancestor(root, p, q):
    pass

root = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
print(lowest_common_ancestor(root, find(root, 5), find(root, 1)).val)   # 3
```
```python check
fn = need("lowest_common_ancestor")
def _run(values, a, b):
    r = build(values)
    got = fn(r, find(r, a), find(r, b))
    if got is not None and not isinstance(got, TreeNode):
        raise AssertionError("Return the ancestor node itself (a TreeNode), not its value.")
    return got.val if got else None
tree = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
test(_run, show="lowest_common_ancestor(root, find(root, {1}), find(root, {2}))  with root = build({0})", cases=[
    ((tree, 5, 1), 3, "on opposite sides of the root"),
    ((tree, 5, 4), 5, "one node is the other's ancestor"),
    ((tree, 6, 4), 5, "both inside the left subtree"),
    ((tree, 7, 4), 2, "siblings deep down"),
    ((tree, 0, 8), 1, "both in the right subtree"),
    (([1, 2], 1, 2), 1, "the root and its child"),
    ((tree, 7, 7), 7, "the same node twice"),
])
```
```python solution
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def find(root, val):
    if root is None or root.val == val:
        return root
    return find(root.left, val) or find(root.right, val)

def lowest_common_ancestor(root, p, q):
    if root is None or root is p or root is q:
        return root                       # found one of them (or nothing here)
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root                       # one on each side: this is where they split
    return left or right                  # pass up whichever side found something

root = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
print(lowest_common_ancestor(root, find(root, 5), find(root, 1)).val)
```
hint: Ask each subtree a yes/no question: "does it contain p or q?" Where do the answers first meet?
hint: If p is found in the left subtree and q in the right, the current node is the LCA. If both are on one side, the LCA is on that side.
hint: Return `root` if it's None, p or q. Recurse left and right. If both results are non-None, return `root`; otherwise return whichever is non-None.
approach:
1. **Understand:** return a node; p and q exist; a node can be its own ancestor.
2. **Examples:** in the sample tree, LCA(5, 1) = 3; LCA(5, 4) = 5; LCA(7, 4) = 2.
3. **Brute force:** store the root-to-p and root-to-q paths, then find the last common node: O(n) time but O(n) extra space and more code.
4. **Pattern:** **return info from children**: each call reports what it found.
5. **Plan:** base cases: None, p or q; combine the two child answers.
6. **Code and test:** one node being the ancestor of the other, p == q, siblings.
walkthrough:
**Line by line**

- If the current node is p or q, return it immediately: if the other node is below it, this node is the LCA; if not, the parent will combine it with the other side's result.
- `left` and `right` are what each subtree found: p, q, the LCA itself, or None.
- Both non-None means p and q are in different subtrees, so this node is the lowest point that contains both.
- Otherwise pass up whatever was found, so the information bubbles up to the split point.

**Trace** for p = 7, q = 4 in [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]:

| node | left result | right result | returns |
|---|---|---|---|
| 6 | None | None | None |
| 7 | — (is p) | | 7 |
| 4 | — (is q) | | 4 |
| 2 | 7 | 4 | **2** (split point) |
| 5 | None (from 6) | 2 | 2 |
| 1 | None | None | None |
| 3 | 2 | None | 2 |

**Complexity:** O(n) time, O(h) space.

**Common wrong approach:** comparing values (`root.val == p.val`) instead of identity, which breaks when values repeat, or returning `root.val` instead of the node.
:::

:::quiz
? Why does the diameter not always pass through the root?
+ The two deepest branches can sit inside one subtree, below the root
- Because the root has no children
- It always does
= That's why each node's left + right height is a candidate, not just the root's.
? Checking balance by computing heights separately at every node costs:
+ O(n²) in the worst case; returning heights from children makes it O(n)
- O(log n)
- O(1)
= Combining children's results avoids recomputing heights.
? In the LCA algorithm, when is the current node the answer?
+ When p is found in one subtree and q in the other (or the node is p or q with the other below it)
- When it's the root
- When it's a leaf
= The first node where the two searches meet is the lowest common ancestor.
? Which pair of traversals is enough to rebuild a binary tree with distinct values?
+ Preorder and inorder
- Preorder and postorder, always
- Inorder alone
= Preorder gives the roots; inorder tells you which values go left and which go right.
:::

@@@ lesson
id: bst
title: Binary search trees
minutes: 26
summary: The BST ordering rule, search and insert in O(h), floor, ceiling and k-th smallest, deleting a node in all three cases, validating a BST with bounds, LCA in a BST, why trees become unbalanced, and how AVL and red-black trees fix it.
---
A **binary search tree (BST)** is a binary tree with one ordering rule at **every** node: everything in the left subtree is smaller than the node, and everything in the right subtree is bigger. That rule turns the tree into a binary search you can also insert into and delete from: each comparison sends you left or right and skips a whole subtree.

![A binary search tree holding 8, 3, 10, 1, 6, 14, 4, 7 and 13 with root 8. The search for 7 is highlighted: 7 < 8 goes left to 3, 7 > 3 goes right to 6, 7 > 6 goes right to 7: found in 4 steps](figures/bst.svg)

Every operation walks one root-to-leaf path, so it costs **O(h)**, where h is the height: **O(log n)** if the tree is balanced, but **O(n)** if it has degenerated into a chain.

### Search and insert

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def search(root, val):
    node = root
    while node and node.val != val:
        node = node.left if val < node.val else node.right   # one comparison discards a subtree
    return node

def insert(root, val):
    if root is None:
        return TreeNode(val)
    node = root
    while True:
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
                return root
            node = node.left
        elif val > node.val:
            if node.right is None:
                node.right = TreeNode(val)
                return root
            node = node.right
        else:
            return root                  # already there: this BST keeps values unique

def inorder(node):
    return [] if node is None else inorder(node.left) + [node.val] + inorder(node.right)

root = None
for v in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    root = insert(root, v)
print(inorder(root))                     # inorder of a BST is always sorted
print(search(root, 7) is not None, search(root, 5) is not None)
```

New values are always added as **leaves**. The smallest value is found by going left until you can't; the largest by going right.

### Floor, ceiling and the k-th smallest

The **floor** of x is the largest value ≤ x; the **ceiling** is the smallest value ≥ x. Walk down as in a search, remembering the best candidate seen. For the k-th smallest, run an inorder traversal and stop after k values.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def floor(root, x):
    best, node = None, root
    while node:
        if node.val == x:
            return x
        if node.val < x:
            best = node.val              # a candidate; something bigger (but still <= x) may be on the right
            node = node.right
        else:
            node = node.left
    return best

def ceiling(root, x):
    best, node = None, root
    while node:
        if node.val == x:
            return x
        if node.val > x:
            best = node.val
            node = node.left
        else:
            node = node.right
    return best

def kth_smallest(root, k):
    stack, node = [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val              # stop early: O(h + k), not O(n)
        node = node.right

root = TreeNode(8, TreeNode(3, TreeNode(1), TreeNode(6, TreeNode(4), TreeNode(7))), TreeNode(10, None, TreeNode(14, TreeNode(13))))
print(floor(root, 5), ceiling(root, 5), floor(root, 0), ceiling(root, 15))
print([kth_smallest(root, k) for k in (1, 3, 9)])
```

### Deleting a node

Deleting needs care, because the tree must stay a BST. There are three cases:

1. **A leaf:** just remove it.
2. **One child:** replace the node with its child.
3. **Two children:** copy in the **inorder successor** (the smallest value of the right subtree, found by going right once and then left all the way), then delete that successor from the right subtree. The successor has no left child, so its own deletion is case 1 or 2.

![Three panels. Deleting leaf 4 removes it. Deleting 10, which has one child 14, links 8 directly to 14. Deleting 3, which has two children, copies its successor 4 (the leftmost node of its right subtree) into its place, then removes the old 4](figures/bst-delete.svg)

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def delete(root, key):
    if root is None:
        return None                              # key not found: nothing changes
    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        if root.left is None:                    # cases 1 and 2: zero or one child
            return root.right
        if root.right is None:
            return root.left
        succ = root.right                        # case 3: smallest value on the right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete(root.right, succ.val)
    return root

def inorder(node):
    return [] if node is None else inorder(node.left) + [node.val] + inorder(node.right)

root = TreeNode(8, TreeNode(3, TreeNode(1), TreeNode(6, TreeNode(4), TreeNode(7))), TreeNode(10, None, TreeNode(14, TreeNode(13))))
for key in (4, 10, 3, 8):
    root = delete(root, key)
    print(f"after deleting {key}: {inorder(root)}, root is {root.val}")
```

Each call goes down one path (plus one more walk for the successor), so deleting is O(h).

### Validating a BST

The tempting check, "left child < node < right child", isn't enough: a value deep in the left subtree could still be bigger than the root. Instead pass down the **range of values allowed** in each subtree. Going left lowers the upper bound; going right raises the lower bound.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def is_bst(node, low=float("-inf"), high=float("inf")):
    if node is None:
        return True
    if not (low < node.val < high):
        return False
    return is_bst(node.left, low, node.val) and is_bst(node.right, node.val, high)

good = TreeNode(5, TreeNode(3, TreeNode(2), TreeNode(4)), TreeNode(8))
sneaky = TreeNode(5, TreeNode(3, TreeNode(2), TreeNode(6)), TreeNode(8))   # 6 is in 5's left subtree
print(is_bst(good), is_bst(sneaky))
```

An equivalent check: an inorder traversal must be **strictly increasing**.

### Lowest common ancestor in a BST

The ordering makes LCA easier than in a general tree: while both values are smaller than the node, go left; while both are bigger, go right; the first node where they split (or that equals one of them) is the answer. O(h) time and O(1) space.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def lca_bst(root, p, q):
    node = root
    while node:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:
            return node.val          # p and q split here (or one of them is this node)

root = TreeNode(6, TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))), TreeNode(8, TreeNode(7), TreeNode(9)))
print(lca_bst(root, 2, 8), lca_bst(root, 3, 5), lca_bst(root, 2, 4))
```

### Why balance matters

The shape of a BST depends on the **order** of insertions. Random order gives a height around 2–3 × log₂ n; sorted order gives a chain, and every operation becomes O(n), no better than a list.

```python
import random

class TreeNode:
    def __init__(self, val):
        self.val, self.left, self.right = val, None, None

def insert(root, val):
    if root is None:
        return TreeNode(val)
    node = root
    while True:
        side = "left" if val < node.val else "right"
        child = getattr(node, side)
        if child is None:
            setattr(node, side, TreeNode(val))
            return root
        node = child

def height(root):                        # level by level, so a chain can't hit the recursion limit
    levels, level = -1, [root] if root else []
    while level:
        levels += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return levels

random.seed(1)
values = list(range(2000))
shuffled = values[:]
random.shuffle(shuffled)
for name, order in [("random order", shuffled), ("sorted order", values)]:
    root = None
    for v in order:
        root = insert(root, v)
    print(f"{name}: height {height(root)} (log2 of 2000 is about 11)")
```

### Self-balancing trees: AVL and red-black

A **self-balancing BST** restructures itself after inserts and deletes so the height stays O(log n). The basic move is a **rotation**: it lifts one child above its parent while keeping the inorder order, in O(1).

![A right rotation. Before: y has left child x; x has subtrees A and B; y has right subtree C. After: x is on top with left subtree A and right child y; y now has B as its left subtree and C on its right. The inorder order A, x, B, y, C is unchanged](figures/rotation.svg)

An **AVL tree** stores each node's height and rotates whenever the two subtrees of a node differ in height by more than 1. Inserting even sorted values keeps it perfectly shallow:

```python
class Node:
    def __init__(self, val):
        self.val, self.left, self.right, self.height = val, None, None, 1

def h(node):
    return node.height if node else 0

def update(node):
    node.height = 1 + max(h(node.left), h(node.right))

def rotate_right(y):
    x = y.left
    y.left = x.right                     # x's right subtree (B) moves under y
    x.right = y
    update(y)
    update(x)
    return x                             # x is the new top of this subtree

def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    update(x)
    update(y)
    return y

def insert(node, val):
    if node is None:
        return Node(val)
    if val < node.val:
        node.left = insert(node.left, val)
    elif val > node.val:
        node.right = insert(node.right, val)
    else:
        return node
    update(node)
    balance = h(node.left) - h(node.right)
    if balance > 1:                      # left side too tall
        if val > node.left.val:          # left-right shape: straighten it first
            node.left = rotate_left(node.left)
        return rotate_right(node)
    if balance < -1:                     # right side too tall
        if val < node.right.val:         # right-left shape
            node.right = rotate_right(node.right)
        return rotate_left(node)
    return node

root = None
for v in range(1, 1001):                 # sorted inserts: the worst case for a plain BST
    root = insert(root, v)
print("AVL height in nodes:", root.height, "| root:", root.val)
```

| Structure | Idea | Search, insert, delete | Where you meet it |
|---|---|---|---|
| Plain BST | no rebalancing | O(h): O(log n) average, O(n) worst | teaching, random data |
| **AVL tree** | heights of siblings differ by ≤ 1; rotate to fix | O(log n) worst case | lookup-heavy workloads |
| **Red-black tree** | nodes coloured red/black; looser balance, fewer rotations | O(log n) worst case | C++ `std::map`, Java `TreeMap`, the Linux kernel |
| **B-tree / B+ tree** | many keys per node, very shallow | O(log n) with few disk reads | database indexes, file systems |
| **Treap, skip list** | randomness keeps it balanced on average | O(log n) expected | Redis sorted sets use a skip list |

You won't usually write a red-black tree in an interview; know what it guarantees and why.

### Sorted collections in Python

Python has no built-in balanced BST. For an ordered collection you can:

- Keep a **sorted list** with `bisect`: searching is O(log n); `bisect.insort` is O(n) per insert because it shifts items, but that shift is a fast C memory move, so it's fine up to around 10⁵ items.
- Use `sortedcontainers.SortedList` (a popular third-party package, also available on LeetCode): O(log n)-style add, remove and index lookups.

```py-static
from sortedcontainers import SortedList     # pip install sortedcontainers

s = SortedList([5, 1, 8])
s.add(3)                     # [1, 3, 5, 8]
s.remove(5)                  # [1, 3, 8]
print(s[0], s[-1])           # smallest and largest: 1 8
print(s.bisect_left(4))      # how many items are < 4: 2
```

:::exercise Validate a binary search tree
Write `is_valid_bst(root)` returning `True` if the tree is a BST with **strictly** increasing values (no duplicates allowed), and `False` otherwise. An empty tree is valid.
```python starter
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def is_valid_bst(root):
    pass

print(is_valid_bst(build([2, 1, 3])))                      # True
print(is_valid_bst(build([5, 1, 4, None, None, 3, 6])))    # False
```
```python check
fn = need("is_valid_bst")
test(lambda v: fn(build(v)), show="is_valid_bst(build({0}))", cases=[
    ([2, 1, 3], True, "a small valid tree"),
    ([5, 1, 4, None, None, 3, 6], False, "a right child smaller than the root"),
    ([5, 4, 6, None, None, 3, 7], False, "3 sits in 5's right subtree (each parent-child pair looks fine)"),
    ([], True, "an empty tree"),
    ([1], True, "a single node"),
    ([2, 2, 2], False, "duplicates"),
    ([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], True, "a bigger valid tree"),
    ([10, 5, 15, None, None, 6, 20], False, "6 is below 15 but smaller than the root 10"),
    ([-2147483648, None, 2147483647], True, "values at the edges of a 32-bit int"),
])
```
```python solution
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def is_valid_bst(root, low=float("-inf"), high=float("inf")):
    if root is None:
        return True
    if not (low < root.val < high):          # must fit the range set by all its ancestors
        return False
    return (is_valid_bst(root.left, low, root.val) and
            is_valid_bst(root.right, root.val, high))

print(is_valid_bst(build([2, 1, 3])))
print(is_valid_bst(build([5, 1, 4, None, None, 3, 6])))
```
hint: Checking each node against its two children isn't enough. Which test case shows why?
hint: In [5, 4, 6, None, None, 3, 7], node 3 is a fine left child of 6, but it's in the **right** subtree of 5, so it must be bigger than 5. Each node has a range of allowed values set by all its ancestors.
hint: Recurse with bounds: `check(node, low, high)`. The node must satisfy `low < node.val < high`; the left child gets `(low, node.val)` and the right child gets `(node.val, high)`. Start with minus and plus infinity.
approach:
1. **Understand:** strict ordering against **all** ancestors, not just the parent; empty is valid; duplicates are invalid.
2. **Examples:** [2, 1, 3] → True; [5, 4, 6, None, None, 3, 7] → False because of the 3.
3. **Brute force:** for every node, compare it with the max of its left subtree and the min of its right subtree: O(n²) on a chain.
4. **Pattern:** **pass information down** (preorder): the allowed range. Alternative: inorder must be strictly increasing.
5. **Plan:** recursive helper with `low` and `high`, tightened at each step.
6. **Code and test:** the "grandchild breaks it" case, duplicates, extreme values.
walkthrough:
**Line by line**

- Default bounds of minus and plus infinity mean the root may hold any value, including ±2³¹.
- `low < root.val < high` uses strict comparisons, so duplicates fail.
- Going left, every value must stay below the current node, so `high` becomes `root.val`; going right, `low` becomes `root.val`. Bounds from higher ancestors are carried along.
- `and` stops early: once one side is invalid, the other isn't checked.

**Trace** on [5, 4, 6, None, None, 3, 7]:

| node | low | high | fits? |
|---|---|---|---|
| 5 | −∞ | ∞ | yes |
| 4 | −∞ | 5 | yes |
| 6 | 5 | ∞ | yes |
| 3 | 5 | 6 | **no**: 3 is not > 5 → False |

**Complexity:** O(n) time, O(h) space.

**Common wrong approach:** comparing a node only with its own children (`node.left.val < node.val < node.right.val`), which passes the [5, 4, 6, None, None, 3, 7] tree.
:::

:::exercise Delete a node from a BST
Write `delete_node(root, key)` that removes `key` from the BST (if it's there) and returns the root of the resulting tree, which must still be a valid BST. The root itself may be deleted.
```python starter
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def inorder(node):
    return [] if node is None else inorder(node.left) + [node.val] + inorder(node.right)

def delete_node(root, key):
    pass

print(inorder(delete_node(build([5, 3, 6, 2, 4, None, 7]), 3)))   # [2, 4, 5, 6, 7]
```
```python check
fn = need("delete_node")
def _ok(node, low=float("-inf"), high=float("inf")):
    return node is None or (low < node.val < high and _ok(node.left, low, node.val) and _ok(node.right, node.val, high))
def _run(values, key):
    got = fn(build(values), key)
    if got is not None and not isinstance(got, TreeNode):
        raise AssertionError("Return the root node of the tree (a TreeNode or None).")
    if not _ok(got):
        return "a tree that is no longer a valid BST"
    return inorder(got)
test(_run, show="inorder(delete_node(build({0}), {1}))", cases=[
    (([5, 3, 6, 2, 4, None, 7], 3), [2, 4, 5, 6, 7], "a node with two children"),
    (([5, 3, 6, 2, 4, None, 7], 7), [2, 3, 4, 5, 6], "a leaf"),
    (([5, 3, 6, 2, 4, None, 7], 6), [2, 3, 4, 5, 7], "a node with one child"),
    (([5, 3, 6, 2, 4, None, 7], 5), [2, 3, 4, 6, 7], "the root"),
    (([5, 3, 6, 2, 4, None, 7], 0), [2, 3, 4, 5, 6, 7], "a key that isn't in the tree"),
    (([1], 1), [], "the only node"),
    (([], 1), [], "an empty tree"),
    (([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], 3), [1, 4, 6, 7, 8, 10, 13, 14], "a successor deep in the right subtree"),
    (([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], 10), [1, 3, 4, 6, 7, 8, 13, 14], "a node whose only child has a child"),
])
```
```python solution
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); queue.append(node.right)
        i += 1
    return root

def inorder(node):
    return [] if node is None else inorder(node.left) + [node.val] + inorder(node.right)

def delete_node(root, key):
    if root is None:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)      # the key can only be on the left
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:                         # no left child: the right subtree takes its place
            return root.right
        if root.right is None:
            return root.left
        succ = root.right                             # two children: find the inorder successor
        while succ.left:
            succ = succ.left
        root.val = succ.val                           # copy it up...
        root.right = delete_node(root.right, succ.val)   # ...and delete it from the right subtree
    return root

print(inorder(delete_node(build([5, 3, 6, 2, 4, None, 7]), 3)))
```
hint: First find the node, using the BST rule to go left or right. Then think about how many children it has: 0, 1 or 2.
hint: With 0 or 1 child, return the other child (possibly None) so the parent links straight past the deleted node. Assign the result back: `root.left = delete_node(root.left, key)`.
hint: With 2 children, find the smallest value in the right subtree (one step right, then left as far as possible), copy it into the node, and delete that value from the right subtree.
approach:
1. **Understand:** return the (possibly new) root; a missing key leaves the tree unchanged; the result must remain a BST.
2. **Examples:** deleting 3 from [5, 3, 6, 2, 4, None, 7] puts 4 in its place.
3. **Brute force:** collect all values except the key and rebuild a balanced BST: O(n), and it throws the structure away.
4. **Pattern:** **recursive BST descent** that returns the new subtree root, plus the **inorder successor** trick.
5. **Plan:** recurse into the correct side; at the node, handle 0/1 children by returning the other child, 2 children by copying the successor.
6. **Code and test:** a leaf, one child, two children, the root, a missing key, the only node.
walkthrough:
**Line by line**

- Each call returns the root of its subtree after deletion, and the parent stores it with `root.left = …` or `root.right = …`. That's how a deleted child gets unlinked.
- `if root.left is None: return root.right` handles both a leaf (returns None) and a node with only a right child.
- The successor is the smallest value bigger than the node, so putting it in the node's place keeps everything on the left smaller and everything on the right bigger.
- Deleting the successor from the right subtree is easy, because it has no left child.

**Trace** deleting 3 from [5, 3, 6, 2, 4, None, 7]:

| call | situation | action | returns |
|---|---|---|---|
| node 5 | 3 < 5 | `5.left = delete(3's subtree, 3)` | 5 |
| node 3 | found, two children | successor = 4; copy 4 into the node; delete 4 on the right | the node (now 4) |
| node 4 | found, no children | return its right child | None |

**Complexity:** O(h) time and O(h) recursion space.

**Common wrong approach:** forgetting to assign the recursive result back (`delete_node(root.left, key)` on its own line), so the parent still points at the deleted node.
:::

:::quiz
? What does an inorder traversal of a binary search tree produce?
+ The values in sorted order
- The values in insertion order
- The values level by level
= Left subtree (smaller), node, right subtree (bigger): sorted.
? You insert 1, 2, 3, …, n in order into a plain BST. How long does a search take afterwards?
+ O(n): the tree is a chain
- O(log n)
- O(1)
= Sorted insertions make every node a right child. Self-balancing trees prevent this.
? When deleting a node with two children, what replaces it?
+ Its inorder successor (the smallest value in its right subtree)
- Its left child
- The root
= The successor is bigger than everything on the left and smaller than everything else on the right. (The inorder predecessor works too.)
? What is the purpose of a rotation in an AVL or red-black tree?
+ To reduce height while keeping the inorder (sorted) order
- To sort the values
- To delete a node
= A rotation lifts a child above its parent in O(1) and preserves the BST order.
:::

@@@ lesson
id: heaps
title: Heaps and priority queues
minutes: 26
summary: The heap property, storing a complete tree in a list, sift up and sift down, O(n) heapify, Python's heapq (including the new max-heap functions in 3.14), priorities and tie-breakers, top-k, merging sorted lists and the two-heap running median.
---
A **priority queue** hands back the **most important** item first (the smallest number, the earliest deadline, the shortest distance) rather than the oldest. The standard way to build one is a **binary heap**: a complete binary tree where every parent is ≤ its children (a **min-heap**) or ≥ its children (a **max-heap**). The smallest item is always at the root.

A heap is **not** sorted: siblings can be in any order. It only promises enough order to find and remove the minimum quickly.

### A tree stored in a list

Because a heap is a **complete** tree (every level full except the last, filled from the left), it fits in a plain list with no pointers. For the item at index i:

| Relative | Index |
|---|---|
| left child | 2i + 1 |
| right child | 2i + 2 |
| parent | (i − 1) // 2 |

![A min-heap drawn as a tree (1 at the root; 3 and 2 below; then 7, 4, 5, 8) and the same heap as a list [1, 3, 2, 7, 4, 5, 8] with indexes 0 to 6. Arrows show that index 1 (value 3) has children at indexes 3 and 4](figures/heap-array.svg)

### Push and pop: sift up and sift down

- **Push:** append the new item at the end, then **sift up**: swap it with its parent while it's smaller. O(log n), the height of the tree.
- **Pop:** the minimum is at index 0. Move the **last** item to the root, then **sift down**: swap it with its smaller child while it's bigger than that child. O(log n).
- **Peek:** `heap[0]`, O(1).

```python
class MinHeap:
    def __init__(self):
        self.a = []

    def push(self, x):
        a = self.a
        a.append(x)
        i = len(a) - 1
        while i > 0 and a[i] < a[(i - 1) // 2]:       # smaller than its parent: swap upwards
            parent = (i - 1) // 2
            a[i], a[parent] = a[parent], a[i]
            i = parent

    def pop(self):
        a = self.a
        top = a[0]
        last = a.pop()
        if a:
            a[0] = last                               # fill the hole at the root with the last item
            i, n = 0, len(a)
            while True:
                smallest = i
                for child in (2 * i + 1, 2 * i + 2):
                    if child < n and a[child] < a[smallest]:
                        smallest = child
                if smallest == i:
                    break                             # both children are bigger: done
                a[i], a[smallest] = a[smallest], a[i]
                i = smallest
        return top

h = MinHeap()
for x in [5, 3, 8, 1, 9, 2]:
    h.push(x)
print("as a list:", h.a)
print("popped in order:", [h.pop() for _ in range(6)])
```

Popping every item gives them in sorted order: that's **heap sort**, O(n log n).

### Heapify in O(n)

Pushing n items one by one costs O(n log n). **Heapify** does better: sift down every non-leaf node, starting from the last one and moving back to the root. Most nodes are near the bottom, where sifting is short (half the nodes are leaves and don't move at all), and the total work adds up to **O(n)**. `heapq.heapify(list)` does this in place.

### Python's heapq

`heapq` turns an ordinary list into a **min-heap**; the list *is* the heap.

| Call | What it does | Cost |
|---|---|---|
| `heapq.heapify(a)` | rearrange list `a` into a heap, in place | O(n) |
| `heapq.heappush(a, x)` | add x | O(log n) |
| `heapq.heappop(a)` | remove and return the smallest | O(log n) |
| `a[0]` | look at the smallest without removing it | O(1) |
| `heapq.heappushpop(a, x)` | push x, then pop the smallest (faster than both) | O(log n) |
| `heapq.heapreplace(a, x)` | pop the smallest, then push x | O(log n) |
| `heapq.nsmallest(k, it)` / `nlargest(k, it)` | the k smallest / largest items | O(n log k) |
| `heapq.merge(*sorted_iterables)` | lazily merge already-sorted inputs | O(n log k) |

```python
import heapq

tasks = [5, 1, 8, 3, 2]
heapq.heapify(tasks)
print(tasks, "smallest:", tasks[0])
heapq.heappush(tasks, 0)
print([heapq.heappop(tasks) for _ in range(3)], "left:", sorted(tasks))

# Priorities with tuples: compared by the first item, then the second...
jobs = []
heapq.heappush(jobs, (2, "write report"))
heapq.heappush(jobs, (1, "fix the outage"))
heapq.heappush(jobs, (3, "lunch"))
print(heapq.heappop(jobs))

# Max-heap: push negated keys
scores = [40, 95, 70]
neg = [-s for s in scores]
heapq.heapify(neg)
print("largest:", -heapq.heappop(neg))
```

**Ties and objects:** with `(priority, item)` tuples, two equal priorities make Python compare the items, which fails for things like dicts (`TypeError: '<' not supported`). Add a counter as a tie-breaker, `(priority, count, item)`; it also keeps equal priorities in first-in, first-out order.

```python
import heapq
from itertools import count

order = count()
heap = []
for priority, job in [(2, {"name": "b"}), (1, {"name": "a"}), (2, {"name": "c"})]:
    heapq.heappush(heap, (priority, next(order), job))   # the counter breaks ties before the dicts are compared
print([heapq.heappop(heap)[2]["name"] for _ in range(3)])
```

**New in Python 3.14:** `heapq` now has max-heap versions of its functions, so you don't have to negate numbers (handy for items that can't be negated, like strings):

```py-static
import heapq                                    # Python 3.14 or newer

a = [3, 9, 4]
heapq.heapify_max(a)
heapq.heappush_max(a, 7)
print(heapq.heappop_max(a))                     # 9
# also: heapq.heapreplace_max, heapq.heappushpop_max
```

Most coding-interview platforms still run older versions, so know the negation trick too.

### Top k: keep a heap of size k

To find the k **largest** of n items, keep a **min-heap of the k best so far**. Its root is the weakest of them; each new item that beats the root replaces it. That's O(n log k) time and O(k) memory, and it works on a stream too big to store. Sorting everything is O(n log n).

```python
import heapq

def k_largest(nums, k):
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:                 # beats the weakest of the current top k
            heapq.heapreplace(heap, x)
    return sorted(heap, reverse=True)

nums = [7, 2, 9, 4, 11, 3, 8, 6]
print(k_largest(nums, 3), heapq.nlargest(3, nums))
print("3rd largest:", k_largest(nums, 3)[-1])
```

The same idea finds the k closest points, the k most frequent words (count with `Counter`, then a heap on the counts) or the k-th largest item (the root of the size-k heap).

### Merging k sorted lists

Put the **first** item of each list in a heap. Pop the smallest, output it, and push the next item from the same list. With N items in total across k lists: O(N log k).

```python
import heapq

def merge_k(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]   # (value, which list, position)
    heapq.heapify(heap)
    out = []
    while heap:
        value, i, j = heapq.heappop(heap)
        out.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out

lists = [[1, 4, 9], [2, 3, 10], [5, 6], []]
print(merge_k(lists))
print(list(heapq.merge(*lists)))          # the built-in does the same, lazily
```

### Running median with two heaps

To get the median of a growing stream, split the numbers into a **max-heap of the smaller half** and a **min-heap of the larger half**, keeping their sizes equal or the lower half one bigger. The median is then at the top of one or both heaps: O(log n) per number, O(1) per median.

![Two heaps side by side. The lower half [1, 2, 3] is a max-heap with 3 on top; the upper half [5, 8, 9] is a min-heap with 5 on top. The median is (3 + 5) / 2 = 4](figures/two-heaps.svg)

The full code is the next exercise.

### Where heaps show up

| Problem | Heap holds | Cost |
|---|---|---|
| k largest / smallest, k closest | the k best so far | O(n log k) |
| Merge k sorted lists | the next item of each list | O(N log k) |
| Running median | two halves | O(log n) per item |
| Dijkstra's shortest paths (Part 8) | (distance, node) | O((V + E) log V) |
| Task scheduling, event simulation | (time, event) | O(log n) per event |
| Huffman coding (Part 9) | (frequency, subtree) | O(n log n) |

Heaps can't search for or remove an arbitrary item quickly (O(n)). When you need to, a common trick is **lazy deletion**: mark the item as removed and skip it when it reaches the top.

:::exercise K closest points to the origin
Write `k_closest(points, k)` returning the `k` points (lists `[x, y]`) closest to `(0, 0)`, in any order. Distance is the usual straight-line distance; you can compare squared distances `x*x + y*y` and skip the square root.
```python starter
import heapq

def k_closest(points, k):
    pass

print(k_closest([[1, 3], [-2, 2]], 1))           # [[-2, 2]]
print(k_closest([[3, 3], [5, -1], [-2, 4]], 2))  # [[3, 3], [-2, 4]] in any order
```
```python check
fn = need("k_closest")
_key = lambda pts: sorted(map(tuple, pts)) if isinstance(pts, list) else pts
test(fn, key=_key, cases=[
    (([[1, 3], [-2, 2]], 1), [[-2, 2]], "the first example"),
    (([[3, 3], [5, -1], [-2, 4]], 2), [[3, 3], [-2, 4]], "the second example"),
    (([[0, 1], [1, 0]], 2), [[0, 1], [1, 0]], "k equals the number of points"),
    (([[2, 2], [1, 1], [3, 3], [0, 0]], 1), [[0, 0]], "a point at the origin"),
    (([[-5, 0], [4, 0], [0, -3], [10, 10]], 3), [[-5, 0], [4, 0], [0, -3]], "negative coordinates"),
])
```
```python solution
import heapq

def k_closest(points, k):
    heap = []                                    # max-heap (by negated distance) of the k closest so far
    for x, y in points:
        d = x * x + y * y
        if len(heap) < k:
            heapq.heappush(heap, (-d, x, y))
        elif -d > heap[0][0]:                    # closer than the farthest point kept
            heapq.heapreplace(heap, (-d, x, y))
    return [[x, y] for _, x, y in heap]

print(k_closest([[1, 3], [-2, 2]], 1))
print(k_closest([[3, 3], [5, -1], [-2, 4]], 2))
```
hint: Sorting all points by distance works in O(n log n). Can you keep just k points as you go?
hint: Keep the k closest points seen so far in a heap whose **top is the farthest** of them, so you can kick it out when a closer point arrives. heapq is a min-heap, so store the **negated** squared distance.
hint: For each point: push `(-d, x, y)` while the heap has fewer than k items; otherwise, if `-d > heap[0][0]` (it's closer than the farthest kept), `heapreplace`. Finally return the points in the heap.
approach:
1. **Understand:** any order; squared distances compare the same way as real distances.
2. **Examples:** [[1, 3], [-2, 2]], k = 1 → [[-2, 2]] (8 < 10).
3. **Brute force:** sort by distance and take the first k: O(n log n), perfectly fine for small inputs. `heapq.nsmallest(k, points, key=...)` is a one-line version.
4. **Pattern:** **top k with a heap of size k**; we want the smallest distances, so the heap keeps the largest of them on top (a max-heap via negation).
5. **Plan:** loop, push or replace, return the heap's points.
6. **Code and test:** k = n, a point at the origin, negative coordinates.
walkthrough:
**Line by line**

- `d = x*x + y*y` avoids `sqrt`, which is slower and would introduce floats.
- The heap stores `(-d, x, y)`: the most negative first item, the farthest kept point, sits at `heap[0]`.
- `-d > heap[0][0]` means `d < (farthest kept distance)`, so the new point deserves a place; `heapreplace` pops the farthest and pushes the new one in one O(log k) step.
- At the end the heap holds exactly the k closest points.

**Trace** on [[3, 3], [5, -1], [-2, 4]], k = 2:

| point | d | heap (as −d, x, y) | action |
|---|---|---|---|
| [3, 3] | 18 | (−18, 3, 3) | push |
| [5, −1] | 26 | (−26, 5, −1), (−18, 3, 3) | push |
| [−2, 4] | 20 | (−20, −2, 4), (−18, 3, 3) | −20 > −26: replace the farthest |

**Complexity:** O(n log k) time, O(k) space.

**Common wrong approach:** using a min-heap of distances and stopping after k pushes: that keeps the first k points, not the closest.
:::

:::exercise Running median
Complete `MedianFinder` with `add(num)` and `median()`, which returns the median of all numbers added so far: the middle value, or the average of the two middle values when the count is even. Both must be fast: 100,000 adds, each followed by a `median()` call, should take well under a second.
```python starter
import heapq

class MedianFinder:
    def __init__(self):
        pass

    def add(self, num):
        pass

    def median(self):
        pass

m = MedianFinder()
for x in [5, 15, 1, 3]:
    m.add(x)
    print(m.median())      # 5, 10.0, 5, 4.0
```
```python check
cls = need("MedianFinder")
def _ops(nums):
    m, out = cls(), []
    for x in nums:
        m.add(x)
        out.append(m.median())
    return out
test(_ops, show="medians after adding each of {0}", cases=[
    (([5, 15, 1, 3],), [5, 10, 5, 4], "the example"),
    (([1],), [1], "a single number"),
    (([2, 2, 2, 2],), [2, 2, 2, 2], "equal numbers"),
    (([1, 2, 3, 4, 5, 6],), [1, 1.5, 2, 2.5, 3, 3.5], "increasing numbers"),
    (([6, 5, 4, 3, 2, 1],), [6, 5.5, 5, 4.5, 4, 3.5], "decreasing numbers"),
    (([-1, -2, -3, -4, -5],), [-1, -1.5, -2, -2.5, -3], "negative numbers"),
])
import heapq as _hq, random as _random
class _Ref:
    def __init__(self): self.lo, self.hi = [], []
    def add(self, x):
        _hq.heappush(self.lo, -x)
        _hq.heappush(self.hi, -_hq.heappop(self.lo))
        if len(self.hi) > len(self.lo): _hq.heappush(self.lo, -_hq.heappop(self.hi))
    def median(self):
        return -self.lo[0] if len(self.lo) > len(self.hi) else (-self.lo[0] + self.hi[0]) / 2
def _bulk(cls_, n):
    rng, m, total = _random.Random(n), cls_(), 0
    for _ in range(n):
        m.add(rng.randint(-10**6, 10**6))
        total += m.median()
    return total
speed(lambda n: _bulk(cls, n), lambda n: n, lambda n: _bulk(_Ref, n), sizes=(1_000, 4_000, 100_000), what="numbers",
      tip="Sorting all the numbers on every median() call is O(n log n) each time. Keep the lower half in a max-heap and the upper half in a min-heap, so the middle is always at their tops.")
```
```python solution
import heapq

class MedianFinder:
    def __init__(self):
        self.low = []     # max-heap of the smaller half (numbers stored negated)
        self.high = []    # min-heap of the larger half

    def add(self, num):
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))   # move low's largest across: halves stay ordered
        if len(self.high) > len(self.low):                    # rebalance: low may be bigger by one, never smaller
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2

m = MedianFinder()
for x in [5, 15, 1, 3]:
    m.add(x)
    print(m.median())
```
```python slow
class MedianFinder:
    def __init__(self):
        self.nums = []

    def add(self, num):
        self.nums.append(num)

    def median(self):
        s = sorted(self.nums)
        n = len(s)
        return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
```
hint: The median only depends on the one or two numbers in the middle. What if the smaller half and the larger half were kept separately?
hint: Keep the smaller half in a **max-heap** (its top is the biggest of the small numbers) and the larger half in a **min-heap** (its top is the smallest of the big numbers). Keep their sizes equal, or the smaller half one bigger.
hint: To add: push onto the low heap (negated), move low's top to high, and if high is now bigger than low, move high's top back. The median is low's top (odd count) or the average of both tops (even count).
approach:
1. **Understand:** median after every add; even counts average the two middle values; many calls, so each must be fast.
2. **Examples:** add 5 → 5; add 15 → 10.0; add 1 → 5; add 3 → 4.0.
3. **Brute force:** sort on every `median()` call: O(n log n) each. Keeping a sorted list with `bisect.insort` is better (O(n) per add, but a fast memory move).
4. **Pattern:** **two heaps** that split the data at the median.
5. **Plan:** every number passes through low into high, then sizes are rebalanced; median from the tops.
6. **Code and test:** one number, equal numbers, increasing and decreasing streams.
walkthrough:
**Line by line**

- `low` stores negated numbers, so `-self.low[0]` is the largest of the smaller half.
- Pushing into `low` and then moving low's top into `high` guarantees every number in `low` is ≤ every number in `high`, wherever the new number belongs.
- The size fix keeps `len(low)` equal to `len(high)` or one more, so with an odd count the median is the top of `low`.
- With an even count the median is the average of the two tops.

**Trace** adding 5, 15, 1, 3:

| add | low (real values) | high | median |
|---|---|---|---|
| 5 | [5] | [] | 5 |
| 15 | [5] | [15] | (5 + 15) / 2 = 10.0 |
| 1 | [1, 5] | [15] | 5 |
| 3 | [1, 3] | [5, 15] | (3 + 5) / 2 = 4.0 |

**Complexity:** O(log n) per `add`, O(1) per `median`, O(n) space.

**Common wrong approach:** pushing into whichever heap is smaller without moving numbers across, so a big number can end up in the low half and the tops no longer surround the middle.
:::

:::quiz
? In a list-based heap, where are the children of the item at index i?
+ 2i + 1 and 2i + 2
- i + 1 and i + 2
- 2i and 2i − 1
= And the parent is at (i − 1) // 2.
? How long does heapq.heapify take on a list of n items?
+ O(n)
- O(n log n)
- O(log n)
= Sifting down from the bottom up costs O(n) in total, because most nodes are near the leaves.
? To find the k largest of n numbers with a heap, which heap do you keep?
+ A min-heap of size k, whose root is the weakest of the current top k
- A max-heap of all n numbers
- A min-heap of all n numbers
= Each new number only needs to beat the root. O(n log k) time, O(k) memory.
? Why add a counter to (priority, item) tuples in heapq?
+ So equal priorities don't fall back to comparing the items, which may not be comparable
- To make the heap a max-heap
- heapq requires exactly three values
= (priority, count, item) never reaches the item in a comparison, and keeps ties in insertion order.
:::

@@@ lesson
id: tries
title: Tries (prefix trees)
minutes: 22
summary: A tree of characters for prefix questions: insert, search and prefix checks in O(length of the word), autocomplete, counting and deleting words, wildcard search, longest-prefix matching, and when a set or a sorted list is the simpler choice.
---
A **trie** (pronounced "try", from re*trie*val), or **prefix tree**, stores strings character by character. Each node is one step along a word, its children are the possible next characters, and a flag marks nodes where a complete word ends. Words that share a prefix share the path for it.

![A trie holding car, cat, cart, dog and do. From the root, c leads to a, which branches to r and t; r continues to t. d leads to o, which continues to g. Nodes where a word ends (car, cat, cart, do, dog) are drawn with a thick green border](figures/trie.svg)

Every operation walks one character at a time, so it costs **O(L)** for a word of length L, **no matter how many words are stored**. That's the trie's selling point for prefix questions: "is there any word starting with *ca*?" takes 2 steps.

### A trie class

```python
class TrieNode:
    def __init__(self):
        self.children = {}          # character -> TrieNode
        self.is_word = False        # does a word end exactly here?

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True

    def _walk(self, text):          # the node reached by following text, or None
        node = self.root
        for ch in text:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

t = Trie()
for w in ["car", "cat", "cart", "dog", "do"]:
    t.insert(w)
print(t.search("car"), t.search("ca"), t.starts_with("ca"), t.starts_with("cow"))
```

`search("ca")` is False even though the path exists, because no word **ends** there. Forgetting the end-of-word flag is the classic trie bug.

A compact version uses nested dicts, with a special key such as `"$"` marking the end of a word. It's popular in interviews because it's short:

```python
def make_trie(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})   # get the child, creating it if missing
        node["$"] = True                     # end-of-word marker
    return root

trie = make_trie(["car", "cat", "cart"])
print(trie)
```

### Autocomplete

Walk down to the prefix's node, then collect every word below it with a depth-first search. Visiting children in alphabetical order gives the words in sorted order, and you can stop after the first few.

```python
class TrieNode:
    def __init__(self):
        self.children, self.is_word = {}, False

def insert(root, word):
    node = root
    for ch in word:
        node = node.children.setdefault(ch, TrieNode())
    node.is_word = True

def complete(root, prefix, limit=5):
    node = root
    for ch in prefix:
        node = node.children.get(ch)
        if node is None:
            return []                         # nothing starts with this prefix
    found = []
    def dfs(node, path):
        if len(found) == limit:
            return
        if node.is_word:
            found.append(prefix + path)
        for ch in sorted(node.children):      # alphabetical order
            dfs(node.children[ch], path + ch)
    dfs(node, "")
    return found

root = TrieNode()
for w in ["apple", "app", "application", "apply", "ape", "banana", "apt"]:
    insert(root, w)
print(complete(root, "app"))
print(complete(root, "ap", limit=3))
print(complete(root, "c"))
```

### Counting words with a prefix, and deleting

Store a **count** in each node of how many words pass through it; then "how many words start with *ap*?" is answered by one walk. Deleting a word decrements the counts along its path and clears its end flag.

```python
class TrieNode:
    def __init__(self):
        self.children, self.count, self.ends = {}, 0, 0   # words passing through / ending here

class CountingTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
            node.count += 1
        node.ends += 1

    def count_prefix(self, prefix):
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return 0
        return node.count

    def delete(self, word):               # assumes the word is present
        node = self.root
        for ch in word:
            child = node.children[ch]
            child.count -= 1
            if child.count == 0:
                del node.children[ch]     # no words use this branch any more: prune it
                return
            node = child
        node.ends -= 1

t = CountingTrie()
for w in ["apple", "app", "apt", "bat"]:
    t.insert(w)
print(t.count_prefix("ap"), t.count_prefix("app"), t.count_prefix("b"))
t.delete("apple")
print(t.count_prefix("ap"), t.count_prefix("appl"))
```

### Wildcard search

To support patterns like `"c.t"` where `.` matches any letter, search recursively: at a `.`, try **every** child.

```python
def make_trie(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True
    return root

def matches(node, pattern, i=0):
    if i == len(pattern):
        return "$" in node
    ch = pattern[i]
    if ch == ".":
        return any(matches(child, pattern, i + 1) for key, child in node.items() if key != "$")
    return ch in node and matches(node[ch], pattern, i + 1)

trie = make_trie(["cat", "cot", "cut", "car", "dog"])
print(matches(trie, "c.t"), matches(trie, "..g"), matches(trie, "c.."), matches(trie, "d.t"))
```

Worst case this branches at every dot (26ᵈ paths for d dots), but real dictionaries prune it quickly.

### Longest prefix match

Routers pick the most specific route for an address; spell checkers and tokenizers find the longest dictionary word at the start of the text. Walk the trie along the text and remember the **last** place a word ended.

```python
def make_trie(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = True
    return root

def longest_prefix(trie, text):
    node, best = trie, ""
    for i, ch in enumerate(text):
        if ch not in node:
            break
        node = node[ch]
        if "$" in node:
            best = text[:i + 1]           # a word ends here: the longest match so far
    return best

routes = make_trie(["10.", "10.1.", "10.1.2.", "192.168."])
print(longest_prefix(routes, "10.1.2.7"), longest_prefix(routes, "10.1.9.9"), repr(longest_prefix(routes, "8.8.8.8")))
```

### Trie or something simpler?

| Need | Simplest good tool | Cost |
|---|---|---|
| Is this exact word present? | a `set` | O(L) average |
| Words with a given prefix, in order | sorted list + `bisect_left(prefix)`, then read forwards | O(L log n) per lookup |
| Many prefix queries, counts per prefix, wildcards, longest-prefix matches | **trie** | O(L) per operation |
| Searching a grid for many dictionary words at once (word search II) | **trie** + DFS, pruning paths that aren't prefixes | far less than one search per word |

Tries use a lot of memory: one node object (with its own dict) per character. A **radix tree** (compressed trie) merges chains of single-child nodes into one edge labelled with a string, and is what many real routers and databases use. A **binary trie** over the bits of numbers solves "maximum XOR of two numbers" problems (Part 10).

:::exercise Implement a trie
Complete `Trie` with `insert(word)`, `search(word)` (True only if that exact word was inserted) and `starts_with(prefix)` (True if any inserted word starts with it). Each operation must take O(length of the string), however many words are stored. Don't keep a list or set of all the words.
```python starter
class Trie:
    def __init__(self):
        pass

    def insert(self, word):
        pass

    def search(self, word):
        pass

    def starts_with(self, prefix):
        pass

t = Trie()
t.insert("apple")
print(t.search("apple"), t.search("app"), t.starts_with("app"))   # True False True
t.insert("app")
print(t.search("app"))                                            # True
```
```python check
cls = need("Trie")
def _ops(ops):
    t, out = cls(), []
    for op, arg in ops:
        if op == "insert":
            t.insert(arg); out.append(None)
        elif op == "search":
            out.append(t.search(arg))
        else:
            out.append(t.starts_with(arg))
    return out
test(_ops, show="the results of the operations {0}", cases=[
    (([("insert", "apple"), ("search", "apple"), ("search", "app"), ("starts_with", "app"), ("insert", "app"), ("search", "app")],),
     [None, True, False, True, None, True], "the example"),
    (([("search", "a"), ("starts_with", "a")],), [False, False], "an empty trie"),
    (([("insert", "a"), ("search", "a"), ("search", "ab"), ("starts_with", "ab")],), [None, True, False, False], "a one-letter word"),
    (([("insert", "car"), ("insert", "cat"), ("search", "ca"), ("starts_with", "ca"), ("search", "cart"), ("starts_with", "dog")],),
     [None, None, False, True, False, False], "a shared prefix that isn't a word"),
    (([("insert", "hello"), ("starts_with", "hello"), ("starts_with", "hellos"), ("starts_with", "")],), [None, True, False, True], "the whole word as a prefix, and the empty prefix"),
    (([("insert", "same"), ("insert", "same"), ("search", "same")],), [None, None, True], "inserting a word twice"),
])
import random as _random
class _Ref:
    def __init__(self): self.root = {}
    def insert(self, w):
        node = self.root
        for ch in w: node = node.setdefault(ch, {})
        node["$"] = True
    def _find(self, t):
        node = self.root
        for ch in t:
            node = node.get(ch)
            if node is None: return None
        return node
    def search(self, w):
        node = self._find(w)
        return node is not None and "$" in node
    def starts_with(self, p): return self._find(p) is not None
def _bulk(cls_, n):
    rng, t, hits = _random.Random(n), cls_(), 0
    words = ["".join(rng.choice("abcdef") for _ in range(rng.randint(2, 8))) for _ in range(n)]
    for w in words:
        t.insert(w)
    for w in words:
        q = w[:rng.randint(1, len(w))] + rng.choice(["", "a", "z"])
        hits += bool(t.starts_with(q)) + 2 * bool(t.search(q))
    return hits
speed(lambda n: _bulk(cls, n), lambda n: n, lambda n: _bulk(_Ref, n), sizes=(1_000, 5_000, 30_000), what="words", factor=10,
      tip="Don't loop over all the stored words in search or starts_with. Walk down from the root one character at a time.")
```
```python solution
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()      # create the path as needed
            node = node.children[ch]
        node.is_word = True                         # mark the end of a complete word

    def _find(self, text):
        node = self.root
        for ch in text:
            node = node.children.get(ch)
            if node is None:
                return None                         # the path breaks off: no such prefix
        return node

    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_word

    def starts_with(self, prefix):
        return self._find(prefix) is not None

t = Trie()
t.insert("apple")
print(t.search("apple"), t.search("app"), t.starts_with("app"))
t.insert("app")
print(t.search("app"))
```
```python slow
class Trie:
    def __init__(self):
        self.words = []

    def insert(self, word):
        self.words.append(word)

    def search(self, word):
        return word in self.words

    def starts_with(self, prefix):
        return any(w.startswith(prefix) for w in self.words)
```
hint: Each node needs two things: its children (one per possible next character) and whether a word ends at it.
hint: Use a small `TrieNode` class with `children = {}` and `is_word = False`. `insert` walks the word, creating missing children, and sets `is_word = True` at the last node.
hint: Write one helper that follows a string from the root and returns the node it reaches (or None if a character is missing). `search` needs that node **and** `is_word`; `starts_with` only needs the node to exist.
approach:
1. **Understand:** `search` is exact; `starts_with` asks about any stored word; the empty prefix gives True, because the walk never leaves the root.
2. **Examples:** after inserting "apple": search("app") → False, starts_with("app") → True.
3. **Brute force:** store words in a list and scan it: O(n · L) per query.
4. **Pattern:** **trie**: shared prefixes share nodes.
5. **Plan:** `TrieNode(children, is_word)`; insert creates the path; a `_find` helper serves both queries.
6. **Code and test:** a prefix that isn't a word, the empty trie, inserting twice.
walkthrough:
**Line by line**

- `self.root` is an empty node standing for the empty string.
- `insert` follows the word, creating any missing child, so words with a common prefix reuse the same nodes.
- `node.is_word = True` is what makes "app" different from "apple"'s first three letters.
- `_find` returns None as soon as the path breaks, so failed lookups stop early.
- `search` requires the end flag; `starts_with` only needs the path.

**Trace** of the example:

| operation | path walked | result |
|---|---|---|
| insert "apple" | creates a → p → p → l → e; marks e | — |
| search "apple" | a p p l e, e is marked | True |
| search "app" | a p p, the second p isn't marked | False |
| starts_with "app" | a p p exists | True |
| insert "app" | reuses a → p → p; marks the second p | — |
| search "app" | now marked | True |

**Complexity:** O(L) per operation; space O(total characters inserted) in the worst case.

**Common wrong approach:** having `search` return True whenever the path exists, so every prefix of a word counts as a word.
:::

:::exercise Search suggestions
Write `suggestions(words, queries)`. For each query string, return a list of up to **3** words from `words` that start with it, the alphabetically smallest ones, in alphabetical order (an empty list if none match). `words` has no duplicates. Return one list per query. With 20,000 words and 20,000 queries this must take well under a second, so don't scan every word for every query.
```python starter
def suggestions(words, queries):
    pass

print(suggestions(["mobile", "mouse", "moneypot", "monitor", "mousepad"], ["m", "mou", "mon", "x"]))
# [['mobile', 'moneypot', 'monitor'], ['mouse', 'mousepad'], ['moneypot', 'monitor'], []]
```
```python check
fn = need("suggestions")
test(fn, cases=[
    ((["mobile", "mouse", "moneypot", "monitor", "mousepad"], ["m", "mou", "mon", "x"]),
     [["mobile", "moneypot", "monitor"], ["mouse", "mousepad"], ["moneypot", "monitor"], []], "the example"),
    ((["havana"], ["h", "havana", "havanas", "a"]), [["havana"], ["havana"], [], []], "one word, the whole word, and longer than it"),
    ((["a", "ab", "abc", "abd", "b"], ["a", "ab", "abc"]), [["a", "ab", "abc"], ["ab", "abc", "abd"], ["abc"]], "a word that is a prefix of others"),
    ((["bags", "baggage", "banner", "box", "cloths"], ["b", "bag", "bags", "c"]),
     [["baggage", "bags", "banner"], ["baggage", "bags"], ["bags"], ["cloths"]], "unsorted input"),
    (([], ["a"]), [[]], "no words"),
])
import random as _random, bisect as _bisect
def _make(n):
    rng, s = _random.Random(n), set()
    while len(s) < n:
        s.add("".join(rng.choice("abcdefgh") for _ in range(rng.randint(3, 9))))
    words = sorted(s)
    rng.shuffle(words)
    return words, [w[:rng.randint(1, 4)] for w in rng.sample(words, n)]
def _ref(words, queries):
    w, out = sorted(words), []
    for q in queries:
        i = _bisect.bisect_left(w, q)
        out.append([x for x in w[i:i + 3] if x.startswith(q)])
    return out
speed(fn, _make, _ref, sizes=(1_000, 5_000, 20_000), what="words and queries",
      tip="Scanning every word for every query is O(n) per query. Build a trie once (or sort the words and use bisect_left to jump to the first match).")
```
```python solution
def suggestions(words, queries):
    root = {}
    for w in words:                          # build a trie; "$" holds the word that ends at a node
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w

    result = []
    for q in queries:
        node = root
        for ch in q:                         # walk down to the prefix
            node = node.get(ch)
            if node is None:
                break
        found = []
        if node is not None:
            stack = [node]                   # depth-first, smallest letter first
            while stack and len(found) < 3:
                cur = stack.pop()
                if "$" in cur:
                    found.append(cur["$"])   # a word here comes before longer words below it
                for ch in sorted((k for k in cur if k != "$"), reverse=True):
                    stack.append(cur[ch])    # pushed in reverse so "a" is popped first
        result.append(found)
    return result

print(suggestions(["mobile", "mouse", "moneypot", "monitor", "mousepad"], ["m", "mou", "mon", "x"]))
```
```python slow
def suggestions(words, queries):
    ordered = sorted(words)
    return [[w for w in ordered if w.startswith(q)][:3] for q in queries]
```
hint: Checking every word against every query is n × q work. Which structure answers "which words start with this prefix?" by walking only the prefix?
hint: Build a trie of all the words once. For a query, walk down to its node; the matching words are exactly the words in that node's subtree.
hint: From the prefix node, do a depth-first search visiting children in alphabetical order, and stop after collecting 3 words. A node's own word comes before the words below it. (Alternative: sort the words, `bisect_left(words, q)`, and check the next 3.)
approach:
1. **Understand:** up to 3 matches per query, alphabetically smallest, in order; words are unsorted.
2. **Examples:** "mou" → ["mouse", "mousepad"]; "x" → [].
3. **Brute force:** sort once, then filter all words per query: O(n · q · L).
4. **Pattern:** **trie + ordered DFS** (or **sorting + binary search**: the matches for a prefix form one contiguous block of the sorted list).
5. **Plan:** build the trie; per query, walk the prefix, then DFS smallest-letter-first until 3 words are found.
6. **Code and test:** a query longer than any word, a word that is a prefix of others, no words.
walkthrough:
**Line by line**

- Storing the word itself under `"$"` saves rebuilding it from the path.
- The walk stops at the first missing character; `node` is then None and the answer is `[]`.
- The DFS uses a stack. Pushing children in reverse alphabetical order means the smallest letter is popped first, so words come out alphabetically: a node's own word ("mouse") before its extensions ("mousepad").
- `len(found) < 3` stops the search early, so each query does only a little work beyond its prefix.

**Trace** for "mo" on the example words: the DFS from the "mo" node visits b → "mobile", then n → e → "moneypot", then n → i → "monitor": 3 found, stop.

**Complexity:** building is O(total characters); each query is O(L + the nodes visited before finding 3 words). The sort-and-bisect alternative is O(n log n) to sort, then O(L log n) per query.

**Common wrong approach:** collecting **all** matching words below the prefix and sorting them, which for a short prefix like "a" means visiting most of the trie on every query.
:::

:::quiz
? Searching a trie for a word of length L takes:
+ O(L), however many words are stored
- O(n), where n is the number of words
- O(log n)
= Each step follows one character.
? A trie contains "apple". Why does search("app") return False?
+ No word is marked as ending at the second "p"
- "app" is too short
- Tries can't store prefixes
= The path exists, but the end-of-word flag isn't set there.
? Which problem is a trie especially good at?
+ Finding all words with a given prefix
- Finding the largest number
- Sorting numbers
= Every word with the prefix lies in the subtree below the prefix's node.
? What is the main downside of a trie compared with a set of strings?
+ Memory: a node (with its own dict) for every character
- Exact lookups are impossible
- It can't store more than 26 words
= Radix trees compress chains of single-child nodes to save space.
:::

@@@ lesson
id: segment-fenwick
title: Segment trees and Fenwick trees
minutes: 28
summary: Range queries on data that changes: why prefix sums aren't enough, Fenwick (binary indexed) trees with the lowest-set-bit trick, segment trees for sums, minimums and any combinable operation, lazy propagation for range updates, and sparse tables for static minimums.
---
Prefix sums (Lesson 9) answer "sum of nums[l..r]" in O(1), but only while the data **doesn't change**: updating one item means rebuilding O(n) prefix sums. A plain list has the opposite problem: O(1) updates, O(n) sums. When there are **many updates and many queries**, both are too slow. Trees that store sums of **blocks** of the list give O(log n) for both.

| Approach | Update one item | Sum of a range | Notes |
|---|---|---|---|
| Plain list | O(1) | O(n) | |
| Prefix sums | O(n) | O(1) | best when nothing changes |
| Square-root decomposition | O(1) | O(√n) | blocks of √n items with stored sums |
| **Fenwick tree** (binary indexed tree) | O(log n) | O(log n) | short code; sums and other invertible operations |
| **Segment tree** | O(log n) | O(log n) | any combinable operation (min, max, gcd); range updates with lazy propagation |

### Fenwick tree (binary indexed tree)

A **Fenwick tree** is a list `tree[1..n]` (1-indexed) where `tree[i]` holds the sum of a block of items **ending at position i**, whose length is the **lowest set bit** of i: `i & -i`. Position 6 (binary 110) covers 2 items, 5 and 6; position 8 (1000) covers 8 items, 1 to 8; odd positions cover just themselves.

![Positions 1 to 8 of [5, 8, 6, 3, 2, 7, 2, 6] with a bar for each Fenwick cell showing the range it sums: tree[1] = 5 (item 1), tree[2] = 13 (items 1–2), tree[3] = 6, tree[4] = 22 (items 1–4), tree[5] = 2, tree[6] = 9 (items 5–6), tree[7] = 2, tree[8] = 39 (items 1–8). The prefix sum of the first 7 items is tree[7] + tree[6] + tree[4] = 2 + 9 + 22 = 33](figures/fenwick.svg)

- **Prefix sum of the first i items:** add `tree[i]`, then jump to `i - (i & -i)` (drop the lowest bit) until i is 0. At most log₂ n jumps.
- **Update position i by delta:** add delta to `tree[i]`, then jump to `i + (i & -i)`, the next block that also contains position i.

`i & -i` works because in two's complement, `-i` flips every bit above the lowest 1, so the AND keeps only that bit:

| i | binary | i & -i | tree[i] covers |
|---|---|---|---|
| 6 | 110 | 2 (010) | items 5–6 |
| 7 | 111 | 1 (001) | item 7 |
| 8 | 1000 | 8 (1000) | items 1–8 |
| 12 | 1100 | 4 (0100) | items 9–12 |

```python
class Fenwick:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] + list(nums)              # 1-indexed; position 0 is unused
        for i in range(1, self.n + 1):            # O(n) build: push each block's sum to its parent block
            j = i + (i & -i)
            if j <= self.n:
                self.tree[j] += self.tree[i]

    def add(self, i, delta):                      # i is a 0-based index into nums
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix(self, i):                          # sum of the first i items
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total

    def range_sum(self, l, r):                    # sum of nums[l..r], inclusive, 0-based
        return self.prefix(r + 1) - self.prefix(l)

nums = [5, 8, 6, 3, 2, 7, 2, 6]
f = Fenwick(nums)
print("tree:", f.tree[1:])
print("first 7:", f.prefix(7), "| nums[2..6]:", f.range_sum(2, 6))
f.add(3, 10)                                      # nums[3] goes from 3 to 13
print("after the update, nums[2..6]:", f.range_sum(2, 6))
```

To **set** an item to a new value, add the difference (new − old), keeping a copy of the values to know the old one.

### Segment tree

A **segment tree** is a binary tree over the list: each leaf is one item, and each internal node stores the combined value (sum, min, max…) of the range below it. A range query combines the few nodes that exactly cover the range, **at most about 2 per level**: O(log n).

![A segment tree for [5, 8, 6, 3, 2, 7, 2, 6]. The root holds 39 for range 0–7; its children hold 22 (0–3) and 17 (4–7); then 13, 9, 9, 8; then the eight leaves. For the query sum of indexes 2 to 6, the three highlighted nodes 9 (2–3), 9 (4–5) and 2 (6) add up to 20](figures/segment-tree.svg)

The neatest way to code it stores the tree in a list of size 2n: the leaves at `t[n..2n-1]`, and each internal node `t[i]` combining `t[2i]` and `t[2i+1]`. Passing in the combining function makes one class work for sums, minimums, maximums or gcds:

```python
from math import gcd

class SegmentTree:
    def __init__(self, nums, combine, identity):
        self.n = n = len(nums)
        self.f, self.e = combine, identity       # identity: f(e, x) == x, e.g. 0 for sums, inf for min
        self.t = [identity] * n + list(nums)
        for i in range(n - 1, 0, -1):
            self.t[i] = combine(self.t[2 * i], self.t[2 * i + 1])

    def update(self, i, value):                   # set nums[i] = value
        i += self.n
        self.t[i] = value
        while i > 1:
            i //= 2
            self.t[i] = self.f(self.t[2 * i], self.t[2 * i + 1])

    def query(self, l, r):                        # combine nums[l..r], inclusive
        left = right = self.e
        l += self.n
        r += self.n + 1
        while l < r:
            if l & 1:                             # l is a right child: take it, step past it
                left = self.f(left, self.t[l])
                l += 1
            if r & 1:
                r -= 1
                right = self.f(self.t[r], right)
            l //= 2
            r //= 2
        return self.f(left, right)

nums = [5, 8, 6, 3, 2, 7, 2, 6]
sums = SegmentTree(nums, lambda a, b: a + b, 0)
mins = SegmentTree(nums, min, float("inf"))
gcds = SegmentTree([12, 18, 24, 9, 30], gcd, 0)
print(sums.query(2, 6), mins.query(0, 3), mins.query(4, 7), gcds.query(0, 2))
mins.update(5, 1)
print("min of 4..7 after setting index 5 to 1:", mins.query(4, 7))
```

Unlike the Fenwick tree, a segment tree doesn't need an inverse operation (there's no "un-min"), which is why it handles minimums and maximums.

### Lazy propagation: updating a whole range

"Add 5 to every item from l to r" would touch O(n) leaves. **Lazy propagation** stops at the O(log n) nodes that cover the range, updates their totals, and leaves a **pending** note for their children, which is passed down (pushed) only when a later operation needs to go below that node.

```python
class LazySegmentTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.sum = [0] * (4 * self.n)
        self.pending = [0] * (4 * self.n)        # amount still to add to every item below this node
        self._build(1, 0, self.n - 1, nums)

    def _build(self, x, lo, hi, nums):
        if lo == hi:
            self.sum[x] = nums[lo]
            return
        mid = (lo + hi) // 2
        self._build(2 * x, lo, mid, nums)
        self._build(2 * x + 1, mid + 1, hi, nums)
        self.sum[x] = self.sum[2 * x] + self.sum[2 * x + 1]

    def _apply(self, x, lo, hi, v):              # add v to every item of this node's range
        self.sum[x] += v * (hi - lo + 1)
        self.pending[x] += v

    def _push(self, x, lo, hi):                  # hand the pending note down to the children
        if self.pending[x]:
            mid = (lo + hi) // 2
            self._apply(2 * x, lo, mid, self.pending[x])
            self._apply(2 * x + 1, mid + 1, hi, self.pending[x])
            self.pending[x] = 0

    def range_add(self, l, r, v, x=1, lo=0, hi=None):
        hi = self.n - 1 if hi is None else hi
        if r < lo or hi < l:
            return                               # no overlap
        if l <= lo and hi <= r:
            self._apply(x, lo, hi, v)            # fully covered: stop here, lazily
            return
        self._push(x, lo, hi)
        mid = (lo + hi) // 2
        self.range_add(l, r, v, 2 * x, lo, mid)
        self.range_add(l, r, v, 2 * x + 1, mid + 1, hi)
        self.sum[x] = self.sum[2 * x] + self.sum[2 * x + 1]

    def range_sum(self, l, r, x=1, lo=0, hi=None):
        hi = self.n - 1 if hi is None else hi
        if r < lo or hi < l:
            return 0
        if l <= lo and hi <= r:
            return self.sum[x]
        self._push(x, lo, hi)
        mid = (lo + hi) // 2
        return self.range_sum(l, r, 2 * x, lo, mid) + self.range_sum(l, r, 2 * x + 1, mid + 1, hi)

st = LazySegmentTree([5, 8, 6, 3, 2, 7, 2, 6])
print(st.range_sum(0, 7))
st.range_add(2, 5, 10)                           # add 10 to indexes 2, 3, 4, 5
print(st.range_sum(0, 7), st.range_sum(3, 3), st.range_sum(6, 7))
```

Both `range_add` and `range_sum` are O(log n). The 4n size is a safe upper bound on the number of nodes for any n.

### Sparse table: O(1) minimums on data that never changes

If the list is fixed and you need range **minimums** (or maximums), precompute the minimum of every block whose length is a power of two. Any range is covered by **two overlapping** such blocks, and overlap doesn't matter for min. O(n log n) to build, **O(1)** per query.

```python
def build_sparse(nums):
    table = [nums[:]]                                # table[j][i] = min of nums[i : i + 2**j]
    j = 1
    while (1 << j) <= len(nums):
        prev, half = table[-1], 1 << (j - 1)
        table.append([min(prev[i], prev[i + half]) for i in range(len(nums) - (1 << j) + 1)])
        j += 1
    return table

def range_min(table, l, r):
    j = (r - l + 1).bit_length() - 1                 # largest power of two that fits in the range
    return min(table[j][l], table[j][r - (1 << j) + 1])

table = build_sparse([5, 8, 6, 3, 2, 7, 2, 6])
print(range_min(table, 0, 2), range_min(table, 1, 4), range_min(table, 5, 7))
```

This trick doesn't work for sums, because overlapping blocks would count items twice.

### Choosing a range-query structure

| Situation | Use |
|---|---|
| Sums, data never changes | prefix sums: O(1) query |
| Min / max, data never changes | sparse table: O(1) query |
| Sums with single-item updates | Fenwick tree (short) or segment tree |
| Min / max / gcd with updates | segment tree |
| Updates to whole ranges | segment tree with lazy propagation (or a Fenwick tree over differences, for range-add / point-query) |
| Counting how many earlier values are smaller (inversions, rankings) | Fenwick tree over value ranks |

When values are huge or negative but there are only n of them, replace each value by its **rank** in sorted order first (**coordinate compression**), so the tree has n positions instead of one per possible value.

:::exercise Range sums with updates
Complete `NumArray(nums)` with `update(i, val)` (set `nums[i] = val`) and `sum_range(l, r)` (the sum of `nums[l..r]`, inclusive). Both must be O(log n): 100,000 mixed operations on 100,000 numbers should take about a second at most.
```python starter
class NumArray:
    def __init__(self, nums):
        pass

    def update(self, i, val):
        pass

    def sum_range(self, l, r):
        pass

a = NumArray([1, 3, 5])
print(a.sum_range(0, 2))   # 9
a.update(1, 2)
print(a.sum_range(0, 2))   # 8
```
```python check
cls = need("NumArray")
def _ops(nums, ops):
    a, out = cls(list(nums)), []
    for op in ops:
        if op[0] == "update":
            a.update(op[1], op[2]); out.append(None)
        else:
            out.append(a.sum_range(op[1], op[2]))
    return out
test(_ops, show="NumArray({0}) with operations {1}", cases=[
    (([1, 3, 5], [("sum", 0, 2), ("update", 1, 2), ("sum", 0, 2)]), [9, None, 8], "the example"),
    (([7], [("sum", 0, 0), ("update", 0, -3), ("sum", 0, 0)]), [7, None, -3], "a single number"),
    (([5, 8, 6, 3, 2, 7, 2, 6], [("sum", 2, 6), ("sum", 0, 7), ("sum", 4, 4), ("update", 3, 13), ("sum", 2, 6), ("sum", 0, 3)]),
     [20, 39, 2, None, 30, 32], "several ranges and an update"),
    (([0, 0, 0, 0], [("update", 0, 1), ("update", 3, 4), ("update", 0, 2), ("sum", 0, 3), ("sum", 1, 2)]), [None, None, None, 6, 0], "updating the same index twice"),
    (([-2, 0, 3, -5, 2, -1], [("sum", 0, 2), ("sum", 2, 5), ("sum", 0, 5)]), [1, -1, -3], "negative numbers"),
])
import random as _random
class _Ref:
    def __init__(self, nums):
        self.n, self.v, self.t = len(nums), list(nums), [0] + list(nums)
        for i in range(1, self.n + 1):
            j = i + (i & -i)
            if j <= self.n: self.t[j] += self.t[i]
    def update(self, i, val):
        d, self.v[i] = val - self.v[i], val
        i += 1
        while i <= self.n:
            self.t[i] += d; i += i & -i
    def _p(self, i):
        s = 0
        while i > 0:
            s += self.t[i]; i -= i & -i
        return s
    def sum_range(self, l, r): return self._p(r + 1) - self._p(l)
def _bulk(cls_, n):
    rng = _random.Random(n)
    a, total = cls_([rng.randint(-1000, 1000) for _ in range(n)]), 0
    for _ in range(n):
        if rng.random() < 0.25:
            a.update(rng.randrange(n), rng.randint(-1000, 1000))
        else:
            total += a.sum_range(rng.randrange(n // 10 + 1), n - 1 - rng.randrange(n // 10 + 1))
    return total
speed(lambda n: _bulk(cls, n), lambda n: n, lambda n: _bulk(_Ref, n), sizes=(1_000, 10_000, 100_000), what="numbers and operations",
      factor=8, tip="Summing a slice is O(n) per query, and rebuilding prefix sums is O(n) per update. A Fenwick tree or a segment tree makes both O(log n).")
```
```python solution
class NumArray:
    def __init__(self, nums):
        self.n = len(nums)
        self.nums = list(nums)                    # current values, to work out update differences
        self.tree = [0] + list(nums)              # Fenwick tree, 1-indexed
        for i in range(1, self.n + 1):
            j = i + (i & -i)                      # the next block that contains position i
            if j <= self.n:
                self.tree[j] += self.tree[i]

    def update(self, i, val):
        delta = val - self.nums[i]
        self.nums[i] = val
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i                           # move to the next block covering this position

    def _prefix(self, i):                         # sum of the first i numbers
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i                           # drop the lowest set bit
        return total

    def sum_range(self, l, r):
        return self._prefix(r + 1) - self._prefix(l)

a = NumArray([1, 3, 5])
print(a.sum_range(0, 2))
a.update(1, 2)
print(a.sum_range(0, 2))
```
```python slow
class NumArray:
    def __init__(self, nums):
        self.nums = list(nums)

    def update(self, i, val):
        self.nums[i] = val

    def sum_range(self, l, r):
        return sum(self.nums[l:r + 1])
```
hint: Summing a slice is O(n) per query; prefix sums make queries O(1) but updates O(n). You need something in between: O(log n) for both.
hint: A Fenwick tree stores sums of blocks whose lengths are powers of two. A prefix sum adds about log n blocks; an update changes about log n blocks. Remember an update **sets** a value, so add the difference `val - old`.
hint: Keep `self.nums` and a 1-indexed `self.tree`. Update: `i += 1`, then `while i <= n: tree[i] += delta; i += i & -i`. Prefix(i): `while i > 0: total += tree[i]; i -= i & -i`. `sum_range(l, r) = prefix(r + 1) - prefix(l)`.
approach:
1. **Understand:** point **set** updates (not add), inclusive range sums, many of both.
2. **Examples:** [1, 3, 5]: sum(0, 2) = 9; set index 1 to 2; sum(0, 2) = 8.
3. **Brute force:** slice and sum per query (O(n)), or rebuild prefix sums per update (O(n)).
4. **Pattern:** **Fenwick tree** (or segment tree) for point updates and range sums.
5. **Plan:** build in O(n); update by the difference; a range is the difference of two prefix sums.
6. **Code and test:** one number, the same index updated twice, negative numbers.
walkthrough:
**Line by line**

- `self.tree = [0] + list(nums)` puts each number at its 1-based position; the build loop then adds each block's total into the next larger block that contains it, so the tree is ready in O(n).
- `update` converts "set" into "add `delta`", then climbs with `i += i & -i` through every block containing position i.
- `_prefix(i)` walks down with `i -= i & -i`, adding disjoint blocks that together cover positions 1..i.
- `sum_range(l, r)` is prefix(r + 1) − prefix(l), the same subtraction as with ordinary prefix sums.

**Trace** on [1, 3, 5]: the tree after building is [_, 1, 4, 5] (tree[2] = 1 + 3).

| operation | steps | result |
|---|---|---|
| sum_range(0, 2) | prefix(3) = tree[3] + tree[2] = 5 + 4 = 9; prefix(0) = 0 | 9 |
| update(1, 2) | delta = −1; i = 2: tree[2] = 3; i = 4 > 3, stop | — |
| sum_range(0, 2) | prefix(3) = tree[3] + tree[2] = 5 + 3 = 8 | 8 |

**Complexity:** O(n) to build, O(log n) per update and per query, O(n) space.

**Common wrong approach:** treating `update(i, val)` as "add val" instead of "set to val", or mixing 0-based and 1-based indexes, which silently skips `tree[0]` or loops forever at i = 0.
:::

:::exercise Count smaller numbers to the right
Write `count_smaller(nums)` returning a list where item i is how many numbers **to the right** of `nums[i]` are strictly smaller than it. Aim for O(n log n): 50,000 numbers should take well under a second.
```python starter
def count_smaller(nums):
    pass

print(count_smaller([5, 2, 6, 1]))   # [2, 1, 1, 0]
```
```python check
fn = need("count_smaller")
test(fn, cases=[
    ([5, 2, 6, 1], [2, 1, 1, 0], "the example"),
    ([-1], [0], "a single number"),
    ([-1, -1], [0, 0], "equal numbers aren't smaller"),
    ([], [], "an empty list"),
    ([1, 2, 3, 4], [0, 0, 0, 0], "increasing"),
    ([4, 3, 2, 1], [3, 2, 1, 0], "decreasing"),
    ([2, 0, 1, 2, 0, -5, 10**9], [4, 1, 2, 2, 1, 0, 0], "duplicates, negatives and a huge value"),
])
import random as _random
def _make(n):
    rng = _random.Random(n)
    return [rng.randint(-10**4, 10**4) for _ in range(n)]
def _ref(nums):
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    m, tree, out = len(rank), [0] * (len(rank) + 1), [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):
        r, s = rank[nums[i]] - 1, 0
        while r > 0: s += tree[r]; r -= r & -r
        out[i], r = s, rank[nums[i]]
        while r <= m: tree[r] += 1; r += r & -r
    return out
speed(fn, _make, _ref, sizes=(500, 5_000, 50_000), what="numbers",
      tip="Comparing every pair is O(n^2). Walk from the right, keeping counts of the numbers seen so far in a Fenwick tree indexed by each value's rank.")
```
```python solution
def count_smaller(nums):
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}   # coordinate compression: values -> 1..m
    m = len(rank)
    tree = [0] * (m + 1)                       # Fenwick tree of counts per rank
    result = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):     # right to left: the tree holds everything to the right
        r = rank[nums[i]] - 1                  # count values with a smaller rank
        smaller = 0
        while r > 0:
            smaller += tree[r]
            r -= r & -r
        result[i] = smaller
        r = rank[nums[i]]                      # then record this value
        while r <= m:
            tree[r] += 1
            r += r & -r
    return result

print(count_smaller([5, 2, 6, 1]))
```
```python slow
def count_smaller(nums):
    result = []
    for i in range(len(nums)):
        result.append(sum(1 for j in range(i + 1, len(nums)) if nums[j] < nums[i]))
    return result
```
hint: Go from right to left. When you reach nums[i], everything to its right has already been seen. What question do you need to ask about those seen values?
hint: "How many seen values are smaller than x?" is a prefix sum over counts indexed by value. A Fenwick tree gives that in O(log n), with an O(log n) update to record x. Values can be negative or huge, so index by **rank** instead.
hint: `rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}`. Right to left: `result[i] = prefix(rank[x] - 1)`, then `add(rank[x], 1)`. (A merge sort that counts, like Lesson 22's inversions, also works.)
approach:
1. **Understand:** strictly smaller, only to the right; duplicates and negatives allowed.
2. **Examples:** [5, 2, 6, 1] → [2, 1, 1, 0].
3. **Brute force:** for each i, scan everything to its right: O(n²).
4. **Pattern:** **Fenwick tree over ranks** (coordinate compression), scanning right to left. Merge sort with counting is the other O(n log n) way.
5. **Plan:** compress values to 1..m; for each item from the right, query the count of smaller ranks, then add the item.
6. **Code and test:** duplicates, decreasing order, a huge value, empty input.
walkthrough:
**Line by line**

- `sorted(set(nums))` lists the distinct values in order; each gets a rank from 1 to m, so the tree has at most n positions however big the values are.
- Scanning right to left, the tree contains exactly the numbers to the right of i.
- `prefix(rank - 1)` counts values with a smaller rank: strictly smaller values (equal values share a rank, so they're excluded).
- Adding 1 at `rank[x]` records x for the items further left.

**Trace** on [5, 2, 6, 1] (ranks: 1 → 1, 2 → 2, 5 → 3, 6 → 4):

| i | value (rank) | seen so far | smaller | result[i] |
|---|---|---|---|---|
| 3 | 1 (1) | — | count of ranks < 1 | 0 |
| 2 | 6 (4) | 1 | ranks < 4: {1} | 1 |
| 1 | 2 (2) | 1, 6 | ranks < 2: {1} | 1 |
| 0 | 5 (3) | 1, 6, 2 | ranks < 3: {1, 2} | 2 |

**Complexity:** O(n log n) time (sorting plus n Fenwick operations), O(n) space.

**Common wrong approach:** sizing the Fenwick tree by the largest value (10⁹ cells) instead of by rank, or counting `prefix(rank)`, which includes equal values.
:::

:::quiz
? What does `i & -i` give?
+ The lowest set bit of i, which is the length of the block tree[i] covers
- i rounded down to a power of two
- The highest set bit of i
= For i = 12 (1100), i & -i = 4 (0100): tree[12] covers items 9–12.
? Why can't a Fenwick tree easily answer range minimums?
+ A range is found by subtracting two prefixes, and minimum has no "subtract"
- Fenwick trees only store positive numbers
- Minimums need O(n) memory
= Segment trees combine covering nodes directly, so they handle min, max and gcd.
? What does lazy propagation make fast?
+ Updating every item in a range, in O(log n)
- Building the tree in O(1)
- Sorting the array
= Fully covered nodes store a pending update instead of touching every leaf.
? The data never changes and you need many range-minimum queries. What's fastest per query?
+ A sparse table: O(1) per query after O(n log n) preprocessing
- A Fenwick tree
- Scanning the range each time
= Two overlapping power-of-two blocks cover any range; overlap doesn't affect a minimum.
:::
