@@@ part
id: 7
title: Advanced Python
level: Advanced
blurb: Write Pythonic, efficient code with generators, decorators, context managers, type hints and the functional toolkit, then reason about performance and build a complete project.

@@@ lesson
id: iterators-and-generators
title: Iterators and generators
minutes: 15
summary: Understand how for loops really work and produce values lazily with yield.
---
### How a for loop really works

Anything you can loop over is an **iterable**. When a `for` loop starts, it calls `iter()` on the iterable to get an **iterator**, then calls `next()` on it repeatedly until it raises `StopIteration`.

```python
colors = ["red", "green"]
it = iter(colors)
print(next(it))
print(next(it))
try:
    next(it)
except StopIteration:
    print("No more items: this is how the loop knows to stop")
```

### Generators: functions that yield

A **generator function** uses `yield` instead of `return`. Calling it doesn't run the body; it returns a generator object. Each `next()` runs the body until the next `yield`, then **pauses**, remembering where it was.

```python
def count_up_to(limit):
    print("  (starting)")
    n = 1
    while n <= limit:
        yield n
        n += 1
    print("  (finished)")

gen = count_up_to(3)
print(next(gen))
print(next(gen))
for value in gen:          # carries on from where it paused
    print(value)
```

### Why generators matter: laziness

A generator produces values **one at a time, on demand**. It never builds the whole sequence in memory. That makes it possible to work with huge or even infinite sequences:

```python
def fibonacci():
    a, b = 0, 1
    while True:            # infinite, but only computed as needed
        yield a
        a, b = b, a + b

for i, f in enumerate(fibonacci()):
    if i >= 10:
        break
    print(f, end=" ")
print()
```

### Generator expressions

Like a list comprehension, but with parentheses. It produces items lazily:

```python
squares_list = [n * n for n in range(10)]     # builds the whole list
squares_gen = (n * n for n in range(10))      # builds nothing yet
print(squares_list)
print(squares_gen)
print(sum(n * n for n in range(1_000_000)))   # no million-item list in memory
```

When you pass a generator expression as the only argument, you can drop the extra parentheses, as with `sum(...)` above.

### Generator pipelines

Generators chain together like an assembly line, each stage pulling items from the previous one. This is how you'd process a log file too big to fit in memory:

```python
log_lines = [
    "INFO start",
    "ERROR disk full",
    "INFO retry",
    "ERROR timeout",
    "WARN slow",
]

def read(lines):
    for line in lines:
        yield line.strip()

def only_errors(lines):
    for line in lines:
        if line.startswith("ERROR"):
            yield line

def messages(lines):
    for line in lines:
        yield line.split(" ", 1)[1]

for msg in messages(only_errors(read(log_lines))):
    print(msg)
```

### yield from

`yield from` hands over to another iterable, yielding all of its items:

```python
def walk(tree):
    for item in tree:
        if isinstance(item, list):
            yield from walk(item)
        else:
            yield item

print(list(walk([1, [2, [3, 4]], 5])))
```

### A generator is single-use

Once a generator is exhausted, it stays empty. Call the generator function again to get a fresh one.

```python
gen = (x for x in range(3))
print(list(gen))
print(list(gen))
```

:::exercise Chunks
Write a generator `chunks(items, size)` that yields lists of at most `size` items.

`list(chunks([1, 2, 3, 4, 5], 2))` → `[[1, 2], [3, 4], [5]]`
```python starter
def chunks(items, size):
    return [items]

print(list(chunks([1, 2, 3, 4, 5], 2)))
```
```python check
import types
assert isinstance(chunks([1], 1), types.GeneratorType), "chunks should be a generator function (use yield)"
assert list(chunks([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
assert list(chunks([1, 2, 3], 3)) == [[1, 2, 3]]
assert list(chunks([], 4)) == []
assert list(chunks("abcde", 2)) == [["a", "b"], ["c", "d"], ["e"]], "Should work for any iterable sequence; yield lists"
```
```python solution
def chunks(items, size):
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch

print(list(chunks([1, 2, 3, 4, 5], 2)))
```
hint: Collect items into a batch list. When it reaches size, yield it and start a new one. After the loop, yield any leftover batch.
:::

:::exercise Running total
Write a generator `running_total(nums)` that yields the cumulative sum after each number.

`list(running_total([3, 1, 4]))` → `[3, 4, 8]`
```python starter
def running_total(nums):
    pass

print(list(running_total([3, 1, 4])))
```
```python check
import types
assert isinstance(running_total([]), types.GeneratorType), "Use yield to make a generator"
assert list(running_total([3, 1, 4])) == [3, 4, 8]
assert list(running_total([])) == []
def _endless():
    n = 0
    while True:
        n += 1
        yield n
g = running_total(_endless())
assert [next(g) for _ in range(4)] == [1, 3, 6, 10], "Should work lazily on an endless input"
```
```python solution
def running_total(nums):
    total = 0
    for n in nums:
        total += n
        yield total

print(list(running_total([3, 1, 4])))
```
hint: Keep a total variable; for each n, add it and yield total.
:::

