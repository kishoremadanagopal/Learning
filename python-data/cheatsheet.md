# Python for Data cheat sheet

Everything from the course on one page. The number in brackets is the lesson where it's taught.

## Files and JSON (plain Python)

```python
with open("file.txt") as f:          text = f.read()                         # [2]
with open("out.txt", "w") as f:      f.write("hello\n")                      # [2]
import csv
rows = list(csv.DictReader(open("sales.csv")))   # one dict per row, values are text   [2]
import json
data = json.loads(text)      text = json.dumps(data, indent=2)               # [3]
data = json.load(f)          json.dump(data, f, indent=2)                    # [3]
from collections import Counter
Counter(values).most_common(3)                                               # [4]
```

## NumPy

```python
import numpy as np
a = np.array([1, 2, 3])      a.shape  a.ndim  a.dtype  a.astype(float)       # [5]
np.arange(0, 10, 2)   np.linspace(0, 1, 5)   np.zeros((2, 3))   np.ones(4)   # [5]
a[0]  a[-1]  a[1:4]  m[row, col]  m[:, 0]                                    # [6]
a[a > 5]   a[(a > 5) & (a < 9)]   (a > 5).sum()   b = a.copy()               # [6]
a * 2   a + b   np.sqrt(a)   np.round(a, 2)   np.where(a > 0, a, 0)          # [7]
np.nan   np.isnan(a)   np.nanmean(a)                                         # [7]
a.sum()  a.mean()  np.median(a)  a.std()  a.argmax()  np.percentile(a, 90)   # [8]
m.mean(axis=0)   # per column        m.sum(axis=1)   # per row               # [8]
a.cumsum()   a.reshape(2, -1)                                                # [8]
rng = np.random.default_rng(42)                                              # [9]
rng.integers(1, 7, size=10)  rng.random(3)  rng.normal(170, 8, 1000)         # [9]
rng.choice(items, size=5)    rng.permutation(items)                          # [9]
```

## pandas: load and look

```python
import pandas as pd
s = pd.Series([1, 2], index=["a", "b"])      s.value_counts()  s.idxmax()    # [10]
df = pd.read_csv("sales.csv")      pd.read_json("movies.json")               # [11]
df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})                            # [11]
df.head()  df.tail()  df.shape  df.columns  df.dtypes  df.info()             # [11]
df.describe()   df.describe(include="all")                                   # [11]
```

## Select, filter, sort

```python
df["col"]   df[["a", "b"]]                                                   # [12]
df.loc[label, "col"]   df.loc[0:3, ["a", "b"]]   # labels, end included      # [12]
df.iloc[0, 2]   df.iloc[:5, :3]                  # positions, end excluded   # [12]
df.set_index("id")   df.reset_index()   df.loc[3, "price"] = 9.5             # [12]
df[df["units"] > 5]                                                          # [13]
df[(df["a"] > 1) & (df["b"] == "x")]   df[~mask]   df[df["c"].isin(["p", "q"])]   # [13]
df[df["score"].between(60, 75)]   df.query("region == 'West' and price > @limit")  # [13]
df.sort_values("col", ascending=False)   df.sort_values(["a", "b"])          # [14]
df.nlargest(5, "col")                                                        # [14]
df["rev"] = df["units"] * df["price"]   df.assign(rev=lambda d: d.units * d.price)   # [14]
df.rename(columns={"old": "new"})   df.drop(columns=["col"])                 # [14]
```

## Summarise

```python
df["col"].sum()  .mean()  .median()  .min()  .max()  .count()  .nunique()    # [15]
df["col"].agg(["mean", "max"])   df["col"].value_counts(normalize=True)      # [15]
(df["score"] >= 50).mean()      # share of rows that are True                # [15]
f"{x:,.2f}"   f"{share:.0%}"                                                 # [15]
```

## Clean

