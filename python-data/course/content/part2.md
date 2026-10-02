@@@ part
id: 2
title: NumPy
level: Beginner
blurb: Work with whole arrays of numbers at once: create, slice, filter, calculate and summarise them, and simulate randomness. NumPy is the engine underneath pandas and almost every AI library.

@@@ lesson
id: numpy-arrays
title: NumPy arrays
minutes: 15
summary: What an array is, why it's faster than a list, and how to create arrays and inspect their shape and type.
---
A **NumPy array** is a grid of numbers that all have the same type. It looks like a list, but it's built for maths: you can add, multiply or average a million numbers with one short line, and it runs far faster than a loop.

```python
import numpy as np

prices = np.array([4.5, 6.0, 35.0, 59.0, 79.0])
print(prices)
print(type(prices))
```

### Arrays do maths on every item

This is the big difference from lists. Watch what `* 2` does to each:

```python
import numpy as np

as_list = [1, 2, 3]
as_array = np.array([1, 2, 3])

print(as_list * 2)    # a list repeats itself
print(as_array * 2)   # an array doubles every number
print(as_array + 10)
print(as_array * as_array)
```

Doing the same operation to every item without writing a loop is called **vectorisation**. Here's the payoff: adding 20% tax to every price.

```python
import numpy as np

prices = np.array([4.5, 6.0, 35.0, 59.0, 79.0])
with_tax = prices * 1.2
print(with_tax)
```

### How much faster?

Let's time a loop against NumPy on a million numbers:

```python
import time
import numpy as np

numbers = list(range(1_000_000))
start = time.perf_counter()
total = 0
for n in numbers:
    total += n * n
loop_time = time.perf_counter() - start

arr = np.arange(1_000_000)
start = time.perf_counter()
total2 = (arr * arr).sum()
numpy_time = time.perf_counter() - start

print(total == total2)
print(f"NumPy was about {loop_time / numpy_time:.0f} times faster")
```

The exact number changes each run and from computer to computer, but NumPy usually wins by 10 to 100 times. That's why pandas, scikit-learn and PyTorch are all built on arrays.

### Shape, size and dtype

Every array knows its **shape** (how many items along each direction), its **size** (total items) and its **dtype** (the type of every item):

```python
import numpy as np

scores = np.array([[72, 85, 90],
                   [64, 70, 58]])

print(scores.shape)   # (rows, columns)
print(scores.ndim)    # number of dimensions
print(scores.size)
print(scores.dtype)
```

A 1-D array is a row of numbers; a 2-D array is a table (rows and columns). Machine learning uses 3-D and bigger arrays too, such as a stack of images.

Because every item shares one dtype, NumPy converts mixed inputs to the most general type:

```python
import numpy as np

print(np.array([1, 2, 3]).dtype)       # all whole numbers
print(np.array([1, 2, 3.5]).dtype)     # one float makes them all floats
print(np.array([1, 2, 3.5]))
print(np.array([1, 2, 3]).astype(float))
```

### Ready-made arrays

You don't always type the numbers in. These functions create arrays for you:

| Function | Makes |
|---|---|
| `np.arange(start, stop, step)` | evenly spaced numbers, like `range` (stop not included) |
| `np.linspace(start, stop, n)` | `n` evenly spaced numbers, stop included |
| `np.zeros(n)` / `np.ones(n)` | `n` zeros or ones |
| `np.full(n, value)` | `n` copies of a value |

```python
import numpy as np

print(np.arange(0, 10, 2))
print(np.linspace(0, 1, 5))
print(np.zeros(3))
print(np.ones((2, 3)))
print(np.full(4, 7))
```

`np.ones((2, 3))` takes the shape as a tuple: 2 rows, 3 columns.

:::exercise Prices with a discount
Make an array called `prices` holding `899.0, 249.0, 79.0, 189.0` (in that order). Then make `sale` by taking 15% off every price (multiply by 0.85). Don't use a loop.
```python starter
import numpy as np

```
```python check
import numpy as np
p = need("prices", np.ndarray)
same(p, np.array([899.0, 249.0, 79.0, 189.0]), "prices")
same(need("sale", np.ndarray), np.array([899.0, 249.0, 79.0, 189.0]) * 0.85, "sale")
assert not uses("for "), "Do it without a loop: multiply the whole array."
```
```python solution
import numpy as np

prices = np.array([899.0, 249.0, 79.0, 189.0])
sale = prices * 0.85
print(sale)
```
hint: `sale = prices * 0.85` multiplies every item at once.
:::