:::quiz
? What does calling a generator function return?
- The first yielded value
+ A generator object, without running the body yet
- A list of all values
= The body only starts running when you ask for the first value with `next()` or a loop.

? What's the main benefit of `(x * 2 for x in data)` over `[x * 2 for x in data]`?
+ It doesn't build the whole result in memory
- It's always faster
- It can be reused many times
= Generator expressions are lazy. They're single-use, though.
:::

@@@ lesson
id: decorators
title: Decorators
minutes: 15
summary: Wrap functions to add behaviour like timing, logging, caching and validation.
---
A **decorator** is a function that takes a function and returns a new function that usually wraps the original with extra behaviour. You've already used some: `@property`, `@dataclass`, `@lru_cache`.

It builds on two ideas from Part 4: functions are values, and inner functions can remember outer variables (closures).

### Building one step by step

```python
def shout(func):
    def wrapper():
        result = func()
        return result.upper() + "!"
    return wrapper

def greet():
    return "hello"

loud_greet = shout(greet)      # wrap it by hand
print(loud_greet())
```

The `@` syntax does the same wrapping at definition time. These two are equivalent:

```python
def shout(func):
    def wrapper():
        return func().upper() + "!"
    return wrapper

@shout
def greet():
    return "hello"
# same as: greet = shout(greet)

print(greet())
```

### Handling any arguments

Real decorators must work with functions of any signature, so the wrapper accepts `*args, **kwargs` and passes them through. `functools.wraps` copies the original function's name and docstring onto the wrapper.

```python
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"-> {func.__name__}{args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"<- {func.__name__} returned {result!r}")
        return result
    return wrapper

@log_calls
def add(a, b, round_to=None):
    total = a + b
    return round(total, round_to) if round_to is not None else total

add(2, 3)
add(1.234, 2.5, round_to=1)
print(add.__name__)
```

### A timing decorator

```python
import functools, time

def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{func.__name__} took {elapsed:.1f} ms")
        return result
    return wrapper

@timed
def slow_sum(n):
    return sum(i * i for i in range(n))

print(slow_sum(200_000))
```

### Decorators with arguments

To pass settings, add one more layer: a function that takes the settings and returns a decorator.

```python
import functools

def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator

@repeat(3)
def roll():
    return "dice"

print(roll())
```

### Real-world uses

- **Caching**: `@functools.lru_cache` remembers results.
- **Web frameworks**: Flask and FastAPI use `@app.get("/users")` to map URLs to functions.
- **Access control**: check that a user is logged in before running a view.
- **Retrying**: re-run a function that failed because of a flaky network.

:::exercise Call counter
Write a decorator `count_calls` that counts how many times the decorated function has been called. Store the count in an attribute named `calls` on the wrapper (`wrapper.calls = 0` before returning it) and increase it on each call.
```python starter
import functools

def count_calls(func):
    return func

@count_calls
def hello(name):
    return f"hi {name}"

hello("a")
hello("b")
print(hello.calls)
```
```python check
@count_calls
def _f(x, y=1):
    return x + y
assert _f.calls == 0, "calls should start at 0"
assert _f(1) == 2 and _f(1, y=5) == 6, "The wrapper must pass arguments through and return the result"
assert _f.calls == 2, f"After two calls, calls should be 2, got {_f.calls}"
assert _f.__name__ == "_f", "Use functools.wraps so the name is preserved"
```
```python solution
import functools

def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@count_calls
def hello(name):
    return f"hi {name}"

hello("a")
hello("b")
print(hello.calls)
```
hint: Inside count_calls, define wrapper(*args, **kwargs) decorated with @functools.wraps(func). In it, do wrapper.calls += 1 and return func(*args, **kwargs). Set wrapper.calls = 0 before return wrapper.
:::

:::exercise Validate positive
Write a decorator `positive_args` that raises `ValueError` if any **positional** argument is a number less than or equal to 0. Otherwise it calls the function normally.
```python starter
import functools

def positive_args(func):
    return func

@positive_args
def area(w, h):
    return w * h

print(area(3, 4))
```
```python check
@positive_args
def _area(w, h):
    return w * h
assert _area(3, 4) == 12
for bad in [(0, 4), (3, -1)]:
    try:
        _area(*bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"area{bad} should raise ValueError")
```
```python solution
import functools

def positive_args(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for value in args:
            if isinstance(value, (int, float)) and value <= 0:
                raise ValueError(f"{func.__name__} needs positive numbers, got {value}")
        return func(*args, **kwargs)
    return wrapper

@positive_args
def area(w, h):
    return w * h

print(area(3, 4))
```
hint: In the wrapper, loop over args; if a number is <= 0, raise ValueError. Then return func(*args, **kwargs).
:::

:::quiz
? What is `@deco` above `def f(): ...` equivalent to?
+ `f = deco(f)`
- `deco = f(deco)`
- `f = deco`
= The decorator receives the function and its return value replaces it.

