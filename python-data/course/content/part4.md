@@@ part
id: 4
title: Cleaning Data
level: Intermediate
blurb: Real data is messy. Find and fix missing values, wrong types, untidy text, duplicates, impossible values and dates, then clean a whole HR export from start to finish.

@@@ lesson
id: missing-values
title: Missing values
minutes: 18
summary: Find missing values, decide whether to drop or fill them, and fill them sensibly.
---
Almost every real dataset has gaps: a sensor that didn't report, a form field left blank, a film with no box-office figure. pandas marks them as **missing** (shown as `NaN`, `None` or `<NA>`). Most summaries skip them quietly, which is convenient but can hide problems. So the first job is to find them.

### Finding missing values

`isna()` gives True where a value is missing. Add `.sum()` to count per column:

```python
import pandas as pd

weather = pd.read_csv("weather.csv")
print(weather.isna().sum())
print("Rows with any gap:", weather.isna().any(axis=1).sum())
```

Look at the rows themselves before deciding what to do:

```python
import pandas as pd

weather = pd.read_csv("weather.csv")
print(weather[weather["temp_c"].isna()].head())
```

`notna()` is the opposite, handy for keeping only complete rows of one column.

### How missing values behave

```python
import pandas as pd

movies = pd.read_json("movies.json")
box = movies["box_office_musd"]
print(len(box), box.count())     # count() skips the missing ones
print(box.mean())                # the mean of the 37 known values
print(box.sum())
```

The mean is the average of the films **with** a figure. That's often right, but always say so ("average box office of the 37 films with data").

### Option 1: drop them

`dropna()` removes rows with a missing value. `subset=` limits which columns to look at:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
print(len(employees))
print(len(employees.dropna()))                     # any column missing: drop
print(len(employees.dropna(subset=["salary"])))    # only if salary is missing
```

Dropping is fine when only a few rows are affected and they're not special. Here `dropna()` would throw away 12 of 40 rows, far too many. Notice that `subset` lets you drop only rows that lack the value **this** analysis needs.

### Option 2: fill them

`fillna(value)` replaces missing values. What you fill with is a judgement call:

| Situation | Fill with |
|---|---|
| a missing count really means none | `0` |
| a missing category | a label like `"Unknown"` |
| a number roughly typical of its column | the median (or mean) |
| a reading in a time series | the previous value (`ffill`) |

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
employees["email"] = employees["email"].fillna("unknown")
print(employees["email"].isna().sum())

movies = pd.read_json("movies.json")
median_box = movies["box_office_musd"].median()
movies["box_filled"] = movies["box_office_musd"].fillna(median_box)
print(movies[movies["box_office_musd"].isna()][["title", "box_office_musd", "box_filled"]])
```

For a time series, the day before is usually the best guess for a missing day. Sort by date first, and fill **within each city**, otherwise London's last value could fill Mumbai's gap:

```python
import pandas as pd

weather = pd.read_csv("weather.csv").sort_values(["city", "date"])
weather["temp_filled"] = weather.groupby("city")["temp_c"].ffill()
gaps = weather["temp_c"].isna()
print(weather[gaps][["date", "city", "temp_c", "temp_filled"]].head())
```

`groupby` gets a full lesson in Part 5; here it just means "do this separately for each city".

### Option 3: flag them

Sometimes the fact that a value is missing is information. Keep a True/False column so it isn't lost:

```python
import pandas as pd

movies = pd.read_json("movies.json")
movies["box_office_known"] = movies["box_office_musd"].notna()
print(movies["box_office_known"].value_counts())
```

### Missing values hiding as text

Files sometimes write gaps as `"N/A"`, `"-"` or `"missing"`. pandas only recognises some of these, so tell `read_csv` with `na_values`:

```python
import io
import pandas as pd

text = "city,temp\nLeeds,14\nYork,-\nHull,missing\n"
print(pd.read_csv(io.StringIO(text)))
print(pd.read_csv(io.StringIO(text), na_values=["-", "missing"]))
```

`io.StringIO` lets `read_csv` read from a string as if it were a file, which is handy for small tests.

:::exercise Count the gaps
Load `employees_messy.csv` and store the number of missing values **in each column** in `missing` (a Series), and the total number of missing values in the whole table in `total_missing`.
```python starter
import pandas as pd

employees = pd.read_csv("employees_messy.csv")

```
```python check
import pandas as pd
e = pd.read_csv("employees_messy.csv")
same(need("missing", pd.Series), e.isna().sum(), "missing")
same(int(need("total_missing")), int(e.isna().sum().sum()), "total_missing")
```
```python solution
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
missing = employees.isna().sum()
total_missing = missing.sum()
print(missing)
print(total_missing)
```
hint: `isna().sum()` counts per column; summing that Series gives the total.
:::

