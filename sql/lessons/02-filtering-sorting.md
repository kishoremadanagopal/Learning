# Lesson 2: Combining conditions, sorting and limiting

**You'll learn:** `AND`, `OR`, `NOT`, `IN`, `BETWEEN`, `ORDER BY` (several columns, expressions and NULLs), `ASC`/`DESC`, `LIMIT` and `OFFSET`, and which clauses are optional.

## Key terms

- **AND / OR:** combine conditions. `AND` needs both true; `OR` needs either.
- **IN:** tests whether a value is in a list.
- **ORDER BY:** sorts the result.
- **ASC / DESC:** ascending (the default) or descending sort order.
- **LIMIT:** caps how many rows come back.
- **Top N:** the first N rows after sorting, from `ORDER BY` + `LIMIT`.
- **BETWEEN:** tests whether a value lies in a range, **including** both ends.
- **OFFSET:** skips a number of rows before `LIMIT` starts counting.
- **Tie-breaker:** a second sort column that decides the order when the first column has equal values.

## Syntax

```sql
SELECT columns
FROM table_name
WHERE condition1 AND (condition2 OR condition3)
ORDER BY column [ASC | DESC], column2 [ASC | DESC]
LIMIT number;
```

## AND / OR

```sql
SELECT name FROM customers
WHERE city = 'Fremont' AND age > 35;      -- both must be true → Priya
```

```sql
SELECT name FROM customers
WHERE city = 'San Jose' OR age > 50;      -- either can be true → Sam, Ana
```

When you mix them, use parentheses to make the meaning clear:

```sql
WHERE (city = 'Fremont' OR city = 'Oakland') AND age < 40
```

## IN: a shortcut for several ORs

```sql
WHERE city IN ('Fremont', 'San Jose')
```

Each text value still needs its own quotes.

## NOT, NOT IN and BETWEEN

`NOT` flips any condition:

```sql
WHERE city NOT IN ('Fremont', 'San Jose')        -- Leo, Ana
WHERE NOT (city = 'Oakland' AND age > 30)
```

`BETWEEN low AND high` includes **both** ends, so it's the same as `>= low AND <= high`:

```sql
SELECT name, salary FROM employees
WHERE salary BETWEEN 60000 AND 75000;            -- Alice 60000, Grace, Emma, Hank 72000
```

Put the smaller value first: `BETWEEN 75000 AND 60000` matches nothing. To test for missing values, use `IS NULL` / `IS NOT NULL` (Lesson 5), never `= NULL`.

## ORDER BY: sorting

```sql
SELECT name, age FROM customers
ORDER BY age;          -- youngest first (ascending is the default)
```

Add `DESC` for the reverse: `ORDER BY age DESC`.

- **ASC** = ascending = climbing up (1, 2, 3… or A, B, C…)
- **DESC** = descending = going down (3, 2, 1… or Z, Y, X…)

`ORDER BY` always needs a column: `ORDER BY name`, never just `ORDER BY DESC`.

### Several columns: tie-breakers

```sql
SELECT name, city, age FROM customers
ORDER BY city, age DESC;     -- by city A→Z; within each city, oldest first
```

Each column has its own direction: `ORDER BY city, age DESC` sorts the city ascending and only the age descending.

### Sorting by a calculation

You can sort by an expression, not just a column. "The shortest city name, alphabetically first if there's a tie" (a HackerRank classic):

```sql
SELECT city, LENGTH(city) AS len
FROM customers
ORDER BY LENGTH(city), city
LIMIT 1;                     -- Fremont 7 (Oakland is 7 letters too; `city` breaks the tie)
```

Most databases also let you sort by a column alias (`ORDER BY len`) or by position (`ORDER BY 2`), but positions break when someone adds a column, so prefer names.

### Where do NULLs go?

When the sort column has missing values, databases disagree about where they go:

| Database | NULLs with `ASC` |
|---|---|
| SQLite, MySQL, MSSQL | first |
| PostgreSQL, Oracle | last |

Say what you want with `NULLS FIRST` / `NULLS LAST` (SQLite 3.30+, PostgreSQL, Oracle): `ORDER BY order_date DESC NULLS LAST`. MySQL and MSSQL don't have it; use `ORDER BY col IS NULL, col` (MySQL) or a `CASE` in the `ORDER BY`.

## LIMIT: how many rows come back

```sql
SELECT name, age FROM customers
ORDER BY age DESC
LIMIT 2;               -- the two oldest: Ana, Priya
```

**`ORDER BY` + `LIMIT` = "top N" or "bottom N."** It's one of the most useful patterns in SQL.

## OFFSET: skipping rows

`OFFSET n` skips the first `n` rows. It's how websites show "page 2", and how you get "the second highest":

```sql
SELECT name, age FROM customers
ORDER BY age DESC
LIMIT 1 OFFSET 1;      -- skip the oldest, take the next: Priya 41
```

Page 3 of a list with 10 per page is `LIMIT 10 OFFSET 20`.

⚠️ `OFFSET` counts **rows**, not distinct values. If two people tie for oldest, `OFFSET 1` returns the other one, not the next-oldest age. Lesson 18 shows the tie-safe way.

