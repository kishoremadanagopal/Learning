@@@ part
id: 3
title: Collections
level: Beginner
blurb: Store many values together with lists, tuples, dictionaries and sets, and transform them with comprehensions and string methods.

@@@ lesson
id: lists
title: Lists
minutes: 15
summary: Create, read, change, add to and sort lists, and understand references.
---
A **list** holds an ordered collection of values in square brackets. Lists can grow, shrink and change. They are **mutable**.

```python
fruits = ["apple", "banana", "cherry"]
numbers = [3, 1, 4, 1, 5]
mixed = ["Ada", 36, True]
empty = []
print(fruits, len(fruits))
```

### Reading items

Indexing and slicing work just like strings:

```python
fruits = ["apple", "banana", "cherry", "date"]
print(fruits[0], fruits[-1])
print(fruits[1:3])
```

### Changing items

Unlike strings, you can change list items in place:

```python
fruits = ["apple", "banana", "cherry"]
fruits[1] = "blueberry"
print(fruits)
```

### Adding and removing

| Method | What it does |
|---|---|
| `lst.append(x)` | add `x` to the end |
| `lst.insert(i, x)` | insert `x` at position `i` |
| `lst.extend(other)` | add every item from `other` |
| `lst.remove(x)` | remove the first `x` (error if missing) |
| `lst.pop()` | remove and return the last item |
| `lst.pop(i)` | remove and return item `i` |
| `del lst[i]` | delete item `i` |

```python
tasks = ["email"]
tasks.append("code review")
tasks.insert(0, "coffee")
tasks.extend(["lunch", "deploy"])
print(tasks)

done = tasks.pop(0)
tasks.remove("lunch")
print("Finished:", done)
print("Left:", tasks)
```

### Searching and counting

```python
nums = [3, 1, 4, 1, 5, 9]
print(4 in nums)
print(nums.index(5))     # position of the first 5
print(nums.count(1))
print(sum(nums), min(nums), max(nums))
```

### Sorting

`sorted(lst)` returns a **new** sorted list. `lst.sort()` sorts the list **in place** and returns `None`.

```python
nums = [3, 1, 4, 1, 5, 9]
print(sorted(nums))
print(sorted(nums, reverse=True))
print(nums)          # unchanged
nums.sort()
print(nums)          # now sorted
```

A classic bug is `nums = nums.sort()`, which sets `nums` to `None`.

### Lists are references

Assigning a list to another variable does **not** copy it. Both names refer to the same list:

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)        # a changed too!

c = a.copy()    # or a[:] or list(a)
c.append(5)
print(a, c)
```

### Lists of lists

Lists can contain other lists, which is handy for grids and tables:

```python
grid = [
    [1, 2, 3],
    [4, 5, 6],
]
print(grid[1][2])
for row in grid:
    print(row)
```

:::exercise Shopping list manager
Starting from `cart = ["bread", "milk"]`, write code that:

1. adds `"eggs"` to the end,
2. inserts `"coffee"` at the front,
3. removes `"milk"`,
4. sorts the list alphabetically in place.

The final list should be `['bread', 'coffee', 'eggs']`.
```python starter
cart = ["bread", "milk"]

print(cart)
```
```python check
assert cart == ["bread", "coffee", "eggs"], f"cart should be ['bread', 'coffee', 'eggs'] but is {cart}"
assert ".sort(" in __source__, "Use the .sort() method"
assert ".remove(" in __source__ or ".pop(" in __source__ or "del " in __source__, "Remove milk with .remove()"
```
```python solution
cart = ["bread", "milk"]
cart.append("eggs")
cart.insert(0, "coffee")
cart.remove("milk")
cart.sort()
print(cart)
```
hint: cart.append("eggs"), cart.insert(0, "coffee"), cart.remove("milk"), cart.sort()
:::

:::exercise Second largest
Write `second_largest(nums)` that returns the second largest **distinct** value. For `[4, 9, 2, 9, 7]` it returns `7`. You can assume there are at least two distinct values.
```python starter
def second_largest(nums):
    return max(nums)

print(second_largest([4, 9, 2, 9, 7]))
```
```python check
for nums, want in [([4, 9, 2, 9, 7], 7), ([1, 2], 1), ([5, 5, 5, 3], 3), ([-1, -5, -3], -3)]:
    got = second_largest(list(nums))
    assert got == want, f"second_largest({nums}) should be {want} but was {got}"
```
```python solution
def second_largest(nums):
    unique = sorted(set(nums))
    return unique[-2]

