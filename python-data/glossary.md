# Python for Data glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **& \| ~** | "and", "or" and "not" for masks. [13] |
| **agg** | Applies one or more summaries at once, like `agg(["mean", "max"])`. [15] |
| **aggfunc** | The summary a pivot table uses, such as "sum" or "mean". [23] |
| **Aggregate** | A single number that summarises many, such as a sum, count or average. [4] |
| **API** | A way for programs to talk to each other over the internet, usually sending JSON. [3] |
| **apply** | Runs a function on every value of a Series, or every row with `axis=1`. [26] |
| **ascending** | The sort direction; `ascending=False` puts the largest first. [14] |
| **assert** | A statement that stops with an error if a condition isn't true, used as an automatic check. [21] |
| **assign** | Returns a copy of the table with new columns added. [14] |
| **astype** | Converts a column to another type; fails if any value can't be converted. [17] |
| **Axes** | One chart area inside a figure, with its own x and y axes. You draw on it with `ax.` methods. [28] |
| **axis** | Which direction to summarise: `axis=0` down the columns, `axis=1` across the rows. [8] |
| **Bar chart** | Bars whose lengths compare values across categories. [29] |
| **between** | True where a value lies within a range (both ends included). [13] |
| **Bin** | A range of values grouped together, like ages 30–44. [26] |
| **Boolean mask** | An array of `True`/`False` values used to pick items. [6, 13] |
| **Box plot** | A summary of a distribution: median, quartiles, typical range and outliers. [29] |
| **Brief** | The request that starts an analysis, often vague. [31] |
| **Broadcasting** | NumPy stretching a smaller array (or a single number) to match a bigger one. [7] |
| **Calculated column** | A new column built from other columns, like revenue = units × price. [14] |
| **Categorical** | A type for a column with a few repeating values, optionally in a set order. [17] |
| **Causation** | One thing actually causing another. Correlation alone doesn't show it. [29] |
| **Chart clutter** | Anything on a chart that doesn't help the reader, like heavy grids or 3-D effects. [30] |
| **Cleaning pipeline** | The ordered steps that turn raw data into clean data. [21] |
| **clip** | Caps values at a lower and upper limit. [19] |
| **Coerce** | Force a conversion, replacing what can't be converted with a missing value. [17] |
| **Column (field)** | One fact recorded for every row, such as the price or the date. [1] |
| **concat** | Stacks tables on top of each other (or side by side with `axis=1`). [25] |
| **copy()** | Makes an independent array that doesn't share data. [6] |
| **Copy-on-write** | Pandas 3's rule that a selection behaves like a copy, so changing it never changes the original table. [12] |
| **Correlation** | Two variables tending to rise or fall together. [29] |
| **count** | The number of values that aren't missing. [15] |
| **Counter** | A dictionary from `collections` that counts things and can add up amounts. [4] |
| **Crosstab** | A table counting how often each combination of two categories occurs. [23] |
| **CSV (comma-separated values)** | A plain-text table with one row per line and commas between the columns. [1] |
| **csv.DictReader** | Reads a CSV file as one dictionary per row, keyed by the header names. [2] |
| **csv.DictWriter** | Writes dictionaries out as CSV rows. [2] |
| **csv module** | Python's built-in tool for reading and writing CSV files correctly, including quoted values. [2] |
| **cumsum** | A running total. [8] |
| **Dashboard** | A few related charts shown together to answer a set of questions. [31] |
| **Data analysis** | Answering questions by loading, cleaning, summarising and charting data. [1] |
| **DataFrame** | A table of rows and named columns; each column is a Series. [11] |
| **Data quality check** | A test that the cleaned data meets your expectations. [21] |
| **DateOffset** | A calendar step such as one month, which respects different month lengths. [20] |
| **datetime64** | Pandas' type for dates and times. [20] |
| **DatetimeIndex** | An index made of dates, which unlocks time-based selection and resampling. [27] |
| **describe()** | Summary statistics for each number column. [11] |
| **df.plot** | Pandas' built-in charting, which draws with matplotlib. [30] |
| **Distribution** | How likely each possible value is. [9, 29] |
| **drop_duplicates** | Removes repeated rows; `subset=` checks only some columns, `keep=` chooses which copy stays. [19] |
| **dropna** | Removes rows (or columns) with missing values. [16] |
| **.dt accessor** | Gives a date column its parts and methods, like `.dt.month`. [20] |
| **dtype** | The data type shared by every item in an array, such as `int64` or `float64`. [5] |
| **dtypes** | The data type of each column. [11] |
| **Duplicate** | A row that repeats another, completely or by its key. [19] |
| **Element-wise** | Done item by item, matching positions in two arrays. [7] |
| **Fancy indexing** | Selecting items with a list of positions, like `a[[0, 3]]`. [6] |
| **figsize** | The figure's (width, height) in inches. [28] |
| **Figure** | The whole image, which can hold one or more charts. [28] |
| **FileNotFoundError** | The error raised when a file name doesn't exist. [2] |
| **File path** | The name (and folder) of a file, like `"sales.csv"`. [2] |
| **fillna** | Replaces missing values with something you choose. [16] |
| **fill_value** | What to show where a combination has no data. [23] |
| **Filter** | Keep only the rows that match a condition. [4, 13] |
| **Format code** | Instructions inside an f-string's `{}` that control how a number looks, like `:,.2f` or `:.0%`. [15] |
| **Forward fill (ffill)** | Filling a gap with the previous value, common for time series. [16] |
| **Generator expression** | A comprehension in round brackets, like `sum(x for x in items)`, that produces values one at a time. [4] |
| **Group** | Split rows by the values of a column, then summarise each part. [4] |
| **groupby** | Splits a table into groups by a column's values so each group can be summarised. [22] |
| **Grouped bar chart** | Bars for several series side by side, one group per category. [30] |
| **Header** | The first line of a CSV file, which names the columns. [1] |
| **head / tail** | The first / last rows of a table (5 by default). [11] |
| **Histogram** | Bars counting how many values fall in each range (bin), showing a distribution's shape. [29] |
| **idxmax / idxmin** | The label of the largest / smallest value. [10] |
| **iloc** | Selects rows and columns by position (integers); slices exclude the end. [12] |
| **Impossible value** | A value that can't be true, like a negative age. [19] |
| **Imputation** | Filling missing values with an estimate, such as the median. [16] |
| **Index** | The position of an item, starting at 0. [6, 10] |
| **indicator** | Adds a `_merge` column showing whether each row matched. [24] |
| **info()** | A summary of columns, types and non-missing counts. [11] |
| **Inner join** | Keeps only rows that match in both tables. [24] |
| **IQR (interquartile range)** | The third quartile minus the first: the spread of the middle half of the data. [19] |
| **isin** | True where a value is one of a given list. [13] |
| **isna / notna** | True where a value is missing / present. [16] |
| **Join (merge)** | Combining two tables by matching rows on a key. [24] |
| **JSON** | A text format for structured data made of objects, arrays, strings, numbers, `true`/`false` and `null`. [3] |
| **JSON array** | An ordered list of values in `[ ]`, which becomes a Python list. [3] |
| **json.load / json.dump** | The same, but reading from or writing to a file. [3] |
| **json.loads / json.dumps** | Convert JSON text to Python objects, and Python objects to JSON text. [3] |
| **JSON object** | A set of key-value pairs in `{ }`, which becomes a Python dictionary. [3] |
| **Jupyter notebook** | A document of code cells and their results, the usual way analysts run Python. [1] |
| **Key** | A column that should uniquely identify each row, such as an order ID. [19, 24] |
| **KeyError** | The error raised when a column or label doesn't exist. [12] |
| **Label alignment** | Pandas matching values by index label, not position, when combining Series. [10] |
| **lambda** | A tiny unnamed function, like `lambda p: p[1]`, often used as a sort key. [4] |
| **Left join** | Keeps every row of the left table, with gaps where there's no match. [24] |
| **Legend** | The key that says which line or colour is which. [28] |
| **Library (package)** | A collection of ready-made code you import, such as pandas. [1] |
| **Line chart** | Points joined by lines, best for change over time. [28] |
| **List comprehension** | `[x for x in items if condition]`, a one-line way to build a filtered list. [4] |
| **loc** | Selects rows and columns by label; slices include the end. [12] |
| **Long (tidy) data** | One row per thing per measurement, with a column naming the measurement. [25] |
| **map** | Replaces each value using a dictionary (or function). [26] |
| **Margin** | Profit as a percentage of revenue. [31] |
| **Margins** | Total rows and columns added to a pivot table. [23] |
| **mask** | Replaces values with missing where a condition is True. [19] |
| **matplotlib** | The library for drawing charts. [1, 28] |
| **Mean** | The average: the total divided by the number of values. [8] |
| **Median** | The middle value when the values are sorted. [8] |
| **melt** | Turns columns into rows (wide to long). [25] |
| **Method chain** | Several methods called one after another, each on the previous result. [14] |
| **Missing value** | A gap in the data, shown as `NaN`, `None` or `<NA>`. [16] |
| **Mode** | How a file is opened: `"r"` read (the default), `"w"` write (replaces), `"a"` append. [2] |
| **MultiIndex** | An index with more than one level, as you get when grouping by two columns. [22] |
| **Named aggregation** | `agg(new_name=("column", "summary"))`, which names each result column. [22] |
| **NaN** | "not a number", the marker pandas shows for a missing value. [10] |
| **na_values** | Tells `read_csv` which extra strings (like `"-"`) mean missing. [16] |
| **ndim** | The number of dimensions: 1 for a row of numbers, 2 for a table. [5] |
| **Nested data** | Values inside values, such as a list of items inside an order. [3] |
| **Newline character** | The invisible `\n` at the end of each line of a file. [2] |
| **nlargest / nsmallest** | The top / bottom n rows by a column. [14] |
| **Non-null count** | How many values in a column are present (not missing). [11] |
| **Normal distribution** | The bell curve: values cluster around the mean, with fewer far away. [9] |
| **normalize** | Turns counts into shares, by row (`"index"`), column (`"columns"`) or overall (`True`). [23] |
| **np.arange** | Makes evenly spaced numbers, like `range()`. [5] |
| **np.linspace** | Makes a set number of evenly spaced values between two ends. [5] |
| **np.nan** | "not a number", NumPy's marker for a missing value. [6] |
| **np.nanmean** | An average that skips missing (`nan`) values. [7] |
| **np.select** | Chooses a result from several conditions, first match wins. [26] |
| **np.where** | Chooses between two values item by item based on a condition. [7] |
| **null** | JSON's "no value", which becomes Python's `None`. [3] |
| **Nullable integer (Int64)** | A whole-number type that can also hold missing values. [17] |
| **NumPy** | The library for fast maths on whole arrays of numbers. [1] |
| **NumPy array (ndarray)** | A grid of numbers that all share one type, built for fast maths. [5] |
| **One-to-many** | One row on one side matches many on the other, like one customer to many orders. [24] |
| **Outer join** | Keeps every row from both tables. [24] |
| **Outlier** | A value far from the others, which may be an error or genuinely unusual. [19] |
| **pandas** | The library for working with tables of data. [1] |
| **parse_dates** | Converts date columns while loading with `read_csv`. [20] |
| **pct_change** | The change from the previous value as a fraction. [27] |
| **pd.cut** | Sorts numbers into bins with edges you choose. [26] |
| **pd.qcut** | Sorts numbers into bins holding roughly equal numbers of rows. [26] |
| **pd.read_csv / pd.read_json** | Load a CSV or JSON file into a DataFrame. [11] |
| **pd.to_datetime** | Converts text to dates. [20] |
| **pd.to_numeric** | Converts values to numbers; `errors="coerce"` turns failures into missing values. [17] |
| **Percentage** | A share multiplied by 100. [15] |
| **Percentile** | The value below which a given percentage of the data falls. [8] |
| **pivot** | Turns rows into columns (long to wide). [25] |
| **Pivot table** | A summary grid with one category down the side, another across the top, and a number in each cell. [23] |
| **plt.subplots** | Creates a figure and its axes in one call. [28] |
| **Profit** | Revenue minus cost. [31] |
| **Quantile** | The value below which a given share of the data falls (the 0.25 quantile is the first quartile). [26] |
| **Quartiles** | The 25th, 50th and 75th percentiles. [8] |
| **query** | Filters rows using a condition written as text. [13] |
| **Random generator** | An object, made with `np.random.default_rng()`, that produces random numbers. [9] |
| **Raw data** | The data exactly as it arrived, kept unchanged for reference. [21] |
| **regex=False** | Tells `.str.replace` to treat the search text literally, not as a pattern. [17] |
| **Regular expression (regex)** | A pattern for matching text, like `\d+` for "one or more digits". [18] |
| **rename / drop** | Change column names / remove columns. [14] |
| **Reproducible** | Giving the same result every time it's run on the same input. [21] |
| **resample** | Groups a time series into periods such as weeks or months. [27] |
| **reset_index** | Turns the index back into a normal column. [12] |
| **reshape** | Rearranging an array's values into a new shape with the same total size. [8] |
| **Revenue** | Money from sales: units × price. [31] |
| **Rolling (moving) average** | The average over a sliding window, such as the last 7 days. [27] |
| **Row (record)** | One thing being described, such as one order or one day. [1] |
| **savefig** | Writes a figure to an image file. [28] |
| **Scaling (normalising)** | Rescaling numbers to a common range such as 0 to 1. [7] |
| **Scatter plot** | One dot per row, placed by two numbers, to show whether they're related. [29] |
| **Seasonality** | A pattern that repeats at the same time each year. [31] |
| **Seed** | A starting number that makes a generator produce the same sequence every run. [9] |
| **Selection** | Picking particular rows, columns or cells from a table. [12] |
| **Series** | A one-dimensional column of values, each with a label. [10] |
| **set_index** | Makes a column the row labels. [12] |
| **Shape** | The size of an array along each dimension, like `(3, 4)` for 3 rows and 4 columns. [5, 11] |
| **Share (proportion)** | A part divided by the whole, between 0 and 1. [15] |
| **sharey** | Makes every subplot use the same y-axis scale. [30] |
| **shift** | Moves values down (or up) by a number of steps, to compare with earlier periods. [27] |
| **Simulation** | Answering a question by acting it out many times with random numbers and counting. [9] |
| **size()** | The number of rows in each group. [22] |
| **Slice** | A range of positions, like `a[2:5]`. [6] |
| **sort_values** | Sorts rows by one or more columns. [14] |
| **Split-apply-combine** | The three steps of grouping: split into groups, summarise each, combine the answers. [22] |
| **Stacked bar chart** | Series stacked on top of each other in one bar. [30] |
| **Standard deviation (std)** | A measure of how spread out values are around the mean. [8] |
| **Standardise** | Make values that mean the same thing look the same. [18] |
| **.str accessor** | Gives a text column all the string methods, applied to every value. [18] |
| **str.contains** | True where the text includes a substring. [18] |
| **str.extract** | Pulls out the part of each value that matches a pattern. [18] |
| **strftime** | Formats dates as text using codes like `%Y-%m-%d`. [20] |
| **strip** | Removes spaces (and newlines) from both ends of text. [18] |
| **str.split** | Breaks text into parts at a separator. [18] |
| **Subplots** | Several charts arranged in a grid in one figure. [30] |
| **Summary statistic** | One number describing many, such as a total, average or count. [15] |
| **Tabular data** | Data arranged as a table of rows and columns. [1] |
| **tight_layout** | Adjusts spacing so labels don't overlap. [30] |
| **Timedelta** | A length of time, the result of subtracting dates. [20] |
| **Time series** | A measurement recorded over time, like daily sales. [27] |
| **Timestamp** | A single date and time, like `pd.Timestamp("2026-01-01")`. [20] |
| **title case** | Each Word Starting With A Capital. [18] |
| **to_csv** | Writes a DataFrame to a CSV file; `index=False` leaves out the index. [21] |
| **Train/test split** | Dividing data so a model learns from one part and is tested on the other. [9] |
| **transform** | A group summary repeated on every row of that group. [22] |
| **ufunc (universal function)** | A fast NumPy function that works on every item, like `np.sqrt`. [7] |
| **Uniform distribution** | Every value in a range is equally likely. [9] |
| **unique / nunique** | The distinct values, and how many there are. [10] |
| **unstack** | Moves an index level into the columns. [25] |
| **value_counts** | Counts how often each distinct value appears, most common first. [10] |
| **Vectorisation** | Doing an operation on every item of an array at once, without a loop. [5] |
| **View** | A slice that shares data with the original array, so changes show up in both. [6] |
| **Wide data** | One row per thing, with a column for each measurement. [25] |
| **with block** | `with open(...) as f:` opens a file and closes it automatically afterwards. [2] |
| **Write-up** | A short plain-language summary of findings and recommendations. [31] |
| **Year to date (YTD)** | The running total from the start of the year. [27] |