? Why use `functools.wraps` in a decorator?
- It makes the function faster
+ It keeps the original function's name and docstring
- It's required for decorators to work
= Without it, the decorated function reports the wrapper's name, which confuses debugging and tools.
:::

@@@ lesson
id: context-managers
title: Context managers
minutes: 10
summary: Guarantee setup and cleanup with the with statement, and write your own context managers.
---
You've used `with open(...) as f:`. The `with` statement works with any **context manager**: an object that runs setup code at the start of the block and cleanup code at the end, **even if an error happens**.

Typical uses: closing files, releasing locks, committing or rolling back database transactions, restoring settings, timing a block.

### Writing one as a class

A context manager defines `__enter__` and `__exit__`:

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self                     # bound to the name after 'as'

    def __exit__(self, exc_type, exc_value, traceback):
        import time
        self.elapsed = time.perf_counter() - self.start
        print(f"block took {self.elapsed * 1000:.1f} ms")
        return False                    # don't suppress exceptions

with Timer() as t:
    total = sum(range(300_000))
print(total)
```

`__exit__` receives details of any exception raised inside the block. Returning `True` swallows the exception; returning `False` (or `None`) lets it continue.

### Writing one with contextlib

The `@contextmanager` decorator turns a generator into a context manager. Code before `yield` is setup, code after is cleanup. Wrap the `yield` in `try/finally` so cleanup always runs.

```python
from contextlib import contextmanager

@contextmanager
def html_tag(name):
    print(f"<{name}>")
    try:
        yield
    finally:
        print(f"</{name}>")

with html_tag("ul"):
    for item in ["tea", "coffee"]:
        with html_tag("li"):
            print(item)
```

### Cleanup happens even on errors

```python
from contextlib import contextmanager

@contextmanager
def transaction(db):
    snapshot = dict(db)
    try:
        yield db
        print("commit")
    except Exception:
        db.clear()
        db.update(snapshot)
        print("rollback")
        raise

accounts = {"ana": 100, "ben": 50}
try:
    with transaction(accounts) as db:
        db["ana"] -= 80
        db["ben"] += 80
        raise RuntimeError("power cut!")
except RuntimeError as e:
    print("Error:", e)
print(accounts)
```

The money wasn't lost: the context manager restored the original balances.

### Handy built-ins from contextlib

```python
from contextlib import suppress

data = {}
with suppress(KeyError):        # ignore one specific exception
    print(data["missing"])
print("carried on")
```

:::exercise Indented printer
Write a context manager `indent()` using `@contextmanager` that increases a global indentation level by one for the duration of the block, and restores it afterwards (even if an error occurs). Use the provided `say()` function to print.
```python starter
from contextlib import contextmanager

level = 0

def say(text):
    print("  " * level + text)

def indent():
    pass

say("start")
with indent():
    say("inside")
    with indent():
        say("deeper")
say("end")
```
```python check
assert level == 0, "level should be back to 0 after the blocks"
import io, contextlib as _cl
buf = io.StringIO()
with _cl.redirect_stdout(buf):
    say("a")
    with indent():
        say("b")
        with indent():
            say("c")
    say("d")
assert buf.getvalue() == "a\n  b\n    c\nd\n", f"Unexpected output:\n{buf.getvalue()}"
try:
    with indent():
        raise ValueError
except ValueError:
    pass
assert level == 0, "level must be restored even when an error happens (use try/finally)"
```
```python solution
from contextlib import contextmanager

level = 0

def say(text):
    print("  " * level + text)

@contextmanager
def indent():
    global level
    level += 1
    try:
        yield
    finally:
        level -= 1

say("start")
with indent():
    say("inside")
    with indent():
        say("deeper")
say("end")
```
hint: Decorate indent with @contextmanager. Inside: global level; level += 1; then try: yield finally: level -= 1.
:::

:::quiz
? When does a context manager's cleanup code run?
- Only if the block succeeds
+ When the block ends, whether or not an error occurred
- When the program ends
= That guarantee is the whole point of `with`.

? In a `@contextmanager` generator, what separates setup from cleanup?
+ The `yield`
- A `return`
- The `with` keyword
= Code before `yield` runs on entry; code after it runs on exit.
:::

@@@ lesson
id: type-hints
title: Type hints
minutes: 12
summary: Annotate your code with types to document intent and catch bugs with tools like mypy.
---
**Type hints** describe what types a function expects and returns. Python doesn't enforce them at runtime, but they make code easier to read, and editors and tools like **mypy** and **Pyright** use them to catch bugs before you run anything.

```python
def greet(name: str, excited: bool = False) -> str:
    message = f"Hello, {name}"
    return message + "!" if excited else message + "."

print(greet("Ada"))
print(greet("Ada", excited=True))
```

Hints are not checked when the program runs. This still works, even though it breaks the promise:

```python
def double(n: int) -> int:
    return n * 2