:::exercise Build a grid
Create a 2-D array called `grid` of zeros with **3 rows and 4 columns**, and store its shape in `grid_shape`.
```python starter
import numpy as np

```
```python check
import numpy as np
g = need("grid", np.ndarray)
same(g, np.zeros((3, 4)), "grid")
same(need("grid_shape"), (3, 4), "grid_shape")
```
```python solution
import numpy as np

grid = np.zeros((3, 4))
grid_shape = grid.shape
print(grid)
print(grid_shape)
```
hint: Pass the shape as a tuple: `np.zeros((3, 4))`. The shape is in `grid.shape`.
:::

:::quiz
? What does `np.array([1, 2, 3]) * 2` give?
- `[1, 2, 3, 1, 2, 3]`
+ `[2 4 6]`
- An error
= Arrays apply maths to every item. It's lists that repeat themselves when multiplied.
? An array has shape `(4, 6)`. How many numbers does it hold?
- 10
+ 24
- 6
= Shape `(4, 6)` means 4 rows and 6 columns, so 4 × 6 = 24 items.
? Why is `np.array([1, 2, 3.5]).dtype` a float type?
+ Every item in an array shares one type, so the whole numbers become floats
- NumPy always uses floats
- Because the array has three items
= An array has a single dtype. One float forces the rest to be stored as floats too.
:::

@@@ lesson
id: array-indexing
title: Indexing, slicing and filtering arrays
minutes: 16
summary: Pick items, rows and columns out of arrays, and filter them with true/false masks.
---
Getting the right numbers out of an array works like lists, with two big extras: you can index rows and columns together, and you can filter with a **mask**.

### Single items and slices

```python
import numpy as np

temps = np.array([3.1, 4.8, 7.2, 10.5, 14.0, 17.3, 19.6])
print(temps[0])      # first
print(temps[-1])     # last
print(temps[2:5])    # items 2, 3 and 4
print(temps[::2])    # every second item
```

### Rows and columns in 2-D

For a 2-D array, put the row and column inside one pair of brackets, separated by a comma: `arr[row, col]`. A `:` on its own means "all".

```python
import numpy as np

# rows are students, columns are math, science, english
scores = np.array([[72, 85, 90],
                   [64, 70, 58],
                   [88, 91, 79],
                   [55, 62, 71]])

print(scores[1, 2])     # row 1, column 2
print(scores[0])        # the whole first row
print(scores[:, 0])     # the whole first column (all math scores)
print(scores[1:3, :2])  # rows 1-2, first two columns
```

### Boolean masks: filtering

Comparing an array with a value gives an array of `True`/`False`, one per item. That's a **mask**:

```python
import numpy as np

temps = np.array([3.1, 4.8, 7.2, 10.5, 14.0, 17.3, 19.6])
warm = temps > 10
print(warm)
```

Put a mask inside the brackets and you get only the items where it's `True`:

```python
import numpy as np

temps = np.array([3.1, 4.8, 7.2, 10.5, 14.0, 17.3, 19.6])
print(temps[temps > 10])
print(temps[temps < 5])
print("Warm days:", (temps > 10).sum())
```

`(temps > 10).sum()` counts the warm days, because `True` counts as 1 and `False` as 0. You'll use this trick constantly.

### Combining conditions

Use `&` (and), `|` (or) and `~` (not). Each condition **must** be in brackets:

```python
import numpy as np

temps = np.array([3.1, 4.8, 7.2, 10.5, 14.0, 17.3, 19.6])
mild = temps[(temps > 5) & (temps < 15)]
extreme = temps[(temps < 4) | (temps > 18)]
print(mild)
print(extreme)
```

Python's `and`/`or` don't work on arrays and give an error:

```python error
import numpy as np

temps = np.array([3.1, 4.8, 7.2, 10.5])
print(temps[temps > 5 and temps < 15])
```

### Picking by a list of positions

You can also pass a list of positions, called **fancy indexing**:

```python
import numpy as np

products = np.array(["Laptop", "Monitor", "Headphones", "Notebook", "Pen Pack"])
print(products[[0, 3]])
```

### Changing values

Assigning to an index, slice or mask changes the array in place. A common use is fixing bad readings:

