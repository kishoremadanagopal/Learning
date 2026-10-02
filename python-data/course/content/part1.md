@@@ part
id: 1
title: Data with Plain Python
level: Beginner
blurb: See what data analysis is, then read CSV and JSON files and crunch numbers with the Python you already know, so you understand what pandas does for you later.

@@@ lesson
id: what-is-data-analysis
title: What data analysis is
minutes: 12
summary: The questions data answers, how tables of data are organised, and the three tools this course teaches.
---
**Data analysis** means answering questions with data. "Which product earns the most?", "Is it hotter this year?", "Do students who study more score higher?" are all data questions.

Every analysis, whether you're an analyst making a dashboard or an AI engineer preparing training data, follows the same steps:

| Step | What you do | Where you'll learn it |
|---|---|---|
| 1. Ask | turn a vague goal into a clear question | every lesson |
| 2. Load | read the data from a file, database or website | Parts 1 and 3 |
| 3. Clean | fix gaps, typos, wrong types and duplicates | Part 4 |
| 4. Analyse | filter, group, combine and summarise | Parts 3 and 5 |
| 5. Show | draw charts that make the answer obvious | Part 6 |
| 6. Share | save results and explain what they mean | Part 6 |

![The data analysis workflow in six steps: ask a question, load the data, clean it, analyse it, show it in charts, share the results](figures/workflow.svg)

### Data comes in tables

Most data you'll meet is **tabular**: a table where each **row** is one thing (one order, one customer, one day) and each **column** is one fact about it (the date, the price, the city). Here's the start of `sales.csv`, one of this course's practice files:

```output
order_id,order_date,customer_id,region,product,category,units,unit_price
1001,2025-01-01,C034,West,Headphones,Electronics,1,79.0
1002,2025-01-04,C086,North,Desk Lamp,Home,3,35.0
```

This format is called **CSV** (comma-separated values): one row per line, with commas between the columns. The first line, the **header**, names the columns. You can look at any practice file as plain text:

```python
text = open("products.csv").read()
print(text)
```

Open the **Data files** tab beside the editor to see all seven practice files. They reset before every run, so you can't break them.

### The tools: NumPy, pandas and matplotlib

Python on its own can do all of this, but it takes a lot of code. Three free **libraries** (packages of ready-made code) make it quick:

| Library | What it's for | How everyone imports it |
|---|---|---|
| **NumPy** | fast maths on whole lists of numbers at once | `import numpy as np` |
| **pandas** | tables: load, clean, filter, group and join data | `import pandas as pd` |
| **matplotlib** | charts | `import matplotlib.pyplot as plt` |

The short names `np`, `pd` and `plt` are a convention. You could pick any name, but every tutorial, job and AI assistant uses these, so you should too.

### Plain Python versus pandas

Here's a small set of orders as a list of dictionaries, and the total revenue worked out with a loop:

```python
orders = [
    {"product": "Pen", "units": 10, "price": 1.5},
    {"product": "Lamp", "units": 2, "price": 35.0},
    {"product": "Chair", "units": 1, "price": 189.0},
]

total = 0
for order in orders:
    total += order["units"] * order["price"]
print("Revenue:", total)
```

And here's the whole of `sales.csv` (600 orders) loaded and totalled with pandas. Don't worry about the details yet; just notice how short it is:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
revenue = (sales["units"] * sales["unit_price"]).sum()
print("Orders:", len(sales))
print("Revenue:", revenue)
```

In this part you'll do things the plain-Python way first, so that when pandas does them in one line, you'll know exactly what that line means.

### Working on your own computer

The sandbox runs real Python in your browser. At work, people use **Jupyter notebooks** (or VS Code), where code runs in small cells and tables and charts appear under each cell. Everything in this course works there too: see the course README for the two install commands.

:::exercise Revenue from a few orders
Using the `orders` list below, work out the total revenue (units × price for every order, added up) and store it in a variable called `total`. Use a loop.
```python starter
orders = [
    {"product": "Notebook", "units": 12, "price": 4.5},
    {"product": "Monitor", "units": 2, "price": 249.0},
    {"product": "Pen Pack", "units": 5, "price": 6.0},
    {"product": "Desk Lamp", "units": 1, "price": 35.0},
]

