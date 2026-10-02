@@@ part
id: 4
title: Functions
level: Intermediate
blurb: Package code into reusable functions, master parameters and scope, and pass functions around as values.

@@@ lesson
id: functions-basics
title: Defining functions
minutes: 12
summary: Write functions with def, return results, document them, and understand print vs return.
---
A **function** is a named, reusable block of code. You've already used many: `print`, `len`, `sorted`. Now you'll write your own.

```python
def greet(name):
    """Return a friendly greeting for name."""
    return f"Hello, {name}!"

message = greet("Ada")
print(message)
print(greet("Alan"))
```

- `def` starts the definition, followed by the name and **parameters** in parentheses.
- The indented block is the **body**. It doesn't run until the function is **called**.
- `return` sends a value back to the caller and ends the function immediately.
- The string right under `def` is a **docstring**: documentation that tools and `help()` can read.

The values you pass in when calling (`"Ada"`) are called **arguments**.

### Why functions?

- **Reuse**: write once, call many times.
- **Names**: `calculate_tax(price)` explains itself better than the raw formula.
- **Testing**: small functions are easy to check in isolation.
- **Don't Repeat Yourself (DRY)**: fix a bug in one place instead of five.

### print vs return

This is the biggest beginner confusion. `print` **shows** a value on screen. `return` **hands it back** so the program can keep using it.

```python
def add_print(a, b):
    print(a + b)

def add_return(a, b):
    return a + b

x = add_print(2, 3)     # shows 5, but x gets nothing
y = add_return(2, 3)    # shows nothing, y gets 5
print("x =", x)
print("y =", y, "and y * 10 =", y * 10)
```

A function without a `return` gives back `None`. Prefer returning values; let the caller decide whether to print.

### Returning early

`return` can appear anywhere. It's often used to handle special cases first, which keeps the main logic unindented:

```python
def describe_age(age):
    if age < 0:
        return "invalid"
    if age < 13:
        return "child"
    if age < 20:
        return "teenager"
    return "adult"

for a in (-1, 8, 15, 42):
    print(a, describe_age(a))
```

### Functions calling functions

```python
def area(width, height):
    return width * height

def paint_needed(width, height, coats=2):
    litres_per_m2 = 0.1
    return area(width, height) * coats * litres_per_m2

print(f"{paint_needed(4, 2.5):.1f} litres")
```

:::exercise Average of a list
Write `average(nums)` that **returns** the mean of a list of numbers. If the list is empty, return `0` instead of crashing.
```python starter
def average(nums):
    print(sum(nums) / len(nums))

result = average([2, 4, 9])
print(result)
```
```python check
assert average([2, 4, 9]) == 5, f"average([2, 4, 9]) should be 5 but was {average([2, 4, 9])}"
assert average([10]) == 10, "average([10]) should be 10"
assert average([]) == 0, "average([]) should return 0"
```
```python solution
def average(nums):
    if not nums:
        return 0
    return sum(nums) / len(nums)

result = average([2, 4, 9])
print(result)
```
hint: Replace print with return. Handle the empty list first: if not nums: return 0.
:::

:::exercise BMI category
Write `bmi(weight_kg, height_m)` returning `weight / height ** 2` rounded to 1 decimal place, and `bmi_category(value)` returning `"underweight"` (below 18.5), `"normal"` (below 25), `"overweight"` (below 30) or `"obese"`.
```python starter
def bmi(weight_kg, height_m):
    pass

def bmi_category(value):
    pass

b = bmi(70, 1.75)
print(b, bmi_category(b))
```
```python check
assert bmi(70, 1.75) == 22.9, f"bmi(70, 1.75) should be 22.9 but was {bmi(70, 1.75)}"
assert bmi(50, 1.8) == 15.4, f"bmi(50, 1.8) should be 15.4 but was {bmi(50, 1.8)}"
for v, want in [(17.0, "underweight"), (18.5, "normal"), (24.9, "normal"), (25.0, "overweight"), (29.9, "overweight"), (30.0, "obese")]:
    assert bmi_category(v) == want, f"bmi_category({v}) should be {want!r} but was {bmi_category(v)!r}"
```
```python solution
def bmi(weight_kg, height_m):
    return round(weight_kg / height_m ** 2, 1)

def bmi_category(value):
    if value < 18.5:
        return "underweight"
    if value < 25:
        return "normal"
    if value < 30:
        return "overweight"
    return "obese"

b = bmi(70, 1.75)
print(b, bmi_category(b))
```
hint: bmi: return round(weight_kg / height_m ** 2, 1). bmi_category: a chain of if value < ...: return ... checks from low to high.
:::