print(double("ha"))     # a type checker would flag this line
```

### Common hints

```python
from typing import Optional, Union, Callable, Iterable

def total(prices: list[float]) -> float:
    return sum(prices)

def lookup(table: dict[str, int], key: str) -> Optional[int]:   # int or None
    return table.get(key)

def first_word(text: str | None) -> str:     # modern "or" syntax (3.10+)
    return text.split()[0] if text else ""

def apply(func: Callable[[int], int], values: Iterable[int]) -> list[int]:
    return [func(v) for v in values]

point: tuple[int, int] = (3, 4)
print(total([1.5, 2.5]), lookup({"a": 1}, "b"), first_word("hi there"), apply(abs, [-1, 2]))
```

| Hint | Meaning |
|---|---|
| `int`, `str`, `float`, `bool` | basic types |
| `list[int]` | list of ints |
| `dict[str, float]` | dict with str keys and float values |
| `tuple[int, str]` | exactly an int then a str |
| `tuple[int, ...]` | any number of ints |
| `X \| None` or `Optional[X]` | X or None |
| `X \| Y` or `Union[X, Y]` | either type |
| `Callable[[int], str]` | function taking an int, returning a str |
| `Any` | anything (turns off checking) |

### Hints in classes and dataclasses

Dataclasses rely on hints to know which fields exist:

```python
from dataclasses import dataclass

@dataclass
class Task:
    title: str
    priority: int = 3
    done: bool = False

    def complete(self) -> None:
        self.done = True

tasks: list[Task] = [Task("write tests", 1), Task("tidy desk")]
tasks[0].complete()
print(tasks)
```

### Generics: one function, many types

A `TypeVar` says "whatever type goes in, the same type comes out":

```python
from typing import TypeVar

T = TypeVar("T")

def last(items: list[T]) -> T:
    return items[-1]

print(last([1, 2, 3]), last(["a", "b"]))
```

### Should you use them?

For small scripts, hints are optional. For anything you'll maintain, share or grow, they're worth it: they're documentation that tools can verify. Most modern Python libraries ship with type hints.

:::exercise Annotate the function
Add type hints to `summarize` so that `scores` is a dict mapping `str` to a list of `int`, and the function returns a dict mapping `str` to `float`. The body is already correct.
```python starter
def summarize(scores):
    return {name: sum(vals) / len(vals) for name, vals in scores.items() if vals}

print(summarize({"ana": [90, 80], "ben": []}))
```
```python check
assert summarize({"ana": [90, 80], "ben": []}) == {"ana": 85.0}
sig = [ln for ln in __source__.splitlines() if ln.startswith("def summarize")][0].replace(" ", "")
assert "scores:dict[str,list[int]]" in sig, "Annotate scores as dict[str, list[int]]"
assert "->dict[str,float]" in sig, "Annotate the return type as dict[str, float]"
```
```python solution
def summarize(scores: dict[str, list[int]]) -> dict[str, float]:
    return {name: sum(vals) / len(vals) for name, vals in scores.items() if vals}

print(summarize({"ana": [90, 80], "ben": []}))
```
hint: def summarize(scores: dict[str, list[int]]) -> dict[str, float]:
:::

:::quiz
? What happens if you pass a str to a function hinted as taking an int?
- Python raises TypeError
+ It runs anyway; hints aren't enforced at runtime
- Python converts it automatically
= Hints are for readers and tools like mypy, not for the interpreter.

? What does `Optional[str]` mean?
+ A str or None
- An optional argument
- Any type
= It's the same as `str | None`. Whether the argument has a default is a separate matter.
:::

@@@ lesson
id: itertools-functools
title: itertools and functools
minutes: 12
summary: Power tools for looping and for working with functions.
---
### itertools: building blocks for iteration

The `itertools` module provides fast, memory-efficient tools that return iterators.

**Counting, cycling and slicing**

```python
import itertools as it

print(list(it.islice(it.count(start=10, step=5), 4)))   # 10, 15, 20, 25
colors = it.cycle(["red", "green"])
print([next(colors) for _ in range(5)])
print(list(it.repeat("ha", 3)))
```

**Combining iterables**

```python
import itertools as it

print(list(it.chain([1, 2], (3, 4), "ab")))
print(list(it.zip_longest("abc", [1, 2], fillvalue="-")))
print(list(it.accumulate([3, 1, 4, 1, 5])))       # running totals
```

**Combinatorics**

```python
import itertools as it

print(list(it.product("AB", [1, 2])))             # every pairing
print(list(it.permutations("abc", 2)))            # ordered arrangements
print(list(it.combinations([1, 2, 3, 4], 2)))     # unordered selections
```

**Grouping consecutive items**

`groupby` groups **adjacent** items with the same key, so sort by that key first:

```python
import itertools as it

words = ["apple", "avocado", "banana", "blueberry", "cherry"]
for letter, group in it.groupby(sorted(words), key=lambda w: w[0]):
    print(letter, list(group))
```

**Filtering**

```python
import itertools as it

