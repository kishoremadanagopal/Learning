# Lesson 5: JOINs, combining tables

**You'll learn:** `JOIN ... ON`, table aliases, `LEFT`/`RIGHT`/`FULL OUTER`/`CROSS JOIN`, `NULL`, self joins, joins on a range (non-equi joins) and `USING`.

## Key terms

- **JOIN:** combines rows from two tables.
- **ON:** the condition saying how rows of the two tables match.
- **Primary key:** a column that uniquely identifies each row (`customers.id`).
- **Foreign key:** a column that points to another table's primary key (`orders.customer_id`).
- **INNER JOIN:** keeps only rows that match in both tables.
- **LEFT JOIN:** keeps every row of the first table, with NULL where nothing matches.
- **Table alias:** a short name for a table, like `c` for `customers`.
- **NULL:** "no value." Test for it with `IS NULL`, never `= NULL`.
- **Self join:** a table joined to itself, using two different aliases.
- **Non-equi join:** a join whose `ON` uses something other than `=`, like `BETWEEN`.

## Syntax

```sql
SELECT a.column, b.column
FROM table_a a
[INNER | LEFT | RIGHT | FULL OUTER] JOIN table_b b
  ON b.foreign_key = a.primary_key
WHERE ...;
```

## Why tables are split

Real databases split data so nothing is stored twice: customer details in `customers`, orders in `orders`. The link is **`orders.customer_id` = `customers.id`**.

- `customers.id` is a **primary key**: it uniquely identifies each customer.
- `orders.customer_id` is a **foreign key**: it points to a customer's primary key.

## INNER JOIN

```sql
SELECT customers.name, orders.product
FROM customers
JOIN orders ON orders.customer_id = customers.id;
```

- `FROM customers JOIN orders` combines the two tables.
- `ON ...` says **how rows match**.
- `table.column` says which table a column comes from.

Maya appears twice (two orders), and **Sam is missing**, because `JOIN` (also written `INNER JOIN`) keeps only rows with a match in **both** tables.

## Table aliases

```sql
SELECT c.name, o.product, o.amount
FROM customers c
JOIN orders o ON o.customer_id = c.id;
```

**Every alias must be declared right after its table name.** Using `c.name` without writing `FROM customers c` gives `no such column: c.name`. Keep the same capitalization everywhere (`o`, not `O` in one place and `o` in another).

## LEFT JOIN: keep everyone from the first table

```sql
SELECT c.name, o.product
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id;
```

Now Sam appears, with `NULL` as his product. `NULL` means "no value."

## Finding rows with no match

```sql
SELECT c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.order_id IS NULL;          -- → Sam
```

- It's **`IS NULL`**, never `= NULL`. Comparing anything to `NULL` with `=` never matches.
- `'NULL'` in quotes is just the text N-U-L-L.
- Check a column from the **right-hand** table (`o.order_id`), since that's the side that becomes `NULL`.

## The whole join family

| Join | Matched rows | Left-only rows | Right-only rows |
|---|---|---|---|
| `INNER JOIN` | ✓ | dropped | dropped |
| `LEFT JOIN` | ✓ | ✓ | dropped |
| `RIGHT JOIN` | ✓ | dropped | ✓ |
| `FULL OUTER JOIN` | ✓ | ✓ | ✓ |
| `CROSS JOIN` | every row paired with every row, no `ON` |

"Outer" means "also keep the leftovers." `LEFT JOIN` and `LEFT OUTER JOIN` are the same thing. Most people use `LEFT JOIN` with the "keep everything" table first, rather than `RIGHT JOIN`.

A `CROSS JOIN` of 5 customers and 7 orders gives 35 rows. Forgetting the `ON` condition is a classic way to create one by accident.

## JOIN + everything else

```sql
SELECT c.name, SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
ORDER BY total_spent DESC;
```

Clause order:
```
SELECT → FROM → JOIN ... ON → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
```

## Self joins: a table joined to itself

Sometimes the rows you need to compare are in the **same** table: pairs of employees in the same department, customers in the same city, a manager and the people who report to them. Join the table to itself, giving it two different aliases:

