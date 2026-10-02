@@@ part
id: 6
title: Charts and a Final Project
level: Intermediate
blurb: Draw clear charts with matplotlib and pandas, choose the right chart for each question, then run a complete analysis from raw files to findings.

@@@ lesson
id: matplotlib-basics
title: Your first charts with matplotlib
minutes: 18
summary: Figures and axes, line charts, titles, labels, legends and saving a chart to a file.
---
A good chart shows in a second what a table takes a minute to read. **matplotlib** is Python's main charting library; pandas and most other chart tools are built on it. In the sandbox, charts appear under your code's output.

### Figure and axes

Every chart starts with two objects:

- the **figure**: the whole image, like a blank page;
- the **axes** (`ax`): one chart area on the page, with its x and y axes. You draw on `ax`.

`plt.subplots()` creates both:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5], [3, 5, 4, 7, 8])
plt.show()
```

`ax.plot(x, y)` draws a line through the points. `plt.show()` displays the chart; in the sandbox charts appear even without it, but on your own computer you need it.

### Titles and labels

A chart without labels makes the reader guess. Always set a title and label both axes, with units:

```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
revenue = [14.2, 15.8, 13.9, 17.5, 18.1, 19.6]

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(months, revenue, marker="o")
ax.set_title("Revenue grew 38% in the first half")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (£ thousands)")
plt.show()
```

`figsize=(width, height)` sets the size in inches. `marker="o"` puts a dot on each point.

### Several lines and a legend

Call `plot` again for each line. Give each a `label`, then `ax.legend()` shows the key:

```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(months, [5, 6, 8, 11, 14, 17], marker="o", label="London")
ax.plot(months, [3, 3, 7, 13, 19, 23], marker="o", label="New York")
ax.set_title("New York warms up faster than London")
ax.set_ylabel("Average temperature (°C)")
ax.legend()
plt.show()
```

### Plotting real data

pandas Series and dates work directly. Here's London's daily temperature for a year:

```python
import pandas as pd
import matplotlib.pyplot as plt

weather = pd.read_csv("weather.csv", parse_dates=["date"])
london = weather[weather["city"] == "London"]

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(london["date"], london["temp_c"], linewidth=1)
ax.plot(london["date"], london["temp_c"].rolling(14).mean(), linewidth=2.5, label="14-day average")
ax.set_title("London temperature, 2025")
ax.set_ylabel("°C")
ax.legend()
plt.show()
```

### Styling basics

Most style choices are arguments to `plot`:

| Argument | Example | Does |
|---|---|---|
| `color` | `"tab:orange"`, `"#2c679c"` | line colour |
| `linewidth` | `2` | line thickness |
| `linestyle` | `"--"`, `":"` | dashed or dotted |
| `marker` | `"o"`, `"s"` | dots or squares on points |
| `alpha` | `0.5` | transparency (0 to 1) |

```python
import matplotlib.pyplot as plt

x = list(range(10))
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(x, [v * v for v in x], color="tab:purple", linewidth=2, label="squared")
ax.plot(x, [v * 8 for v in x], color="gray", linestyle="--", label="times 8")
ax.grid(alpha=0.3)
ax.legend()
ax.set_title("Squares overtake a straight line at 8")
plt.show()
```

`ax.grid(alpha=0.3)` adds faint grid lines, which help reading values without shouting.

### Saving a chart

`fig.savefig` writes the chart to an image file for a report or slide. `dpi` sets the sharpness and `bbox_inches="tight"` trims the white border:

```python
import os
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [2, 4, 3])
ax.set_title("Saved chart")
fig.savefig("chart.png", dpi=150, bbox_inches="tight")
print(os.path.getsize("chart.png"), "bytes written")
```

:::exercise Steps this week
Draw a line chart of `steps` against `days`, with the title `"Daily steps"` and the y-axis label `"Steps"`.
```python starter
import matplotlib.pyplot as plt

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
steps = [8200, 10450, 6300, 12100, 9800, 15200, 4300]

```
```python check
ax = chart()
assert ax.get_lines(), "Draw a line with ax.plot(days, steps)."
ys = list(ax.get_lines()[0].get_ydata())
assert ys == [8200, 10450, 6300, 12100, 9800, 15200, 4300], "Plot the steps values on the y axis."
assert ax.get_title() == "Daily steps", f"The title should be 'Daily steps', not {ax.get_title()!r}."
assert ax.get_ylabel() == "Steps", f"The y label should be 'Steps', not {ax.get_ylabel()!r}."
```
```python solution
import matplotlib.pyplot as plt

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
steps = [8200, 10450, 6300, 12100, 9800, 15200, 4300]

