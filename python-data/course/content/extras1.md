@@ what-is-data-analysis
topics: the analysis workflow, rows and columns, CSV files, NumPy, pandas and matplotlib
terms:
- **Data analysis:** answering questions by loading, cleaning, summarising and charting data.
- **Tabular data:** data arranged as a table of rows and columns.
- **Row (record):** one thing being described, such as one order or one day.
- **Column (field):** one fact recorded for every row, such as the price or the date.
- **CSV (comma-separated values):** a plain-text table with one row per line and commas between the columns.
- **Header:** the first line of a CSV file, which names the columns.
- **Library (package):** a collection of ready-made code you import, such as pandas.
- **NumPy:** the library for fast maths on whole arrays of numbers.
- **pandas:** the library for working with tables of data.
- **matplotlib:** the library for drawing charts.
- **Jupyter notebook:** a document of code cells and their results, the usual way analysts run Python.
mistakes:
- Starting to code before you know the question. Write the question down first: it decides which data and which steps you need.
- Using a different short name like `import pandas as p`. It works, but everyone expects `pd`, `np` and `plt`.
- Treating a library as magic. Every pandas line does something you could write in plain Python; knowing that makes errors easier to understand.

@@ files-and-csv
topics: `open()`, `with`, reading lines, `csv.DictReader`, writing text and CSV files
terms:
- **File path:** the name (and folder) of a file, like `"sales.csv"`.
- **with block:** `with open(...) as f:` opens a file and closes it automatically afterwards.
- **Mode:** how a file is opened: `"r"` read (the default), `"w"` write (replaces), `"a"` append.
- **csv module:** Python's built-in tool for reading and writing CSV files correctly, including quoted values.
- **csv.DictReader:** reads a CSV file as one dictionary per row, keyed by the header names.
- **csv.DictWriter:** writes dictionaries out as CSV rows.
- **Newline character:** the invisible `\n` at the end of each line of a file.
- **FileNotFoundError:** the error raised when a file name doesn't exist.
mistakes:
- Doing maths on values straight from a file. They're strings: `"4.5" * 2` gives `"4.54.5"`. Convert with `float()` or `int()` first.
- Splitting CSV lines with `line.split(",")`. It breaks on quoted values like `"92,000"`. Use the `csv` module (or pandas).
- Opening a file you want to keep with `"w"`. Write mode empties the file first; use `"a"` to add to it.

@@ json-data
topics: JSON syntax, `json.loads`, `json.dumps`, `json.load`, `json.dump`, nested data, `.get()`
terms:
- **JSON:** a text format for structured data made of objects, arrays, strings, numbers, `true`/`false` and `null`.
- **JSON object:** a set of key-value pairs in `{ }`, which becomes a Python dictionary.
- **JSON array:** an ordered list of values in `[ ]`, which becomes a Python list.
- **null:** JSON's "no value", which becomes Python's `None`.
- **json.loads / json.dumps:** convert JSON text to Python objects, and Python objects to JSON text.
- **json.load / json.dump:** the same, but reading from or writing to a file.
- **Nested data:** values inside values, such as a list of items inside an order.
- **API:** a way for programs to talk to each other over the internet, usually sending JSON.
mistakes:
- Writing JSON by hand with single quotes or `True`. JSON needs double quotes and lowercase `true`/`false`/`null`; let `json.dumps` write it for you.
- Mixing up `loads` and `load`. The `s` versions work with strings; the others work with open files.
- Assuming every record has every key. Use `record.get("key", default)` or check `is None` first.

@@ crunching-with-python
topics: filtering with comprehensions, `sum()`, `Counter`, grouping with a dictionary, ranking with `sorted(key=...)`
terms:
- **Filter:** keep only the rows that match a condition.
- **List comprehension:** `[x for x in items if condition]`, a one-line way to build a filtered list.
- **Generator expression:** a comprehension in round brackets, like `sum(x for x in items)`, that produces values one at a time.
- **Counter:** a dictionary from `collections` that counts things and can add up amounts.
- **Group:** split rows by the values of a column, then summarise each part.
- **Aggregate:** a single number that summarises many, such as a sum, count or average.
- **lambda:** a tiny unnamed function, like `lambda p: p[1]`, often used as a sort key.
mistakes:
- Forgetting to convert strings before adding: `sum(s["units"] for s in sales)` fails because units are text. Wrap them in `int()`.
- Writing `revenue[key] += amount` for a key that doesn't exist yet, which raises `KeyError`. Use `revenue.get(key, 0) + amount` or a `Counter`.
- Sorting a dictionary with `sorted(d)` and expecting values. That sorts the keys; use `sorted(d.items(), key=...)`.