```python
import numpy as np

readings = np.array([12.0, -999.0, 14.5, 13.2, -999.0, 15.1])
readings[readings == -999.0] = np.nan    # mark missing values
print(readings)
```

`np.nan` means "not a number", NumPy's marker for a missing value. You'll see much more of it in pandas.

### Slices are views

A slice of an array is a **view**: a window onto the same numbers, not a copy. Changing the view changes the original. Use `.copy()` when you want an independent array:

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
part = a[1:4]
part[0] = 99
print(a)          # the original changed!

b = np.array([1, 2, 3, 4, 5])
safe = b[1:4].copy()
safe[0] = 99
print(b)          # unchanged
```

:::exercise Warm days
Using the `temps` array of 14 daily temperatures, make `warm` holding only the temperatures **above 15**, and `n_warm` holding how many there are.
```python starter
import numpy as np

temps = np.array([12.5, 16.1, 14.8, 18.0, 21.3, 15.0, 13.9,
                  17.6, 19.2, 11.4, 15.5, 22.0, 14.1, 16.8])

```
```python check
import numpy as np
t = np.array([12.5, 16.1, 14.8, 18.0, 21.3, 15.0, 13.9, 17.6, 19.2, 11.4, 15.5, 22.0, 14.1, 16.8])
same(need("warm", np.ndarray), t[t > 15], "warm")
same(need("n_warm"), 8, "n_warm")
```
```python solution
import numpy as np

temps = np.array([12.5, 16.1, 14.8, 18.0, 21.3, 15.0, 13.9,
                  17.6, 19.2, 11.4, 15.5, 22.0, 14.1, 16.8])
warm = temps[temps > 15]
n_warm = (temps > 15).sum()
print(warm, n_warm)
```
hint: `temps[temps > 15]` filters; `(temps > 15).sum()` counts the `True` values.
:::

:::exercise Science column
`scores` has one row per student and the columns math, science, english. Store the **science** column (all rows) in `science`, and the scores of the **third student** (row 2) in `third`.
```python starter
import numpy as np

scores = np.array([[72, 85, 90],
                   [64, 70, 58],
                   [88, 91, 79],
                   [55, 62, 71]])

```
```python check
import numpy as np
same(need("science", np.ndarray), np.array([85, 70, 91, 62]), "science")
same(need("third", np.ndarray), np.array([88, 91, 79]), "third")
```
```python solution
import numpy as np

scores = np.array([[72, 85, 90],
                   [64, 70, 58],
                   [88, 91, 79],
                   [55, 62, 71]])
science = scores[:, 1]
third = scores[2]
print(science, third)
```
hint: Columns are the second index: `scores[:, 1]` means all rows, column 1.
:::

:::quiz
? What does `arr[:, 0]` select from a 2-D array?
- The first row
+ The first column, from every row
- The first item only
= `:` means "every row", and `0` picks column 0.
? Which line correctly keeps values between 5 and 15?
- `a[a > 5 and a < 15]`
+ `a[(a > 5) & (a < 15)]`
- `a[a > 5 & a < 15]`
= Use `&` with each condition in brackets. `and` doesn't work on arrays, and without brackets `&` runs first.
? `part = a[1:4]` then `part[0] = 99`. What happens to `a`?
+ `a` changes too, because a slice is a view
- Nothing, a slice is a copy
- An error is raised
= Slices share the original's numbers. Use `.copy()` when you want to change one without the other.
:::

@@@ lesson
id: vectorised-math
title: Maths on whole arrays
minutes: 15
summary: Arithmetic between arrays, broadcasting, NumPy's maths functions, np.where and missing values.
---
In the last two lessons you multiplied an array by a number. This lesson covers the rest of array maths: arrays with arrays, rows with tables, and NumPy's library of functions.

### Array with array

When two arrays have the same shape, maths happens item by item, matching positions:

```python
import numpy as np

units = np.array([3, 1, 12, 2])
price = np.array([35.0, 899.0, 4.5, 249.0])
revenue = units * price
print(revenue)
print("Total:", revenue.sum())
```

Shapes that don't match give an error:

```python error
import numpy as np

print(np.array([1, 2, 3]) + np.array([10, 20]))
```

### Broadcasting

NumPy will stretch a smaller array to fit a bigger one when it can. This is called **broadcasting**. A single number broadcasts to every item, and a row broadcasts down every row of a table:

```python
import numpy as np

