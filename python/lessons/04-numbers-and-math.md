# Lesson 4: Numbers and math

**You'll learn:** `+ - * /`, `//`, `%`, `**`, `round()`, the `math` module.

▶ **Practise this lesson in the [sandbox](https://kishoremadanagopal.github.io/Learning/python/#numbers-and-math)**: run every example and check your exercise answers.

## Key terms

- **Operator:** a symbol that performs an operation, like `+` or `*`.
- **Floor division (`//`):** divides and rounds down to a whole number.
- **Modulo (`%`):** the remainder after division.
- **Exponent (`**`):** raises a number to a power.
- **Operator precedence:** the order in which operators are applied (`**`, then `* / // %`, then `+ -`).
- **Augmented assignment:** shortcuts like `x += 1` for `x = x + 1`.
- **Module:** a file of reusable code you bring in with `import`, like `math`.

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

## Remainders are surprisingly useful

`%` tells you what's left over after division. Common uses:

```python
n = 17
print(n % 2 == 0)       # is n even?
total_minutes = 135
print(total_minutes // 60, "h", total_minutes % 60, "min")
```

## Order of operations

Python follows the usual math rules: `**` first, then `*`, `/`, `//`, `%`, then `+` and `-`. Use parentheses when in doubt. They make your intent clear.

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
```

## Shortcut assignment

`x += 3` is short for `x = x + 3`. The same works for `-=`, `*=`, `/=` and the others.

```python
balance = 100
balance -= 30
balance *= 2
print(balance)
```

## Floats are approximate

Computers store decimals in binary, so some values can't be represented exactly:

```python
print(0.1 + 0.2)
print(round(0.1 + 0.2, 2))
```

This is not a Python bug; almost every language does this. Use `round(value, digits)` when displaying results. For money in real applications, use the `decimal` module.

## The math module

For more functions, **import** the `math` module:

```python
import math

print(math.sqrt(81))
print(math.pi)
print(math.floor(3.7), math.ceil(3.2))
print(abs(-5), max(3, 9, 4), min(3, 9, 4))
```

`abs`, `max`, `min` and `round` are built in, so they don't need an import.

## Common mistakes

- Expecting `/` to give a whole number: `6 / 2` is `3.0`. Use `//` for whole-number division.
- Comparing floats with `==`: `0.1 + 0.2 == 0.3` is `False`. Round first or compare with a small tolerance.
- Forgetting parentheses: `2 + 3 * 4` is `14`, not `20`.
- Using `math.sqrt` without `import math`.

## Exercises

### 1. Split the bill

Three friends share a bill of `127` dollars, plus a `15%` tip. Calculate the amount each person pays, rounded to 2 decimal places, and store it in a variable named `each`. Print it.

Starter code:

```python
bill = 127
tip_rate = 0.15
people = 3

each = 0  # replace with your calculation
print(each)
```

### 2. Seconds to clock time

Convert `seconds = 7384` into hours, minutes and remaining seconds using `//` and `%`. Store them in `hours`, `minutes` and `secs`, then print `2h 3m 4s`.

Starter code:

```python
seconds = 7384

```

**In the sandbox:** exercises 6–7. Press **Check** to test your answer.

<details>
<summary>Hints</summary>

1. The total with tip is bill * (1 + tip_rate). Divide by people, then use round(..., 2).
2. An hour has 3600 seconds: hours = seconds // 3600. What's left is seconds % 3600; divide that by 60 for minutes. To print without spaces before the letters, try print(str(hours) + "h", ...) or an f-string (next lesson).

</details>

<details>
<summary>Answers</summary>

**1. Split the bill**

```python
bill = 127
tip_rate = 0.15
people = 3

each = round(bill * (1 + tip_rate) / people, 2)
print(each)
```

**2. Seconds to clock time**

```python
seconds = 7384
hours = seconds // 3600
minutes = seconds % 3600 // 60
secs = seconds % 60
print(f"{hours}h {minutes}m {secs}s")
```

</details>

## Quick quiz

1. What is `17 // 5`?
   - A) 3.4
   - B) 3
   - C) 2

2. What is `17 % 5`?
   - A) 3
   - B) 2
   - C) 3.4

3. What type does `10 / 5` produce?
   - A) int
   - B) float
   - C) str

<details>
<summary>Quiz answers</summary>

1. **B) 3**: Floor division divides and rounds down to a whole number.
2. **B) 2**: 5 goes into 17 three times (15), leaving a remainder of 2.
3. **B) float**: The `/` operator always returns a float, so the result is `2.0`.

</details>

---
Previous: [Lesson 3](03-variables-and-types.md) · Next: [Lesson 5: Strings and f-strings](05-strings-basics.md)
