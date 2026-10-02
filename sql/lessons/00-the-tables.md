# The practice tables

Every lesson uses these three tables. They're already loaded in the [practice sandbox](https://kishoremadanagopal.github.io/Learning/sql/), and you can press **Reset data** there at any time to get back to exactly this data.

## `customers`

| id | name  | city     | age |
|----|-------|----------|-----|
| 1  | Maya  | Fremont  | 34  |
| 2  | Leo   | Oakland  | 27  |
| 3  | Priya | Fremont  | 41  |
| 4  | Sam   | San Jose | 19  |
| 5  | Ana   | Oakland  | 52  |

## `employees`

| id | name  | department  | salary | years |
|----|-------|-------------|--------|-------|
| 1  | Alice | Sales       | 60000  | 3     |
| 2  | Bob   | Engineering | 95000  | 5     |
| 3  | Carla | Sales       | 55000  | 1     |
| 4  | Dev   | Engineering | 105000 | 8     |
| 5  | Emma  | Marketing   | 70000  | 4     |
| 6  | Frank | Engineering | 88000  | 2     |
| 7  | Grace | Marketing   | 62000  | 6     |
| 8  | Hank  | Sales       | 72000  | 7     |

## `orders`

| order_id | customer_id | product  | amount | order_date |
|----------|-------------|----------|--------|------------|
| 101      | 1           | Laptop   | 1200   | 2025-11-20 |
| 102      | 1           | Mouse    | 25     | 2025-12-02 |
| 103      | 2           | Desk     | 300    | 2026-01-10 |
| 104      | 3           | Chair    | 150    | 2026-01-25 |
| 105      | 5           | Monitor  | 400    | 2026-02-14 |
| 106      | 5           | Keyboard | 80     | 2026-02-14 |
| 107      | 3           | Lamp     | 45     | 2026-03-03 |

`orders.customer_id` points to `customers.id`. Order 101 has `customer_id` 1, so Maya placed it. Sam (id 4) has no orders, which matters in Lesson 5.

## Watch the table names

All three table names are **plural**: `customers`, `employees`, `orders`. Writing `customer` or `employee` is the single most common typo in this course, and SQL answers it with `no such table`.
