@@ numpy-arrays
topics: `np.array`, vectorised maths, speed, `shape`, `ndim`, `dtype`, `arange`, `linspace`, `zeros`, `ones`
terms:
- **NumPy array (ndarray):** a grid of numbers that all share one type, built for fast maths.
- **Vectorisation:** doing an operation on every item of an array at once, without a loop.
- **Shape:** the size of an array along each dimension, like `(3, 4)` for 3 rows and 4 columns.
- **ndim:** the number of dimensions: 1 for a row of numbers, 2 for a table.
- **dtype:** the data type shared by every item in an array, such as `int64` or `float64`.
- **np.arange:** makes evenly spaced numbers, like `range()`.
- **np.linspace:** makes a set number of evenly spaced values between two ends.
mistakes:
- Expecting a list to do maths: `[1, 2] * 2` repeats the list. Convert it with `np.array()` first.
- Passing a shape without brackets: `np.zeros(3, 4)` is an error; write `np.zeros((3, 4))`.
- Forgetting that `np.arange(0, 10)` stops at 9, just like `range`.

@@ array-indexing
topics: indexing and slicing, `arr[row, col]`, boolean masks, `&`, `|`, `~`, fancy indexing, views and copies
terms:
- **Index:** the position of an item, starting at 0.
- **Slice:** a range of positions, like `a[2:5]`.
- **Boolean mask:** an array of `True`/`False` values used to pick items.
- **Fancy indexing:** selecting items with a list of positions, like `a[[0, 3]]`.
- **np.nan:** "not a number", NumPy's marker for a missing value.
- **View:** a slice that shares data with the original array, so changes show up in both.
- **copy():** makes an independent array that doesn't share data.
mistakes:
- Using `and`/`or` with arrays. Use `&`/`|` and wrap each condition in brackets: `(a > 5) & (a < 15)`.
- Writing `scores[1][2]` everywhere. It works, but `scores[1, 2]` is the NumPy way and is needed for column slices like `scores[:, 2]`.
- Changing a slice and being surprised the original changed. Call `.copy()` when you need independence.

@@ vectorised-math
topics: array-with-array maths, broadcasting, ufuncs, `np.where`, `np.nan`, `np.isnan`, scaling
terms:
- **Element-wise:** done item by item, matching positions in two arrays.
- **Broadcasting:** NumPy stretching a smaller array (or a single number) to match a bigger one.
- **ufunc (universal function):** a fast NumPy function that works on every item, like `np.sqrt`.
- **np.where:** chooses between two values item by item based on a condition.
- **np.nanmean:** an average that skips missing (`nan`) values.
- **Scaling (normalising):** rescaling numbers to a common range such as 0 to 1.
mistakes:
- Adding arrays of different lengths. Shapes must match or be broadcastable; check `.shape` first.
- Testing for missing values with `== np.nan`, which is always `False`. Use `np.isnan()`.
- Using Python's `math.sqrt` on an array. It only takes single numbers; use `np.sqrt`.

@@ array-statistics
topics: `sum`, `mean`, `median`, `std`, `percentile`, `argmax`, `axis`, `cumsum`, `reshape`, `np.loadtxt`
terms:
- **Mean:** the average: the total divided by the number of values.
- **Median:** the middle value when the values are sorted.
- **Standard deviation (std):** a measure of how spread out values are around the mean.
- **Percentile:** the value below which a given percentage of the data falls.
- **Quartiles:** the 25th, 50th and 75th percentiles.
- **axis:** which direction to summarise: `axis=0` down the columns, `axis=1` across the rows.
- **cumsum:** a running total.
- **reshape:** rearranging an array's values into a new shape with the same total size.
mistakes:
- Mixing up the axes. Remember the axis you name disappears: `(rows, cols)` with `axis=0` leaves one value per column.
- Reporting only the mean for skewed data like salaries or response times. Show the median (or percentiles) too.
- Confusing `max()` (the value) with `argmax()` (its position).

@@ random-and-simulation
topics: `default_rng`, seeds, `integers`, `random`, `normal`, `choice`, `permutation`, `binomial`, simulation
terms:
- **Random generator:** an object, made with `np.random.default_rng()`, that produces random numbers.
- **Seed:** a starting number that makes a generator produce the same sequence every run.
- **Distribution:** how likely each possible value is.
- **Uniform distribution:** every value in a range is equally likely.
- **Normal distribution:** the bell curve: values cluster around the mean, with fewer far away.
- **Simulation:** answering a question by acting it out many times with random numbers and counting.
- **Train/test split:** dividing data so a model learns from one part and is tested on the other.
mistakes:
- Forgetting the seed, so your results change every run and nobody can reproduce them.
- Thinking `rng.integers(1, 6)` can return 6. The upper number is excluded; use `integers(1, 7)` for a dice.
- Running too few simulations. With 10 tries the answer is noisy; use thousands.
