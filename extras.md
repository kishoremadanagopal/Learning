@@ how-python-runs
topics: what a program is, `print()`, syntax vs runtime errors, how code is compiled
terms:
- **Program:** a list of instructions for a computer, run from top to bottom.
- **Python:** a popular, readable programming language. The standard version is called CPython.
- **Function:** a named piece of code that does a job, like `print`. You call it with parentheses: `print("hi")`.
- **Output:** what a program shows on the screen.
- **Syntax:** the grammar rules of a language. Breaking them gives a *syntax error* before anything runs.
- **Token:** the smallest meaningful piece of code, like `print`, `(` or `"hello"`.
- **AST (Abstract Syntax Tree):** the tree Python builds to represent the structure of your program.
- **Bytecode:** the low-level instructions CPython compiles your code into before running it.
- **Interpreter:** the program that reads and runs your Python code.
mistakes:
- Forgetting the closing quote or bracket: `print("Hello)` is a syntax error. Every `(` needs a `)` and every `"` needs a matching `"`.
- Capitalising built-in names: `Print("hi")` gives `NameError`. Python is case-sensitive.
- Panicking at red text. An error message is information: read the last line first, then the line number.

@@ print-and-comments
topics: `print()` with several values, `sep`, `end`, escape sequences, `#` comments
terms:
- **Argument:** a value you pass to a function inside its parentheses.
- **Keyword argument:** an argument passed by name, like `sep="-"` or `end=""`.
- **sep:** the text `print` puts between values (a space by default).
- **end:** the text `print` puts after the last value (a new line by default).
- **Escape sequence:** a backslash code inside a string, like `\n` (new line) or `\t` (tab).
- **Comment:** text after `#` that Python ignores. Used to explain code.
mistakes:
- Putting a `#` inside quotes and expecting a comment: `print("# hi")` prints `# hi`.
- Joining text and numbers with commas and expecting no space: `print("Total:", 5)` prints `Total: 5` with a space, because `sep` is a space.
- Writing comments that repeat the code (`x = 5  # set x to 5`). Explain *why*, not *what*.

@@ variables-and-types
topics: `=`, naming rules, `int`, `float`, `str`, `bool`, `type()`, `None`
terms:
- **Variable:** a name that refers to a value.
- **Assignment:** storing a value in a variable with `=`.
- **Data type:** the kind of value: `int`, `float`, `str`, `bool` and others.
- **int:** a whole number, like `42`.
- **float:** a number with a decimal point, like `3.14`.
- **str (string):** text, written in quotes.
- **bool (boolean):** `True` or `False`.
- **None:** a special value meaning "nothing" or "no value yet".
- **snake_case:** the Python naming style: lowercase words joined by underscores.
- **Concatenation:** joining strings with `+`.
mistakes:
- Reading `=` as "equals". It means "store this value in this name"; comparison is `==`.
- Quoting numbers by accident: `age = "36"` is text, so `age + 1` fails.
- Using a variable before assigning it, or misspelling it: `nmae` gives `NameError`.
- Writing `true` or `none` in lowercase. They're `True`, `False` and `None`.

@@ numbers-and-math
topics: `+ - * /`, `//`, `%`, `**`, `round()`, the `math` module
terms:
- **Operator:** a symbol that performs an operation, like `+` or `*`.
- **Floor division (`//`):** divides and rounds down to a whole number.
- **Modulo (`%`):** the remainder after division.
- **Exponent (`**`):** raises a number to a power.
- **Operator precedence:** the order in which operators are applied (`**`, then `* / // %`, then `+ -`).
- **Augmented assignment:** shortcuts like `x += 1` for `x = x + 1`.
- **Module:** a file of reusable code you bring in with `import`, like `math`.
mistakes:
- Expecting `/` to give a whole number: `6 / 2` is `3.0`. Use `//` for whole-number division.
- Comparing floats with `==`: `0.1 + 0.2 == 0.3` is `False`. Round first or compare with a small tolerance.
- Forgetting parentheses: `2 + 3 * 4` is `14`, not `20`.
- Using `math.sqrt` without `import math`.

