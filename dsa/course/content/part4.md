@@@ part
id: 4
title: Linked Lists, Stacks and Queues
level: Beginner
blurb: Structures built from links and rules: linked lists and their pointer tricks, stacks (last in, first out), queues and deques (first in, first out), monotonic stacks, and how to design an LRU cache.

@@@ lesson
id: linked-lists
title: Linked lists
minutes: 20
summary: Nodes joined by pointers: singly, doubly and circular linked lists, their operations and costs, and how they compare with Python lists.
---
A Python list keeps its items side by side in memory, so jumping to item 1,000 is instant, but inserting at the front shifts every item. A **linked list** makes the opposite trade. Each item lives in its own **node**, and each node holds a **pointer** (a reference) to the next one. The list itself only remembers the first node, the **head**.

![A singly linked list: head points to a node holding 3, which points to 7, then 1, then 9, whose next is None. Below, inserting 5 at the front only creates one node and changes one pointer](figures/linked-list.svg)

### A node, and walking the list

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next          # the next node, or None at the end

# build 3 -> 7 -> 1 -> 9 by hand
head = ListNode(3, ListNode(7, ListNode(1, ListNode(9))))

node = head
while node:                       # stop when we fall off the end (None)
    print(node.val, end=" -> ")
    node = node.next
print("None")
```

**Traversal** is the basic move of every linked-list algorithm: start at the head and follow `next` until `None`. Reaching item *i* takes *i* steps, so access by position is **O(n)**, not O(1).

Two helpers you'll use in every exercise turn Python lists into linked lists and back:

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def build(values):
    dummy = ListNode(0)                 # a placeholder before the real head
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

head = build([4, 8, 15, 16])
print(to_list(head), "head value:", head.val)
```

### The operations and their costs

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None                # keeping a tail makes append O(1)
        self.size = 0

    def push_front(self, val):          # O(1): new node points at the old head
        self.head = ListNode(val, self.head)
        if self.tail is None:
            self.tail = self.head
        self.size += 1

    def append(self, val):              # O(1) thanks to the tail pointer
        node = ListNode(val)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def find(self, val):                # O(n): walk until found
        node = self.head
        while node and node.val != val:
            node = node.next
        return node

    def delete(self, val):              # O(n) to find it, O(1) to unlink it
        dummy = ListNode(0, self.head)
        prev = dummy
        while prev.next and prev.next.val != val:
            prev = prev.next
        if prev.next:                   # found: skip over it
            if prev.next is self.tail:
                self.tail = prev if prev is not dummy else None
            prev.next = prev.next.next
            self.size -= 1
        self.head = dummy.next

    def __iter__(self):
        node = self.head
        while node:
            yield node.val
            node = node.next

ll = LinkedList()
for x in [7, 1, 9]:
    ll.append(x)
ll.push_front(3)
ll.delete(1)
print(list(ll), "size", ll.size, "tail", ll.tail.val)
```

| Operation | Linked list | Python list (array) |
|---|---|---|
| Access item *i* | O(n): walk from the head | **O(1)** |
| Insert / delete at the front | **O(1)** | O(n): everything shifts |
| Insert / delete after a node you already hold | **O(1)** | O(n) |
| Append at the end | O(1) with a tail pointer | O(1) amortised |
| Search for a value | O(n) | O(n) |
| Extra memory | one pointer per node | none (plus spare capacity) |

**The dummy (sentinel) node trick:** a placeholder node in front of the head means "delete the head" is no longer a special case. You'll see it in almost every linked-list solution; return `dummy.next` at the end.

### Doubly linked lists

Each node also points **back** (`prev`). Now, given a node, you can remove it in O(1) without searching for the node before it, and you can walk in both directions. The price is one more pointer per node and more pointers to keep correct.

![A doubly linked list between a head sentinel and a tail sentinel: every node has a next arrow to the right and a prev arrow to the left. Removing the middle node reconnects its neighbours to each other](figures/doubly-linked.svg)

```python
class DNode:
    def __init__(self, val):
        self.val, self.prev, self.next = val, None, None

class DoublyLinkedList:
    def __init__(self):
        self.head, self.tail = DNode(None), DNode(None)    # two sentinels
        self.head.next, self.tail.prev = self.tail, self.head

    def add_last(self, val):                               # O(1)
        node = DNode(val)
        node.prev, node.next = self.tail.prev, self.tail
        self.tail.prev.next = node
        self.tail.prev = node
        return node

    def remove(self, node):                                # O(1): no search needed
        node.prev.next = node.next
        node.next.prev = node.prev

    def values(self):
        out, node = [], self.head.next
        while node is not self.tail:
            out.append(node.val)
            node = node.next
        return out

d = DoublyLinkedList()
a, b, c = d.add_last("a"), d.add_last("b"), d.add_last("c")
d.remove(b)
print(d.values())
```

Doubly linked lists power the LRU cache (Lesson 20), browser history and text editors' undo lists. Python's `collections.deque` is built from linked blocks for the same reason: O(1) at both ends.

### Circular linked lists

The last node points back to the first instead of to `None`. Useful for things that go round and round: players taking turns, a round-robin scheduler, a playlist on repeat. Be careful: a plain `while node:` loop never ends on a circle, so stop when you're back at the start.

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

# players 1..5 in a circle; every 2nd player is out (the Josephus problem)
first = ListNode(1)
node = first
for v in range(2, 6):
    node.next = ListNode(v)
    node = node.next
node.next = first                        # close the circle

prev, cur, out = node, first, []
while cur.next is not cur:               # until one player is left
    prev, cur = cur, cur.next            # skip one player
    out.append(cur.val)                  # this one is out
    prev.next = cur.next                 # unlink it: O(1)
    cur = cur.next
print("out in order:", out, " winner:", cur.val)
```

### When to use a linked list

In Python you'll rarely build one for real work: lists and `deque` are faster in practice because of how memory caches work. But linked lists matter because:

- they're the classic interview topic for **pointer manipulation**;
- they're the building block of other structures (stacks, queues, hash-table chains, LRU caches, adjacency lists for graphs);
- they're what you'd use in a lower-level language when you need O(1) inserts and deletes in the middle of a sequence you're already walking through.

:::exercise Remove every copy
Write `remove_value(head, val)` that removes **every** node whose value equals `val` and returns the new head (which may be `None`). The `ListNode` class and the `build` / `to_list` helpers are in the starter.
```python starter
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def build(values):
    dummy = ListNode(0)
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def remove_value(head, val):
    pass

print(to_list(remove_value(build([1, 2, 6, 3, 6]), 6)))
```
```python check
fn = need("remove_value")
def _run(values, val):
    return to_list(fn(build(values), val))
test(_run, [
    (([1, 2, 6, 3, 4, 5, 6], 6), [1, 2, 3, 4, 5], "the example"),
    (([7, 7, 7, 7], 7), [], "every node is removed"),
    (([7, 1, 2], 7), [1, 2], "the head itself is removed"),
    (([1, 2, 7], 7), [1, 2], "the last node is removed"),
    (([1, 7, 7, 2], 7), [1, 2], "two in a row"),
    (([], 1), [], "an empty list (head is None)"),
    (([1, 2, 3], 9), [1, 2, 3], "nothing to remove"),
])
```
```python solution
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def build(values):
    dummy = ListNode(0)
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def remove_value(head, val):
    dummy = ListNode(0, head)        # sentinel: the head is no longer a special case
    prev = dummy
    while prev.next:
        if prev.next.val == val:
            prev.next = prev.next.next   # unlink; don't move prev (the next one may match too)
        else:
            prev = prev.next
    return dummy.next

print(to_list(remove_value(build([1, 2, 6, 3, 6]), 6)))
```
hint: Removing a node means making the node **before** it skip over it. What if the node to remove is the head, which has nothing before it?
hint: Put a dummy node in front of the head, then walk with a `prev` pointer and look at `prev.next`.
hint: If `prev.next.val == val`, set `prev.next = prev.next.next` and **stay** (the new `prev.next` might match too); otherwise move `prev` forward. Return `dummy.next`.
approach:
1. **Understand:** remove all matches, keep the order of the rest, return the (possibly new) head.
2. **Examples:** [1, 2, 6, 3, 6], 6 → [1, 2, 3]. [7, 7], 7 → [] (head becomes None). [] → [].
3. **Brute force:** copy the values into a Python list, filter, rebuild: O(n) time but O(n) extra space, and it dodges the pointer skill being practised.
4. **Pattern:** **dummy head + prev pointer**: unlink a node by changing the pointer of the node before it.
5. **Plan:** dummy → head; prev = dummy; while prev.next: skip it if it matches, else advance; return dummy.next.
6. **Code and test:** test a match at the head, at the tail, two in a row, and an empty list.
walkthrough:
**Line by line**

- `dummy = ListNode(0, head)` puts a node in front of the real head, so removing the head works exactly like removing any other node.
- `prev` always points to the last node we've decided to **keep**; we look one step ahead at `prev.next`.
- On a match, `prev.next = prev.next.next` unlinks the node. We don't move `prev`, because the new `prev.next` hasn't been checked yet: that's what handles `7, 7` in a row.
- Otherwise the next node stays, so `prev` moves onto it.
- `dummy.next` is the new head, which may be `None` if everything was removed.

**Trace** on 7 → 1 → 7 → 2, removing 7:

| prev | prev.next | action | list after |
|---|---|---|---|
| dummy | 7 | unlink | dummy → 1 → 7 → 2 |
| dummy | 1 | keep, move | dummy → 1 → 7 → 2 |
| 1 | 7 | unlink | dummy → 1 → 2 |
| 1 | 2 | keep, move | dummy → 1 → 2 |
| 2 | None | stop | return 1 → 2 |

**Complexity:** O(n) time (each node is looked at once), O(1) extra space.

**Common wrong approach:** moving `prev` forward after every removal skips the node right after a removed one, so `1, 7, 7, 2` leaves a 7 behind.
:::

:::exercise Insert into a sorted list
Write `insert_sorted(head, val)` that inserts a new node with `val` into a linked list already sorted in ascending order, keeps it sorted, and returns the head.
```python starter
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def build(values):
    dummy = ListNode(0)
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def insert_sorted(head, val):
    pass

print(to_list(insert_sorted(build([1, 3, 7]), 5)))
```
```python check
fn = need("insert_sorted")
def _run(values, val):
    return to_list(fn(build(values), val))
test(_run, [
    (([1, 3, 7], 5), [1, 3, 5, 7], "the middle"),
    (([3, 7], 1), [1, 3, 7], "a new smallest value (new head)"),
    (([3, 7], 9), [3, 7, 9], "a new largest value (end)"),
    (([], 4), [4], "an empty list"),
    (([2, 4, 4, 6], 4), [2, 4, 4, 4, 6], "a value already present"),
    (([5], 5), [5, 5], "one node, same value"),
])
```
```python solution
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def build(values):
    dummy = ListNode(0)
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def insert_sorted(head, val):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.val < val:   # find the last node smaller than val
        prev = prev.next
    prev.next = ListNode(val, prev.next)       # splice the new node in after it
    return dummy.next

print(to_list(insert_sorted(build([1, 3, 7]), 5)))
```
hint: The new node goes right after the last node whose value is smaller than `val`.
hint: Use a dummy node so "insert before the head" needs no special case. Walk `prev` while `prev.next.val < val`.
hint: Splice in one line: `prev.next = ListNode(val, prev.next)`. Return `dummy.next`.
approach:
1. **Understand:** keep ascending order; the new node may become the head or the tail; the list may be empty.
2. **Examples:** [1, 3, 7] + 5 → [1, 3, 5, 7]; [3, 7] + 1 → [1, 3, 7]; [] + 4 → [4].
3. **Brute force:** convert to a Python list, `bisect.insort`, rebuild: works, but O(n) extra space.
4. **Pattern:** **dummy head**, then walk to the insertion point and splice.
5. **Plan:** prev = dummy; move while the next value is smaller; link the new node between prev and prev.next.
6. **Code and test:** smallest, largest, empty, equal values.
walkthrough:
**Line by line**

