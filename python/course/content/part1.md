@@@ part
id: 1
title: First Steps
level: Beginner
blurb: Write your first programs. Learn how Python reads your code, how to print, store values in variables, do math, work with text and read input.

@@@ lesson
id: how-python-runs
title: How Python runs your code
minutes: 8
summary: What a program is, what happens when you press Run, and how to use the editor.
---
A **program** is a list of instructions written for a computer. Python reads your instructions from top to bottom and carries them out one at a time.

Here is a complete Python program. Press **Run** on it and watch the output panel.

```python
print("Hello, world!")
print("I am learning Python.")
```

Two lines of code produced two lines of output. `print` is a built-in **function**: you give it a value inside the parentheses, and it shows that value on the screen.

### What happens when you press Run

Python does not understand your text directly. It processes it in stages, and the editor lets you look at each one using the tabs above the output:

1. **Tokens**: Python splits your text into small pieces called tokens, like `print`, `(`, `"Hello, world!"` and `)`.
2. **AST**: it arranges those tokens into a tree that shows the structure of your program. This is where *syntax errors* (grammar mistakes) are caught.
3. **Compile**: the tree is turned into low-level instructions. Regular Python (CPython) produces *bytecode*. This course runs Python inside your browser with Brython, which produces JavaScript instead.
4. **Run**: the instructions execute and you see the result.

![Your code goes through four stages: tokens, then a tree called the AST where syntax errors are caught, then compiling, then running, where runtime errors like dividing by zero are found](figures/run-stages.svg)

You don't need to memorise these stages now. Just remember that a typo is caught *before* anything runs, while a mistake like dividing by zero is only found *while* the program runs.

### Your first error

Errors are normal. Every programmer sees hundreds of them every week. Run this and read the message:

```python error
print("Hello)
```

Python tells you the file, the line number, and what went wrong: the text was never closed with a `"`. Fix it by adding the missing quote and run it again.

### How to use this course

- In the sandbox, every code block has a **Run** button that loads it into the editor. Change the code and run it again. Breaking things on purpose is a great way to learn.
- Each lesson ends with **exercises**. Write your answer in the editor and press **Check**. Your progress is saved in this browser.
- Short **quizzes** check that the ideas stuck.

:::exercise Say hello
Write a program that prints exactly these two lines:

```output
Hello, Python!
Let's learn together.
```
```python starter
# Write your code below
```
```python check
lines = __output__.strip().splitlines()
assert len(lines) == 2, f"Expected 2 lines of output, got {len(lines)}"
assert lines[0] == "Hello, Python!", f"Line 1 should be 'Hello, Python!' but was {lines[0]!r}"
assert lines[1] == "Let's learn together.", f"Line 2 should be \"Let's learn together.\" but was {lines[1]!r}"
```
```python solution
print("Hello, Python!")
print("Let's learn together.")
```
hint: Use two print() calls. The second line contains an apostrophe, so wrap it in double quotes: "Let's learn together."
:::

:::quiz
? What does `print("2 + 2")` display?
- 4
+ 2 + 2
- Nothing, it's an error
= The quotes make it text, so Python prints the characters exactly as written. Without quotes, `print(2 + 2)` would print 4.

? When is a syntax error detected?
+ Before the program starts running
- Only when that line runs
- After the program finishes
= Syntax errors are found while Python parses your code into a tree, before any line runs. That's why a typo on line 50 stops line 1 from running too.
:::

@@@ lesson
id: print-and-comments
title: Printing and comments
minutes: 10
summary: Print several values at once, control separators and line endings, and leave notes in your code.
---
`print` can show more than one value. Separate the values with commas and Python puts a space between them:

```python
print("Apples:", 5)
print("Total price:", 5 * 0.4, "dollars")
```

Notice that `5 * 0.4` was calculated first. Python works out each value, then prints it.

### Changing the separator and the ending

`print` has two optional settings, called **keyword arguments**:

- `sep` is what goes *between* values (a space by default).
- `end` is what goes *after* the last value (a new line by default).

```python
print("2026", "10", "02", sep="-")
print("Loading", end="")
print("...", end="")
print(" done!")
```

### Blank lines and special characters

`print()` with nothing inside prints an empty line. Inside text, a backslash starts an **escape sequence**: `\n` is a new line and `\t` is a tab.