fig, ax = plt.subplots()
ax.plot(days, steps, marker="o")
ax.set_title("Daily steps")
ax.set_ylabel("Steps")
plt.show()
```
hint: `fig, ax = plt.subplots()`, then `ax.plot(days, steps)`, `ax.set_title(...)` and `ax.set_ylabel(...)`.
:::

:::exercise Two cities
Plot New York's and Mumbai's daily `temp_c` from `weather.csv` on the **same axes** as two lines labelled `"New York"` and `"Mumbai"`, and show a legend.
```python starter
import pandas as pd
import matplotlib.pyplot as plt

weather = pd.read_csv("weather.csv", parse_dates=["date"])

```
```python check
ax = chart()
labels = sorted(l.get_label() for l in ax.get_lines())
assert labels == ["Mumbai", "New York"], f"Draw two lines labelled 'New York' and 'Mumbai' (found {labels})."
assert ax.get_legend() is not None, "Add a legend with ax.legend()."
assert all(len(l.get_ydata()) == 365 for l in ax.get_lines()), "Each line should have one point per day (365)."
```
```python solution
import pandas as pd
import matplotlib.pyplot as plt

weather = pd.read_csv("weather.csv", parse_dates=["date"])
fig, ax = plt.subplots(figsize=(8, 3.5))
for city in ["New York", "Mumbai"]:
    one = weather[weather["city"] == city]
    ax.plot(one["date"], one["temp_c"], label=city, linewidth=1)
ax.set_title("Daily temperature")
ax.set_ylabel("°C")
ax.legend()
plt.show()
```
hint: Filter each city, call `ax.plot(..., label=city)` for each, then `ax.legend()`.
:::

:::quiz
? In `fig, ax = plt.subplots()`, what is `ax`?
- The whole image
+ The chart area you draw on
- The x axis only
= The figure is the page; the axes object is the chart area with its own x and y axes.
? What does `ax.legend()` need in order to show anything?
+ Lines drawn with a `label=`
- A title
- At least three lines
= The legend lists each labelled line. Without labels it has nothing to show.
? What makes a good chart title?
- The column names
+ The finding, like "Revenue grew 38% in the first half"
- The file name
= A title that states the takeaway tells the reader what to look for.
:::

@@@ lesson
id: chart-types
title: Choosing the right chart
minutes: 20
summary: Bar charts, histograms, scatter plots and box plots, and which question each one answers.
---
Every chart type answers a particular kind of question. Pick the question first, then the chart:

| Question | Chart | matplotlib |
|---|---|---|
| How does a value change over time? | line | `ax.plot` |
| How do categories compare? | bar | `ax.bar` / `ax.barh` |
| How are values spread out? | histogram | `ax.hist` |
| Are two numbers related? | scatter | `ax.scatter` |
| How do spreads compare between groups? | box plot | `ax.boxplot` |

### Bar charts: comparing categories

```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
by_region = sales.groupby("region")["revenue"].sum().sort_values()

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.bar(by_region.index, by_region.values, color="tab:blue")
ax.set_title("North brings in the most revenue")
ax.set_ylabel("Revenue (£)")
plt.show()
```

With long category names, or many of them, a **horizontal** bar chart (`barh`) is easier to read. Sort the values so the ranking jumps out, and label each bar with `bar_label`:

```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
by_product = sales.groupby("product")["revenue"].sum().sort_values()

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(by_product.index, by_product.values / 1000, color="tab:green")
ax.bar_label(bars, fmt="%.0fk", padding=3)
ax.set_title("Laptops earn the most, despite few orders")
ax.set_xlabel("Revenue (£ thousands)")
plt.show()
```

Bar charts must start at zero: bar length *is* the value, so a cut-off axis exaggerates differences.

### Histograms: how values are spread

A **histogram** splits a number column into bins and shows how many values fall in each. It shows the shape of the data: where most values are, how spread out, and whether it's lopsided.

```python
import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_csv("students.csv")
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.hist(students["math"], bins=10, color="tab:purple", edgecolor="white")
ax.axvline(students["math"].mean(), color="black", linestyle="--", label="mean")
ax.set_title("Most students score between 40 and 80 in math")
ax.set_xlabel("Math score")
ax.set_ylabel("Number of students")
ax.legend()
plt.show()
```

`axvline` draws a vertical reference line, here at the mean.

### Scatter plots: are two things related?

Each point is one row, placed by two numbers. If the points slope upwards, the two values tend to rise together:

```python
import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_csv("students.csv")
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(students["hours_studied"], students["math"], alpha=0.7)
ax.set_title("More study hours, higher math scores")
ax.set_xlabel("Hours studied per week")
ax.set_ylabel("Math score")
plt.show()
```

Colour can add a third variable. Here each class gets its own colour:

```python
import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_csv("students.csv")
fig, ax = plt.subplots(figsize=(6, 4))
for name, group in students.groupby("class"):
    ax.scatter(group["attendance_pct"], group["math"], label=f"Class {name}", alpha=0.75)