@@ strings-basics
topics: indexing, slicing, `len()`, `+` and `*`, immutability, f-strings and format specs
terms:
- **Index:** the position of an item, starting at 0. Negative indexes count from the end.
- **Slice:** part of a sequence, `s[start:stop:step]`. The stop position isn't included.
- **len():** returns how many items (characters) something has.
- **Immutable:** can't be changed after it's created. Strings are immutable.
- **f-string:** a string starting with `f` where `{expressions}` are filled in.
- **Format spec:** formatting after a colon in an f-string, like `{price:.2f}`.
mistakes:
- Off-by-one indexes: the last character of `"Python"` is `s[5]` or `s[-1]`, not `s[6]`.
- Forgetting that the slice stop is excluded: `"Python"[0:2]` is `"Py"`.
- Trying to change a character: `s[0] = "J"` fails. Build a new string instead.
- Forgetting the `f`: `"Hi {name}"` prints the braces literally.
- Joining text and a number with `+`: `"Age: " + 36` is a `TypeError`. Use an f-string.

@@ input-and-conversion
topics: `input()`, `int()`, `float()`, `str()`, `ValueError`
terms:
- **input():** pauses the program, shows a prompt and returns what the user typed, always as a string.
- **Prompt:** the message shown to the user before they type.
- **Type conversion (casting):** turning a value into another type with `int()`, `float()`, `str()` or `bool()`.
- **ValueError:** raised when a value has the right type but can't be used, like `int("abc")`.
- **TypeError:** raised when an operation gets the wrong type, like `2026 - "1990"`.
mistakes:
- Doing math on `input()` directly. Convert first: `int(input("Age? "))`.
- Calling `int("3.5")`. Convert to `float` first, or use `float()` if decimals are allowed.
- Expecting `int(3.99)` to round. It cuts off the decimals and gives `3`; use `round()` to round.

@@ booleans-and-comparisons
topics: `==` `!=` `<` `>`, `and` / `or` / `not`, truthiness, `in`
terms:
- **Boolean expression:** an expression that results in `True` or `False`.
- **Comparison operator:** `==`, `!=`, `<`, `>`, `<=`, `>=`.
- **Logical operator:** `and`, `or`, `not`, which combine or flip booleans.
- **Short-circuiting:** Python stops evaluating `and` / `or` as soon as the answer is known.
- **Truthy / falsy:** whether a value counts as `True` or `False`. `0`, `""`, `[]`, `{}` and `None` are falsy.
- **Membership test:** checking whether a value is inside another with `in`.
mistakes:
- Using `=` instead of `==` in a condition.
- Writing `x == 1 or 2` instead of `x == 1 or x == 2` (or `x in (1, 2)`). The first is always true.
- Reading "at least 18" as `> 18`. "At least" is `>=`; "over" is `>`.
- Testing `if name != "":` when `if name:` says the same thing more clearly.

@@ if-statements
topics: `if`, `elif`, `else`, indentation, nesting, conditional expressions, `match`
terms:
- **Condition:** the boolean expression an `if` tests.
- **Block:** a group of indented lines that belong together.
- **Indentation:** spaces at the start of a line. Python uses it to define blocks (4 spaces is standard).
- **Branch:** one of the paths an `if` / `elif` / `else` can take.
- **Conditional expression:** a one-line choice: `a if condition else b`.
- **match / case:** compares one value against several patterns (Python 3.10+).
mistakes:
- Forgetting the colon at the end of `if`, `elif`, `else`.
- Mixing tabs and spaces, or indenting inconsistently, which causes `IndentationError`.
- Putting a broad condition first: check `score >= 90` before `score >= 80`, or the higher branch never runs.
- Writing a separate `if` instead of `elif`, so several branches run.

@@ while-loops
topics: `while`, loop conditions, infinite loops, accumulators, input loops
terms:
- **Loop:** code that repeats.
- **Iteration:** one pass through a loop.
- **while loop:** repeats while its condition is true.
- **Infinite loop:** a loop whose condition never becomes false.
- **Accumulator:** a variable that collects a running result, like a total.
- **Counter:** a variable that counts iterations.
mistakes:
- Forgetting to update the loop variable (`count += 1`), creating an infinite loop.
- Off-by-one conditions: `while n < 10` stops at 9; `while n <= 10` includes 10.
- Initialising the accumulator inside the loop, so it resets every time.

