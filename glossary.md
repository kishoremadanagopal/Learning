# Python glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **Abstract base class** | A class that can't be instantiated and defines methods subclasses must implement. [28] |
| **Accumulator** | A variable that collects a running result, like a total. [9] |
| **Algorithm** | A step-by-step method for solving a problem. [36] |
| **Alternative constructor** | A `@classmethod` that creates objects from another format, like CSV. [37] |
| **`*args`** | Collects extra positional arguments into a tuple. [19] |
| **Argument** | A value you pass to a function inside its parentheses. [2, 18] |
| **assert** | Checks a condition and raises `AssertionError` if it's false. [26] |
| **Assignment** | Storing a value in a variable with `=`. [3] |
| **AST (Abstract Syntax Tree)** | The tree Python builds to represent the structure of your program. [1] |
| **Attribute** | Data stored on an object, like `self.name`. [27] |
| **Augmented assignment** | Shortcuts like `x += 1` for `x = x + 1`. [4] |
| **Base case** | The condition where the function returns without recursing. [22] |
| **Big-O notation** | Describes how running time grows with input size `n`. [36] |
| **Binary search** | Finds a value in sorted data by halving the range each step: O(log n). [36] |
| **Block** | A group of indented lines that belong together. [8] |
| **bool (boolean)** | `True` or `False`. [3] |
| **Boolean expression** | An expression that results in `True` or `False`. [7] |
| **Branch** | One of the paths an `if` / `elif` / `else` can take. [8] |
| **break** | Exits the loop immediately. [11] |
| **Bug** | A mistake in code that makes it behave wrongly. [26] |
| **Bytecode** | The low-level instructions CPython compiles your code into before running it. [1] |
| **Call** | Running a function with `name(arguments)`. [18] |
| **Callable** | The type of a function. [34] |
| **Call stack** | The list of function calls waiting to finish. [22] |
| **Capstone project** | A project that combines everything you've learned. [37] |
| **Class** | A blueprint for creating objects of a new type. [27] |
| **Class attribute** | A value shared by all instances. [27] |
| **classmethod / staticmethod** | Methods that receive the class, or nothing, instead of an instance. [27] |
| **Closure** | An inner function that remembers variables from the function that created it. [20] |
| **Combination** | An unordered selection of items. [35] |
| **Comment** | Text after `#` that Python ignores. Used to explain code. [2] |
| **Comparison operator** | `==`, `!=`, `<`, `>`, `<=`, `>=`. [7] |
| **Composition** | Building objects that contain other objects ("has a"). [28] |
| **Comprehension** | A compact expression that builds a collection from an iterable. [16] |
| **Concatenation** | Joining strings with `+`. [3] |
| **Condition** | The boolean expression an `if` tests. [8] |
| **Conditional expression** | A one-line choice: `a if condition else b`. [8] |
| **Context manager** | An object that runs setup and cleanup around a `with` block. [33] |
| **@contextmanager** | Turns a generator into a context manager; code before `yield` is setup, after it is cleanup. [33] |
| **continue** | Skips the rest of this iteration and moves to the next. [11] |
| **Counter** | A variable that counts iterations. [9] |
| **CSV** | Comma-separated values, a plain-text table format. [25] |
| **Custom exception** | Your own exception class, inheriting from `Exception`. [23] |
| **Dataclass** | A class whose `__init__`, `__repr__` and `__eq__` are generated from annotated fields. [30] |
| **Data type** | The kind of value: `int`, `float`, `str`, `bool` and others. [3] |
| **Debugging** | Finding and fixing bugs. [26] |
| **Decorator** | A function that takes a function and returns a new function with extra behaviour. [32] |
| **Decorator factory** | A function that takes settings and returns a decorator, like `@repeat(3)`. [32] |
| **Default value** | The value a parameter gets when no argument is given. [19] |
| **Dict comprehension** | `{key: value for item in iterable}`. [16] |
| **Dictionary (dict)** | A collection of key-value pairs in braces. [14] |
| **Difference (`-`)** | Items in the first set but not the second. [15] |
| **Divide and conquer** | Split a problem in parts, solve each, combine the results. [36] |
| **Docstring** | The string right under `def` that documents the function. [18] |
| **DRY (Don't Repeat Yourself)** | Putting repeated logic in one function. [18] |
| **Duck typing** | Caring what an object can do, not what class it is. [28] |
| **EAFP** | "Easier to Ask Forgiveness than Permission": try the operation and handle failure. [23] |
| **Edge case** | An unusual input at the boundary, like an empty list or a negative number. [26] |
| **Element (item)** | One value in a list. [12] |
| **Encapsulation** | Keeping an object's data valid by controlling access to it. [30] |
| **Encoding** | How text is stored as bytes. Use `encoding="utf-8"`. [25] |
| **end** | The text `print` puts after the last value (a new line by default). [2] |
| **`__enter__` / `__exit__`** | The methods called at the start and end of the block. [33] |
| **enumerate()** | Gives each item together with its index. [10] |
| **`__eq__` / `__lt__`** | Define `==` and `<`. [29] |
| **Escape sequence** | A backslash code inside a string, like `\n` (new line) or `\t` (tab). [2] |
| **Exception** | An error that happens while the program runs. [23] |
| **Exponent (`**`)** | Raises a number to a power. [4] |
| **field(default_factory=...)** | Gives each object its own fresh default, like a new list. [30] |
| **File mode** | How a file is opened: `"r"` read, `"w"` write, `"a"` append. [25] |
| **Filter clause** | The `if` at the end of a comprehension, which drops items. [16] |
| **finally** | A block that always runs, used for cleanup. [23] |
| **First-class function** | A function treated as a value: stored, passed and returned. [21] |
| **float** | A number with a decimal point, like `3.14`. [3] |
| **Floor division (`//`)** | Divides and rounds down to a whole number. [4] |
| **for loop** | Runs once for each item of a sequence. [10] |
| **Format spec** | Formatting after a colon in an f-string, like `{price:.2f}`. [5] |
| **Frozen dataclass** | A dataclass whose objects can't be changed after creation. [30] |
| **f-string** | A string starting with `f` where `{expressions}` are filled in. [5] |
| **Function** | A named piece of code that does a job, like `print`. You call it with parentheses: `print("hi")`. [1] |
| **Function definition** | Creating a function with `def name(parameters):`. [18] |
| **functools.wraps** | Copies the original function's name and docstring onto the wrapper. [32] |
| **Generator expression** | `(expr for x in items)`, a lazy comprehension. [31] |
| **Generator function** | A function with `yield`, which returns a generator. [31] |
| **Generic / TypeVar** | A placeholder type so one function works with many types. [34] |
| **.get(key, default)** | Looks up a key, returning a default instead of raising an error. [14] |
| **global / nonlocal** | Declare that an assignment refers to a global or enclosing variable. [20] |
| **Global variable** | Defined at the top level of a file. [20] |
| **groupby** | Groups consecutive items that share a key. [35] |
| **Hashable** | Usable as a dict key or set member. Tuples of immutable values are hashable. [13] |
| **Hashing** | The technique that makes set and dict lookups fast. [15] |
| **Higher-order function** | A function that takes or returns another function. [21] |
| **Immutable** | Can't be changed after it's created. Strings are immutable. [5] |
| **import / from ... import / as** | Ways to bring a module or its names into your code. [24] |
| **Indentation** | Spaces at the start of a line. Python uses it to define blocks (4 spaces is standard). [8] |
| **Index** | The position of an item, starting at 0. Negative indexes count from the end. [5] |
| **Infinite loop** | A loop whose condition never becomes false. [9] |
| **Inheritance** | Creating a class that reuses and extends another. [28] |
| **`__init__`** | The initializer that sets up a new object. [27] |
| **input()** | Pauses the program, shows a prompt and returns what the user typed, always as a string. [6] |
| **int** | A whole number, like `42`. [3] |
| **Interpreter** | The program that reads and runs your Python code. [1] |
| **Intersection (`&`)** | Items in both sets. [15] |
| **.items()** | Gives each key together with its value. [14] |
| **Iterable** | Anything you can loop over: strings, lists, ranges, dicts and more. [10, 31] |
| **Iteration** | One pass through a loop. [9] |
| **Iterator** | An object that produces items one at a time with `next()`. [31] |
| **itertools** | The standard module of fast, lazy iteration tools. [35] |
| **join()** | Glues a list of strings together with a separator. [17] |
| **JSON** | A text format for data that maps closely onto dicts and lists. [14, 25] |
| **Key** | The label used to look up a value. Keys must be unique and hashable. [14] |
| **KeyError** | Raised when you look up a key that doesn't exist. [14] |
| **key function** | A function that tells `sorted`, `min` or `max` what to compare. [21] |
| **Keyword argument** | An argument passed by name, like `sep="-"` or `end=""`. [2, 19] |
| **Keyword-only parameter** | A parameter after `*` that must be passed by name. [19] |
| **`**kwargs`** | Collects extra keyword arguments into a dict. [19] |
| **lambda** | A small anonymous function written in one expression. [21] |
| **Lazy evaluation** | Computing values only when they're needed. [31] |
| **LEGB rule** | The lookup order: Local, Enclosing, Global, Built-in. [20] |
| **len()** | Returns how many items (characters) something has. [5] |
| **List** | An ordered, changeable collection in square brackets. [12] |
| **List comprehension** | `[expression for item in iterable if condition]`. [16] |
| **Local variable** | Created inside a function; exists only while it runs. [20] |
| **Logical operator** | `and`, `or`, `not`, which combine or flip booleans. [7] |
| **Loop** | Code that repeats. [9] |
| **Loop else** | A block that runs only if the loop finished without `break`. [11] |
| **map() / filter()** | Apply a function to every item / keep items where it's truthy. [21] |
| **match / case** | Compares one value against several patterns (Python 3.10+). [8] |
| **Membership test** | Checking whether a value is inside another with `in`. [7] |
| **Memoization** | Caching results so repeated calls are instant, e.g. with `@lru_cache`. [22] |
| **Merge sort** | A divide-and-conquer sort that runs in O(n log n). [36] |
| **Method** | A function attached to a value, called with a dot: `items.append(x)`. [12, 27] |
| **Method chaining** | Calling one method on the result of another: `s.strip().lower()`. [17] |
| **Module** | A file of reusable code you bring in with `import`, like `math`. [4, 24] |
| **Modulo (`%`)** | The remainder after division. [4] |
| **Mutable** | Can be changed in place. Lists are mutable. [12] |
| **`__name__`** | The module's name; it's `"__main__"` when the file is run directly. [24] |
| **Nested loop** | A loop inside another loop. [10] |
| **None** | A special value meaning "nothing" or "no value yet". [3] |
| **Object (instance)** | One value created from a class. [27] |
| **Operator** | A symbol that performs an operation, like `+` or `*`. [4] |
| **Operator overloading** | Defining what operators like `+` mean for your class. [29] |
| **Operator precedence** | The order in which operators are applied (`**`, then `* / // %`, then `+ -`). [4] |
| **Optional[X]** | X or `None`, also written `X \| None`. [34] |
| **Output** | What a program shows on the screen. [1] |
| **Override** | Redefining a parent's method in the child. [28] |
| **Package** | A folder of modules. [24] |
| **Parameter** | A name in the definition that receives a value. [18] |
| **Parent (base) class / child (sub) class** | The class inherited from / the class that inherits. [28] |
| **partial** | Creates a function with some arguments pre-filled. [35] |
| **Permutation** | An ordered arrangement of items. [35] |
| **Polymorphism** | Different classes responding to the same method call in their own way. [28] |
| **Positional argument** | Matched to parameters by position. [19] |
| **Program** | A list of instructions for a computer, run from top to bottom. [1] |
| **Prompt** | The message shown to the user before they type. [6] |
| **Property** | A method accessed like an attribute, created with `@property`. [30] |
| **Protocol** | A set of methods that make an object behave a certain way, like `__iter__` for iteration. [29] |
| **PyPI and pip** | The Python Package Index and the tool that installs packages from it. [24] |
| **Python** | A popular, readable programming language. The standard version is called CPython. [1] |
| **raise** | Trigger an exception yourself. [23] |
| **range()** | Generates a sequence of numbers. The stop value isn't included. [10] |
| **Recursion** | A function calling itself on a smaller version of the problem. [22] |
| **RecursionError** | Raised when calls go too deep. [22] |
| **Recursive case** | The part that calls the function again with a smaller input. [22] |
| **reduce** | Combines items pairwise into a single value. [35] |
| **Reference** | A name pointing at an object. Two names can refer to the same list. [12] |
| **`__repr__`** | The unambiguous string for developers, ideally code that recreates the object. [29] |
| **Resource** | Something that must be released: a file, a lock, a connection. [33] |
| **Return value** | What a function hands back with `return`. [18] |
| **Scope** | Where in the code a name can be used. [20] |
| **self** | The object a method is working on. [27] |
| **Sentinel value** | A special input that means "stop", like `"done"`. [11] |
| **sep** | The text `print` puts between values (a space by default). [2] |
| **Serialization** | Converting Python data to text (`json.dumps`) and back (`json.loads`). [25] |
| **Set** | An unordered collection of unique values. [15] |
| **Set comprehension** | `{expression for item in iterable}`. [16] |
| **Setter** | A method that runs when a property is assigned. [30] |
| **Shallow copy** | A new list with the same items, made with `.copy()`, `list(x)` or `x[:]`. [12] |
| **Short-circuiting** | Python stops evaluating `and` / `or` as soon as the answer is known. [7] |
| **Slice** | Part of a sequence, `s[start:stop:step]`. The stop position isn't included. [5] |
| **snake_case** | The Python naming style: lowercase words joined by underscores. [3] |
| **sorted() vs .sort()** | `sorted()` returns a new list; `.sort()` sorts in place and returns `None`. [12] |
| **Special (dunder) method** | A method with double underscores that Python calls for built-in syntax. [29] |
| **split()** | Breaks a string into a list of strings. [17] |
| **Standard library** | The modules that come with Python. [24] |
| **Starred target** | `*rest` in unpacking, which collects the remaining items into a list. [13] |
| **Static type checker** | A tool like mypy or Pyright that checks hints without running code. [34] |
| **StopIteration** | The exception an iterator raises when it has no more items. [31] |
| **`__str__`** | The readable string for users (`print`, `str`). [29] |
| **String method** | A function called on a string, like `"hi".upper()`. [17] |
| **str (string)** | Text, written in quotes. [3] |
| **super()** | Gives access to the parent class's methods. [28] |
| **Symmetric difference (`^`)** | Items in exactly one of the sets. [15] |
| **Syntax** | The grammar rules of a language. Breaking them gives a *syntax error* before anything runs. [1] |
| **@ syntax** | `@deco` above `def f` means `f = deco(f)`. [32] |
| **TDD (Test-Driven Development)** | Write a failing test first, then the code to pass it. [26] |
| **Time complexity** | How the number of steps grows with input size. [36] |
| **Token** | The smallest meaningful piece of code, like `print`, `(` or `"hello"`. [1] |
| **Traceback** | The error report showing the exception and the chain of calls that led to it. [23] |
| **Truthy / falsy** | Whether a value counts as `True` or `False`. `0`, `""`, `[]`, `{}` and `None` are falsy. [7] |
| **try / except** | Run code and handle specific exceptions if they happen. [23] |
| **Tuple** | An ordered, unchangeable collection, usually written with parentheses. [13] |
| **Type conversion (casting)** | Turning a value into another type with `int()`, `float()`, `str()` or `bool()`. [6] |
| **TypeError** | Raised when an operation gets the wrong type, like `2026 - "1990"`. [6] |
| **Type hint (annotation)** | A note saying what type a variable, parameter or return value should be. [34] |
| **Union (`\|`)** | Items in either set. [15] |
| **Union** | One of several types, written `X \| Y`. [34] |
| **Unit test** | A small test of one function or piece of behaviour. [26] |
| **Unpacking** | Assigning the items of a sequence to several variables at once. [13] |
| **Validation** | Checking data is correct before using it. [37] |
| **Value** | The data stored under a key. [14] |
| **ValueError** | Raised when a value has the right type but can't be used, like `int("abc")`. [6] |
| **Variable** | A name that refers to a value. [3] |
| **Version control (Git)** | A system that records every change to your code. [37] |
| **Virtual environment (venv)** | An isolated folder of packages for one project. [37] |
| **while loop** | Repeats while its condition is true. [9] |
| **while True** | An intentionally infinite loop that ends with `break`. [11] |
| **Whitespace** | Spaces, tabs and new lines. [17] |
| **with statement** | Opens a resource and closes it automatically. [25] |
| **Wrapper** | The inner function a decorator returns. [32] |
| **zip()** | Walks several sequences side by side. [10] |
