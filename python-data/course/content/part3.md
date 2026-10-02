@@@ part
id: 3
title: pandas Foundations
level: Beginner
blurb: Meet the Series and the DataFrame, load files into tables, pick out the rows and columns you need, filter, sort, add columns and summarise.

@@@ lesson
id: pandas-series
title: The Series
minutes: 15
summary: pandas' one-column building block: values with labels, vectorised maths, and quick counts.
---
pandas has two main objects. A **DataFrame** is a whole table. A **Series** is a single column: a list of values, each with a **label**. Every column you pull out of a table is a Series, so it's worth knowing well.

```python
import pandas as pd

units = pd.Series([12, 7, 3, 9])
print(units)
```

The left-hand numbers (0, 1, 2, 3) are the **index**: the label of each value. By default it counts from 0, like list positions. The last line says the **dtype**, the type of the values.

### Your own labels

You can label values with anything, which makes them easier to read and look up:

```python
import pandas as pd

units = pd.Series([12, 7, 3, 9], index=["Mon", "Tue", "Wed", "Thu"], name="units")
print(units)
print(units["Tue"])
```

A dictionary works too: its keys become the index.

```python
import pandas as pd

population = pd.Series({"London": 8.9, "Manchester": 0.55, "Leeds": 0.8})
print(population)
```

### Maths works like NumPy

A Series is built on a NumPy array, so vectorised maths, comparisons and masks all work the same way:

```python
import pandas as pd

prices = pd.Series([899.0, 249.0, 79.0, 4.5], index=["Laptop", "Monitor", "Headphones", "Notebook"])
print(prices * 1.2)
print(prices[prices > 100])
print(prices.mean(), prices.max())
print(prices.idxmax())     # the label of the biggest value
```

### Labels line up

When you combine two Series, pandas matches them **by label**, not by position. A label that's missing from one side gives `NaN` (missing):

```python
import pandas as pd

jan = pd.Series({"North": 120, "South": 95, "East": 80})
feb = pd.Series({"South": 110, "North": 130, "West": 60})
print(jan + feb)
```

North and South were added correctly even though they were in a different order. East and West only appear once, so their totals are missing. You'll fix those with `fill_value` or `fillna` later.

```python
import pandas as pd

jan = pd.Series({"North": 120, "South": 95, "East": 80})
feb = pd.Series({"South": 110, "North": 130, "West": 60})
print(jan.add(feb, fill_value=0))
```

### Counting values

`value_counts()` is one of the most-used methods in pandas. It counts how often each value appears, biggest first:

```python
import pandas as pd

answers = pd.Series(["yes", "no", "yes", "maybe", "yes", "no"])
print(answers.value_counts())
print(answers.value_counts(normalize=True).round(2))   # shares instead of counts
print(answers.unique(), answers.nunique())
```

### Useful Series methods

```python
import pandas as pd

temps = pd.Series([14.2, 17.8, 13.1, 21.5, 19.0])
print(temps.sort_values(ascending=False))
print(temps.round(0))
print(temps.describe())
```

`describe()` gives a quick summary: the count, mean, standard deviation, minimum, quartiles and maximum.

:::exercise Weekly steps
Make a Series called `steps` with the values `8200, 10450, 6300, 12100, 9800` and the labels `"Mon"` to `"Fri"`. Then store the label of the day with the most steps in `best_day`.
```python starter
import pandas as pd

```
```python check
import pandas as pd
s = need("steps", pd.Series)
same(s, pd.Series([8200, 10450, 6300, 12100, 9800], index=["Mon", "Tue", "Wed", "Thu", "Fri"]), "steps")
assert list(s.index) == ["Mon", "Tue", "Wed", "Thu", "Fri"], "Label the days Mon, Tue, Wed, Thu, Fri."
same(need("best_day"), "Thu", "best_day")
```
```python solution
import pandas as pd

steps = pd.Series([8200, 10450, 6300, 12100, 9800], index=["Mon", "Tue", "Wed", "Thu", "Fri"])
best_day = steps.idxmax()
print(steps)
print(best_day)
```
hint: Pass `index=["Mon", ...]` when you create the Series, then use `.idxmax()`.
:::