print(second_largest([4, 9, 2, 9, 7]))
```
hint: Remove duplicates with set(nums), sort the result with sorted(...), then take the item at index -2. (Sets come up two lessons from now.) You can also loop and track the top two values.
:::

:::quiz
? After `x = [1, 2]`, `y = x`, `y.append(3)`, what is `x`?
- [1, 2]
+ [1, 2, 3]
- An error
= `y = x` doesn't copy; both names refer to the same list.

? What does `[3, 1, 2].sort()` return?
- [1, 2, 3]
+ None
- [3, 2, 1]
= `.sort()` sorts in place and returns None. Use `sorted()` to get a new list back.

? How do you get the last item of a list `items`?
- `items[len(items)]`
+ `items[-1]`
- `items.last()`
= `items[len(items)]` is one past the end and raises IndexError.
:::

@@@ lesson
id: tuples-and-unpacking
title: Tuples and unpacking
minutes: 10
summary: Use immutable tuples for fixed groups of values and unpack them into variables.
---
A **tuple** is like a list that can't change. Use parentheses (or just commas):

```python
point = (3, 4)
rgb = 255, 128, 0
single = (42,)          # one-item tuple needs a trailing comma
print(point[0], rgb, type(single))
```

Trying to change a tuple fails:

```python error
point = (3, 4)
point[0] = 10
```

### When to use a tuple

Use a tuple for a **fixed group of related values** where position has meaning: coordinates `(x, y)`, a date `(2026, 10, 2)`, an RGB color. Use a list for a **collection of similar items** that may grow or shrink.

Tuples are also slightly faster and can be used as dictionary keys (lists can't), as you'll see next lesson.

### Unpacking

Unpacking assigns each item of a sequence to its own variable:

```python
point = (3, 4)
x, y = point
print(x, y)

name, age, city = ["Ada", 36, "London"]
print(f"{name} ({age}) lives in {city}")
```

The number of variables must match the number of items, unless you use a **starred** variable to collect the rest:

```python
first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)

head, *tail = "python"
print(head, tail)
```

### Returning several values from a function

Functions can return a tuple, which the caller unpacks:

```python
def min_max(nums):
    return min(nums), max(nums)

low, high = min_max([7, 2, 9, 4])
print(low, high)
```

### Unpacking in loops

```python
pairs = [("Ana", 91), ("Ben", 78)]
for name, score in pairs:
    print(name, "scored", score)
