# Lesson 8: Handy functions

**You'll learn:** `DISTINCT`, `LIKE`, text functions, `ROUND`, and `COALESCE`.

## Key terms

- **DISTINCT:** removes duplicate rows from a result.
- **LIKE:** matches text against a pattern.
- **Wildcard:** a pattern character: `%` (any number of characters) or `_` (exactly one).
- **Function:** a named operation that takes values and returns one, like `UPPER(name)`.
- **COALESCE:** returns the first value that isn't NULL.

## Syntax

```sql
SELECT DISTINCT column FROM table;
SELECT COUNT(DISTINCT column) FROM table;
WHERE column LIKE 'pattern%'
UPPER(x)   LOWER(x)   LENGTH(x)   x || y   ROUND(x, decimals)   COALESCE(x, fallback)
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

## LIKE: pattern matching

| Wildcard | Means | Example | Matches |
|---|---|---|---|
| `%` | any number of characters (even none) | `name LIKE 'A%'` | starts with A |
| `_` | exactly one character | `name LIKE '_e_'` | Leo |

`'A%'` = starts with A · `'%a'` = ends with a · `'%a%'` = contains a

## Text functions

| Function | Does | Example → Result |
|---|---|---|
| `UPPER(x)` / `LOWER(x)` | change case | `UPPER('Maya')` → `MAYA` |
| `LENGTH(x)` | number of characters | `LENGTH('Maya')` → `4` |
| `x \|\| y` | join text | `name \|\| ' - ' \|\| city` → `Maya - Fremont` |

`WHERE LOWER(city) = 'fremont'` matches regardless of capital letters.

## ROUND

```sql
SELECT department, ROUND(AVG(salary), 2) AS avg_salary
FROM employees GROUP BY department;       -- Sales 62333.33
```

## COALESCE: replace NULL with something readable

```sql
SELECT c.name, COALESCE(o.product, 'No orders') AS product
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id;      -- Sam | No orders
```

`COALESCE(SUM(o.amount), 0)` shows 0 instead of NULL for customers with no orders.

## In MSSQL, MySQL and Oracle

| SQLite | MSSQL | MySQL | Oracle |
|---|---|---|---|
| `LENGTH(x)` | `LEN(x)` | `LENGTH(x)` | `LENGTH(x)` |
| `a \|\| b` | `a + b` or `CONCAT(a, b)` | `CONCAT(a, b)` | `a \|\| b` |
| `COALESCE(x, 0)` | `COALESCE` or `ISNULL` | `COALESCE` or `IFNULL` | `COALESCE` or `NVL` |

⚠️ **MSSQL averages whole-number columns as whole numbers:** `AVG(salary)` gives 62333, not 62333.33. Use `AVG(salary * 1.0)` for decimals.

`COALESCE` works everywhere, so prefer it.

## Exercises

1. The list of departments, each shown only once.
2. How many different cities do customers **who placed orders** live in?
3. Names of customers whose name ends with the letter a.
4. Each product and the length of its name, only for names longer than 5 characters.
5. Each department and its average salary, rounded to 0 decimal places.
6. Every customer's name and product, showing 'No orders' instead of NULL.
7. Every customer's name and total spent, showing 0 for customers with no orders.

**In the sandbox:** exercises 31–37.

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
```
</details>

---
Previous: [Lesson 7](07-case.md) · Next: [Lesson 9: Dates](09-dates.md)