:::exercise Favourite colours
Count how many times each colour appears in `colours` and store the result in `counts`. Then store the share (between 0 and 1) of answers that were `"blue"` in `blue_share`.
```python starter
import pandas as pd

colours = pd.Series(["blue", "green", "blue", "red", "blue", "green", "blue", "red"])

```
```python check
import pandas as pd
c = need("counts", pd.Series)
same(int(c["blue"]), 4, "counts['blue']")
same(int(c["green"]), 2, "counts['green']")
same(float(need("blue_share")), 0.5, "blue_share")
```
```python solution
import pandas as pd

colours = pd.Series(["blue", "green", "blue", "red", "blue", "green", "blue", "red"])
counts = colours.value_counts()
blue_share = colours.value_counts(normalize=True)["blue"]
print(counts)
print(blue_share)
```
hint: `colours.value_counts()` counts; `value_counts(normalize=True)` gives shares.
:::

:::quiz
? What is the index of a Series?
- The number of values
+ The labels attached to the values
- The type of the values
= The index labels each value. By default it's 0, 1, 2…, but it can be any labels you like.
? You add two Series. How does pandas pair the values up?
- By position
+ By matching labels
- Randomly
= pandas aligns on the index labels. Labels missing from one side give NaN.
? Which method counts how often each value appears?
+ `value_counts()`
- `count()`
- `describe()`
= `value_counts()` returns each distinct value with its count, most common first. `count()` just counts non-missing values.
:::

@@@ lesson
id: dataframes
title: DataFrames and loading data
minutes: 18
summary: Create tables, load CSV and JSON files, and take a first look at any dataset with head, shape, info and describe.
---
A **DataFrame** is a table: rows and named columns, where each column is a Series. It's the object you'll use in almost every line of pandas.

![A DataFrame has column names along the top, an index down the left side, and each column on its own is a Series](figures/dataframe-anatomy.svg)

### Making a DataFrame

From a dictionary of lists (each key becomes a column):

```python
import pandas as pd

df = pd.DataFrame({
    "product": ["Laptop", "Notebook", "Desk Lamp"],
    "price": [899.0, 4.5, 35.0],
    "in_stock": [True, True, False],
})
print(df)
```

From a list of dictionaries (each dictionary becomes a row), which is exactly what you get from JSON or `csv.DictReader`:

```python
import pandas as pd

rows = [{"city": "Leeds", "temp": 14.2}, {"city": "Mumbai", "temp": 31.0}]
print(pd.DataFrame(rows))
```

### Loading files

In practice you'll load data far more than you'll type it. One line reads a whole CSV, with the number columns already converted:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
print(sales.head())
```

`head()` shows the first 5 rows (`head(10)` for 10); `tail()` shows the last ones. When a table is wider than the screen, pandas hides the middle columns behind `...`.

JSON files of records load the same way:

```python
import pandas as pd

movies = pd.read_json("movies.json")
print(movies.head(3))
```

### Your first look at any dataset

These five checks are the first thing every analyst does with new data:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
print(sales.shape)           # (rows, columns)
print(list(sales.columns))   # the column names
print(sales.dtypes)          # the type of each column
```

`info()` puts the size, columns, types and missing counts on one screen:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales.info()
```

The "Non-Null Count" tells you how many values are present in each column. If it's less than the number of rows, some values are missing.

### The dtypes you'll see

| dtype | What it holds |
|---|---|
| `int64` | whole numbers |
| `float64` | decimals (and any number column with missing values) |
| `str` | text |
| `bool` | True / False |
| `datetime64` | dates and times (Part 4) |

### describe(): numbers at a glance

`describe()` summarises every number column. It's the fastest way to spot strange values, like a negative price or an age of 230:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
print(sales.describe().round(2))
```

Add `include="all"` to describe the text columns too: their number of distinct values and the most common one.

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
print(customers.describe(include="all"))
```

### The index

Every DataFrame has an index labelling its rows, just like a Series. `read_csv` gives the default 0, 1, 2… You'll set your own in the next lesson.

```python
import pandas as pd

products = pd.read_csv("products.csv")
print(products.index)
print(products.columns)
```

:::exercise Load the weather
Load `weather.csv` into a DataFrame called `weather`, store the number of rows in `n_rows`, and print the first 3 rows.
```python starter
import pandas as pd