:::quiz
? What does a function return if it has no `return` statement?
- 0
+ None
- An empty string
= Every function returns something; without `return`, it's None.

? What's the difference between a parameter and an argument?
+ Parameters are the names in `def`; arguments are the values passed in a call
- They are the same thing
- Arguments are in `def`; parameters are in the call
= In `def f(x)` x is a parameter; in `f(5)` the 5 is an argument.
:::

@@@ lesson
id: parameters
title: Parameters in depth
minutes: 15
summary: Default values, keyword arguments, *args, **kwargs, and the mutable default trap.
---
Python gives you flexible ways to pass arguments.

### Positional and keyword arguments

```python
def describe_pet(name, animal="dog"):
    return f"{name} is a {animal}"

print(describe_pet("Rex"))                     # uses the default
print(describe_pet("Tom", "cat"))              # positional
print(describe_pet(animal="parrot", name="Polly"))  # keywords, any order
```

Keyword arguments make calls self-explanatory: `connect(host="db", timeout=5)` is clearer than `connect("db", 5)`. Parameters with defaults must come after those without.

### *args: any number of positional arguments

A parameter with `*` collects extra positional arguments into a **tuple**:

```python
def total(*numbers):
    print("received", numbers)
    return sum(numbers)

print(total(1, 2))
print(total(5, 10, 15, 20))
```

### **kwargs: any number of keyword arguments

A parameter with `**` collects extra keyword arguments into a **dict**:

```python
def make_profile(name, **details):
    profile = {"name": name}
    profile.update(details)
    return profile

print(make_profile("Ada", job="mathematician", born=1815))
```

### Unpacking when calling

`*` and `**` also work the other way: they spread a list or dict into arguments.

```python
def volume(length, width, height):
    return length * width * height

dims = [2, 3, 4]
print(volume(*dims))

opts = {"length": 1, "width": 5, "height": 2}
print(volume(**opts))
```

### Keyword-only parameters

Parameters after a bare `*` must be passed by keyword. This prevents confusing calls:

```python
def resize(image, *, width, height):
    return f"{image} -> {width}x{height}"

print(resize("cat.png", width=200, height=100))
```

Calling `resize("cat.png", 200, 100)` would raise a `TypeError`.

### The mutable default trap

Default values are created **once**, when the function is defined, not each time it's called. A mutable default like `[]` is shared between calls:

```python
def add_item_buggy(item, basket=[]):
    basket.append(item)
    return basket

print(add_item_buggy("apple"))
print(add_item_buggy("pear"))    # surprise: apple is still there

def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket

print(add_item("apple"))
print(add_item("pear"))
```

Use `None` as the default and create the list inside the function.

:::exercise Flexible greeting
Write `greet(*names, greeting="Hello")` that returns one greeting for all names, joined by `" and "`.

- `greet("Ana")` → `"Hello, Ana!"`
- `greet("Ana", "Ben", greeting="Hi")` → `"Hi, Ana and Ben!"`
- `greet()` → `"Hello, nobody!"`
```python starter
def greet(names, greeting):
    pass

print(greet("Ana", "Ben", greeting="Hi"))
```
```python check
assert greet("Ana") == "Hello, Ana!", f"greet('Ana') gave {greet('Ana')!r}"
assert greet("Ana", "Ben", greeting="Hi") == "Hi, Ana and Ben!", f"Got {greet('Ana', 'Ben', greeting='Hi')!r}"
assert greet("A", "B", "C") == "Hello, A and B and C!", f"Got {greet('A', 'B', 'C')!r}"
assert greet() == "Hello, nobody!", f"greet() gave {greet()!r}"
```
```python solution
def greet(*names, greeting="Hello"):
    who = " and ".join(names) if names else "nobody"
    return f"{greeting}, {who}!"

print(greet("Ana", "Ben", greeting="Hi"))
```
hint: Use def greet(*names, greeting="Hello"):. names is a tuple; " and ".join(names) joins it. An empty tuple is falsy.
:::