@@ for-loops
topics: `for`, `range()`, `enumerate()`, `zip()`, nested loops
terms:
- **for loop:** runs once for each item of a sequence.
- **Iterable:** anything you can loop over: strings, lists, ranges, dicts and more.
- **range():** generates a sequence of numbers. The stop value isn't included.
- **enumerate():** gives each item together with its index.
- **zip():** walks several sequences side by side.
- **Nested loop:** a loop inside another loop.
mistakes:
- Expecting `range(1, 5)` to include 5. It gives 1, 2, 3, 4.
- Looping with `for i in range(len(items))` and then using `items[i]` when `for item in items` (or `enumerate`) is simpler.
- Changing a list while looping over it. Loop over a copy, or build a new list.

@@ loop-control
topics: `break`, `continue`, `while True`, loop `else`
terms:
- **break:** exits the loop immediately.
- **continue:** skips the rest of this iteration and moves to the next.
- **while True:** an intentionally infinite loop that ends with `break`.
- **Loop else:** a block that runs only if the loop finished without `break`.
- **Sentinel value:** a special input that means "stop", like `"done"`.
mistakes:
- Putting `break` outside the `if`, so the loop always stops after one pass.
- Forgetting that `else` on a loop runs when there was *no* `break`. Add a comment when you use it.
- Writing `while True` without any reachable `break`.

@@ lists
topics: creating lists, indexing, `append`/`insert`/`remove`/`pop`, sorting, references, nested lists
terms:
- **List:** an ordered, changeable collection in square brackets.
- **Element (item):** one value in a list.
- **Mutable:** can be changed in place. Lists are mutable.
- **Method:** a function attached to a value, called with a dot: `items.append(x)`.
- **sorted() vs .sort():** `sorted()` returns a new list; `.sort()` sorts in place and returns `None`.
- **Reference:** a name pointing at an object. Two names can refer to the same list.
- **Shallow copy:** a new list with the same items, made with `.copy()`, `list(x)` or `x[:]`.
mistakes:
- Writing `nums = nums.sort()`, which sets `nums` to `None`.
- Expecting `b = a` to copy a list. Both names refer to the same list; use `a.copy()`.
- Calling `.remove(x)` when `x` might be missing, which raises `ValueError`. Check with `in` first.
- Confusing `append` (adds one item) with `extend` (adds every item from another list).

@@ tuples-and-unpacking
topics: tuples, immutability, unpacking, starred targets, returning several values
terms:
- **Tuple:** an ordered, unchangeable collection, usually written with parentheses.
- **Unpacking:** assigning the items of a sequence to several variables at once.
- **Starred target:** `*rest` in unpacking, which collects the remaining items into a list.
- **Hashable:** usable as a dict key or set member. Tuples of immutable values are hashable.
mistakes:
- Writing `(5)` for a one-item tuple. It needs a comma: `(5,)`.
- Unpacking the wrong number of items: `a, b = [1, 2, 3]` raises `ValueError`.
- Trying to change a tuple item. Build a new tuple or use a list.

@@ dictionaries
topics: key-value pairs, adding/changing/removing, `.get()`, `.items()`, counting, nested data
terms:
- **Dictionary (dict):** a collection of key-value pairs in braces.
- **Key:** the label used to look up a value. Keys must be unique and hashable.
- **Value:** the data stored under a key.
- **KeyError:** raised when you look up a key that doesn't exist.
- **.get(key, default):** looks up a key, returning a default instead of raising an error.
- **.items():** gives each key together with its value.
- **JSON:** a text format for data that maps closely onto dicts and lists.
mistakes:
- Using `d[key]` when the key might be missing. Use `in` or `.get()`.
- Looping with `for k in d` and expecting values. That gives keys; use `.items()` for both.
- Using a list as a key. Keys must be immutable; use a tuple.
- Forgetting the default in counting: `counts[w] = counts.get(w) + 1` fails on the first word. Use `counts.get(w, 0)`.

@@ sets
topics: unique values, membership, union `|`, intersection `&`, difference `-`
terms:
- **Set:** an unordered collection of unique values.
- **Union (`|`):** items in either set.
- **Intersection (`&`):** items in both sets.
- **Difference (`-`):** items in the first set but not the second.
- **Symmetric difference (`^`):** items in exactly one of the sets.
- **Hashing:** the technique that makes set and dict lookups fast.
mistakes:
- Writing `{}` for an empty set. That's an empty dict; use `set()`.
- Indexing a set with `s[0]`. Sets have no order; use `sorted(s)` if you need one.
- Expecting a set to keep duplicates or insertion order.