ax.set_xlabel("Attendance (%)")
ax.set_ylabel("Math score")
ax.set_title("Attendance and math score, by class")
ax.legend()
plt.show()
```

A relationship in a scatter plot doesn't prove that one thing **causes** the other. You'll learn how to measure and test relationships in the statistics course.

### Box plots: comparing spreads

A **box plot** summarises a distribution in five numbers: the box spans the middle half (first to third quartile), the line inside is the median, the whiskers reach to the typical range, and dots beyond them are outliers. Side by side, box plots compare groups at a glance:

```python
import pandas as pd
import matplotlib.pyplot as plt

weather = pd.read_csv("weather.csv").dropna()
cities = ["London", "New York", "Mumbai"]
data = [weather.loc[weather["city"] == c, "temp_c"] for c in cities]

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.boxplot(data, tick_labels=cities)
ax.set_title("New York has the widest range of temperatures")
ax.set_ylabel("Daily temperature (°C)")
plt.show()
```

### What about pie charts?

Pie charts are hard to read: people judge angles badly, so slices of 23% and 27% look the same. A sorted bar chart almost always works better. If you do use one, keep it to two or three slices.

:::exercise Orders per segment
Join `sales.csv` with `customers.csv` on `customer_id`, count the orders per `segment`, and draw them as a **bar chart** (vertical or horizontal) with a title.
```python starter
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
customers = pd.read_csv("customers.csv")

```
```python check
import pandas as pd
ax = chart()
s = pd.read_csv("sales.csv").merge(pd.read_csv("customers.csv"), on="customer_id")
exp = sorted(s["segment"].value_counts().tolist())
bars = [p for p in ax.patches]
assert bars, "Draw bars with ax.bar or ax.barh."
vals_v = sorted(round(p.get_height()) for p in bars)
vals_h = sorted(round(p.get_width()) for p in bars)
assert exp in (vals_v, vals_h), f"The bars should show the order counts per segment: {exp}."
assert ax.get_title(), "Give the chart a title."
```
```python solution
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
customers = pd.read_csv("customers.csv")
orders = sales.merge(customers, on="customer_id")
per_segment = orders["segment"].value_counts().sort_values()

fig, ax = plt.subplots(figsize=(6, 3))
ax.barh(per_segment.index, per_segment.values)
ax.set_title("Consumers place most of the orders")
ax.set_xlabel("Orders")
plt.show()
```
hint: Merge, then `value_counts()` on `segment`, then `ax.bar(counts.index, counts.values)`.
:::

:::exercise Runtime and rating
Load `movies.json` and draw a **scatter plot** with `runtime_min` on the x axis and `rating` on the y axis. Label both axes.
```python starter
import pandas as pd
import matplotlib.pyplot as plt

movies = pd.read_json("movies.json")

```
```python check
import pandas as pd
ax = chart()
m = pd.read_json("movies.json")
assert ax.collections, "Draw points with ax.scatter(x, y)."
pts = ax.collections[0].get_offsets()
assert len(pts) == len(m), f"Plot one point per film ({len(m)})."
assert sorted(map(float, pts[:, 0])) == sorted(map(float, m["runtime_min"])), "Put runtime_min on the x axis."
assert ax.get_xlabel() and ax.get_ylabel(), "Label both axes."
```
```python solution
import pandas as pd
import matplotlib.pyplot as plt

