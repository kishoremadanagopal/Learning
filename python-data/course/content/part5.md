@@@ part
id: 5
title: Analysing Data
level: Intermediate
blurb: Answer real questions: group and aggregate, build pivot tables, join tables like SQL, reshape between wide and long, bin and map values, and analyse trends over time.

@@@ lesson
id: groupby
title: Grouping and aggregating
minutes: 20
summary: Split a table into groups, summarise each one, and combine the results, with groupby and named aggregations.
---
"Revenue **per region**", "average score **per class**", "orders **per month**": whenever a question says *per* or *by*, the answer is a **groupby**. You did it by hand with a dictionary in Part 1. pandas does it in one line.

### Split, apply, combine

`groupby` works in three steps:

![Split the rows into one group per region, apply sum to each group, then combine the answers into one small table](figures/split-apply-combine.svg)

1. **split** the rows into groups by a column's values;
2. **apply** a summary (sum, mean, count…) to each group;
3. **combine** the answers into one result.

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
print(sales.groupby("region")["revenue"].sum())
```

Read it as: "group sales by region, take the revenue column, sum it". The result is a Series indexed by region. Sort it to rank the groups:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
print(sales.groupby("product")["revenue"].sum().sort_values(ascending=False))
```

### Different summaries

Any summary works: `sum`, `mean`, `median`, `min`, `max`, `count`, `nunique`. And `size()` counts the rows in each group:

```python
import pandas as pd

students = pd.read_csv("students.csv")
print(students.groupby("class")["math"].mean().round(1))
print(students.groupby("class").size())
print(students.groupby("class")[["math", "science", "english"]].mean().round(1))
```

### Several summaries: named aggregation

`agg` with **named aggregation** gives you one tidy table with your own column names. Each new column is `name=("column", "summary")`:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
summary = sales.groupby("region").agg(
    orders=("order_id", "count"),
    units=("units", "sum"),
    revenue=("revenue", "sum"),
    avg_order=("revenue", "mean"),
    customers=("customer_id", "nunique"),
).round(1)
print(summary.sort_values("revenue", ascending=False))
```

That one table answers five questions about every region. This is the most useful pattern in the whole course.

### Grouping by two columns

Pass a list to group by combinations. The result has a two-level index:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
by_two = sales.groupby(["region", "category"])["revenue"].sum().round(0)
print(by_two)
```

`reset_index()` turns the group labels back into normal columns, which is easier to filter, merge and save:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
flat = sales.groupby(["region", "category"])["revenue"].sum().reset_index()
print(flat.head(6))
print(flat[flat["category"] == "Home"])
```

### transform: a group value on every row

`transform` returns a result **the same length as the table**, so you can compare each row with its group. Here, each order's share of its region's revenue:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
sales["region_total"] = sales.groupby("region")["revenue"].transform("sum")
sales["share_of_region"] = (sales["revenue"] / sales["region_total"] * 100).round(2)
print(sales[["region", "product", "revenue", "region_total", "share_of_region"]].head())
```

Another use: students who beat their own class average.

```python
import pandas as pd

students = pd.read_csv("students.csv")
class_avg = students.groupby("class")["math"].transform("mean")
above = students[students["math"] > class_avg]
print(len(above), "students beat their class average in math")
```

### Groups by a calculated value

You can group by any Series of the right length, not just a column, such as a date part:

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
print(sales.groupby(sales["order_date"].dt.quarter)["revenue"].sum())
```

:::exercise Units per category
Load `sales.csv` and store the **total units** sold in each `category` in `units_by_cat`, sorted from largest to smallest.
```python starter
import pandas as pd

sales = pd.read_csv("sales.csv")

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv")
same(need("units_by_cat", pd.Series), s.groupby("category")["units"].sum().sort_values(ascending=False), "units_by_cat")
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv")
units_by_cat = sales.groupby("category")["units"].sum().sort_values(ascending=False)
print(units_by_cat)
```
hint: `sales.groupby("category")["units"].sum()`, then `.sort_values(ascending=False)`.
:::

:::exercise City report
Load `customers.csv` and build `city_report`, indexed by `city`, with three named columns: `customers` (how many customers, counting `customer_id`), `avg_age` (mean `age`) and `oldest` (max `age`).
```python starter
import pandas as pd

customers = pd.read_csv("customers.csv")

```
```python check
import pandas as pd
c = pd.read_csv("customers.csv")
exp = c.groupby("city").agg(customers=("customer_id", "count"), avg_age=("age", "mean"), oldest=("age", "max"))
same(need("city_report", pd.DataFrame), exp, "city_report")
```
```python solution
import pandas as pd