@@ comprehensions
topics: list, dict and set comprehensions, filtering with `if`, conditional values, nesting
terms:
- **Comprehension:** a compact expression that builds a collection from an iterable.
- **List comprehension:** `[expression for item in iterable if condition]`.
- **Dict comprehension:** `{key: value for item in iterable}`.
- **Set comprehension:** `{expression for item in iterable}`.
- **Filter clause:** the `if` at the end of a comprehension, which drops items.
mistakes:
- Putting a filter `if` at the front, or an `if/else` at the end. Filters go last; `a if c else b` goes first.
- Writing comprehensions so long they're hard to read. Switch to a normal loop.
- Using a list comprehension only for its side effects, like `[print(x) for x in items]`. Use a loop.

@@ string-methods
topics: `upper`/`lower`, `strip`, `split`/`join`, `find`/`replace`, `isdigit`, padding
terms:
- **String method:** a function called on a string, like `"hi".upper()`.
- **Whitespace:** spaces, tabs and new lines.
- **split():** breaks a string into a list of strings.
- **join():** glues a list of strings together with a separator.
- **Method chaining:** calling one method on the result of another: `s.strip().lower()`.
mistakes:
- Expecting a method to change the string in place. Strings are immutable: write `s = s.upper()`.
- Calling `join` on the list: it's `", ".join(items)`, not `items.join(", ")`.
- Joining non-strings: `" ".join([1, 2])` fails. Convert with `map(str, items)` first.