nums = [1, 4, 6, 3, 8, 2]
print(list(it.takewhile(lambda n: n < 5, nums)))   # stop at first failure
print(list(it.dropwhile(lambda n: n < 5, nums)))   # skip until first failure
```

### functools: tools for functions

```python
from functools import reduce, partial, lru_cache

# reduce: combine items pairwise into one value
print(reduce(lambda a, b: a * b, [1, 2, 3, 4, 5]))

# partial: pre-fill some arguments
def power(base, exp):
    return base ** exp
square = partial(power, exp=2)
cube = partial(power, exp=3)
print(square(9), cube(2))

# lru_cache: memoize expensive pure functions
@lru_cache(maxsize=None)
def ways_to_climb(steps):
    if steps <= 1:
        return 1
    return ways_to_climb(steps - 1) + ways_to_climb(steps - 2)

print(ways_to_climb(60))
print(ways_to_climb.cache_info())
```

### operator: functions for common operations

Instead of writing small lambdas, use ready-made functions from `operator`:

```python
from operator import itemgetter, attrgetter, mul
from functools import reduce

rows = [("ana", 31), ("ben", 25), ("cy", 35)]
print(sorted(rows, key=itemgetter(1)))
print(reduce(mul, [2, 3, 4]))
```

:::exercise Team pairings
Write `pairings(players)` that returns all unique pairs of players as a list of tuples, in the order `itertools.combinations` produces them. Then write `schedule_size(n)` returning how many pairs `n` players produce.
```python starter
import itertools

def pairings(players):
    return []

def schedule_size(n):
    return 0

print(pairings(["Ana", "Ben", "Cy"]), schedule_size(10))
```
```python check
assert pairings(["Ana", "Ben", "Cy"]) == [("Ana", "Ben"), ("Ana", "Cy"), ("Ben", "Cy")], f"Got {pairings(['Ana', 'Ben', 'Cy'])}"
assert pairings(["solo"]) == []
assert schedule_size(10) == 45, f"10 players make 45 pairs, got {schedule_size(10)}"
assert schedule_size(2) == 1
```
```python solution
import itertools

def pairings(players):
    return list(itertools.combinations(players, 2))

def schedule_size(n):
    return len(pairings(range(n)))

print(pairings(["Ana", "Ben", "Cy"]), schedule_size(10))
```
hint: list(itertools.combinations(players, 2)). For schedule_size, count the pairings of range(n), or use the formula n * (n - 1) // 2.
:::

:::exercise Group by length
Write `group_by_length(words)` that returns a dict mapping each word length to a list of words with that length, using `itertools.groupby`. Words within a group should keep alphabetical order.

`group_by_length(["hi", "cat", "ox", "dog"])` → `{2: ['hi', 'ox'], 3: ['cat', 'dog']}`
```python starter
import itertools

def group_by_length(words):
    return {}

print(group_by_length(["hi", "cat", "ox", "dog"]))
```
```python check
assert group_by_length(["hi", "cat", "ox", "dog"]) == {2: ["hi", "ox"], 3: ["cat", "dog"]}, f"Got {group_by_length(['hi', 'cat', 'ox', 'dog'])}"
assert group_by_length([]) == {}
assert "groupby" in __source__, "Use itertools.groupby"
```
```python solution
import itertools

def group_by_length(words):
    ordered = sorted(words, key=lambda w: (len(w), w))
    return {length: list(group) for length, group in itertools.groupby(ordered, key=len)}

print(group_by_length(["hi", "cat", "ox", "dog"]))
```
hint: Sort first with key=lambda w: (len(w), w), then groupby(ordered, key=len) and build a dict with list(group).
:::

:::quiz
? Why must you usually sort before `itertools.groupby`?
+ It only groups items that are next to each other
- It sorts in reverse otherwise
- It only accepts sorted lists
= Unsorted input produces several separate groups for the same key.

? What does `partial(pow, 2)` create?
+ A function where the first argument of pow is fixed to 2
- The number 2
- A copy of pow
= Calling it with x gives `pow(2, x)`.
:::

@@@ lesson
id: algorithms-and-big-o
title: Algorithms and Big-O
minutes: 18
summary: Measure how code scales, choose the right data structure, and implement searching and sorting.
---
Two programs can give the same answer while one takes a second and the other takes a day. **Big-O notation** describes how the running time grows as the input size `n` grows.

| Big-O | Name | Example | 1,000 items → 1,000,000 items |
|---|---|---|---|
| O(1) | constant | dict lookup, list index | same time |
| O(log n) | logarithmic | binary search | 10 steps → 20 steps |
| O(n) | linear | loop over a list, `x in list` | 1,000× slower |
| O(n log n) | linearithmic | good sorting (`sorted`) | ~2,000× slower |
| O(n²) | quadratic | nested loops over the same data | 1,000,000× slower |

![Line chart of steps against number of items: O(1) and O(log n) stay almost flat, O(n) grows steadily, O(n log n) faster, and O(n squared) shoots up](figures/big-o.svg)

Big-O ignores constants and focuses on the shape of growth. For small inputs, anything is fast. For big inputs, the shape is all that matters.

### The right data structure is the biggest win

Checking `x in some_list` looks at items one by one: O(n). Checking `x in some_set` uses hashing: O(1) on average. Watch the difference:

```python
import time