# 3 stores x 4 products: units sold
units = np.array([[5, 2, 0, 7],
                  [3, 8, 1, 4],
                  [6, 1, 2, 2]])
prices = np.array([10.0, 25.0, 40.0, 5.0])   # one price per product

revenue = units * prices     # the price row is used for every store
print(revenue)
print("Per store:", revenue.sum(axis=1))
```

The rule: shapes line up from the right, and each pair of sizes must be equal or one of them must be 1. Here `(3, 4)` and `(4,)` line up on the 4.

### Maths functions (ufuncs)

NumPy has fast versions of every maths function. They work on whole arrays and are called **ufuncs** (universal functions):

```python
import numpy as np

x = np.array([1.0, 4.0, 9.0, 16.0])
print(np.sqrt(x))
print(np.round(np.log(x), 3))
print(np.abs(np.array([-3, 2, -7])))
print(np.round(np.array([2.456, 3.14159]), 2))
print(np.maximum(np.array([1, 5, 3]), np.array([4, 2, 6])))
```

### np.where: if/else for every item

`np.where(condition, a, b)` picks from `a` where the condition is true and from `b` where it's false. It's the array version of an `if`:

```python
import numpy as np

scores = np.array([45, 72, 38, 90, 61])
result = np.where(scores >= 50, "pass", "fail")
print(result)

capped = np.where(scores > 80, 80, scores)
print(capped)
```

### Missing values: nan

`np.nan` marks a missing number. It spreads: any maths with `nan` gives `nan`. The `nan` functions skip it:

```python
import numpy as np

temps = np.array([12.0, np.nan, 14.5, 13.0])
print(temps.mean())         # nan: one missing value spoils it
print(np.nanmean(temps))    # ignores the missing value
print(np.isnan(temps))
print("Missing:", np.isnan(temps).sum())
```

Note `np.nan == np.nan` is `False`, so always test with `np.isnan()`, never `==`.

### A worked example: normalising

A common step before machine learning is **scaling** numbers to the range 0 to 1, so big and small features count equally. With arrays it's one line:

```python
import numpy as np

ages = np.array([18, 25, 40, 33, 61, 52])
scaled = (ages - ages.min()) / (ages.max() - ages.min())
print(np.round(scaled, 2))
```

:::exercise Line totals
`units` and `prices` describe five order lines. Make `line_totals` (units × price for each line) and `grand_total` (the sum of all lines).
```python starter
import numpy as np

units = np.array([2, 10, 1, 4, 3])
prices = np.array([249.0, 4.5, 899.0, 35.0, 59.0])

```
```python check
import numpy as np
u = np.array([2, 10, 1, 4, 3]); p = np.array([249.0, 4.5, 899.0, 35.0, 59.0])
same(need("line_totals", np.ndarray), u * p, "line_totals")
same(need("grand_total"), float((u * p).sum()), "grand_total")
```
```python solution
import numpy as np

units = np.array([2, 10, 1, 4, 3])
prices = np.array([249.0, 4.5, 899.0, 35.0, 59.0])
line_totals = units * prices
grand_total = line_totals.sum()
print(line_totals, grand_total)
```
hint: Multiply the two arrays directly, then call `.sum()` on the result.
:::

:::exercise Grade labels
Use `np.where` to turn `scores` into an array called `grades` that holds `"pass"` for scores of **60 or more** and `"retake"` otherwise.
```python starter
import numpy as np

scores = np.array([58, 73, 91, 60, 44, 67])

```
```python check
import numpy as np
same(list(need("grades", np.ndarray)), ["retake", "pass", "pass", "pass", "retake", "pass"], "grades")
assert uses("np.where"), "Use np.where."
```
```python solution
import numpy as np

