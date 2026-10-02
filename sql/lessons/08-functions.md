# Lesson 8: Handy functions

**You'll learn:** `DISTINCT`, `LIKE`, number functions (`ROUND`, `FLOOR`, `CEIL`, `ABS`, `%`, `POWER`), integer division and `CAST`, text functions (`SUBSTR`, `INSTR`, `REPLACE`, `TRIM`…), NULL helpers (`COALESCE`, `NULLIF`), `GROUP_CONCAT`, and how each one is spelled in MySQL, PostgreSQL, MSSQL and Oracle.

## Key terms

- **DISTINCT:** removes duplicate rows from a result.
- **LIKE:** matches text against a pattern.
- **Wildcard:** a pattern character: `%` (any number of characters) or `_` (exactly one).
- **Function:** a named operation that takes values and returns one, like `UPPER(name)`.
- **Scalar function:** a function that works on one value per row (like `ROUND`), as opposed to an aggregate (like `SUM`), which works on many rows.
- **FLOOR / CEIL:** round **down** / **up** to a whole number.
- **Modulo (`%` or `MOD`):** the remainder after dividing. `7 % 3` is `1`.
- **Integer division:** dividing two whole numbers in some databases throws away the decimals: `7 / 2` gives `3`.
- **CAST:** converts a value to another type, like `CAST(years AS REAL)`.
- **COALESCE:** returns the first value that isn't NULL.
- **NULLIF(a, b):** returns NULL when `a` equals `b`, otherwise `a`. Used to avoid dividing by zero.
- **GROUP_CONCAT / STRING_AGG:** an aggregate that joins a group's text values into one string.

## Syntax

```sql
SELECT DISTINCT column FROM table;
SELECT COUNT(DISTINCT column) FROM table;
WHERE column LIKE 'pattern%'

-- numbers
ROUND(x, decimals)  FLOOR(x)  CEIL(x)  ABS(x)  x % y  POWER(x, y)  SQRT(x)  CAST(x AS type)

-- text
UPPER(x)  LOWER(x)  LENGTH(x)  x || y  SUBSTR(x, start, length)  INSTR(x, find)
REPLACE(x, find, with)  TRIM(x)

-- NULLs and lists
COALESCE(x, fallback)  NULLIF(x, value)  GROUP_CONCAT(x, ', ')
```

## DISTINCT: remove duplicates

```sql
SELECT DISTINCT city FROM customers;               -- Fremont, Oakland, San Jose
SELECT COUNT(DISTINCT city) FROM customers;        -- 3  (COUNT(city) would be 5)
```

`GROUP BY city` without an aggregate gives the same rows, but the two say different things:

| Use | When you mean |
|---|---|
| `DISTINCT` | "just remove the duplicates" |
| `GROUP BY` | "make groups so I can count/sum/average each one" |

`DISTINCT` applies to the **whole row**: `SELECT DISTINCT city, age` removes rows where both the city *and* the age repeat.

## LIKE: pattern matching

| Wildcard | Means | Example | Matches |
|---|---|---|---|
| `%` | any number of characters (even none) | `name LIKE 'A%'` | starts with A |
| `_` | exactly one character | `name LIKE '_e_'` | Leo |

`'A%'` = starts with A · `'%a'` = ends with a · `'%a%'` = contains a · `'___'` = exactly three characters

**Capital letters:** SQLite and MySQL's `LIKE` ignore case for English letters (`'a%'` matches `Ana`). PostgreSQL and Oracle are case-sensitive; PostgreSQL has `ILIKE` for case-insensitive matching, and `LOWER(name) LIKE 'a%'` works everywhere.

**Searching for a real `%` or `_`:** add an escape character: `WHERE code LIKE '%\_%' ESCAPE '\'` finds codes containing an underscore.

### Starts or ends with a vowel (a HackerRank favourite)

`LIKE` can't say "any of these letters", so either list them, or take the first letter with `SUBSTR` and use `IN`:

```sql
SELECT DISTINCT city FROM customers
WHERE LOWER(SUBSTR(city, 1, 1)) IN ('a', 'e', 'i', 'o', 'u');     -- starts with a vowel → Oakland
```

`SUBSTR(city, -1)` takes the **last** character, so `LOWER(SUBSTR(city, -1)) IN (...)` means "ends with a vowel". Other options: `city GLOB '[AEIOU]*'` (SQLite), `city REGEXP '^[aeiou]'` (MySQL), `city ~* '^[aeiou]'` (PostgreSQL), `REGEXP_LIKE(city, '^[aeiou]', 'i')` (Oracle, and MSSQL from SQL Server 2025).

## Number functions