```sql
SELECT a.name AS higher_paid, b.name AS lower_paid, a.department
FROM employees a
JOIN employees b
  ON a.department = b.department     -- same department
 AND a.salary > b.salary;            -- a earns more than b
```

| higher_paid | lower_paid | department |
|---|---|---|
| Dev | Bob | Engineering |
| Dev | Frank | Engineering |
| Bob | Frank | Engineering |
| Emma | Grace | Marketing |
| … | … | … |

`a.salary > b.salary` also stops each person being paired with themselves, and stops every pair appearing twice. To list pairs without comparing values, use `a.id < b.id` for the same effect. Classic uses: an `employees` table with a `manager_id` column (`JOIN employees m ON e.manager_id = m.id`), and HackerRank's *Symmetric Pairs*.

## Non-equi joins: matching on a range

`ON` doesn't have to use `=`. Any condition works, such as `BETWEEN`, which matches each row to a range in another table (a grade band, a tax bracket, a price tier):

```sql
WITH bands(band, low, high) AS (
  VALUES ('A', 90000, 999999), ('B', 70000, 89999), ('C', 0, 69999)
)
SELECT e.name, e.salary, b.band
FROM employees e
JOIN bands b ON e.salary BETWEEN b.low AND b.high;     -- Dev A, Frank B, Alice C, ...
```

The `WITH bands(...) AS (VALUES ...)` part builds a small table on the fly (CTEs are Lesson 12). HackerRank's *The Report* is exactly this pattern: students joined to grades with `marks BETWEEN min_mark AND max_mark`.

## USING and NATURAL JOIN

When the key column has the **same name** in both tables, `JOIN orders USING (customer_id)` is a shorter `ON`. It works in SQLite, MySQL, PostgreSQL and Oracle (not MSSQL). Avoid `NATURAL JOIN`, which silently joins on every column with a matching name, so adding a column can change your results.

## In Oracle

Oracle doesn't allow `AS` before a **table** alias: write `FROM customers c`, not `FROM customers AS c`. Writing aliases without `AS` works in every database.

## Exercises

1. Each order's product and amount, with the name of the customer who placed it.
2. Products ordered by customers who live in Fremont.
3. Each customer's name and how many orders they placed (only customers with orders).
4. Every customer's name and product, **including** customers with no orders.
5. Names of customers who have never placed an order.
6. Each customer's name and total spent, highest first.

**In the sandbox:** exercises 11–16.

### More practice

7. Every pair of employees in the same department where the first earns more than the second: higher_paid, lower_paid, department.
8. Each employee's pay band, using the `bands` CTE above and `JOIN ... ON salary BETWEEN low AND high`.

**In the sandbox:** exercises 83–84.

<details>
<summary>Answers</summary>

```sql
-- 1
SELECT o.product, o.amount, c.name
FROM customers c
JOIN orders o ON o.customer_id = c.id;

-- 2  → Laptop, Mouse, Chair, Lamp
SELECT o.product
FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE c.city = 'Fremont';

-- 3  → Ana 2, Leo 1, Maya 2, Priya 2
SELECT c.name, COUNT(*) AS num_orders
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;

-- 4
SELECT c.name, o.product
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id;

-- 5  → Sam
SELECT c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.order_id IS NULL;

-- 6  → Maya 1225, Ana 480, Leo 300, Priya 195
SELECT c.name, SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
ORDER BY total_spent DESC;

-- 7  → 7 pairs: Dev>Bob, Dev>Frank, Bob>Frank, Emma>Grace, Hank>Alice, Hank>Carla, Alice>Carla
SELECT a.name AS higher_paid, b.name AS lower_paid, a.department
FROM employees a
JOIN employees b
  ON a.department = b.department
 AND a.salary > b.salary;

-- 8  → A: Bob, Dev · B: Emma, Frank, Hank · C: Alice, Carla, Grace
WITH bands(band, low, high) AS (
  VALUES ('A', 90000, 999999), ('B', 70000, 89999), ('C', 0, 69999)
)
SELECT e.name, e.salary, b.band
FROM employees e
JOIN bands b ON e.salary BETWEEN b.low AND b.high;
```
</details>

---
Previous: [Lesson 4](04-having.md) · Next: [Lesson 6: Subqueries](06-subqueries.md)