:::exercise Fill the temperatures
Load `weather.csv` and fill the missing `temp_c` values with the **median temperature of that city**. Store the result back in `weather["temp_c"]`, so no gaps remain.
```python starter
import pandas as pd

weather = pd.read_csv("weather.csv")

```
```python check
import pandas as pd
w = pd.read_csv("weather.csv")
med = w.groupby("city")["temp_c"].transform("median")
exp = w["temp_c"].fillna(med)
got = need("weather", pd.DataFrame)
assert got["temp_c"].isna().sum() == 0, "There are still missing temperatures."
same(got.sort_index()["temp_c"], exp, "weather['temp_c']")
```
```python solution
import pandas as pd

weather = pd.read_csv("weather.csv")
city_median = weather.groupby("city")["temp_c"].transform("median")
weather["temp_c"] = weather["temp_c"].fillna(city_median)
print(weather["temp_c"].isna().sum())
```
hint: `weather.groupby("city")["temp_c"].transform("median")` gives each row its city's median. Pass that to `fillna`.
:::

:::quiz
? What does `df.isna().sum()` show?
+ The number of missing values in each column
- The number of rows
- The sum of each column
= `isna()` marks gaps as True, and summing counts them per column.
? When is `fillna(0)` a good choice?
- Always
+ When a missing value really means zero, like "no sales recorded"
- For temperatures
= Filling with 0 claims the value was zero. That's only right when missing really means none.
? What does `dropna(subset=["salary"])` drop?
- Every row with any missing value
+ Only rows where salary is missing
- The salary column
= `subset` limits the check to the listed columns.
:::

@@@ lesson
id: data-types
title: Fixing data types
minutes: 16
summary: Spot columns with the wrong type and convert them with astype, to_numeric and categories.
---
A column's dtype decides what you can do with it. A salary stored as text can't be averaged; a postcode stored as a number loses its leading zero. Fixing types is one of the most common cleaning jobs.

### Spotting the problem

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
print(employees.dtypes)
print(employees["salary"].head(6))
```

`salary` is `str` (text) because some values contain `$` and commas. Trying to do maths fails or gives nonsense:

```python error
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
print(employees["salary"].mean())
```

### astype: convert when the values are clean

`astype` converts a whole column. It works when every value can be converted:

```python
import pandas as pd

df = pd.DataFrame({"units": ["3", "12", "7"], "price": ["4.5", "6", "35"]})
print(df.dtypes)
df["units"] = df["units"].astype(int)
df["price"] = df["price"].astype(float)
print(df.dtypes)
print((df["units"] * df["price"]).sum())
```

### Cleaning text into numbers

For the salaries, first strip out the `$` and the commas with `.str.replace`, then convert. `pd.to_numeric` is safer than `astype` because `errors="coerce"` turns anything that still can't be converted into a missing value instead of crashing:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
cleaned = (employees["salary"]
           .str.replace("$", "", regex=False)
           .str.replace(",", "", regex=False))
employees["salary"] = pd.to_numeric(cleaned, errors="coerce")
print(employees["salary"].head(6))
print(employees["salary"].dtype)
print("Average salary:", employees["salary"].mean().round(0))
```

`regex=False` tells pandas to treat `"$"` as a plain character. (In patterns, `$` has a special meaning.)

See what `errors="coerce"` does with values that aren't numbers:

```python
import pandas as pd

raw = pd.Series(["10", "12.5", "n/a", "eight", "7"])
print(pd.to_numeric(raw, errors="coerce"))
```

After converting, always count how many values became missing. If it's more than you expected, some formats weren't handled.

### Whole numbers with gaps

A normal integer column can't hold missing values, so pandas makes it `float64` (that's why `age` shows `49.0`). The **nullable** integer type `"Int64"` (capital I) keeps whole numbers and allows gaps:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
print(employees["age"].head(6))
employees["age"] = employees["age"].astype("Int64")
print(employees["age"].head(6))
```

### Numbers that should be text

IDs, phone numbers and postcodes look like numbers but aren't for maths. Read them as text with `dtype=` so leading zeros survive:

```python
import io
import pandas as pd

text = "store,postcode\nA,02134\nB,10001\n"
print(pd.read_csv(io.StringIO(text)))
print(pd.read_csv(io.StringIO(text), dtype={"postcode": str}))
```

### Categories

A text column with a few repeating values (regions, segments, sizes) can be a **category**. It uses less memory and can have a meaningful order:

```python
import pandas as pd

sizes = pd.Series(["M", "S", "L", "M", "S"])
sizes = pd.Categorical(sizes, categories=["S", "M", "L"], ordered=True)
print(sizes)
print(sorted(sizes))
print(sizes.max())
```

Without the category, sorting gives `L, M, S` (alphabetical). With it, sorting follows S, M, L.

:::exercise Clean the salaries
Load `employees_messy.csv` and convert `salary` into numbers: remove `$` and commas, then use `pd.to_numeric(..., errors="coerce")`. Store the result back in `employees["salary"]`, and store the **median salary** in `median_salary`.
```python starter
import pandas as pd

employees = pd.read_csv("employees_messy.csv")

