# Python syntax cheat sheet

Everything from the course on one page. The number in brackets is the lesson where it's taught.

## Basics

```python
print("Hello", name, sep=" ", end="\n")   # show values                 [2]
# comment                                  # ignored by Python           [2]
x = 10                                     # assign                      [3]
x, y = y, x                                # swap                        [3]
name = input("Name? ")                     # always returns a str        [6]
age = int(input("Age? "))                  # convert before math         [6]
type(x)                                    # what type is it?            [3]
```

| Type | Example | Notes |
|---|---|---|
| `int` | `42`, `1_000_000` | whole numbers [3] |
| `float` | `3.14`, `2.0` | approximate decimals [4] |
| `str` | `"hi"`, `'hi'`, `"""multi-line"""` | immutable text [5] |
| `bool` | `True`, `False` | capitalised [7] |
| `None` | `None` | "no value" [3] |
| `list` | `[1, 2, 3]` | ordered, changeable [12] |
| `tuple` | `(1, 2)`, `(1,)` | ordered, unchangeable [13] |
| `dict` | `{"a": 1}` | key → value [14] |
| `set` | `{1, 2}`, `set()` | unique, unordered [15] |

## Operators

| Operator | Meaning | Example |
|---|---|---|
| `+ - * /` | arithmetic (`/` always gives a float) | `7 / 2` → `3.5` [4] |
| `//` `%` `**` | floor divide, remainder, power | `7 // 2` → `3`, `7 % 2` → `1`, `2 ** 3` → `8` [4] |
| `+=` `-=` `*=` | update in place | `total += price` [4] |
| `==` `!=` `<` `>` `<=` `>=` | compare | `18 <= age < 65` [7] |
| `and` `or` `not` | combine conditions | `a and not b` [7] |
| `in` `not in` | membership | `"x" in text` [7] |
| `is` | same object (use for `None`) | `if result is None:` [19] |

**Falsy values:** `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None`, `False`. Everything else is truthy. [7]

## Strings

```python
s = "Python"
s[0], s[-1]            # 'P', 'n'                          [5]
s[1:4], s[::-1]        # 'yth', 'nohtyP'                    [5]
len(s)                 # 6                                  [5]
f"{name} is {age}"     # f-string                           [5]
f"{price:.2f}"         # 2 decimals: 3.50                   [5]
f"{n:,}"  f"{p:.1%}"   # 1,234,567   25.6%                  [5]
f"{x:>8}" f"{x:<8}"    # right / left align in 8 chars      [5]
```

| Method | Result [17] |
|---|---|
| `s.upper()` `s.lower()` `s.title()` | change case |
| `s.strip()` | remove surrounding whitespace |
| `s.split(",")` / `s.split()` | list of parts / split on any whitespace |
| `", ".join(items)` | glue strings together |
| `s.replace(a, b)` | swap text |
| `s.find(x)` / `s.count(x)` | index of first match (-1 if none) / count |
| `s.startswith(x)` `s.endswith(x)` | True / False |
| `s.isdigit()` `s.isalpha()` `s.isalnum()` | test contents |

## Decisions

```python
if score >= 90:                         # colon + indented block      [8]
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

kind = "even" if n % 2 == 0 else "odd"  # conditional expression       [8]

match command:                          # Python 3.10+                [8]
    case "start":
        ...
    case "stop" | "quit":
        ...
    case _:
        ...
```

## Loops

```python
while count < 5:                 # repeat while true              [9]
    count += 1

for item in items:               # each item                      [10]
for i in range(1, 6):            # 1, 2, 3, 4, 5  (stop excluded)  [10]
for i, item in enumerate(items, start=1):                         # [10]
for a, b in zip(list1, list2):                                    # [10]

break                            # leave the loop now             [11]
continue                         # skip to the next iteration     [11]
for x in items:
    ...
else:                            # runs only if no break          [11]
    ...
```

## Lists, tuples, dicts, sets

```python
nums.append(4); nums.insert(0, 9); nums.extend([5, 6])            # [12]
nums.remove(9); last = nums.pop(); del nums[0]                    # [12]
sorted(nums) / nums.sort()     # new list / in place (returns None)  [12]
copy = nums.copy()             # b = a does NOT copy               [12]

first, *rest = items           # unpacking                        [13]

d["key"] = value               # add or change                    [14]
d.get("key", default)          # safe lookup                      [14]
for k, v in d.items():         # keys and values                  [14]
counts[w] = counts.get(w, 0) + 1                                  # [14]

a | b, a & b, a - b            # union, intersection, difference  [15]
```

