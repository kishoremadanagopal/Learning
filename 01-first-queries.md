# Lesson 1: Tables and your first query

**You'll learn:** `SELECT`, `FROM`, `WHERE`, and comparison operators.

## Key terms

- **Query:** a request for data, written in SQL.
- **Statement:** one complete SQL command, ending with `;`.
- **Clause:** one part of a statement, like `SELECT ...` or `WHERE ...`.
- **SELECT:** chooses which columns to show.
- **FROM:** names the table to read.
- **WHERE:** keeps only the rows that match a condition.
- **Operator:** a symbol that compares values, like `=` or `>`.

## Syntax

```sql
SELECT column1, column2      -- or * for every column
FROM table_name
WHERE condition;             -- optional
```

## What SQL is

SQL (Structured Query Language) is how you ask questions of a database. A database stores data in **tables**, which look like spreadsheets:

- each **row** is one record (one customer, one order)
- each **column** is one attribute (name, city, age)

This lesson uses the `customers` table from [the practice tables](00-the-tables.md).

## Getting everything back

```sql
SELECT * FROM customers;
```

Read it as "select all columns from customers." The `*` means every column, and the semicolon ends the statement.

## Picking specific columns

```sql
SELECT name, city FROM customers;
```

This returns just the name and city of all 5 people. Column names must be spelled exactly as they are in the table: `name`, not `names`.

## Filtering rows with WHERE

```sql
SELECT name, age
FROM customers
WHERE city = 'Fremont';
```

| name  | age |
|-------|-----|
| Maya  | 34  |
| Priya | 41  |

- Text goes in **single quotes**: `'Fremont'`. Numbers don't: `age = 34`.
- Keywords like `SELECT` aren't case-sensitive. Writing them in capitals is a convention that makes queries easier to read.
- Line breaks don't matter. Splitting a query over several lines is just for readability.

## Comparison operators

| Operator | Meaning |
|---|---|
| `=` | equal to |
| `<>` or `!=` | not equal to |
| `>` `<` | greater than, less than |
| `>=` `<=` | greater/less than or equal to |

`WHERE age >= 30` returns Maya, Priya, and Ana.

## Common mistakes

- **Wrong column or table name.** `SELECT names FROM customer` fails twice: the column is `name` and the table is `customers`.
- **Text inside quotes is case-sensitive in some databases.** In SQLite and PostgreSQL, `city = 'fremont'` returns **no rows**, with no error, because the data says `Fremont`. MySQL and MSSQL ignore case by default. The safe habit is to match the data exactly.

## Exercises

1. Show every column for everyone.
2. Show only the names of people younger than 30.
3. Show the name and age of everyone who is **not** in Oakland.

**In the sandbox:** exercise 1.

<details>
<summary>Answers</summary>

```sql
-- 1
SELECT * FROM customers;

-- 2  → Leo, Sam
SELECT name FROM customers WHERE age < 30;

-- 3  → Maya, Priya, Sam
SELECT name, age FROM customers WHERE city != 'Oakland';
```
</details>

---
Next: [Lesson 2: Filtering, sorting and limiting](02-filtering-sorting.md)