```python
print("Line one\nLine two")
print()
print("Name:\tAda")
print("She said \"hi\"")
```

### Comments

A **comment** starts with `#`. Python ignores everything after the `#` on that line. Use comments to explain *why* the code does something, not to repeat what it obviously does.

```python
# Prices are in US dollars
price = 4.99
print(price)  # this comment sits at the end of a line
```

You can also "comment out" a line to switch it off temporarily while testing.

:::exercise Receipt line
Use **one** `print` call with the `sep` setting to print:

```output
milk|eggs|bread
```
```python starter
print("milk", "eggs", "bread")
```
```python check
assert __output__.strip() == "milk|eggs|bread", f"Expected 'milk|eggs|bread' but got {__output__.strip()!r}"
assert __source__.count("print(") == 1, "Use exactly one print() call"
```
```python solution
print("milk", "eggs", "bread", sep="|")
```
hint: Add sep="|" inside the parentheses, after the last value.
:::

:::exercise Countdown on one line
Print `3... 2... 1... Liftoff!` on a single line using **four** separate `print` calls and the `end` setting.
```python starter
print("3...")
print("2...")
print("1...")
print("Liftoff!")
```
```python check
assert __output__.strip() == "3... 2... 1... Liftoff!", f"Got {__output__.strip()!r}"
assert __source__.count("print(") == 4, "Keep the four print() calls"
```
```python solution
print("3...", end=" ")
print("2...", end=" ")
print("1...", end=" ")
print("Liftoff!")
```
hint: Give the first three calls end=" " so they finish with a space instead of a new line.
:::

:::quiz
? What does `print("a", "b", "c", sep="")` show?
+ abc
- a b c
- a,b,c
= `sep=""` puts nothing between the values.

? Which line is ignored completely by Python?
- `print("# hello")`
+ `# print("hello")`
- `print("hello") #`
= A `#` inside quotes is just a character. A `#` at the start of a line makes the whole line a comment. The third line still prints.
:::

@@@ lesson
id: variables-and-types
title: Variables and data types
minutes: 12
summary: Store values with names, understand int, float, str and bool, and check types.
---
A **variable** is a name that refers to a value. You create one with `=`, which means "assign", not "equals".

```python
name = "Ada"
age = 36
print(name, "is", age)
```

You can change what a variable refers to at any time. The newest assignment wins:

```python
score = 10
score = score + 5   # take the old value, add 5, store the result
print(score)
```

Read `score = score + 5` from right to left: Python works out `score + 5` first (15), then stores it in `score`.

![A variable is a name that points to a value: name points to the string "Ada" and age points to the integer 36](figures/variables.svg)

### Naming rules

- Names can contain letters, digits and underscores, but can't start with a digit: `total_2` is fine, `2total` is not.
- Names are case-sensitive: `Age` and `age` are different variables.
- You can't use Python keywords such as `if`, `for` or `class` as names.
- By convention, Python uses **snake_case**: lowercase words joined by underscores, like `first_name`.

### The four basic types

Every value has a **type**, which decides what you can do with it.

| Type | Meaning | Examples |
|---|---|---|
| `int` | whole number | `7`, `-3`, `1_000_000` |
| `float` | decimal number | `3.14`, `-0.5`, `2.0` |
| `str` | text (a *string*) | `"hello"`, `'Python'` |
| `bool` | true or false | `True`, `False` |

Use `type()` to ask Python what type a value is:

```python
print(type(42))
print(type(3.5))
print(type("42"))
print(type(True))
```

`42` and `"42"` look similar but are different types. One is a number you can do math with; the other is text.

```python
print(42 + 8)
print("42" + "8")
```

Adding strings joins them together. This is called **concatenation**.

### Multiple assignment

You can assign several variables in one line, and even swap two values without a temporary variable:

```python
x, y = 1, 2
x, y = y, x
print(x, y)
```

### None: the "no value" value

`None` means "nothing here yet". It has its own type, `NoneType`.

```python
result = None
print(result, type(result))
```

