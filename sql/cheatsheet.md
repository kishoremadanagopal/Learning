# SQL syntax cheat sheet

Everything from the course on one page. Examples use the [practice tables](lessons/00-the-tables.md). Where MSSQL differs, it's shown alongside; [Lesson 19](lessons/19-sql-dialects-2026.md) compares all five major databases. The number in brackets is the lesson.

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
LIMIT n OFFSET m;                        -- how many, skipping m  (MSSQL: SELECT TOP n)  [2]
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
| `NOT IN` | `city NOT IN ('Fremont')` (returns nothing if the list has a NULL) [6] |
| `LIKE '_e_'` | `_` is exactly one character [8] |
| `EXISTS` | `WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)` [6] |

**Sorting extras** [2]: `ORDER BY city, age DESC` (tie-breaker) · `ORDER BY LENGTH(name)` (expression) · `NULLS FIRST` / `NULLS LAST` · `LIMIT 1 OFFSET 1` (second row)

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

Rows with no match: `LEFT JOIN ... WHERE o.order_id IS NULL` (or `NOT EXISTS`)

```sql
FROM employees a JOIN employees b ON a.department = b.department AND a.salary > b.salary   -- self join [5]
JOIN bands b ON e.salary BETWEEN b.low AND b.high                                         -- range join [5]
```

## Subqueries

```sql
WHERE salary > (SELECT AVG(salary) FROM employees)          -- one value
WHERE id IN (SELECT customer_id FROM orders)                -- a list
WHERE e.salary = (SELECT MAX(salary) FROM employees e2
                  WHERE e2.department = e.department)       -- correlated: once per row  [6]
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)   -- no match   [6]
FROM (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id) t   -- derived table [6]
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

### Numbers [8]

| Task | SQLite (sandbox) | MySQL | PostgreSQL | MSSQL | Oracle |
|---|---|---|---|---|---|
| round to d decimals | `ROUND(x, d)` | same | same | same | same |
| round down | `FLOOR(x)` | same | same | same | same |
| round up | `CEIL(x)` | `CEIL`/`CEILING` | `CEIL`/`CEILING` | `CEILING(x)` | `CEIL(x)` |
| truncate decimals | `CAST(x AS INTEGER)` | `TRUNCATE(x, d)` | `TRUNC(x, d)` | `ROUND(x, d, 1)` | `TRUNC(x, d)` |
| remainder | `x % y` | `%`, `MOD` | `%`, `MOD` | `%` | `MOD(x, y)` |
| absolute / power / root | `ABS`, `POWER`, `SQRT` | same | same | same | same |
| decimals from integers | `x * 1.0`, `CAST(x AS REAL)` | not needed | `x * 1.0` | `x * 1.0` | not needed |

`FLOOR(4.9)` → 4 · `CEIL(4.1)` → 5 · `ROUND(4.5)` → 5 · truncate 4.9 → 4 · `7 / 2` → 3 in SQLite, PostgreSQL, MSSQL (3.5 in MySQL, Oracle)

### Text [8]

| Task | SQLite | MySQL | PostgreSQL | MSSQL | Oracle |
|---|---|---|---|---|---|
| upper / lower | `UPPER`, `LOWER` | same | same | same | same |
| length | `LENGTH(x)` | `CHAR_LENGTH(x)` | `LENGTH(x)` | `LEN(x)` | `LENGTH(x)` |
| join | `a \|\| b`, `CONCAT` | `CONCAT(a, b)` | `a \|\| b`, `CONCAT` | `a + b`, `CONCAT` | `a \|\| b` |
| part | `SUBSTR(x, 1, 3)` | `SUBSTRING` | `SUBSTRING` | `SUBSTRING` | `SUBSTR` |
| last n chars | `SUBSTR(x, -n)` | `RIGHT(x, n)` | `RIGHT(x, n)` | `RIGHT(x, n)` | `SUBSTR(x, -n)` |
| position | `INSTR(x, 'a')` | `INSTR`, `LOCATE` | `POSITION('a' IN x)` | `CHARINDEX('a', x)` | `INSTR` |
| replace / trim | `REPLACE`, `TRIM` | same | same | same | same |
| list per group | `GROUP_CONCAT(x, ', ')` | `GROUP_CONCAT(x SEPARATOR ', ')` | `STRING_AGG(x, ', ')` | `STRING_AGG(x, ', ')` | `LISTAGG(x, ', ')` |

Starts with a vowel: `LOWER(SUBSTR(city, 1, 1)) IN ('a','e','i','o','u')` · ends with one: `SUBSTR(city, -1)`

### NULLs [5, 8]

| Task | Everywhere | Also |
|---|---|---|
| replace NULL | `COALESCE(x, 0)` | `IFNULL` (SQLite, MySQL), `ISNULL` (MSSQL), `NVL` (Oracle) |
| avoid dividing by zero | `a / NULLIF(b, 0)` | |
| inline if | `CASE WHEN c THEN a ELSE b END` | `IIF` (SQLite, MSSQL), `IF` (MySQL) |

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
NTILE(4)     OVER (ORDER BY salary DESC)                      -- quartiles 1–4           [13]
FIRST_VALUE(name) OVER (PARTITION BY dept ORDER BY salary DESC)  -- top value on every row  [13]
SUM(salary)  OVER ()                                          -- grand total on every row (percent of total)
AVG(amount)  OVER (ORDER BY d ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)   -- moving average [13]
LAG(x, 1, 0) OVER (ORDER BY month)                            -- previous row, 0 if none
```