```
```python check
import pandas as pd
w = need("weather", pd.DataFrame)
assert w.shape == (1095, 4), "Load weather.csv with pd.read_csv."
same(need("n_rows"), 1095, "n_rows")
assert uses("head("), "Print the first rows with .head(3)."
```
```python solution
import pandas as pd

weather = pd.read_csv("weather.csv")
n_rows = len(weather)        # or weather.shape[0]
print(weather.head(3))
```
hint: `len(weather)` or `weather.shape[0]` gives the number of rows.
:::

:::exercise Build a table
Create a DataFrame called `team` with two columns: `name` holding `"Ada"`, `"Grace"` and `"Alan"`, and `score` holding `91`, `88` and `79`.
```python starter
import pandas as pd

```
```python check
import pandas as pd
same(need("team", pd.DataFrame), pd.DataFrame({"name": ["Ada", "Grace", "Alan"], "score": [91, 88, 79]}), "team")
```
```python solution
import pandas as pd

team = pd.DataFrame({
    "name": ["Ada", "Grace", "Alan"],
    "score": [91, 88, 79],
})
print(team)
```
hint: Pass a dictionary: `{"name": [...], "score": [...]}`.
:::

:::quiz
? What is a DataFrame's single column, taken on its own?
+ A Series
- A list
- A NumPy array
= Every column of a DataFrame is a Series, sharing the table's index.
? `df.shape` is `(1095, 4)`. What does that mean?
- 1095 columns and 4 rows
+ 1095 rows and 4 columns
- 1095 missing values
= Shape is always (rows, columns).
? Which command shows column types and how many values are missing in each?
- `df.head()`
+ `df.info()`
- `df.shape`
= `info()` lists each column with its non-null count and dtype.
:::

@@@ lesson
id: selecting-data
title: Selecting columns and rows
minutes: 18
summary: Pick columns by name, and rows and cells by label with loc or by position with iloc.
---
Analysis starts with getting the slice of data you need. pandas has three main tools: square brackets for columns, `.loc` for labels and `.iloc` for positions.

### Columns

One column name in brackets gives a **Series**. A **list** of names (note the double brackets) gives a smaller **DataFrame**:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
print(sales["product"].head(3))
print(sales[["order_date", "product", "units"]].head(3))
```

```python error
import pandas as pd

sales = pd.read_csv("sales.csv")
print(sales["Product"])      # capital P: no such column
```

Column names are case-sensitive. When you get a `KeyError`, print `df.columns` and compare.

You may also see `sales.product` (dot style). It works for simple names, but brackets always work, so prefer them.

### loc: rows by label

`df.loc[row, column]` selects by **label**. With the default index the labels are 0, 1, 2…, so it looks like positions, but it's the labels that count:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
print(sales.loc[0])                       # one row, as a Series
print(sales.loc[0, "product"])            # one cell
print(sales.loc[0:3, ["product", "units"]])
```

Unlike Python slices, a **`loc` slice includes the end label**: `0:3` gives rows 0, 1, 2 and 3.

### Setting a meaningful index

Rows are easier to find when the index is a real identifier. `set_index` makes a column the index:

```python
import pandas as pd

products = pd.read_csv("products.csv").set_index("product")
print(products)
print(products.loc["Monitor", "unit_price"])
print(products.loc[["Laptop", "Notebook"], ["unit_price", "unit_cost"]])
```

`reset_index()` turns the index back into an ordinary column.

### iloc: rows by position

`df.iloc[row, column]` uses **positions** (whole numbers from 0), and its slices exclude the end, like Python lists:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
print(sales.iloc[0, 4])        # row 0, column 4
print(sales.iloc[-1])          # the last row
print(sales.iloc[:3, :4])      # first 3 rows, first 4 columns
```

| You want | Use |
|---|---|
| one or more columns by name | `df["col"]` or `df[["a", "b"]]` |
| rows and columns by label | `df.loc[rows, cols]` |
| rows and columns by position | `df.iloc[rows, cols]` |

### Changing a value

Use `loc` to change a cell. This is the safe way: it finds the row and column in one step.

```python
import pandas as pd

products = pd.read_csv("products.csv").set_index("product")
products.loc["Notebook", "unit_price"] = 4.99
print(products.loc["Notebook"])
```

Don't chain two sets of brackets to change data, like `products["unit_price"]["Notebook"] = 4.99`. In pandas 3 that never changes the table, because the first brackets give you a copy.