movies = pd.read_json("movies.json")
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(movies["runtime_min"], movies["rating"])
ax.set_xlabel("Runtime (minutes)")
ax.set_ylabel("Rating")
ax.set_title("Longer films aren't rated much higher")
plt.show()
```
hint: `ax.scatter(movies["runtime_min"], movies["rating"])`, then set both labels.
:::

:::quiz
? Which chart shows how exam scores are spread out?
- Line chart
+ Histogram
- Pie chart
= A histogram counts how many values fall in each range, showing the shape of the distribution.
? Why must a bar chart's axis start at zero?
+ The bar's length represents the value, so a cut axis exaggerates differences
- matplotlib requires it
- To fit the labels
= If the axis starts at 90, a bar of 95 looks twice as long as one of 92.
? A scatter plot shows that ice-cream sales and sunburn rise together. What can you conclude?
- Ice cream causes sunburn
+ They're related; something else (sunny weather) may drive both
- Nothing at all
= Correlation isn't causation. A third factor often explains both.
:::

@@@ lesson
id: pandas-plotting
title: Charts straight from pandas
minutes: 18
summary: Plot Series and DataFrames in one line, build grids of charts, and apply the habits that make charts clear.
---
pandas can draw charts itself with `.plot`, using matplotlib underneath. It's the fastest way to look at your data while analysing, and it handles labels and legends for you.

### .plot on a Series

```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
monthly = sales.set_index("order_date")["revenue"].resample("ME").sum()

ax = monthly.plot(figsize=(7, 3.5), marker="o", title="Monthly revenue, 2025")
ax.set_ylabel("Revenue (£)")
plt.show()
```

`.plot` returns the axes, so you can keep customising with the `ax.` methods you know. Change the chart type with `kind=` or the shortcut methods:

```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
ax = sales["product"].value_counts().sort_values().plot.barh(figsize=(6, 3.5), color="tab:orange")
ax.set_title("Pen packs are ordered most often")
ax.set_xlabel("Orders")
plt.show()
```

| Shortcut | Chart |
|---|---|
| `.plot()` / `.plot.line()` | line |
| `.plot.bar()` / `.plot.barh()` | bars |
| `.plot.hist(bins=…)` | histogram |
| `.plot.scatter(x=…, y=…)` | scatter (DataFrame) |
| `.plot.box()` | box plot |

### .plot on a DataFrame

Each column becomes its own line or bar series, with a legend. A pivot table is the perfect input:

```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
table = sales.pivot_table(index="region", columns="category", values="revenue", aggfunc="sum")

ax = table.plot.bar(figsize=(7, 3.5), rot=0)
ax.set_title("Electronics leads in every region")
ax.set_ylabel("Revenue (£)")
plt.show()
```

`rot=0` keeps the labels horizontal. Add `stacked=True` to stack the categories into one bar per region.

### A grid of charts

`plt.subplots(rows, cols)` makes several axes at once. Pass `ax=` to `.plot` to draw on a particular one. This is how small dashboards are built:

```python
import pandas as pd
import matplotlib.pyplot as plt

weather = pd.read_csv("weather.csv", parse_dates=["date"])
cities = ["London", "Mumbai", "New York"]

fig, axes = plt.subplots(1, 3, figsize=(10, 3), sharey=True)
for ax, city in zip(axes, cities):
    one = weather[weather["city"] == city].set_index("date")["temp_c"]
    one.resample("ME").mean().plot(ax=ax, marker="o")
    ax.set_title(city)
    ax.set_xlabel("")
axes[0].set_ylabel("Average temperature (°C)")
fig.suptitle("Monthly average temperature, 2025")
fig.tight_layout()
plt.show()
```

`sharey=True` gives every chart the same y scale, so they can be compared fairly. `tight_layout()` stops labels overlapping.

### Habits of clear charts

The same data can be shown clearly or confusingly. Five habits make the difference:

1. **Title the finding**, not the data: "Electronics leads in every region" beats "Revenue by region and category".
2. **Label axes with units**: "Revenue (£)", "°C", "Orders".
3. **Sort bars** by value unless the categories have a natural order (like months).
4. **Remove clutter**: fewer gridlines, no 3-D, no unnecessary colours.
5. **Use colour to highlight**, not decorate. Grey for context, one colour for what matters:

```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
by_product = sales.groupby("product")["revenue"].sum().sort_values()
colours = ["tab:red" if p == "Desk Chair" else "lightgray" for p in by_product.index]

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.barh(by_product.index, by_product.values, color=colours)
ax.set_title("Desk chairs: the fourth-biggest earner")
ax.set_xlabel("Revenue (£)")
ax.spines[["top", "right"]].set_visible(False)
plt.show()
```

`ax.spines[...]` hides the top and right borders, a small change that makes charts look cleaner.

:::exercise Units by category
Use pandas plotting to draw a **bar chart** of total `units` per `category` from `sales.csv`, sorted from largest to smallest, with a title.
```python starter
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")