```

:::exercise Distance between points
Write `distance(p1, p2)` where each point is a tuple `(x, y)`. Unpack the tuples and return the straight-line distance using `((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5`.
```python starter
def distance(p1, p2):
    return 0

print(distance((0, 0), (3, 4)))
```
```python check
for a, b, want in [((0, 0), (3, 4), 5.0), ((1, 1), (1, 1), 0.0), ((-1, 2), (2, 6), 5.0)]:
    got = distance(a, b)
    assert abs(got - want) < 1e-9, f"distance({a}, {b}) should be {want} but was {got}"
```
```python solution
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

print(distance((0, 0), (3, 4)))
```
hint: Start with x1, y1 = p1 and x2, y2 = p2.
:::

:::quiz
? Which creates a tuple with one item?
- `(5)`
+ `(5,)`
- `tuple 5`
= `(5)` is just the number 5 in parentheses. The comma makes it a tuple.

? What is `b` after `a, *b = [1, 2, 3]`?
- 2
+ [2, 3]
- (2, 3)
= A starred target always collects the remaining items into a list.
:::

@@@ lesson
id: dictionaries
title: Dictionaries
minutes: 15
summary: Store key-value pairs, look things up fast, loop over items, and count with dicts.
---
A **dictionary** (`dict`) maps **keys** to **values**, like a real dictionary maps words to definitions. Instead of looking items up by position, you look them up by key.

```python
person = {
    "name": "Ada",
    "age": 36,
    "languages": ["English", "French"],
}
print(person["name"])
print(person["languages"][1])
```

### Adding, changing and removing

```python
stock = {"apples": 10, "pears": 4}
stock["bananas"] = 6        # add a new key
stock["apples"] -= 3        # change a value
del stock["pears"]          # remove a key
print(stock)
print(len(stock), "products")
```

### Missing keys

Looking up a key that doesn't exist raises a `KeyError`. Use `in` to check first, or `.get()` to supply a default:

```python
prices = {"tea": 2.5, "coffee": 3.0}
print("juice" in prices)
print(prices.get("juice"))         # None
print(prices.get("juice", 0))      # default value
```

### Looping over a dictionary

```python
scores = {"Ana": 91, "Ben": 78, "Cy": 85}
for name in scores:                 # keys
    print(name)
for name, score in scores.items():  # key and value
    print(f"{name}: {score}")
print(list(scores.values()))
```

Dictionaries remember the order in which keys were added.

### Counting with a dictionary

Counting things is one of the most common dictionary jobs:

```python
text = "the cat and the hat and the bat"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1
print(counts)

top = max(counts, key=counts.get)
print("Most common:", top)
```

### Keys must be immutable

Strings, numbers and tuples can be keys. Lists can't, because they can change.

```python
distances = {("London", "Paris"): 344, ("Paris", "Rome"): 1105}
print(distances[("London", "Paris")])
```

### Nested data

Real-world data (like JSON from a web API) is often dictionaries inside lists inside dictionaries:

```python
users = [
    {"name": "Ana", "roles": ["admin", "dev"]},
    {"name": "Ben", "roles": ["dev"]},
]
for user in users:
    if "admin" in user["roles"]:
        print(user["name"], "is an admin")
```

:::exercise Word frequency
Write `word_counts(text)` that returns a dictionary mapping each **lowercased** word to how many times it appears. Split on whitespace with `.split()`.

`word_counts("The cat saw the dog")` → `{'the': 2, 'cat': 1, 'saw': 1, 'dog': 1}`
```python starter
def word_counts(text):
    counts = {}

    return counts

print(word_counts("The cat saw the dog"))
```
```python check
got = word_counts("The cat saw the dog")
assert got == {"the": 2, "cat": 1, "saw": 1, "dog": 1}, f"Got {got}"
assert word_counts("a A a b") == {"a": 3, "b": 1}, "Remember to lowercase the words"
```
```python solution
def word_counts(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts

print(word_counts("The cat saw the dog"))
```
hint: Loop over text.lower().split() and use counts[word] = counts.get(word, 0) + 1.
:::

:::exercise Invert a phone book
Write `invert(book)` that swaps keys and values: `{"Ana": "555-1234"}` becomes `{"555-1234": "Ana"}`.
```python starter
def invert(book):
    return {}

print(invert({"Ana": "555-1234", "Ben": "555-9876"}))
```
```python check
got = invert({"Ana": "555-1234", "Ben": "555-9876"})
assert got == {"555-1234": "Ana", "555-9876": "Ben"}, f"Got {got}"
assert invert({}) == {}, "An empty dict should give an empty dict"
```
```python solution
def invert(book):
    result = {}
    for name, number in book.items():
        result[number] = name
    return result

print(invert({"Ana": "555-1234", "Ben": "555-9876"}))
```
hint: Loop with for name, number in book.items(): and set result[number] = name.
:::

:::quiz
? What does `{"a": 1}.get("b", 0)` return?
- None
+ 0
- KeyError
= `.get()` returns the default when the key is missing.

? Which can NOT be a dictionary key?
- `"name"`
- `(1, 2)`
+ `[1, 2]`
= Keys must be immutable (hashable). Lists can change, so they can't be keys.

? What does `for k, v in d.items():` give you?
+ Each key and its value
- Each value twice
- Only the keys
= `.items()` produces (key, value) pairs, which the loop unpacks.
:::

@@@ lesson
id: sets
title: Sets
minutes: 8
summary: Store unique values, remove duplicates and use union, intersection and difference.
---
A **set** is an unordered collection of **unique** values. Duplicates disappear automatically.

```python
tags = {"python", "code", "python", "fun"}
print(tags)
print(len(tags))

numbers = [1, 2, 2, 3, 3, 3]
print(set(numbers))       # remove duplicates
```

`{}` creates an empty **dictionary**, so use `set()` for an empty set.

### Fast membership tests

Checking `x in some_set` is very fast, even for millions of items, because sets use hashing (as dictionaries do). Checking `x in some_list` has to look at items one by one.

```python
seen = set()
for word in ["red", "blue", "red", "green", "blue"]:
    if word in seen:
        print("Duplicate:", word)
    seen.add(word)
```

### Set operations

```python
python_devs = {"Ana", "Ben", "Cy"}
java_devs = {"Ben", "Dee"}

print(python_devs | java_devs)   # union: in either
print(python_devs & java_devs)   # intersection: in both
print(python_devs - java_devs)   # difference: only Python
print(python_devs ^ java_devs)   # symmetric difference: in exactly one
```

### Adding and removing

```python
s = {1, 2}
s.add(3)
s.discard(10)    # no error if missing (remove() would raise KeyError)
print(s, 2 in s)
```

Sets have no order and no indexes, so `s[0]` doesn't work. Convert to a sorted list when order matters: `sorted(s)`.

:::exercise Common interests
Write `shared(a, b)` that takes two lists of hobbies and returns a **sorted list** of the hobbies that appear in both, without duplicates.
```python starter
def shared(a, b):
    return []

print(shared(["chess", "hiking", "chess", "art"], ["art", "chess", "golf"]))
```
```python check
got = shared(["chess", "hiking", "chess", "art"], ["art", "chess", "golf"])
assert got == ["art", "chess"], f"Expected ['art', 'chess'] but got {got}"
assert shared(["a"], ["b"]) == [], "No overlap should give []"
```
```python solution
def shared(a, b):
    return sorted(set(a) & set(b))

print(shared(["chess", "hiking", "chess", "art"], ["art", "chess", "golf"]))
```
hint: Convert both to sets, use &, then sorted(...).
:::

:::quiz
? What does `type({})` give?
- set
+ dict
= Empty braces make an empty dictionary. Use `set()` for an empty set.

? What is `{1, 2, 3} - {2, 4}`?
+ {1, 3}
- {4}
- {1, 3, 4}
= Difference keeps items in the first set that aren't in the second.
:::

@@@ lesson
id: comprehensions
title: Comprehensions
minutes: 12
summary: Build lists, dicts and sets in one readable line, with filters.
---
A **comprehension** builds a new collection from an existing one in a single expression. Compare the loop version with the comprehension:

```python
squares = []
for n in range(1, 6):
    squares.append(n * n)
print(squares)

squares = [n * n for n in range(1, 6)]
print(squares)
```

Read it as: "**n * n** for each **n** in **range(1, 6)**".

### Filtering with if

Add an `if` at the end to keep only some items:

```python
nums = [5, 12, 7, 20, 3, 18]
big = [n for n in nums if n > 10]
print(big)

words = ["apple", "Kiwi", "banana", "Fig"]
short_upper = [w.upper() for w in words if len(w) <= 4]
print(short_upper)
```

### Choosing a value with if/else

To transform every item differently (not filter), put the conditional expression at the **front**:

```python
nums = [1, 2, 3, 4, 5]
labels = ["even" if n % 2 == 0 else "odd" for n in nums]
print(labels)
```

### Dict and set comprehensions

```python
names = ["ana", "ben", "cy"]
lengths = {name: len(name) for name in names}
print(lengths)

prices = {"tea": 2.5, "cake": 4.0, "coffee": 3.0}
cheap = {item: p for item, p in prices.items() if p < 3.5}
print(cheap)

first_letters = {name[0] for name in ["Ana", "Alan", "Ben"]}
print(first_letters)
```

### Nested comprehensions

You can use two `for` clauses. They read in the same order as nested loops:

```python
pairs = [(x, y) for x in range(1, 3) for y in "ab"]
print(pairs)

grid = [[1, 2, 3], [4, 5, 6]]
flat = [n for row in grid for n in row]
print(flat)
```

### When not to use them

If a comprehension needs more than one `if` and two `for`s, or doesn't fit comfortably on a line or two, a regular loop is clearer. Readability beats cleverness.

:::exercise Clean the data
Write `clean(values)` that takes a list of strings, strips whitespace, drops empty strings, and converts the rest to integers, using **one list comprehension**.

`clean([" 4", "", "15 ", "  ", "8"])` → `[4, 15, 8]`
```python starter
def clean(values):
    return values

print(clean([" 4", "", "15 ", "  ", "8"]))
```
```python check
assert clean([" 4", "", "15 ", "  ", "8"]) == [4, 15, 8], f"Got {clean([' 4', '', '15 ', '  ', '8'])}"
assert clean([]) == [], "An empty list should give []"
assert "[" in __source__ and " for " in __source__, "Use a list comprehension"
```
```python solution
def clean(values):
    return [int(v.strip()) for v in values if v.strip()]

print(clean([" 4", "", "15 ", "  ", "8"]))
```
hint: [int(v.strip()) for v in values if v.strip()] — an empty string is falsy, so the if drops it.
:::

:::exercise Grade book
Given `scores = {"Ana": 91, "Ben": 58, "Cy": 74, "Dee": 45}`, build a dict comprehension `passed` that keeps only students with 60 or more.
```python starter
scores = {"Ana": 91, "Ben": 58, "Cy": 74, "Dee": 45}
passed = {}
print(passed)
```
```python check
assert passed == {"Ana": 91, "Cy": 74}, f"passed should be {{'Ana': 91, 'Cy': 74}} but is {passed}"
```
```python solution
scores = {"Ana": 91, "Ben": 58, "Cy": 74, "Dee": 45}
passed = {name: s for name, s in scores.items() if s >= 60}
print(passed)
```
hint: {name: s for name, s in scores.items() if s >= 60}
:::

:::quiz
? What is `[x * 2 for x in range(3)]`?
+ [0, 2, 4]
- [2, 4, 6]
- [0, 1, 2, 0, 1, 2]
= range(3) gives 0, 1 and 2, each doubled.

? Where does a filtering `if` go in a list comprehension?
- At the start
+ At the end
- Anywhere
= `[x for x in items if condition]`. A conditional *expression* (`a if c else b`) goes at the start instead.
:::

@@@ lesson
id: string-methods
title: String methods
minutes: 12
summary: Split, join, strip, replace, search and test text with built-in string methods.
---
Strings come with many **methods**: functions you call with a dot after the value. Because strings are immutable, they always return a **new** string.

### Changing case

```python
s = "hello World"
print(s.upper(), s.lower(), s.title(), s.capitalize())
```

### Cleaning up whitespace

```python
raw = "   ada@example.com \n"
print(f"[{raw.strip()}]")
print(f"[{raw.lstrip()}]")
print("--title--".strip("-"))
```

### Split and join

`split` breaks a string into a list. `join` glues a list of strings together with a separator. You'll use these two constantly.

```python
line = "Ana,36,London"
parts = line.split(",")
print(parts)

words = "  many   spaces here ".split()   # no argument: split on any whitespace
print(words)

print(" - ".join(["red", "green", "blue"]))
print("".join(reversed("stressed")))
```

### Search and replace

```python
s = "the rain in Spain"
print(s.find("ain"))          # index of first match, -1 if none
print(s.count("ain"))
print(s.replace("ain", "AIN"))
print(s.startswith("the"), s.endswith("pain"))
```

### Testing what a string contains

```python
print("123".isdigit(), "abc".isalpha(), "abc123".isalnum())
print("   ".isspace(), "Hello".istitle())
```

### Padding and alignment

```python
print("7".zfill(3))
print("menu".center(12, "*"))
print("left".ljust(8) + "|", "right".rjust(8) + "|")
```

### Method chaining

Since each method returns a new string, you can chain them:

```python
messy = "  Hello, World!  "
slug = messy.strip().lower().replace(",", "").replace("!", "").replace(" ", "-")
print(slug)
```

:::exercise Title case a headline
Write `headline(text)` that removes extra spaces between and around words and capitalises each word.

`headline("  the   quick brown  fox ")` → `"The Quick Brown Fox"`
```python starter
def headline(text):
    return text

print(headline("  the   quick brown  fox "))
```
```python check
assert headline("  the   quick brown  fox ") == "The Quick Brown Fox", f"Got {headline('  the   quick brown  fox ')!r}"
assert headline("python") == "Python", "Single word should be capitalised"
assert headline("   ") == "", "Only spaces should give an empty string"
```
```python solution
def headline(text):
    return " ".join(word.capitalize() for word in text.split())

print(headline("  the   quick brown  fox "))
```
hint: text.split() removes all extra spaces. Capitalise each word, then " ".join(...) them back together.
:::

:::exercise Palindrome checker
Write `is_palindrome(text)` that returns `True` if the text reads the same forwards and backwards, **ignoring case, spaces and punctuation**. Keep only characters where `ch.isalnum()` is true.

`is_palindrome("A man, a plan, a canal: Panama!")` → `True`
```python starter
def is_palindrome(text):
    return False

print(is_palindrome("A man, a plan, a canal: Panama!"))
```
```python check
assert is_palindrome("A man, a plan, a canal: Panama!") is True, "This famous sentence is a palindrome"
assert is_palindrome("racecar") is True
assert is_palindrome("Was it a car or a cat I saw?") is True
assert is_palindrome("hello") is False, "hello is not a palindrome"
```
```python solution
def is_palindrome(text):
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]

print(is_palindrome("A man, a plan, a canal: Panama!"))
```
hint: Build cleaned = "".join(ch.lower() for ch in text if ch.isalnum()), then compare it with cleaned[::-1].
:::

:::quiz
? What does `"a,b,c".split(",")` return?
+ ['a', 'b', 'c']
- 'abc'
- ('a', 'b', 'c')
= `split` always returns a list of strings.

? What does `"-".join(["x", "y", "z"])` return?
- ['x-y-z']
+ 'x-y-z'
- 'x-y-z-'
= The separator goes between items only.

? After `s = "hi"`, `s.upper()`, what is `s`?
+ 'hi'
- 'HI'
= String methods return new strings. To keep the result, write `s = s.upper()`.
:::