@@ functions-basics
topics: `def`, parameters, `return`, docstrings, print vs return, returning early
terms:
- **Function definition:** creating a function with `def name(parameters):`.
- **Parameter:** a name in the definition that receives a value.
- **Argument:** the value passed in when calling.
- **Return value:** what a function hands back with `return`.
- **Docstring:** the string right under `def` that documents the function.
- **Call:** running a function with `name(arguments)`.
- **DRY (Don't Repeat Yourself):** putting repeated logic in one function.
mistakes:
- Printing instead of returning, then trying to use the result. A function without `return` gives `None`.
- Forgetting the parentheses when calling: `greet` is the function itself; `greet()` runs it.
- Putting code after `return` and expecting it to run.
- Defining a function and never calling it.

@@ parameters
topics: defaults, keyword arguments, `*args`, `**kwargs`, unpacking, keyword-only, mutable defaults
terms:
- **Default value:** the value a parameter gets when no argument is given.
- **Positional argument:** matched to parameters by position.
- **Keyword argument:** matched to parameters by name.
- **`*args`:** collects extra positional arguments into a tuple.
- **`**kwargs`:** collects extra keyword arguments into a dict.
- **Keyword-only parameter:** a parameter after `*` that must be passed by name.
mistakes:
- Using a mutable default like `def f(items=[])`. The list is shared between calls; default to `None` instead.
- Putting a parameter without a default after one with a default.
- Passing arguments in the wrong order. Keyword arguments make calls clearer.

@@ scope-and-closures
topics: local vs global, the LEGB rule, `global`, `nonlocal`, closures
terms:
- **Scope:** where in the code a name can be used.
- **Local variable:** created inside a function; exists only while it runs.
- **Global variable:** defined at the top level of a file.
- **LEGB rule:** the lookup order: Local, Enclosing, Global, Built-in.
- **global / nonlocal:** declare that an assignment refers to a global or enclosing variable.
- **Closure:** an inner function that remembers variables from the function that created it.
mistakes:
- Assigning to a global inside a function without `global`, which creates a new local instead, or raises `UnboundLocalError` with `+=`.
- Relying on global variables to pass data around. Pass arguments and return values instead.
- Naming a variable after a built-in, like `list = [1, 2]`, which hides the real `list`.

@@ lambdas-and-higher-order
topics: functions as values, `lambda`, `key=` for sorting, `map`, `filter`, `any`, `all`
terms:
- **First-class function:** a function treated as a value: stored, passed and returned.
- **Higher-order function:** a function that takes or returns another function.
- **lambda:** a small anonymous function written in one expression.
- **key function:** a function that tells `sorted`, `min` or `max` what to compare.
- **map() / filter():** apply a function to every item / keep items where it's truthy.
mistakes:
- Calling the key function by accident: `sorted(words, key=len())` is wrong; pass `key=len`.
- Assigning lambdas to names (`square = lambda x: x * x`). Use `def` for named functions.
- Forgetting that `map` and `filter` are lazy. Wrap them in `list()` to see the results.

@@ recursion
topics: base case, recursive case, the call stack, `RecursionError`, memoization
terms:
- **Recursion:** a function calling itself on a smaller version of the problem.
- **Base case:** the condition where the function returns without recursing.
- **Recursive case:** the part that calls the function again with a smaller input.
- **Call stack:** the list of function calls waiting to finish.
- **RecursionError:** raised when calls go too deep.
- **Memoization:** caching results so repeated calls are instant, e.g. with `@lru_cache`.
mistakes:
- Missing or unreachable base case, causing `RecursionError`.
- Not moving towards the base case (calling `f(n)` instead of `f(n - 1)`).
- Forgetting to `return` the recursive call's result.

@@ exceptions
topics: tracebacks, `try`/`except`/`else`/`finally`, `raise`, custom exceptions, EAFP
terms:
- **Exception:** an error that happens while the program runs.
- **Traceback:** the error report showing the exception and the chain of calls that led to it.
- **try / except:** run code and handle specific exceptions if they happen.
- **finally:** a block that always runs, used for cleanup.
- **raise:** trigger an exception yourself.
- **Custom exception:** your own exception class, inheriting from `Exception`.
- **EAFP:** "Easier to Ask Forgiveness than Permission": try the operation and handle failure.
mistakes:
- Using a bare `except:` that hides every error, including typos in your code.
- Wrapping huge blocks in `try`. Keep the `try` around just the line that can fail.
- Catching an exception and doing nothing (`pass`) so the problem disappears silently.
- Reading a traceback from the top. Start at the bottom line.

@@ modules-and-stdlib
topics: `import` forms, `random`, `datetime`, `collections`, `__name__ == "__main__"`, pip
terms:
- **Module:** a `.py` file of reusable code.
- **Package:** a folder of modules.
- **Standard library:** the modules that come with Python.
- **import / from ... import / as:** ways to bring a module or its names into your code.
- **`__name__`:** the module's name; it's `"__main__"` when the file is run directly.
- **PyPI and pip:** the Python Package Index and the tool that installs packages from it.
mistakes:
- Naming your own file after a module, like `random.py`, which then gets imported instead of the real one.
- Using `from module import *`, which hides where names come from.
- Running code at the top level of a module you also import. Put it under `if __name__ == "__main__":`.

@@ files-csv-json
topics: `open()` and `with`, file modes, `io.StringIO`, `csv`, `json`
terms:
- **File mode:** how a file is opened: `"r"` read, `"w"` write, `"a"` append.
- **with statement:** opens a resource and closes it automatically.
- **Encoding:** how text is stored as bytes. Use `encoding="utf-8"`.
- **CSV:** comma-separated values, a plain-text table format.
- **JSON:** JavaScript Object Notation, a text format for nested data.
- **Serialization:** converting Python data to text (`json.dumps`) and back (`json.loads`).
mistakes:
- Opening a file with `"w"` when you meant `"a"`, which erases it.
- Forgetting that CSV values are strings: convert with `int()` / `float()` before doing math.
- Mixing up `json.load` (from a file) and `json.loads` (from a string).
- Splitting CSV lines with `.split(",")`, which breaks on quoted values with commas. Use the `csv` module.

@@ testing-and-debugging
topics: debugging routine, debug prints, `assert`, test functions, `unittest`, edge cases
terms:
- **Bug:** a mistake in code that makes it behave wrongly.
- **Debugging:** finding and fixing bugs.
- **assert:** checks a condition and raises `AssertionError` if it's false.
- **Unit test:** a small test of one function or piece of behaviour.
- **Edge case:** an unusual input at the boundary, like an empty list or a negative number.
- **TDD (Test-Driven Development):** write a failing test first, then the code to pass it.
mistakes:
- Changing several things at once while debugging, so you can't tell which change mattered.
- Only testing the "happy path". Test empty, single-item and negative inputs too.
- Using `assert` to validate user input. Asserts can be switched off; raise `ValueError` instead.
- Leaving debug prints in finished code.

@@ classes-and-objects
topics: `class`, `__init__`, `self`, attributes, methods, class attributes, `@classmethod`
terms:
- **Class:** a blueprint for creating objects of a new type.
- **Object (instance):** one value created from a class.
- **Attribute:** data stored on an object, like `self.name`.
- **Method:** a function defined in a class.
- **`__init__`:** the initializer that sets up a new object.
- **self:** the object a method is working on.
- **Class attribute:** a value shared by all instances.
- **classmethod / staticmethod:** methods that receive the class, or nothing, instead of an instance.
mistakes:
- Forgetting `self` as the first parameter of a method.
- Writing `name = name` instead of `self.name = name` in `__init__`, so nothing is stored.
- Calling a method without parentheses: `rex.bark` instead of `rex.bark()`.
- Creating mutable data (like a list) as a class attribute, so every object shares it.

@@ inheritance
topics: subclasses, overriding, `super()`, polymorphism, duck typing, ABCs, composition
terms:
- **Inheritance:** creating a class that reuses and extends another.
- **Parent (base) class / child (sub) class:** the class inherited from / the class that inherits.
- **Override:** redefining a parent's method in the child.
- **super():** gives access to the parent class's methods.
- **Polymorphism:** different classes responding to the same method call in their own way.
- **Duck typing:** caring what an object can do, not what class it is.
- **Abstract base class:** a class that can't be instantiated and defines methods subclasses must implement.
- **Composition:** building objects that contain other objects ("has a").
mistakes:
- Forgetting to call `super().__init__(...)`, so the parent's attributes are never set.
- Using inheritance for "has a" relationships. A Car has an Engine; it isn't one.
- Building deep inheritance chains that are hard to follow. Keep hierarchies shallow.

@@ special-methods
topics: `__str__`, `__repr__`, `__eq__`, `__lt__`, `__add__`, `__len__`, `__iter__`
terms:
- **Special (dunder) method:** a method with double underscores that Python calls for built-in syntax.
- **`__str__`:** the readable string for users (`print`, `str`).
- **`__repr__`:** the unambiguous string for developers, ideally code that recreates the object.
- **`__eq__` / `__lt__`:** define `==` and `<`.
- **Operator overloading:** defining what operators like `+` mean for your class.
- **Protocol:** a set of methods that make an object behave a certain way, like `__iter__` for iteration.
mistakes:
- Returning something other than a string from `__str__` or `__repr__`.
- Changing an object in `__add__` instead of returning a new one.
- Defining `__eq__` and expecting objects to still work in sets. Defining `__eq__` removes the default `__hash__`.

@@ properties-and-dataclasses
topics: `@property`, setters, validation, `@dataclass`, `field`, `frozen`, `order`, `__post_init__`
terms:
- **Property:** a method accessed like an attribute, created with `@property`.
- **Setter:** a method that runs when a property is assigned.
- **Encapsulation:** keeping an object's data valid by controlling access to it.
- **Dataclass:** a class whose `__init__`, `__repr__` and `__eq__` are generated from annotated fields.
- **field(default_factory=...):** gives each object its own fresh default, like a new list.
- **Frozen dataclass:** a dataclass whose objects can't be changed after creation.
mistakes:
- Naming the stored attribute the same as the property (`self.celsius` inside the `celsius` setter), causing infinite recursion. Store it as `self._celsius`.
- Using `tags: list = []` in a dataclass. Use `field(default_factory=list)`.
- Forgetting type annotations in a dataclass. Fields without annotations are ignored.

@@ iterators-and-generators
topics: `iter()`/`next()`, `yield`, laziness, generator expressions, pipelines, `yield from`
terms:
- **Iterable:** an object you can loop over.
- **Iterator:** an object that produces items one at a time with `next()`.
- **StopIteration:** the exception an iterator raises when it has no more items.
- **Generator function:** a function with `yield`, which returns a generator.
- **Generator expression:** `(expr for x in items)`, a lazy comprehension.
- **Lazy evaluation:** computing values only when they're needed.
mistakes:
- Reusing an exhausted generator. It stays empty; create a new one.
- Calling `len()` on a generator. It doesn't know its length; convert to a list if you need it.
- Using `return value` in a generator to produce items. Use `yield`.

@@ decorators
topics: wrapping functions, `@` syntax, `*args, **kwargs`, `functools.wraps`, decorators with arguments
terms:
- **Decorator:** a function that takes a function and returns a new function with extra behaviour.
- **Wrapper:** the inner function a decorator returns.
- **@ syntax:** `@deco` above `def f` means `f = deco(f)`.
- **functools.wraps:** copies the original function's name and docstring onto the wrapper.
- **Decorator factory:** a function that takes settings and returns a decorator, like `@repeat(3)`.
mistakes:
- Forgetting to return the wrapper from the decorator, so the function becomes `None`.
- Forgetting to return the result inside the wrapper.
- Not using `*args, **kwargs`, so the decorator only works for one signature.
- Writing `@repeat` instead of `@repeat(3)` for a decorator that takes arguments.

@@ context-managers
topics: `with`, `__enter__`/`__exit__`, `@contextmanager`, cleanup on errors, `suppress`
terms:
- **Context manager:** an object that runs setup and cleanup around a `with` block.
- **`__enter__` / `__exit__`:** the methods called at the start and end of the block.
- **@contextmanager:** turns a generator into a context manager; code before `yield` is setup, after it is cleanup.
- **Resource:** something that must be released: a file, a lock, a connection.
mistakes:
- Forgetting `try/finally` around `yield` in a `@contextmanager`, so cleanup is skipped on errors.
- Returning `True` from `__exit__` by accident, which silently swallows exceptions.
- Using the resource after the `with` block has closed it.

@@ type-hints
topics: annotations, `list[int]`, `dict[str, float]`, `Optional`, `X | None`, `Callable`, `TypeVar`
terms:
- **Type hint (annotation):** a note saying what type a variable, parameter or return value should be.
- **Static type checker:** a tool like mypy or Pyright that checks hints without running code.
- **Optional[X]:** X or `None`, also written `X | None`.
- **Union:** one of several types, written `X | Y`.
- **Callable:** the type of a function.
- **Generic / TypeVar:** a placeholder type so one function works with many types.
mistakes:
- Expecting Python to enforce hints at runtime. It doesn't; use a type checker.
- Writing `def f(x: int = None)`. The hint should be `int | None`.
- Overusing `Any`, which switches checking off.

@@ itertools-functools
topics: `count`, `chain`, `product`, `combinations`, `groupby`, `reduce`, `partial`, `lru_cache`
terms:
- **itertools:** the standard module of fast, lazy iteration tools.
- **Permutation:** an ordered arrangement of items.
- **Combination:** an unordered selection of items.
- **groupby:** groups consecutive items that share a key.
- **reduce:** combines items pairwise into a single value.
- **partial:** creates a function with some arguments pre-filled.
mistakes:
- Using `groupby` on unsorted data, which splits one key into several groups.
- Forgetting that itertools functions return iterators: wrap them in `list()` to see or reuse them.
- Caching functions with side effects or changing results with `lru_cache`.

@@ algorithms-and-big-o
topics: Big-O, lists vs sets, spotting O(n²), binary search, merge sort, operation costs
terms:
- **Algorithm:** a step-by-step method for solving a problem.
- **Big-O notation:** describes how running time grows with input size `n`.
- **Time complexity:** how the number of steps grows with input size.
- **Binary search:** finds a value in sorted data by halving the range each step: O(log n).
- **Divide and conquer:** split a problem in parts, solve each, combine the results.
- **Merge sort:** a divide-and-conquer sort that runs in O(n log n).
mistakes:
- Using `x in some_list` inside a loop over big data. Convert the list to a set first.
- Running binary search on unsorted data.
- Optimising before measuring. Make it correct first, then time it.

@@ capstone
topics: dataclasses, custom exceptions, CSV, generators and reports in one program
terms:
- **Capstone project:** a project that combines everything you've learned.
- **Validation:** checking data is correct before using it.
- **Alternative constructor:** a `@classmethod` that creates objects from another format, like CSV.
- **Virtual environment (venv):** an isolated folder of packages for one project.
- **Version control (Git):** a system that records every change to your code.
mistakes:
- Letting one bad record crash a whole import. Handle errors per row and report them.
- Mixing input parsing, calculations and output in one long function. Split them up.
- Skipping tests for the tricky parts (dates, money, empty data).