customers = pd.read_csv("customers.csv")
city_report = customers.groupby("city").agg(
    customers=("customer_id", "count"),
    avg_age=("age", "mean"),
    oldest=("age", "max"),
)
print(city_report)
```
hint: `.agg(customers=("customer_id", "count"), avg_age=("age", "mean"), oldest=("age", "max"))`.
:::

:::quiz
? Which question needs a groupby?
- How many rows does the table have?
+ What's the average order value per region?
- What's the largest order?
= "Per region" means split by region and summarise each group.
? What's the difference between `.agg(...)` and `.transform(...)` after a groupby?
+ `agg` gives one row per group; `transform` gives one value per original row
- They're the same
- `transform` only works on text
= `transform` broadcasts each group's result back to its rows, so you can compare rows with their group.
? What does `reset_index()` do after a groupby?
- Deletes the groups
+ Turns the group labels into ordinary columns
- Sorts the result
= The groups move from the index into columns, giving a flat table.
:::

@@@ lesson
id: pivot-tables
title: Pivot tables and crosstabs
minutes: 16
summary: Build spreadsheet-style summary tables with one variable down the side and another across the top.
---
If you've used Excel, you've probably met **pivot tables**: a summary with one category down the rows, another across the columns, and a number in each cell. They're perfect for reports, because people can read across and down.

### pivot_table

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
table = sales.pivot_table(index="region", columns="category", values="revenue", aggfunc="sum")
print(table.round(0))
```

| Argument | Meaning |
|---|---|
| `index` | what goes down the side (one row per value) |
| `columns` | what goes across the top |
| `values` | the number to summarise |
| `aggfunc` | how to summarise it: `"sum"`, `"mean"`, `"count"`… |

It's the same as `groupby(["region", "category"])["revenue"].sum()`, laid out as a grid.

### Totals and gaps

`margins=True` adds an "All" row and column with totals. `fill_value=0` puts 0 where a combination never happened:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
table = sales.pivot_table(index="product", columns="region", values="units",
                          aggfunc="sum", fill_value=0, margins=True)
print(table)
```

### Months across the top

Dates make great pivot columns. Here's units per category per quarter:

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
sales["quarter"] = "Q" + sales["order_date"].dt.quarter.astype(str)
print(sales.pivot_table(index="category", columns="quarter", values="units", aggfunc="sum"))
```

### Averages in a pivot

Any summary works. Average exam scores by class, for each subject:

```python
import pandas as pd

students = pd.read_csv("students.csv")
print(students.pivot_table(index="class", values=["math", "science", "english"], aggfunc="mean").round(1))
```

Without `columns`, you get one column per value. This is identical to a groupby with `mean`.

### crosstab: counting combinations

`pd.crosstab` counts how often each combination of two columns occurs. It's the quickest way to see how two categories relate:

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
print(pd.crosstab(customers["city"], customers["segment"]))
```

`normalize="index"` turns each row into shares, so rows of different sizes can be compared:

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
shares = pd.crosstab(customers["city"], customers["segment"], normalize="index")
print((shares * 100).round(0))
```

Now you can see which cities lean towards business customers, whatever their size.

### Reading values out

A pivot table is an ordinary DataFrame, so `loc` works:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
table = sales.pivot_table(index="region", columns="category", values="units", aggfunc="sum")
print(table.loc["North", "Office"])
print(table["Home"].idxmax(), "buys the most Home units")
```

:::exercise Revenue grid
Load `sales.csv`, add `revenue`, and make `grid`: a pivot table with `product` down the side, `region` across the top, and the **sum of revenue** in the cells. Fill gaps with 0.
```python starter
import pandas as pd

