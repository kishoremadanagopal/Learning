# Lesson 1: Smoke test

**You'll learn:** test.

▶ **Practise this lesson in the [sandbox](https://kishoremadanagopal.github.io/learning/python-data/#smoke)**: run every example and check your exercise answers.

## Key terms

- **DataFrame:** a table.

```python
import pandas as pd
sales = pd.read_csv("sales.csv")
print(sales.head(3))
print(sales.dtypes)
```

*This example raises an error on purpose.*

```python
import pandas as pd
pd.read_csv("sales.csv")["Revenue"]
```

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1,2,3])
ax.set_title("x")
plt.show()
```

## Common mistakes

- none.

## Exercises

### 1. Total units

Make `total` the sum of the units column.

Starter code:

```python
import pandas as pd
sales = pd.read_csv("sales.csv")
total = 0
```

### 2. Chart

Draw a chart titled "Units".

Starter code:

```python
import matplotlib.pyplot as plt
```

**In the sandbox:** exercises 1–2. Press **Check** to test your answer.

<details>
<summary>Answers</summary>

**1. Total units**

```python
import pandas as pd
sales = pd.read_csv("sales.csv")
total = sales["units"].sum()
```

**2. Chart**

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.bar(["a"], [1])
ax.set_title("Units")
```

</details>

## Quick quiz

1. q?
   - A) a
   - B) b
   - C) c

<details>
<summary>Quiz answers</summary>

1. **B) b**: because

</details>

---
Back to the [course home](../README.md) · Back to the [course home](../README.md)