```
```python check
import pandas as pd
e = pd.read_csv("employees_messy.csv")
s = pd.to_numeric(e["salary"].str.replace("$", "", regex=False).str.replace(",", "", regex=False), errors="coerce")
got = need("employees", pd.DataFrame)
assert pd.api.types.is_numeric_dtype(got["salary"]), "employees['salary'] should be numbers now."
same(got["salary"], s, "employees['salary']")
same(float(need("median_salary")), float(s.median()), "median_salary")
```
```python solution
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
cleaned = employees["salary"].str.replace("$", "", regex=False).str.replace(",", "", regex=False)
employees["salary"] = pd.to_numeric(cleaned, errors="coerce")
median_salary = employees["salary"].median()
print(median_salary)
```
hint: Chain two `.str.replace(..., "", regex=False)` calls, then wrap the result in `pd.to_numeric(..., errors="coerce")`.
:::

:::exercise Numbers from a survey
`answers` holds how many hours people said they slept, typed by hand. Convert it with `pd.to_numeric` so the words become missing values, store it in `hours`, and store how many answers couldn't be converted in `bad`.
```python starter
import pandas as pd

answers = pd.Series(["7", "8", "six", "7.5", "", "9", "about 6", "5"])

```
```python check
import pandas as pd
a = pd.Series(["7", "8", "six", "7.5", "", "9", "about 6", "5"])
h = pd.to_numeric(a, errors="coerce")
same(need("hours", pd.Series), h, "hours")
same(int(need("bad")), int(h.isna().sum()), "bad")
```
```python solution
import pandas as pd

answers = pd.Series(["7", "8", "six", "7.5", "", "9", "about 6", "5"])
hours = pd.to_numeric(answers, errors="coerce")
bad = hours.isna().sum()
print(hours)
print(bad)
```
hint: `errors="coerce"` turns what it can't read into NaN; count those with `.isna().sum()`.
:::

:::quiz
? Why did `salary` load as text?
- CSV files can't hold numbers
+ Some values contain `$` and commas, so pandas can't read them as numbers
- pandas always reads money as text
= One unreadable value is enough to make pandas keep the whole column as text.
? What does `pd.to_numeric(s, errors="coerce")` do with `"eight"`?
- Converts it to 8
+ Turns it into a missing value
- Raises an error
= "coerce" replaces anything it can't convert with NaN, so check how many values went missing.
? Why read postcodes with `dtype={"postcode": str}`?
+ To keep leading zeros, since postcodes aren't for maths
- To make them faster to sort
- Because numbers can't be in CSV files
= As numbers, `02134` becomes `2134`. Codes and IDs should stay text.
:::

@@@ lesson
id: text-cleaning
title: Cleaning text
minutes: 18
summary: Fix spaces, capitals and spelling variants with the .str methods, and search and split text columns.
---
Text typed by people is inconsistent: `"Sales"`, `"sales"` and `"SALES "` are the same department to you, but three different values to a computer. Until they match, counts and groups are wrong.

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
print(employees["department"].value_counts())
```

There are really only four departments. Let's fix it.

### The .str accessor

Every string method you know (`strip`, `lower`, `replace`…) works on a whole text column through `.str`:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
dept = employees["department"].str.strip().str.title()
print(dept.value_counts())
```

`strip()` removes spaces at the ends, and `title()` makes every word start with a capital. Four departments, but look closely: `title()` turned `HR` into `Hr`. Fix exceptions like that with `.replace`, which swaps whole values:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
dept = employees["department"].str.strip().str.title().replace({"Hr": "HR"})
print(dept.value_counts())
```

| Method | Does | `"  sales team "` becomes |
|---|---|---|
| `.str.strip()` | remove spaces at both ends | `"sales team"` |
| `.str.lower()` / `.str.upper()` | all small / all capital letters | `"  sales team "` → `"  SALES TEAM "` |
| `.str.title()` | capitalise each word | `"  Sales Team "` |
| `.str.replace(a, b)` | swap text | |
| `.str.len()` | number of characters | `14` |

### Names

The same treatment tidies names:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
print(employees["name"].head(4).tolist())
employees["name"] = employees["name"].str.strip().str.title()
print(employees["name"].head(4).tolist())
```

`title()` isn't perfect: it would turn "McDonald" into "Mcdonald". For real people's names, check a sample by eye.

### Mapping spelling variants

When the variants aren't just spaces and capitals, map them to one value with `replace` and a dictionary:

```python
import pandas as pd

answers = pd.Series(["UK", "U.K.", "United Kingdom", "uk", "France", "FR"])
clean = answers.str.upper().replace({"U.K.": "UK", "UNITED KINGDOM": "UK", "FR": "FRANCE"})
print(clean.value_counts())
```

Note the difference: `.str.replace` swaps **part** of each string, while `.replace` (no `.str`) swaps **whole** values.

### Searching text

`contains`, `startswith` and `endswith` give True/False masks for filtering. `case=False` ignores capitals:

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
desk = sales[sales["product"].str.contains("desk", case=False)]
print(desk["product"].unique())

customers = pd.read_csv("customers.csv")
print(customers[customers["name"].str.endswith("Patel")]["name"].tolist())
```