- `dummy = ListNode(0, head)`: inserting before the head becomes "insert after dummy".
- The `while` stops at the last node with a value **smaller** than `val` (or at the dummy, or at the last node).
- `ListNode(val, prev.next)` creates the node already pointing at the rest of the list; assigning it to `prev.next` links it in. The order of these two steps matters: if you set `prev.next` first, you lose the rest of the list.

**Trace** inserting 5 into 1 → 3 → 7:

| prev | prev.next.val | < 5? | action |
|---|---|---|---|
| dummy | 1 | yes | move |
| 1 | 3 | yes | move |
| 3 | 7 | no | stop; link 3 → 5 → 7 |

**Complexity:** O(n) time in the worst case (walk to the end), O(1) extra space.

**Common wrong approach:** writing `prev.next = new` and then `new.next = prev.next`. By the second line `prev.next` already **is** the new node, so the node points to itself and the rest of the list is lost.
:::

:::quiz
? Why is reading the 1,000th item of a linked list slow?
+ You must follow 999 pointers from the head: O(n)
- Linked lists store items in random order
- Python checks every item for errors
= Nodes aren't side by side in memory, so there's no way to jump straight to position i.
? Which operation is O(1) for a linked list but O(n) for a Python list?
- Reading the last item
+ Inserting at the front
- Searching for a value
= A new head just points at the old head. A Python list must shift every item.
? What is a dummy (sentinel) node for?
+ It sits before the head so that changing the head needs no special case
- It marks the end of the list instead of None
- It stores the list's length
= With a dummy, every real node has a node before it, including the head. Return dummy.next.
? What does a doubly linked list let you do in O(1) that a singly linked list can't?
+ Remove a node you hold, without searching for the node before it
- Access any position directly
- Sort the list
= With prev pointers, the node already knows its neighbour on each side.
:::

@@@ lesson
id: linked-list-patterns
title: "Linked list patterns: reverse, fast and slow pointers, merge"
minutes: 22
summary: The pointer techniques behind most linked-list questions: reversing in place, the middle node and cycle detection with fast and slow pointers, merging sorted lists and a k-step gap.
---
Almost every linked-list question is a combination of four moves. Learn them as templates.

### 1. Reverse a list in place