sales = pd.read_csv("sales.csv")

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv")
s["revenue"] = s["units"] * s["unit_price"]
exp = s.pivot_table(index="product", columns="region", values="revenue", aggfunc="sum", fill_value=0)
got = need("grid", pd.DataFrame)
same(got.reindex(columns=exp.columns), exp, "grid")
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
grid = sales.pivot_table(index="product", columns="region", values="revenue", aggfunc="sum", fill_value=0)
print(grid.round(0))
```
hint: `pivot_table(index="product", columns="region", values="revenue", aggfunc="sum", fill_value=0)`.
:::

:::exercise Genre by decade
Load `movies.json`, add a column `decade` holding `"2000s"`, `"2010s"` or `"2020s"` (hint: `(year // 10 * 10).astype(str) + "s"`), and store `pd.crosstab(movies["genre"], movies["decade"])` in `counts`.
```python starter
import pandas as pd

movies = pd.read_json("movies.json")

```
```python check
import pandas as pd
m = pd.read_json("movies.json")
m["decade"] = (m["year"] // 10 * 10).astype(str) + "s"
same(need("counts", pd.DataFrame), pd.crosstab(m["genre"], m["decade"]), "counts")
```
```python solution
import pandas as pd

movies = pd.read_json("movies.json")
movies["decade"] = (movies["year"] // 10 * 10).astype(str) + "s"
counts = pd.crosstab(movies["genre"], movies["decade"])
print(counts)
```
hint: `year // 10 * 10` rounds 2017 down to 2010. Convert to text and add `"s"`.
:::

:::quiz
? In `pivot_table(index="region", columns="category", ...)`, what are the rows?
+ One row per region
- One row per category
- One row per order
= `index` goes down the side; `columns` goes across the top.
? What does `margins=True` add?
- Spaces between columns
+ Total rows and columns labelled "All"
- Percentages
= Margins are the totals along each side, like a spreadsheet's grand total.
? What does `pd.crosstab(a, b)` count?
- The values of a
+ How often each combination of a and b occurs
- The missing values
= A crosstab is a table of combination counts. `normalize=` turns them into shares.
:::

@@@ lesson
id: merging-tables
title: Combining tables with merge
minutes: 20
summary: Join tables on a shared key, the pandas version of SQL joins, and check for rows that didn't match.
---
Real data is spread over several tables. Orders don't repeat the customer's city; they store a `customer_id` that points to the customers table. To ask "revenue per city", you need to **join** the tables on that key. If you've done the SQL course, this is `JOIN`.

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
customers = pd.read_csv("customers.csv")
print(sales[["order_id", "customer_id", "product"]].head(3))
print(customers[["customer_id", "name", "city"]].head(3))
```

### merge

`merge` matches rows where the key columns are equal:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
customers = pd.read_csv("customers.csv")
joined = sales.merge(customers, on="customer_id")
print(joined.shape)
print(joined[["order_id", "customer_id", "name", "city", "product"]].head())
```

Every order now carries its customer's details. Now "revenue per city" is a groupby:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
customers = pd.read_csv("customers.csv")
joined = sales.merge(customers, on="customer_id")
joined["revenue"] = joined["units"] * joined["unit_price"]
print(joined.groupby("city")["revenue"].sum().sort_values(ascending=False).round(0))
```

### Types of join

When some keys don't match, the `how` argument decides what happens:

![Inner, left, right and outer joins as overlapping circles: the shaded part shows which rows each join keeps](figures/merge-joins.svg)

| `how=` | Keeps | SQL |
|---|---|---|
| `"inner"` (default) | only rows with a match in both tables | `INNER JOIN` |
| `"left"` | every row of the left table; gaps where no match | `LEFT JOIN` |
| `"right"` | every row of the right table | `RIGHT JOIN` |
| `"outer"` | every row of both | `FULL OUTER JOIN` |

A small example makes the difference clear:

```python
import pandas as pd

orders = pd.DataFrame({"order": [1, 2, 3, 4], "cust": ["A", "B", "B", "Z"]})
people = pd.DataFrame({"cust": ["A", "B", "C"], "name": ["Ada", "Ben", "Cy"]})

print(orders.merge(people, on="cust", how="inner"))
print(orders.merge(people, on="cust", how="left"))
print(orders.merge(people, on="cust", how="outer"))
```

Order 4 (customer Z, not in `people`) disappears in the inner join and has a missing name in the left join. Customer C (no orders) only appears in the outer join.

### Finding what didn't match

`indicator=True` adds a `_merge` column saying where each row came from. It's the best way to check a join:

```python
import pandas as pd

orders = pd.DataFrame({"order": [1, 2, 3, 4], "cust": ["A", "B", "B", "Z"]})
people = pd.DataFrame({"cust": ["A", "B", "C"], "name": ["Ada", "Ben", "Cy"]})
check = orders.merge(people, on="cust", how="outer", indicator=True)
print(check)
print(check["_merge"].value_counts())
```

`left_only` rows are orders with an unknown customer, a data-quality problem worth reporting.

### Key names that differ

If the key has different names in the two tables, use `left_on` and `right_on`. When both tables have other columns with the same name, pandas adds `_x` and `_y`; `suffixes` makes them clearer:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
products = pd.read_csv("products.csv").rename(columns={"product": "item"})
both = sales.merge(products, left_on="product", right_on="item", suffixes=("_sold", "_list"))
print(both[["product", "unit_price_sold", "unit_price_list", "unit_cost"]].head(3))
```

### Joining three tables

Chain merges to bring everything together. Here profit needs the cost from `products` and the segment from `customers`:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
customers = pd.read_csv("customers.csv")
products = pd.read_csv("products.csv")[["product", "unit_cost"]]

full = (sales
        .merge(customers[["customer_id", "segment"]], on="customer_id", how="left")
        .merge(products, on="product", how="left"))
full["profit"] = full["units"] * (full["unit_price"] - full["unit_cost"])
print(full.groupby("segment")["profit"].sum().round(0))
```

Selecting only the columns you need before merging keeps the result small and readable.

### Watch the row count

If a key repeats in **both** tables, every match is paired up and rows multiply. Compare the length before and after, or let pandas check with `validate`:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
customers = pd.read_csv("customers.csv")
joined = sales.merge(customers, on="customer_id", how="left", validate="many_to_one")
print(len(sales), len(joined))
```

`validate="many_to_one"` means "many orders per customer, but each customer only once", and raises an error if that's not true.

:::exercise Orders with names
Merge `sales.csv` with `customers.csv` on `customer_id` (a **left** join, so no order is lost) and store the result in `orders`. Then store the number of distinct **cities** that have placed orders in `n_cities`.
```python starter
import pandas as pd

sales = pd.read_csv("sales.csv")
customers = pd.read_csv("customers.csv")

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv"); c = pd.read_csv("customers.csv")
j = s.merge(c, on="customer_id", how="left")
got = need("orders", pd.DataFrame)
assert len(got) == len(j), f"orders should have {len(j)} rows (one per order), but has {len(got)}."
assert "city" in got.columns, "orders should include the customers' columns, like city."
same(int(need("n_cities")), int(j["city"].nunique()), "n_cities")
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv")
customers = pd.read_csv("customers.csv")
orders = sales.merge(customers, on="customer_id", how="left")
n_cities = orders["city"].nunique()
print(n_cities)
```
hint: `sales.merge(customers, on="customer_id", how="left")`.
:::

:::exercise Profit by product
Merge `sales.csv` with the `product` and `unit_cost` columns of `products.csv`, add `profit` = units × (unit_price − unit_cost), and store the **total profit per product**, largest first, in `profit_by_product`.
```python starter
import pandas as pd

sales = pd.read_csv("sales.csv")
products = pd.read_csv("products.csv")

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv"); p = pd.read_csv("products.csv")[["product", "unit_cost"]]
f = s.merge(p, on="product")
f["profit"] = f["units"] * (f["unit_price"] - f["unit_cost"])
same(need("profit_by_product", pd.Series), f.groupby("product")["profit"].sum().sort_values(ascending=False), "profit_by_product")
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv")
products = pd.read_csv("products.csv")
full = sales.merge(products[["product", "unit_cost"]], on="product")
full["profit"] = full["units"] * (full["unit_price"] - full["unit_cost"])
profit_by_product = full.groupby("product")["profit"].sum().sort_values(ascending=False)
print(profit_by_product)
```
hint: Merge on `"product"`, calculate `profit`, then groupby product and sum.
:::

:::quiz
? An order's customer_id isn't in the customers table. What happens in an inner join?
+ The order is dropped
- It's kept with missing customer details
- An error is raised
= An inner join only keeps rows that match in both tables. Use `how="left"` to keep every order.
? What does `indicator=True` add?
- A row count
+ A `_merge` column showing whether each row matched
- An index
= `_merge` is `both`, `left_only` or `right_only`, which makes unmatched rows easy to find.
? After a merge you have far more rows than before. What's the likely cause?
- The merge was a left join
+ The key repeats in both tables, so matches multiply
- Missing values
= Each left row pairs with every matching right row. Check keys are unique where they should be, or use `validate=`.
:::

@@@ lesson
id: reshaping-data
title: Stacking and reshaping tables
minutes: 16
summary: Stack tables with concat, and switch between wide and long layouts with melt and pivot.
---
Data doesn't always arrive in the shape you need. Sometimes it's split into several files with the same columns; sometimes the layout is "wide" when your tools want "long". Here are the tools to rearrange it.

### concat: stacking tables

`pd.concat` puts tables with the same columns on top of each other, like appending this month's file to last month's:

```python
import pandas as pd

jan = pd.DataFrame({"product": ["Pen", "Lamp"], "units": [10, 2]})
feb = pd.DataFrame({"product": ["Pen", "Chair"], "units": [7, 1]})
both = pd.concat([jan, feb], ignore_index=True)
print(both)
```

`ignore_index=True` renumbers the rows 0, 1, 2…; without it you'd get the labels 0, 1, 0, 1. To remember which file each row came from, add a column first:

```python
import pandas as pd

jan = pd.DataFrame({"product": ["Pen", "Lamp"], "units": [10, 2]}).assign(month="Jan")
feb = pd.DataFrame({"product": ["Pen", "Chair"], "units": [7, 1]}).assign(month="Feb")
print(pd.concat([jan, feb], ignore_index=True))
```

A common real use: splitting a big file by a column, then stacking the parts back:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
parts = [sales[sales["region"] == r] for r in ["North", "South"]]
north_south = pd.concat(parts)
print(len(parts[0]), len(parts[1]), len(north_south))
```

### Wide and long

The same data can be laid out two ways:

![The same scores in two layouts: wide has one column per subject; long has one row per student and subject. melt goes wide to long, pivot goes back](figures/wide-long.svg)

- **wide**: one row per thing, one column per measurement (easy for people to read);
- **long** (also called **tidy**): one row per thing *per measurement*, with a column saying which measurement it is (easy for computers to group, filter and chart).

```python
import pandas as pd

wide = pd.DataFrame({
    "student": ["Ana", "Ben"],
    "math": [72, 64],
    "science": [85, 70],
})
print(wide)
```

### melt: wide to long

`melt` turns columns into rows. `id_vars` stay as they are; the other columns are "melted" into two: which column it was, and its value:

```python
import pandas as pd

wide = pd.DataFrame({"student": ["Ana", "Ben"], "math": [72, 64], "science": [85, 70]})
long = wide.melt(id_vars="student", var_name="subject", value_name="score")
print(long)
```

Now "average score per subject" is a simple groupby, and it works however many subjects there are:

```python
import pandas as pd

students = pd.read_csv("students.csv")
long = students.melt(id_vars=["student", "class"], value_vars=["math", "science", "english"],
                     var_name="subject", value_name="score")
print(long.head())
print(long.groupby(["class", "subject"])["score"].mean().round(1).unstack())
```

`unstack()` moves the inner index level (subject) into the columns, turning the result wide again for reading.

### pivot: long to wide

`pivot` is the opposite of `melt`. Daily weather is long (one row per city per day); pivot it to put the cities side by side:

```python
import pandas as pd

weather = pd.read_csv("weather.csv")
by_city = weather.pivot(index="date", columns="city", values="temp_c")
print(by_city.head())
print(by_city.corr().round(2))
```

With the cities as columns, comparing them is easy, like this table of **correlations** (how closely the temperatures rise and fall together; you'll learn it properly in the statistics course).

`pivot` needs each index/column pair to appear only once. If there are repeats, use `pivot_table`, which summarises them.

:::exercise Stack the quarters
`q1` and `q2` are two quarters of results with the same columns. Stack them into one table called `half_year` with a fresh index (0 to 5), after adding a `quarter` column holding `"Q1"` or `"Q2"` to each.
```python starter
import pandas as pd

q1 = pd.DataFrame({"region": ["North", "South", "East"], "revenue": [120, 95, 80]})
q2 = pd.DataFrame({"region": ["North", "South", "East"], "revenue": [130, 110, 85]})

```
```python check
import pandas as pd
q1 = pd.DataFrame({"region": ["North", "South", "East"], "revenue": [120, 95, 80]})
q2 = pd.DataFrame({"region": ["North", "South", "East"], "revenue": [130, 110, 85]})
exp = pd.concat([q1.assign(quarter="Q1"), q2.assign(quarter="Q2")], ignore_index=True)
got = need("half_year", pd.DataFrame)
same(got[["region", "revenue", "quarter"]], exp, "half_year")
assert list(got.index) == list(range(6)), "Use ignore_index=True so the index runs 0 to 5."
```
```python solution
import pandas as pd

q1 = pd.DataFrame({"region": ["North", "South", "East"], "revenue": [120, 95, 80]})
q2 = pd.DataFrame({"region": ["North", "South", "East"], "revenue": [130, 110, 85]})
q1["quarter"] = "Q1"
q2["quarter"] = "Q2"
half_year = pd.concat([q1, q2], ignore_index=True)
print(half_year)
```
hint: Add the column to each table, then `pd.concat([q1, q2], ignore_index=True)`.
:::

:::exercise Melt the scores
Melt `students.csv` into a long table called `long` with the columns `student`, `subject` and `score` (subjects: math, science, english). Then store the **highest score in each subject** in `best`.
```python starter
import pandas as pd

students = pd.read_csv("students.csv")

```
```python check
import pandas as pd
s = pd.read_csv("students.csv")
l = s.melt(id_vars="student", value_vars=["math", "science", "english"], var_name="subject", value_name="score")
got = need("long", pd.DataFrame)
assert {"student", "subject", "score"} <= set(got.columns), "long needs the columns student, subject and score."
assert len(got) == 180, f"long should have 180 rows (60 students x 3 subjects), but has {len(got)}."
same(need("best", pd.Series).sort_index(), l.groupby("subject")["score"].max().sort_index(), "best")
```
```python solution
import pandas as pd

students = pd.read_csv("students.csv")
long = students.melt(id_vars="student", value_vars=["math", "science", "english"],
                     var_name="subject", value_name="score")
best = long.groupby("subject")["score"].max()
print(best)
```
hint: `melt(id_vars="student", value_vars=[...], var_name="subject", value_name="score")`, then groupby subject.
:::

:::quiz
? What does `pd.concat([a, b])` do?
+ Stacks b underneath a
- Joins a and b on a key
- Adds the numbers in a and b
= concat stacks tables. To match rows on a key, use `merge`.
? Which layout has one row per student per subject?
- Wide
+ Long
- Pivot
= Long (tidy) data has one row per measurement, with a column naming which measurement it is.
? Which method turns wide data into long data?
+ `melt`
- `pivot`
- `concat`
= `melt` turns columns into rows; `pivot` does the reverse.
:::

@@@ lesson
id: map-apply-and-bins
title: Mapping, applying and binning
minutes: 16
summary: Translate values with map, run your own functions with apply, and sort numbers into bands with cut and qcut.
---
Sometimes the transformation you need isn't built in: a code that needs translating, a custom rule, or numbers that should become bands like "low / medium / high". This lesson covers the three tools for that.

### map: translate values

`map` with a dictionary swaps each value for its partner. Values not in the dictionary become missing, which helps you spot codes you forgot:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
managers = {"North": "Asha", "South": "Ben", "East": "Chen", "West": "Dana"}
sales["manager"] = sales["region"].map(managers)
print(sales[["region", "manager"]].drop_duplicates())
```

### apply with your own function

`apply` runs a function on every value of a Series. Write the rule as a normal `def`, then apply it:

```python
import pandas as pd

def size_label(units):
    if units >= 10:
        return "bulk"
    elif units >= 4:
        return "medium"
    return "single"

sales = pd.read_csv("sales.csv")
sales["order_size"] = sales["units"].apply(size_label)
print(sales["order_size"].value_counts())
```

A `lambda` works for short rules:

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
customers["initials"] = customers["name"].apply(lambda n: "".join(word[0] for word in n.split()))
print(customers[["name", "initials"]].head(3))
```

### apply on rows

With `axis=1`, `apply` gives your function a whole **row**, so the rule can use several columns:

```python
import pandas as pd

def shipping(row):
    if row["category"] == "Electronics" and row["units"] >= 2:
        return 0.0
    return 4.99

sales = pd.read_csv("sales.csv")
sales["shipping"] = sales.apply(shipping, axis=1)
print(sales.groupby("shipping").size())
```

Row-by-row `apply` is a hidden loop, so it's slow on big tables. Prefer vectorised tools when you can. The same rule with `np.where`:

```python
import numpy as np
import pandas as pd

sales = pd.read_csv("sales.csv")
free = (sales["category"] == "Electronics") & (sales["units"] >= 2)
sales["shipping"] = np.where(free, 0.0, 4.99)
print(sales.groupby("shipping").size())
```

### np.select: several conditions

For more than two outcomes, `np.select` takes a list of conditions and a matching list of results; the first true condition wins:

```python
import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")
conditions = [students["math"] >= 80, students["math"] >= 60, students["math"] >= 40]
grades = ["A", "B", "C"]
students["grade"] = np.select(conditions, grades, default="Fail")
print(students["grade"].value_counts().sort_index())
```

### cut: numbers into bands

`pd.cut` sorts numbers into **bins** (bands) you define. Each bin includes its right edge, so with the edges below a score of 60 is a "C":

![pd.cut splits 0 to 100 into bands at the edges 40, 60 and 80, labelled D, C, B and A; a score of exactly 60 falls in C because the right edge is included](figures/cut-bins.svg)

```python
import pandas as pd

students = pd.read_csv("students.csv")
students["band"] = pd.cut(students["math"], bins=[0, 40, 60, 80, 100], labels=["D", "C", "B", "A"])
print(students[["student", "math", "band"]].head())
print(students["band"].value_counts().sort_index())
```

Age groups are a classic use:

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
customers["age_group"] = pd.cut(customers["age"], bins=[17, 29, 44, 59, 100],
                                labels=["18-29", "30-44", "45-59", "60+"])
print(customers.groupby("age_group", observed=True)["customer_id"].count())
```

`observed=True` tells groupby to show only the bands that actually occur.

### qcut: equal-sized groups

`pd.qcut` makes bins with (roughly) the same number of rows in each, using quantiles. It's how you'd split customers into "top 25%, next 25%…":

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
sales["value_band"] = pd.qcut(sales["revenue"], q=4, labels=["low", "mid-low", "mid-high", "high"])
print(sales["value_band"].value_counts())
print(sales.groupby("value_band", observed=True)["revenue"].agg(["min", "max"]))
```

:::exercise Supplier lookup
Add a `supplier` column to `sales` by mapping each product to its supplier with the dictionary built from `products.csv` (`dict(zip(products["product"], products["supplier"]))`). Then store the number of orders per supplier in `orders_per_supplier`.
```python starter
import pandas as pd

sales = pd.read_csv("sales.csv")
products = pd.read_csv("products.csv")

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv"); p = pd.read_csv("products.csv")
sup = s["product"].map(dict(zip(p["product"], p["supplier"])))
got = need("sales", pd.DataFrame)
same(got["supplier"], sup, "sales['supplier']")
o = need("orders_per_supplier", pd.Series)
exp = sup.value_counts()
for k in exp.index:
    same(int(o[k]), int(exp[k]), f"orders_per_supplier[{k!r}]")
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv")
products = pd.read_csv("products.csv")
lookup = dict(zip(products["product"], products["supplier"]))
sales["supplier"] = sales["product"].map(lookup)
orders_per_supplier = sales["supplier"].value_counts()
print(orders_per_supplier)
```
hint: Build the dictionary, then `sales["product"].map(lookup)`. Count with `value_counts()`.
:::

:::exercise Attendance bands
Load `students.csv` and add `attendance_band` using `pd.cut` with the edges `[0, 75, 90, 100]` and the labels `"low"`, `"ok"`, `"great"`. Then store the **average math score per band** in `math_by_band` (use `observed=True`).
```python starter
import pandas as pd

students = pd.read_csv("students.csv")

```
```python check
import pandas as pd
s = pd.read_csv("students.csv")
b = pd.cut(s["attendance_pct"], bins=[0, 75, 90, 100], labels=["low", "ok", "great"])
got = need("students", pd.DataFrame)
same(list(got["attendance_band"].astype(str)), list(b.astype(str)), "students['attendance_band']")
exp = s.groupby(b, observed=True)["math"].mean()
m = need("math_by_band", pd.Series)
for k in exp.index:
    same(float(m[k]), float(exp[k]), f"math_by_band[{k!r}]")
```
```python solution
import pandas as pd

students = pd.read_csv("students.csv")
students["attendance_band"] = pd.cut(students["attendance_pct"], bins=[0, 75, 90, 100],
                                     labels=["low", "ok", "great"])
math_by_band = students.groupby("attendance_band", observed=True)["math"].mean()
print(math_by_band.round(1))
```
hint: `pd.cut(students["attendance_pct"], bins=[0, 75, 90, 100], labels=[...])`.
:::

:::quiz
? What does `s.map({"N": "North"})` do to a value `"S"`?
- Leaves it as "S"
+ Makes it missing, since "S" isn't in the dictionary
- Raises an error
= Unmapped values become NaN, which helps you spot codes you didn't cover.
? Why prefer `np.where` over `df.apply(func, axis=1)` when possible?
+ It's vectorised, so much faster on big tables
- `apply` gives wrong answers
- `np.where` works on text only
= Row-wise `apply` is a Python loop in disguise. Vectorised tools do the work in fast compiled code.
? How do `cut` and `qcut` differ?
- They're the same
+ `cut` uses edges you choose; `qcut` makes groups of roughly equal size
- `qcut` only works on dates
= `cut` bins by value ranges; `qcut` bins by quantiles so each bin has a similar count.
:::

@@@ lesson
id: time-series
title: Trends over time
minutes: 20
summary: Use a date index to resample to weeks and months, smooth with rolling averages, and compare periods with shift and pct_change.
---
"Are sales growing?", "Which month was hottest?", "How does this week compare with last week?" are **time series** questions: the same measurement tracked over time. pandas has special tools for them, and they work best when the dates are the index.

### A date index

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
daily = sales.groupby("order_date")["revenue"].sum()
print(daily.head())
print(daily.index.dtype)
```

With dates as the index, you can select by date text, even partial dates:

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
daily = sales.groupby("order_date")["revenue"].sum()
print(daily.loc["2025-03"].sum())                  # all of March
print(daily.loc["2025-06-01":"2025-06-07"])        # one week
```

### resample: change the frequency

`resample` groups by time periods, like a groupby for dates. Pass a period code:

| Code | Period |
|---|---|
| `"D"` | day |
| `"W"` | week (ending Sunday) |
| `"ME"` | month (labelled by its last day) |
| `"QE"` | quarter |
| `"YE"` | year |

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
monthly = sales.set_index("order_date")["revenue"].resample("ME").sum()
print(monthly.round(0))
print("Best month:", monthly.idxmax().strftime("%B"))
```

`set_index("order_date")` makes the dates the index so `resample` can use them. Days with no orders still get a row (with 0), unlike a plain groupby.

### Growth: shift and pct_change

`shift(1)` moves values down one step, lining each period up with the one before. `pct_change()` does the growth calculation for you:

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
monthly = sales.set_index("order_date")["revenue"].resample("ME").sum()

report = pd.DataFrame({"revenue": monthly})
report["previous"] = report["revenue"].shift(1)
report["change_pct"] = (report["revenue"].pct_change() * 100).round(1)
report.index = report.index.strftime("%b")
print(report.round(0).head(6))
```

The first month has no previous month, so its change is missing.

### Rolling averages

Daily numbers are noisy. A **rolling average** (moving average) replaces each day with the average of the last few days, smoothing out the noise so the trend shows:

![London's noisy daily temperatures with a smoother 7-day rolling average and an even smoother 30-day average drawn through them](figures/rolling-average.svg)

```python
import pandas as pd

weather = pd.read_csv("weather.csv", parse_dates=["date"])
london = weather[weather["city"] == "London"].set_index("date")["temp_c"]
smooth = london.rolling(7).mean()
print(pd.DataFrame({"daily": london, "7-day avg": smooth.round(1)}).iloc[5:12])
```

The first six days have no 7-day average yet. `rolling(7, min_periods=1)` would use whatever days are available.

### Cumulative totals

`cumsum` gives a running total, like "revenue year to date":

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
monthly = sales.set_index("order_date")["revenue"].resample("ME").sum()
ytd = monthly.cumsum()
print(ytd.round(0).tail(3))
print(f"Half the year's revenue was reached by {ytd[ytd >= ytd.iloc[-1] / 2].index[0]:%B}")
```

### Several series at once

Group first, then resample, to get a time series per group. Monthly average temperature for each city:

```python
import pandas as pd

weather = pd.read_csv("weather.csv", parse_dates=["date"])
monthly = (weather.set_index("date")
           .groupby("city")["temp_c"]
           .resample("ME").mean()
           .unstack(level=0)
           .round(1))
monthly.index = monthly.index.strftime("%b")
print(monthly)
```

London and New York peak in July and swing widely through the year, while Mumbai stays between about 25 and 30 °C all year. Its big seasonal change is rain: the June to September monsoon (you'll find it in the exercise).

:::exercise Weekly units
Load `sales.csv` with dates parsed, make the dates the index, and store the **total units per week** (resample `"W"`) in `weekly`. Then store the date of the busiest week in `busiest`.
```python starter
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv", parse_dates=["order_date"])
w = s.set_index("order_date")["units"].resample("W").sum()
same(need("weekly", pd.Series), w, "weekly")
assert pd.Timestamp(need("busiest")) == w.idxmax(), f"busiest should be {w.idxmax().date()}."
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
weekly = sales.set_index("order_date")["units"].resample("W").sum()
busiest = weekly.idxmax()
print(busiest)
```
hint: `sales.set_index("order_date")["units"].resample("W").sum()`, then `idxmax()`.
:::

:::exercise Monsoon month
Load `weather.csv` with dates parsed, keep only **Mumbai**, and store the **total rain per month** (resample `"ME"`, sum of `rain_mm`) in `mumbai_rain`. Store the name of the wettest month (like `"July"`) in `wettest`.
```python starter
import pandas as pd

weather = pd.read_csv("weather.csv", parse_dates=["date"])

```
```python check
import pandas as pd
w = pd.read_csv("weather.csv", parse_dates=["date"])
r = w[w["city"] == "Mumbai"].set_index("date")["rain_mm"].resample("ME").sum()
same(need("mumbai_rain", pd.Series), r, "mumbai_rain")
same(need("wettest"), r.idxmax().strftime("%B"), "wettest")
```
```python solution
import pandas as pd

weather = pd.read_csv("weather.csv", parse_dates=["date"])
mumbai = weather[weather["city"] == "Mumbai"].set_index("date")
mumbai_rain = mumbai["rain_mm"].resample("ME").sum()
wettest = mumbai_rain.idxmax().strftime("%B")
print(mumbai_rain.round(0))
print(wettest)
```
hint: Filter, `set_index("date")`, `["rain_mm"].resample("ME").sum()`. Format the best date with `.strftime("%B")`.
:::

:::quiz
? What does `resample("ME").sum()` do?
+ Totals the values for each month
- Removes months with missing values
- Sorts by month
= resample groups by time period. "ME" means month (labelled by its end date).
? Why use a 7-day rolling average?
- To make the data longer
+ To smooth out day-to-day noise so the trend is visible
- To fill missing days
= Each value becomes the average of the last 7 days, which evens out spikes.
? What does `pct_change()` calculate?
- The share of the total
+ The change from the previous value, as a fraction
- The running total
= It's (this − previous) / previous. Multiply by 100 for a percentage.
:::
