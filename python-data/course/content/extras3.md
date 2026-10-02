@@ pandas-series
topics: `pd.Series`, the index, label alignment, `value_counts`, `unique`, `nunique`, `idxmax`
terms:
- **Series:** a one-dimensional column of values, each with a label.
- **Index:** the labels of a Series' values (or a DataFrame's rows).
- **Label alignment:** pandas matching values by index label, not position, when combining Series.
- **NaN:** "not a number", the marker pandas shows for a missing value.
- **value_counts:** counts how often each distinct value appears, most common first.
- **unique / nunique:** the distinct values, and how many there are.
- **idxmax / idxmin:** the label of the largest / smallest value.
mistakes:
- Expecting two Series to add by position. They line up by label; different labels give NaN. Use `.add(other, fill_value=0)` if you want missing labels treated as 0.
- Writing `pd.series(...)`. The class names start with capitals: `pd.Series`, `pd.DataFrame`.
- Confusing `count()` (non-missing values) with `value_counts()` (how often each value appears).

@@ dataframes
topics: `pd.DataFrame`, `read_csv`, `read_json`, `head`, `tail`, `shape`, `columns`, `dtypes`, `info`, `describe`
terms:
- **DataFrame:** a table of rows and named columns; each column is a Series.
- **pd.read_csv / pd.read_json:** load a CSV or JSON file into a DataFrame.
- **head / tail:** the first / last rows of a table (5 by default).
- **shape:** a table's size as (rows, columns).
- **dtypes:** the data type of each column.
- **info():** a summary of columns, types and non-missing counts.
- **describe():** summary statistics for each number column.
- **Non-null count:** how many values in a column are present (not missing).
mistakes:
- Calling `df.shape()` with brackets. `shape` is an attribute, not a method: write `df.shape`.
- Skipping the first look. Always check `shape`, `info()` and `describe()` before analysing: they reveal missing values and impossible numbers.
- Trusting the type of a column without checking. A number column with one stray word loads as text (`str`).

@@ selecting-data
topics: `df["col"]`, `df[["a", "b"]]`, `loc`, `iloc`, `set_index`, `reset_index`, changing cells
terms:
- **Selection:** picking particular rows, columns or cells from a table.
- **loc:** selects rows and columns by label; slices include the end.
- **iloc:** selects rows and columns by position (integers); slices exclude the end.
- **set_index:** makes a column the row labels.
- **reset_index:** turns the index back into a normal column.
- **KeyError:** the error raised when a column or label doesn't exist.
- **Copy-on-write:** pandas 3's rule that a selection behaves like a copy, so changing it never changes the original table.
mistakes:
- Using single brackets for several columns: `df["a", "b"]` is a `KeyError`. Use a list: `df[["a", "b"]]`.
- Changing data with chained brackets like `df["price"][3] = 9`. In pandas 3 it does nothing; use `df.loc[3, "price"] = 9`.
- Mixing up `loc` and `iloc`. With a custom index, `loc[0]` looks for the label 0, which may not exist.

@@ filtering-rows
topics: boolean masks, `&`, `|`, `~`, `isin`, `between`, filtering text and dates, `query`, `loc` with a mask
terms:
- **Filter:** keeping only the rows that meet a condition.
- **Boolean mask:** a Series of True/False values, one per row, used to filter.
- **isin:** True where a value is one of a given list.
- **between:** True where a value lies within a range (both ends included).
- **query:** filters rows using a condition written as text.
- **& | ~:** "and", "or" and "not" for masks.
mistakes:
- Leaving out the brackets around each condition. Write `(df["a"] > 1) & (df["b"] < 5)`.
- Using `and`/`or` instead of `&`/`|`, which raises "The truth value of a Series is ambiguous".
- Comparing text with the wrong capitals or spaces: `"north"` doesn't match `"North"`. Check the values with `unique()` first.

@@ sorting-and-new-columns
topics: `sort_values`, `nlargest`, new calculated columns, `np.where`, `assign`, method chains, `rename`, `drop`
terms:
- **sort_values:** sorts rows by one or more columns.
- **ascending:** the sort direction; `ascending=False` puts the largest first.
- **nlargest / nsmallest:** the top / bottom n rows by a column.
- **Calculated column:** a new column built from other columns, like revenue = units × price.
- **assign:** returns a copy of the table with new columns added.
- **Method chain:** several methods called one after another, each on the previous result.
- **rename / drop:** change column names / remove columns.
mistakes:
- Forgetting to save the result: `df.sort_values("x")` on its own changes nothing. Write `df = df.sort_values("x")`.
- Using `inplace=True`. It still works but is discouraged; assigning the result is clearer.
- Dividing to get a percentage and forgetting `* 100`, or rounding too early and losing accuracy in later steps.

@@ summarising-data
topics: `sum`, `mean`, `median`, `agg`, `count`, `nunique`, `value_counts(normalize=True)`, `idxmax`, formatting with `:,` and `:%`
terms:
- **Summary statistic:** one number describing many, such as a total, average or count.
- **agg:** applies one or more summaries at once, like `agg(["mean", "max"])`.
- **count:** the number of values that aren't missing.
- **Share (proportion):** a part divided by the whole, between 0 and 1.
- **Percentage:** a share multiplied by 100.
- **Format code:** instructions inside an f-string's `{}` that control how a number looks, like `:,.2f` or `:.0%`.
mistakes:
- Using `count()` to get the number of rows. It skips missing values; use `len(df)`.
- Adding up an ID column. `order_id.sum()` is a number, but it means nothing. Think about what each summary means.
- Reporting averages without counts. "Average rating 9.1" means little if it's from 2 films.