n = 20_000
as_list = list(range(n))
as_set = set(as_list)
targets = range(n - 2_000, n)     # values near the end

start = time.perf_counter()
hits = sum(1 for t in targets if t in as_list)
list_ms = (time.perf_counter() - start) * 1000

start = time.perf_counter()
hits = sum(1 for t in targets if t in as_set)
set_ms = (time.perf_counter() - start) * 1000

print(f"list: {list_ms:.1f} ms   set: {set_ms:.2f} ms")
```

### Spotting O(n²)

A loop inside a loop over the same data is the classic warning sign:

```python
def has_duplicates_slow(items):          # O(n²)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False

def has_duplicates_fast(items):          # O(n)
    seen = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False

data = [5, 3, 8, 1, 3]
print(has_duplicates_slow(data), has_duplicates_fast(data))
```

### Binary search: O(log n)

On **sorted** data you can find a value by repeatedly halving the search range. A million items take at most 20 steps.

```python
def binary_search(items, target):
    low, high = 0, len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

nums = list(range(0, 1000, 7))
print(binary_search(nums, 693), binary_search(nums, 50))
```

The standard library's `bisect` module provides a well-tested version.

### Sorting: merge sort, O(n log n)

Merge sort splits the list in half, sorts each half recursively, then merges the two sorted halves. It's a classic **divide and conquer** algorithm:

```python
def merge_sort(items):
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])

    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
```

In real code, use `sorted()`. Python's built-in sort (Timsort) is O(n log n), stable and highly optimised. Learning how sorting works trains you to think about algorithms, and it comes up in technical interviews.

### Common operation costs

| Operation | list | dict / set |
|---|---|---|
| index / key lookup | O(1) | O(1) |
| `x in ...` | O(n) | O(1) |
| append / add | O(1) | O(1) |
| insert or remove at the front | O(n) | n/a |
| sort | O(n log n) | n/a |

Need fast adds and removes at both ends? Use `collections.deque`.

:::exercise Two sum
Write `two_sum(nums, target)` that returns the indexes `(i, j)` with `i < j` of the two numbers that add up to `target`, or `None` if there are none. Make it **O(n)** with a dictionary that remembers numbers you've seen and their positions.

`two_sum([2, 7, 11, 15], 9)` → `(0, 1)`
```python starter
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None

print(two_sum([2, 7, 11, 15], 9))
```
```python check
assert two_sum([2, 7, 11, 15], 9) == (0, 1)
assert two_sum([3, 2, 4], 6) == (1, 2)
assert two_sum([1, 2, 3], 100) is None
assert two_sum([5, 5], 10) == (0, 1)
body = __source__.split("def two_sum", 1)[1].split("\nprint", 1)[0]
assert body.count("for ") == 1, "Use a single loop with a dictionary (O(n)), not nested loops"
```
```python solution
def two_sum(nums, target):
    seen = {}
    for j, n in enumerate(nums):
        need = target - n
        if need in seen:
            return (seen[need], j)
        seen[n] = j
    return None

print(two_sum([2, 7, 11, 15], 9))
```
hint: Loop once with enumerate. For each number n at index j, check whether target - n is already in a dict seen (number → index). If so, return (seen[target - n], j). Otherwise store seen[n] = j.
:::

:::exercise Insertion sort
Implement `insertion_sort(items)` that returns a new sorted list without using `sorted` or `.sort`. Take each item and insert it into the correct position of a growing sorted list.
```python starter
def insertion_sort(items):
    return items

print(insertion_sort([5, 2, 9, 1, 5, 6]))
```
```python check
import random as _r
for _ in range(20):
    data = [_r.randint(-50, 50) for _ in range(_r.randint(0, 15))]
    original = list(data)
    assert insertion_sort(data) == sorted(original), f"Wrong result for {original}"
    assert data == original, "Don't modify the input list"
assert "sorted(" not in __source__.split("def insertion_sort", 1)[1].split("\nprint", 1)[0] and ".sort(" not in __source__, "Don't use sorted() or .sort()"
```
```python solution
def insertion_sort(items):
    result = []
    for item in items:
        i = len(result)
        while i > 0 and result[i - 1] > item:
            i -= 1
        result.insert(i, item)
    return result