## Comprehensions [16]

```python
[x * 2 for x in nums]                  # transform
[x for x in nums if x > 0]             # filter (if at the end)
["even" if x % 2 == 0 else "odd" for x in nums]   # choose (if/else at the start)
{name: len(name) for name in names}    # dict
{w[0] for w in words}                  # set
(x * x for x in nums)                  # generator expression (lazy)  [31]
```

## Functions

```python
def area(width, height=1):             # default value               [18, 19]
    """Return the area."""             # docstring                   [18]
    return width * height

def total(*args, **kwargs): ...        # any positional / keyword args  [19]
def resize(img, *, width): ...         # width must be passed by name   [19]
def add(item, basket=None):            # never default to [] or {}      [19]
    if basket is None:
        basket = []

square = lambda n: n * n               # tiny anonymous function     [21]
sorted(people, key=lambda p: p.age)    # sort by a key               [21]
max(words, key=len)                                                  # [21]
any(x > 0 for x in nums); all(...)                                   # [21]

nonlocal count; global total           # assign outer / module names [20]
```

## Errors [23]

```python
try:
    value = int(text)
except ValueError as err:              # catch specific exceptions
    print("Not a number:", err)
else:
    print("worked")                    # only if no exception
finally:
    print("always runs")

raise ValueError("amount must be positive")

class InsufficientFunds(Exception):
    pass
```

| Exception | Usual cause |
|---|---|
| `SyntaxError` / `IndentationError` | typo or bad indentation; nothing runs |
| `NameError` | misspelled or undefined name |
| `TypeError` | wrong type, e.g. `"a" + 1` |
| `ValueError` | right type, bad value, e.g. `int("x")` |
| `IndexError` / `KeyError` | missing list position / dict key |
| `AttributeError` | method doesn't exist on that type |
| `ZeroDivisionError` | dividing by zero |

## Modules and files

```python
import math                      # math.sqrt(16)                     [24]
from collections import Counter  # Counter(words).most_common(3)     [24]
import datetime as dt                                                # [24]

if __name__ == "__main__":       # only when run directly            [24]
    main()

with open("notes.txt", "w", encoding="utf-8") as f:   # "r" read, "a" append  [25]
    f.write("hello\n")

import csv, json
rows = list(csv.DictReader(f))   # values are strings                [25]
data = json.loads(text); text = json.dumps(data, indent=2)           # [25]
```

## Classes

```python
class Dog(Animal):                       # inherit from Animal       [27, 28]
    species = "dog"                      # class attribute           [27]

    def __init__(self, name):
        super().__init__(name)           # run the parent's setup    [28]
        self.tricks = []                 # instance attribute        [27]

    def __repr__(self):                  # developer view            [29]
        return f"Dog({self.name!r})"

    def __eq__(self, other): ...         # ==                        [29]
    def __lt__(self, other): ...         # <, makes sorted() work    [29]
    def __len__(self): ...               # len()                     [29]

    @property
    def nickname(self):                  # read like an attribute    [30]
        return self.name[:3]

    @classmethod
    def from_text(cls, text):            # alternative constructor   [27]
        return cls(text.strip())

from dataclasses import dataclass, field
@dataclass(frozen=True, order=True)      # generates __init__, __repr__, __eq__  [30]
class Point:
    x: int
    y: int = 0
    tags: list = field(default_factory=list)
```

## Advanced

```python
def count_up(n):                         # generator                 [31]
    for i in range(n):
        yield i

import functools
def timed(func):                         # decorator                 [32]
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

from contextlib import contextmanager
@contextmanager
def tag(name):                           # context manager           [33]
    print(f"<{name}>")
    try:
        yield
    finally:
        print(f"</{name}>")

def mean(values: list[float]) -> float | None: ...                   # [34]

import itertools as it
it.chain(a, b); it.product(a, b); it.combinations(items, 2)          # [35]
it.groupby(sorted(items, key=k), key=k)                              # [35]
from functools import reduce, partial, lru_cache                     # [35]
```

## Big-O at a glance [36]

| Operation | list | dict / set |
|---|---|---|
| index / key lookup | O(1) | O(1) |
| `x in ...` | O(n) | O(1) |
| append / add | O(1) | O(1) |
| insert or remove at the front | O(n) | n/a |
| `sorted()` | O(n log n) | n/a |

**Rule of thumb:** a loop inside a loop over the same data is O(n²). A set or dict lookup usually removes the inner loop.
