# Lesson 6: Subqueries, a query inside a query

**You'll learn:** subqueries that return one value, subqueries that return a list, and `IN` / `NOT IN`.

## Key terms

- **Subquery:** a query in parentheses inside another query. It runs first.
- **Outer query:** the main query that uses the subquery's result.

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

## Exercises

1. Names and ages of customers older than the average customer age.
2. Name and salary of the employee(s) with the lowest salary.
3. Names of customers who have placed at least one order, using `IN`.
4. Names of employees who earn more than the average salary **of the Sales department**.

**In the sandbox:** exercises 17–20.

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
```
</details>

---
Previous: [Lesson 5](05-joins.md) · Next: [Lesson 7: CASE](07-case.md)