Walk the list once, turning every `next` arrow around. You need three pointers: `prev` (the reversed part so far), `cur` (the node being turned) and `nxt` (saved so you don't lose the rest).

![Reversing 1 → 2 → 3 step by step. At each step, cur's next arrow is turned to point at prev, then prev and cur move one node right. At the end, prev is the new head: 3 → 2 → 1 → None](figures/reverse-list.svg)

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val, self.next = val, next

def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def reverse(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next      # 1. remember the rest
        cur.next = prev     # 2. turn the arrow around
        prev = cur          # 3. move both pointers one step
        cur = nxt
    return prev             # prev is the old tail = the new head

print(to_list(reverse(build([1, 2, 3, 4]))))
```

O(n) time, O(1) space. A recursive version exists (reverse the rest, then hook the current node on the end) but uses O(n) call-stack space and crashes past Python's recursion limit of about 1,000 nodes, so prefer the loop.

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val, self.next = val, next

def reverse_recursive(head):
    if head is None or head.next is None:
        return head                      # 0 or 1 node: already reversed
    new_head = reverse_recursive(head.next)
    head.next.next = head                # the node after me now points back at me
    head.next = None
    return new_head

head = ListNode(1, ListNode(2, ListNode(3)))
node = reverse_recursive(head)
print(node.val, node.next.val, node.next.next.val)
```

### 2. Fast and slow pointers

Two pointers start at the head; `slow` moves one step, `fast` moves two. When `fast` reaches the end, `slow` is in the **middle**:

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val, self.next = val, next

def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head

def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

print(middle(build([1, 2, 3, 4, 5])).val, middle(build([1, 2, 3, 4, 5, 6])).val)
```

(For an even length, this returns the second of the two middle nodes.)

**Cycle detection (Floyd's tortoise and hare).** If a list loops back on itself, a plain walk never ends. With fast and slow pointers, if there's a cycle, the fast one eventually laps the slow one and they meet; if there isn't, fast falls off the end. O(n) time and **O(1) space**, where a "visited" set would need O(n).

![A list 1 → 2 → 3 → 4 → 5 → 6 whose last node points back to 3, forming a loop. The slow pointer moves one step at a time and the fast pointer two; they meet inside the loop. Resetting one pointer to the head and moving both one step at a time makes them meet again at 3, the start of the cycle](figures/fast-slow.svg)

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val, self.next = val, next

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:                 # same node object, not just the same value
            return True
    return False

def cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:                 # they met inside the loop
            slow = head                  # restart one pointer from the head
            while slow is not fast:      # both move 1 step; they meet at the loop's start
                slow, fast = slow.next, fast.next
            return slow
    return None

nodes = [ListNode(v) for v in [1, 2, 3, 4, 5, 6]]
for a, b in zip(nodes, nodes[1:]):
    a.next = b
nodes[-1].next = nodes[2]                # 6 -> 3 makes a loop
print(has_cycle(nodes[0]), cycle_start(nodes[0]).val)
```

Why does restarting find the start? If the head is *a* steps before the loop and they meet *b* steps into the loop, the fast pointer travelled twice as far as the slow one; working that out shows *a* equals the distance from the meeting point forward to the loop's start (plus whole laps). So two pointers moving one step at a time from the head and from the meeting point arrive at the start together.

### 3. Merge two sorted lists

Like merging two sorted arrays (Lesson 7), but you **relink** existing nodes instead of copying values: O(n + m) time, O(1) extra space.

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val, self.next = val, next

def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def merge(a, b):
    dummy = tail = ListNode(0)
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b                  # attach whatever is left
    return dummy.next

print(to_list(merge(build([1, 4, 9]), build([2, 3, 10, 12]))))
```

### 4. A gap of k: remove the k-th node from the end

Move a `lead` pointer k steps ahead, then move `lead` and `trail` together. When `lead` falls off the end, `trail` is just before the node to remove. One pass, no length needed.

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val, self.next = val, next

def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def remove_kth_from_end(head, k):
    dummy = ListNode(0, head)
    lead = trail = dummy
    for _ in range(k):
        lead = lead.next
    while lead.next:
        lead, trail = lead.next, trail.next
    trail.next = trail.next.next
    return dummy.next

print(to_list(remove_kth_from_end(build([1, 2, 3, 4, 5]), 2)))
```

### Putting moves together: is the list a palindrome?

Find the middle (fast/slow), reverse the second half, compare the halves: O(n) time, O(1) space.

```python
class ListNode:
    def __init__(self, val, next=None):
        self.val, self.next = val, next

def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head

def is_palindrome(head):
    slow = fast = head
    while fast and fast.next:            # 1. find the middle
        slow, fast = slow.next, fast.next.next
    prev = None
    while slow:                          # 2. reverse the second half
        slow.next, prev, slow = prev, slow, slow.next
    left, right = head, prev
    while right:                         # 3. compare
        if left.val != right.val:
            return False
        left, right = left.next, right.next
    return True

print(is_palindrome(build([1, 2, 3, 2, 1])), is_palindrome(build([1, 2, 2, 3])))
```

:::exercise Reverse a linked list
Write `reverse_list(head)` that reverses the list **in place** (relink the nodes; don't create new ones) and returns the new head. It must handle 100,000 nodes, so use a loop, not recursion.
```python starter
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def reverse_list(head):
    pass

print(to_list(reverse_list(build([1, 2, 3, 4, 5]))))
```
```python check
fn = need("reverse_list")
def _run(values):
    head = build(values)
    ids = set()
    node = head
    while node:
        ids.add(id(node)); node = node.next
    new = fn(head)
    out, node = [], new
    while node:
        if id(node) not in ids:
            raise AssertionError("Reverse the existing nodes by changing their next pointers; don't create new nodes.")
        out.append(node.val); node = node.next
    return out
test(_run, [
    ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], "the example"),
    ([1, 2], [2, 1], "two nodes"),
    ([7], [7], "one node"),
    ([], [], "an empty list (head is None)"),
    ([1, 1, 2], [2, 1, 1], "repeated values"),
])
def _ref(values):
    return values[::-1]
speed(lambda values: to_list(fn(build(values))), lambda n: list(range(n)), lambda v: v[::-1],
      sizes=(1_000, 100_000), what="nodes", factor=200, floor=1.0,
      tip="Reverse with a loop and three pointers (prev, cur, nxt).")
```
```python solution
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next       # save the rest of the list
        cur.next = prev      # turn this node's arrow around
        prev, cur = cur, nxt # step forward
    return prev

print(to_list(reverse_list(build([1, 2, 3, 4, 5]))))
```
hint: As you walk forward, make each node point to the node **before** it. What do you need to remember so you don't lose the rest of the list?
hint: Keep three pointers: `prev` (starts as None), `cur` (starts at head) and `nxt` (saved before you change `cur.next`).
hint: Loop while `cur`: `nxt = cur.next; cur.next = prev; prev = cur; cur = nxt`. Return `prev`.
approach:
1. **Understand:** relink, don't copy; return the new head (the old tail); empty and one-node lists are valid.
2. **Examples:** 1→2→3 becomes 3→2→1; None stays None.
3. **Brute force:** read the values into a list and write them back reversed: O(n) extra space, and it changes values instead of links.
4. **Pattern:** **pointer reversal with prev / cur / next**.
5. **Plan:** prev = None, cur = head; while cur: save next, point cur back at prev, advance both; return prev.
6. **Code and test:** test empty, one node, two nodes.
walkthrough:
**Line by line**

- `prev = None`: the old head will become the last node, so it must end up pointing at `None`.
- `nxt = cur.next` must come first: the next line overwrites `cur.next`, and without the saved copy the rest of the list would be unreachable.
- `cur.next = prev` turns the arrow around.
- `prev, cur = cur, nxt` moves both pointers one node forward.
- When `cur` is `None`, `prev` is the last node we turned around: the new head.

**Trace** on 1 → 2 → 3:

| step | prev | cur | nxt | links after the step |
|---|---|---|---|---|
| 1 | None → 1 | 1 → 2 | 2 | 1 → None |
| 2 | 1 → 2 | 2 → 3 | 3 | 2 → 1 → None |
| 3 | 2 → 3 | 3 → None | None | 3 → 2 → 1 → None |

Return `prev` = 3.

**Complexity:** O(n) time, O(1) extra space.

**Common wrong approach:** the recursive version is elegant but uses one call-stack frame per node, so 100,000 nodes raise `RecursionError` in Python.
:::

:::exercise Detect a cycle
Write `has_cycle(head)` that returns `True` if following `next` pointers ever loops back to an earlier node, otherwise `False`. Aim for O(1) extra space (no set of visited nodes).
```python starter
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def has_cycle(head):
    pass
```
```python check
fn = need("has_cycle")
def _make(values, pos):
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos >= 0 and nodes:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None
def _run(values, pos):
    return fn(_make(values, pos))
test(_run, [
    (([3, 2, 0, -4], 1), True, "the last node links back to the second"),
    (([1, 2], 0), True, "two nodes in a loop"),
    (([1], 0), True, "one node pointing to itself"),
    (([1, 2, 3], -1), False, "no cycle"),
    (([1], -1), False, "one node, no cycle"),
    (([], -1), False, "an empty list"),
    (([5, 5, 5, 5], -1), False, "equal values but no cycle (compare nodes, not values)"),
])
if uses("set(") or uses("visited"):
    raise AssertionError("Correct, but try the O(1)-space version: a slow pointer (1 step) and a fast pointer (2 steps).")
```
```python solution
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:          # the fast pointer caught up from behind: there's a loop
            return True
    return False                  # fast reached the end: no loop
```
hint: Without a loop, a walk reaches `None`. With a loop, it goes round forever. How can two walkers tell the difference?
hint: Floyd's tortoise and hare: `slow` moves 1 step, `fast` moves 2. In a loop, fast catches slow; without one, fast hits the end.
hint: `while fast and fast.next:` move both, then `if slow is fast: return True`. After the loop, `return False`. Use `is` to compare nodes.
approach:
1. **Understand:** detect a loop in the links, not repeated values; O(1) space wanted.
2. **Examples:** 3→2→0→−4→(back to 2) → True; 1→2→3 → False; one node pointing at itself → True.
3. **Brute force:** remember every visited node in a set: O(n) time, O(n) space.
4. **Pattern:** **fast and slow pointers** (Floyd).
5. **Plan:** slow and fast start at head; while fast and fast.next exist, step them; meeting means a cycle; reaching the end means none.
6. **Code and test:** empty list, one node, a self-loop, equal values without a loop.
walkthrough:
**Line by line**

- Both pointers start at the head.
- `while fast and fast.next:` guards both steps of the fast pointer: if either is `None`, the list has an end, so there's no cycle.
- Each round, the gap between them grows by one node. Inside a loop of length L, the fast pointer gains one node per round, so it must land exactly on the slow one within L rounds.
- `slow is fast` compares **objects**. `slow.val == fast.val` would wrongly report a cycle for 5 → 5 → 5.

**Trace** on 3 → 2 → 0 → −4 → (back to 2):

| round | slow | fast | same node? |
|---|---|---|---|
| start | 3 | 3 | — |
| 1 | 2 | 0 | no |
| 2 | 0 | 2 | no |
| 3 | −4 | −4 | **yes** → True |

**Complexity:** O(n) time, O(1) extra space.

**Common wrong approach:** comparing values instead of nodes, or looping with `while fast.next.next`, which crashes with `AttributeError` when `fast.next` is `None`.
:::

:::exercise Merge two sorted lists
Write `merge_lists(a, b)` that merges two sorted linked lists into one sorted list by **relinking** their nodes, and returns its head.
```python starter
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def merge_lists(a, b):
    pass

print(to_list(merge_lists(build([1, 2, 4]), build([1, 3, 4]))))
```
```python check
fn = need("merge_lists")
def _run(x, y):
    return to_list(fn(build(x), build(y)))
test(_run, [
    (([1, 2, 4], [1, 3, 4]), [1, 1, 2, 3, 4, 4], "the example"),
    (([], []), [], "both empty"),
    (([], [0]), [0], "first list empty"),
    (([5], []), [5], "second list empty"),
    (([1, 2, 3], [7, 8]), [1, 2, 3, 7, 8], "one list finishes first"),
    (([-3, 10], [-5, 0, 0, 20]), [-5, -3, 0, 0, 10, 20], "negatives and duplicates"),
])
speed(lambda x, y: to_list(fn(build(x), build(y))), lambda n: (list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))),
      lambda x, y: sorted(x + y), sizes=(1_000, 50_000), what="nodes in each list", factor=200, floor=1.0,
      tip="Walk both lists once with a tail pointer; don't rebuild or re-sort.")
```
```python solution
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

def merge_lists(a, b):
    dummy = tail = ListNode(0)
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a else b      # one list is finished: attach the other's remainder
    return dummy.next

print(to_list(merge_lists(build([1, 2, 4]), build([1, 3, 4]))))
```
hint: At each step, which of the two front nodes should come next in the result?
hint: Use a dummy node and a `tail` pointer to the end of the merged list. Attach the smaller front node, then advance that list.
hint: `while a and b:` attach the smaller and move on; after the loop, `tail.next = a or b` attaches the leftover part in one step.
approach:
1. **Understand:** both inputs sorted; output sorted; reuse the nodes; either list may be empty.
2. **Examples:** [1, 2, 4] + [1, 3, 4] → [1, 1, 2, 3, 4, 4]; [] + [0] → [0].
3. **Brute force:** collect all values, sort, rebuild: O((n+m) log(n+m)) and new nodes.
4. **Pattern:** **merge with two pointers + dummy head** (same idea as merge sort's merge step).
5. **Plan:** dummy and tail; while both remain, attach the smaller; then attach the remainder.
6. **Code and test:** empties, one list running out first, equal values.
walkthrough:
**Line by line**

- `dummy = tail = ListNode(0)`: `tail` always points at the last node of the merged list.
- Each round compares the two fronts and attaches the smaller (`<=` keeps equal values in their original order: a **stable** merge).
- `tail = tail.next` moves to the node just attached.
- When one list runs out, the rest of the other is already sorted, so `tail.next = a if a else b` attaches it all at once.

**Trace** on [1, 4] and [2, 3]:

| a | b | attach | merged so far |
|---|---|---|---|
| 1 | 2 | 1 | 1 |
| 4 | 2 | 2 | 1, 2 |
| 4 | 3 | 3 | 1, 2, 3 |
| 4 | None | rest of a | 1, 2, 3, 4 |

**Complexity:** O(n + m) time, O(1) extra space.

**Common wrong approach:** forgetting the leftover nodes after the loop, which silently drops the end of the longer list.
:::

:::quiz
? Reversing a list, why must you save cur.next before changing it?
+ Changing cur.next would otherwise lose the only link to the rest of the list
- Python requires a temporary variable for every assignment
- It makes the loop faster
= The next pointer is the only way to reach the remaining nodes.
? In fast/slow pointers, where is slow when fast reaches the end?
+ In the middle of the list
- At the head
- At the end too
= Fast moves twice as far, so slow has covered half the distance.
? Why is Floyd's cycle detection better than storing visited nodes in a set?
+ It uses O(1) extra memory instead of O(n)
- It's always faster
- It works on unsorted lists only
= Both are O(n) time; the two-pointer version needs no extra storage.
? To remove the 2nd node from the end in one pass, you:
+ Move a lead pointer 2 steps ahead, then move lead and trail together until lead reaches the end
- Reverse the list twice
- Count the length first, then walk again
= The fixed gap means trail stops right before the node to remove. (Counting first also works, but takes two passes.)
:::

@@@ lesson
id: stacks
title: Stacks
minutes: 20
summary: Last in, first out: stacks with Python lists, matching brackets, a stack that knows its minimum, evaluating expressions, and why recursion is a stack.
---
A **stack** is a pile: you add to the top (**push**) and take from the top (**pop**). The last item in is the first out (**LIFO**). That one rule makes stacks perfect whenever the most recent unfinished thing must be dealt with first: the browser's Back button, undo in an editor, matching brackets, and the computer's own record of function calls.

![Left: a stack, a vertical pile where push and pop both happen at the top (last in, first out). Right: a queue, a horizontal line where items join at the back and leave from the front (first in, first out)](figures/stack-queue.svg)

### A Python list is a stack

`append` pushes onto the end and `pop()` removes from the end, both O(1). The end of the list is the top of the stack.

```python
stack = []
stack.append("a")        # push
stack.append("b")
stack.append("c")
print("top:", stack[-1])          # peek without removing
print("pop:", stack.pop())        # c: last in, first out
print("pop:", stack.pop())        # b
print("left:", stack, " empty?", not stack)
```

| Operation | Code | Cost |
|---|---|---|
| push | `stack.append(x)` | O(1) amortised |
| pop | `stack.pop()` | O(1) |
| peek (top) | `stack[-1]` | O(1) |
| is empty? | `not stack` | O(1) |

Never use `pop(0)` / `insert(0, x)` for a stack: those work at the **front** and cost O(n).

### Matching brackets

Every closing bracket must match the **most recent** unmatched opening bracket: exactly what a stack's top holds.

```python
def balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack            # anything left open is unbalanced

for t in ["(a[b]{c})", "(]", "((", "x = {1: [2, 3]}"]:
    print(f"{t!r:20} {balanced(t)}")
```

### A stack that knows its minimum

Design questions often ask for an extra O(1) operation. Store, alongside each item, the minimum **at that point**; popping restores the previous minimum for free.

```python
class MinStack:
    def __init__(self):
        self.items = []              # pairs (value, minimum so far)

    def push(self, x):
        current_min = min(x, self.items[-1][1]) if self.items else x
        self.items.append((x, current_min))

    def pop(self):
        return self.items.pop()[0]

    def top(self):
        return self.items[-1][0]

    def get_min(self):
        return self.items[-1][1]     # O(1): no searching

s = MinStack()
for x in [5, 3, 7, 2]:
    s.push(x)
print(s.get_min())   # 2
s.pop()
print(s.get_min())   # 3 again, after 2 is gone
```

### Evaluating expressions

**Reverse Polish notation** (RPN, or postfix) writes the operator after its two numbers: `3 4 +` means 3 + 4, and `2 3 4 * +` means 2 + 3 × 4. No brackets are ever needed, and a stack evaluates it in one pass: push numbers; on an operator, pop two, apply, push the result.

```python
def eval_rpn(tokens):
    stack = []
    for t in tokens:
        if t in {"+", "-", "*", "/"}:
            b, a = stack.pop(), stack.pop()      # careful: b was pushed last
            if t == "+": stack.append(a + b)
            elif t == "-": stack.append(a - b)
            elif t == "*": stack.append(a * b)
            else: stack.append(int(a / b))       # divide, rounding towards zero
        else:
            stack.append(int(t))
    return stack[0]

print(eval_rpn("2 3 4 * +".split()))          # 2 + 3*4 = 14
print(eval_rpn("5 1 2 + 4 * + 3 -".split()))  # 5 + (1+2)*4 - 3 = 14
```

Turning ordinary **infix** expressions like `2 + 3 * 4` into RPN is done with another stack, in Dijkstra's **shunting-yard** algorithm: numbers go straight to the output; operators wait on a stack until an operator with lower precedence (or a closing bracket) pushes them out. That's how calculators and programming-language parsers handle precedence.

```python
def to_rpn(expression):
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    out, ops = [], []
    for tok in expression.replace("(", " ( ").replace(")", " ) ").split():
        if tok.isdigit():
            out.append(tok)
        elif tok in prec:
            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[tok]:
                out.append(ops.pop())            # higher/equal precedence goes first (left to right)
            ops.append(tok)
        elif tok == "(":
            ops.append(tok)
        else:                                    # ")": pop until the matching "("
            while ops[-1] != "(":
                out.append(ops.pop())
            ops.pop()
    while ops:
        out.append(ops.pop())
    return out

print(to_rpn("2 + 3 * 4"))
print(to_rpn("(2 + 3) * 4"))
```

Both are O(n) time and O(n) space for n tokens.

### Recursion runs on a stack

Every function call pushes a **frame** (its local variables and where to return to) onto the **call stack**; returning pops it. That's why very deep recursion raises `RecursionError` in Python (the stack is limited to about 1,000 frames by default), and why any recursive algorithm can be rewritten with an explicit stack. You'll do exactly that for tree and graph traversals in Parts 7 and 8.

```python
def countdown(n):
    if n == 0:
        print("liftoff")
        return
    print("push frame for n =", n)
    countdown(n - 1)
    print("pop frame for n =", n)

countdown(2)
```

:::exercise Valid brackets
Write `is_valid(s)` that returns `True` if every bracket in `s` (any of `()[]{}`, mixed with other characters) is closed by the matching type in the right order, otherwise `False`. Must handle 200,000 characters quickly.
```python starter
def is_valid(s):
    pass
```
```python check
test("is_valid", [
    ("()", True, "one pair"),
    ("()[]{}", True, "three pairs side by side"),
    ("{[()]}", True, "nested"),
    ("(]", False, "wrong type"),
    ("([)]", False, "crossed"),
    ("((", False, "never closed"),
    ("))", False, "closing with nothing open"),
    ("", True, "an empty string"),
    ("f(x[1]) = {a: 2}", True, "other characters mixed in"),
    ("]", False, "a lone closing bracket"),
])
def _ref(s):
    pairs, st = {")": "(", "]": "[", "}": "{"}, []
    for ch in s:
        if ch in "([{": st.append(ch)
        elif ch in pairs:
            if not st or st.pop() != pairs[ch]: return False
    return not st
speed("is_valid", lambda n: "([{" * n + "}])" * n, _ref, sizes=(1_000, 8_000, 50_000), what="bracket triples",
      tip="Use a stack (a list with append / pop). Searching or replacing pairs in the string repeats work: O(n²).")
```
```python solution
def is_valid(s):
    match = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)                      # remember the opening bracket
        elif ch in match:
            if not stack or stack.pop() != match[ch]:
                return False                      # nothing open, or the wrong type
    return not stack                              # leftovers were never closed
```
```python slow
def is_valid(s):
    s = "".join(ch for ch in s if ch in "()[]{}")
    while "()" in s or "[]" in s or "{}" in s:
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""
```
hint: When you meet a closing bracket, which opening bracket must it match?
hint: It must match the **most recent** opening bracket that's still open: the top of a stack.
hint: Push opening brackets. On a closing one: if the stack is empty or `stack.pop()` isn't its partner, return False. At the end, the stack must be empty.
approach:
1. **Understand:** three bracket types, other characters ignored, order matters, an empty string is valid.
2. **Examples:** "{[()]}" → True; "([)]" → False (crossed); "((" → False (unclosed); ")" → False.
3. **Brute force:** repeatedly delete "()", "[]" and "{}" until nothing changes: correct but O(n²).
4. **Pattern:** "most recent unmatched" → **stack**.
5. **Plan:** dict closing → opening; push openers; on a closer, check and pop; return whether the stack is empty.
6. **Code and test:** the empty-stack case on a closer, and leftovers at the end.
walkthrough:
**Line by line**

- `match` maps each closing bracket to the opening one it needs.
- Opening brackets are pushed: they're waiting for their partner.
- For a closing bracket, two things can go wrong: nothing is open (`not stack`), or the most recent opener is the wrong type. `stack.pop()` both checks and removes it.
- Characters that aren't brackets fall through both branches and are ignored.
- `return not stack`: anything still on the stack was opened but never closed.

**Trace** on `([)]`:

| ch | action | stack after |
|---|---|---|
| ( | push | ( |
| [ | push | ( [ |
| ) | pop [ but need ( | **return False** |

**Complexity:** O(n) time, O(n) space in the worst case (all openers).

**Common wrong approach:** counting brackets (opens minus closes) only checks totals, so `([)]` and `)(` look valid.
:::

:::exercise Evaluate reverse Polish notation
Write `eval_rpn(tokens)` for a list of tokens: integers (as strings, possibly negative like `"-3"`) and the operators `+ - * /`. Division rounds **towards zero** (so `-7 / 2` is `-3`). Return the integer result.
```python starter
def eval_rpn(tokens):
    pass

print(eval_rpn(["2", "1", "+", "3", "*"]))   # (2 + 1) * 3 = 9
```
```python check
test("eval_rpn", [
    ((["2", "1", "+", "3", "*"],), 9, "(2 + 1) * 3"),
    ((["4", "13", "5", "/", "+"],), 6, "4 + 13 / 5"),
    ((["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],), 22, "a long expression with a negative number"),
    ((["7"],), 7, "a single number"),
    ((["3", "5", "-"],), -2, "order matters for minus"),
    ((["-7", "2", "/"],), -3, "division rounds towards zero"),
    ((["7", "-2", "/"],), -3, "division by a negative"),
    ((["6", "3", "/"],), 2, "exact division"),
])
```
```python solution
def eval_rpn(tokens):
    stack = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = stack.pop()              # the second operand was pushed last
            a = stack.pop()
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b)) # int() truncates towards zero; // would floor
        else:
            stack.append(int(t))         # handles "-3" too
    return stack.pop()

print(eval_rpn(["2", "1", "+", "3", "*"]))
```
hint: Read left to right. When you see an operator, which two numbers does it use?
hint: The two most recent numbers: pop them from a stack, compute, and push the result back.
hint: Pop `b` first, then `a`, and compute `a op b`. For division use `int(a / b)`, because `//` rounds down (−7 // 2 is −4).
approach:
1. **Understand:** postfix order; operands are strings; negative numbers exist; truncating division.
2. **Examples:** 2 1 + 3 * → 9; 3 5 - → −2 (not 2); −7 2 / → −3.
3. **Brute force:** repeatedly find "number number operator" and replace it with its value: O(n²).
4. **Pattern:** "use the most recent results" → **stack**.
5. **Plan:** for each token: operator → pop b, pop a, push a op b; number → push int(token). Return the last value.
6. **Code and test:** check the operand order for − and /, and negative division.
walkthrough:
**Line by line**

- Numbers are pushed. `int("-3")` handles negatives, and checking for operators first means `"-3"` is never mistaken for minus (it isn't exactly `"-"`).
- On an operator, `b = stack.pop()` comes first because `b` was pushed **last**. For `3 5 -`, a = 3 and b = 5, giving −2.
- `int(a / b)` truncates towards zero, as the task requires. Python's `//` floors, which differs for negatives.
- At the end exactly one number remains: the answer.

**Trace** on `4 13 5 / +`:

| token | stack after |
|---|---|
| 4 | 4 |
| 13 | 4 13 |
| 5 | 4 13 5 |
| / | 4 2 (13 / 5 → 2) |
| + | 6 |

**Complexity:** O(n) time, O(n) space.

**Common wrong approach:** popping as `a, b = stack.pop(), stack.pop()`, which swaps the operands, so `3 5 -` gives 2.
:::

:::exercise A stack with a minimum
Complete `MinStack` with `push(x)`, `pop()`, `top()` and `get_min()`. **Every** method must be O(1): `get_min` can't search the stack.
```python starter
class MinStack:
    def __init__(self):
        pass

    def push(self, x):
        pass

    def pop(self):
        pass

    def top(self):
        pass

    def get_min(self):
        pass
```
```python check
cls = need("MinStack")
def _ops(ops):
    s, out = cls(), []
    for op in ops:
        if op[0] == "push": s.push(op[1]); out.append(None)
        elif op[0] == "pop": s.pop(); out.append(None)
        elif op[0] == "top": out.append(s.top())
        else: out.append(s.get_min())
    return out
test(_ops, [
    (([("push", -2), ("push", 0), ("push", -3), ("min",), ("pop",), ("top",), ("min",)],), [None, None, None, -3, None, 0, -2], "the classic example"),
    (([("push", 5), ("min",), ("push", 5), ("pop",), ("min",)],), [None, 5, None, None, 5], "equal minimums pushed twice"),
    (([("push", 3), ("push", 1), ("push", 2), ("min",), ("pop",), ("min",), ("pop",), ("min",)],), [None, None, None, 1, None, 1, None, 3], "minimum restored after pops"),
])
class _Ref:
    def __init__(self): self.a = []
    def push(self, x): self.a.append((x, min(x, self.a[-1][1]) if self.a else x))
    def pop(self): self.a.pop()
    def top(self): return self.a[-1][0]
    def get_min(self): return self.a[-1][1]
def _bulk(cls_, n):
    s, total = cls_(), 0
    for i in range(n):
        s.push(n - i)
        total += s.get_min()
    for i in range(n // 2):
        s.pop(); total += s.get_min()
    return total
speed(lambda n: _bulk(cls, n), lambda n: n, lambda n: _bulk(_Ref, n), sizes=(1_000, 12_000, 100_000), what="pushes",
      tip="get_min must not scan the stack. Store, with each item, the minimum at the time it was pushed.")
```
```python solution
class MinStack:
    def __init__(self):
        self.items = []                         # pairs: (value, minimum including this value)

    def push(self, x):
        smallest = min(x, self.items[-1][1]) if self.items else x
        self.items.append((x, smallest))

    def pop(self):
        self.items.pop()

    def top(self):
        return self.items[-1][0]

    def get_min(self):
        return self.items[-1][1]
```
```python slow
class MinStack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        self.items.pop()

    def top(self):
        return self.items[-1]

    def get_min(self):
        return min(self.items)
```
hint: `min(self.items)` is O(n). What could you store at push time so the minimum is already known?
hint: The minimum only changes when you push or pop, and popping must bring back the previous minimum. Store the minimum **at each level** of the stack.
hint: Push pairs `(x, min(x, previous_min))`. `get_min` returns `self.items[-1][1]`; `pop` just pops.
approach:
1. **Understand:** a normal stack plus `get_min`, all in O(1); pops must restore older minimums.
2. **Examples:** push 5, 3, 7: min 3; pop 7: still 3; pop 3: min 5.
3. **Brute force:** `min()` over the list on every `get_min`: O(n).
4. **Pattern:** **store extra state with each item** (precompute instead of search).
5. **Plan:** each entry is (value, min so far); push computes the new min from the previous top's min.
6. **Code and test:** equal values, and the minimum returning after pops.
walkthrough:
**Line by line**

- Each stack entry carries the minimum of itself and everything below it.
- `push` needs only the previous entry's minimum: `min(x, self.items[-1][1])`, or `x` if the stack is empty.
- `pop` removes the top pair; the entry now on top already holds the correct minimum for the smaller stack, so nothing else needs updating.
- `top` and `get_min` read the top pair.

**Trace** pushing 5, 3, 7, then popping:

| operation | stack (value, min) | get_min |
|---|---|---|
| push 5 | (5,5) | 5 |
| push 3 | (5,5) (3,3) | 3 |
| push 7 | (5,5) (3,3) (7,3) | 3 |
| pop | (5,5) (3,3) | 3 |
| pop | (5,5) | 5 |

**Complexity:** O(1) per operation, O(n) space (one extra number per item).

**Common wrong approach:** keeping a single `self.min` variable: it can't be restored after the minimum is popped.
:::

:::quiz
? A stack returns items in which order?
+ Last in, first out
- First in, first out
- Smallest first
= You always take from the top: the most recently added item.
? Which list operations make a Python list an O(1) stack?
+ append and pop()
- insert(0, x) and pop(0)
- append and pop(0)
= Both work at the end of the list. Working at the front is O(n).
? Why does `3 5 -` in RPN give -2?
+ The first popped number (5) is the second operand: 3 - 5
- Minus always gives a negative answer
- RPN subtracts in reverse
= Pop b first, then a, and compute a - b.
? What causes Python's RecursionError?
+ Too many nested calls: each one pushes a frame onto the limited call stack
- Using a list as a stack
- Returning None
= The call stack is about 1,000 frames by default; deep recursion overflows it.
:::

@@@ lesson
id: monotonic-stack
title: "Monotonic stacks: next greater element"
minutes: 20
summary: A stack kept in sorted order answers "what's the next bigger (or smaller) item?" for every position in one pass. Used for daily temperatures, stock spans, the largest rectangle and trapping rain water.
---
"For each day, how many days until a warmer one?" The brute force looks ahead from every day: O(n²). A **monotonic stack** answers it for every day in a single pass.

A monotonic stack is an ordinary stack with one rule: its contents stay in increasing (or decreasing) order. Before pushing a new item, you pop everything that would break the order. The trick is that **each pop answers a question**: the item being popped has just found its "next greater element", the new item.

![Daily temperatures 73, 74, 75, 71, 69, 72, 76, 73. The stack holds indexes of days still waiting for a warmer day, with temperatures decreasing from bottom to top. When 72 arrives, it pops 69 and 71, whose answers become 1 and 2 days; then 72 is pushed. When 76 arrives it pops 72 and 75](figures/monotonic-stack.svg)

### The template: next greater element

```python
def next_greater(nums):
    answer = [-1] * len(nums)        # -1 means "no greater element to the right"
    stack = []                       # indexes whose answer we don't know yet; values decrease bottom→top
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            answer[stack.pop()] = x  # x is the first greater value to the right of that index
        stack.append(i)
    return answer

print(next_greater([2, 1, 2, 4, 3]))
```

**Why it's O(n), not O(n²):** the `while` loop sits inside a `for` loop, which looks quadratic. But every index is pushed exactly once and popped at most once, so across the whole run there are at most n pops. Total work: O(n). This is an **amortised** argument, like the list append in Lesson 4.

Variations are small changes to the same template:

| Question | Loop over | Pop while the top is… |
|---|---|---|
| next **greater** to the right | left → right | smaller than x |
| next **smaller** to the right | left → right | larger than x |
| previous greater (to the left) | left → right; the answer is whatever is left on top after popping | smaller or equal |
| circular array | twice round (index `i % n`) | same as above |

### Stock span: the previous greater element

The **span** of a day's price is how many consecutive days (ending today) had a price less than or equal to today's. That's "distance to the previous greater element", read from the stack after popping:

```python
def stock_span(prices):
    span, stack = [], []                      # stack of indexes with decreasing prices
    for i, p in enumerate(prices):
        while stack and prices[stack[-1]] <= p:
            stack.pop()
        span.append(i - stack[-1] if stack else i + 1)
        stack.append(i)
    return span

print(stock_span([100, 80, 60, 70, 60, 75, 85]))
```

### Largest rectangle in a histogram

Given bar heights, what's the biggest rectangle that fits under them? For each bar, the widest rectangle of that bar's height stretches left and right until a **shorter** bar. With an **increasing** stack, when a bar is popped we know both edges at once: the new shorter bar on the right, and the bar now under it on the left.

```python
def largest_rectangle(heights):
    best, stack = 0, []                        # indexes of bars with increasing heights
    for i, h in enumerate(heights + [0]):      # a final 0 flushes the stack
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, height * (i - left))
        stack.append(i)
    return best

print(largest_rectangle([2, 1, 5, 6, 2, 3]))   # 10: heights 5 and 6, width 2
```

O(n) time, O(n) space. The brute force (every pair of edges) is O(n²).

### Trapping rain water

Bars of different heights; how much rain is trapped between them? Water above each bar = min(tallest bar to its left, tallest to its right) − its own height. Two pointers do it in O(1) space: always move the side with the **lower** wall, because that side's water level is already decided.

```python
def trap(heights):
    left, right = 0, len(heights) - 1
    left_max = right_max = water = 0
    while left < right:
        if heights[left] < heights[right]:
            left_max = max(left_max, heights[left])
            water += left_max - heights[left]
            left += 1
        else:
            right_max = max(right_max, heights[right])
            water += right_max - heights[right]
            right -= 1
    return water

print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # 6
```

(A monotonic-stack version also exists: it fills water layer by layer whenever a taller bar closes a dip.)

### Spotting a monotonic-stack problem

Clue words: "next greater", "next smaller", "previous", "how many days until", "span", "the nearest bar that's shorter", "visible" (who can see over whom). If the brute force is "for each item, scan forward or backward until something bigger or smaller", a monotonic stack usually makes it O(n).

:::exercise Daily temperatures
Write `daily_temperatures(temps)` returning a list where entry `i` is how many days you'd wait after day `i` for a **warmer** temperature, or `0` if no warmer day comes. Must handle 100,000 days.
```python starter
def daily_temperatures(temps):
    pass

print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
```
```python check
test("daily_temperatures", [
    (([73, 74, 75, 71, 69, 72, 76, 73],), [1, 1, 4, 2, 1, 1, 0, 0], "the example"),
    (([30, 40, 50, 60],), [1, 1, 1, 0], "always warmer"),
    (([30, 60, 90],), [1, 1, 0], "three days"),
    (([90, 80, 70],), [0, 0, 0], "always colder"),
    (([50, 50, 51],), [2, 1, 0], "equal isn't warmer"),
    (([42],), [0], "one day"),
    (([],), [], "no days"),
])
def _ref(t):
    ans, st = [0] * len(t), []
    for i, x in enumerate(t):
        while st and t[st[-1]] < x:
            j = st.pop(); ans[j] = i - j
        st.append(i)
    return ans
speed("daily_temperatures", lambda n: list(range(n, 0, -1)), _ref, sizes=(1_000, 5_000, 100_000), what="days",
      tip="Scanning ahead from every day is O(n²). Keep a stack of days still waiting for a warmer one; each new day pops the days it answers.")
```
```python solution
def daily_temperatures(temps):
    answer = [0] * len(temps)
    waiting = []                                   # indexes of days with no warmer day yet (temps decreasing)
    for i, t in enumerate(temps):
        while waiting and temps[waiting[-1]] < t:  # today is warmer than those days
            j = waiting.pop()
            answer[j] = i - j
        waiting.append(i)
    return answer

print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
```
```python slow
def daily_temperatures(temps):
    answer = [0] * len(temps)
    for i in range(len(temps)):
        for j in range(i + 1, len(temps)):
            if temps[j] > temps[i]:
                answer[i] = j - i
                break
    return answer
```
hint: Instead of each day looking forward, let each new day answer the earlier days that were waiting for it.
hint: Keep a stack of **indexes** of days still waiting. Their temperatures decrease from bottom to top, so a warm new day pops from the top.
hint: For each `i, t`: while the stack's top day is colder than `t`, pop `j` and set `answer[j] = i - j`. Then push `i`. Days never popped keep 0.
approach:
1. **Understand:** strictly warmer; the answer is a distance in days; 0 if none.
2. **Examples:** [73, 74, 75, 71, 69, 72, 76, 73] → [1, 1, 4, 2, 1, 1, 0, 0]. Equal temperatures don't count.
3. **Brute force:** for each day, scan forward to the first warmer day: O(n²) when temperatures keep falling.
4. **Pattern:** "how many days until a warmer one" = **next greater element** → monotonic (decreasing) stack.
5. **Plan:** answers default to 0; stack of waiting indexes; each day pops the colder days it answers, then waits itself.
6. **Code and test:** equal temperatures, all falling, one day, empty.
walkthrough:
**Line by line**

- `answer = [0] * len(temps)`: days that never find a warmer day keep 0.
- `waiting` holds indexes, not temperatures, because we need distances. Its temperatures always decrease from bottom to top: anything warmer would already have popped them.
- `while waiting and temps[waiting[-1]] < t`: today answers every waiting day that is colder. Use `<`, not `<=`, because an equal temperature isn't warmer.
- `answer[j] = i - j` is the distance in days.
- Every day is then pushed to wait for its own warmer day.

**Trace** on the first six days, [73, 74, 75, 71, 69, 72]:

| i | t | popped (answer set) | waiting after (temps) |
|---|---|---|---|
| 0 | 73 | — | 73 |
| 1 | 74 | day 0 → 1 | 74 |
| 2 | 75 | day 1 → 1 | 75 |
| 3 | 71 | — | 75 71 |
| 4 | 69 | — | 75 71 69 |
| 5 | 72 | day 4 → 1, day 3 → 2 | 75 72 |

**Complexity:** O(n) time (each index is pushed and popped at most once), O(n) space.

**Common wrong approach:** storing temperatures instead of indexes in the stack, which leaves no way to compute the distance.
:::

:::exercise Largest rectangle in a histogram
Write `largest_rectangle(heights)` returning the area of the largest rectangle that fits under the bars (each bar has width 1). Must handle 100,000 bars.
```python starter
def largest_rectangle(heights):
    pass

print(largest_rectangle([2, 1, 5, 6, 2, 3]))   # 10
```
```python check
test("largest_rectangle", [
    (([2, 1, 5, 6, 2, 3],), 10, "the example"),
    (([2, 4],), 4, "two bars"),
    (([5],), 5, "one bar"),
    (([],), 0, "no bars"),
    (([3, 3, 3, 3],), 12, "all equal"),
    (([1, 2, 3, 4, 5],), 9, "increasing"),
    (([5, 4, 3, 2, 1],), 9, "decreasing"),
    (([2, 0, 2],), 2, "a zero-height bar"),
])
def _ref(h):
    best, st = 0, []
    for i, x in enumerate(h + [0]):
        while st and h[st[-1]] >= x:
            hh = h[st.pop()]
            left = st[-1] + 1 if st else 0
            best = max(best, hh * (i - left))
        st.append(i)
    return best
speed("largest_rectangle", lambda n: list(range(1, n + 1)), _ref, sizes=(1_000, 3_000, 100_000), what="bars",
      tip="Trying every pair of edges is O(n²). With an increasing stack, a bar's rectangle is finished when a shorter bar arrives: its left edge is the bar below it on the stack.")
```
```python solution
def largest_rectangle(heights):
    best = 0
    stack = []                                   # indexes of bars, heights increasing bottom→top
    extended = heights + [0]                     # a final 0-height bar flushes everything left
    for i, h in enumerate(extended):
        while stack and extended[stack[-1]] >= h:
            height = extended[stack.pop()]       # this bar's rectangle can't extend past i
            left = stack[-1] + 1 if stack else 0 # ...nor past the shorter bar below it
            best = max(best, height * (i - left))
        stack.append(i)
    return best

print(largest_rectangle([2, 1, 5, 6, 2, 3]))
```
```python slow
def largest_rectangle(heights):
    best = 0
    for i in range(len(heights)):
        low = heights[i]
        for j in range(i, len(heights)):
            low = min(low, heights[j])
            best = max(best, low * (j - i + 1))
    return best
```
hint: For each bar, imagine the widest rectangle exactly as tall as that bar. Where does it stop on the left and on the right?
hint: It stops at the first **shorter** bar on each side. Keep an increasing stack of indexes: a bar is popped exactly when its right edge (a shorter bar) arrives.
hint: When you pop index `top` at position `i`: height = heights[top]; left edge = (new stack top + 1) or 0 if empty; width = i − left. Append a 0 to the heights to flush the stack at the end.
approach:
1. **Understand:** width 1 per bar; the rectangle's height is the shortest bar it covers; return the area.
2. **Examples:** [2, 1, 5, 6, 2, 3] → 10 (5 and 6, width 2); [3, 3, 3, 3] → 12; [] → 0.
3. **Brute force:** every pair of edges, tracking the minimum height: O(n²).
4. **Pattern:** "nearest shorter bar on each side" → **monotonic (increasing) stack**.
5. **Plan:** loop over heights plus a sentinel 0; pop bars taller than or equal to the current one, computing their rectangles; push the index.
6. **Code and test:** increasing, decreasing, equal heights, zeros, empty.
walkthrough:
**Line by line**

- The stack holds indexes whose heights increase from bottom to top.
- When the current bar `h` is not taller than the top bar, that top bar's rectangle can't extend to the right any more: pop it.
- Its left edge is just after the bar now on top of the stack (that bar is shorter, which is why it's still there), or index 0 if the stack is empty.
- `width = i - left`, `area = height * width`.
- The sentinel 0 at the end is shorter than everything, so it pops every remaining bar.

**Trace** on [2, 1, 5, 6, 2, 3]:

| i | h | popped: height × width | stack after (heights) |
|---|---|---|---|
| 0 | 2 | — | 2 |
| 1 | 1 | 2 × 1 = 2 | 1 |
| 2 | 5 | — | 1 5 |
| 3 | 6 | — | 1 5 6 |
| 4 | 2 | 6 × 1 = 6; 5 × 2 = **10** | 1 2 |
| 5 | 3 | — | 1 2 3 |
| 6 | 0 | 3 × 1; 2 × 4 = 8; 1 × 6 = 6 | 0 |

**Complexity:** O(n) time, O(n) space.

**Common wrong approach:** forgetting the final flush (the sentinel 0), so bars still on the stack at the end, like the increasing run [1, 2, 3, 4, 5], are never measured.
:::

:::quiz
? Why is a monotonic stack algorithm O(n) even though it has a while loop inside a for loop?
+ Each index is pushed once and popped at most once, so all the pops together are at most n
- The while loop runs at most once per step
- Python optimises nested loops
= Count the total pops across the whole run, not per step: that's amortised analysis.
? For "next greater element to the right", what order do the values on the stack keep (bottom to top)?
+ Decreasing
- Increasing
- Random
= A larger new value pops the smaller ones; whatever remains is larger than what sits above it.
? In the largest-rectangle algorithm, when is a bar's rectangle complete?
+ When a shorter bar arrives on its right
- When a taller bar arrives
- Only at the end of the list
= A shorter bar stops it from extending further right; the bar below it on the stack marks the left edge.
? Which clue suggests a monotonic stack?
+ "For each day, how many days until a higher price?"
- "Find the shortest path between two cities"
- "Count the distinct words"
= "Next greater" or "previous smaller" questions are the classic monotonic-stack signal.
:::

@@@ lesson
id: queues-deques
title: Queues, circular buffers and deques
minutes: 20
summary: First in, first out: queues with collections.deque, a fixed-size circular buffer, a queue built from two stacks, and the monotonic deque for sliding-window maximums.
---
A **queue** is a line at a shop: people join at the back (**enqueue**) and leave from the front (**dequeue**). First in, first out (**FIFO**). Queues appear whenever things must be handled in arrival order: print jobs, web requests, messages between programs, and breadth-first search (Part 8), which explores a graph level by level.

### Don't use a list as a queue

`list.pop(0)` removes the front item, but then every other item shifts left: O(n). Python's `collections.deque` (a **double-ended queue**, said "deck") adds and removes at **both** ends in O(1).

```python
from collections import deque
import time

n = 20_000
items = list(range(n))
t = time.perf_counter()
while items:
    items.pop(0)                  # shifts everything each time: O(n) per pop
list_time = time.perf_counter() - t

q = deque(range(n))
t = time.perf_counter()
while q:
    q.popleft()                   # O(1) per pop
deque_time = time.perf_counter() - t
print(f"list.pop(0): {list_time:.3f} s   deque.popleft(): {deque_time:.3f} s")
```

| Operation | `deque` | `list` |
|---|---|---|
| `append(x)` / `pop()` (right end) | O(1) | O(1) |
| `appendleft(x)` / `popleft()` (left end) | **O(1)** | O(n) |
| `q[0]`, `q[-1]` (peek at the ends) | O(1) | O(1) |
| `q[i]` in the middle | O(n) | O(1) |
| `deque(maxlen=k)` | keeps only the last k items | — |

```python
from collections import deque

q = deque()
q.append("Ana"); q.append("Ben"); q.append("Cy")   # join at the back
print("served:", q.popleft())                      # Ana: first in, first out
print("next up:", q[0], " waiting:", list(q))

recent = deque(maxlen=3)                           # a bounded deque drops the oldest automatically
for page in ["home", "news", "sport", "weather", "home"]:
    recent.append(page)
print("last 3 pages:", list(recent))
```

### A circular buffer (ring buffer)

With a fixed capacity, you can build a queue on a plain array: two indexes (head and size) move forward and **wrap around** to 0 with `%`. No shifting, no growing: every operation is O(1). Audio players, network cards and logging systems use ring buffers because their memory never changes size.

![A ring of 6 slots. The head index points at the oldest item and the tail at the next free slot; both move clockwise and wrap from slot 5 back to slot 0](figures/circular-buffer.svg)

```python
class RingBuffer:
    def __init__(self, capacity):
        self.data = [None] * capacity
        self.head = 0                    # index of the oldest item
        self.size = 0

    def enqueue(self, x):
        if self.size == len(self.data):
            raise OverflowError("buffer full")
        tail = (self.head + self.size) % len(self.data)   # wrap around
        self.data[tail] = x
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            raise IndexError("buffer empty")
        x = self.data[self.head]
        self.head = (self.head + 1) % len(self.data)
        self.size -= 1
        return x

rb = RingBuffer(3)
rb.enqueue(1); rb.enqueue(2); rb.enqueue(3)
print(rb.dequeue(), rb.dequeue())     # 1 2
rb.enqueue(4); rb.enqueue(5)          # these wrap round into slots 0 and 1
print(rb.data, "->", rb.dequeue(), rb.dequeue(), rb.dequeue())
```

### A queue from two stacks

An interview classic, and a nice example of **amortised** cost. Push onto an `inbox` stack. To dequeue, take from an `outbox` stack; only when the outbox is empty, pour the whole inbox into it, which reverses the order so the oldest item ends up on top.

```python
class TwoStackQueue:
    def __init__(self):
        self.inbox, self.outbox = [], []

    def enqueue(self, x):
        self.inbox.append(x)                      # O(1)

    def dequeue(self):
        if not self.outbox:                       # only when empty...
            while self.inbox:                     # ...move everything once
                self.outbox.append(self.inbox.pop())
        return self.outbox.pop()

q = TwoStackQueue()
for x in [1, 2, 3]:
    q.enqueue(x)
print(q.dequeue())          # 1
q.enqueue(4)
print(q.dequeue(), q.dequeue(), q.dequeue())   # 2 3 4
```

A single dequeue can cost O(n) when it pours, but each item is moved from inbox to outbox **at most once**, so n operations cost O(n) in total: **amortised O(1)** each.

### Sliding window maximum: the monotonic deque

"The maximum of every window of k consecutive numbers." Recomputing `max(window)` is O(k) per window, O(n·k) in total. A deque of indexes, kept in **decreasing** order of value, does it in O(n):

- Before adding index `i`, pop from the **back** every index whose value is ≤ the new value: they can never be a maximum again while the new, larger value is in the window.
- Pop from the **front** if that index has slid out of the window.
- The front is always the current window's maximum.

![The numbers 1, 3, −1, −3, 5, 3, 6, 7 with a window of 3 sliding right. Under each window, the deque's contents (decreasing values) are shown; the front of the deque is that window's maximum: 3, 3, 5, 5, 6, 7](figures/sliding-max.svg)

```python
from collections import deque

def window_max(nums, k):
    dq, out = deque(), []                 # indexes; their values decrease front -> back
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:   # smaller values behind x can never win again
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:                # the front has left the window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out

print(window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
```

Same amortised argument as the monotonic stack: each index enters and leaves the deque at most once.

### Other queues you'll meet

- **Priority queue:** always serves the smallest (or most urgent) item first, not the oldest. Built on a heap with `heapq` (Lesson 32).
- **`queue.Queue`:** a thread-safe queue for passing work between threads (producer and consumer). It locks internally, so it's slower than `deque` for single-threaded code.
- **Message queues** (Kafka, RabbitMQ, cloud queues): the same FIFO idea between whole programs and servers.

:::exercise A queue from two stacks
Complete `MyQueue` using **only two Python lists used as stacks** (append, pop, `[-1]`, len) with `push(x)`, `pop()` (remove and return the front), `peek()` (return the front) and `empty()`. Each operation must be amortised O(1): 100,000 operations in well under a second.
```python starter
class MyQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x):
        pass

    def pop(self):
        pass

    def peek(self):
        pass

    def empty(self):
        pass
```
```python check
if uses("deque") or uses("pop(0)") or uses("insert(0"):
    raise AssertionError("Use only the two lists as stacks: append, pop() from the end, [-1] and len.")
cls = need("MyQueue")
def _ops(ops):
    q, out = cls(), []
    for op in ops:
        if op[0] == "push": q.push(op[1]); out.append(None)
        elif op[0] == "pop": out.append(q.pop())
        elif op[0] == "peek": out.append(q.peek())
        else: out.append(q.empty())
    return out
test(_ops, [
    (([("push", 1), ("push", 2), ("peek",), ("pop",), ("empty",)],), [None, None, 1, 1, False], "the classic example"),
    (([("empty",), ("push", 5), ("empty",), ("pop",), ("empty",)],), [True, None, False, 5, True], "empty before and after"),
    (([("push", 1), ("push", 2), ("pop",), ("push", 3), ("pop",), ("pop",)],), [None, None, 1, None, 2, 3], "pushing between pops keeps FIFO order"),
    (([("push", 1), ("peek",), ("peek",), ("pop",)],), [None, 1, 1, 1], "peek doesn't remove"),
])
from collections import deque as _dq
class _Ref:
    def __init__(self): self.d = _dq()
    def push(self, x): self.d.append(x)
    def pop(self): return self.d.popleft()
    def peek(self): return self.d[0]
    def empty(self): return not self.d
def _bulk(c, n):
    q, total = c(), 0
    for i in range(n):
        q.push(i)
        if i % 3 == 2:
            total += q.pop()
    while not q.empty():
        total += q.peek() + q.pop()
    return total
speed(lambda n: _bulk(cls, n), lambda n: n, lambda n: _bulk(_Ref, n), sizes=(1_000, 10_000, 100_000), what="operations",
      tip="Don't pour the stacks back and forth on every call. Move items from inbox to outbox only when the outbox is empty; each item then moves once.")
```
```python solution
class MyQueue:
    def __init__(self):
        self.inbox = []     # new items are pushed here
        self.outbox = []    # items come out from here, oldest on top

    def _refill(self):
        if not self.outbox:                       # only when the outbox runs dry
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def push(self, x):
        self.inbox.append(x)

    def pop(self):
        self._refill()
        return self.outbox.pop()

    def peek(self):
        self._refill()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox
```
```python slow
class MyQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x):
        self.inbox.append(x)

    def _front(self, remove):
        while self.inbox:
            self.outbox.append(self.inbox.pop())
        x = self.outbox.pop() if remove else self.outbox[-1]
        while self.outbox:
            self.inbox.append(self.outbox.pop())
        return x

    def pop(self):
        return self._front(True)

    def peek(self):
        return self._front(False)

    def empty(self):
        return not self.inbox
```
hint: A stack gives you the **newest** item; a queue needs the **oldest**. What happens to the order if you pour one stack into another?
hint: Pouring reverses the order, so the oldest ends up on top of the outbox. Pour only when the outbox is **empty**, and never pour back.
hint: `push` appends to inbox. `pop`/`peek`: if outbox is empty, move everything from inbox to outbox; then use `outbox.pop()` / `outbox[-1]`. `empty`: both lists empty.
approach:
1. **Understand:** FIFO behaviour using only stack operations; amortised O(1).
2. **Examples:** push 1, push 2, pop → 1; push 3; pop → 2; pop → 3.
3. **Brute force:** pour everything to the other stack and back on every pop: O(n) per operation.
4. **Pattern:** **two stacks reverse order**, with lazy transfer for **amortised O(1)**.
5. **Plan:** inbox for pushes; outbox for pops/peeks; refill the outbox only when it's empty.
6. **Code and test:** pushes in between pops must keep FIFO order.
walkthrough:
**Line by line**

- `push` is a plain append to `inbox`: O(1).
- `_refill` runs only when `outbox` is empty. Popping everything from `inbox` onto `outbox` reverses it, so the oldest item ends up on top of `outbox`.
- New pushes while `outbox` still has items go to `inbox` and wait. They're newer than everything in `outbox`, so serving `outbox` first keeps the order right.
- `empty` must check both lists.

**Trace:**

| operation | inbox | outbox | returns |
|---|---|---|---|
| push 1, push 2 | 1 2 | — | |
| pop | — | 2 1 → pop 1 → 2 | 1 |
| push 3 | 3 | 2 | |
| pop | 3 | — | 2 |
| pop | — (poured) | 3 → pop | 3 |

**Complexity:** amortised O(1) per operation (each item is pushed twice and popped twice in total), O(n) space.

**Common wrong approach:** pouring back into `inbox` after every pop (the "slow" version), which makes each pop O(n) and the whole sequence O(n²).
:::

:::exercise Sliding window maximum
Write `window_max(nums, k)` returning the maximum of every window of `k` consecutive numbers (there are `len(nums) - k + 1` windows; assume `1 <= k <= len(nums)`). Must handle 100,000 numbers with large windows.
```python starter
from collections import deque

def window_max(nums, k):
    pass

print(window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))   # [3, 3, 5, 5, 6, 7]
```
```python check
test("window_max", [
    (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7], "the example"),
    (([1], 1), [1], "one number"),
    (([9, 8, 7, 6], 2), [9, 8, 7], "decreasing"),
    (([1, 2, 3, 4], 2), [2, 3, 4], "increasing"),
    (([4, 4, 4], 2), [4, 4], "equal values"),
    (([5, 1, 2], 3), [5], "one window covering everything"),
    (([-7, -8, 7, 5, 7, 1, 6, 0], 4), [7, 7, 7, 7, 7], "negatives and repeated maximums"),
])
from collections import deque as _dq
def _ref(nums, k):
    dq, out = _dq(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()
        if i >= k - 1: out.append(nums[dq[0]])
    return out
speed("window_max", lambda n: ([(i * 7919) % 10007 for i in range(n)], max(1, n // 4)), _ref, sizes=(1_000, 40_000, 100_000),
      what="numbers (window = a quarter of them)",
      tip="max() over every window is O(n·k). Keep a deque of indexes with decreasing values: drop smaller ones from the back, expired ones from the front.")
```
```python solution
from collections import deque

def window_max(nums, k):
    dq = deque()                       # indexes; nums[dq] decreases from front to back
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()                   # can never be a maximum while x is in the window
        dq.append(i)
        if dq[0] <= i - k:             # the front index has slid out of the window
            dq.popleft()
        if i >= k - 1:                 # the first full window ends at index k - 1
            out.append(nums[dq[0]])
    return out

print(window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
```
```python slow
def window_max(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
```
hint: When a new, bigger number enters the window, can any smaller number before it ever be a window's maximum again?
hint: No, so throw those away. Keep a deque of **indexes** whose values decrease from front to back; the front is always the maximum.
hint: For each `i, x`: pop from the back while the back's value ≤ x; append i; if the front index ≤ i − k, popleft; once i ≥ k − 1, record nums[dq[0]].
approach:
1. **Understand:** n − k + 1 windows; the max of each; negatives and repeats allowed.
2. **Examples:** [1, 3, −1, −3, 5, 3, 6, 7], k = 3 → [3, 3, 5, 5, 6, 7].
3. **Brute force:** `max` of every slice: O(n·k), too slow when k is large.
4. **Pattern:** sliding window + "biggest so far, with expiry" → **monotonic deque**.
5. **Plan:** deque of indexes, values decreasing; push new, drop dominated ones from the back, expired from the front; read the front.
6. **Code and test:** decreasing and increasing input, equal values, k equal to the length.
walkthrough:
**Line by line**

- The deque holds **indexes**, because we must know when the front has left the window.
- `while dq and nums[dq[-1]] <= x: dq.pop()`: a value that's smaller and older than `x` leaves the window before `x` does, so it can never be the maximum. Popping it keeps the deque decreasing.
- `if dq[0] <= i - k`: the window is now `i-k+1 .. i`, so index `i - k` and older are out. At most one index expires per step.
- `if i >= k - 1`: from the first full window onward, the front is the maximum.

**Trace** on [1, 3, −1, −3, 5], k = 3:

| i | x | deque (values) after | window max |
|---|---|---|---|
| 0 | 1 | 1 | — |
| 1 | 3 | 3 (1 popped) | — |
| 2 | −1 | 3 −1 | 3 |
| 3 | −3 | 3 −1 −3 | 3 |
| 4 | 5 | 5 (all popped; 3 had expired anyway) | 5 |

**Complexity:** O(n) time (each index is added and removed at most once), O(k) space.

**Common wrong approach:** storing values instead of indexes, which gives no way to tell when the maximum has slid out of the window.
:::

:::quiz
? Why is `list.pop(0)` a bad way to dequeue?
+ Every remaining item shifts left, so it's O(n) per call
- It removes the last item instead
- It only works on sorted lists
= Use collections.deque and popleft(), which is O(1).
? In a circular buffer, how does the tail index wrap from the last slot to the first?
+ (head + size) % capacity
- It's reset by copying the array
- The buffer grows instead
= The modulo makes indexes go round the ring with no shifting.
? A queue built from two stacks has one dequeue that costs O(n). Why is it still called O(1)?
+ Each item is moved between the stacks at most once, so n operations cost O(n) in total: amortised O(1)
- Because n is always small
- Because Python lists are fast
= Amortised analysis averages the rare expensive step over all the cheap ones.
? In the sliding-window-maximum deque, why can a smaller value be removed when a larger one arrives?
+ It will leave the window before the larger value does, so it can never be the maximum
- Smaller values are never needed in any problem
- Deques can only hold decreasing values
= The newer, larger value dominates it for every future window that contains it.
:::

@@@ lesson
id: lru-cache
title: "Designing a data structure: the LRU cache"
minutes: 18
summary: Combine a hash map with a doubly linked list to get O(1) lookups and O(1) "most recently used" ordering; then the OrderedDict shortcut, Python's lru_cache, and the LFU variant.
---
A **cache** keeps recent results close at hand so you don't recompute or re-download them. It has limited room, so when it's full something must go. **Least Recently Used (LRU)** eviction throws out the item that hasn't been used for the longest time. Browsers, databases, CDNs and operating systems all use it, and "design an LRU cache" is one of the most common interview design questions.

The requirement: `get(key)` and `put(key, value)` both in **O(1)**, where any access makes that key the most recently used.

### Why one structure isn't enough

- A **dict** finds a key in O(1), but has no cheap way to find the least recently used item.
- A **list** ordered by recency knows the oldest item, but moving an item to the end is O(n) (find it, remove it, append it).
- A **doubly linked list** can move or remove a node in O(1)... if you already hold that node.

So combine them: the dict maps each key **to its node** in a doubly linked list ordered from least to most recently used.

![An LRU cache with capacity 3. A dictionary maps keys a, b and c to nodes in a doubly linked list between head and tail sentinels; the node next to head is the least recently used (evicted first) and the node next to tail is the most recently used. A get(a) unlinks a's node and re-inserts it next to the tail](figures/lru-cache.svg)

### The full design

```python
class Node:
    def __init__(self, key=None, value=None):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}                              # key -> node
        self.head, self.tail = Node(), Node()      # sentinels: head.next is the LEAST recent
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):                       # O(1)
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_recent(self, node):                   # O(1): insert just before the tail
        node.prev, node.next = self.tail.prev, self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)                         # touched: move to most recent
        self._add_recent(node)
        return node.value

    def put(self, key, value):
        if key in self.map:
            self._unlink(self.map[key])
        node = Node(key, value)
        self.map[key] = node
        self._add_recent(node)
        if len(self.map) > self.capacity:          # evict the least recent
            oldest = self.head.next
            self._unlink(oldest)
            del self.map[oldest.key]               # this is why nodes store their key

cache = LRUCache(2)
cache.put("a", 1); cache.put("b", 2)
cache.get("a")                 # a is now the most recent
cache.put("c", 3)              # full: evicts b, the least recent
print(cache.get("b"), cache.get("a"), cache.get("c"))
```

Every step is a dict operation or a fixed number of pointer changes: **O(1) time** per call, **O(capacity) space**.

### The Python shortcut: OrderedDict

`collections.OrderedDict` is exactly a dict plus a doubly linked list inside, and gives you `move_to_end` and `popitem(last=False)` in O(1). In an interview, mention it, but expect to be asked to build the real thing.

```python
from collections import OrderedDict

class LRU:
    def __init__(self, capacity):
        self.capacity, self.data = capacity, OrderedDict()

    def get(self, key):
        if key not in self.data:
            return -1
        self.data.move_to_end(key)           # most recent at the end
        return self.data[key]

    def put(self, key, value):
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)    # the first item is the least recent

c = LRU(2)
c.put(1, "one"); c.put(2, "two"); c.get(1); c.put(3, "three")
print(list(c.data.items()))
```

### Caching function results: functools

For caching a **function's** results (memoisation, which you'll use a lot in dynamic programming), Python has it built in:

```python
from functools import lru_cache, cache
import time

@lru_cache(maxsize=1024)          # LRU eviction after 1,024 distinct arguments
def slow_square(n):
    time.sleep(0.01)              # pretend this is expensive
    return n * n

t = time.perf_counter()
slow_square(12); slow_square(12); slow_square(12)
print(f"3 calls took {time.perf_counter() - t:.3f} s")
print(slow_square.cache_info())

@cache                            # unbounded cache (Python 3.9+)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
print(fib(90))
```

Arguments must be hashable (no lists), because they become dict keys.

### LFU: evict the least frequently used

**Least Frequently Used** evicts the key used the fewest times (ties broken by least recent). The O(1) design keeps a count per key and, for each count, an `OrderedDict` of keys in recency order, plus the current minimum count:

```python
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.vals, self.freq = {}, {}                  # key -> value, key -> use count
        self.buckets = defaultdict(OrderedDict)        # count -> keys in recency order
        self.min_freq = 0

    def _touch(self, key):
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f] and self.min_freq == f:
            self.min_freq += 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key):
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) == self.capacity:            # evict from the lowest count, oldest first
            old, _ = self.buckets[self.min_freq].popitem(last=False)
            del self.vals[old], self.freq[old]
        self.vals[key], self.freq[key] = value, 1
        self.buckets[1][key] = None
        self.min_freq = 1

lfu = LFUCache(2)
lfu.put("a", 1); lfu.put("b", 2); lfu.get("a")   # a used twice, b once
lfu.put("c", 3)                                   # evicts b (lowest count)
print(lfu.get("b"), lfu.get("a"), lfu.get("c"))
```

### How to approach any "design a data structure" question

1. **List the operations and their required costs** (e.g. get O(1), put O(1), evict the oldest O(1)).
2. **For each operation, pick the structure that makes it fast**: lookup → hash map; order or oldest/newest → linked list, deque or heap; min/max → heap or extra stored state.
3. **Link the structures** so they stay in sync (the dict stores node references; nodes store their keys).
4. **Walk through an example** by hand, including the full and empty edge cases.

:::exercise Build an LRU cache
Complete `LRUCache(capacity)` with `get(key)` (the value, or `-1` if missing; counts as a use) and `put(key, value)` (insert or update, counts as a use; when over capacity, evict the least recently used key). Both must be O(1): 100,000 operations on a cache of 50,000 keys must be fast. Don't use `OrderedDict` here: build it with a dict and a doubly linked list.
```python starter
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        pass

    def put(self, key, value):
        pass
```
```python check
if uses("OrderedDict"):
    raise AssertionError("Build it from a dict and the doubly linked list, without OrderedDict.")
cls = need("LRUCache")
def _ops(capacity, ops):
    c, out = cls(capacity), []
    for op in ops:
        if op[0] == "put": c.put(op[1], op[2]); out.append(None)
        else: out.append(c.get(op[1]))
    return out
test(_ops, [
    ((2, [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3), ("get", 2), ("put", 4, 4), ("get", 1), ("get", 3), ("get", 4)]),
     [None, None, 1, None, -1, None, -1, 3, 4], "the classic example"),
    ((1, [("put", 1, 1), ("put", 2, 2), ("get", 1), ("get", 2)]), [None, None, -1, 2], "capacity 1"),
    ((2, [("put", 1, 1), ("put", 2, 2), ("put", 1, 10), ("put", 3, 3), ("get", 1), ("get", 2)]), [None, None, None, None, 10, -1], "updating a key makes it most recent"),
    ((2, [("get", 5)]), [-1], "get on an empty cache"),
    ((2, [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3), ("get", 1), ("get", 2), ("get", 3)]), [None, None, 1, None, 1, -1, 3], "get counts as a use"),
])
from collections import OrderedDict as _OD
class _Ref:
    def __init__(self, c): self.c, self.d = c, _OD()
    def get(self, k):
        if k not in self.d: return -1
        self.d.move_to_end(k); return self.d[k]
    def put(self, k, v):
        self.d[k] = v; self.d.move_to_end(k)
        if len(self.d) > self.c: self.d.popitem(last=False)
def _bulk(c_, n):
    c, total = c_(n // 2), 0
    for i in range(n):
        c.put(i, i)
        total += c.get(i // 2) + c.get(i - 7)
    return total
speed(lambda n: _bulk(cls, n), lambda n: n, lambda n: _bulk(_Ref, n), sizes=(1_000, 20_000, 100_000), what="operations",
      tip="Searching a list for the key, or for the least recent item, is O(n). The dict must map each key to its node, so moving or removing it is a few pointer changes.")
```
```python solution
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}                    # key -> node
        self.head = Node()               # head.next = least recently used
        self.tail = Node()               # tail.prev = most recently used
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_recent(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._add_recent(node)
        return node.value

    def put(self, key, value):
        node = self.map.get(key)
        if node:                                 # update: change the value, mark as recent
            node.value = value
            self._unlink(node)
            self._add_recent(node)
            return
        node = Node(key, value)
        self.map[key] = node
        self._add_recent(node)
        if len(self.map) > self.capacity:
            lru = self.head.next                 # least recently used
            self._unlink(lru)
            del self.map[lru.key]
```
```python slow
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        self.order = []                      # keys, least recent first

    def get(self, key):
        if key not in self.map:
            return -1
        self.order.remove(key)               # O(n)
        self.order.append(key)
        return self.map[key]

    def put(self, key, value):
        if key in self.map:
            self.order.remove(key)
        self.map[key] = value
        self.order.append(key)
        if len(self.order) > self.capacity:
            del self.map[self.order.pop(0)]  # O(n)
```
hint: You need two things in O(1): find a key, and find/move the least recently used one. Which structure is good at each?
hint: A dict for lookup, and a doubly linked list in recency order for moving and evicting. The dict's values are the **nodes**.
hint: Write `_unlink(node)` and `_add_recent(node)` (insert before the tail). `get`: if found, unlink + add_recent, return value. `put`: update or create, add_recent, and if over capacity remove `head.next` from the list **and** from the dict (that's why nodes store their key).
approach:
1. **Understand:** get and put both count as a use; updating doesn't add a new key; evict exactly one least recent key when over capacity.
2. **Examples:** capacity 2: put 1, put 2, get 1 → 1, put 3 evicts 2, get 2 → −1.
3. **Brute force:** dict + a Python list of keys in recency order: `list.remove` is O(n).
4. **Pattern:** **hash map + doubly linked list** (the dict stores node references).
5. **Plan:** sentinels head/tail; helpers unlink / add_recent; get moves to recent; put updates or inserts, then evicts head.next if needed.
6. **Code and test:** capacity 1, updating an existing key, get counting as a use.
walkthrough:
**Line by line**

- `self.map` maps each key to its **node**, so we can reach any node in O(1).
- The list runs from least recent (`head.next`) to most recent (`tail.prev`). Sentinels mean inserting and removing never need `if` checks for empty lists.
- `_unlink` connects a node's neighbours to each other; `_add_recent` splices the node in just before `tail`. Both are four pointer assignments at most.
- `get` on a hit moves the node to the recent end, because reading counts as a use.
- `put` on an existing key updates the value and moves it (no eviction needed: the size doesn't change).
- When the size exceeds capacity, `head.next` is the least recent node. Unlink it, and delete `lru.key` from the dict: the node must remember its own key, or we couldn't find the dict entry to delete.

**Trace** with capacity 2:

| operation | list (least → most recent) | returns |
|---|---|---|
| put 1, put 2 | 1 2 | |
| get 1 | 2 1 | 1 |
| put 3 | 2 1 3 → evict 2 → 1 3 | |
| get 2 | 1 3 | −1 |

**Complexity:** O(1) per operation, O(capacity) space.

**Common wrong approach:** forgetting to delete the evicted key from the dict, so `get` still finds a node that's no longer in the list (and the dict grows forever).
:::

:::quiz
? Why does an LRU cache need both a dict and a doubly linked list?
+ The dict finds a key in O(1); the list keeps recency order and moves or removes nodes in O(1)
- The dict stores values and the list stores keys, for no reason
- A dict alone can evict the oldest key in O(1)
= Each structure makes a different operation fast; together they make every operation O(1).
? Why does each node store its key?
+ When the oldest node is evicted, you need its key to delete it from the dict
- Nodes are sorted by key
- To compute the hash
= The list tells you which node is oldest; the key tells you which dict entry to remove.
? What does @lru_cache do to a function?
+ Remembers the results for recent arguments and returns them without recomputing
- Makes the function run in parallel
- Limits how often it can be called
= It's memoisation with LRU eviction; arguments must be hashable.
? An LFU cache evicts:
+ The key used the fewest times (oldest first on ties)
- The most recently used key
- A random key
= Least Frequently Used counts uses; LRU only looks at recency.
:::