### Splitting and extracting

`str.split` breaks text into parts. `expand=True` puts the parts into separate columns, and `.str[0]` takes the first part:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
emails = employees["email"].dropna()
print(emails.str.split("@").str[1].value_counts())

names = employees["name"].str.strip().str.title()
parts = names.str.split(" ", expand=True)
parts.columns = ["first", "last"]
print(parts.head(3))
```

`str.extract` pulls out the part of each value that matches a **pattern** (a regular expression). `(\d+)` means "one or more digits":

```python
import pandas as pd

codes = pd.Series(["Room 12", "Room 3", "Lab 101", "Hall"])
print(codes.str.extract(r"(\d+)"))
```

Regular expressions are a language of their own; you only need simple ones like this for now.

### Missing values in text

`.str` methods leave missing values missing, so they're safe to use on columns with gaps. But masks with gaps need `na=False` to decide what a missing value counts as:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
has_example = employees["email"].str.endswith("@example.com", na=False)
print(has_example.sum(), "of", len(employees), "have an example.com email")
```

:::exercise Tidy departments
Load `employees_messy.csv` and clean `department` so that every value is stripped of spaces and in title case (like `"Sales"`). Store the cleaned column back in `employees["department"]`, then store `employees["department"].value_counts()` in `dept_counts`.
```python starter
import pandas as pd

employees = pd.read_csv("employees_messy.csv")

```
```python check
import pandas as pd
e = pd.read_csv("employees_messy.csv")
d = e["department"].str.strip().str.title()
got = need("employees", pd.DataFrame)
same(got["department"], d, "employees['department']")
c = need("dept_counts", pd.Series)
same(int(c["Sales"]), int((d == "Sales").sum()), "dept_counts['Sales']")
assert len(c) == 4, f"There should be 4 departments, but dept_counts has {len(c)}."
```
```python solution
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
employees["department"] = employees["department"].str.strip().str.title()
dept_counts = employees["department"].value_counts()
print(dept_counts)
```
hint: Chain `.str.strip()` and `.str.title()`.
:::

:::exercise Email domains
`emails` holds some addresses with stray spaces and capitals. Make `domains`: the part after the `@` in each address, lower case with no spaces.
```python starter
import pandas as pd

emails = pd.Series([" Ada@Example.com", "grace@NAVY.mil ", "alan@cam.ac.uk", " LINUS@Example.COM "])

```
```python check
import pandas as pd
same(list(need("domains", pd.Series)), ["example.com", "navy.mil", "cam.ac.uk", "example.com"], "domains")
```
```python solution
import pandas as pd

emails = pd.Series([" Ada@Example.com", "grace@NAVY.mil ", "alan@cam.ac.uk", " LINUS@Example.COM "])
domains = emails.str.strip().str.lower().str.split("@").str[1]
print(domains)
```
hint: Clean first (`strip`, `lower`), then `.str.split("@").str[1]`.
:::

:::quiz
? Why does `value_counts()` show `"Sales"` and `"sales"` separately?
+ Text comparisons are exact, including capital letters
- pandas counts randomly
- One of them is missing
= To a computer they're different strings. Standardise the case before counting.
? What's the difference between `s.str.replace("a", "b")` and `s.replace({"a": "b"})`?
- None
+ `.str.replace` changes part of each string; `.replace` swaps whole values
- `.replace` only works on numbers
= Use `.str.replace` for characters inside text, and `.replace` to map complete values.
? What does `.str.split("@").str[1]` give for `"ada@example.com"`?
- `"ada"`
+ `"example.com"`
- `["ada", "example.com"]`
= Split makes a list of parts; `.str[1]` takes the second part.
:::

@@@ lesson
id: duplicates-and-outliers
title: Duplicates and impossible values
minutes: 16
summary: Find and remove repeated rows, catch values that can't be true, and spot outliers.
---
Two more problems spoil results quietly: rows counted twice, and values that can't be right (an age of 230, a negative price). Neither causes an error. You only find them by looking.

### Exact duplicates

`duplicated()` marks every row that repeats an earlier one. `drop_duplicates()` removes them:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
print("duplicate rows:", employees.duplicated().sum())
print(employees[employees.duplicated(keep=False)].sort_values("emp_id")[["emp_id", "name"]])

employees = employees.drop_duplicates()
print(len(employees), "rows left")
```

`keep=False` marks **all** copies, so you can see both the original and the repeat.

### Duplicates by key

Often the rows aren't identical (one has a typo fixed), but the **key** (the ID that should be unique) repeats. Use `subset=`:

```python
import pandas as pd