Top N per group: `ROW_NUMBER()` in a CTE, then `WHERE rn = 1` (Snowflake, BigQuery, Oracle 26ai: `QUALIFY`). Use `DENSE_RANK` when ties count.

## Recursive CTE [12]

```sql
WITH RECURSIVE nums(n) AS (
  SELECT 1
  UNION ALL
  SELECT n + 1 FROM nums WHERE n < 10      -- always a stopping condition
)
SELECT n FROM nums;                         -- MSSQL/Oracle: WITH (no RECURSIVE)
```

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

```sql
INSERT INTO t (id, name) SELECT id, name FROM customers WHERE city = 'Fremont';   -- copy rows  [10]
INSERT INTO customers (id, name, city, age) VALUES (2, 'Leo', 'Berkeley', 28)
  ON CONFLICT (id) DO UPDATE SET city = excluded.city;     -- upsert (MySQL: ON DUPLICATE KEY UPDATE; MSSQL/Oracle: MERGE)
UPDATE employees SET salary = salary + 5000 WHERE department = 'Marketing' RETURNING name, salary;
TRUNCATE TABLE t;      -- empty the table fast (SQLite: DELETE FROM t)
```

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

## Interview patterns [18]

| Question | Pattern |
|---|---|
| Nth highest | `DENSE_RANK() OVER (ORDER BY x DESC)` in a CTE, `WHERE rnk = N` |
| second highest, NULL if none | `SELECT MAX(x) FROM t WHERE x < (SELECT MAX(x) FROM t)` |
| duplicates | `GROUP BY col HAVING COUNT(*) > 1` |
| pivot counts | `SUM(CASE WHEN c THEN 1 ELSE 0 END)` per column |
| pivot names | `ROW_NUMBER()` per group, then `MAX(CASE WHEN g = 'A' THEN name END)` ... `GROUP BY rn` |
| median | `ROW_NUMBER()` + `COUNT(*) OVER ()`, average rows `(n+1)/2` and `(n+2)/2` |
| change from last period | `total - LAG(total) OVER (ORDER BY month)` |
| consecutive days | date minus `ROW_NUMBER()` is constant within a streak; group by it |
| "every order is under 500" | `HAVING MAX(amount) < 500` |
| "bought all products" | `HAVING COUNT(DISTINCT product) = (SELECT COUNT(*) FROM products)` |