A handy memory trick: `ORDER BY` and `GROUP BY` take a **column** ("by *what*?"), while `LIMIT` takes a **number** ("how *many*?"). So it's `LIMIT 2`, never `LIMIT BY 2`.

## Which clauses are required?

| Clause | Required? | If you leave it out |
|---|---|---|
| `SELECT` | Yes | nothing works |
| `FROM` | Yes (when reading a table) | SQL doesn't know where the data is |
| `WHERE` | No | all rows are included |
| `ORDER BY` | No | rows come back in no guaranteed order |
| `LIMIT` | No | all matching rows come back |

Whichever clauses you use must appear in this order:

```
SELECT → FROM → WHERE → ORDER BY → LIMIT → OFFSET
```

## Don't hardcode from the data

To find the youngest customer, `WHERE age < 20` happens to return Sam, but only because you looked at the data first. Add a 17-year-old and it breaks. Let SQL find it instead:

```sql
SELECT name FROM customers ORDER BY age LIMIT 1;
```

## In MSSQL and Oracle

`LIMIT` doesn't exist in MSSQL or Oracle:

| Database | Youngest customer |
|---|---|
| SQLite / MySQL / PostgreSQL | `SELECT name FROM customers ORDER BY age LIMIT 1;` |
| MSSQL | `SELECT TOP 1 name FROM customers ORDER BY age;` |
| Oracle | `SELECT name FROM customers ORDER BY age FETCH FIRST 1 ROWS ONLY;` |

Skipping rows works like this:

| Database | Second-youngest customer |
|---|---|
| SQLite / MySQL / PostgreSQL | `... ORDER BY age LIMIT 1 OFFSET 1` |
| MSSQL | `... ORDER BY age OFFSET 1 ROWS FETCH NEXT 1 ROWS ONLY` |
| Oracle, PostgreSQL | `... ORDER BY age OFFSET 1 ROWS FETCH FIRST 1 ROWS ONLY` |

`FETCH FIRST n ROWS ONLY` is the official SQL standard, so it also works in PostgreSQL and in MSSQL (with `OFFSET 0 ROWS` before it). Add `WITH TIES` (PostgreSQL 13+, Oracle) to include rows tied with the last one: MSSQL writes `TOP 1 WITH TIES`.

## Common mistakes

- `SORT BY` → it's `ORDER BY`
- `DEC`, `Assen` → it's `DESC`, `ASC`
- `LIMIT BY 2` → it's `LIMIT 2`
- `IN (Fremont, San Jose)` → text needs quotes: `IN ('Fremont', 'San Jose')`
- `ASC` when the question says "oldest first": read the direction carefully
- `ORDER BY city, age DESC` expecting both columns to be descending: `DESC` applies only to the column right before it
- `BETWEEN 75000 AND 60000`: the smaller value must come first

## Exercises

1. Names of people in Oakland who are older than 30.
2. Name and city of everyone in Fremont or San Jose, sorted alphabetically by name.
3. The name of the single youngest customer.
4. Names and ages of everyone, oldest first.
5. Every column for the customer whose id is 3.
6. Names of people aged 25 or older who live in Fremont.
7. Names of people who live in Oakland **or** are younger than 20, sorted alphabetically.
8. Name and city of the **two youngest** people who are **not** in Fremont.

**In the sandbox:** exercises 2 and 5.

### More practice

9. The customer with the longest name, and its length.
10. The name and age of the **second-oldest** customer, using `OFFSET`.
11. Name and salary of employees earning between 60000 and 75000 (both included), lowest salary first.

**In the sandbox:** exercises 80–82.

<details>
<summary>Answers</summary>

```sql
-- 1  → Ana
SELECT name FROM customers WHERE city = 'Oakland' AND age > 30;

-- 2  → Maya, Priya, Sam
SELECT name, city FROM customers
WHERE city IN ('Fremont', 'San Jose')
ORDER BY name;

-- 3  → Sam
SELECT name FROM customers ORDER BY age LIMIT 1;

-- 4
SELECT name, age FROM customers ORDER BY age DESC;

-- 5  → Priya
SELECT * FROM customers WHERE id = 3;

-- 6  → Maya, Priya
SELECT name FROM customers WHERE city = 'Fremont' AND age >= 25;

-- 7  → Ana, Leo, Sam
SELECT name FROM customers
WHERE city = 'Oakland' OR age < 20
ORDER BY name;

-- 8  → Sam, Leo
SELECT name, city FROM customers
WHERE city <> 'Fremont'
ORDER BY age
LIMIT 2;

-- 9  → Priya 5
SELECT name, LENGTH(name) AS name_length
FROM customers
ORDER BY LENGTH(name) DESC, name
LIMIT 1;

-- 10  → Priya 41
SELECT name, age FROM customers
ORDER BY age DESC
LIMIT 1 OFFSET 1;

-- 11  → Alice 60000, Grace 62000, Emma 70000, Hank 72000
SELECT name, salary FROM employees
WHERE salary BETWEEN 60000 AND 75000
ORDER BY salary;
```
</details>

---
Previous: [Lesson 1](01-first-queries.md) · Next: [Lesson 3: Aggregates and GROUP BY](03-aggregates-group-by.md)