total = 0
# your loop here

print(total)
```
```python check
same(need("total"), 617.0, "total")
assert uses("for "), "Use a for loop over the orders."
```
```python solution
orders = [
    {"product": "Notebook", "units": 12, "price": 4.5},
    {"product": "Monitor", "units": 2, "price": 249.0},
    {"product": "Pen Pack", "units": 5, "price": 6.0},
    {"product": "Desk Lamp", "units": 1, "price": 35.0},
]

total = 0
for order in orders:
    total += order["units"] * order["price"]

print(total)
```
hint: Inside the loop, add `order["units"] * order["price"]` to `total` with `+=`.
:::

:::exercise Your first pandas line
Load `customers.csv` with pandas into a variable called `customers`, then print its first five rows with `customers.head()`.
```python starter
import pandas as pd

```
```python check
import pandas as pd
c = need("customers", pd.DataFrame)
assert len(c) == 120, "Load customers.csv (it has 120 rows)."
assert uses("head("), "Print the first rows with .head()."
assert printed("customer_id"), "Print customers.head() so you can see the table."
```
```python solution
import pandas as pd

customers = pd.read_csv("customers.csv")
print(customers.head())
```
hint: Copy the `pd.read_csv(...)` line from the example and change the file name.
:::

:::quiz
? In a table of sales, what is one **row**?
- One fact, like the price
+ One record, like a single order
- The list of column names
= Each row is one thing being described (here, one order). Columns are the facts about it.
? What does CSV stand for?
- Computer Spreadsheet Value
+ Comma-separated values
- Column sorted view
= A CSV file is plain text with one row per line and commas between the columns.
? Which import is the standard way to load pandas?
- `import pandas`
+ `import pandas as pd`
- `from pandas import *`
= Everyone uses the short name `pd`, so code you read and write looks the same everywhere.
:::

@@@ lesson
id: files-and-csv
title: Reading and writing files
minutes: 18
summary: Open text files, read CSV files properly with the csv module, and write your results back out.
---
Before pandas, it helps to see how Python reads files on its own. You'll use this for logs, text and odd formats that pandas can't handle.

### Opening and reading a file

`open(name)` opens a file. The safest way is a **`with` block**, which closes the file for you when the block ends, even if an error happens:

```python
with open("products.csv") as f:
    text = f.read()

print(type(text))
print(len(text), "characters")
print(text[:120])
```

`f.read()` gives you the whole file as one string. Often it's easier to go line by line: looping over a file gives one line at a time, including the newline character at the end. `.strip()` removes it.

```python
with open("products.csv") as f:
    for line in f:
        print(line.strip())
```

### Splitting lines into columns

Each line is text. To get the columns, split it on commas:

```python
with open("products.csv") as f:
    header = f.readline().strip().split(",")
    first = f.readline().strip().split(",")

print(header)
print(first)
print(first[2], "is text, not a number:", type(first[2]))
```

Two lessons here. First, everything read from a file is **text** (a string). `"899.0"` must be converted with `float()` before you can do maths. Second, splitting on commas breaks when a value itself contains a comma, like `"92,000"`. CSV files wrap such values in quotes, and a plain `split(",")` doesn't understand quotes.

### The csv module does it properly

Python's built-in `csv` module understands quotes. `csv.DictReader` is the most useful part: it reads the header for you and gives you each row as a **dictionary** keyed by column name.

```python
import csv

