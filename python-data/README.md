# Learn Python for Data: NumPy, pandas and charts

A hands-on course that takes you from "I know a little Python" to cleaning, analysing and charting real data: 31 lessons on NumPy, pandas and matplotlib, with a practice sandbox that runs real pandas in your browser and checks your answers.

This is the shared core for both the **AI engineer** and the **data / AI analyst** paths: every one of those jobs loads, cleans, summarises and charts data first.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/learning/python-data/)

The sandbox runs real Python 3.14 with NumPy, pandas and matplotlib inside your browser (via [Pyodide](https://pyodide.org)). Nothing to install, no sign-up.

- every lesson, with **227 examples** you can run and change
- **62 exercises**, numbered by lesson, that check your code and tell you what's off
- **93 quiz questions**, with explanations
- **7 practice datasets** that load with one line, like `pd.read_csv("sales.csv")`
- charts drawn right under your code
- your progress and code saved in your own browser

**Before you start:** you should know Python basics: variables, lists, dictionaries, loops, `if` and functions. If you don't yet, do lessons 1 to 20 of [Learn Python from scratch](../python/) first.

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 31 lessons, each with key terms, examples, common mistakes, exercises, answers and a quiz |
| 📖 [Glossary](glossary.md) | every data term used in the course, defined in plain English |
| 🧾 [Cheat sheet](cheatsheet.md) | NumPy, pandas and matplotlib on one page, with lesson numbers |
| 🗂️ [Datasets](https://github.com/kishoremadanagopal/learning/tree/main/python-data/data) | the practice files, to download and use on your own computer |

## How to use this course

1. Read a lesson, here on GitHub or in the sandbox. Start with its **Key terms**.
2. Run the examples in the sandbox and change them to see what happens.
3. Do the lesson's exercises in the sandbox and press **Check**.
4. Only then open the **Answers** section at the bottom of the lesson.

## Lessons

### Part 1: Data with Plain Python (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 1 | [What data analysis is](lessons/01-what-is-data-analysis.md) | the analysis workflow, rows and columns, CSV files, NumPy, pandas and matplotlib | 1–2 |
| 2 | [Reading and writing files](lessons/02-files-and-csv.md) | `open()`, `with`, reading lines, `csv.DictReader`, writing text and CSV files | 3–4 |
| 3 | [JSON data](lessons/03-json-data.md) | JSON syntax, `json.loads`, `json.dumps`, `json.load`, `json.dump`, nested data, `.get()` | 5–6 |
| 4 | [Crunching data with plain Python](lessons/04-crunching-with-python.md) | filtering with comprehensions, `sum()`, `Counter`, grouping with a dictionary, ranking with `sorted(key=...)` | 7–8 |

### Part 2: NumPy (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 5 | [NumPy arrays](lessons/05-numpy-arrays.md) | `np.array`, vectorised maths, speed, `shape`, `ndim`, `dtype`, `arange`, `linspace`, `zeros`, `ones` | 9–10 |
| 6 | [Indexing, slicing and filtering arrays](lessons/06-array-indexing.md) | indexing and slicing, `arr[row, col]`, boolean masks, `&`, `\|`, `~`, fancy indexing, views and copies | 11–12 |
| 7 | [Maths on whole arrays](lessons/07-vectorised-math.md) | array-with-array maths, broadcasting, ufuncs, `np.where`, `np.nan`, `np.isnan`, scaling | 13–14 |
| 8 | [Summarising arrays](lessons/08-array-statistics.md) | `sum`, `mean`, `median`, `std`, `percentile`, `argmax`, `axis`, `cumsum`, `reshape`, `np.loadtxt` | 15–16 |
| 9 | [Random numbers and simulation](lessons/09-random-and-simulation.md) | `default_rng`, seeds, `integers`, `random`, `normal`, `choice`, `permutation`, `binomial`, simulation | 17–18 |

### Part 3: pandas Foundations (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 10 | [The Series](lessons/10-pandas-series.md) | `pd.Series`, the index, label alignment, `value_counts`, `unique`, `nunique`, `idxmax` | 19–20 |
| 11 | [DataFrames and loading data](lessons/11-dataframes.md) | `pd.DataFrame`, `read_csv`, `read_json`, `head`, `tail`, `shape`, `columns`, `dtypes`, `info`, `describe` | 21–22 |
| 12 | [Selecting columns and rows](lessons/12-selecting-data.md) | `df["col"]`, `df[["a", "b"]]`, `loc`, `iloc`, `set_index`, `reset_index`, changing cells | 23–24 |
| 13 | [Filtering rows](lessons/13-filtering-rows.md) | boolean masks, `&`, `\|`, `~`, `isin`, `between`, filtering text and dates, `query`, `loc` with a mask | 25–26 |
| 14 | [Sorting and adding columns](lessons/14-sorting-and-new-columns.md) | `sort_values`, `nlargest`, new calculated columns, `np.where`, `assign`, method chains, `rename`, `drop` | 27–28 |
| 15 | [Summarising a whole table](lessons/15-summarising-data.md) | `sum`, `mean`, `median`, `agg`, `count`, `nunique`, `value_counts(normalize=True)`, `idxmax`, formatting with `:,` and `:%` | 29–30 |

### Part 4: Cleaning Data (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 16 | [Missing values](lessons/16-missing-values.md) | `isna`, `notna`, `dropna`, `fillna`, forward fill, flagging gaps, `na_values` | 31–32 |
| 17 | [Fixing data types](lessons/17-data-types.md) | `dtypes`, `astype`, `pd.to_numeric`, `errors="coerce"`, cleaning text into numbers, `Int64`, `dtype=` on load, categories | 33–34 |
| 18 | [Cleaning text](lessons/18-text-cleaning.md) | `.str` methods, `strip`, `lower`, `title`, `replace` vs `.str.replace`, `contains`, `split`, `extract`, `na=False` | 35–36 |
| 19 | [Duplicates and impossible values](lessons/19-duplicates-and-outliers.md) | `duplicated`, `drop_duplicates`, `subset` and `keep`, impossible values, `mask`, `clip`, the IQR rule | 37–38 |
| 20 | [Dates and times](lessons/20-dates-and-times.md) | `pd.to_datetime`, `parse_dates`, the `.dt` accessor, filtering by date, `Timedelta`, `DateOffset`, `strftime`, `dayfirst` | 39–40 |
| 21 | [Project: clean an HR export](lessons/21-cleaning-project.md) | a full cleaning workflow, working on a copy, cleaning functions, `assert` checks, `to_csv` | 41–42 |

### Part 5: Analysing Data (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 22 | [Grouping and aggregating](lessons/22-groupby.md) | split-apply-combine, `groupby`, `size`, named aggregation with `agg`, grouping by several columns, `reset_index`, `transform` | 43–44 |
| 23 | [Pivot tables and crosstabs](lessons/23-pivot-tables.md) | `pivot_table`, `index`, `columns`, `values`, `aggfunc`, `margins`, `fill_value`, `pd.crosstab`, `normalize` | 45–46 |
| 24 | [Combining tables with merge](lessons/24-merging-tables.md) | `merge`, `on`, `how` (inner, left, right, outer), `indicator`, `left_on`/`right_on`, `suffixes`, `validate` | 47–48 |
| 25 | [Stacking and reshaping tables](lessons/25-reshaping-data.md) | `pd.concat`, `ignore_index`, wide vs long (tidy) data, `melt`, `pivot`, `unstack` | 49–50 |
| 26 | [Mapping, applying and binning](lessons/26-map-apply-and-bins.md) | `map` with a dictionary, `apply` with functions and lambdas, `apply(axis=1)`, `np.select`, `pd.cut`, `pd.qcut` | 51–52 |
| 27 | [Trends over time](lessons/27-time-series.md) | date index, partial-date selection, `resample`, period codes, `shift`, `pct_change`, `rolling`, `cumsum`, groupby + resample | 53–54 |

### Part 6: Charts and a Final Project (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 28 | [Your first charts with matplotlib](lessons/28-matplotlib-basics.md) | figure and axes, `plt.subplots`, `ax.plot`, titles and labels, legends, `figsize`, styling, `savefig` | 55–56 |
| 29 | [Choosing the right chart](lessons/29-chart-types.md) | bar and horizontal bar charts, `bar_label`, histograms, scatter plots, box plots, why to avoid pie charts | 57–58 |
| 30 | [Charts straight from pandas](lessons/30-pandas-plotting.md) | `Series.plot`, `kind=` and `.plot.bar()`-style shortcuts, plotting DataFrames, `plt.subplots(rows, cols)`, `ax=`, `sharey`, chart design habits | 59–60 |
| 31 | [Final project: a sales analysis](lessons/31-final-project.md) | turning a brief into questions, joining and checking data, headline numbers, profit analysis, a dashboard, writing up findings, saving results | 61–62 |

## The practice datasets

| File | Rows | What's in it |
|---|---|---|
| [`sales.csv`](data/sales.csv) | 600 | 600 orders from 2025: date, customer, region, product, units and price. |
| [`customers.csv`](data/customers.csv) | 120 | 120 customers: name, city, segment, age and signup date. |
| [`products.csv`](data/products.csv) | 8 | 8 products with category, price, cost and supplier. |
| [`employees_messy.csv`](data/employees_messy.csv) | 40 | An HR export full of problems to clean: stray spaces, mixed capitals, text salaries, gaps and duplicates. |
| [`weather.csv`](data/weather.csv) | 1095 | Daily temperature and rain for London, Mumbai and New York in 2025. |
| [`students.csv`](data/students.csv) | 60 | 60 students: class, hours studied, attendance and exam scores. |
| [`movies.json`](data/movies.json) | 40 | 40 (made-up) films: year, genre, runtime, rating and box office. |

All of the data is made up for practice, so it's safe to share and experiment with.

## Running it on your own computer

Everything in the course also works in a normal Python setup. Install Python from [python.org](https://www.python.org/), then:

```bash
pip install numpy pandas matplotlib jupyterlab
jupyter lab
```

Download the files from [`data/`](data/) into the same folder as your notebook. The sandbox runs pandas 3, so if your computer has an older pandas, upgrade with `pip install --upgrade pandas`.

## Editing the course

Lessons are generated from the Markdown sources in [`course/`](course/). See [course/README.md](course/README.md).