:::exercise Pick the columns
Load `customers.csv` and make `contact` a DataFrame with just the `name` and `city` columns (in that order).
```python starter
import pandas as pd

customers = pd.read_csv("customers.csv")

```
```python check
import pandas as pd
c = pd.read_csv("customers.csv")
same(need("contact", pd.DataFrame), c[["name", "city"]], "contact")
```
```python solution
import pandas as pd

customers = pd.read_csv("customers.csv")
contact = customers[["name", "city"]]
print(contact.head())
```
hint: A list of column names inside the brackets: `customers[["name", "city"]]`.
:::

:::exercise Look up a product
Load `products.csv` with `product` as the index. Store the `supplier` of `"Desk Chair"` in `supplier` and the `unit_cost` of `"Laptop"` in `laptop_cost`, using `.loc`.
```python starter
import pandas as pd

```
```python check
same(need("supplier"), "OfficeHub", "supplier")
same(float(need("laptop_cost")), 640.0, "laptop_cost")
assert uses(".loc["), "Use .loc[row, column]."
```
```python solution
import pandas as pd

products = pd.read_csv("products.csv").set_index("product")
supplier = products.loc["Desk Chair", "supplier"]
laptop_cost = products.loc["Laptop", "unit_cost"]
print(supplier, laptop_cost)
```
hint: `pd.read_csv("products.csv").set_index("product")`, then `products.loc["Desk Chair", "supplier"]`.
:::

:::quiz
? What does `df[["a", "b"]]` return?
- A Series
+ A DataFrame with columns a and b
- An error
= A list of names (double brackets) gives a DataFrame. A single name gives a Series.
? With the default index, how many rows does `df.loc[0:3]` return?
- 3
+ 4
- 2
= `loc` slices include the end label, so it returns rows 0, 1, 2 and 3. `iloc[0:3]` would return 3.
? Which selects by position, whatever the labels are?
- `loc`
+ `iloc`
- `set_index`
= The "i" in `iloc` stands for integer position.
:::

@@@ lesson
id: filtering-rows
title: Filtering rows
minutes: 18
summary: Keep the rows that match conditions with boolean masks, isin, between and query.
---
"Show me only the orders from the North" or "students who scored over 80" are **filters**. In pandas a filter is a boolean mask, exactly as in NumPy, but applied to whole rows.

### One condition

A comparison on a column gives a Series of True/False. Put it inside `df[...]` to keep the matching rows:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
is_laptop = sales["product"] == "Laptop"
print(is_laptop.head())
laptops = sales[is_laptop]
print(len(laptops), "laptop orders")
print(laptops.head(3))
```

Usually it's written in one go:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
big = sales[sales["units"] >= 10]
print(big[["order_id", "product", "units"]])
```

### Several conditions

Combine masks with `&` (and), `|` (or) and `~` (not), with **each condition in brackets**:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
north_electronics = sales[(sales["region"] == "North") & (sales["category"] == "Electronics")]
print(len(north_electronics))

cheap_or_bulk = sales[(sales["unit_price"] < 10) | (sales["units"] >= 8)]
print(len(cheap_or_bulk))

not_office = sales[~(sales["category"] == "Office")]
print(not_office["category"].unique())
```

### isin: one of several values

`isin` is shorter than a chain of `|`:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
desk_items = sales[sales["product"].isin(["Desk Chair", "Desk Lamp"])]
print(desk_items["product"].value_counts())
```

### between: a range

`between(low, high)` includes both ends:

```python
import pandas as pd

students = pd.read_csv("students.csv")
middle = students[students["math"].between(60, 75)]
print(middle[["student", "math"]].head())
```

### Filtering text and dates

Text columns have string methods under `.str`, which you'll see properly in Part 4. Dates stored as `YYYY-MM-DD` text even compare correctly, because that format sorts in date order:

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
print(customers[customers["name"].str.startswith("A")]["name"].head())

sales = pd.read_csv("sales.csv")
march = sales[(sales["order_date"] >= "2025-03-01") & (sales["order_date"] < "2025-04-01")]
print(len(march), "orders in March")
```

### query: filters as text

`query` lets you write the condition as a readable string. Column names go in plainly, and `@` brings in a Python variable:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
limit = 200
print(sales.query("region == 'West' and unit_price > @limit").head())
```

Both styles are common. Masks are more flexible; `query` is easier to read.