| Function | Does | Example → Result |
|---|---|---|
| `ROUND(x, d)` | round to `d` decimals (0 if left out) | `ROUND(62333.333, 2)` → `62333.33` |
| `ROUND(x, -3)` | negative `d` rounds to tens, hundreds, thousands (MySQL, PostgreSQL, MSSQL, Oracle; SQLite leaves the number unchanged) | `ROUND(62333, -3)` → `62000` |
| `FLOOR(x)` | round **down** to a whole number | `FLOOR(4.9)` → `4`, `FLOOR(-4.1)` → `-5` |
| `CEIL(x)` / `CEILING(x)` | round **up** to a whole number | `CEIL(4.1)` → `5` |
| `ABS(x)` | drop the minus sign | `ABS(-250)` → `250` |
| `x % y` / `MOD(x, y)` | remainder | `7 % 3` → `1`; `years % 2 = 0` means even |
| `POWER(x, y)` | x to the power y | `POWER(2, 10)` → `1024` |
| `SQRT(x)` | square root | `SQRT(16)` → `4` |
| `SIGN(x)` | -1, 0 or 1 | `SIGN(-5)` → `-1` |

```sql
SELECT name,
  salary,
  FLOOR(salary / 1000.0)  AS thousands_down,   -- 62000 → 62
  CEIL(salary / 1000.0)   AS thousands_up,
  ABS(salary - 70000)     AS distance_from_70k
FROM employees;
```

### FLOOR, CEIL, ROUND and truncating: which is which?

| Value | `ROUND` | `FLOOR` (down) | `CEIL` (up) | truncate (cut off) |
|---|---|---|---|---|
| 4.5 | 5 | 4 | 5 | 4 |
| 4.4 | 4 | 4 | 5 | 4 |
| -4.5 | -5 | -5 | -4 | -4 |

**Truncating** means cutting off the decimals without rounding. It's spelled differently everywhere: `TRUNCATE(x, d)` in MySQL, `TRUNC(x, d)` in PostgreSQL and Oracle, `ROUND(x, d, 1)` in MSSQL, and `CAST(x AS INTEGER)` (whole numbers only) in SQLite. HackerRank's "truncate to 4 decimal places" questions mean this, not `ROUND`.

**"Round up" problems** use `CEIL`. A classic example is HackerRank's *The Blunder*: `CEIL(AVG(salary) - AVG(REPLACE(salary, '0', '')))`.

### Integer division: the silent bug

```sql
SELECT 7 / 2;          -- SQLite, PostgreSQL, MSSQL: 3   (whole numbers in, whole number out)
SELECT 7 / 2.0;        -- 3.5 everywhere
SELECT 7 * 1.0 / 2;    -- 3.5 everywhere
SELECT CAST(7 AS REAL) / 2;   -- 3.5 (PostgreSQL/MSSQL: CAST(7 AS DECIMAL(10,2)) or NUMERIC)
```

MySQL and Oracle return `3.5` for `7 / 2`, which is why the same query can give different answers on different databases. MySQL's `DIV` operator does whole-number division on purpose: `7 DIV 2` → `3`.

A percentage of two whole-number columns is the classic trap: `100 * part / total` can come out as 0 when part < total in SQLite, PostgreSQL or MSSQL. Write `100.0 * part / total`.

### CAST: change a value's type

```sql
SELECT CAST('42' AS INTEGER) + 1;      -- 43
SELECT CAST(3.99 AS INTEGER);          -- 3   (cuts off, doesn't round)
SELECT CAST(salary AS TEXT) || ' USD' FROM employees;
```

PostgreSQL also accepts the short form `'42'::integer`.

## Text functions

| Function | Does | Example → Result |
|---|---|---|
| `UPPER(x)` / `LOWER(x)` | change case | `UPPER('Maya')` → `MAYA` |
| `LENGTH(x)` | number of characters | `LENGTH('Maya')` → `4` |
| `x \|\| y` | join text | `name \|\| ' - ' \|\| city` → `Maya - Fremont` |
| `CONCAT(a, b, …)` | join text (NULLs count as empty) | `CONCAT(name, ' (', city, ')')` |
| `SUBSTR(x, start, length)` | part of the text; positions start at **1** | `SUBSTR('Fremont', 1, 3)` → `Fre` |
| `SUBSTR(x, -n)` | the last `n` characters | `SUBSTR('Fremont', -4)` → `mont` |
| `INSTR(x, find)` | position of `find` (0 if absent) | `INSTR('San Jose', ' ')` → `4` |
| `REPLACE(x, find, with)` | swap every match | `REPLACE('San Jose', ' ', '_')` → `San_Jose` |
| `TRIM(x)` / `LTRIM` / `RTRIM` | remove spaces at the ends | `TRIM('  Leo ')` → `Leo` |

`WHERE LOWER(city) = 'fremont'` matches regardless of capital letters.

