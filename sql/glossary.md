# SQL glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **ABS** | The absolute value: a number without its minus sign. `ABS(-250)` is 250. [8] |
| **ACID** | The guarantees of a transaction: Atomic (all or nothing), Consistent, Isolated, Durable. [16] |
| **Aggregate function** | A function that turns many rows into one value: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. [3] |
| **Alias** | A temporary name given with `AS`, for a column (`AVG(age) AS average_age`) or a table (`FROM customers c`). [3, 5] |
| **ALTER TABLE** | Changes an existing table's structure, e.g. adds a column. [11] |
| **AND / OR** | Combine conditions: `AND` needs both true, `OR` needs either. [2] |
| **ANY / ALL** | Compare a value with every value a subquery returns: `> ALL (...)` means more than all of them. Not in SQLite. [6] |
| **ASC / DESC** | Sort direction in `ORDER BY`: ascending (A→Z, 1→9, the default) or descending. [2] |
| **BETWEEN** | Inclusive range test: `rating BETWEEN 1 AND 5`. [9, 11] |
| **CASE** | If/then logic that produces a value: `CASE WHEN ... THEN ... ELSE ... END`. [7] |
| **CAST** | Converts a value to another type, like `CAST('42' AS INTEGER)`. [8] |
| **CEIL / CEILING** | Rounds up to the next whole number. `CEIL(4.1)` is 5. [8] |
| **CHECK** | A constraint requiring each value to pass a test. [11] |
| **Clause** | One part of a statement, like `WHERE ...` or `ORDER BY ...`. [1] |
| **COALESCE** | Returns the first value that isn't NULL: `COALESCE(x, 0)`. [8] |
| **Collation** | The rules a database uses to compare and sort text, including whether capital letters matter. [19] |
| **Column (field)** | One attribute that every row of a table has. [0] |
| **COMMIT** | Makes a transaction's changes permanent. [16] |
| **Conditional aggregation** | An aggregate over a `CASE`, used to count or pivot by condition, like `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`. [7, 18] |
| **Constraint** | A rule the database enforces on data: `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, foreign key. [11] |
| **Correlated subquery** | A subquery that refers to a column of the outer query's current row, so it runs once per row. [6] |
| **CREATE TABLE** | Defines a new table. [11] |
| **CROSS JOIN** | Pairs every row of one table with every row of another. [5] |
| **CTE (Common Table Expression)** | A named temporary result defined with `WITH`, used by the query that follows. [12] |
| **Database** | An organized collection of data. [0] |
| **Data type** | The kind of value a column holds: integer, decimal, text, date… [11] |
| **Data warehouse** | A database built for analysing large amounts of data, such as Snowflake, BigQuery or Databricks. [19] |
| **DBMS** | The software that manages a database (SQLite, MySQL, PostgreSQL, SQL Server, Oracle). [0] |
| **DEFAULT** | A constraint giving a column's value when none is supplied. [11] |
| **DELETE** | Removes rows: `DELETE FROM table WHERE ...`. [10] |
| **DENSE_RANK** | Window function that ranks with ties and no gaps (1, 2, 2, 3). [13] |
| **Derived table** | A subquery in `FROM`, used like a temporary table. It needs an alias. [6] |
| **Dialect** | A DBMS's own version of SQL. [0] |
| **DISTINCT** | Removes duplicate rows from a result. [8] |
| **DROP** | Deletes a whole table, view, or index. [11, 15] |
| **EXCEPT (MINUS)** | Rows in the first query's result but not the second's. [14] |
| **Execution order** | The order SQL actually runs clauses: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. [4] |
| **EXISTS / NOT EXISTS** | True when a subquery returns at least one row (or none). The NULL-safe way to write "has a match" or "has no match". [6] |
| **FILTER** | A clause that limits which rows an aggregate counts: `COUNT(*) FILTER (WHERE years >= 5)`. PostgreSQL, SQLite and Oracle 26ai. [18] |
| **FIRST_VALUE / LAST_VALUE** | Window functions that return the first or last value in the window. `LAST_VALUE` needs a full frame to work as expected. [13] |
| **FLOOR** | Rounds down to a whole number. `FLOOR(4.9)` is 4. [8] |
| **Foreign key** | A column that points to another table's primary key. [5, 11] |
| **FULL OUTER JOIN** | A join that keeps unmatched rows from both tables. [5] |
| **Gaps and islands** | Finding runs of consecutive values (islands) and the breaks between them (gaps), often with date minus `ROW_NUMBER`. [18] |
| **GROUP BY** | Splits rows into groups so aggregates are calculated per group. [3] |
| **GROUP_CONCAT / STRING_AGG / LISTAGG** | Aggregates that join a group's text values into one string, like `Alice, Carla, Hank`. [8] |
| **HAVING** | Filters groups after `GROUP BY`; may use aggregates. [4] |
| **Index** | A lookup structure that speeds up finding rows. [15] |
| **INNER JOIN (JOIN)** | Combines rows from two tables where they match; unmatched rows are dropped. [5] |
| **IN / NOT IN** | Tests whether a value is (or isn't) in a list or subquery result. [2, 6] |
| **INSERT** | Adds rows: `INSERT INTO table (cols) VALUES (...)`. [10] |
| **INSERT ... SELECT** | Adds the rows a query returns to a table, instead of typed-in values. [10] |
| **INSTR** | The position of one piece of text inside another (0 if it isn't there). [8] |
| **Integer division** | Dividing two whole numbers and dropping the decimals: `7 / 2` is 3 in SQLite, PostgreSQL and MSSQL. [8] |
| **INTERSECT** | Rows present in both queries' results. [14] |
| **IS NULL / IS NOT NULL** | The only correct way to test for NULL. [5] |
| **LAG / LEAD** | Window functions returning a value from the previous / next row. [13] |
| **LEFT JOIN** | A join that keeps every row of the first (left) table. [5] |
| **LIKE** | Pattern matching on text with `%` (any characters) and `_` (one character). [8] |
| **LIMIT / TOP / FETCH FIRST** | Caps the number of rows returned (SQLite and MySQL / MSSQL / Oracle). [2] |
| **LTS (long-term support)** | A database release that gets fixes for several years, such as MySQL 8.4 and 9.7. [19] |
| **Median** | The middle value when the values are sorted, or the average of the middle two. [18] |
| **Modulo (% / MOD)** | The remainder after division: `7 % 3` is 1. `x % 2 = 0` means x is even. [8] |
| **Moving average** | The average of the current row and a fixed number of rows around it, using a window frame. [13] |
| **Non-equi join** | A join whose `ON` uses something other than `=`, such as `BETWEEN`. [5] |
| **NOT NULL** | A constraint requiring a value. [11] |
| **NTILE** | A window function that splits rows into n equal-sized buckets, numbered 1 to n. [13] |
| **NULL** | A marker for "no value / unknown". Not zero, not empty text. [5] |
| **NULLIF** | Returns NULL when two values are equal, otherwise the first. `x / NULLIF(y, 0)` avoids dividing by zero. [8] |
| **NULLS FIRST / NULLS LAST** | Says where NULLs go in an `ORDER BY`. [2] |
| **OFFSET** | Skips a number of rows before `LIMIT` starts counting. [2] |
| **ORDER BY** | Sorts the result. [2] |
| **OVER** | Turns a function into a window function and defines its window. [13] |
| **PARTITION BY** | Splits a window into groups, like `GROUP BY` without collapsing rows. [13] |
| **Pivot** | Turning the values of one column into separate columns. [18] |
| **Primary key** | A column that uniquely identifies each row. [0, 11] |
| **QUALIFY** | A clause that filters on window functions directly, in Snowflake, BigQuery, Databricks, DuckDB and Oracle 26ai. [13] |
| **Query** | A request for data, written in SQL. [0] |
| **Query plan** | The database's plan for running a query; see it with `EXPLAIN QUERY PLAN`. [15] |
| **RANK** | Window function that ranks with ties and gaps (1, 2, 2, 4). [13] |
| **Recursive CTE** | A CTE that refers to itself, adding rows step by step until a condition stops it. [12] |
| **Relational database** | A database of linked tables. [0] |
| **Relational division** | Finding the rows related to all items of another set, like customers who bought every product. [18] |
| **REPLACE** | Swaps every occurrence of some text for other text. [8] |
| **Result set** | The rows a query returns. [0] |
| **RETURNING** | Makes `INSERT`, `UPDATE` or `DELETE` return the rows it changed. MSSQL uses `OUTPUT`. [10] |
| **RIGHT JOIN** | A join that keeps every row of the second (right) table. [5] |
| **ROLLBACK** | Undoes every change in the current transaction. [16] |
| **ROUND** | Rounds a number to a given number of decimal places. [8] |
| **ROW_NUMBER** | Window function numbering rows 1, 2, 3… with no ties. [13] |
| **Row (record)** | One item in a table. [0] |
| **Running total** | A cumulative sum, row by row: `SUM(x) OVER (ORDER BY ...)`. [13] |
| **Schema** | The structure of a database: tables, columns, links. [0] |
| **SELECT** | The statement that reads data. [1] |
| **Self join** | A table joined to itself, using two different aliases. [5] |
| **SET** | The part of `UPDATE` that says what to change. [10] |
| **SQL** | Structured Query Language, the language of relational databases. [0] |
| **Statement** | One complete SQL command, ending with `;`. [1] |
| **STRICT table** | A SQLite table that rejects values of the wrong type, as other databases do. [11] |
| **Subquery** | A query in parentheses inside another query. [6] |
| **SUBSTR / SUBSTRING** | Takes part of a text value by position, starting at 1. [8] |
| **Table** | Data about one kind of thing, in rows and columns. [0] |
| **Transaction** | A group of changes that succeed or fail together. [16] |
| **TRIM** | Removes spaces (or other characters) from the ends of text. [8] |
| **Truncate (a number)** | Cut off decimals without rounding: `TRUNCATE(x, d)` in MySQL, `TRUNC(x, d)` in Oracle and PostgreSQL. [8] |
| **TRUNCATE TABLE** | Deletes every row of a table in one fast step and keeps the empty table. [10] |
| **T-SQL** | Transact-SQL, Microsoft SQL Server's dialect. [16] |
| **UNION / UNION ALL** | Stack two results; `UNION` removes duplicates, `UNION ALL` keeps them. [14] |
| **UNIQUE** | A constraint forbidding duplicate values in a column. [11] |
| **UPDATE** | Changes existing rows: `UPDATE table SET ... WHERE ...`. [10] |
| **Upsert** | Insert a row, or update it if it already exists: `ON CONFLICT`, `ON DUPLICATE KEY UPDATE` or `MERGE`. [10] |
| **Vector embedding** | A list of numbers representing the meaning of text or images, stored in databases for AI similarity search. [19] |
| **View** | A saved query you can use like a table. [15] |
| **WHERE** | Filters individual rows. [1] |
| **Wildcard** | A pattern character in `LIKE`: `%` or `_`. [8] |
| **Window frame** | The rows around the current row that a window function uses, set with `ROWS BETWEEN ...`. [13] |
| **Window function** | A function over related rows that keeps every row in the result. [13] |
| **WITH** | Starts one or more CTEs. [12] |
