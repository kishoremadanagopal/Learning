# SQL syntax cheat sheet

Everything from the course on one page. Examples use the [practice tables](lessons/00-the-tables.md). Where MSSQL differs, it's shown alongside.

## The full SELECT statement

```sql
WITH step AS (...)                       -- optional: CTEs            [12]
SELECT [DISTINCT] columns                -- what to show              [1, 8]
FROM table t                             -- where from                [1]
[LEFT] JOIN other o ON o.x = t.y         -- combine tables            [5]
WHERE row_condition                      -- filter rows               [1]
GROUP BY columns                         -- make groups               [3]
HAVING group_condition                   -- filter groups             [4]
ORDER BY columns [ASC | DESC]            -- sort                      [2]
LIMIT n;                                 -- how many  (MSSQL: SELECT TOP n)  [2]
```

**Written order:** SELECT → FROM → JOIN → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
**Run order:** FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

## Filtering (WHERE)

| Operator | Example |
|---|---|
| `=` `<>` `!=` | `city = 'Fremont'` |
| `>` `<` `>=` `<=` | `age >= 30` |
| `AND` `OR` `NOT` | `city = 'Oakland' AND age > 30` |
| `IN` | `city IN ('Fremont', 'Oakland')` |
| `BETWEEN` (inclusive) | `rating BETWEEN 1 AND 5` |
| `LIKE` | `name LIKE 'A%'` (starts with A), `'%a'` (ends), `'%a%'` (contains) |
| `IS NULL` / `IS NOT NULL` | `o.order_id IS NULL` (never `= NULL`) |

**Boundary words:** over / more than → `>` · at least / or more → `>=` · under / less than → `<` · at most / up to → `<=`

## Aggregates and grouping

```sql
SELECT department, COUNT(*), SUM(salary), AVG(salary), MIN(salary), MAX(salary)
FROM employees
GROUP BY department
HAVING COUNT(*) > 2;
```

- `COUNT(*)` counts rows; `COUNT(col)` skips NULLs; `COUNT(DISTINCT col)` counts different values.
- **The GROUP BY rule:** every other column must be inside an aggregate.
- Condition on one row → `WHERE`. Condition on a group → `HAVING`.

## Joins

```sql
FROM customers c
JOIN orders o ON o.customer_id = c.id          -- matches only
LEFT JOIN orders o ON o.customer_id = c.id     -- all customers, NULL where no order
RIGHT JOIN ... / FULL OUTER JOIN ... / CROSS JOIN ...
```

Rows with no match: `LEFT JOIN ... WHERE o.order_id IS NULL`

## Subqueries

```sql
WHERE salary > (SELECT AVG(salary) FROM employees)          -- one value
WHERE id IN (SELECT customer_id FROM orders)                -- a list
```

## CASE

```sql
CASE
  WHEN condition1 THEN 'label 1'      -- first true WHEN wins
  WHEN condition2 THEN 'label 2'
  ELSE 'other'
END AS new_column

SUM(CASE WHEN condition THEN 1 ELSE 0 END)   -- conditional count
```

## Functions

| Task | SQLite | MSSQL |
|---|---|---|
| upper / lower case | `UPPER(x)`, `LOWER(x)` | same |
| length | `LENGTH(x)` | `LEN(x)` |
| join text | `a \|\| b` | `a + b`, `CONCAT(a, b)` |
| part of text | `SUBSTR(x, 1, 3)` | `SUBSTRING(x, 1, 3)` |
| round | `ROUND(x, 2)` | same |
| replace NULL | `COALESCE(x, 0)` | `COALESCE(x, 0)`, `ISNULL(x, 0)` |
| decimals from integers | `x * 1.0` | `x * 1.0` |

## Dates

| Task | SQLite | MSSQL |
|---|---|---|
| format | `'YYYY-MM-DD'` | same |
| today | `date('now')` | `GETDATE()` |
| year | `strftime('%Y', d)` → `'2026'` (text) | `YEAR(d)` → `2026` |
| month | `strftime('%m', d)` → `'01'` | `MONTH(d)` → `1` |
| year-month | `strftime('%Y-%m', d)` | `FORMAT(d, 'yyyy-MM')` |
| days between | `julianday(b) - julianday(a)` | `DATEDIFF(day, a, b)` |
| add days | `date(d, '+30 days')` | `DATEADD(day, 30, d)` |
| a month's range | `d >= '2026-02-01' AND d < '2026-03-01'` | same |

SQLite codes: `%Y` year · `%m` month · `%d` day · `%H` hour · `%M` minute · `%S` second

## Window functions

```sql
ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)   -- 1, 2, 3
RANK()       OVER (...)                                       -- 1, 2, 2, 4
DENSE_RANK() OVER (...)                                       -- 1, 2, 2, 3
SUM(amount)  OVER (ORDER BY order_date, order_id)             -- running total
AVG(salary)  OVER (PARTITION BY department)                   -- group value on every row
LAG(x)  OVER (ORDER BY ...)    LEAD(x) OVER (ORDER BY ...)    -- previous / next row
```

Top N per group: `ROW_NUMBER()` in a CTE, then `WHERE rn = 1`.

## Combining results

```sql
SELECT ... UNION SELECT ...        -- stack, remove duplicates
SELECT ... UNION ALL SELECT ...    -- stack, keep everything
SELECT ... INTERSECT SELECT ...    -- in both
SELECT ... EXCEPT SELECT ...       -- in first, not second (Oracle: MINUS)
```

Same number of columns on both sides; one `ORDER BY` at the end.

## Changing data

```sql
INSERT INTO customers (id, name, city, age) VALUES (6, 'Zoe', 'Oakland', 23);
UPDATE employees SET salary = salary + 5000 WHERE department = 'Marketing';
DELETE FROM orders WHERE order_id = 107;
```

⚠️ Always write the `WHERE`. Run a `SELECT` with the same `WHERE` first.

## Transactions

```sql
BEGIN TRANSACTION;
  -- changes
COMMIT;      -- keep
ROLLBACK;    -- undo
```

## Tables, views and indexes

```sql
CREATE TABLE reviews (
  review_id   INTEGER PRIMARY KEY,                   -- MSSQL: INT IDENTITY(1,1) PRIMARY KEY
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  rating      INTEGER CHECK (rating BETWEEN 1 AND 5),
  comment     TEXT DEFAULT '',                        -- MSSQL: VARCHAR(500)
  code        TEXT UNIQUE
);
ALTER TABLE customers ADD COLUMN email TEXT;          -- MSSQL: ADD email VARCHAR(100)
DROP TABLE reviews;

CREATE VIEW customer_spending AS SELECT ...;
DROP VIEW customer_spending;

CREATE INDEX idx_orders_customer ON orders (customer_id);
DROP INDEX idx_orders_customer;
```

| Type | SQLite | MSSQL |
|---|---|---|
| whole number | `INTEGER` | `INT` |
| decimal / money | `REAL` | `DECIMAL(10,2)` |
| text | `TEXT` | `VARCHAR(n)`, `NVARCHAR(n)` |
| date | `TEXT` | `DATE`, `DATETIME2` |
| true/false | `INTEGER` | `BIT` |

## Top N rows in each database

| SQLite / MySQL / PostgreSQL | MSSQL | Oracle |
|---|---|---|
| `... ORDER BY age LIMIT 1` | `SELECT TOP 1 ... ORDER BY age` | `... ORDER BY age FETCH FIRST 1 ROWS ONLY` |