scores = np.array([58, 73, 91, 60, 44, 67])
grades = np.where(scores >= 60, "pass", "retake")
print(grades)
```
hint: `np.where(scores >= 60, "pass", "retake")`.
:::

:::quiz
? What does broadcasting let you do?
- Send arrays over the internet
+ Combine arrays of different shapes by stretching the smaller one
- Print an array on several lines
= A single number or a row is "stretched" to match a bigger array, so you don't have to copy it yourself.
? What is `np.array([1.0, np.nan, 3.0]).mean()`?
- `2.0`
+ `nan`
- An error
= Any maths involving `nan` gives `nan`. Use `np.nanmean` to skip missing values.
? What does `np.where(a > 0, a, 0)` do?
+ Replaces negative numbers (and zeros) with 0 and keeps positive ones
- Finds the position of the first positive number
- Removes negative numbers from the array
= It chooses item by item: `a` where the condition is true, `0` where it isn't. The length stays the same.
:::

@@@ lesson
id: array-statistics
title: Summarising arrays
minutes: 16
summary: Sum, mean, median, spread and extremes, along rows or columns with axis, plus reshaping and loading numbers from a file.
---
Summary numbers like the total, average and spread are the backbone of every report. NumPy computes them in one call, for a whole array or for each row or column.

### The essential summaries

```python
import numpy as np

sales = np.array([120, 95, 143, 88, 160, 132, 101])
print("total  ", sales.sum())
print("mean   ", sales.mean())
print("median ", np.median(sales))
print("min/max", sales.min(), sales.max())
print("std    ", round(sales.std(), 2))
print("best day index:", sales.argmax())
```

| Summary | Meaning |
|---|---|
| **mean** | the average: total divided by count |
| **median** | the middle value when sorted; not pulled around by extreme values |
| **std** (standard deviation) | how spread out the values are around the mean |
| **argmax / argmin** | the *position* of the largest / smallest value |

### Mean versus median

One huge value drags the mean but not the median. That's why house prices and salaries are usually reported as medians:

```python
import numpy as np

salaries = np.array([32_000, 35_000, 38_000, 41_000, 45_000])
print(salaries.mean(), np.median(salaries))

with_ceo = np.append(salaries, 900_000)
print(with_ceo.mean(), np.median(with_ceo))
```

### Percentiles

The 90th **percentile** is the value 90% of the data falls below. The 25th, 50th and 75th percentiles are called the **quartiles**, and the 50th is the median:

```python
import numpy as np

times = np.array([1.2, 0.8, 2.5, 1.9, 0.6, 3.8, 1.1, 1.4, 0.9, 7.2])
print(np.percentile(times, [25, 50, 75]))
print("90% of requests took under", np.percentile(times, 90), "seconds")
```

### axis: rows or columns

On a 2-D array, `axis=0` summarises **down the columns** (one answer per column) and `axis=1` summarises **across the rows** (one answer per row):

```python
import numpy as np

# rows: 4 students. columns: math, science, english
scores = np.array([[72, 85, 90],
                   [64, 70, 58],
                   [88, 91, 79],
                   [55, 62, 71]])

print("average per subject:", scores.mean(axis=0))
print("average per student:", scores.mean(axis=1).round(1))
print("best student per subject:", scores.argmax(axis=0))
```

A way to remember it: the axis you name is the one that **disappears**. Shape `(4, 3)` with `axis=0` gives 3 answers; with `axis=1` it gives 4.

### Running totals

`cumsum()` gives a running total, handy for "sales so far this year":

```python
import numpy as np

monthly = np.array([10, 12, 9, 15, 14, 18])
print(monthly.cumsum())
```

### Reshaping

`reshape` rearranges the same numbers into a new shape. The total size must match; `-1` means "work this one out":

```python
import numpy as np

days = np.arange(1, 15)        # 14 days
weeks = days.reshape(2, 7)     # 2 weeks of 7 days
print(weeks)
print(weeks.sum(axis=1))       # total per week
print(days.reshape(-1, 2).shape)
```

### Loading numbers from a file

`np.loadtxt` reads a file of numbers straight into an array. Here are the five number columns of `students.csv` (columns 2 to 6), skipping the header:

```python
import numpy as np

data = np.loadtxt("students.csv", delimiter=",", skiprows=1, usecols=(2, 3, 4, 5, 6))
print(data.shape)
print(data[:3])
hours, math = data[:, 0], data[:, 2]
print("Average hours:", hours.mean().round(2))
print("Average math:", math.mean().round(1))
```

That works for files that are all numbers. Real files mix text and numbers, which is where pandas takes over next.

:::exercise Subject averages
`scores` has one row per student and the columns math, science, english. Make `subject_avg` (the average of each **column**) and `student_total` (the total of each **row**).
```python starter
import numpy as np

scores = np.array([[72, 85, 90],
                   [64, 70, 58],
                   [88, 91, 79],
                   [55, 62, 71],
                   [93, 80, 84]])

