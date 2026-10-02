@@@ part
id: 3
title: Hashing
level: Beginner
blurb: How hash tables give O(1) lookups (hash functions, buckets, collisions, resizing), then the hashing patterns behind a huge share of interview problems: counting, Two Sum, grouping, and prefix sums with a hash map.

@@@ lesson
id: hash-tables
title: How hash tables work
minutes: 20
summary: Hash functions, buckets, collisions (chaining and open addressing), load factor and resizing. Why dict and set are O(1) on average, when they degrade, and why keys must be immutable.
---
A list finds an item by its **position**. A **hash table** finds a value by its **key**, almost instantly, whatever the size. Python's `dict` and `set` are hash tables.

The idea: turn the key into a number with a **hash function**, and use that number to pick a **bucket** (a slot in an internal array) where the value is stored. Looking it up later repeats the same calculation and goes straight to that bucket.

![A hash table with 8 buckets. The key "cat" goes through the hash function, giving a big number; that number modulo 8 is 3, so "cat" is stored in bucket 3. The key "dog" lands in bucket 6. The key "owl" also hashes to bucket 3, a collision, so bucket 3 holds a short chain of two entries](figures/hash-table.svg)

```python
for key in ["cat", "dog", 42, (1, 2)]:
    h = hash(key)
    print(f"{str(key):>6}  hash = {h:>22}  bucket in a table of 8: {h % 8}")
```

(String hashes change each time Python starts, a security feature called **hash randomisation**; numbers hash to themselves.)

### Collisions

Different keys can land in the **same bucket**: that's a **collision**, and it's unavoidable (there are infinitely many possible keys and only so many buckets). Two classic fixes:

| Strategy | How it works | Used by |
|---|---|---|
| **Separate chaining** | each bucket holds a small list of (key, value) pairs; search that list | Java's HashMap, many textbooks |
| **Open addressing** | if the bucket is taken, probe other buckets in a fixed sequence until a free one is found | Python's dict and set |

### Load factor and resizing

