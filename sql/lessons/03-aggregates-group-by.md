# Lesson 3: Counting and math with aggregates

**You'll learn:** `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `AS`, and `GROUP BY`.

## Key terms

- **Aggregate function:** turns many rows into one value (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).
- **Alias:** a name for a result column, given with `AS`.
- **GROUP BY:** splits rows into groups so aggregates are calculated per group.
- **NULL:** "no value." `COUNT(column)` skips it; `COUNT(*)` doesn't.

## Syntax

```sql
SELECT group_column, AGGREGATE(column) AS alias
FROM table_name
WHERE row_condition
GROUP BY group_column
ORDER BY alias;
```

## Aggregate functions

Normal queries return individual rows. **Aggregate functions** squash many rows into one answer.

| Function | Does |
|---|---|
| `COUNT()` | how many rows |
| `SUM()` | adds up a column |
| `AVG()` | average of a column |
| `MIN()` | smallest value |
| `MAX()` | largest value |

```sql
SELECT COUNT(*) FROM customers;                          -- 5
SELECT AVG(age) FROM customers;                          -- 34.6
SELECT COUNT(*) FROM customers WHERE city = 'Oakland';   -- 2 (WHERE filters first, then it counts)
```

## COUNT(*) vs COUNT(column)

- `COUNT(*)` counts **every row**.
- `COUNT(age)` counts rows where `age` **has a value**, skipping `NULL` (unknown).

For "how many customers…" questions, `COUNT(*)` is the usual choice.

## MIN/MAX vs ORDER BY + LIMIT

- `SELECT MIN(age) FROM customers` answers "**what** is the youngest age?" → 19
- `SELECT name FROM customers ORDER BY age LIMIT 1` answers "**who** is the youngest?" → Sam

## AS: naming a result column

```sql
SELECT AVG(age) AS average_age FROM customers;
```

## GROUP BY: one answer per group

```sql
SELECT city, COUNT(*) AS num_customers
FROM customers
GROUP BY city;
```

| city     | num_customers |
|----------|---------------|
| Fremont  | 2             |
| Oakland  | 2             |
| San Jose | 1             |

Think of it as sorting rows into piles by city, then counting each pile. A question that says **"for each ___"** or **"per ___"** puts that ___ in `GROUP BY` and in `SELECT`.

## ⚠️ The GROUP BY rule

> Once you write `GROUP BY`, every other column in `SELECT`, `HAVING`, and `ORDER BY` must either be the grouped column or be inside an aggregate.

`SELECT department, salary FROM employees GROUP BY department` is wrong: Sales has three salaries, so which one should SQL show? Wrap it: `AVG(salary)`, `MAX(salary)`, and so on.

**SQLite (and old MySQL) don't always stop you.** They quietly pick a value from some row, which *looks* like a real answer. MSSQL, Oracle, and PostgreSQL give an error. So don't rely on the database; follow the rule.

## Clause order

```
SELECT → FROM → WHERE → GROUP BY → ORDER BY → LIMIT
```

## Common mistakes

- **Aggregates in `WHERE`.** `WHERE AVG(age) > 30` fails: `WHERE` looks at one row at a time, before any math. (Lesson 4 fixes this with `HAVING`.)
- **`COUNT` vs `SUM`.** "How many" is `COUNT`. "Total amount" is `SUM`.
- **SQLite's `TOTAL()`** exists and adds values up like `SUM`, so a typo like `TOTAL(customer_id)` runs and gives meaningless numbers. Other databases don't have it.

## Exercises

1. How many customers are older than 30?
2. The age of the youngest customer.
3. The average age in each city.
4. The total of all ages for customers not in Fremont, with the column named `total_age`.

**In the sandbox:** exercises 3 and 6.

<details>
<summary>Answers</summary>

```sql
-- 1  → 3
SELECT COUNT(*) FROM customers WHERE age > 30;

-- 2  → 19
SELECT MIN(age) FROM customers;

-- 3  → Fremont 37.5, Oakland 39.5, San Jose 19
SELECT city, AVG(age) AS average_age
FROM customers
GROUP BY city;

-- 4  → 98
SELECT SUM(age) AS total_age FROM customers WHERE city != 'Fremont';
```
</details>

---
Previous: [Lesson 2](02-filtering-sorting.md) · Next: [Lesson 4: HAVING](04-having.md)
