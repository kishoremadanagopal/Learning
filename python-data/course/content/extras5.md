@@ groupby
topics: split-apply-combine, `groupby`, `size`, named aggregation with `agg`, grouping by several columns, `reset_index`, `transform`
terms:
- **groupby:** splits a table into groups by a column's values so each group can be summarised.
- **Split-apply-combine:** the three steps of grouping: split into groups, summarise each, combine the answers.
- **size():** the number of rows in each group.
- **Named aggregation:** `agg(new_name=("column", "summary"))`, which names each result column.
- **MultiIndex:** an index with more than one level, as you get when grouping by two columns.
- **transform:** a group summary repeated on every row of that group.
mistakes:
- Forgetting to choose a column: `df.groupby("region").sum()` tries to add up every column, including IDs and text. Select what you need: `df.groupby("region")["revenue"].sum()`.
- Using `count()` when you want the number of rows. `count()` skips missing values; `size()` counts every row.
- Grouping on uncleaned text, so "Sales" and "sales " become separate groups. Clean first.

@@ pivot-tables
topics: `pivot_table`, `index`, `columns`, `values`, `aggfunc`, `margins`, `fill_value`, `pd.crosstab`, `normalize`
terms:
- **Pivot table:** a summary grid with one category down the side, another across the top, and a number in each cell.
- **aggfunc:** the summary a pivot table uses, such as "sum" or "mean".
- **Margins:** total rows and columns added to a pivot table.
- **fill_value:** what to show where a combination has no data.
- **Crosstab:** a table counting how often each combination of two categories occurs.
- **normalize:** turns counts into shares, by row (`"index"`), column (`"columns"`) or overall (`True`).
mistakes:
- Leaving out `aggfunc` and getting averages. The default is the mean; say `aggfunc="sum"` when you want totals.
- Comparing raw counts between groups of different sizes. Use `normalize="index"` to compare shares.
- Treating `NaN` in a pivot as zero without saying so. Use `fill_value=0` only when no data really means zero.

@@ merging-tables
topics: `merge`, `on`, `how` (inner, left, right, outer), `indicator`, `left_on`/`right_on`, `suffixes`, `validate`
terms:
- **Join (merge):** combining two tables by matching rows on a key.
- **Key:** the column used to match rows, like `customer_id`.
- **Inner join:** keeps only rows that match in both tables.
- **Left join:** keeps every row of the left table, with gaps where there's no match.
- **Outer join:** keeps every row from both tables.
- **indicator:** adds a `_merge` column showing whether each row matched.
- **One-to-many:** one row on one side matches many on the other, like one customer to many orders.
mistakes:
- Using an inner join and silently losing rows that didn't match. Check the row count, or use `how="left"` with `indicator=True`.
- Joining on keys with different types (`"101"` vs `101`) or spellings. They won't match; clean and convert first.
- Merging whole wide tables and getting `_x`/`_y` columns everywhere. Select the columns you need first.

@@ reshaping-data
topics: `pd.concat`, `ignore_index`, wide vs long (tidy) data, `melt`, `pivot`, `unstack`
terms:
- **concat:** stacks tables on top of each other (or side by side with `axis=1`).
- **Wide data:** one row per thing, with a column for each measurement.
- **Long (tidy) data:** one row per thing per measurement, with a column naming the measurement.
- **melt:** turns columns into rows (wide to long).
- **pivot:** turns rows into columns (long to wide).
- **unstack:** moves an index level into the columns.
mistakes:
- Concatenating tables whose column names differ slightly, which creates extra columns full of gaps. Make the names match first.
- Forgetting `ignore_index=True` and ending up with repeated index labels.
- Using `pivot` when an index/column pair repeats, which raises an error. Use `pivot_table` to summarise the repeats.

@@ map-apply-and-bins
topics: `map` with a dictionary, `apply` with functions and lambdas, `apply(axis=1)`, `np.select`, `pd.cut`, `pd.qcut`
terms:
- **map:** replaces each value using a dictionary (or function).
- **apply:** runs a function on every value of a Series, or every row with `axis=1`.
- **np.select:** chooses a result from several conditions, first match wins.
- **Bin:** a range of values grouped together, like ages 30–44.
- **pd.cut:** sorts numbers into bins with edges you choose.
- **pd.qcut:** sorts numbers into bins holding roughly equal numbers of rows.
- **Quantile:** the value below which a given share of the data falls (the 0.25 quantile is the first quartile).
mistakes:
- Reaching for `apply(axis=1)` first. It's slow on big tables; try `np.where`, `np.select` or vectorised maths.
- Getting the `cut` edges wrong: bins include the right edge, so with edges `[0, 60, 100]` a score of 60 lands in the first bin.
- Forgetting that `map` turns unknown values into missing. Check with `isna().sum()` afterwards.

@@ time-series
topics: date index, partial-date selection, `resample`, period codes, `shift`, `pct_change`, `rolling`, `cumsum`, groupby + resample
terms:
- **Time series:** a measurement recorded over time, like daily sales.
- **DatetimeIndex:** an index made of dates, which unlocks time-based selection and resampling.
- **resample:** groups a time series into periods such as weeks or months.
- **shift:** moves values down (or up) by a number of steps, to compare with earlier periods.
- **pct_change:** the change from the previous value as a fraction.
- **Rolling (moving) average:** the average over a sliding window, such as the last 7 days.
- **Year to date (YTD):** the running total from the start of the year.
mistakes:
- Resampling without a date index. Use `set_index("date")` (with real datetimes) first.
- Using the old period code `"M"`; in pandas 3 it's `"ME"` for month end (and `"QE"`, `"YE"`).
- Reading too much into the start of a rolling average, which is missing or based on few values.