print(insertion_sort([5, 2, 9, 1, 5, 6]))
```
hint: Start with result = []. For each item, walk backwards from the end of result while the previous element is bigger, then result.insert(i, item).
:::

:::quiz
? What's the Big-O of checking `x in my_set`?
+ O(1) on average
- O(n)
- O(log n)
= Sets use hash tables, so lookups don't depend on the size.

? What's the Big-O of two nested loops over the same list?
- O(n)
+ O(n²)
- O(2n)
= For each of n items you do up to n more steps.

? What does binary search require?
- A set
+ Sorted data
- Unique values
= Halving only works if you know which side the target must be on.
:::

@@@ lesson
id: capstone
title: "Capstone: build an expense tracker"
minutes: 30
summary: Combine everything into a complete program, then learn how to keep going on your own computer.
---
Time to put it all together. You'll build an **expense tracker** step by step: a dataclass for each expense, a tracker class that stores and analyses them, input validation with exceptions, CSV import and export, and a text report.

### The finished program

Read through the complete program, run it, and change things. Every piece uses something from an earlier lesson.

```python
from dataclasses import dataclass
from datetime import date
from collections import defaultdict
import csv
import io


class InvalidExpense(ValueError):
    """Raised when an expense has bad data."""


@dataclass(frozen=True)
class Expense:
    day: date
    category: str
    amount: float
    note: str = ""

    def __post_init__(self):
        if self.amount <= 0:
            raise InvalidExpense(f"amount must be positive, got {self.amount}")
        if not self.category.strip():
            raise InvalidExpense("category is required")


class Tracker:
    def __init__(self):
        self._expenses: list[Expense] = []

    def add(self, day: date, category: str, amount: float, note: str = "") -> Expense:
        expense = Expense(day, category.strip().lower(), round(amount, 2), note)
        self._expenses.append(expense)
        return expense

    def __len__(self) -> int:
        return len(self._expenses)

    def __iter__(self):
        return iter(sorted(self._expenses, key=lambda e: e.day))

    def total(self) -> float:
        return round(sum(e.amount for e in self._expenses), 2)

    def by_category(self) -> dict[str, float]:
        totals = defaultdict(float)
        for e in self._expenses:
            totals[e.category] += e.amount
        return {cat: round(v, 2) for cat, v in sorted(totals.items(), key=lambda kv: -kv[1])}

    def in_month(self, year: int, month: int):
        return (e for e in self if e.day.year == year and e.day.month == month)

    def to_csv(self) -> str:
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(["day", "category", "amount", "note"])
        for e in self:
            writer.writerow([e.day.isoformat(), e.category, f"{e.amount:.2f}", e.note])
        return out.getvalue()

    @classmethod
    def from_csv(cls, text: str) -> "Tracker":
        tracker = cls()
        for line_no, row in enumerate(csv.DictReader(io.StringIO(text)), start=2):
            try:
                tracker.add(date.fromisoformat(row["day"]), row["category"],
                            float(row["amount"]), row.get("note", ""))
            except (ValueError, KeyError) as err:
                print(f"skipping line {line_no}: {err}")
        return tracker

    def report(self) -> str:
        lines = [f"{'Category':<14}{'Amount':>10}{'Share':>8}", "-" * 32]
        total = self.total()
        for cat, amount in self.by_category().items():
            lines.append(f"{cat:<14}{amount:>10,.2f}{amount / total:>8.0%}")
        lines += ["-" * 32, f"{'TOTAL':<14}{total:>10,.2f}"]
        return "\n".join(lines)


data = """day,category,amount,note
2026-09-01,Rent,1200,September
2026-09-03,Groceries,84.20,
2026-09-07,Transport,32.5,bus pass
2026-09-12,Groceries,61.35,
2026-09-15,Fun,-20,typo
2026-09-20,Eating out,45.00,birthday dinner
2026-10-01,Rent,1200,October
"""

tracker = Tracker.from_csv(data)
print(f"Loaded {len(tracker)} expenses\n")
print(tracker.report())

september = list(tracker.in_month(2026, 9))
print(f"\nSeptember: {len(september)} expenses, {sum(e.amount for e in september):,.2f} total")
biggest = max(tracker, key=lambda e: e.amount)
print(f"Biggest: {biggest.category} {biggest.amount:,.2f} on {biggest.day:%d %b}")
```

### What each part demonstrates

| Feature | Lesson |
|---|---|
| `@dataclass(frozen=True)` with `__post_init__` validation | Properties and dataclasses |
| Custom exception `InvalidExpense` | Exceptions |
| `__len__` and `__iter__` | Special methods |
| `defaultdict`, `date` | Modules and the standard library |
| `csv` with `io.StringIO` | Files, CSV and JSON |
| `@classmethod` alternative constructor | Classes and objects |
| Generator expression in `in_month` | Iterators and generators |
| `sorted(..., key=lambda ...)`, `max(..., key=...)` | Lambdas |
| f-string format specs for the report | Strings |
| Type hints | Type hints |

### Your turn

The exercises below extend the tracker. Each one includes the code it needs, so you can solve them independently.

:::exercise Monthly budget alert
Write `over_budget(expenses, budgets)` where `expenses` is a list of `(category, amount)` tuples and `budgets` maps category to its limit. Return a **sorted list** of categories whose total spending is **above** their budget. Categories without a budget are never over.
```python starter
def over_budget(expenses, budgets):
    return []