### Filter, then pick columns

Use `loc` to filter rows and choose columns in one step:

```python
import pandas as pd

students = pd.read_csv("students.csv")
print(students.loc[students["attendance_pct"] < 75, ["student", "attendance_pct", "math"]])
```

:::exercise Top students
Load `students.csv` and make `stars`, holding only the students who scored **85 or more in math AND 85 or more in science**.
```python starter
import pandas as pd

students = pd.read_csv("students.csv")

```
```python check
import pandas as pd
s = pd.read_csv("students.csv")
same(need("stars", pd.DataFrame), s[(s["math"] >= 85) & (s["science"] >= 85)], "stars")
```
```python solution
import pandas as pd

students = pd.read_csv("students.csv")
stars = students[(students["math"] >= 85) & (students["science"] >= 85)]
print(stars)
```
hint: Two conditions joined with `&`, each in its own brackets.
:::

:::exercise Big-city customers
Load `customers.csv` and make `big_city`, holding the customers whose `city` is `"London"` or `"Manchester"` and whose `segment` is `"Business"`. Use `isin`.
```python starter
import pandas as pd

customers = pd.read_csv("customers.csv")

```
```python check
import pandas as pd
c = pd.read_csv("customers.csv")
same(need("big_city", pd.DataFrame), c[c["city"].isin(["London", "Manchester"]) & (c["segment"] == "Business")], "big_city")
assert uses(".isin("), "Use .isin([...]) for the cities."
```
```python solution
import pandas as pd

customers = pd.read_csv("customers.csv")
big_city = customers[customers["city"].isin(["London", "Manchester"]) & (customers["segment"] == "Business")]
print(big_city)
```
hint: `customers["city"].isin(["London", "Manchester"]) & (customers["segment"] == "Business")`.
:::

:::quiz
? Why does `df[df["a"] > 1 & df["b"] < 5]` go wrong?
- `&` doesn't work in pandas
+ Without brackets, `&` is applied before the comparisons
- You can't filter on two columns
= `&` binds tighter than `>` and `<`, so wrap each condition: `(df["a"] > 1) & (df["b"] < 5)`.
? What does `sales["product"].isin(["Pen Pack", "Notebook"])` produce?
+ True for rows whose product is either of those, False otherwise
- A list of the two products
- The number of matching rows
= `isin` gives a mask you can use to filter.
? In `query`, what does the `@` in `"price > @limit"` mean?
- A column called limit
+ Use the Python variable `limit`
- A comment
= `@` refers to a variable from your code rather than a column.
:::

@@@ lesson
id: sorting-and-new-columns
title: Sorting and adding columns
minutes: 18
summary: Sort by one or more columns, get the top rows, create calculated columns, and rename or drop columns.
---
Most analyses add a few calculated columns (like revenue) and then sort to see the biggest or smallest. This lesson covers both.

### Sorting

`sort_values` sorts by a column. It returns a **new** DataFrame; the original stays as it was.

```python
import pandas as pd

products = pd.read_csv("products.csv")
print(products.sort_values("unit_price")[["product", "unit_price"]])
print(products.sort_values("unit_price", ascending=False).head(3)[["product", "unit_price"]])
```

Sort by several columns by passing lists. Here: category A to Z, then price high to low within each category:

```python
import pandas as pd

products = pd.read_csv("products.csv")
print(products.sort_values(["category", "unit_price"], ascending=[True, False]))
```

`nlargest` and `nsmallest` are shortcuts for "sort and take the top":

```python
import pandas as pd

students = pd.read_csv("students.csv")
print(students.nlargest(3, "math")[["student", "math"]])
```

### New columns from calculations

Assigning to a new column name creates it. The calculation runs on every row at once:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
sales["big_order"] = sales["revenue"] > 500
print(sales[["product", "units", "unit_price", "revenue", "big_order"]].head())
```

A column can be a fixed value, or built from text:

```python
import pandas as pd

products = pd.read_csv("products.csv")
products["currency"] = "GBP"
products["margin"] = products["unit_price"] - products["unit_cost"]
products["margin_pct"] = (products["margin"] / products["unit_price"] * 100).round(1)
products["label"] = products["product"] + " (" + products["category"] + ")"
print(products[["label", "margin", "margin_pct", "currency"]])
```

### np.where for if/else columns

You met `np.where` in Part 2. It's the usual way to make a column from a condition:

```python
import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")
students["result"] = np.where(students["math"] >= 50, "pass", "fail")
print(students["result"].value_counts())
```

### assign: several columns in a chain

`assign` returns a new DataFrame with added columns, which suits step-by-step chains. `lambda d:` refers to the DataFrame at that point in the chain:

```python
import pandas as pd