log = pd.DataFrame({
    "order_id": [1, 2, 2, 3],
    "status":   ["sent", "packed", "sent", "sent"],
    "updated":  ["09:00", "09:05", "11:30", "10:00"],
})
print(log.duplicated(subset=["order_id"]).sum(), "repeated order ids")
latest = log.sort_values("updated").drop_duplicates(subset=["order_id"], keep="last")
print(latest)
```

`keep="last"` keeps the final version of each order. Sorting first makes "last" mean "most recent".

Duplicates can also hide behind formatting: `"MEI BROWN"` and `"Mei Brown"` only match after cleaning the text. Clean first, then de-duplicate.

### Impossible values

`describe()` shows the minimum and maximum of every number column, which is where impossible values show up:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
print(employees["age"].describe())
print(employees[(employees["age"] < 16) | (employees["age"] > 100)][["emp_id", "name", "age"]])
```

An employee can't be 230 or -1. These are typing errors. The safest fix is to mark them as missing (you can't know the true age), using `mask`:

```python
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
bad = (employees["age"] < 16) | (employees["age"] > 100)
employees["age"] = employees["age"].mask(bad)
print(employees["age"].describe())
```

`mask(condition)` replaces values where the condition is True with missing. (Its opposite, `where`, keeps values where the condition is True.)

### Capping with clip

When values are possible but extreme and you want to limit their effect, `clip` caps them at a floor and ceiling:

```python
import pandas as pd

scores = pd.Series([45, 102, 88, -5, 67])
print(scores.clip(lower=0, upper=100))
```

### Outliers

An **outlier** is a value far from the rest. Unlike an impossible value, it might be real: a genuinely huge order, a heatwave day. A common rule of thumb uses the **IQR** (interquartile range, the spread of the middle half of the data): anything more than 1.5 × IQR beyond the quartiles is flagged.

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]

q1, q3 = sales["revenue"].quantile([0.25, 0.75])
iqr = q3 - q1
high = q3 + 1.5 * iqr
outliers = sales[sales["revenue"] > high]
print(f"Q1 {q1}, Q3 {q3}, cut-off {high}")
print(len(outliers), "unusually large orders")
print(outliers["product"].value_counts())
```

The "outliers" here are all laptop, monitor and desk-chair orders: perfectly real, just expensive. That's the lesson: **flag outliers and investigate; don't delete them automatically.**

:::exercise Remove the repeats
Load `employees_messy.csv`, remove exact duplicate rows, and store the result in `unique_emps`. Store the number of rows that were removed in `removed`.
```python starter
import pandas as pd

employees = pd.read_csv("employees_messy.csv")

```
```python check
import pandas as pd
e = pd.read_csv("employees_messy.csv")
same(need("unique_emps", pd.DataFrame), e.drop_duplicates(), "unique_emps")
same(int(need("removed")), 3, "removed")
```
```python solution
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
unique_emps = employees.drop_duplicates()
removed = len(employees) - len(unique_emps)
print(removed)
```
hint: `drop_duplicates()`, then compare the lengths before and after.
:::

:::exercise Impossible ages
Load `employees_messy.csv` and replace every `age` below 16 or above 100 with a missing value, using `mask`. Store the cleaned table in `employees` and the oldest valid age in `oldest`.
```python starter
import pandas as pd

employees = pd.read_csv("employees_messy.csv")

```
```python check
import pandas as pd
e = pd.read_csv("employees_messy.csv")
a = e["age"].mask((e["age"] < 16) | (e["age"] > 100))
got = need("employees", pd.DataFrame)
same(got["age"], a, "employees['age']")
same(float(need("oldest")), float(a.max()), "oldest")
```
```python solution
import pandas as pd

employees = pd.read_csv("employees_messy.csv")
bad = (employees["age"] < 16) | (employees["age"] > 100)
employees["age"] = employees["age"].mask(bad)
oldest = employees["age"].max()
print(oldest)
```
hint: Build the condition with `|`, then `employees["age"].mask(bad)`.
:::

:::quiz
? What does `df.duplicated()` mark as True?
- Every row that has a copy, including the first
+ Each row that repeats an earlier row
- Rows with missing values
= By default the first copy is kept (False) and later repeats are True. `keep=False` marks all copies.
? An age of 230 appears. What's usually the best fix?
- Change it to 23
+ Mark it as missing, since the true value is unknown
- Delete the whole column
= Guessing could be wrong. Marking it missing is honest, and you can decide later whether to fill it.
? Why not delete every outlier?
+ Outliers can be real and important, like a very large genuine order
- pandas can't delete rows
- Outliers are always errors
= Investigate first. Impossible values are errors; unusual ones may be the most interesting rows.
:::

@@@ lesson
id: dates-and-times
title: Dates and times
minutes: 18
summary: Convert text to real dates, pull out years, months and weekdays, filter by date, and measure time between dates.
---
Dates in a CSV are just text like `"2025-03-14"`. Until you convert them, pandas can't tell March from May or work out how many days apart two dates are.

### Converting with to_datetime

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
print(sales["order_date"].dtype)
sales["order_date"] = pd.to_datetime(sales["order_date"])
print(sales["order_date"].dtype)
print(sales["order_date"].head(3))
```