Splitting at a character combines `SUBSTR` and `INSTR`: the first word of `'San Jose'` is `SUBSTR(city, 1, INSTR(city, ' ') - 1)`.

`'a' || NULL` is NULL: one missing piece blanks the whole result. `CONCAT` treats NULL as empty text instead (except in Oracle, where `||` already does).

## NULL helpers: COALESCE and NULLIF

```sql
SELECT c.name, COALESCE(o.product, 'No orders') AS product
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id;      -- Sam | No orders
```

`COALESCE(SUM(o.amount), 0)` shows 0 instead of NULL for customers with no orders. `COALESCE(a, b, c)` takes the first of any number of values that isn't NULL.

`NULLIF(x, 0)` turns a zero into NULL. Dividing by NULL gives NULL instead of an error, so it's the standard guard against **division by zero** (an error in PostgreSQL, MSSQL and Oracle; SQLite and MySQL quietly return NULL):

```sql
SELECT c.name,
  SUM(o.amount) * 1.0 / NULLIF(COUNT(o.order_id), 0) AS avg_order    -- Sam → NULL, not an error
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;
```

## GROUP_CONCAT: a group's values in one cell

```sql
SELECT department, GROUP_CONCAT(name, ', ' ORDER BY name) AS names
FROM employees
GROUP BY department;          -- Sales | Alice, Carla, Hank
```

| SQLite | MySQL | PostgreSQL / MSSQL | Oracle |
|---|---|---|---|
| `GROUP_CONCAT(x, ', ')` or `STRING_AGG(x, ', ')` | `GROUP_CONCAT(x ORDER BY x SEPARATOR ', ')` | `STRING_AGG(x, ', ')` (MSSQL: add `WITHIN GROUP (ORDER BY x)`) | `LISTAGG(x, ', ') WITHIN GROUP (ORDER BY x)` |

## The same functions in other databases

The sandbox runs SQLite. Most functions have the same name everywhere; these are the ones that don't:

| Task | SQLite | MySQL | PostgreSQL | MSSQL | Oracle |
|---|---|---|---|---|---|
| length | `LENGTH` | `CHAR_LENGTH` (`LENGTH` counts bytes) | `LENGTH` | `LEN` | `LENGTH` |
| join text | `a \|\| b`, `CONCAT` | `CONCAT(a, b)` (`\|\|` means OR by default) | `a \|\| b`, `CONCAT` | `a + b`, `CONCAT` | `a \|\| b`, `CONCAT` |
| part of text | `SUBSTR` | `SUBSTRING` / `SUBSTR` | `SUBSTRING` / `SUBSTR` | `SUBSTRING` | `SUBSTR` |
| first / last n chars | `SUBSTR(x, 1, n)` / `SUBSTR(x, -n)` | `LEFT` / `RIGHT` | `LEFT` / `RIGHT` | `LEFT` / `RIGHT` | `SUBSTR(x, 1, n)` / `SUBSTR(x, -n)` |
| find text | `INSTR(x, f)` | `INSTR` / `LOCATE(f, x)` | `POSITION(f IN x)` / `STRPOS` | `CHARINDEX(f, x)` | `INSTR` |
| pad | `printf('%05d', x)` | `LPAD(x, 5, '0')` | `LPAD` | `RIGHT('00000' + x, 5)` | `LPAD` |
| round up | `CEIL` | `CEIL` / `CEILING` | `CEIL` / `CEILING` | `CEILING` | `CEIL` |
| remainder | `%` | `%`, `MOD` | `%`, `MOD` | `%` | `MOD` |
| truncate decimals | `CAST(x AS INTEGER)` | `TRUNCATE(x, d)` | `TRUNC(x, d)` | `ROUND(x, d, 1)` | `TRUNC(x, d)` |
| `7 / 2` | `3` | `3.5` | `3` | `3` | `3.5` |
| replace NULL | `COALESCE`, `IFNULL` | `COALESCE`, `IFNULL` | `COALESCE` | `COALESCE`, `ISNULL` | `COALESCE`, `NVL` |
| inline if | `IIF(c, a, b)` | `IF(c, a, b)` | `CASE` only | `IIF(c, a, b)` | `CASE`, `DECODE` |
| bigger of two | `MAX(a, b)` | `GREATEST` | `GREATEST` | `GREATEST` (2022+) | `GREATEST` |

⚠️ **MSSQL averages whole-number columns as whole numbers:** `AVG(salary)` gives 62333, not 62333.33. Use `AVG(salary * 1.0)` for decimals. PostgreSQL's `AVG` of integers returns a decimal, so it's fine.

`COALESCE`, `CASE`, `NULLIF`, `ROUND`, `FLOOR`, `ABS`, `UPPER` and `LOWER` work everywhere, so prefer them.