```
```python check
import numpy as np
s = np.array([[72, 85, 90], [64, 70, 58], [88, 91, 79], [55, 62, 71], [93, 80, 84]])
same(need("subject_avg", np.ndarray), s.mean(axis=0), "subject_avg")
same(need("student_total", np.ndarray), s.sum(axis=1), "student_total")
```
```python solution
import numpy as np

scores = np.array([[72, 85, 90],
                   [64, 70, 58],
                   [88, 91, 79],
                   [55, 62, 71],
                   [93, 80, 84]])
subject_avg = scores.mean(axis=0)
student_total = scores.sum(axis=1)
print(subject_avg, student_total)
```
hint: `axis=0` gives one answer per column; `axis=1` gives one answer per row.
:::

:::exercise Typical and extreme
For the response times below, store the **median** in `typical` and the **95th percentile** in `slow`.
```python starter
import numpy as np

times = np.array([0.4, 0.6, 0.5, 2.8, 0.7, 0.5, 0.9, 0.6, 5.2, 0.8,
                  0.6, 0.7, 1.1, 0.5, 0.6, 0.9, 0.7, 0.4, 3.9, 0.6])

```
```python check
import numpy as np
t = np.array([0.4, 0.6, 0.5, 2.8, 0.7, 0.5, 0.9, 0.6, 5.2, 0.8, 0.6, 0.7, 1.1, 0.5, 0.6, 0.9, 0.7, 0.4, 3.9, 0.6])
same(float(need("typical")), float(np.median(t)), "typical")
same(float(need("slow")), float(np.percentile(t, 95)), "slow")
```
```python solution
import numpy as np

times = np.array([0.4, 0.6, 0.5, 2.8, 0.7, 0.5, 0.9, 0.6, 5.2, 0.8,
                  0.6, 0.7, 1.1, 0.5, 0.6, 0.9, 0.7, 0.4, 3.9, 0.6])
typical = np.median(times)
slow = np.percentile(times, 95)
print(typical, slow)
```
hint: `np.median(times)` and `np.percentile(times, 95)`.
:::

:::quiz
? Why might you report the median salary instead of the mean?
- The median is always bigger
+ A few very high salaries pull the mean up but barely move the median
- The mean can't be calculated for salaries
= The median is the middle value, so extreme values don't drag it around.
? `scores` has shape `(30, 4)`: 30 students, 4 subjects. What shape is `scores.mean(axis=0)`?
+ `(4,)`, one average per subject
- `(30,)`, one average per student
- A single number
= `axis=0` collapses the rows, leaving one answer per column.
? What does `argmax()` return?
- The largest value
+ The position of the largest value
- The number of values
= `max()` gives the value; `argmax()` gives where it is.
:::

@@@ lesson
id: random-and-simulation
title: Random numbers and simulation
minutes: 15
summary: Generate random numbers with a seed, sample from distributions and lists, and answer questions by simulating them.
---
Random numbers are everywhere in data work: shuffling data before training a model, splitting it into training and test sets, creating test data, and **simulating** situations that are hard to calculate by hand.

### A random generator

NumPy's modern way is to create a **generator** first, then ask it for numbers:

```python
import numpy as np

rng = np.random.default_rng()
print(rng.integers(1, 7, size=10))    # 10 dice rolls (7 is not included)
print(rng.random(3))                  # 3 decimals between 0 and 1
```

Run it twice and you get different numbers each time.

### Seeds make results repeatable

Pass a **seed** (any whole number) and the generator produces the same "random" numbers every run. Always seed when someone else needs to reproduce your results, such as a model's training run or a lesson's examples:

```python
import numpy as np

rng = np.random.default_rng(42)
print(rng.integers(1, 7, size=5))

rng = np.random.default_rng(42)
print(rng.integers(1, 7, size=5))   # exactly the same
```

### Distributions

A **distribution** describes how likely each value is. Two you'll meet constantly:

- **uniform**: every value in a range is equally likely, like a fair dice;
- **normal** (the bell curve): most values sit near the average and fewer appear further away, like people's heights.

```python
import numpy as np