```
```python check
import pandas as pd
ax = chart()
s = pd.read_csv("sales.csv")
exp = s.groupby("category")["units"].sum().sort_values(ascending=False)
bars = ax.patches
assert len(bars) == 3, "Draw one bar per category (3 bars)."
vals = [round(p.get_height()) if p.get_height() >= p.get_width() else round(p.get_width()) for p in bars]
assert sorted(vals) == sorted(exp.astype(int).tolist()), f"The bars should show units per category: {exp.to_dict()}."
assert ax.get_title(), "Give the chart a title."
```
```python solution
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
units = sales.groupby("category")["units"].sum().sort_values(ascending=False)
ax = units.plot.bar(rot=0, title="Office items sell the most units")
ax.set_ylabel("Units")
plt.show()
```
hint: `sales.groupby("category")["units"].sum().sort_values(ascending=False).plot.bar(title="...")`.
:::

:::exercise Rain histogram
Draw a **histogram** of London's daily `rain_mm` (from `weather.csv`) with `bins=20`, using pandas (`.plot.hist`) or matplotlib. Give it a title and an x-axis label.
```python starter
import pandas as pd
import matplotlib.pyplot as plt

weather = pd.read_csv("weather.csv")

```
```python check
ax = chart()
assert len(ax.patches) == 20, f"Use 20 bins (found {len(ax.patches)} bars)."
total = sum(round(p.get_height()) for p in ax.patches)
assert total == 365, f"The histogram should count London's 365 days (it counts {total})."
assert ax.get_title() and ax.get_xlabel(), "Add a title and an x-axis label."
```
```python solution
import pandas as pd
import matplotlib.pyplot as plt

weather = pd.read_csv("weather.csv")
london = weather[weather["city"] == "London"]
ax = london["rain_mm"].plot.hist(bins=20, title="Most London days are dry or nearly dry")
ax.set_xlabel("Rain (mm)")
plt.show()
```
hint: Filter London first, then `["rain_mm"].plot.hist(bins=20, title=...)` and `ax.set_xlabel(...)`.
:::

:::quiz
? What does `df.plot.bar()` do with a DataFrame of three columns?
- Draws only the first column
+ Draws a bar for each column, grouped by the index, with a legend
- Raises an error
= Each column becomes a bar series, and the index provides the categories.
? Why use `sharey=True` in a grid of charts?
+ So every chart uses the same y scale and can be compared fairly
- To share one title
- To make the charts smaller
= Different scales can make a small change look as big as a large one.
? Which title is best for a chart of revenue by region?
- "Revenue by region"
- "groupby region sum"
+ "North brings in 30% of all revenue"
= Title the finding, so the reader knows what to notice.
:::

@@@ lesson
id: final-project
title: "Final project: a sales analysis"
minutes: 30
summary: Answer a business question from start to finish: load and join the files, check the data, analyse, chart and write up the findings.
---
Here's a realistic brief, the kind an analyst gets in their first month:

> *"We're planning next year's budget. How did 2025 go? Which products and customers should we focus on, and is there a seasonal pattern we should plan stock around?"*

You'll answer it with everything from this course. Each step builds on the last, so run them in order.

### Step 1: Turn the brief into questions

A vague brief becomes concrete questions you can answer with data:

1. What were total revenue, profit and order count, and how did they move month by month?
2. Which products make the most **profit** (not just revenue)?
3. Which customer segments and cities matter most?
4. Is there a seasonal pattern?

### Step 2: Load, join and check

Bring the three tables together, then check the join didn't lose or duplicate orders:

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
customers = pd.read_csv("customers.csv")
products = pd.read_csv("products.csv")

df = (sales
      .merge(customers[["customer_id", "segment", "city"]], on="customer_id", how="left", validate="many_to_one")
      .merge(products[["product", "unit_cost"]], on="product", how="left", validate="many_to_one"))
df["revenue"] = df["units"] * df["unit_price"]
df["profit"] = df["units"] * (df["unit_price"] - df["unit_cost"])

assert len(df) == len(sales), "the join changed the number of orders"
assert df[["segment", "unit_cost"]].notna().all().all(), "some orders didn't match"
print(df.shape)
print(df[["order_date", "product", "segment", "city", "revenue", "profit"]].head())
```

