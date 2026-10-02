@@@ part
id: 5
title: Robust Programs
level: Intermediate
blurb: Handle errors gracefully, use Python's standard library, work with CSV and JSON data, and test your code.

@@@ lesson
id: exceptions
title: Exceptions and error handling
minutes: 15
summary: Read tracebacks, catch errors with try/except, raise your own and clean up with finally.
---
An **exception** is Python's way of saying "something went wrong while running". If nothing handles it, the program stops and prints a **traceback**.

```python error
def divide(a, b):
    return a / b

print(divide(10, 2))
print(divide(1, 0))
```

### Reading a traceback

Read tracebacks from the **bottom up**:

1. The last line names the exception type and message: `ZeroDivisionError: division by zero`.
2. The lines above show the chain of calls, ending at the line that failed.

Common exceptions you'll meet:

| Exception | Typical cause |
|---|---|
| `NameError` | using a variable that doesn't exist (often a typo) |
| `TypeError` | wrong type, like `"a" + 1` |
| `ValueError` | right type, wrong value, like `int("abc")` |
| `IndexError` | list index out of range |
| `KeyError` | missing dictionary key |
| `AttributeError` | method or attribute doesn't exist, like `[].push(1)` |
| `ZeroDivisionError` | dividing by zero |

### Catching exceptions with try/except

Put risky code in `try`. If an exception happens, Python jumps to the matching `except` block instead of crashing:

```python
for text in ["42", "3.5", "abc"]:
    try:
        number = int(text)
        print("Got", number)
    except ValueError:
        print(f"{text!r} is not a whole number")
```

Catch **specific** exceptions. A bare `except:` hides real bugs, including typos in your own code.

### Several excepts, else and finally

```python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Can't divide by zero")
        return None
    except TypeError as err:          # 'as' gives you the exception object
        print("Bad input:", err)
        return None
    else:
        print("Division worked")      # runs only if no exception
        return result
    finally:
        print("-- done --")           # always runs

print(safe_divide(10, 4))
print(safe_divide(1, 0))
print(safe_divide("a", 2))
```

`finally` is for cleanup that must always happen, like closing a file or a network connection.

### Raising exceptions

Use `raise` when your function receives something it can't handle. Failing loudly and early is better than returning a wrong answer quietly.

```python
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("age must be an integer")
    if age < 0:
        raise ValueError(f"age can't be negative (got {age})")
    return age

try:
    set_age(-5)
except ValueError as e:
    print("Error:", e)
```

### Custom exceptions

For your own programs, create exception classes by inheriting from `Exception` (classes are covered in Part 6):

```python
class InsufficientFunds(Exception):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFunds(f"Need {amount - balance} more")
    return balance - amount

try:
    withdraw(50, 80)
except InsufficientFunds as e:
    print("Declined:", e)
```

### EAFP vs LBYL

Python style prefers **EAFP**: "Easier to Ask Forgiveness than Permission". Just try the operation and handle the failure, rather than checking every condition first (**LBYL**, "Look Before You Leap"):

```python
config = {"theme": "dark"}

# LBYL
if "font" in config:
    font = config["font"]
else:
    font = "default"

# EAFP
try:
    font = config["font"]
except KeyError:
    font = "default"
print(font)
```

:::exercise Safe number parser
Write `parse_number(text)` that returns an `int` if the text is a whole number, a `float` if it's a decimal number, and `None` if it's neither. Use `try/except`, not string checks.

`parse_number("42")` → `42`, `parse_number("2.5")` → `2.5`, `parse_number("hi")` → `None`
```python starter
def parse_number(text):
    return int(text)

print(parse_number("42"), parse_number("2.5"), parse_number("hi"))
```
```python check
assert parse_number("42") == 42 and type(parse_number("42")) is int, "'42' should give the int 42"
assert parse_number("2.5") == 2.5 and type(parse_number("2.5")) is float, "'2.5' should give the float 2.5"
assert parse_number("-7") == -7, "'-7' should give -7"
assert parse_number("hi") is None, "'hi' should give None"
assert parse_number("") is None, "An empty string should give None"
assert "except" in __source__, "Use try/except"
```
```python solution
def parse_number(text):
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return None

print(parse_number("42"), parse_number("2.5"), parse_number("hi"))
```
hint: Try int(text) first and return it. If that raises ValueError, try float(text). If that fails too, return None.
:::