:::exercise Profile card
Create three variables: `name` set to `"Grace"`, `year` set to the number `1906`, and `is_programmer` set to `True`. Then print them on one line, separated by spaces.
```python starter
# Create the three variables, then print them

```
```python check
assert "name" in dir() and name == "Grace", "name should be the string 'Grace'"
assert "year" in dir() and year == 1906 and type(year) is int, "year should be the number 1906 (no quotes)"
assert "is_programmer" in dir() and is_programmer is True, "is_programmer should be True (capital T, no quotes)"
assert __output__.strip() == "Grace 1906 True", f"Expected 'Grace 1906 True' but got {__output__.strip()!r}"
```
```python solution
name = "Grace"
year = 1906
is_programmer = True
print(name, year, is_programmer)
```
hint: Numbers and True/False are written without quotes. Then use print(name, year, is_programmer).
:::

:::exercise Swap them
The variables `left` and `right` are in the wrong order. Swap their values using a single line of multiple assignment.
```python starter
left = "right"
right = "left"
# swap them here

print(left, right)
```
```python check
assert left == "left" and right == "right", f"After swapping, left should be 'left' and right should be 'right' (got {left!r}, {right!r})"
```
```python solution
left = "right"
right = "left"
left, right = right, left
print(left, right)
```
hint: left, right = right, left
:::

:::quiz
? What is the type of `"3.14"`?
- float
+ str
- int
= It's in quotes, so it's text. `float("3.14")` would convert it to a number.

? After `a = 5`, `b = a`, `a = 10`, what is `b`?
+ 5
- 10
- An error
= `b = a` makes `b` refer to the value 5. Later pointing `a` at 10 doesn't change what `b` refers to.

? Which is a valid variable name?
- `2nd_place`
- `my-score`
+ `_total`
= Names can start with an underscore. They can't start with a digit, and `-` means subtraction.
:::

@@@ lesson
id: numbers-and-math
title: Numbers and math
minutes: 12
summary: Arithmetic operators, integer division, remainders, powers, rounding and the math module.
---
Python is a handy calculator. Here are the arithmetic operators:

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | add | `7 + 2` | `9` |
| `-` | subtract | `7 - 2` | `5` |
| `*` | multiply | `7 * 2` | `14` |
| `/` | divide | `7 / 2` | `3.5` |
| `//` | floor divide (round down) | `7 // 2` | `3` |
| `%` | remainder (modulo) | `7 % 2` | `1` |
| `**` | power | `7 ** 2` | `49` |

```python
print(7 / 2)
print(7 // 2)
print(7 % 2)
print(2 ** 10)
```

Note that `/` **always** gives a float, even when the answer is whole: `6 / 2` is `3.0`.

### Remainders are surprisingly useful

`%` tells you what's left over after division. Common uses:

```python
n = 17
print(n % 2 == 0)       # is n even?
total_minutes = 135
print(total_minutes // 60, "h", total_minutes % 60, "min")
```

### Order of operations

Python follows the usual math rules: `**` first, then `*`, `/`, `//`, `%`, then `+` and `-`. Use parentheses when in doubt. They make your intent clear.

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
```

### Shortcut assignment

`x += 3` is short for `x = x + 3`. The same works for `-=`, `*=`, `/=` and the others.

```python
balance = 100
balance -= 30
balance *= 2
print(balance)
```

### Floats are approximate

Computers store decimals in binary, so some values can't be represented exactly:

```python
print(0.1 + 0.2)
print(round(0.1 + 0.2, 2))
```

This is not a Python bug; almost every language does this. Use `round(value, digits)` when displaying results. For money in real applications, use the `decimal` module.

### The math module

For more functions, **import** the `math` module:

```python
import math

print(math.sqrt(81))
print(math.pi)
print(math.floor(3.7), math.ceil(3.2))
print(abs(-5), max(3, 9, 4), min(3, 9, 4))
```

`abs`, `max`, `min` and `round` are built in, so they don't need an import.

:::exercise Split the bill
Three friends share a bill of `127` dollars, plus a `15%` tip. Calculate the amount each person pays, rounded to 2 decimal places, and store it in a variable named `each`. Print it.
```python starter
bill = 127
tip_rate = 0.15
people = 3

each = 0  # replace with your calculation
print(each)
```
```python check
assert abs(each - 48.68) < 0.001, f"each should be 48.68 but is {each}"
```
```python solution
bill = 127
tip_rate = 0.15
people = 3