### Step 3: The headline numbers

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
products = pd.read_csv("products.csv")
df = sales.merge(products[["product", "unit_cost"]], on="product")
df["revenue"] = df["units"] * df["unit_price"]
df["profit"] = df["units"] * (df["unit_price"] - df["unit_cost"])

print(f"Orders:  {len(df):,}")
print(f"Revenue: £{df['revenue'].sum():,.0f}")
print(f"Profit:  £{df['profit'].sum():,.0f}  ({df['profit'].sum() / df['revenue'].sum():.0%} margin)")
print(f"Average order value: £{df['revenue'].mean():,.2f}")
```

### Step 4: Products by profit

Revenue and profit can tell different stories, because margins differ:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
products = pd.read_csv("products.csv")
df = sales.merge(products[["product", "unit_cost"]], on="product")
df["revenue"] = df["units"] * df["unit_price"]
df["profit"] = df["units"] * (df["unit_price"] - df["unit_cost"])

by_product = df.groupby("product").agg(
    orders=("order_id", "count"),
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
)
by_product["margin_pct"] = (by_product["profit"] / by_product["revenue"] * 100).round(0)
by_product["profit_share"] = (by_product["profit"] / by_product["profit"].sum() * 100).round(1)
print(by_product.sort_values("profit", ascending=False).round(0))
```

### Step 5: Customers

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
customers = pd.read_csv("customers.csv")
products = pd.read_csv("products.csv")
df = (sales.merge(customers[["customer_id", "segment", "city"]], on="customer_id")
           .merge(products[["product", "unit_cost"]], on="product"))
df["profit"] = df["units"] * (df["unit_price"] - df["unit_cost"])

seg = df.groupby("segment").agg(customers=("customer_id", "nunique"), profit=("profit", "sum"))
seg["profit_per_customer"] = (seg["profit"] / seg["customers"]).round(0)
print(seg.sort_values("profit_per_customer", ascending=False))

top_customers = df.groupby("customer_id")["profit"].sum().nlargest(10)
print(f"Top 10 customers bring {top_customers.sum() / df['profit'].sum():.0%} of profit")
```

### Step 6: Seasonality, in a chart

A two-chart dashboard: the monthly trend, and profit by product:

```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
products = pd.read_csv("products.csv")
df = sales.merge(products[["product", "unit_cost"]], on="product")
df["profit"] = df["units"] * (df["unit_price"] - df["unit_cost"])

monthly = df.set_index("order_date")["profit"].resample("ME").sum()
by_product = df.groupby("product")["profit"].sum().sort_values()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
ax1.plot(monthly.index.strftime("%b"), monthly.values / 1000, marker="o")
ax1.set_title("Monthly profit (£k)")
ax1.set_ylim(bottom=0)
ax1.grid(alpha=0.3)

colours = ["tab:blue" if v >= by_product.iloc[-3] else "lightgray" for v in by_product.values]
ax2.barh(by_product.index, by_product.values / 1000, color=colours)
ax2.set_title("Profit by product (£k): top 3 highlighted")
for ax in (ax1, ax2):
    ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
plt.show()
```

### Step 7: Write it up

Numbers don't speak for themselves. The last step is a short summary in plain language: the answer first, then the evidence, then what to do. For example:

> **2025 summary.** 600 orders brought in about £195k revenue and £71k profit (a 36% margin).
> Laptops alone earn 39% of the profit from only 41 orders; with headphones and monitors, the top three products earn nearly three-quarters of it, so stock-outs there are expensive.
> Pen packs and notebooks are ordered most often but earn little; they bring customers back rather than profit.
> Business customers are worth the most each (about £670 of profit per customer, against £590 for consumers). Monthly profit swings from about £2.7k (November) to £8.7k (August), but one year of data isn't enough to call that a reliable season; compare with 2024 before planning stock around it.

Always check every number in the write-up against your output before sending it. That habit is what makes people trust an analyst.

### Step 8: Save the results

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
products = pd.read_csv("products.csv")
df = sales.merge(products[["product", "unit_cost"]], on="product")
df["profit"] = df["units"] * (df["unit_price"] - df["unit_cost"])
summary = df.groupby("product")["profit"].sum().round(2).sort_values(ascending=False)

summary.to_csv("profit_by_product.csv")
summary.to_json("profit_by_product.json", indent=2)
print(open("profit_by_product.csv").read())
```