:::exercise Fix the shared list
This function has the mutable default bug. Fix it so that every call without a `log` argument starts with a fresh list.
```python starter
def record(event, log=[]):
    log.append(event)
    return log

print(record("start"))
print(record("stop"))
```
```python check
a = record("x")
b = record("y")
assert a == ["x"] and b == ["y"], f"Each call should start fresh, got {a} and {b}"
mine = ["old"]
assert record("new", mine) == ["old", "new"], "Passing a list should still append to it"
```
```python solution
def record(event, log=None):
    if log is None:
        log = []
    log.append(event)
    return log

print(record("start"))
print(record("stop"))
```
hint: Change the default to None, and inside the function write: if log is None: log = []
:::

:::quiz
? Inside `def f(*args)`, what type is `args`?
+ tuple
- list
- dict
= `*args` collects positional arguments into a tuple.

? What does `f(**{"a": 1, "b": 2})` do?
- Passes one dict argument
+ Calls `f(a=1, b=2)`
- Raises an error
= `**` unpacks a dict into keyword arguments.

? Why is `def f(x=[])` risky?
+ The same list is reused across calls
- Lists can't be defaults
- It makes x a tuple
= Defaults are evaluated once at definition time, so all calls share one list.
:::

@@@ lesson
id: scope-and-closures
title: Scope and closures
minutes: 12
summary: Where variables live (LEGB), global and nonlocal, and functions that remember values.
---
**Scope** is the region of code where a name is visible. Variables created inside a function are **local**: they exist only while the function runs.

```python
def make_greeting():
    message = "hi"          # local variable
    return message

print(make_greeting())
print("message" in dir())   # it doesn't exist out here
```

### The LEGB rule

When Python looks up a name, it searches four places in order:

1. **L**ocal: inside the current function
2. **E**nclosing: inside any outer functions
3. **G**lobal: at the top level of the file
4. **B**uilt-in: names like `print` and `len`

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print("inner sees:", x)
    inner()
    print("outer sees:", x)

outer()
print("module sees:", x)
```

### Reading vs assigning globals

A function can **read** a global variable, but assigning to a name inside a function creates a new local one instead:

```python
counter = 0

def bump():
    global counter      # say we mean the global one
    counter += 1

bump()
bump()
print(counter)
```

Use `global` sparingly. Functions that change globals are hard to test and reason about. Passing values in and returning results is almost always better.

### Closures: functions that remember

An inner function can use variables from the enclosing function, and it **keeps** them even after the outer function has returned. This is called a **closure**.

```python
def make_multiplier(factor):
    def multiply(n):
        return n * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(10), triple(10))
```

To **change** an enclosing variable, declare it `nonlocal`:

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

clicks = make_counter()
clicks()
clicks()
print(clicks())
```

Each call to `make_counter()` creates a separate `count`, so you can have several independent counters. Closures are the foundation of decorators, which you'll meet in Part 7.

:::exercise Running average
Write `make_averager()` that returns a function. Each time you call the returned function with a number, it returns the average of **all numbers passed so far**.

```output
avg = make_averager()
avg(10) -> 10.0
avg(20) -> 15.0
avg(30) -> 20.0
```
```python starter
def make_averager():
    pass

avg = make_averager()
print(avg(10), avg(20), avg(30))
```
```python check
avg = make_averager()
assert avg(10) == 10.0, "First call should return 10.0"
assert avg(20) == 15.0, "Second call should return 15.0"
assert avg(30) == 20.0, "Third call should return 20.0"
other = make_averager()
assert other(4) == 4.0, "Each averager should keep its own numbers"
```
```python solution
def make_averager():
    values = []
    def averager(n):
        values.append(n)
        return sum(values) / len(values)
    return averager

avg = make_averager()
print(avg(10), avg(20), avg(30))
```
hint: Create values = [] inside make_averager, define an inner function that appends n and returns sum(values) / len(values), and return the inner function. Appending to a list doesn't need nonlocal.
:::

:::quiz
? In which order does Python look up names?
+ Local, Enclosing, Global, Built-in
- Global, Local, Built-in, Enclosing
- Built-in, Global, Enclosing, Local
= That's the LEGB rule.

? What keyword lets an inner function reassign a variable of its outer function?
- global
+ nonlocal
- outer
= `nonlocal` refers to the enclosing function's variable; `global` refers to the module level.
:::