each = round(bill * (1 + tip_rate) / people, 2)
print(each)
```
hint: The total with tip is bill * (1 + tip_rate). Divide by people, then use round(..., 2).
:::

:::exercise Seconds to clock time
Convert `seconds = 7384` into hours, minutes and remaining seconds using `//` and `%`. Store them in `hours`, `minutes` and `secs`, then print `2h 3m 4s`.
```python starter
seconds = 7384

```
```python check
assert hours == 2 and minutes == 3 and secs == 4, f"Expected 2, 3, 4 but got {hours}, {minutes}, {secs}"
assert __output__.strip() == "2h 3m 4s", f"Expected '2h 3m 4s' but got {__output__.strip()!r}"
```
```python solution
seconds = 7384
hours = seconds // 3600
minutes = seconds % 3600 // 60
secs = seconds % 60
print(f"{hours}h {minutes}m {secs}s")
```
hint: An hour has 3600 seconds: hours = seconds // 3600. What's left is seconds % 3600; divide that by 60 for minutes. To print without spaces before the letters, try print(str(hours) + "h", ...) or an f-string (next lesson).
:::

:::quiz
? What is `17 // 5`?
- 3.4
+ 3
- 2
= Floor division divides and rounds down to a whole number.

? What is `17 % 5`?
- 3
+ 2
- 3.4
= 5 goes into 17 three times (15), leaving a remainder of 2.

? What type does `10 / 5` produce?
- int
+ float
- str
= The `/` operator always returns a float, so the result is `2.0`.
:::

@@@ lesson
id: strings-basics
title: Strings and f-strings
minutes: 15
summary: Index and slice text, measure its length, repeat it, and build messages with f-strings.
---
A **string** is a sequence of characters. You can use single or double quotes; pick whichever avoids clashing with quotes inside the text.

```python
a = 'She said "hi"'
b = "It's sunny"
c = """Triple quotes
let text span
several lines."""
print(a)
print(b)
print(c)
```

### Length, joining and repeating

```python
word = "Python"
print(len(word))
print(word + "!")
print("ha" * 3)
```

### Indexing: getting one character

Each character has a position called an **index**. Counting starts at **0**. Negative indexes count from the end.

![The letters of "Python" with their positions: 0 to 5 counting from the front, and -6 to -1 counting from the end](figures/string-index.svg)

```output
 P  y  t  h  o  n
 0  1  2  3  4  5
-6 -5 -4 -3 -2 -1
```

```python
word = "Python"
print(word[0])
print(word[5])
print(word[-1])
```

Asking for `word[6]` causes an `IndexError` because there is no position 6.

### Slicing: getting part of a string

`word[start:stop]` gives the characters from `start` up to, but **not including**, `stop`. Leave a side empty to mean "from the beginning" or "to the end". An optional third number is the step.

![Slice positions sit between the characters: word[0:2] cuts before P and after y, giving "Py"](figures/string-slice.svg)

```python
word = "Python"
print(word[0:2])
print(word[2:])
print(word[:-1])
print(word[::2])
print(word[::-1])   # step -1 reverses
```

### Strings can't be changed

Strings are **immutable**: you can't change a character in place. `word[0] = "J"` is an error. Instead, build a new string:

```python
word = "Python"
new_word = "J" + word[1:]
print(new_word)
```

### f-strings: the best way to build messages

Put an `f` before the opening quote, then write any variable or expression inside `{}`:

```python
name = "Ada"
items = 3
price = 4.5
print(f"{name} bought {items} items for ${items * price}")
```

After a colon you can add a **format spec** to control how a value looks:

```python
pi = 3.14159265
print(f"{pi:.2f}")        # 2 decimal places
print(f"{1234567:,}")     # thousands separator
print(f"{0.256:.1%}")     # percentage
print(f"[{'left':<8}]")   # pad to 8, align left
print(f"[{'right':>8}]")  # align right
print(f"{pi=}")           # show the expression too (debugging)
```

Mixing types with `+` fails: `"Age: " + 36` is a `TypeError`. f-strings handle the conversion for you, which is one more reason to use them.

:::exercise Initials
Given `first = "grace"` and `last = "hopper"`, build the string `"G.H."` and store it in `initials`. Use indexing and the `.upper()` method (for example, `"g".upper()` gives `"G"`).
```python starter
first = "grace"
last = "hopper"

initials = ""
print(initials)
```
```python check
assert initials == "G.H.", f"initials should be 'G.H.' but is {initials!r}"
```
```python solution
first = "grace"
last = "hopper"

initials = first[0].upper() + "." + last[0].upper() + "."
print(initials)
```
hint: first[0] is "g". Uppercase it, then join everything with + and add the dots.
:::