:::exercise Validate an order
Write `validate_quantity(qty)` that returns `qty` if it's an `int` from 1 to 100. Otherwise it should **raise** `ValueError` with a helpful message.
```python starter
def validate_quantity(qty):
    return qty

print(validate_quantity(5))
```
```python check
assert validate_quantity(1) == 1 and validate_quantity(100) == 100, "1 and 100 are valid"
for bad in [0, 101, -3]:
    try:
        validate_quantity(bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"validate_quantity({bad}) should raise ValueError")
try:
    validate_quantity("5")
except (ValueError, TypeError):
    pass
else:
    raise AssertionError("A string like '5' should be rejected")
```
```python solution
def validate_quantity(qty):
    if not isinstance(qty, int) or not 1 <= qty <= 100:
        raise ValueError(f"quantity must be a whole number from 1 to 100, got {qty!r}")
    return qty

print(validate_quantity(5))
```
hint: if not isinstance(qty, int) or not 1 <= qty <= 100: raise ValueError("...")
:::

:::quiz
? Which part of a try statement always runs?
- else
- except
+ finally
= `finally` runs whether or not an exception happened.

? What does `int("12a")` raise?
- TypeError
+ ValueError
- SyntaxError
= The type (str) is acceptable, but the value can't be converted.

? Where should you start reading a traceback?
+ The last line
- The first line
- The middle
= The bottom line names the error; the lines above show how the program got there.
:::

@@@ lesson
id: modules-and-stdlib
title: Modules and the standard library
minutes: 15
summary: Import modules in different ways and tour the most useful parts of Python's standard library.
---
A **module** is a file of Python code you can reuse. Python ships with a huge **standard library** ("batteries included"), so you rarely start from zero.

### Ways to import

```python
import math
print(math.sqrt(16))

from math import pi, floor
print(pi, floor(2.9))

import statistics as stats
print(stats.mean([2, 4, 9]))
```

- `import module` keeps names tidy: `math.sqrt` makes it obvious where `sqrt` comes from.
- `from module import name` is shorter for names you use often.
- `import module as alias` shortens long names. Some aliases are conventions, like `import numpy as np`.
- Avoid `from module import *`: it dumps unknown names into your file.

### A tour of useful modules

**random**: random numbers and choices

```python
import random
print(random.randint(1, 6))
print(random.choice(["rock", "paper", "scissors"]))
deck = list(range(1, 11))
random.shuffle(deck)
print(deck[:3])
```

Your output will differ every run. That's the point.

**datetime**: dates and times

```python
from datetime import date, timedelta
start = date(2026, 1, 15)
deadline = start + timedelta(days=45)
print(deadline, deadline.strftime("%A, %d %B %Y"))
print((deadline - start).days, "days")
```

**collections**: specialised containers

```python
from collections import Counter, defaultdict, deque

votes = Counter(["red", "blue", "red", "green", "red"])
print(votes.most_common(2))

groups = defaultdict(list)
for name in ["Ana", "Ben", "Alan", "Bea"]:
    groups[name[0]].append(name)
print(dict(groups))

queue = deque(["a", "b"])
queue.appendleft("first")
print(queue.popleft(), queue)
```

**string** and **textwrap**

```python
import string, textwrap
print(string.ascii_lowercase)
print(string.punctuation)
long_text = "Python is a programming language that lets you work quickly and integrate systems more effectively."
print(textwrap.fill(long_text, width=40))
```

**itertools** and **functools** have powerful tools for loops and functions; they get their own lesson in Part 7.

### Your own modules

Any `.py` file is a module. If you save functions in `helpers.py`, another file in the same folder can use `import helpers`. A folder of modules with an `__init__.py` file is a **package**.

### if __name__ == "__main__"

When Python runs a file directly, its `__name__` is `"__main__"`. When the file is imported, `__name__` is the module's name. This lets a file work both as a script and as an importable module:

```python
def main():
    print("Running as a script")

if __name__ == "__main__":
    main()
```

### Third-party packages

Beyond the standard library, the Python Package Index (PyPI) has over half a million packages, installed with `pip` on your own computer:

```py-static
pip install requests
```

This browser editor can only use the standard library. The last lesson explains how to set Python up on your computer.

:::exercise Most common letters
Use `collections.Counter` to write `top_letters(text, n)` that returns the `n` most common **letters** (ignore case, spaces and punctuation) as a list of `(letter, count)` tuples.