@@@ lesson
id: lambdas-and-higher-order
title: Lambdas and higher-order functions
minutes: 12
summary: Treat functions as values, write small lambdas, and sort, map and filter with them.
---
In Python, functions are **values**, just like numbers and strings. You can store them in variables, put them in lists and pass them to other functions.

```python
def shout(text):
    return text.upper() + "!"

def whisper(text):
    return text.lower() + "..."

for style in [shout, whisper]:
    print(style("Hello"))
```

A function that takes or returns another function is called a **higher-order function**.

### lambda: tiny anonymous functions

`lambda` creates a small function in one expression: `lambda parameters: expression`.

```python
square = lambda n: n * n
print(square(7))

add = lambda a, b: a + b
print(add(2, 3))
```

Lambdas are best used inline, as arguments. If you're assigning one to a name, a normal `def` is clearer.

### Sorting with a key

`sorted`, `min` and `max` accept a `key` function that decides **what to compare**:

```python
words = ["banana", "Kiwi", "apple", "fig"]
print(sorted(words))                      # capital letters sort first
print(sorted(words, key=str.lower))       # case-insensitive
print(sorted(words, key=len))             # by length

people = [("Ana", 31), ("Ben", 25), ("Cy", 35)]
print(sorted(people, key=lambda p: p[1]))
print(max(people, key=lambda p: p[1]))
```

Sort by several things by returning a tuple: `key=lambda p: (p.age, p.name)`.

### map and filter

`map(func, items)` applies a function to every item. `filter(func, items)` keeps items where the function returns something truthy. Both return lazy iterators, so wrap them in `list()` to see the results.

```python
nums = [1, 2, 3, 4, 5, 6]
print(list(map(lambda n: n * 10, nums)))
print(list(filter(lambda n: n % 2 == 0, nums)))
print(list(map(str.upper, ["a", "b"])))
```

Comprehensions usually read better than `map`/`filter` with lambdas: `[n * 10 for n in nums]`. Use whichever is clearer.

### any and all

```python
scores = [72, 88, 95, 61]
print(any(s > 90 for s in scores))
print(all(s >= 60 for s in scores))
```

### Dispatch tables

A dictionary of functions can replace a long `if/elif` chain:

```python
ops = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
}
print(ops["*"](6, 7))
```

:::exercise Leaderboard
Write `leaderboard(scores)` that takes a list of `(name, points)` tuples and returns the names sorted by points **highest first**. When points are tied, sort those names alphabetically.

`leaderboard([("Cy", 50), ("Ana", 70), ("Ben", 50)])` → `["Ana", "Ben", "Cy"]`
```python starter
def leaderboard(scores):
    return [name for name, points in scores]

print(leaderboard([("Cy", 50), ("Ana", 70), ("Ben", 50)]))
```
```python check
got = leaderboard([("Cy", 50), ("Ana", 70), ("Ben", 50)])
assert got == ["Ana", "Ben", "Cy"], f"Got {got}"
got = leaderboard([("Zed", 10), ("Amy", 10), ("Max", 99), ("Bo", 1)])
assert got == ["Max", "Amy", "Zed", "Bo"], f"Got {got}"
```
```python solution
def leaderboard(scores):
    ordered = sorted(scores, key=lambda s: (-s[1], s[0]))
    return [name for name, points in ordered]

print(leaderboard([("Cy", 50), ("Ana", 70), ("Ben", 50)]))
```
hint: Sort with key=lambda s: (-s[1], s[0]). Negating the points puts the highest first while names stay A to Z.
:::

:::exercise Apply twice
Write `apply_twice(func, value)` that calls `func` on `value`, then calls `func` again on the result.

`apply_twice(lambda x: x + 3, 10)` → `16`
```python starter
def apply_twice(func, value):
    return value

print(apply_twice(lambda x: x + 3, 10))
```
```python check
assert apply_twice(lambda x: x + 3, 10) == 16, "Adding 3 twice to 10 should give 16"
assert apply_twice(lambda s: s + "!", "hi") == "hi!!", "Should work with strings too"
assert apply_twice(str.upper, "abc") == "ABC"
```
```python solution
def apply_twice(func, value):
    return func(func(value))

print(apply_twice(lambda x: x + 3, 10))
```
hint: return func(func(value))
:::