You can also convert while loading with `parse_dates`:

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
print(sales.dtypes["order_date"])
```

### Parts of a date: .dt

Once a column is a datetime, `.dt` gives you its parts:

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
d = sales["order_date"]
parts = pd.DataFrame({
    "date": d,
    "year": d.dt.year,
    "month": d.dt.month,
    "month_name": d.dt.month_name(),
    "day": d.dt.day,
    "weekday": d.dt.day_name(),
    "quarter": d.dt.quarter,
})
print(parts.head())
```

These make great grouping columns. Which weekday gets the most orders?

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
print(sales["order_date"].dt.day_name().value_counts())
```

### Filtering by date

Compare a datetime column with a date written as text, or use the parts:

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
q4 = sales[sales["order_date"] >= "2025-10-01"]
print(len(q4), "orders in Q4")

summer = sales[sales["order_date"].dt.month.isin([6, 7, 8])]
print(len(summer), "orders in summer")

first_week = sales[sales["order_date"].between("2025-01-01", "2025-01-07")]
print(first_week[["order_id", "order_date"]])
```

### Time between dates

Subtracting dates gives a **Timedelta** (a length of time). `.dt.days` turns it into a number of days:

```python
import pandas as pd

customers = pd.read_csv("customers.csv", parse_dates=["signup_date"])
today = pd.Timestamp("2026-01-01")
customers["days_since_signup"] = (today - customers["signup_date"]).dt.days
customers["years"] = (customers["days_since_signup"] / 365.25).round(1)
print(customers[["name", "signup_date", "days_since_signup", "years"]].head())
```

You can add time to dates too:

```python
import pandas as pd

order = pd.Timestamp("2025-03-28")
print(order + pd.Timedelta(days=5))
print(order + pd.DateOffset(months=1))
```

`Timedelta(days=5)` is an exact length; `DateOffset(months=1)` moves along the calendar (months have different lengths).

### Formatting dates as text

`dt.strftime` writes dates in any format, for reports and labels:

```python
import pandas as pd

dates = pd.to_datetime(pd.Series(["2025-03-14", "2025-12-01"]))
print(dates.dt.strftime("%d %b %Y").tolist())
print(dates.dt.strftime("%Y-%m").tolist())
```

| Code | Means | Example |
|---|---|---|
| `%Y` | year | 2025 |
| `%m` | month number | 03 |
| `%b` / `%B` | short / full month name | Mar / March |
| `%d` | day | 14 |
| `%A` | weekday | Friday |

### Day-first dates

`03/04/2025` is 3 April in the UK and March 4 in the US. Tell pandas which you mean with `dayfirst=True`, or better, give the exact `format`:

```python
import pandas as pd

raw = pd.Series(["03/04/2025", "25/12/2025"])
print(pd.to_datetime(raw, dayfirst=True))
print(pd.to_datetime(raw, format="%d/%m/%Y"))
```

Bad dates can be turned into missing values with `errors="coerce"`, just like numbers.

:::exercise Orders by month
Load `sales.csv` with `order_date` as a real date, add a column `month` holding each order's **month number** (1 to 12), and store how many orders were placed in **December** in `dec_orders`.
```python starter
import pandas as pd

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv", parse_dates=["order_date"])
got = need("sales", pd.DataFrame)
same(got["month"], s["order_date"].dt.month, "sales['month']")
same(int(need("dec_orders")), int((s["order_date"].dt.month == 12).sum()), "dec_orders")
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["order_date"])
sales["month"] = sales["order_date"].dt.month
dec_orders = (sales["month"] == 12).sum()
print(dec_orders)
```
hint: Use `parse_dates=["order_date"]`, then `sales["order_date"].dt.month`.
:::

:::exercise Customer tenure
Load `customers.csv` with `signup_date` as a date. Add `tenure_days`: the number of days from each signup date to **1 January 2026**. Store the name of the customer who signed up **earliest** in `first_customer`.
```python starter
import pandas as pd

```
```python check
import pandas as pd
c = pd.read_csv("customers.csv", parse_dates=["signup_date"])
t = (pd.Timestamp("2026-01-01") - c["signup_date"]).dt.days
got = need("customers", pd.DataFrame)
same(got["tenure_days"], t, "customers['tenure_days']")
same(need("first_customer"), c.loc[c["signup_date"].idxmin(), "name"], "first_customer")
```
```python solution
import pandas as pd

customers = pd.read_csv("customers.csv", parse_dates=["signup_date"])
customers["tenure_days"] = (pd.Timestamp("2026-01-01") - customers["signup_date"]).dt.days
first_customer = customers.loc[customers["signup_date"].idxmin(), "name"]
print(first_customer)
```
hint: `(pd.Timestamp("2026-01-01") - customers["signup_date"]).dt.days`. The earliest signup has the smallest date: `idxmin()`.
:::