`top_letters("Hello World", 2)` → `[('l', 3), ('o', 2)]`
```python starter
def top_letters(text, n):
    return []

print(top_letters("Hello World", 2))
```
```python check
assert top_letters("Hello World", 2) == [("l", 3), ("o", 2)], f"Got {top_letters('Hello World', 2)}"
assert top_letters("aAbB!!", 1)[0][1] == 2, "Count letters case-insensitively"
assert "Counter" in __source__, "Use collections.Counter"
```
```python solution
from collections import Counter

def top_letters(text, n):
    letters = [ch for ch in text.lower() if ch.isalpha()]
    return Counter(letters).most_common(n)

print(top_letters("Hello World", 2))
```
hint: Build a list of lowercase letters with a comprehension (ch.isalpha()), pass it to Counter, and call .most_common(n).
:::

:::exercise Days until
Write `days_until(year, month, day, today)` that returns the number of days from the `date` object `today` to the given date (negative if it's in the past). Use `datetime.date`.
```python starter
from datetime import date

def days_until(year, month, day, today):
    return 0

print(days_until(2026, 12, 25, date(2026, 10, 2)))
```
```python check
from datetime import date as _d
assert days_until(2026, 12, 25, _d(2026, 10, 2)) == 84, f"Expected 84, got {days_until(2026, 12, 25, _d(2026, 10, 2))}"
assert days_until(2026, 1, 1, _d(2026, 1, 1)) == 0, "Same day should be 0"
assert days_until(2025, 12, 31, _d(2026, 1, 1)) == -1, "Yesterday should be -1"
```
```python solution
from datetime import date

def days_until(year, month, day, today):
    return (date(year, month, day) - today).days

print(days_until(2026, 12, 25, date(2026, 10, 2)))
```
hint: Subtracting two dates gives a timedelta; its .days attribute is the number of days.
:::

:::quiz
? What does `if __name__ == "__main__":` check?
+ Whether the file is being run directly rather than imported
- Whether a function called main exists
- Whether Python is installed
= `__name__` is "__main__" only for the file you run directly.

? Which import style is generally discouraged?
- `import math`
- `from math import sqrt`
+ `from math import *`
= Star imports pull in unknown names and make code harder to read.
:::

@@@ lesson
id: files-csv-json
title: Files, CSV and JSON
minutes: 15
summary: Read and write files with open and with, and parse CSV and JSON data.
---
Programs often read data from files and save results back. On your own computer you use `open()`:

```py-static
# Write a file
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("first line\n")
    f.write("second line\n")

# Read it back, one line at a time
with open("notes.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

| Mode | Meaning |
|---|---|
| `"r"` | read (the default) |
| `"w"` | write, replacing the file |
| `"a"` | append to the end |
| `"x"` | create, failing if the file exists |

The `with` statement closes the file automatically, even if an error happens. Always use it.

### Practising in the browser

This browser editor has no real disk, so the runnable examples use `io.StringIO`, an in-memory object that behaves exactly like an open text file. Everything you learn transfers directly: replace `io.StringIO(...)` with `open("file.txt")`.

```python
import io

f = io.StringIO("apples 3\npears 5\nplums 2\n")
total = 0
for line in f:
    name, count = line.split()
    total += int(count)
    print(f"{name:<8}{count:>3}")
print("Total:", total)
```

Useful file methods: `f.read()` returns the whole content as one string, `f.readlines()` returns a list of lines, and looping over `f` reads one line at a time (best for big files).

### CSV: spreadsheet-style data

CSV (comma-separated values) is the most common format for tables. The `csv` module handles quoting and commas inside values for you.

```python
import csv, io

data = io.StringIO("""name,department,salary
Ana,Engineering,95000
Ben,Sales,62000
"Cy, Jr.",Engineering,88000
""")

reader = csv.DictReader(data)
by_dept = {}
for row in reader:
    salary = int(row["salary"])          # CSV values are always strings
    by_dept.setdefault(row["department"], []).append(salary)

for dept, salaries in by_dept.items():
    print(f"{dept}: average {sum(salaries) / len(salaries):,.0f}")
```

Writing CSV works the same way with `csv.writer` or `csv.DictWriter`:

```python
import csv, io

out = io.StringIO()
writer = csv.writer(out)
writer.writerow(["city", "temp"])
writer.writerows([["Oslo", -2], ["Lima", 19]])
print(out.getvalue())
```

### JSON: data for the web

JSON is how most web APIs exchange data. It maps neatly onto Python dicts and lists.

```python
import json

text = '{"user": "ada", "active": true, "tags": ["math", "code"], "score": null}'
data = json.loads(text)          # JSON string -> Python
print(data["tags"], data["active"], data["score"])

data["score"] = 99
print(json.dumps(data, indent=2))   # Python -> JSON string
```

Note how JSON's `true`/`null` become Python's `True`/`None`. With real files, use `json.load(f)` and `json.dump(data, f)` (no `s`).

:::exercise Total sales from CSV
Write `total_by_product(csv_text)` that takes CSV text with columns `product,qty,price` and returns a dict mapping each product to its total revenue (`qty * price`), rounded to 2 decimals.
```python starter
import csv, io

def total_by_product(csv_text):
    totals = {}
    return totals

sample = """product,qty,price
pen,10,1.5
book,2,12.99
pen,4,1.5
"""
print(total_by_product(sample))
```
```python check
sample = "product,qty,price\npen,10,1.5\nbook,2,12.99\npen,4,1.5\n"
got = total_by_product(sample)
assert got == {"pen": 21.0, "book": 25.98}, f"Expected {{'pen': 21.0, 'book': 25.98}} but got {got}"
assert total_by_product("product,qty,price\n") == {}, "A header-only CSV should give {}"
```
```python solution
import csv, io

def total_by_product(csv_text):
    totals = {}
    for row in csv.DictReader(io.StringIO(csv_text)):
        revenue = int(row["qty"]) * float(row["price"])
        totals[row["product"]] = totals.get(row["product"], 0) + revenue
    return {name: round(value, 2) for name, value in totals.items()}

sample = """product,qty,price
pen,10,1.5
book,2,12.99
pen,4,1.5
"""
print(total_by_product(sample))
```
hint: Loop over csv.DictReader(io.StringIO(csv_text)). Convert qty with int() and price with float(), and accumulate with totals.get(name, 0) + revenue. Round at the end.
:::

:::exercise Active users from JSON
Write `active_names(json_text)` that parses a JSON list of user objects and returns a sorted list of the `name`s of users whose `active` field is `true`.
```python starter
import json

def active_names(json_text):
    return []

sample = '[{"name": "ben", "active": true}, {"name": "ana", "active": true}, {"name": "cy", "active": false}]'
print(active_names(sample))
```
```python check
sample = '[{"name": "ben", "active": true}, {"name": "ana", "active": true}, {"name": "cy", "active": false}]'
assert active_names(sample) == ["ana", "ben"], f"Got {active_names(sample)}"
assert active_names("[]") == [], "An empty JSON list should give []"
```
```python solution
import json

def active_names(json_text):
    users = json.loads(json_text)
    return sorted(u["name"] for u in users if u["active"])

sample = '[{"name": "ben", "active": true}, {"name": "ana", "active": true}, {"name": "cy", "active": false}]'
print(active_names(sample))
```
hint: users = json.loads(json_text), then sorted(u["name"] for u in users if u["active"]).
:::

:::quiz
? Why use `with open(...) as f:`?
+ The file is closed automatically, even after an error
- It reads faster
- It's required to write files
= `with` guarantees cleanup. Forgetting to close files can lose data.

? What does `json.loads('{"a": null}')` return?
- {'a': 'null'}
+ {'a': None}
- {'a': 0}
= JSON null becomes Python None.

? What type are values read by `csv.DictReader`?
- They're converted automatically
+ Always strings
= CSV has no types, so every value arrives as a string. Convert numbers yourself.
:::

@@@ lesson
id: testing-and-debugging
title: Testing and debugging
minutes: 15
summary: Find bugs systematically, check assumptions with assert, and write unit tests.
---
Every programmer writes bugs. The skill is finding and fixing them quickly, and catching them before your users do.

### A debugging routine

1. **Read the error message** carefully, bottom line first.
2. **Reproduce** the bug with the smallest possible input.
3. **Inspect** values: add `print()` calls (f-strings with `=` are great for this) to see what the program actually has, rather than what you assume.
4. **Form a hypothesis**, change one thing, and test again.
5. **Explain the code out loud**, line by line. "Rubber duck debugging" works surprisingly often.

```python
def average_positive(nums):
    positives = [n for n in nums if n > 0]
    print(f"{nums=} {positives=}")       # debug print, remove later
    return sum(positives) / len(nums)    # bug!

print(average_positive([4, -2, 6]))
```

The debug print shows `positives` has 2 items while we divide by 3. The fix is `len(positives)`.

### assert: check your assumptions

`assert condition, message` raises `AssertionError` if the condition is false. Use it to catch impossible situations early:

```python
def apply_discount(price, percent):
    assert 0 <= percent <= 100, f"percent out of range: {percent}"
    return price * (1 - percent / 100)

print(apply_discount(80, 25))
```

Asserts can be switched off when Python runs with optimisation, so don't use them to validate user input. Raise `ValueError` for that.

### Writing tests

A **test** is code that checks other code. The simplest tests are functions full of asserts:

```python
def slugify(title):
    return "-".join(title.lower().split())

def test_slugify():
    assert slugify("Hello World") == "hello-world"
    assert slugify("  Many   Spaces ") == "many-spaces"
    assert slugify("") == ""
    print("all slugify tests passed")

test_slugify()
```

Think about **edge cases**: empty input, one item, negative numbers, duplicates, very large values. Bugs live at the edges.

### unittest: the built-in test framework

`unittest` organises tests into classes and gives clear reports. (In real projects, many developers use `pytest`, which runs plain `assert` tests like the one above with nicer output.)

```python
import sys
import unittest

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

class TestLeapYear(unittest.TestCase):
    def test_typical_leap_year(self):
        self.assertTrue(is_leap_year(2024))

    def test_century_is_not_leap(self):
        self.assertFalse(is_leap_year(1900))

    def test_every_400_years_is_leap(self):
        self.assertTrue(is_leap_year(2000))

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLeapYear)
result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
print("passed" if result.wasSuccessful() else "failed")
```

On your computer you'd normally run tests with `python -m unittest` or `pytest` from the terminal.

### Test-driven development (TDD)

A popular workflow: write a failing test that describes what you want, write just enough code to pass it, then tidy up ("red, green, refactor"). The exercises in this course work the same way: the checker is a set of tests.

:::exercise Fix the bug
This function should return the largest number in a list, but it has a bug that only shows up for some inputs. Find and fix it.
```python starter
def largest(nums):
    biggest = 0
    for n in nums:
        if n > biggest:
            biggest = n
    return biggest

