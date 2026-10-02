# Python for Data glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **Aggregate** | A single number that summarises many, such as a sum, count or average. [4] |
| **API** | A way for programs to talk to each other over the internet, usually sending JSON. [3] |
| **Column (field)** | One fact recorded for every row, such as the price or the date. [1] |
| **Counter** | A dictionary from `collections` that counts things and can add up amounts. [4] |
| **CSV (comma-separated values)** | A plain-text table with one row per line and commas between the columns. [1] |
| **csv.DictReader** | Reads a CSV file as one dictionary per row, keyed by the header names. [2] |
| **csv.DictWriter** | Writes dictionaries out as CSV rows. [2] |
| **csv module** | Python's built-in tool for reading and writing CSV files correctly, including quoted values. [2] |
| **Data analysis** | Answering questions by loading, cleaning, summarising and charting data. [1] |
| **FileNotFoundError** | The error raised when a file name doesn't exist. [2] |
| **File path** | The name (and folder) of a file, like `"sales.csv"`. [2] |
| **Filter** | Keep only the rows that match a condition. [4] |
| **Generator expression** | A comprehension in round brackets, like `sum(x for x in items)`, that produces values one at a time. [4] |
| **Group** | Split rows by the values of a column, then summarise each part. [4] |
| **Header** | The first line of a CSV file, which names the columns. [1] |
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
| **Mode** | How a file is opened: `"r"` read (the default), `"w"` write (replaces), `"a"` append. [2] |
| **Nested data** | Values inside values, such as a list of items inside an order. [3] |
| **Newline character** | The invisible `\n` at the end of each line of a file. [2] |
| **null** | JSON's "no value", which becomes Python's `None`. [3] |
| **NumPy** | The library for fast maths on whole arrays of numbers. [1] |
| **pandas** | The library for working with tables of data. [1] |
| **Row (record)** | One thing being described, such as one order or one day. [1] |
| **Tabular data** | Data arranged as a table of rows and columns. [1] |
| **with block** | `with open(...) as f:` opens a file and closes it automatically afterwards. [2] |
