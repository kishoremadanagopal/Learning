# Learn Python from scratch

A complete, hands-on Python course for beginners: 37 lessons from your first `print()` to generators, decorators and a final project, with a practice sandbox that runs your code in the browser and checks your answers.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/Learning/python/)

The sandbox runs Python in your browser. Nothing to install, no sign-up.

- every lesson, with **187 examples** you can run and change
- **62 exercises**, numbered by lesson, that check your code with tests and tell you what's off
- **87 quiz questions**, with explanations
- a compiler view that shows your code as **tokens**, an **AST** and the **compiled JavaScript**
- a free [playground](https://kishoremadanagopal.github.io/Learning/python/playground.html) for experimenting
- your progress and code saved in your own browser

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 37 lessons, each with key terms, examples, common mistakes, exercises, answers and a quiz |
| 📖 [Glossary](glossary.md) | every Python term used in the course, defined in plain English |
| 🧾 [Syntax cheat sheet](cheatsheet.md) | the whole language on one page, with lesson numbers |

## How to use this course

1. Read a lesson, here on GitHub or in the sandbox. Start with its **Key terms**.
2. Run the examples in the sandbox and change them to see what happens.
3. Do the lesson's exercises in the sandbox and press **Check**.
4. Only then open the **Answers** section at the bottom of the lesson.

Each lesson has a **Common mistakes** section. Read it: these are the errors beginners hit most often, and you'll recognise them when they happen to you.

## Lessons

### Part 1: First Steps (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 1 | [How Python runs your code](lessons/01-how-python-runs.md) | what a program is, `print()`, syntax vs runtime errors, how code is compiled | 1 |
| 2 | [Printing and comments](lessons/02-print-and-comments.md) | `print()` with several values, `sep`, `end`, escape sequences, `#` comments | 2–3 |
| 3 | [Variables and data types](lessons/03-variables-and-types.md) | `=`, naming rules, `int`, `float`, `str`, `bool`, `type()`, `None` | 4–5 |
| 4 | [Numbers and math](lessons/04-numbers-and-math.md) | `+ - * /`, `//`, `%`, `**`, `round()`, the `math` module | 6–7 |
| 5 | [Strings and f-strings](lessons/05-strings-basics.md) | indexing, slicing, `len()`, `+` and `*`, immutability, f-strings and format specs | 8–9 |
| 6 | [Input and type conversion](lessons/06-input-and-conversion.md) | `input()`, `int()`, `float()`, `str()`, `ValueError` | 10 |

### Part 2: Decisions and Loops (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 7 | [Booleans and comparisons](lessons/07-booleans-and-comparisons.md) | `==` `!=` `<` `>`, `and` / `or` / `not`, truthiness, `in` | 11 |
| 8 | [if, elif and else](lessons/08-if-statements.md) | `if`, `elif`, `else`, indentation, nesting, conditional expressions, `match` | 12–13 |
| 9 | [while loops](lessons/09-while-loops.md) | `while`, loop conditions, infinite loops, accumulators, input loops | 14 |
| 10 | [for loops and range](lessons/10-for-loops.md) | `for`, `range()`, `enumerate()`, `zip()`, nested loops | 15–16 |
| 11 | [break, continue and loop else](lessons/11-loop-control.md) | `break`, `continue`, `while True`, loop `else` | 17 |

### Part 3: Collections (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 12 | [Lists](lessons/12-lists.md) | creating lists, indexing, `append`/`insert`/`remove`/`pop`, sorting, references, nested lists | 18–19 |
| 13 | [Tuples and unpacking](lessons/13-tuples-and-unpacking.md) | tuples, immutability, unpacking, starred targets, returning several values | 20 |
| 14 | [Dictionaries](lessons/14-dictionaries.md) | key-value pairs, adding/changing/removing, `.get()`, `.items()`, counting, nested data | 21–22 |
| 15 | [Sets](lessons/15-sets.md) | unique values, membership, union `\|`, intersection `&`, difference `-` | 23 |
| 16 | [Comprehensions](lessons/16-comprehensions.md) | list, dict and set comprehensions, filtering with `if`, conditional values, nesting | 24–25 |
| 17 | [String methods](lessons/17-string-methods.md) | `upper`/`lower`, `strip`, `split`/`join`, `find`/`replace`, `isdigit`, padding | 26–27 |

### Part 4: Functions (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 18 | [Defining functions](lessons/18-functions-basics.md) | `def`, parameters, `return`, docstrings, print vs return, returning early | 28–29 |
| 19 | [Parameters in depth](lessons/19-parameters.md) | defaults, keyword arguments, `*args`, `**kwargs`, unpacking, keyword-only, mutable defaults | 30–31 |
| 20 | [Scope and closures](lessons/20-scope-and-closures.md) | local vs global, the LEGB rule, `global`, `nonlocal`, closures | 32 |
| 21 | [Lambdas and higher-order functions](lessons/21-lambdas-and-higher-order.md) | functions as values, `lambda`, `key=` for sorting, `map`, `filter`, `any`, `all` | 33–34 |
| 22 | [Recursion](lessons/22-recursion.md) | base case, recursive case, the call stack, `RecursionError`, memoization | 35–36 |

### Part 5: Robust Programs (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 23 | [Exceptions and error handling](lessons/23-exceptions.md) | tracebacks, `try`/`except`/`else`/`finally`, `raise`, custom exceptions, EAFP | 37–38 |
| 24 | [Modules and the standard library](lessons/24-modules-and-stdlib.md) | `import` forms, `random`, `datetime`, `collections`, `__name__ == "__main__"`, pip | 39–40 |
| 25 | [Files, CSV and JSON](lessons/25-files-csv-json.md) | `open()` and `with`, file modes, `io.StringIO`, `csv`, `json` | 41–42 |
| 26 | [Testing and debugging](lessons/26-testing-and-debugging.md) | debugging routine, debug prints, `assert`, test functions, `unittest`, edge cases | 43–44 |

### Part 6: Object-Oriented Python (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 27 | [Classes and objects](lessons/27-classes-and-objects.md) | `class`, `__init__`, `self`, attributes, methods, class attributes, `@classmethod` | 45–46 |
| 28 | [Inheritance and polymorphism](lessons/28-inheritance.md) | subclasses, overriding, `super()`, polymorphism, duck typing, ABCs, composition | 47–48 |
| 29 | [Special (dunder) methods](lessons/29-special-methods.md) | `__str__`, `__repr__`, `__eq__`, `__lt__`, `__add__`, `__len__`, `__iter__` | 49 |
| 30 | [Properties and dataclasses](lessons/30-properties-and-dataclasses.md) | `@property`, setters, validation, `@dataclass`, `field`, `frozen`, `order`, `__post_init__` | 50 |

### Part 7: Advanced Python (Advanced)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 31 | [Iterators and generators](lessons/31-iterators-and-generators.md) | `iter()`/`next()`, `yield`, laziness, generator expressions, pipelines, `yield from` | 51–52 |
| 32 | [Decorators](lessons/32-decorators.md) | wrapping functions, `@` syntax, `*args, **kwargs`, `functools.wraps`, decorators with arguments | 53–54 |
| 33 | [Context managers](lessons/33-context-managers.md) | `with`, `__enter__`/`__exit__`, `@contextmanager`, cleanup on errors, `suppress` | 55 |
| 34 | [Type hints](lessons/34-type-hints.md) | annotations, `list[int]`, `dict[str, float]`, `Optional`, `X \| None`, `Callable`, `TypeVar` | 56 |
| 35 | [itertools and functools](lessons/35-itertools-functools.md) | `count`, `chain`, `product`, `combinations`, `groupby`, `reduce`, `partial`, `lru_cache` | 57–58 |
| 36 | [Algorithms and Big-O](lessons/36-algorithms-and-big-o.md) | Big-O, lists vs sets, spotting O(n²), binary search, merge sort, operation costs | 59–60 |
| 37 | [Capstone: build an expense tracker](lessons/37-capstone.md) | dataclasses, custom exceptions, CSV, generators and reports in one program | 61–62 |

## Which Python is this?

The sandbox uses [Brython](https://brython.info), which compiles Python 3 to JavaScript so it can run in your browser. The lessons teach standard Python, and everything in them also works on your own computer with Python from [python.org](https://www.python.org/). A few things differ in the sandbox:

- Only the standard library is available. Packages installed with `pip` (NumPy, pandas, requests) need Python on your computer; the [last lesson](lessons/37-capstone.md) shows how to set it up.
- Code runs on the page, so an infinite loop freezes the tab. Reload it; your progress is kept.
- Deep recursion hits the limit sooner than in regular Python.
- `input()` reads from the **Input** box under the editor, one line per call.

## Five habits that prevent most bugs

1. Read a traceback from the **bottom** up: the last line says what went wrong, the lines above say where.
2. `=` stores a value, `==` compares. Conditions always use `==`.
3. `input()` always returns text. Convert with `int()` or `float()` before doing math.
4. Indent with 4 spaces, and end every `if`, `for`, `while`, `def` and `class` line with a colon.
5. Never use `[]` or `{}` as a default argument. Default to `None` and create the list inside the function.

## Editing the course

Lessons are generated from the Markdown sources in [`course/`](course/). See [course/README.md](course/README.md) to edit lessons or add new ones.
