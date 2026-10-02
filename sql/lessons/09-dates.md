# Lesson 9: Dates

**You'll learn:** date formats, filtering by date, pulling out the year and month, grouping by month, and date math, in SQLite and MSSQL.

## Key terms

- **ISO date format:** `YYYY-MM-DD`, which sorts and compares correctly.
- **strftime:** SQLite's function for pulling parts out of a date or formatting it.
- **Format code:** a letter code for a date part, like `%Y` (year) or `%m` (month).
- **julianday:** SQLite's function that turns a date into a day number, for date math.

## Syntax

```sql
WHERE date_col >= 'YYYY-MM-DD' AND date_col < 'YYYY-MM-DD'
strftime('%Y', date_col)           -- year as text
strftime('%Y-%m', date_col)        -- year-month as text
julianday(end) - julianday(start)  -- days between
date(date_col, '+30 days')         -- add days
```

This lesson uses the `order_date` column of `orders` (see [the practice tables](00-the-tables.md)).

## The date format: YYYY-MM-DD

Write dates as year-month-day with leading zeros: `'2026-01-10'`. This format sorts correctly and compares correctly with `<` and `>`, and every database accepts it.

## Filtering by date

```sql
SELECT product, order_date FROM orders
WHERE order_date >= '2026-02-01';                              -- Monitor, Keyboard, Lamp
```

For a range, use "on or after the start, and before the next period":

```sql
WHERE order_date >= '2026-02-01' AND order_date < '2026-03-01'   -- all of February
```

You don't need to know how many days February has, and it still works when dates include a time of day.

## Pulling out parts of a date

| Want | SQLite | MSSQL | Oracle |
|---|---|---|---|
| year | `strftime('%Y', d)` → `'2026'` | `YEAR(d)` → `2026` | `EXTRACT(YEAR FROM d)` |
| month | `strftime('%m', d)` → `'01'` | `MONTH(d)` → `1` | `EXTRACT(MONTH FROM d)` |
| year-month | `strftime('%Y-%m', d)` | `FORMAT(d, 'yyyy-MM')` | `TO_CHAR(d, 'YYYY-MM')` |

⚠️ In SQLite, `strftime` returns **text with leading zeros**. Compare with `= '2025'` and `= '01'`, in quotes. `= 2025` (a number) silently matches nothing.

⚠️ **Letter case matters in format codes.** In SQLite `%m` is month and `%M` is **minute**. `strftime('%Y-%M', ...)` turns every date into `2026-00` and your query returns nothing. MSSQL flips it (`MM` = month, `mm` = minutes), and Oracle uses `MM` and `MI`.

| SQLite code | Means |
|---|---|
| `%Y` | year |
| `%m` | month |
| `%d` | day |
| `%H` / `%M` / `%S` | hour / minute / second |

## Grouping by month or year

```sql
SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
FROM orders
GROUP BY strftime('%Y-%m', order_date);
```

## Date math

| Want | SQLite | MSSQL |
|---|---|---|
| today | `date('now')` | `GETDATE()` |
| days between | `julianday(end) - julianday(start)` | `DATEDIFF(day, start, end)` |
| add 30 days | `date(d, '+30 days')` | `DATEADD(day, 30, d)` |

`MIN(order_date)` is the earliest date and `MAX(order_date)` the latest.

## "First order" needs MIN, not luck

```sql
-- Correct in every database
SELECT c.name, MIN(o.order_date) AS first_order
FROM orders o
JOIN customers c ON o.customer_id = c.id
GROUP BY c.name;
```

`SELECT c.name, o.order_date ... GROUP BY c.name` may show the right dates in SQLite, but only because it picks a date from whichever row it reads first. It breaks as soon as an older order is added, and MSSQL and Oracle reject it. **A correct result doesn't always mean a correct query.**

To format the result, wrap the format *around* the `MIN`: `FORMAT(MIN(o.order_date), 'yyyy-MM-dd')` in MSSQL, `TO_CHAR(MIN(o.order_date), 'YYYY-MM-DD')` in Oracle.

## Debugging tip

When a query runs but returns nothing, put the expression in `SELECT` to see what it actually produces:

```sql
SELECT order_date, strftime('%Y-%M', order_date) FROM orders;   -- shows 2026-00: aha!
```

## Exercises

1. Product and order date of every order placed in January 2026.
2. Products of all orders placed in 2025.
3. The number of orders in each month, shown as year-month.
4. The total amount of orders in each year.
5. Each customer's name and the date of their first order.
6. Each order's product and how many days before 2026-03-31 it was placed.

**In the sandbox:** exercises 38–43.

<details>
<summary>Answers</summary>

```sql
-- 1  → Desk, Chair
SELECT product, order_date FROM orders
WHERE order_date >= '2026-01-01' AND order_date < '2026-02-01';

-- 2  → Laptop, Mouse
SELECT product FROM orders
WHERE strftime('%Y', order_date) = '2025';

-- 3
SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS num_orders
FROM orders
GROUP BY strftime('%Y-%m', order_date);

-- 4  → 2025: 1225, 2026: 975
SELECT strftime('%Y', order_date) AS year, SUM(amount) AS total
FROM orders
GROUP BY strftime('%Y', order_date);

-- 5
SELECT c.name, MIN(o.order_date) AS first_order
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;

-- 6  → Laptop 131, Mouse 119, …
SELECT product, julianday('2026-03-31') - julianday(order_date) AS days_before
FROM orders;
```
</details>

---
Previous: [Lesson 8](08-functions.md) · Next: [Lesson 10: Changing data](10-insert-update-delete.md)