rng = np.random.default_rng(7)
heights = rng.normal(loc=170, scale=8, size=10_000)   # mean 170 cm, spread 8 cm
print(heights[:5].round(1))
print("mean", heights.mean().round(1), "std", heights.std().round(1))
print("share between 162 and 178:", ((heights > 162) & (heights < 178)).mean().round(3))
```

About 68% of normal values fall within one standard deviation of the mean. The simulation shows it without any formulas. `.mean()` of a true/false array gives the **share** that are true.

### Picking from a list

`rng.choice` picks items, with optional probabilities, and `rng.permutation` shuffles:

```python
import numpy as np

rng = np.random.default_rng(1)
regions = ["North", "South", "East", "West"]
print(rng.choice(regions, size=6))
print(rng.choice(regions, size=6, p=[0.4, 0.3, 0.2, 0.1]))
print(rng.choice(10, size=4, replace=False))   # 4 different numbers from 0-9
print(rng.permutation(regions))
```

### Simulation: let the computer try it

**Simulation** answers a probability question by acting it out many times and counting. What's the chance two dice add up to 7?

```python
import numpy as np

rng = np.random.default_rng(0)
n = 100_000
die1 = rng.integers(1, 7, size=n)
die2 = rng.integers(1, 7, size=n)
print("P(total is 7) is about", ((die1 + die2) == 7).mean().round(3))
print("Exact answer:", round(6 / 36, 3))
```

A business example: a shop gets between 20 and 40 customers a day, and each buys with a 30% chance. How many sales should it expect in a 30-day month, and how bad could it be?

```python
import numpy as np

rng = np.random.default_rng(3)
months = 10_000
customers = rng.integers(20, 41, size=(months, 30))   # 10,000 simulated months of 30 days
sales = rng.binomial(customers, 0.3)                  # each customer buys with chance 0.3
monthly = sales.sum(axis=1)
print("average month:", monthly.mean().round(1))
print("worst 5% of months: below", np.percentile(monthly, 5))
```

`rng.binomial(n, p)` counts successes out of `n` tries that each succeed with chance `p`.

### A train/test split

In machine learning you hide some data from the model to test it later. Shuffling positions does it:

```python
import numpy as np

rng = np.random.default_rng(10)
ids = np.arange(20)              # 20 rows of data
shuffled = rng.permutation(ids)
train, test = shuffled[:16], shuffled[16:]
print("train:", np.sort(train))
print("test: ", np.sort(test))
```

:::exercise Coin flips
Create a generator with seed `2026`, simulate **1,000** coin flips with `rng.integers(0, 2, size=1000)` (1 means heads), and store the share of heads in `heads_share`.
```python starter
import numpy as np

```
```python check
import numpy as np
rng = np.random.default_rng(2026)
exp = rng.integers(0, 2, size=1000).mean()
same(float(need("heads_share")), float(exp), "heads_share")
```
```python solution
import numpy as np

rng = np.random.default_rng(2026)
flips = rng.integers(0, 2, size=1000)
heads_share = flips.mean()
print(heads_share)
```
hint: The mean of an array of 0s and 1s is the share of 1s.
:::

:::exercise A fair split
Shuffle the 50 row numbers in `ids` with a generator seeded with `5`, then put the first 40 in `train` and the last 10 in `test`.
```python starter
import numpy as np

ids = np.arange(50)

```
```python check
import numpy as np
rng = np.random.default_rng(5)
s = rng.permutation(np.arange(50))
same(need("train", np.ndarray), s[:40], "train")
same(need("test", np.ndarray), s[40:], "test")
```
```python solution
import numpy as np

ids = np.arange(50)
rng = np.random.default_rng(5)
shuffled = rng.permutation(ids)
train = shuffled[:40]
test = shuffled[40:]
print(len(train), len(test))
```
hint: `rng = np.random.default_rng(5)`, then `shuffled = rng.permutation(ids)` and slice it.
:::

:::quiz
? Why give a random generator a seed?
- To make the numbers more random
+ So the same "random" numbers come out every run, and results can be reproduced
- To make it faster
= With a seed, anyone running your code gets the same results, which matters for experiments and models.
? What does `(rolls == 6).mean()` give for an array of dice rolls?
- The average roll
+ The share of rolls that were 6
- The number of 6s
= The comparison makes True/False values; their mean is the fraction that are True.
? Which describes the normal distribution?
- Every value equally likely
+ Most values near the average, fewer further away
- Only whole numbers
= The normal "bell curve" clusters around the mean, with fewer values in the tails.
:::