## Common mistakes

- **Expecting `ROUND` when the question says "round up" or "round down".** Up is `CEIL`, down is `FLOOR`, and "truncate" is neither.
- **Integer division.** `100 * part / total` can give 0 in SQLite, PostgreSQL and MSSQL. Multiply by `100.0` or `1.0` first.
- **Counting positions from 0.** SQL text positions start at 1: `SUBSTR('Leo', 1, 1)` is `L`.
- **Joining text that might be NULL with `||`.** The whole result becomes NULL; wrap the column in `COALESCE(col, '')` or use `CONCAT`.
- **Using `LIKE 'a%'` in PostgreSQL for "starts with a or A".** It's case-sensitive there; use `ILIKE` or `LOWER()`.

## Exercises

1. The list of departments, each shown only once.
2. How many different cities do customers **who placed orders** live in?
3. Names of customers whose name ends with the letter a.
4. Each product and the length of its name, only for names longer than 5 characters.
5. Each department and its average salary, rounded to 0 decimal places.
6. Every customer's name and product, showing 'No orders' instead of NULL.
7. Every customer's name and total spent, showing 0 for customers with no orders.

**In the sandbox:** exercises 31–37.

### More practice: numbers, text and NULLs

8. Each employee's name and salary in thousands, rounded **down** (60000 → 60). Use `FLOOR`.
9. Each department and its average salary rounded **up** to the next whole thousand (62333.33 → 63000). Use `CEIL`.
10. Name and years of employees with an even number of years.
11. Each employee's name and how far their salary is from 70000, always as a positive number.
12. Each customer's name and a city code: the first three letters of their city in capitals.
13. Each customer's name and their city with spaces replaced by underscores.
14. Every customer's name and average order amount, using `NULLIF` so customers with no orders show NULL.
15. Each department and its employees' names in one text value, alphabetical, separated by `, `.
16. Each employee's name and half of their years as a decimal (3 years → 1.5).

**In the sandbox:** exercises 88–96.

<details>
<summary>Answers</summary>

```sql
-- 1
SELECT DISTINCT department FROM employees;

-- 2  → 2  (Sam in San Jose has no orders, so the JOIN drops him)
SELECT COUNT(DISTINCT c.city) AS num_cities
FROM customers c
JOIN orders o ON o.customer_id = c.id;

-- 3  → Maya, Priya, Ana
SELECT name FROM customers WHERE name LIKE '%a';

-- 4  → Laptop 6, Monitor 7, Keyboard 8
SELECT product, LENGTH(product) AS name_length
FROM orders
WHERE LENGTH(product) > 5;

-- 5
SELECT department, ROUND(AVG(salary)) AS avg_salary
FROM employees
GROUP BY department;

-- 6
SELECT c.name, COALESCE(o.product, 'No orders') AS product
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id;

-- 7
SELECT c.name, COALESCE(SUM(o.amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;

-- 8  → Alice 60, Bob 95, Carla 55, Dev 105, ...
SELECT name, FLOOR(salary / 1000.0) AS salary_k
FROM employees;

-- 9  → Engineering 96000, Marketing 66000, Sales 63000
SELECT department, CEIL(AVG(salary) / 1000.0) * 1000 AS avg_salary_rounded_up
FROM employees
GROUP BY department;

-- 10  → Dev 8, Emma 4, Frank 2, Grace 6
SELECT name, years
FROM employees
WHERE years % 2 = 0;

-- 11  → Emma 0, Hank 2000, Grace 8000, ...
SELECT name, ABS(salary - 70000) AS distance_from_70k
FROM employees;

-- 12  → Maya FRE, Leo OAK, Sam SAN, ...
SELECT name, UPPER(SUBSTR(city, 1, 3)) AS city_code
FROM customers;

-- 13  → Sam San_Jose
SELECT name, REPLACE(city, ' ', '_') AS city_slug
FROM customers;

-- 14  → Maya 612.5, Leo 300, Priya 97.5, Sam NULL, Ana 240
SELECT c.name,
  SUM(o.amount) * 1.0 / NULLIF(COUNT(o.order_id), 0) AS avg_order
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;

-- 15  → Engineering: Bob, Dev, Frank · Marketing: Emma, Grace · Sales: Alice, Carla, Hank
SELECT department, GROUP_CONCAT(name, ', ' ORDER BY name) AS names
FROM employees
GROUP BY department;

-- 16  → Alice 1.5, Bob 2.5, Carla 0.5, ...   (years / 2 would give 1, 2, 0: integer division)
SELECT name, years / 2.0 AS half_years
FROM employees;
```
</details>

---
Previous: [Lesson 7](07-case.md) · Next: [Lesson 9: Dates](09-dates.md)