top = (
    pd.read_csv("sales.csv")
    .assign(revenue=lambda d: d["units"] * d["unit_price"])
    .sort_values("revenue", ascending=False)
    .head(5)
)
print(top[["order_id", "product", "revenue"]])
```

Wrapping a chain in brackets lets you put one step per line, which reads like a recipe.

### Renaming and dropping

```python
import pandas as pd

products = pd.read_csv("products.csv")
products = products.rename(columns={"unit_price": "price", "unit_cost": "cost"})
products = products.drop(columns=["supplier"])
print(products.head(3))
```

Notice the `products = ...`. Like `sort_values`, these methods return a new table; if you don't save the result, nothing changes.

:::exercise Margins
Load `products.csv`, add a column `margin` (unit_price minus unit_cost), then make `by_margin`: the table sorted by `margin` from **highest to lowest**.
```python starter
import pandas as pd

products = pd.read_csv("products.csv")

```
```python check
import pandas as pd
p = pd.read_csv("products.csv")
p["margin"] = p["unit_price"] - p["unit_cost"]
same(need("by_margin", pd.DataFrame), p.sort_values("margin", ascending=False), "by_margin", ignore_index=True)
```
```python solution
import pandas as pd

products = pd.read_csv("products.csv")
products["margin"] = products["unit_price"] - products["unit_cost"]
by_margin = products.sort_values("margin", ascending=False)
print(by_margin)
```
hint: Create the column first, then `sort_values("margin", ascending=False)`.
:::

:::exercise Biggest orders
Load `sales.csv`, add a `revenue` column (units × unit_price), and store the **5 rows with the highest revenue** in `top5`.
```python starter
import pandas as pd

sales = pd.read_csv("sales.csv")

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv")
s["revenue"] = s["units"] * s["unit_price"]
exp = s.nlargest(5, "revenue")
got = need("top5", pd.DataFrame)
assert "revenue" in got.columns, "top5 should include the revenue column."
same(sorted(got["revenue"].tolist(), reverse=True), exp["revenue"].tolist(), "the revenue values in top5")
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
top5 = sales.nlargest(5, "revenue")
print(top5)
```
hint: `sales.nlargest(5, "revenue")`, or sort descending and take `.head(5)`.
:::

:::quiz
? After `df.sort_values("price")`, is `df` sorted?
- Yes
+ No, the sorted table is returned and must be saved
- Only if the column is numeric
= Most pandas methods return a new object. Write `df = df.sort_values("price")` to keep it.
? How do you sort by category A–Z, then price high to low?
+ `df.sort_values(["category", "price"], ascending=[True, False])`
- `df.sort_values("category").sort_values("price")`
- `df.sort_values("category", "price", False)`
= Pass lists of columns and directions, in priority order.
? What does `df["total"] = df["a"] * df["b"]` do?
- Multiplies only the first row
+ Creates a total column, row by row
- Raises an error because total doesn't exist
= Assigning to a new name creates the column, calculated for every row at once.
:::

@@@ lesson
id: summarising-data
title: Summarising a whole table
minutes: 16
summary: Totals, averages and counts for columns, the most common values, distinct values and the row with the biggest value.
---
Before grouping and charts, you need the basic question answers: how many, how much in total, what's typical, what's most common. pandas gives each in one method.

### Column summaries

The NumPy summaries all exist on Series, and they skip missing values automatically:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
print("orders:     ", len(sales))
print("units sold: ", sales["units"].sum())
print("revenue:    ", sales["revenue"].sum())
print("avg order:  ", sales["revenue"].mean().round(2))
print("median:     ", sales["revenue"].median())
print("largest:    ", sales["revenue"].max())
```

### Several summaries at once

`agg` takes a list of summary names:

```python
import pandas as pd

students = pd.read_csv("students.csv")
print(students["math"].agg(["mean", "median", "min", "max", "std"]).round(1))
print(students[["math", "science", "english"]].agg(["mean", "max"]).round(1))
```

