@@ missing-values
topics: `isna`, `notna`, `dropna`, `fillna`, forward fill, flagging gaps, `na_values`
terms:
- **Missing value:** a gap in the data, shown as `NaN`, `None` or `<NA>`.
- **isna / notna:** True where a value is missing / present.
- **dropna:** removes rows (or columns) with missing values.
- **fillna:** replaces missing values with something you choose.
- **Imputation:** filling missing values with an estimate, such as the median.
- **Forward fill (ffill):** filling a gap with the previous value, common for time series.
- **na_values:** tells `read_csv` which extra strings (like `"-"`) mean missing.
mistakes:
- Calling `dropna()` without thinking and losing a large part of the data. Check how many rows it removes; use `subset=` to target the columns you need.
- Filling with 0 when missing doesn't mean zero. It drags averages down and invents data.
- Forward-filling unsorted data, or across groups. Sort by date and fill within each group.

@@ data-types
topics: `dtypes`, `astype`, `pd.to_numeric`, `errors="coerce"`, cleaning text into numbers, `Int64`, `dtype=` on load, categories
terms:
- **astype:** converts a column to another type; fails if any value can't be converted.
- **pd.to_numeric:** converts values to numbers; `errors="coerce"` turns failures into missing values.
- **Coerce:** force a conversion, replacing what can't be converted with a missing value.
- **Nullable integer (Int64):** a whole-number type that can also hold missing values.
- **Categorical:** a type for a column with a few repeating values, optionally in a set order.
- **regex=False:** tells `.str.replace` to treat the search text literally, not as a pattern.
mistakes:
- Using `astype(float)` on dirty text and getting an error. Clean the characters first, or use `pd.to_numeric(..., errors="coerce")`.
- Coercing without checking. Count the new missing values; if there are many, some formats weren't handled.
- Storing IDs and postcodes as numbers, which drops leading zeros. Load them as text.

@@ text-cleaning
topics: `.str` methods, `strip`, `lower`, `title`, `replace` vs `.str.replace`, `contains`, `split`, `extract`, `na=False`
terms:
- **.str accessor:** gives a text column all the string methods, applied to every value.
- **strip:** removes spaces (and newlines) from both ends of text.
- **title case:** Each Word Starting With A Capital.
- **Standardise:** make values that mean the same thing look the same.
- **str.contains:** True where the text includes a substring.
- **str.split:** breaks text into parts at a separator.
- **Regular expression (regex):** a pattern for matching text, like `\d+` for "one or more digits".
- **str.extract:** pulls out the part of each value that matches a pattern.
mistakes:
- Forgetting `.str`: `df["name"].strip()` is an error. Write `df["name"].str.strip()`.
- Cleaning case but not spaces (or the reverse). `"SALES "` needs both `strip()` and a case change.
- Searching with `contains` on a column with gaps and getting an error when filtering. Add `na=False`.

@@ duplicates-and-outliers
topics: `duplicated`, `drop_duplicates`, `subset` and `keep`, impossible values, `mask`, `clip`, the IQR rule
terms:
- **Duplicate:** a row that repeats another, completely or by its key.
- **Key:** a column that should uniquely identify each row, such as an order ID.
- **drop_duplicates:** removes repeated rows; `subset=` checks only some columns, `keep=` chooses which copy stays.
- **Impossible value:** a value that can't be true, like a negative age.
- **mask:** replaces values with missing where a condition is True.
- **clip:** caps values at a lower and upper limit.
- **Outlier:** a value far from the others, which may be an error or genuinely unusual.
- **IQR (interquartile range):** the third quartile minus the first: the spread of the middle half of the data.
mistakes:
- De-duplicating before cleaning text, so `"MEI BROWN"` and `"Mei Brown"` both survive.
- Deleting outliers automatically. Check them first: they might be your most important customers.
- "Fixing" impossible values with a guess (230 → 23). Mark them missing unless you know the true value.

@@ dates-and-times
topics: `pd.to_datetime`, `parse_dates`, the `.dt` accessor, filtering by date, `Timedelta`, `DateOffset`, `strftime`, `dayfirst`
terms:
- **datetime64:** pandas' type for dates and times.
- **pd.to_datetime:** converts text to dates.
- **parse_dates:** converts date columns while loading with `read_csv`.
- **.dt accessor:** gives a date column its parts and methods, like `.dt.month`.
- **Timestamp:** a single date and time, like `pd.Timestamp("2026-01-01")`.
- **Timedelta:** a length of time, the result of subtracting dates.
- **DateOffset:** a calendar step such as one month, which respects different month lengths.
- **strftime:** formats dates as text using codes like `%Y-%m-%d`.
mistakes:
- Doing date logic on text. `"2025-9-1"` sorts after `"2025-10-01"` as text; convert first.
- Mixing up day-first and month-first dates. Pass `dayfirst=True` or an exact `format=`.
- Forgetting `.dt` before date parts: `df["date"].month` is an error; use `df["date"].dt.month`.

@@ cleaning-project
topics: a full cleaning workflow, working on a copy, cleaning functions, `assert` checks, `to_csv`
terms:
- **Raw data:** the data exactly as it arrived, kept unchanged for reference.
- **Cleaning pipeline:** the ordered steps that turn raw data into clean data.
- **Reproducible:** giving the same result every time it's run on the same input.
- **assert:** a statement that stops with an error if a condition isn't true, used as an automatic check.
- **to_csv:** writes a DataFrame to a CSV file; `index=False` leaves out the index.
- **Data quality check:** a test that the cleaned data meets your expectations.
mistakes:
- Cleaning in scattered cells or by hand in a spreadsheet, so nobody (including you) can repeat it.
- Changing the raw table in place, then being unable to compare before and after. Work on `raw.copy()`.
- Skipping the checks. A one-line `assert` catches a step that silently didn't work.