spent = [("food", 120), ("fun", 60), ("food", 95), ("rent", 1200), ("fun", 10)]
limits = {"food": 200, "fun": 100, "rent": 1200}
print(over_budget(spent, limits))
```
```python check
spent = [("food", 120), ("fun", 60), ("food", 95), ("rent", 1200), ("fun", 10)]
limits = {"food": 200, "fun": 100, "rent": 1200}
assert over_budget(spent, limits) == ["food"], f"Expected ['food'], got {over_budget(spent, limits)}"
assert over_budget([("a", 5), ("b", 50)], {"a": 1, "b": 10}) == ["a", "b"]
assert over_budget([("misc", 999)], {}) == [], "Categories without a budget are never over"
assert over_budget([], {"a": 1}) == []
```
```python solution
def over_budget(expenses, budgets):
    totals = {}
    for category, amount in expenses:
        totals[category] = totals.get(category, 0) + amount
    return sorted(cat for cat, total in totals.items() if cat in budgets and total > budgets[cat])

spent = [("food", 120), ("fun", 60), ("food", 95), ("rent", 1200), ("fun", 10)]
limits = {"food": 200, "fun": 100, "rent": 1200}
print(over_budget(spent, limits))
```
hint: First total the spending per category in a dict. Then keep categories that are in budgets and whose total is greater than the limit, and sort them.
:::

:::exercise Spending streak
Write `longest_streak(days)` that takes a list of `datetime.date` objects (unsorted, may contain duplicates) on which money was spent, and returns the length of the longest run of **consecutive** days.
```python starter
from datetime import date, timedelta

def longest_streak(days):
    return 0

d = [date(2026, 9, 1), date(2026, 9, 2), date(2026, 9, 4), date(2026, 9, 3), date(2026, 9, 10)]
print(longest_streak(d))
```
```python check
from datetime import date as _d
assert longest_streak([_d(2026, 9, 1), _d(2026, 9, 2), _d(2026, 9, 4), _d(2026, 9, 3), _d(2026, 9, 10)]) == 4
assert longest_streak([]) == 0
assert longest_streak([_d(2026, 1, 1)]) == 1
assert longest_streak([_d(2026, 1, 1), _d(2026, 1, 1), _d(2026, 1, 2)]) == 2, "Duplicates shouldn't break or extend a streak"
assert longest_streak([_d(2025, 12, 31), _d(2026, 1, 1)]) == 2, "Streaks can cross years"
```
```python solution
from datetime import date, timedelta

def longest_streak(days):
    unique = sorted(set(days))
    best = current = 0
    previous = None
    for day in unique:
        if previous is not None and day - previous == timedelta(days=1):
            current += 1
        else:
            current = 1
        best = max(best, current)
        previous = day
    return best

d = [date(2026, 9, 1), date(2026, 9, 2), date(2026, 9, 4), date(2026, 9, 3), date(2026, 9, 10)]
print(longest_streak(d))
```
hint: Remove duplicates and sort with sorted(set(days)). Walk through the dates; if a date is exactly one day after the previous one (timedelta(days=1)), extend the current streak, otherwise restart it at 1. Track the best.
:::

### Where to go next

You now know the core of Python. To keep growing:

**1. Install Python on your computer.** Download it from python.org, then install a code editor such as VS Code with its Python extension. Run your first script from the terminal with `python hello.py`.

**2. Learn your tools.** Create a *virtual environment* per project so each project has its own packages, and install packages with `pip`:

```py-static
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install requests pytest
```

**3. Use version control.** Learn Git basics (`git add`, `git commit`, `git push`) and put every project on GitHub. A profile full of small, working projects is a strong portfolio.

**4. Pick a direction and build things:**

| Direction | Libraries to learn |
|---|---|
| Web APIs and backends | FastAPI, Flask, Django, SQLAlchemy |
| Data analysis | pandas, NumPy, Matplotlib, Jupyter |
| Machine learning and AI | scikit-learn, PyTorch, Hugging Face Transformers, LangChain |
| Automation and scripting | requests, BeautifulSoup, Playwright, pathlib |
| Testing | pytest, hypothesis |

**5. Practise regularly.** Small daily problems (Exercism, LeetCode, Advent of Code) build fluency. Reading other people's code on GitHub builds taste.

**6. Read the official docs.** The Python tutorial at docs.python.org is excellent, and the standard library reference answers most "is there a module for this?" questions.

Congratulations on finishing the course. Come back to the playground whenever you want to try an idea.

:::quiz
? In the tracker, why is `Expense` a frozen dataclass?
+ Expenses shouldn't change after they're recorded, and frozen objects are safer to share
- Frozen dataclasses are faster to print
- It's required for CSV export
= Immutability prevents accidental edits and makes objects hashable.

? Why does `from_csv` wrap each row in try/except instead of the whole loop?
+ So one bad row is skipped while the others still load
- Because try/except only works inside loops
- To make the code shorter
= Handling errors per row gives better results and clearer messages than failing the whole import.
:::
