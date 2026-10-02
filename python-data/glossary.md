# Python for Data glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **Aggregate** | A single number that summarises many, such as a sum, count or average. [4] |
| **API** | A way for programs to talk to each other over the internet, usually sending JSON. [3] |
| **axis** | Which direction to summarise: `axis=0` down the columns, `axis=1` across the rows. [8] |
| **Boolean mask** | An array of `True`/`False` values used to pick items. [6] |
| **Broadcasting** | NumPy stretching a smaller array (or a single number) to match a bigger one. [7] |
| **Column (field)** | One fact recorded for every row, such as the price or the date. [1] |
| **copy()** | Makes an independent array that doesn't share data. [6] |
| **Counter** | A dictionary from `collections` that counts things and can add up amounts. [4] |
| **CSV (comma-separated values)** | A plain-text table with one row per line and commas between the columns. [1] |
| **csv.DictReader** | Reads a CSV file as one dictionary per row, keyed by the header names. [2] |
| **csv.DictWriter** | Writes dictionaries out as CSV rows. [2] |
| **csv module** | Python's built-in tool for reading and writing CSV files correctly, including quoted values. [2] |
| **cumsum** | A running total. [8] |
| **Data analysis** | Answering questions by loading, cleaning, summarising and charting data. [1] |
| **Distribution** | How likely each possible value is. [9] |
| **dtype** | The data type shared by every item in an array, such as `int64` or `float64`. [5] |
| **Element-wise** | Done item by item, matching positions in two arrays. [7] |
| **Fancy indexing** | Selecting items with a list of positions, like `a[[0, 3]]`. [6] |
| **FileNotFoundError** | The error raised when a file name doesn't exist. [2] |
| **File path** | The name (and folder) of a file, like `"sales.csv"`. [2] |
| **Filter** | Keep only the rows that match a condition. [4] |
| **Generator expression** | A comprehension in round brackets, like `sum(x for x in items)`, that produces values one at a time. [4] |
| **Group** | Split rows by the values of a column, then summarise each part. [4] |
| **Header** | The first line of a CSV file, which names the columns. [1] |
| **Index** | The position of an item, starting at 0. [6] |
| **JSON** | A text format for structured data made of objects, arrays, strings, numbers, `true`/`false` and `null`. [3] |
| **JSON array** | An ordered list of values in `[ ]`, which becomes a Python list. [3] |
| **json.load / json.dump** | The same, but reading from or writing to a file. [3] |
| **json.loads / json.dumps** | Convert JSON text to Python objects, and Python objects to JSON text. [3] |
| **JSON object** | A set of key-value pairs in `{ }`, which becomes a Python dictionary. [3] |
| **Jupyter notebook** | A document of code cells and their results, the usual way analysts run Python. [1] |
| **lambda** | A tiny unnamed function, like `lambda p: p[1]`, often used as a sort key. [4] |
| **Library (package)** | A collection of ready-made code you import, such as pandas. [1] |
| **List comprehension** | `[x for x in items if condition]`, a one-line way to build a filtered list. [4] |
| **matplotlib** | The library for drawing charts. [1] |
| **Mean** | The average: the total divided by the number of values. [8] |
| **Median** | The middle value when the values are sorted. [8] |
| **Mode** | How a file is opened: `"r"` read (the default), `"w"` write (replaces), `"a"` append. [2] |
| **ndim** | The number of dimensions: 1 for a row of numbers, 2 for a table. [5] |
| **Nested data** | Values inside values, such as a list of items inside an order. [3] |
| **Newline character** | The invisible `\n` at the end of each line of a file. [2] |
| **Normal distribution** | The bell curve: values cluster around the mean, with fewer far away. [9] |
| **np.arange** | Makes evenly spaced numbers, like `range()`. [5] |
| **np.linspace** | Makes a set number of evenly spaced values between two ends. [5] |
| **np.nan** | "not a number", NumPy's marker for a missing value. [6] |
| **np.nanmean** | An average that skips missing (`nan`) values. [7] |
| **np.where** | Chooses between two values item by item based on a condition. [7] |
| **null** | JSON's "no value", which becomes Python's `None`. [3] |
| **NumPy** | The library for fast maths on whole arrays of numbers. [1] |
| **NumPy array (ndarray)** | A grid of numbers that all share one type, built for fast maths. [5] |
| **pandas** | The library for working with tables of data. [1] |
| **Percentile** | The value below which a given percentage of the data falls. [8] |
| **Quartiles** | The 25th, 50th and 75th percentiles. [8] |
| **Random generator** | An object, made with `np.random.default_rng()`, that produces random numbers. [9] |
| **reshape** | Rearranging an array's values into a new shape with the same total size. [8] |
| **Row (record)** | One thing being described, such as one order or one day. [1] |
| **Scaling (normalising)** | Rescaling numbers to a common range such as 0 to 1. [7] |
| **Seed** | A starting number that makes a generator produce the same sequence every run. [9] |
| **Shape** | The size of an array along each dimension, like `(3, 4)` for 3 rows and 4 columns. [5] |
| **Simulation** | Answering a question by acting it out many times with random numbers and counting. [9] |
| **Slice** | A range of positions, like `a[2:5]`. [6] |
| **Standard deviation (std)** | A measure of how spread out values are around the mean. [8] |
| **Tabular data** | Data arranged as a table of rows and columns. [1] |
| **Train/test split** | Dividing data so a model learns from one part and is tested on the other. [9] |
| **ufunc (universal function)** | A fast NumPy function that works on every item, like `np.sqrt`. [7] |
| **Uniform distribution** | Every value in a range is equally likely. [9] |
| **Vectorisation** | Doing an operation on every item of an array at once, without a loop. [5] |
| **View** | A slice that shares data with the original array, so changes show up in both. [6] |
| **with block** | `with open(...) as f:` opens a file and closes it automatically afterwards. [2] |