print(largest([3, 9, 4]))
print(largest([-5, -2, -8]))
```
```python check
assert largest([3, 9, 4]) == 9
assert largest([-5, -2, -8]) == -2, f"largest([-5, -2, -8]) should be -2 but was {largest([-5, -2, -8])}"
assert largest([7]) == 7
assert "max(" not in __source__, "Fix the loop instead of using max()"
```
```python solution
def largest(nums):
    biggest = nums[0]
    for n in nums[1:]:
        if n > biggest:
            biggest = n
    return biggest

print(largest([3, 9, 4]))
print(largest([-5, -2, -8]))
```
hint: Starting biggest at 0 breaks when every number is negative. Start it at nums[0] instead.
:::

:::exercise Write the tests
The function `normalize_phone` is finished. Your job is to write `test_normalize_phone()` containing **at least four** `assert` statements that would catch bugs, then call it.

Expected behaviour: it keeps only digits, and returns `None` unless exactly 10 digits remain. `"(555) 123-4567"` → `"5551234567"`.
```python starter
def normalize_phone(text):
    digits = "".join(ch for ch in text if ch.isdigit())
    return digits if len(digits) == 10 else None

def test_normalize_phone():
    pass

test_normalize_phone()
print("tests passed")
```
```python check
assert __source__.split("def test_normalize_phone", 1)[1].count("assert") >= 4, "Write at least four assert statements inside test_normalize_phone"
_real = normalize_phone
def _broken(text):
    return "".join(ch for ch in text if ch.isdigit())
normalize_phone = _broken
try:
    test_normalize_phone()
except AssertionError:
    pass
else:
    raise AssertionError("Your tests didn't catch a broken version that never returns None. Add a test for an invalid number.")
normalize_phone = _real
test_normalize_phone()
```
```python solution
def normalize_phone(text):
    digits = "".join(ch for ch in text if ch.isdigit())
    return digits if len(digits) == 10 else None

def test_normalize_phone():
    assert normalize_phone("(555) 123-4567") == "5551234567"
    assert normalize_phone("555.123.4567") == "5551234567"
    assert normalize_phone("123") is None
    assert normalize_phone("") is None
    assert normalize_phone("555-123-45678") is None

test_normalize_phone()
print("tests passed")
```
hint: Test a formatted valid number, another valid format, a too-short number, an empty string and a too-long number.
:::

:::quiz
? What's the first thing to do when you see an error?
+ Read the last line of the traceback
- Rewrite the function from scratch
- Add try/except around everything
= The message usually tells you exactly what went wrong and where.

? Why shouldn't you use `assert` to validate user input?
- It's too slow
+ Asserts can be disabled when Python runs with optimisation
- It only works with numbers
= With `python -O`, asserts are skipped. Raise ValueError for real validation.
:::