with open("products.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        margin = float(row["unit_price"]) - float(row["unit_cost"])
        print(f'{row["product"]:<13} margin {margin:7.2f}')
```

Here's the comma problem solved. The salary `"92,000"` stays in one piece:

```python
import csv

with open("employees_messy.csv") as f:
    rows = list(csv.DictReader(f))

print(len(rows), "rows")
print(rows[1])
```

`list(reader)` reads every row into a list in one go, so you can use them after the `with` block ends.

### Writing files

Open a file with `"w"` (write) to create it, or replace it if it already exists. `"a"` (append) adds to the end instead.

```python
with open("notes.txt", "w") as f:
    f.write("First line\n")
    f.write("Second line\n")

with open("notes.txt", "a") as f:
    f.write("Added later\n")

print(open("notes.txt").read())
```

`csv.DictWriter` writes dictionaries as CSV rows. Pass `newline=""` when opening, which stops blank lines appearing between rows on Windows:

```python
import csv

cheap = [{"product": "Notebook", "price": 4.5}, {"product": "Pen Pack", "price": 6.0}]

with open("cheap.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["product", "price"])
    writer.writeheader()
    writer.writerows(cheap)

print(open("cheap.csv").read())
```

### When the file isn't there

A wrong file name raises `FileNotFoundError`. Read the message: it tells you the name Python tried.

```python error
with open("sale.csv") as f:
    print(f.read())
```

:::exercise Count the North orders
Use `csv.DictReader` to read `sales.csv` and count how many orders have `region` equal to `"North"`. Store the count in `north_orders`.
```python starter
import csv

north_orders = 0

print(north_orders)
```
```python check
same(need("north_orders"), 198, "north_orders")
assert uses("DictReader"), "Read the file with csv.DictReader."
```
```python solution
import csv

north_orders = 0
with open("sales.csv") as f:
    for row in csv.DictReader(f):
        if row["region"] == "North":
            north_orders += 1

print(north_orders)
```
hint: Inside `with open("sales.csv") as f:`, loop `for row in csv.DictReader(f):` and add 1 when `row["region"] == "North"`.
:::

:::exercise Write a price list
Read `products.csv` and write a new file called `price_list.csv` with just two columns, `product` and `unit_price`, for every product that costs **less than 100**. Include the header row.
```python starter
import csv

```
```python check
import csv
with open("price_list.csv") as f:
    rows = list(csv.DictReader(f))
assert rows, "price_list.csv is empty. Did you call writeheader() and writerows()?"
assert list(rows[0].keys()) == ["product", "unit_price"], f"The columns should be product and unit_price, not {list(rows[0].keys())}."
got = [(r["product"], float(r["unit_price"])) for r in rows]
expected = [("Headphones", 79.0), ("Notebook", 4.5), ("Pen Pack", 6.0), ("Coffee Maker", 59.0), ("Desk Lamp", 35.0)]
assert got == expected, f"Expected these rows: {expected}\nGot: {got}"
```
```python solution
import csv

with open("products.csv") as f:
    products = list(csv.DictReader(f))

cheap = []
for p in products:
    if float(p["unit_price"]) < 100:
        cheap.append({"product": p["product"], "unit_price": p["unit_price"]})

with open("price_list.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["product", "unit_price"])
    writer.writeheader()
    writer.writerows(cheap)

print(open("price_list.csv").read())
```
hint: Remember the prices are text: compare `float(p["unit_price"]) < 100`. Build a list of small dictionaries, then write it with `csv.DictWriter`.
:::

:::quiz
? Why use `with open(...) as f:` instead of just `f = open(...)`?
- It reads the file faster
+ It closes the file automatically when the block ends
- It converts numbers for you
= A `with` block always closes the file, even if an error happens inside it.
? You read `"249.0"` from a CSV file. What type is it?
+ `str`
- `float`
- `int`
= Everything read from a text file is a string. Convert it with `float()` before doing maths.
? What does `csv.DictReader` give you for each row?
- A list of values
+ A dictionary keyed by the column names
- A single string
= It uses the header line as keys, so you can write `row["region"]` instead of remembering positions.
:::

@@@ lesson
id: json-data
title: JSON data
minutes: 16
summary: Read, explore and write JSON, the format most websites, APIs and AI tools use to exchange data.
---
**JSON** (JavaScript Object Notation) is the most common way programs send data to each other. Web APIs, configuration files, AI model responses and app exports all use it. If CSV is a flat table, JSON is a tree: values can contain other values.

```output
{
  "title": "Broken Station",
  "year": 2006,
  "genres": ["Comedy", "Drama"],
  "awards": null,
  "streaming": true
}
```

JSON maps almost exactly onto Python types:

| JSON | Python | Example |
|---|---|---|
| object `{ }` | `dict` | `{"year": 2006}` |
| array `[ ]` | `list` | `["Comedy", "Drama"]` |
| string | `str` | `"Broken Station"` (always double quotes) |
| number | `int` or `float` | `2006`, `7.6` |
| `true` / `false` | `True` / `False` | lowercase in JSON |
| `null` | `None` | means "no value" |

### Text to Python: json.loads

`json.loads` (load **s**tring) turns JSON text into Python objects:

```python
import json

text = '{"title": "Broken Station", "year": 2006, "genres": ["Comedy", "Drama"], "awards": null}'
movie = json.loads(text)

print(type(movie))
print(movie["title"], movie["year"])
print(movie["genres"][0])
print(movie["awards"])
```

### Python to text: json.dumps

`json.dumps` (dump **s**tring) goes the other way. `indent=2` makes it readable:

```python
import json

report = {"region": "North", "orders": 198, "top_products": ["Pen Pack", "Notebook"], "final": True}
print(json.dumps(report))
print(json.dumps(report, indent=2))
```

Notice how `True` became `true`. JSON text is what you'd send to an API or save to a file.

### Reading a JSON file

`json.load(f)` (no **s**) reads straight from an open file. `movies.json` holds a list of 40 film records:

```python
import json

with open("movies.json") as f:
    movies = json.load(f)

print(type(movies), len(movies))
print(movies[0])
for m in movies[:3]:
    print(m["title"], "-", m["genre"], "-", m["rating"])
```

### Nested data

Real JSON is often nested several levels deep. You reach inside one step at a time, chaining `[...]`:

![A CSV file is a flat table of rows and columns; a JSON file can put values inside values, like a customer inside an order and a list of items](figures/csv-vs-json.svg)

```python
import json

order = json.loads("""
{
  "order_id": 1042,
  "customer": {"name": "Priya Patel", "address": {"city": "Leeds", "postcode": "LS1 4AP"}},
  "items": [
    {"product": "Notebook", "units": 3, "price": 4.5},
    {"product": "Desk Lamp", "units": 1, "price": 35.0}
  ]
}
""")

print(order["customer"]["address"]["city"])
for item in order["items"]:
    print(item["product"], item["units"] * item["price"])
total = sum(item["units"] * item["price"] for item in order["items"])
print("Order total:", total)
```

When you meet unfamiliar JSON, print it with `json.dumps(data, indent=2)` and read the structure first.

### Missing keys

Records don't always have every key, and some values are `null`. `dict.get(key, default)` returns a default instead of crashing:

```python
import json

with open("movies.json") as f:
    movies = json.load(f)

no_box_office = [m["title"] for m in movies if m["box_office_musd"] is None]
print(len(no_box_office), "films have no box office figure:")
print(no_box_office)

print(movies[0].get("director", "unknown director"))
```

### Writing a JSON file

`json.dump(data, f)` writes to an open file:

```python
import json

summary = {"films": 40, "genres": ["Drama", "Comedy", "Action"]}
with open("summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(open("summary.json").read())
```

### Invalid JSON

JSON is strict. Single quotes, trailing commas and Python's `True`/`None` are not allowed, and `json.loads` raises an error that points at the problem:

```python error
import json

json.loads("{'title': 'Broken Station'}")
```

:::exercise The best-rated film
Load `movies.json` and find the film with the highest `rating`. Store its title in `best`.
```python starter
import json

best = ""

print(best)
```
```python check
import json
with open("movies.json") as f:
    ms = json.load(f)
expected = max(ms, key=lambda m: m["rating"])["title"]
same(need("best", str), expected, "best")
```
```python solution
import json

with open("movies.json") as f:
    movies = json.load(f)

top = movies[0]
for m in movies:
    if m["rating"] > top["rating"]:
        top = m
best = top["title"]

print(best)
```
hint: Keep track of the best record so far in a loop, or use `max(movies, key=lambda m: m["rating"])` and take its `"title"`.
:::

:::exercise Build a JSON report
Make a dictionary with three keys: `"course"` set to `"Python for Data"`, `"lessons_done"` set to `3`, and `"topics"` set to the list `["csv", "json"]`. Turn it into JSON text with `json.dumps` and store the text in `report_json`.
```python starter
import json

```
```python check
import json
text = need("report_json", str)
try:
    data = json.loads(text)
except ValueError:
    raise AssertionError("report_json isn't valid JSON. Create it with json.dumps(...).")
same(data, {"course": "Python for Data", "lessons_done": 3, "topics": ["csv", "json"]}, "The JSON in report_json")
```
```python solution
import json

report = {"course": "Python for Data", "lessons_done": 3, "topics": ["csv", "json"]}
report_json = json.dumps(report, indent=2)

print(report_json)
```
hint: Build the dictionary first, then `report_json = json.dumps(report)`.
:::

:::quiz
? What does the JSON value `null` become in Python?
- `0`
+ `None`
- `"null"`
= `null` means "no value", which Python writes as `None`.
? Which function turns JSON **text** into Python objects?
+ `json.loads`
- `json.dumps`
- `json.dump`
= `loads` = load from a string. `dumps` goes the other way, and `load`/`dump` work with files.
? Why does `json.loads("{'a': 1}")` fail?
- JSON can't hold numbers
+ JSON strings must use double quotes
- The dictionary is too short
= JSON only allows double quotes, so `'a'` is invalid. Python's single-quote style doesn't work in JSON.
:::

@@@ lesson
id: crunching-with-python
title: Crunching data with plain Python
minutes: 18
summary: Filter, count, group and rank records with comprehensions, Counter and sorted, the ideas pandas is built on.
---
You now have records in a list of dictionaries. This lesson covers the four things analysts do all day: **filter**, **count**, **group** and **rank**. You'll do them in plain Python here; pandas does each one in a single line later.

All the examples start from the sales file, read with `csv.DictReader` and with the number columns converted:

```python
import csv

with open("sales.csv") as f:
    sales = list(csv.DictReader(f))

for s in sales:
    s["units"] = int(s["units"])
    s["unit_price"] = float(s["unit_price"])

print(len(sales), "orders")
print(sales[0])
```

### Filter: keep the rows you want

A **list comprehension** with an `if` keeps only matching records:

```python
import csv

with open("sales.csv") as f:
    sales = list(csv.DictReader(f))

laptops = [s for s in sales if s["product"] == "Laptop"]
big = [s for s in sales if int(s["units"]) >= 10]
print(len(laptops), "laptop orders")
print(len(big), "orders of 10 or more units")
print([s["order_id"] for s in big[:5]])
```

### Totals with sum()

`sum()` accepts a **generator expression**, a comprehension without square brackets:

```python
import csv

with open("sales.csv") as f:
    sales = list(csv.DictReader(f))

units = sum(int(s["units"]) for s in sales)
revenue = sum(int(s["units"]) * float(s["unit_price"]) for s in sales)
print("Units sold:", units)
print(f"Revenue: {revenue:,.2f}")
print(f"Average order value: {revenue / len(sales):.2f}")
```

### Count: how many of each?

`collections.Counter` counts things for you. `most_common(n)` gives the top `n`:

```python
import csv
from collections import Counter

with open("sales.csv") as f:
    sales = list(csv.DictReader(f))

by_region = Counter(s["region"] for s in sales)
print(by_region)
print(by_region.most_common(2))
print(by_region["West"])
```

A Counter can also add up amounts instead of counting rows:

```python
import csv
from collections import Counter

with open("sales.csv") as f:
    sales = list(csv.DictReader(f))

units_by_product = Counter()
for s in sales:
    units_by_product[s["product"]] += int(s["units"])
print(units_by_product.most_common(3))
```

### Group: a total per category

Grouping means "split the rows by a column, then total each group". The pattern is a dictionary that starts each new key at zero:

```python
import csv

with open("sales.csv") as f:
    sales = list(csv.DictReader(f))

revenue = {}
for s in sales:
    key = s["category"]
    revenue[key] = revenue.get(key, 0) + int(s["units"]) * float(s["unit_price"])

for category, total in revenue.items():
    print(f"{category:<12} {total:>10,.2f}")
```

`revenue.get(key, 0)` returns 0 the first time a category appears. Keep this pattern in mind: it's exactly what pandas' `groupby` does.

### Rank: sort by a value

`sorted()` with `key=` sorts records (or dictionary items) by whatever you choose. `reverse=True` puts the biggest first:

```python
products = {"Laptop": 41, "Notebook": 101, "Pen Pack": 121, "Monitor": 59}

ranked = sorted(products.items(), key=lambda pair: pair[1], reverse=True)
print(ranked)
print("Top seller:", ranked[0][0])
print("Fewest orders:", min(products, key=products.get))
```

`lambda pair: pair[1]` is a tiny function that says "sort by the second item" (the count).

### Why pandas next

Each task above took 5 to 10 lines and careful type conversion. Here's a preview of the same group-and-rank in pandas:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
print(sales.groupby("category")["revenue"].sum().sort_values(ascending=False))
```

Next comes NumPy, the fast number engine underneath pandas, and then pandas itself.

:::exercise Revenue per region
Read `sales.csv` and build a dictionary called `revenue` that maps each region to its total revenue (units × unit_price, added up). Round nothing; just total.
```python starter
import csv

revenue = {}

print(revenue)
```
```python check
import pandas as pd
s = pd.read_csv("sales.csv")
exp = (s["units"] * s["unit_price"]).groupby(s["region"]).sum()
got = need("revenue", dict)
assert set(got) == set(exp.index), f"revenue should have one key per region: {sorted(exp.index)}"
for k in exp.index:
    same(got[k], float(exp[k]), f"revenue[{k!r}]")
```
```python solution
import csv

revenue = {}
with open("sales.csv") as f:
    for s in csv.DictReader(f):
        amount = int(s["units"]) * float(s["unit_price"])
        revenue[s["region"]] = revenue.get(s["region"], 0) + amount

print(revenue)
```
hint: Loop with `csv.DictReader`, and use `revenue[region] = revenue.get(region, 0) + amount`.
:::

:::exercise Top three products by units
Use `Counter` to add up the **units** sold for each product in `sales.csv`, then store the three best sellers in `top3` using `most_common(3)`. `top3` should be a list of `(product, units)` pairs.
```python starter
import csv
from collections import Counter

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv")
exp = s.groupby("product")["units"].sum().sort_values(ascending=False).head(3)
got = need("top3", list)
same([(p, int(u)) for p, u in got], [(p, int(u)) for p, u in exp.items()], "top3")
```
```python solution
import csv
from collections import Counter

units = Counter()
with open("sales.csv") as f:
    for s in csv.DictReader(f):
        units[s["product"]] += int(s["units"])

top3 = units.most_common(3)
print(top3)
```
hint: `units[s["product"]] += int(s["units"])` inside the loop, then `top3 = units.most_common(3)`.
:::

:::quiz
? What does `Counter(["a", "b", "a"])` give?
+ `Counter({'a': 2, 'b': 1})`
- `['a', 'b']`
- `3`
= A Counter counts how many times each value appears.
? In `revenue.get(key, 0)`, what is the `0` for?
- It sets every value to zero
+ It's returned when the key isn't in the dictionary yet
- It limits the dictionary to one key
= `.get` returns the default when the key is missing, so the first amount for a new key starts from 0.
? What does `sorted(items, key=lambda p: p[1], reverse=True)` do?
- Sorts by the first item, smallest first
+ Sorts by the second item, biggest first
- Removes duplicates
= `key=` chooses what to sort by (the second item), and `reverse=True` puts the largest first.
:::