:::quiz
? Why convert a date column with `pd.to_datetime`?
- To make it shorter
+ So pandas understands it as dates: parts, sorting, filtering and differences
- CSV files require it
= As text it's just characters. As datetimes you get `.dt.month`, date maths and correct comparisons.
? What does subtracting two dates give?
+ A Timedelta (a length of time)
- A date
- A number of seconds as text
= Use `.dt.days` on a Timedelta column to get whole days.
? What does `dayfirst=True` change?
- The weekday names
+ `03/04/2025` is read as 3 April, not 4 March
- Dates are sorted newest first
= It tells pandas the day comes before the month, as in UK-style dates.
:::

@@@ lesson
id: cleaning-project
title: "Project: clean an HR export"
minutes: 25
summary: Put the whole of Part 4 together: clean employees_messy.csv step by step into a tidy, trustworthy table.
---
Time to clean a real mess from start to finish. `employees_messy.csv` is an HR export with every problem from this part. You'll build the cleaning one step at a time, checking as you go, and wrap it in a function so it can be re-run on next month's export.

### Step 0: look before you touch

```python
import pandas as pd

raw = pd.read_csv("employees_messy.csv")
print(raw.shape)
raw.info()
print(raw.head(8))
```

Problems spotted:

1. three exact duplicate rows;
2. names with stray spaces and mixed capitals;
3. departments with stray spaces and mixed capitals (8 spellings of 4 departments);
4. salaries as text with `$` and commas, and some missing;
5. impossible ages (230 and -1) and some missing;
6. start dates as text, some missing;
7. some emails missing.

### Steps 1 to 3: duplicates and text

Work on a copy, so the raw data stays untouched for comparison:

```python
import pandas as pd

raw = pd.read_csv("employees_messy.csv")
df = raw.drop_duplicates().copy()
df["name"] = df["name"].str.strip().str.title()
df["department"] = df["department"].str.strip().str.title().replace({"Hr": "HR"})
print(len(df))
print(df["department"].value_counts())
print(df["name"].head(5).tolist())
```

### Steps 4 to 6: numbers and dates

```python
import pandas as pd

raw = pd.read_csv("employees_messy.csv")
df = raw.drop_duplicates().copy()

salary_text = df["salary"].str.replace("$", "", regex=False).str.replace(",", "", regex=False)
df["salary"] = pd.to_numeric(salary_text, errors="coerce")

df["age"] = df["age"].mask((df["age"] < 16) | (df["age"] > 100)).astype("Int64")
df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

print(df.dtypes)
print(df[["salary", "age"]].describe().round(0))
```

### Step 7: decide about the gaps

Not every gap should be filled. A guessed salary would distort pay analysis, so leave salaries missing but count them. A missing email is fine to label:

```python
import pandas as pd

raw = pd.read_csv("employees_messy.csv")
df = raw.drop_duplicates().copy()
df["email"] = df["email"].fillna("not provided")
print(df["email"].value_counts().head(3))
```

### Wrapping it in a function

Putting every step in one function makes the cleaning **repeatable**: next month you call `clean()` on the new file and get the same result, with no forgotten steps.

```python
import pandas as pd

def clean_employees(raw):
    """Return a cleaned copy of the HR export."""
    df = raw.drop_duplicates().copy()
    for col in ["name", "department"]:
        df[col] = df[col].str.strip().str.title()
    df["department"] = df["department"].replace({"Hr": "HR"})
    salary_text = df["salary"].str.replace("$", "", regex=False).str.replace(",", "", regex=False)
    df["salary"] = pd.to_numeric(salary_text, errors="coerce")
    df["age"] = df["age"].mask((df["age"] < 16) | (df["age"] > 100)).astype("Int64")
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["email"] = df["email"].fillna("not provided")
    return df.reset_index(drop=True)

clean = clean_employees(pd.read_csv("employees_messy.csv"))
print(clean.head())
print(clean.isna().sum())
```

### Check the result

Cleaning isn't done until you've checked it. `assert` statements turn your expectations into automatic tests: if one fails, you know straight away.

```python
import pandas as pd

def clean_employees(raw):
    df = raw.drop_duplicates().copy()
    for col in ["name", "department"]:
        df[col] = df[col].str.strip().str.title()
    df["department"] = df["department"].replace({"Hr": "HR"})
    salary_text = df["salary"].str.replace("$", "", regex=False).str.replace(",", "", regex=False)
    df["salary"] = pd.to_numeric(salary_text, errors="coerce")
    df["age"] = df["age"].mask((df["age"] < 16) | (df["age"] > 100)).astype("Int64")
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["email"] = df["email"].fillna("not provided")
    return df.reset_index(drop=True)

clean = clean_employees(pd.read_csv("employees_messy.csv"))
assert clean["emp_id"].is_unique, "employee ids repeat"
assert clean["department"].nunique() == 4
assert clean["age"].dropna().between(16, 100).all()
assert clean["salary"].dtype == "float64"
print("All checks passed:", clean.shape)
print(clean.groupby("department")["salary"].median())
```

Now the question "what's the median salary by department?" has a trustworthy answer.

### Saving the clean data