:::quiz
? What does `sorted(["bb", "a", "ccc"], key=len)` return?
+ ['a', 'bb', 'ccc']
- ['ccc', 'bb', 'a']
- [1, 2, 3]
= `key=len` compares lengths but returns the original strings.

? What does `list(filter(lambda x: x > 2, [1, 2, 3, 4]))` give?
- [True, True]
+ [3, 4]
- [1, 2]
= filter keeps the items for which the function returns True.
:::

@@@ lesson
id: recursion
title: Recursion
minutes: 12
summary: Functions that call themselves, base cases, and when recursion is the right tool.
---
A **recursive** function calls itself to solve a smaller version of the same problem. Every recursive function needs:

1. A **base case** that returns an answer directly, without recursing.
2. A **recursive case** that moves towards the base case.

```python
def countdown(n):
    if n == 0:              # base case
        print("Liftoff!")
        return
    print(n)
    countdown(n - 1)        # recursive case: smaller problem

countdown(3)
```

### Factorial

The factorial of `n` (written `n!`) is `n × (n-1) × ... × 1`. Notice that `n! = n × (n-1)!`, which is a recursive definition:

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))
print(factorial(20))
```

Trace `factorial(3)`: it waits for `factorial(2)`, which waits for `factorial(1)`, which returns 1. Then the results multiply back up: 1, 2, 6. Each waiting call sits on the **call stack**.

### Forgetting the base case

Without a base case, the function calls itself until Python gives up with a `RecursionError`. Python limits the depth (usually about 1000 calls; less in this browser version) to protect your computer.

### Recursion fits tree-shaped data

Recursion is most useful when data contains smaller copies of itself, like folders inside folders, or lists inside lists:

```python
def flatten(items):
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))   # recurse into the sub-list
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, 4], 5], [[6]], 7]))
```

### Recursion vs loops

Many recursive functions can be written as loops, which are often faster in Python and have no depth limit. Use recursion when it makes the code clearer: trees, nested structures, divide-and-conquer algorithms like merge sort (Part 7).

### Memoization: remembering results

A naive recursive Fibonacci recomputes the same values again and again. Caching results makes it dramatically faster:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(80))
```

The `@lru_cache` line is a *decorator*; you'll learn how they work in Part 7.

:::exercise Sum of digits
Write a **recursive** `digit_sum(n)` that returns the sum of the digits of a non-negative integer. `digit_sum(1234)` → `10`.

Hint: the last digit is `n % 10`, and the rest is `n // 10`.
```python starter
def digit_sum(n):
    return 0

print(digit_sum(1234))
```
```python check
for n, want in [(0, 0), (7, 7), (1234, 10), (99999, 45), (1000000, 1)]:
    got = digit_sum(n)
    assert got == want, f"digit_sum({n}) should be {want} but was {got}"
assert __source__.count("digit_sum(") >= 3, "Your function should call itself"
```
```python solution
def digit_sum(n):
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)

print(digit_sum(1234))
```
hint: Base case: if n < 10, return n. Otherwise return n % 10 + digit_sum(n // 10).
:::

:::exercise Power
Write a recursive `power(base, exp)` for non-negative integer exponents without using `**` or `pow`.
```python starter
def power(base, exp):
    return 1

print(power(2, 10))
```
```python check
for b, e in [(2, 10), (3, 0), (5, 3), (10, 5), (7, 1)]:
    assert power(b, e) == b ** e, f"power({b}, {e}) should be {b ** e} but was {power(b, e)}"
src_body = __source__.split("def power", 1)[1].split("print(", 1)[0]
assert "**" not in src_body and "pow(" not in src_body, "Don't use ** or pow() inside power"
```
```python solution
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

print(power(2, 10))
```
hint: Anything to the power 0 is 1 (base case). Otherwise base ** exp equals base * power(base, exp - 1).
:::

:::quiz
? What happens if a recursive function has no base case?
- It returns None
+ It raises RecursionError
- It runs forever silently
= Python limits how deep calls can go and raises RecursionError when the limit is reached.

? Which problem is the most natural fit for recursion?
- Adding numbers from 1 to 10
+ Walking through folders that contain folders
- Printing a list
= Nested, tree-shaped data maps naturally onto a function that calls itself for each sub-part.
:::