Called on a DataFrame, `mean()` and friends give one answer per column:

```python
import pandas as pd

students = pd.read_csv("students.csv")
print(students[["math", "science", "english"]].mean().round(1))
```

### Counting

`count()` counts the values that are present (not missing), `value_counts()` counts each distinct value, and `nunique()` counts how many distinct values there are:

```python
import pandas as pd

movies = pd.read_json("movies.json")
print(movies["box_office_musd"].count(), "films have a box office figure, out of", len(movies))
print(movies["genre"].nunique(), "genres")
print(movies["genre"].value_counts())
```

### Shares and percentages

`value_counts(normalize=True)` gives shares; multiply by 100 for percentages:

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
print((customers["segment"].value_counts(normalize=True) * 100).round(1))
```

The mean of a True/False column is the share of True values, a trick from NumPy that works here too:

```python
import pandas as pd

students = pd.read_csv("students.csv")
print("share passing math:", (students["math"] >= 50).mean().round(2))
print("students under 80% attendance:", (students["attendance_pct"] < 80).sum())
```

### Which row has the biggest value?

`idxmax()` gives the **index label** of the largest value; pass it to `loc` to see the whole row:

```python
import pandas as pd

movies = pd.read_json("movies.json")
best = movies["rating"].idxmax()
print(best)
print(movies.loc[best])
```

### Answering a question

Putting it together. Question: *"What does a typical Electronics order look like?"*

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
elec = sales[sales["category"] == "Electronics"]

print(f"{len(elec)} Electronics orders ({len(elec) / len(sales):.0%} of all orders)")
print(f"Median order value: {elec['revenue'].median():,.2f}")
print(f"Most common product: {elec['product'].value_counts().idxmax()}")
print(f"Share of revenue: {elec['revenue'].sum() / sales['revenue'].sum():.0%}")
```

The format code `:.0%` turns 0.31 into `31%`, and `:,.2f` adds thousands commas and 2 decimals.

:::exercise Movie numbers
Load `movies.json`. Store the average `rating` in `avg_rating`, the number of distinct genres in `n_genres`, and the **title** of the longest film (highest `runtime_min`) in `longest`.
```python starter
import pandas as pd

movies = pd.read_json("movies.json")

```
```python check
import pandas as pd
m = pd.read_json("movies.json")
same(float(need("avg_rating")), float(m["rating"].mean()), "avg_rating")
same(int(need("n_genres")), int(m["genre"].nunique()), "n_genres")
same(need("longest"), m.loc[m["runtime_min"].idxmax(), "title"], "longest")
```
```python solution
import pandas as pd

movies = pd.read_json("movies.json")
avg_rating = movies["rating"].mean()
n_genres = movies["genre"].nunique()
longest = movies.loc[movies["runtime_min"].idxmax(), "title"]
print(avg_rating, n_genres, longest)
```
hint: `idxmax()` gives the row label; use it with `.loc[label, "title"]`.
:::

:::exercise Segment shares
Load `customers.csv` and make `shares`: the **percentage** of customers in each `segment` (so they add up to 100).
```python starter
import pandas as pd

customers = pd.read_csv("customers.csv")

```
```python check
import pandas as pd
c = pd.read_csv("customers.csv")
exp = c["segment"].value_counts(normalize=True) * 100
got = need("shares", pd.Series)
for k in exp.index:
    same(float(got[k]), float(exp[k]), f"shares[{k!r}]", tol=1e-3)
```
```python solution
import pandas as pd

customers = pd.read_csv("customers.csv")
shares = customers["segment"].value_counts(normalize=True) * 100
print(shares.round(1))
```
hint: `value_counts(normalize=True)` gives shares between 0 and 1; multiply by 100.
:::

:::quiz
? What does `df["col"].count()` count?
- The distinct values
+ The values that aren't missing
- Every row, including missing ones
= `count()` skips missing values. Use `len(df)` for the number of rows.
? What does `(df["score"] >= 50).mean()` give?
+ The share of rows with a score of 50 or more
- The average score
- The number of passing rows
= True counts as 1 and False as 0, so the mean is the fraction of True.
? What does `idxmax()` return?
- The largest value
+ The index label of the row with the largest value
- The row number, always counting from 0
= It returns the label, which you can pass to `loc` to fetch the whole row.
:::
