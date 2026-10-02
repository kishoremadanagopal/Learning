# Lesson 6: Subqueries, a query inside a query

**You'll learn:** subqueries that return one value or a list, `IN` / `NOT IN` (and its NULL trap), correlated subqueries, `EXISTS` / `NOT EXISTS`, and subqueries in `FROM` and `SELECT`.

## Key terms

- **Subquery:** a query in parentheses inside another query. It runs first.
- **Outer query:** the main query that uses the subquery's result.
- **Correlated subquery:** a subquery that refers to the outer query's current row, so it runs once per row.
- **EXISTS:** true if a subquery returns at least one row.
- **Derived table:** a subquery in `FROM`, used like a temporary table.

## Syntax

```sql
-- subquery returning one value
SELECT ... FROM table WHERE column > (SELECT AGGREGATE(column) FROM table);

-- subquery returning a list
SELECT ... FROM table WHERE column IN (SELECT column FROM other_table);
```

## Why subqueries

"Who earns more than the average?" takes two steps: first work out the average, then compare everyone to it. This fails, because aggregates can't go in `WHERE`:

```sql
SELECT name FROM employees WHERE salary > AVG(salary);   -- error
```

A subquery does step one in parentheses, and SQL runs it first:

```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

1. The inner query gives **75875**.
2. The outer query becomes `WHERE salary > 75875` → Bob, Dev, Frank.

## Finding the whole row for a MIN or MAX

```sql
SELECT name, salary
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);   -- Dev, 105000
```

Unlike `ORDER BY ... LIMIT 1`, this returns **everyone** tied for the top.

## Subqueries that return a list: IN

```sql
SELECT name
FROM customers
WHERE id IN (SELECT customer_id FROM orders WHERE amount > 200);   -- Maya, Leo, Ana
```

`NOT IN` flips it:

```sql
SELECT name FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);   -- Sam
```

That's the same answer as `LEFT JOIN ... IS NULL` in Lesson 5. Many questions have more than one correct solution.

## Rules

- A subquery always goes in **parentheses**.
- **One value** (`AVG`, `MAX`, `MIN`) → compare with `=`, `>`, `<`.
- **A list** → use `IN` / `NOT IN`.
- The subquery should select **one column**.
- Write and run the inner query on its own first, then wrap it.

## ⚠️ The NOT IN trap: NULLs

If the subquery's list contains even one `NULL`, `NOT IN` returns **no rows at all**. `x NOT IN (1, 2, NULL)` means "x isn't 1, isn't 2, and isn't unknown", and "isn't unknown" is never definitely true. So if `orders.customer_id` had a NULL, the "customers with no orders" query above would silently return nothing.

Safe versions: add `WHERE customer_id IS NOT NULL` inside the subquery, or use `NOT EXISTS` (below), which handles NULLs correctly.

## Correlated subqueries: one per row

A **correlated** subquery refers to a column from the outer query, so it's worked out again for every outer row. "Employees who earn the most **in their own department**":

```sql
SELECT e.name, e.department, e.salary
FROM employees e
WHERE e.salary = (
  SELECT MAX(e2.salary)
  FROM employees e2
  WHERE e2.department = e.department      -- the current row's department
);                                         -- Dev, Emma, Hank
```

Read it row by row: for Alice (Sales), the inner query finds the highest Sales salary (72000); Alice's 60000 isn't equal, so she's skipped. For Hank, it's equal, so he's kept. The aliases (`e` and `e2`) are essential: they say which `employees` each column comes from.

## EXISTS and NOT EXISTS

`EXISTS (subquery)` is true when the subquery finds **at least one row**. It doesn't care what the rows contain, which is why people write `SELECT 1` inside:

```sql
-- customers with at least one order over 200
SELECT c.name
FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.id AND o.amount > 200
);                                         -- Maya, Leo, Ana

-- customers with no orders at all
SELECT c.name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.id
);                                         -- Sam
```

`NOT EXISTS` is the standard way to write "has no matching rows" (an **anti-join**). It's NULL-safe and usually as fast as `LEFT JOIN ... IS NULL`.

## Subqueries in FROM and SELECT

A subquery in `FROM` is a **derived table**: a temporary result you query like a table. It needs an alias:

```sql
SELECT AVG(total) AS avg_customer_spend
FROM (
  SELECT customer_id, SUM(amount) AS total
  FROM orders
  GROUP BY customer_id
) AS per_customer;                         -- 550: the average of the four customers' totals
```

A subquery in `SELECT` must return one value per row:

```sql
SELECT name,
  (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS num_orders
FROM customers c;                          -- Sam 0, unlike a plain JOIN
```

Lesson 12's CTEs do the same job as derived tables, but read more clearly when there are several steps.

## ANY and ALL

`salary > ALL (SELECT salary FROM employees WHERE department = 'Sales')` means "more than every Sales salary"; `> ANY (...)` means "more than at least one". They work in MySQL, PostgreSQL, MSSQL and Oracle, but **not SQLite**. Use `> (SELECT MAX(...))` and `> (SELECT MIN(...))` instead, which work everywhere.

## Exercises

1. Names and ages of customers older than the average customer age.
2. Name and salary of the employee(s) with the lowest salary.
3. Names of customers who have placed at least one order, using `IN`.
4. Names of employees who earn more than the average salary **of the Sales department**.

**In the sandbox:** exercises 17–20.

### More practice

5. Names of customers who have placed an order over 200, using `EXISTS`.
6. The top earner in each department (name, department, salary), using a correlated subquery.
7. Names of customers who have never placed an order, using `NOT EXISTS`.

**In the sandbox:** exercises 85–87.

<details>
<summary>Answers</summary>

```sql
-- 1  → Priya 41, Ana 52
SELECT name, age FROM customers
WHERE age > (SELECT AVG(age) FROM customers);

-- 2  → Carla 55000
SELECT name, salary FROM employees
WHERE salary = (SELECT MIN(salary) FROM employees);

-- 3  → Maya, Leo, Priya, Ana
SELECT name FROM customers
WHERE id IN (SELECT customer_id FROM orders);

-- 4  → Bob, Dev, Emma, Frank, Hank
SELECT name FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees WHERE department = 'Sales');

-- 5  → Maya, Leo, Ana
SELECT c.name
FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.id AND o.amount > 200
);

-- 6  → Dev, Emma, Hank
SELECT e.name, e.department, e.salary
FROM employees e
WHERE e.salary = (
  SELECT MAX(e2.salary) FROM employees e2
  WHERE e2.department = e.department
);

-- 7  → Sam
SELECT c.name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```
</details>

---
Previous: [Lesson 5](05-joins.md) · Next: [Lesson 7: CASE](07-case.md)