The **load factor** is items ÷ buckets. As it grows, collisions grow too, and lookups slow down. So hash tables **resize**: when the load factor passes a threshold (Python's dict keeps it below about ⅔), they allocate a bigger array and re-insert every item. That one resize is O(n), but like a list's growth it happens rarely, so inserts are **amortised O(1)** (Lesson 4).

### Average O(1), worst case O(n)

With a good hash function, keys spread evenly, every bucket holds O(1) items, and lookups, inserts and deletes are **O(1) on average**. In the worst case, when every key collides, the table degrades to a list: O(n). Attackers once exploited this by sending web servers many colliding keys, which is why string hashes are now randomised.

### Build one yourself (chaining)

```python
class TinyHashMap:
    def __init__(self, size=8):
        self.buckets = [[] for _ in range(size)]
        self.count = 0

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:          # key already there: update
                pair[1] = value
                return
        bucket.append([key, value])
        self.count += 1
        if self.count / len(self.buckets) > 0.75:
            self._resize()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def _resize(self):
        old = [pair for bucket in self.buckets for pair in bucket]
        self.buckets = [[] for _ in range(2 * len(self.buckets))]
        self.count = 0
        for k, v in old:
            self.put(k, v)

m = TinyHashMap()
for i, word in enumerate(["cat", "dog", "owl", "emu", "yak", "elk", "ant"]):
    m.put(word, i)
print(m.get("owl"), m.get("ant"), m.get("cow", "missing"), "buckets:", len(m.buckets))
```

### Why keys must be immutable

A key's hash decides where it's stored. If the key could change after insertion, its hash would change, and the table would look in the wrong bucket. So Python only allows **hashable** keys: numbers, strings, tuples (of hashable things), frozensets. Lists, dicts and sets can't be keys.

```python
locations = {(51.5, -0.1): "London"}      # a tuple works as a key
print(locations[(51.5, -0.1)])
try:
    bad = {[1, 2]: "no"}
except TypeError as e:
    print("TypeError:", e)
```

Need a list-like key? Convert it: `tuple(my_list)`. Need a set-like key? Use `frozenset`.

### Sets, dicts and their costs

| Operation | dict / set average | worst |
|---|---|---|
| insert, look up, delete, `in` | O(1) | O(n) |
| iterate over everything | O(n) | O(n) |
| build from n items | O(n) | O(n²) |

Since Python 3.7, a `dict` remembers **insertion order** (sets don't promise any order).

:::exercise Your own hash map
Complete the class `MyHashMap` (using **separate chaining**, without using Python's `dict` or `set` inside it) with:
- `put(key, value)`: insert, or update if the key exists;
- `get(key)`: the value, or `-1` if the key is missing;
- `remove(key)`: delete the key if present.
```python starter
class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def put(self, key, value):
        pass

    def get(self, key):
        pass

    def remove(self, key):
        pass
```
```python check
if uses("dict(") or uses("{}") or uses("set("):
    raise AssertionError("Build it from the buckets list, without a dict or set inside the class.")
cls = need("MyHashMap")
m = cls()
m.put(1, 1); m.put(2, 2)
if m.get(1) != 1:
    raise AssertionError(f"After put(1, 1), get(1) should be 1 but was {m.get(1)!r}.")
if m.get(3) != -1:
    raise AssertionError(f"get on a missing key should return -1, but returned {m.get(3)!r}.")
m.put(2, 20)
if m.get(2) != 20:
    raise AssertionError(f"put(2, 20) on an existing key should update it, but get(2) returned {m.get(2)!r}.")
m.remove(2)
if m.get(2) != -1:
    raise AssertionError("After remove(2), get(2) should return -1.")
m.remove(99)
m.put(1001, 7)
if m.get(1) != 1 or m.get(1001) != 7:
    raise AssertionError("Keys 1 and 1001 land in the same bucket (1001 % 1000 == 1). Both must be stored: check your chaining.")
m.remove(1)
if m.get(1001) != 7 or m.get(1) != -1:
    raise AssertionError("Removing key 1 must not remove key 1001 from the same bucket.")
m2 = cls()
for i in range(5000):
    m2.put(i, i * 2)
if any(m2.get(i) != i * 2 for i in range(0, 5000, 7)):
    raise AssertionError("After 5,000 puts, some values are wrong.")
```
```python solution
class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _bucket(self, key):
        return self.buckets[hash(key) % self.size]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value          # update in place
                return
        bucket.append([key, value])

    def get(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                return
```
hint: Every method starts the same way: find the bucket with `self.buckets[hash(key) % self.size]`.
hint: A bucket is a list of `[key, value]` pairs. `put` updates the pair if the key is there, otherwise appends a new pair; `get` searches the bucket.
hint: For `remove`, find the pair's position in the bucket with `enumerate` and `bucket.pop(i)`. Only remove the pair whose key matches.
approach:
1. **Understand:** three operations; missing keys give −1; keys can collide (1 and 1001).
2. **Examples:** put(1, 1), get(1) → 1; put(1, 5) then get(1) → 5; get(3) → −1.
3. **Brute force:** one big list of pairs, searched every time: O(n) per operation.
4. **Pattern:** **hashing + separate chaining**: the hash picks a short bucket; search only that.
5. **Plan:** a helper to find the bucket; put: search, update or append; get: search or −1; remove: search and pop.
6. **Code and test:** test two keys in the same bucket and removing one of them.
walkthrough:
**Line by line**

- `_bucket(key)`: `hash(key) % self.size` maps any key to a bucket index 0–999. A helper avoids repeating it.
- `put`: if a pair with this key exists, change its value (`pair[1] = value`, which works because the pair is a list) and stop; otherwise append a new pair. Without the search you'd store duplicate keys.
- `get`: scan only this bucket. Return −1 if the key isn't there.
- `remove`: `enumerate` gives the position; `bucket.pop(i)` deletes that pair only.

**Trace:** put(1, 1), put(1001, 7) (both hash to bucket 1), then remove(1):

| operation | bucket 1 |
|---|---|
| put(1, 1) | [[1, 1]] |
| put(1001, 7) | [[1, 1], [1001, 7]] |
| get(1001) | scan → 7 |
| remove(1) | [[1001, 7]] |

**Complexity:** O(1 + chain length) per operation. With 1,000 buckets and evenly spread keys, chains are short: O(1) on average. A production table would also resize as it fills (like `TinyHashMap` above) to keep chains short.
:::

:::quiz
? What does a hash function do in a hash table?
+ Turns a key into a number used to pick a bucket
- Sorts the keys
- Encrypts the values
= The same key always gives the same bucket, so lookups go straight there.
? Two different keys land in the same bucket. This is called:
+ A collision
- A resize
- A rehash attack
= Collisions are normal; chaining or probing handles them.
? Why can't a list be a dict key?
+ Lists can change, which would change their hash and lose the entry
- Lists are too long
- Only strings can be keys
= Keys must be hashable (immutable). Use a tuple instead.
? What keeps a hash table's operations O(1) on average as it grows?
+ Resizing when the load factor gets too high
- Sorting the buckets
- Using only integer keys
= Fewer items per bucket means short searches.
:::

@@@ lesson
id: hashing-patterns
title: Hashing patterns: counting, Two Sum, grouping
minutes: 24
summary: The hash-map patterns behind many interview problems: frequency counting, "have I seen the complement?", grouping by a key, prefix sums with a hash map, and longest consecutive sequence.
---
Whenever a brute force asks "have I seen this before?" or "how many times?", a hash map usually turns O(n²) into O(n). This lesson collects the patterns.

### 1. Counting with Counter

```python
from collections import Counter

words = "the cat and the hat and the bat".split()
counts = Counter(words)
print(counts)
print(counts["the"], counts["dog"])          # missing keys count as 0
print(counts.most_common(2))

# the same by hand, which is what Counter does
manual = {}
for w in words:
    manual[w] = manual.get(w, 0) + 1
print(manual)
```

First unique character: count everything, then scan again in order:

```python
from collections import Counter

def first_unique(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1

print(first_unique("leetcode"), first_unique("loveleetcode"), first_unique("aabb"))
```

### 2. "Have I seen the complement?": Two Sum

> Given numbers and a target, return the indexes of two numbers that add up to the target.

For each number `x`, the partner we need is `target - x` (its **complement**). Remember every number we've passed in a dict of value → index; then each check is O(1):

![Walking through [2, 7, 11, 15] looking for target 9. At 2, the needed partner is 7, which hasn't been seen, so 2 is stored with index 0. At 7, the needed partner is 2, which is in the dict with index 0, so the answer is [0, 1]](figures/two-sum.svg)

```python
def two_sum(nums, target):
    seen = {}                          # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i                    # store AFTER checking, so x can't pair with itself
    return []

print(two_sum([2, 7, 11, 15], 9), two_sum([3, 2, 4], 6), two_sum([3, 3], 6))
```

Compare with the two-pointer version in Lesson 7: that needs **sorted** input and O(1) space; this works on **any** order, with O(n) space.

### 3. Grouping by a key: anagrams

Words that are anagrams of each other share the same **sorted letters**. Use that as the dict key and collect the words in lists. `defaultdict(list)` creates an empty list the first time a key is used:

```python
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)       # "eat", "tea", "ate" -> key "aet"
    return list(groups.values())

print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
```

Choosing the right **key** is the whole trick. Others you'll see: the tuple of 26 letter counts (avoids sorting), a normalised form (lowercase, no spaces), or `(row // 3, col // 3)` for Sudoku boxes.

### 4. Prefix sums + hash map: subarray sum equals k

How many contiguous subarrays add up to k? Negative numbers rule out a sliding window. With prefix sums, a subarray `i..j` sums to k exactly when `prefix[j + 1] - prefix[i] == k`, so at each position, ask: **how many earlier prefix sums equal `current - k`?** Count prefix sums in a dict as you go.

```python
def count_subarrays_sum_k(nums, k):
    counts = {0: 1}            # the empty prefix (sum 0) has been seen once
    current = answer = 0
    for x in nums:
        current += x
        answer += counts.get(current - k, 0)      # subarrays ending here with sum k
        counts[current] = counts.get(current, 0) + 1
    return answer

print(count_subarrays_sum_k([1, 1, 1], 2))          # [1,1] twice
print(count_subarrays_sum_k([1, -1, 1, -1], 0))     # four subarrays sum to 0
```

### 5. Sets for O(1) "is it there?": longest consecutive sequence

Find the length of the longest run of consecutive integers (in any order) in O(n). Put everything in a set; only **start counting from numbers that begin a run** (whose predecessor isn't in the set), so each number is visited a constant number of times:

```python
def longest_consecutive(nums):
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 not in values:            # x starts a run
            length = 1
            while x + length in values:
                length += 1
            best = max(best, length)
    return best

print(longest_consecutive([100, 4, 200, 1, 3, 2]))    # 1, 2, 3, 4
```

### Pattern summary

| Clue | Hash pattern | Key → value |
|---|---|---|
| "how many times", "most frequent" | counting | item → count |
| "two numbers that sum to", "pair with difference" | complement lookup | value → index |
| "group", "anagrams", "same pattern" | grouping | normalised key → list |
| "subarray sum equals k" (negatives allowed) | prefix sum counts | prefix sum → how many times |
| "consecutive", "is it present" | set membership | value (set) |
| "first unique", "first repeated" | count, then scan in order | item → count |

:::exercise Two Sum
Write `two_sum(nums, target)` returning `[i, j]` with `i < j` and `nums[i] + nums[j] == target`, or `[]` if no pair exists. The list is **not** sorted. Make it fast for 100,000 numbers.
```python starter
def two_sum(nums, target):
    pass
```
```python check
def _valid(got, nums, target):
    exists = any(nums[a] + nums[b] == target for a in range(len(nums)) for b in range(a + 1, len(nums)))
    if not exists:
        return got == []
    return isinstance(got, (list, tuple)) and len(got) == 2 and 0 <= got[0] < got[1] < len(nums) and nums[got[0]] + nums[got[1]] == target
test("two_sum", [
    (([2, 7, 11, 15], 9), [0, 1], "the example"),
    (([3, 2, 4], 6), [1, 2], "the answer isn't at the start"),
    (([3, 3], 6), [0, 1], "two equal numbers"),
    (([3], 6), [], "one number can't pair with itself"),
    (([1, 2, 3], 100), [], "no pair"),
    (([], 0), [], "an empty list"),
    (([-3, 4, 3, 90], 0), [0, 2], "negative numbers"),
], valid=_valid)
def _ref(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen: return [seen[target - x], i]
        seen[x] = i
    return []
speed("two_sum", lambda n: (list(range(0, 2 * n, 2)), -1), _ref, sizes=(1_000, 6_000, 100_000), what="numbers",
      valid=lambda got, nums, t: got == [],
      tip="Checking every pair is O(n²). For each number, the partner you need is target - x: remember the numbers you've seen in a dict (value -> index).")
```
```python solution
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []
```
```python slow
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```
hint: For a number `x`, which partner would complete the pair?
hint: The partner is `target - x`. Keep a dict of the numbers you've already seen, mapping each value to its index.
hint: For each `i, x`: if `target - x` is in the dict, return `[seen[target - x], i]`; otherwise `seen[x] = i`. Check before storing.
approach:
1. **Understand:** unsorted input; two **different** positions; return their indexes (smaller first) or [].
2. **Examples:** `[2, 7, 11, 15]`, 9 → [0, 1]. `[3, 3]`, 6 → [0, 1]. `[3]`, 6 → [] (can't reuse the same 3).
3. **Brute force:** all pairs: O(n²).
4. **Pattern:** "two numbers that sum to" + unsorted → **complement lookup** in a hash map.
5. **Plan:** dict value → index; for each number, look up its complement; if found, done; else store the number.
6. **Code and test:** storing **after** the check is what stops `[3]`, 6 from pairing 3 with itself.
walkthrough:
**Line by line**

- `seen = {}` maps each value already passed to its index.
- `need = target - x` is the only number that can pair with `x`.
- `if need in seen:` is O(1). If true, the earlier index is `seen[need]` and the current one is `i`, already in the right order.
- `seen[x] = i` comes **after** the check, so a number can't pair with itself; for `[3, 3]`, the second 3 finds the first one.

**Trace** on `[3, 2, 4]`, target 6:

| i | x | need | in seen? | seen after |
|---|---|---|---|---|
| 0 | 3 | 3 | no (empty) | {3: 0} |
| 1 | 2 | 4 | no | {3: 0, 2: 1} |
| 2 | 4 | 2 | **yes**, index 1 | return [1, 2] |

**Complexity:** O(n) time, O(n) space.

**Interview talking point:** if the input were sorted, two pointers would need only O(1) space. Mention the trade-off.
:::

:::exercise Group the anagrams
Write `group_anagrams(words)` that groups words that are anagrams of each other. Return a list of groups (lists). The order of the groups and of words inside a group doesn't matter.
```python starter
def group_anagrams(words):
    pass
```
```python check
def _norm(groups):
    return sorted(sorted(g) for g in groups)
test("group_anagrams", [
    (["eat", "tea", "tan", "ate", "nat", "bat"], [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]], "the example"),
    ([], [], "no words"),
    ([""], [[""]], "one empty word"),
    (["a"], [["a"]], "one word"),
    (["abc", "cab", "bca", "xyz"], [["abc", "cab", "bca"], ["xyz"]], "one big group"),
    (["ab", "ba", "aab", "aba"], [["ab", "ba"], ["aab", "aba"]], "different lengths aren't anagrams"),
], key=_norm)
def _ref(words):
    from collections import defaultdict
    g = defaultdict(list)
    for w in words: g["".join(sorted(w))].append(w)
    return list(g.values())
import random, string
def _make(n):
    r = random.Random(n)
    return ["".join(r.choice("abcde") for _ in range(6)) for _ in range(n)]
speed("group_anagrams", _make, _ref, sizes=(500, 15_000, 50_000), what="words", key=_norm,
      tip="Comparing every word with every group is O(n²). Give each word a key that's the same for all its anagrams (its sorted letters) and use a dict of key -> list.")
```
```python solution
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        key = "".join(sorted(w))      # all anagrams share their sorted letters
        groups[key].append(w)
    return list(groups.values())
```
```python slow
def group_anagrams(words):
    groups = []
    for w in words:
        for g in groups:
            if sorted(g[0]) == sorted(w):
                g.append(w)
                break
        else:
            groups.append([w])
    return groups
```
hint: What do "eat", "tea" and "ate" have in common that "tan" doesn't?
hint: Sort the letters: all three become "aet". Use that as a dictionary key.
hint: `groups = defaultdict(list)`; for each word: `groups["".join(sorted(w))].append(w)`; return `list(groups.values())`.
approach:
1. **Understand:** split words into groups of anagrams; any order is fine.
2. **Examples:** ["eat", "tea", "tan", "ate", "nat", "bat"] → [eat, tea, ate], [tan, nat], [bat].
3. **Brute force:** for each word, compare with a representative of every existing group: O(n × groups).
4. **Pattern:** **grouping by a normalised key** in a hash map.
5. **Plan:** key = sorted letters; dict key → list of words; return the lists.
6. **Code and test:** the empty word "" has key "", which is fine.
walkthrough:
**Line by line**

- `defaultdict(list)`: looking up a new key creates an empty list, so `.append` always works.
- `"".join(sorted(w))`: `sorted("tea")` is `['a', 'e', 't']`; joining gives `"aet"`. Every anagram of "tea" gets the same key.
- `list(groups.values())`: the groups, in the order their keys first appeared.

**Trace:**

| word | key | groups |
|---|---|---|
| eat | aet | {aet: [eat]} |
| tea | aet | {aet: [eat, tea]} |
| tan | ant | {aet: [eat, tea], ant: [tan]} |
| ate | aet | {aet: [eat, tea, ate], ant: [tan]} |
| nat | ant | … ant: [tan, nat] |
| bat | abt | … abt: [bat] |

**Complexity:** O(n · k log k) time for n words of length up to k (sorting each word), O(n · k) space.

**Faster key:** a tuple of 26 letter counts makes each key O(k) instead of O(k log k): `counts = [0] * 26; for ch in w: counts[ord(ch) - 97] += 1; key = tuple(counts)`.
:::

:::exercise Subarrays that sum to k
Write `count_subarrays(nums, k)` returning how many **contiguous** subarrays add up to exactly `k`. Numbers can be negative. Make it O(n): fast for 100,000 numbers.
```python starter
def count_subarrays(nums, k):
    pass
```
```python check
test("count_subarrays", [
    (([1, 1, 1], 2), 2, "[1, 1, 1] with k = 2"),
    (([1, 2, 3], 3), 2, "[1, 2] and [3]"),
    (([1, -1, 1, -1], 0), 4, "negative numbers, k = 0"),
    (([], 0), 0, "an empty list"),
    (([5], 5), 1, "one number equal to k"),
    (([0, 0, 0], 0), 6, "zeros: every one of the 6 subarrays"),
    (([3, 4, 7, 2, -3, 1, 4, 2], 7), 4, "a longer list"),
])
def _ref(nums, k):
    counts = {0: 1}; cur = ans = 0
    for x in nums:
        cur += x; ans += counts.get(cur - k, 0); counts[cur] = counts.get(cur, 0) + 1
    return ans
import random
speed("count_subarrays", lambda n: ([_r.randint(-5, 5) for _r in [random.Random(n)] for _ in range(n)], 3), _ref,
      sizes=(1_000, 5_000, 100_000), what="numbers",
      tip="Trying every start and end is O(n²). Keep a running prefix sum and a dict counting how often each prefix sum has appeared: a subarray ending here sums to k when an earlier prefix equals current - k.")
```
```python solution
def count_subarrays(nums, k):
    counts = {0: 1}               # prefix sum -> how many times it has appeared
    current = answer = 0
    for x in nums:
        current += x
        answer += counts.get(current - k, 0)
        counts[current] = counts.get(current, 0) + 1
    return answer
```
```python slow
def count_subarrays(nums, k):
    answer = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                answer += 1
    return answer
```
hint: A subarray `i..j` sums to k exactly when `prefix[j + 1] - prefix[i] == k`.
hint: So at each position, count how many **earlier** prefix sums equal `current - k`. Keep those counts in a dict as you go.
hint: Start with `counts = {0: 1}` (the empty prefix). For each x: `current += x`; `answer += counts.get(current - k, 0)`; then `counts[current] += 1` (with get).
approach:
1. **Understand:** count (not find) contiguous subarrays with sum exactly k; negatives allowed, so no sliding window.
2. **Examples:** `[1, 1, 1]`, k = 2 → 2. `[0, 0, 0]`, k = 0 → 6 (every subarray).
3. **Brute force:** every start, extend to every end, keeping a running total: O(n²).
4. **Pattern:** **prefix sums + hash map of counts**: turn "sum of a range" into "difference of two prefix sums".
5. **Plan:** running sum; at each step add how many earlier prefix sums equal current − k; then record the current prefix sum.
6. **Code and test:** the `{0: 1}` start is what counts subarrays that begin at index 0.
walkthrough:
**Line by line**

- `counts = {0: 1}`: before any number, the prefix sum 0 has occurred once (the empty prefix). It lets a subarray starting at index 0 be counted.
- `current += x`: the prefix sum up to and including this number.
- `answer += counts.get(current - k, 0)`: every earlier prefix equal to `current - k` marks a start where the subarray up to here sums to k.
- Recording `current` **after** counting stops a prefix from pairing with itself (which would mean an empty subarray when k = 0).

**Trace** on `[1, 2, 3]`, k = 3:

| x | current | current − k | earlier count | answer | counts after |
|---|---|---|---|---|---|
| 1 | 1 | −2 | 0 | 0 | {0:1, 1:1} |
| 2 | 3 | 0 | 1 ([1, 2]) | 1 | {0:1, 1:1, 3:1} |
| 3 | 6 | 3 | 1 ([3]) | **2** | … |

**Complexity:** O(n) time, O(n) space.
:::

:::quiz
? In Two Sum with a dict, why store the current number only after checking for its complement?
+ So a number can't pair with itself
- It's faster
- Dicts can't be read and written in the same step
= With target 6 and [3], checking first means 3 doesn't find itself.
? What's a good key for grouping anagrams?
+ The word's letters in sorted order
- The word's length
- The first letter
= All anagrams share their sorted letters; non-anagrams don't.
? Why does "subarray sum equals k" start with counts = {0: 1}?
+ It counts subarrays that start at index 0
- To avoid a KeyError
- Because k is never 0
= The empty prefix has sum 0, so a prefix equal to k itself is a valid subarray.
? In longest consecutive sequence, why only start counting from x when x − 1 isn't in the set?
+ So each run is counted once from its start, keeping the total O(n)
- Because negative numbers aren't allowed
- To sort the numbers
= Starting from every number would recount the same run many times.
:::