You've now done the full workflow from the first lesson: **ask, load, clean, analyse, show, share**. That's the core of both the analyst and AI engineer paths. The next courses build on it with statistics and machine learning.

:::exercise The project table
Join `sales.csv` with `products.csv` (the `product` and `unit_cost` columns) and build `report`, indexed by `category`, with three named columns: `revenue` (sum), `profit` (sum) and `margin_pct` (profit ÷ revenue × 100, not rounded). Sort it by `profit`, largest first.
```python starter
import pandas as pd

sales = pd.read_csv("sales.csv")
products = pd.read_csv("products.csv")

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv").merge(pd.read_csv("products.csv")[["product", "unit_cost"]], on="product")
s["revenue"] = s["units"] * s["unit_price"]
s["profit"] = s["units"] * (s["unit_price"] - s["unit_cost"])
exp = s.groupby("category").agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
exp["margin_pct"] = exp["profit"] / exp["revenue"] * 100
exp = exp.sort_values("profit", ascending=False)
got = need("report", pd.DataFrame)
same(got[["revenue", "profit", "margin_pct"]], exp, "report", tol=1e-4)
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv")
products = pd.read_csv("products.csv")
df = sales.merge(products[["product", "unit_cost"]], on="product")
df["revenue"] = df["units"] * df["unit_price"]
df["profit"] = df["units"] * (df["unit_price"] - df["unit_cost"])

report = df.groupby("category").agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
report["margin_pct"] = report["profit"] / report["revenue"] * 100
report = report.sort_values("profit", ascending=False)
print(report.round(1))
```
hint: Merge, add `revenue` and `profit`, `groupby("category").agg(...)`, then add `margin_pct` and sort.
:::

:::exercise Profit by month chart
Draw a **line chart** of total `profit` per month (resample `"ME"`) for 2025, with a title. There should be 12 points.
```python starter
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
products = pd.read_csv("products.csv")

```
```python check
import pandas as pd
ax = chart()
s = pd.read_csv("sales.csv", parse_dates=["order_date"]).merge(pd.read_csv("products.csv")[["product", "unit_cost"]], on="product")
s["profit"] = s["units"] * (s["unit_price"] - s["unit_cost"])
m = s.set_index("order_date")["profit"].resample("ME").sum()
lines = ax.get_lines()
assert lines, "Draw a line chart."
ys = [float(v) for v in lines[0].get_ydata()]
assert len(ys) == 12, f"There should be 12 monthly points, not {len(ys)}."
ok = all(abs(a - b) < 1e-6 for a, b in zip(ys, m.values)) or all(abs(a - b / 1000) < 1e-6 for a, b in zip(ys, m.values))
assert ok, "The line should show total profit per month."
assert ax.get_title() or ax.figure._suptitle, "Give the chart a title."
```
```python solution
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
products = pd.read_csv("products.csv")
df = sales.merge(products[["product", "unit_cost"]], on="product")
df["profit"] = df["units"] * (df["unit_price"] - df["unit_cost"])
monthly = df.set_index("order_date")["profit"].resample("ME").sum()

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(monthly.index, monthly.values, marker="o")
ax.set_title("Monthly profit, 2025")
ax.set_ylabel("Profit (£)")
plt.show()
```
hint: Merge, add `profit`, then `df.set_index("order_date")["profit"].resample("ME").sum()` and plot it.
:::

:::quiz
? What should come first in an analysis?
+ Turning the brief into specific questions
- Drawing charts
- Removing outliers
= Clear questions decide which data, steps and charts you need.
? Why check `len(df) == len(sales)` after the joins?
- To make the code faster
+ To catch a join that dropped or duplicated orders
- pandas requires it
= A bad join silently changes your totals. Checking the row count catches it.
? What belongs first in a write-up?
- The code
+ The answer to the question
- A list of every number calculated
= Lead with the finding, then the evidence, then the recommendation.
:::
