# Lesson 2: Combining conditions, sorting and limiting

**You'll learn:** `AND`, `OR`, `IN`, `ORDER BY`, `ASC`/`DESC`, `LIMIT`, and which clauses are optional.

## Key terms

- **AND / OR:** combine conditions. `AND` needs both true; `OR` needs either.
- **IN:** tests whether a value is in a list.
- **ORDER BY:** sorts the result.
- **ASC / DESC:** ascending (the default) or descending sort order.
- **LIMIT:** caps how many rows come back.
- **Top N:** the first N rows after sorting, from `ORDER BY` + `LIMIT`.

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

## ORDER BY: sorting

```sql
SELECT name, age FROM customers
ORDER BY age;          -- youngest first (ascending is the default)
```

Add `DESC` for the reverse: `ORDER BY age DESC`.

- **ASC** = ascending = climbing up (1, 2, 3… or A, B, C…)
- **DESC** = descending = going down (3, 2, 1… or Z, Y, X…)

`ORDER BY` always needs a column: `ORDER BY name`, never just `ORDER BY DESC`.

## LIMIT: how many rows come back

```sql
SELECT name, age FROM customers
ORDER BY age DESC
LIMIT 2;               -- the two oldest: Ana, Priya
```

**`ORDER BY` + `LIMIT` = "top N" or "bottom N."** It's one of the most useful patterns in SQL.

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
SELECT → FROM → WHERE → ORDER BY → LIMIT
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

## Common mistakes

- `SORT BY` → it's `ORDER BY`
- `DEC`, `Assen` → it's `DESC`, `ASC`
- `LIMIT BY 2` → it's `LIMIT 2`
- `IN (Fremont, San Jose)` → text needs quotes: `IN ('Fremont', 'San Jose')`
- `ASC` when the question says "oldest first": read the direction carefully

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
```
</details>

---
Previous: [Lesson 1](01-first-queries.md) · Next: [Lesson 3: Aggregates and GROUP BY](03-aggregates-group-by.md)