```python
df.isna().sum()   df.dropna(subset=["col"])   df["col"].fillna(0)            # [16]
df.groupby("g")["col"].ffill()   pd.read_csv(f, na_values=["-", "n/a"])      # [16]
df["col"].astype(int)   pd.to_numeric(s, errors="coerce")   .astype("Int64") # [17]
s.str.replace("$", "", regex=False)   pd.read_csv(f, dtype={"zip": str})    # [17]
s.str.strip().str.lower().str.title()   s.replace({"U.K.": "UK"})            # [18]
s.str.contains("x", case=False, na=False)   s.str.split("@").str[1]          # [18]
s.str.extract(r"(\d+)")                                                      # [18]
df.duplicated().sum()   df.drop_duplicates(subset=["id"], keep="last")       # [19]
s.mask((s < 0) | (s > 100))   s.clip(0, 100)   s.quantile([0.25, 0.75])      # [19]
pd.to_datetime(s)   pd.read_csv(f, parse_dates=["date"])                     # [20]
s.dt.year  .dt.month  .dt.day_name()  .dt.quarter  .dt.strftime("%d %b %Y")  # [20]
(end - start).dt.days   date + pd.Timedelta(days=5)   pd.DateOffset(months=1)  # [20]
df.to_csv("clean.csv", index=False)                                          # [21]
```

## Analyse

```python
df.groupby("g")["col"].sum()                                                 # [22]
df.groupby("g").agg(orders=("id", "count"), revenue=("rev", "sum"))          # [22]
df.groupby(["a", "b"])["col"].sum().reset_index()                            # [22]
df.groupby("g")["col"].transform("mean")    # group value on every row       # [22]
df.pivot_table(index="r", columns="c", values="v", aggfunc="sum", fill_value=0, margins=True)  # [23]
pd.crosstab(df["a"], df["b"], normalize="index")                             # [23]
a.merge(b, on="key", how="left", indicator=True, validate="many_to_one")     # [24]
pd.concat([a, b], ignore_index=True)                                         # [25]
df.melt(id_vars="id", var_name="var", value_name="val")                      # [25]
df.pivot(index="date", columns="city", values="temp")   s.unstack()          # [25]
s.map({"N": "North"})   s.apply(func)   df.apply(func, axis=1)               # [26]
np.select([c1, c2], ["A", "B"], default="C")                                 # [26]
pd.cut(s, bins=[0, 50, 100], labels=["low", "high"])   pd.qcut(s, q=4)       # [26]
s.resample("ME").sum()    # "D" "W" "ME" "QE" "YE"                           # [27]
s.shift(1)   s.pct_change()   s.rolling(7).mean()   s.cumsum()               # [27]
```

| Join | Keeps |
|---|---|
| `how="inner"` | rows that match in both [24] |
| `how="left"` | every row of the left table [24] |
| `how="outer"` | every row of both [24] |

## Charts

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(7, 4))                                       # [28]
ax.plot(x, y, marker="o", label="name")   ax.legend()                        # [28]
ax.set_title("The finding")  ax.set_xlabel("x (units)")  ax.set_ylabel("y")  # [28]
fig.savefig("chart.png", dpi=150, bbox_inches="tight")   plt.show()          # [28]
ax.bar(cats, vals)   ax.barh(cats, vals)   ax.bar_label(bars)                # [29]
ax.hist(values, bins=20)   ax.scatter(x, y, alpha=0.7)   ax.boxplot([a, b])  # [29]
s.plot()  s.plot.bar()  s.plot.barh()  s.plot.hist(bins=20)  df.plot.scatter(x="a", y="b")  # [30]
fig, axes = plt.subplots(1, 3, sharey=True)   s.plot(ax=axes[0])   fig.tight_layout()  # [30]
ax.spines[["top", "right"]].set_visible(False)                               # [30]
```

| Question | Chart |
|---|---|
| change over time | line [28] |
| compare categories | bar (sorted) [29] |
| how values are spread | histogram or box plot [29] |
| are two numbers related? | scatter [29] |