:::exercise Price tag
Write a function-free program that sets `product = "Notebook"` and `price = 3.5`, then prints exactly:

```output
Notebook ...... $3.50
```

Use an f-string with `:.2f` for the price.
```python starter
product = "Notebook"
price = 3.5

```
```python check
assert __output__.strip() == "Notebook ...... $3.50", f"Got {__output__.strip()!r}"
```
```python solution
product = "Notebook"
price = 3.5
print(f"{product} ...... ${price:.2f}")
```
hint: print(f"{product} ...... ${price:.2f}") — the $ is just a normal character before the braces.
:::

:::quiz
? What is `"banana"[1:4]`?
+ "ana"
- "anan"
- "ban"
= Start at index 1 ('a') and stop *before* index 4, giving indexes 1, 2 and 3.

? What does `"abc"[-1]` give?
- "a"
+ "c"
- An error
= Negative indexes count from the end; -1 is the last character.

? What does `f"{7/2:.1f}"` produce?
- "3"
+ "3.5"
- "3.50"
= `.1f` means one digit after the decimal point.
:::

@@@ lesson
id: input-and-conversion
title: Input and type conversion
minutes: 10
summary: Ask the user for information, convert text to numbers and handle common conversion mistakes.
---
`input()` pauses the program, shows a prompt and waits for the user to type something. It **always returns a string**.

In this course, the **Input** box under the editor plays the role of the keyboard: each line in it answers one `input()` call. The example below fills it in for you.

```python stdin=Ada
name = input("What is your name? ")
print(f"Nice to meet you, {name}!")
```

### Converting types

Because `input()` returns text, you must convert it before doing math. These functions convert values:

| Function | Converts to | Example |
|---|---|---|
| `int()` | whole number | `int("42")` → `42` |
| `float()` | decimal | `float("2.5")` → `2.5` |
| `str()` | text | `str(42)` → `"42"` |
| `bool()` | True/False | `bool("")` → `False` |

```python stdin=1990
year = input("Birth year? ")
print(type(year))
age = 2026 - int(year)
print(f"You are about {age} years old")
```

Forget the conversion and Python complains, because it can't subtract text from a number:

```python stdin=1990 error
year = input("Birth year? ")
print(2026 - year)
```

### When conversion fails

`int("hello")` raises a `ValueError` because the text isn't a number. `int("3.7")` also fails: convert to `float` first, then to `int` (which cuts off the decimals).

```python
print(int(float("3.7")))
print(int(3.99))
print(round(3.7))
```

Later, in the Exceptions lesson, you'll learn how to catch these errors so a typo doesn't crash your program.

### Putting it together

```python stdin=4.5|3
price = float(input("Price per item: "))
qty = int(input("Quantity: "))
print(f"Total: ${price * qty:.2f}")
```

:::exercise Temperature converter
Read a temperature in Celsius with `input()`, convert it to Fahrenheit using `F = C * 9 / 5 + 32`, and print it with one decimal place, like `Fahrenheit: 98.6`.

The checker will type `37` into your program.
```python starter
celsius = input("Celsius: ")

```
```python check
assert __output__.strip().endswith("Fahrenheit: 98.6"), f"The output should end with 'Fahrenheit: 98.6'. Got {__output__.strip()!r}"
```
```python stdin
37
```
```python solution
celsius = float(input("Celsius: "))
fahrenheit = celsius * 9 / 5 + 32
print(f"Fahrenheit: {fahrenheit:.1f}")
```
hint: Wrap input(...) in float(...) so you can do math. Then print(f"Fahrenheit: {fahrenheit:.1f}").
:::

:::quiz
? What type does `input()` return?
- It depends on what the user types
+ Always str
- int
= `input()` always returns a string, even if the user types digits.

? What does `int("12") + int("3")` give?
+ 15
- "123"
- An error
= Both strings are converted to numbers first, so they add normally.

? What happens with `int("3.5")`?
- 3
- 4
+ ValueError
= `int()` can't read decimal text directly. Use `int(float("3.5"))`.
:::