`to_csv` writes a DataFrame to a file. `index=False` leaves out the 0, 1, 2… index column:

```python
import pandas as pd

df = pd.read_csv("employees_messy.csv").drop_duplicates()
df.to_csv("employees_clean.csv", index=False)
print(open("employees_clean.csv").read()[:200])
```

:::exercise Write the cleaner
Write a function `clean_employees(raw)` that takes the raw DataFrame and returns a cleaned copy where:

1. exact duplicate rows are removed and the index is reset (`reset_index(drop=True)`);
2. `name` and `department` are stripped and in title case;
3. `salary` is a number (`$` and commas removed, `errors="coerce"`);
4. ages below 16 or above 100 are missing.

Then store `clean_employees(pd.read_csv("employees_messy.csv"))` in `clean`.
```python starter
import pandas as pd

def clean_employees(raw):
    df = raw.copy()
    # your steps here
    return df

clean = clean_employees(pd.read_csv("employees_messy.csv"))
print(clean.head())
```
```python check
import pandas as pd
raw = pd.read_csv("employees_messy.csv")
e = raw.drop_duplicates().copy()
for c in ["name", "department"]:
    e[c] = e[c].str.strip().str.title()
e["salary"] = pd.to_numeric(e["salary"].str.replace("$", "", regex=False).str.replace(",", "", regex=False), errors="coerce")
e["age"] = e["age"].mask((e["age"] < 16) | (e["age"] > 100))
e = e.reset_index(drop=True)
got = need("clean", pd.DataFrame)
assert len(got) == len(e), f"clean should have {len(e)} rows (duplicates removed), but has {len(got)}."
same(got["name"], e["name"], "clean['name']")
same(got["department"].replace({"HR": "Hr"}), e["department"], "clean['department']")
same(got["salary"].astype(float), e["salary"], "clean['salary']")
same(got["age"].astype(float), e["age"].astype(float), "clean['age']")
f = need("clean_employees")
again = f(raw)
assert len(again) == len(e), "Calling clean_employees on the raw data again should give the same result."
```
```python solution
import pandas as pd

def clean_employees(raw):
    df = raw.drop_duplicates().copy()
    for col in ["name", "department"]:
        df[col] = df[col].str.strip().str.title()
    salary_text = df["salary"].str.replace("$", "", regex=False).str.replace(",", "", regex=False)
    df["salary"] = pd.to_numeric(salary_text, errors="coerce")
    df["age"] = df["age"].mask((df["age"] < 16) | (df["age"] > 100))
    return df.reset_index(drop=True)

clean = clean_employees(pd.read_csv("employees_messy.csv"))
print(clean.head())
```
hint: Copy the steps from the lesson into the function, one per line, and finish with `return df.reset_index(drop=True)`.
:::

:::exercise Pay by department
Using your cleaned data (copy your `clean_employees` function in), store the **median salary for each department** in `median_pay` (a Series indexed by department), using `groupby("department")["salary"].median()`.
```python starter
import pandas as pd

# paste your clean_employees function here

```
```python check
import pandas as pd
raw = pd.read_csv("employees_messy.csv")
e = raw.drop_duplicates().copy()
e["department"] = e["department"].str.strip().str.title()
e["salary"] = pd.to_numeric(e["salary"].str.replace("$", "", regex=False).str.replace(",", "", regex=False), errors="coerce")
exp = e.groupby("department")["salary"].median()
got = need("median_pay", pd.Series).rename(index={"HR": "Hr"})
same(got.astype(float).sort_index(), exp.sort_index(), "median_pay")
```
```python solution
import pandas as pd

def clean_employees(raw):
    df = raw.drop_duplicates().copy()
    for col in ["name", "department"]:
        df[col] = df[col].str.strip().str.title()
    salary_text = df["salary"].str.replace("$", "", regex=False).str.replace(",", "", regex=False)
    df["salary"] = pd.to_numeric(salary_text, errors="coerce")
    df["age"] = df["age"].mask((df["age"] < 16) | (df["age"] > 100))
    return df.reset_index(drop=True)

clean = clean_employees(pd.read_csv("employees_messy.csv"))
median_pay = clean.groupby("department")["salary"].median()
print(median_pay)
```
hint: The departments must be cleaned first, or "Sales" and "SALES" become separate groups.
:::

:::quiz
? Why wrap the cleaning steps in a function?
- Functions run faster
+ So the same cleaning can be re-run on new data, with no steps forgotten
- pandas requires it
= A cleaning function is repeatable and testable: next month's file gets exactly the same treatment.
? Why were missing salaries left missing instead of filled?
+ A guessed salary would distort the pay analysis
- pandas can't fill numbers
- Because there were too many of them
= Filling with a typical value makes the data look more certain than it is. Leave it, count it and mention it.
? What does `df.to_csv("out.csv", index=False)` leave out?
- The header row
+ The row index (0, 1, 2…)
- Missing values
= Without `index=False`, the index is written as an extra unnamed first column.
:::
