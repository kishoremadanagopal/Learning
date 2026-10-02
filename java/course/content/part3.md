@@@ part
id: 3
title: Arrays and Methods
level: Beginner
blurb: Store many values in arrays and grids, and organise your code into reusable methods, including recursive ones.

@@@ lesson
id: arrays
title: Arrays
minutes: 15
summary: Create arrays, read and change elements, loop over them, and use the Arrays helper class.
---
An **array** holds a fixed number of values of the same type. Each value is an **element**, reached by its index starting at 0.

```java
public class Main {
    public static void main(String[] args) {
        int[] scores = {90, 72, 85};
        String[] names = {"Ana", "Ben", "Cy"};

        System.out.println(scores[0]);
        System.out.println(names[2]);
        System.out.println("There are " + scores.length + " scores");

        scores[1] = 75;             // change an element
        System.out.println(scores[1]);
    }
}
```

Note `scores.length` has no parentheses: for arrays it's a field, while for strings it's a method, `s.length()`.

### Creating an empty array

`new int[5]` makes an array of 5 elements filled with default values: `0` for numbers, `false` for booleans, `'\u0000'` for chars and `null` for objects like strings.

```java
public class Main {
    public static void main(String[] args) {
        int[] squares = new int[5];
        for (int i = 0; i < squares.length; i++) {
            squares[i] = i * i;
        }
        for (int s : squares) {
            System.out.print(s + " ");
        }
        System.out.println();

        String[] empty = new String[2];
        System.out.println(empty[0]);
    }
}
```

An array's size is fixed once created. When you need a list that grows and shrinks, use `ArrayList` (Part 5).

### Out of bounds

Using an index outside `0` to `length - 1` throws an exception at runtime:

```java error
public class Main {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        System.out.println(a[3]);
    }
}
```

### Common array algorithms

```java
public class Main {
    public static void main(String[] args) {
        int[] nums = {4, 9, 2, 7, 5};

        int sum = 0;
        int max = nums[0];
        for (int n : nums) {
            sum += n;
            if (n > max) {
                max = n;
            }
        }
        double average = (double) sum / nums.length;
        System.out.println("sum=" + sum + " max=" + max + " avg=" + average);

        int target = 7;
        int found = -1;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] == target) {
                found = i;
                break;
            }
        }
        System.out.println("7 is at index " + found);
    }
}
```

### The Arrays helper class

`java.util.Arrays` has ready-made tools:

```java
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        int[] nums = {4, 9, 2, 7, 5};
        System.out.println(nums);                    // not helpful: a memory reference
        System.out.println(Arrays.toString(nums));   // readable

        int[] copy = Arrays.copyOf(nums, nums.length);
        Arrays.sort(copy);
        System.out.println(Arrays.toString(copy));
        System.out.println(Arrays.toString(nums));   // original unchanged

        int[] filled = new int[4];
        Arrays.fill(filled, 7);
        System.out.println(Arrays.toString(filled));
        System.out.println(Arrays.equals(new int[]{1, 2}, new int[]{1, 2}));
    }
}
```

### Arrays are references

An array variable holds a **reference** to the array. Assigning it to another variable doesn't copy the array; both names point at the same one:

```java
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = a;
        b[0] = 99;
        System.out.println(Arrays.toString(a));   // a changed too!

        int[] c = a.clone();
        c[0] = 1;
        System.out.println(Arrays.toString(a) + " " + Arrays.toString(c));
    }
}
```

:::exercise Statistics
Write `static double average(int[] nums)` returning the mean (return `0` for an empty array), and `static int countAbove(int[] nums, int limit)` returning how many values are strictly greater than `limit`.
```java starter
public class Main {
    static double average(int[] nums) {
        return 0;
    }

    static int countAbove(int[] nums, int limit) {
        return 0;
    }

    public static void main(String[] args) {
        int[] data = {4, 9, 2, 7, 5};
        System.out.println(average(data) + " " + countAbove(data, 4));
    }
}
```
```java check
near(5.4, call("average", new int[]{4, 9, 2, 7, 5}), "average({4, 9, 2, 7, 5})");
near(2.5, call("average", new int[]{2, 3}), "average({2, 3})");
near(0, call("average", new int[]{}), "average({})");
eq(3, call("countAbove", new int[]{4, 9, 2, 7, 5}, 4), "countAbove({4, 9, 2, 7, 5}, 4)");
eq(0, call("countAbove", new int[]{1, 2}, 5), "countAbove({1, 2}, 5)");
```
```java solution
public class Main {
    static double average(int[] nums) {
        if (nums.length == 0) {
            return 0;
        }
        int sum = 0;
        for (int n : nums) {
            sum += n;
        }
        return (double) sum / nums.length;
    }

    static int countAbove(int[] nums, int limit) {
        int count = 0;
        for (int n : nums) {
            if (n > limit) {
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        int[] data = {4, 9, 2, 7, 5};
        System.out.println(average(data) + " " + countAbove(data, 4));
    }
}
```
hint: Add up the numbers in a loop, then divide by nums.length after casting the sum to double. Remember the empty-array case.
:::

:::exercise Reverse in place
Write `static void reverse(int[] a)` that reverses the array **in place** (change `a` itself, don't create a new array). Swap the first and last elements, then the second and second-to-last, and so on.
```java starter
import java.util.Arrays;

public class Main {
    static void reverse(int[] a) {

    }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4, 5};
        reverse(nums);
        System.out.println(Arrays.toString(nums));
    }
}
```
```java check
int[] a = {1, 2, 3, 4, 5};
call("reverse", (Object) a);
eq(new int[]{5, 4, 3, 2, 1}, a, "After reverse, {1, 2, 3, 4, 5}");
int[] b = {7, 8};
call("reverse", (Object) b);
eq(new int[]{8, 7}, b, "After reverse, {7, 8}");
int[] c = {};
call("reverse", (Object) c);
```
```java solution
import java.util.Arrays;

public class Main {
    static void reverse(int[] a) {
        for (int i = 0, j = a.length - 1; i < j; i++, j--) {
            int temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }
    }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3, 4, 5};
        reverse(nums);
        System.out.println(Arrays.toString(nums));
    }
}
```
hint: Use two indexes, i from the start and j from the end. Swap a[i] and a[j] with a temporary variable, then move them towards each other until they meet.
:::

:::quiz
? What is the last valid index of `int[] a = new int[5];`?
- 5
+ 4
- 6
= Indexes run from 0 to length - 1.

? What does `new boolean[3]` contain?
+ false, false, false
- null, null, null
- true, true, true
= New arrays are filled with default values: false for booleans.

? What does `System.out.println(Arrays.toString(new int[]{3, 1}))` print?
+ [3, 1]
- 3, 1
- [I@1b6d3586
= `Arrays.toString` formats the elements. Printing the array directly shows a reference.
:::

@@@ lesson
id: two-d-arrays
title: 2D arrays
minutes: 10
summary: Store grids and tables as arrays of arrays, and loop over rows and columns.
---
A **2D array** is an array of arrays: perfect for grids, game boards and tables.

```java
public class Main {
    public static void main(String[] args) {
        int[][] grid = {
            {1, 2, 3},
            {4, 5, 6}
        };
        System.out.println(grid[1][2]);          // row 1, column 2
        System.out.println(grid.length + " rows, " + grid[0].length + " columns");
    }
}
```

`grid[row][col]`: the first index picks the row, the second picks the column.

### Looping over a grid

```java
public class Main {
    public static void main(String[] args) {
        int[][] grid = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        int total = 0;
        for (int r = 0; r < grid.length; r++) {
            for (int c = 0; c < grid[r].length; c++) {
                System.out.print(grid[r][c] + " ");
                total += grid[r][c];
            }
            System.out.println();
        }
        System.out.println("total = " + total);

        for (int[] row : grid) {             // for-each works too
            System.out.println(java.util.Arrays.toString(row));
        }
    }
}
```

### Creating an empty grid

```java
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        char[][] board = new char[3][3];
        for (char[] row : board) {
            Arrays.fill(row, '.');
        }
        board[1][1] = 'X';
        board[0][2] = 'O';
        for (char[] row : board) {
            System.out.println(new String(row));
        }
        System.out.println(Arrays.deepToString(new int[2][3]));
    }
}
```

`Arrays.deepToString` prints nested arrays. Rows don't even have to be the same length; such arrays are called **jagged**.

:::exercise Row sums
Write `static int[] rowSums(int[][] grid)` returning an array with the sum of each row. For `{{1, 2}, {3, 4}, {5, 6}}` it returns `{3, 7, 11}`.
```java starter
import java.util.Arrays;

public class Main {
    static int[] rowSums(int[][] grid) {
        return new int[0];
    }

    public static void main(String[] args) {
        int[][] g = {{1, 2}, {3, 4}, {5, 6}};
        System.out.println(Arrays.toString(rowSums(g)));
    }
}
```
```java check
eq(new int[]{3, 7, 11}, call("rowSums", (Object) new int[][]{{1, 2}, {3, 4}, {5, 6}}), "rowSums({{1, 2}, {3, 4}, {5, 6}})");
eq(new int[]{6, 0, 5}, call("rowSums", (Object) new int[][]{{1, 2, 3}, {}, {5}}), "rowSums of a jagged grid");
```
```java solution
import java.util.Arrays;

public class Main {
    static int[] rowSums(int[][] grid) {
        int[] sums = new int[grid.length];
        for (int r = 0; r < grid.length; r++) {
            for (int value : grid[r]) {
                sums[r] += value;
            }
        }
        return sums;
    }

    public static void main(String[] args) {
        int[][] g = {{1, 2}, {3, 4}, {5, 6}};
        System.out.println(Arrays.toString(rowSums(g)));
    }
}
```
hint: Create int[] sums = new int[grid.length]. For each row r, add every value in grid[r] to sums[r].
:::

:::quiz
? In `int[][] g = new int[3][5];`, what is `g.length`?
+ 3
- 5
- 15
= `g.length` is the number of rows; `g[0].length` is the number of columns.

? How do you print a 2D array readably?
- `Arrays.toString(g)`
+ `Arrays.deepToString(g)`
- `System.out.println(g)`
= `deepToString` goes inside the nested arrays.
:::

@@@ lesson
id: methods
title: Methods
minutes: 15
summary: Define methods with parameters and return values, understand void and static, and print vs return.
---
A **method** is a named, reusable block of code. You've been calling methods all along: `println`, `length`, `Math.max`. Now you'll write your own.

```java
public class Main {
    static String greet(String name) {
        return "Hello, " + name + "!";
    }

    public static void main(String[] args) {
        String message = greet("Ada");
        System.out.println(message);
        System.out.println(greet("Alan"));
    }
}
```

The **method header** `static String greet(String name)` says:

- `static`: the method belongs to the class, so `main` can call it directly. (Part 4 explains non-static methods.)
- `String`: the **return type**, the type of value the method gives back.
- `greet`: the name, in camelCase.
- `(String name)`: the **parameters**, each with a type.

The values you pass when calling, like `"Ada"`, are called **arguments**.

### return and void

`return` hands a value back and ends the method immediately. A method that doesn't return anything has the return type `void`:

```java
public class Main {
    static void printBanner(String title, int width) {
        String line = "=".repeat(width);
        System.out.println(line);
        System.out.println(title);
        System.out.println(line);
    }

    static int area(int width, int height) {
        return width * height;
    }

    public static void main(String[] args) {
        printBanner("Report", 10);
        int a = area(4, 5);
        System.out.println("Area: " + a + ", double: " + area(4, 5) * 2);
    }
}
```

### print vs return

This trips up many beginners. `System.out.println` **shows** a value. `return` **hands it back** so the program can keep using it. A method that only prints can't be used in a calculation. Prefer returning values and let the caller decide what to print.

The compiler checks that a non-void method always returns a value:

```java error
public class Main {
    static String sign(int n) {
        if (n > 0) {
            return "positive";
        } else if (n < 0) {
            return "negative";
        }
    }

    public static void main(String[] args) {
        System.out.println(sign(5));
    }
}
```

That's the error "missing return statement": what if `n` is 0? Adding a final `return "zero";` fixes it.

### Early returns keep code flat

```java
public class Main {
    static String describeAge(int age) {
        if (age < 0) {
            return "invalid";
        }
        if (age < 13) {
            return "child";
        }
        if (age < 20) {
            return "teenager";
        }
        return "adult";
    }

    public static void main(String[] args) {
        for (int a : new int[]{-1, 8, 15, 42}) {
            System.out.println(a + " " + describeAge(a));
        }
    }
}
```

### Why methods?

- **Reuse**: write once, call many times.
- **Readability**: `calculateTax(price)` explains itself.
- **Testing**: small methods are easy to check, which is exactly how this course's checker works.

:::exercise Max of three
Write `static int maxOfThree(int a, int b, int c)` that returns the largest of the three, **without** using `Math.max`.
```java starter
public class Main {
    static int maxOfThree(int a, int b, int c) {
        return a;
    }

    public static void main(String[] args) {
        System.out.println(maxOfThree(3, 9, 4));
    }
}
```
```java check
int[][] cases = {{3, 9, 4, 9}, {9, 3, 4, 9}, {3, 4, 9, 9}, {-1, -5, -3, -1}, {2, 2, 2, 2}};
for (int[] c : cases) eq(c[3], call("maxOfThree", c[0], c[1], c[2]), "maxOfThree(" + c[0] + ", " + c[1] + ", " + c[2] + ")");
sourceLacks("Math.max", "Solve it without Math.max.");
```
```java solution
public class Main {
    static int maxOfThree(int a, int b, int c) {
        int max = a;
        if (b > max) {
            max = b;
        }
        if (c > max) {
            max = c;
        }
        return max;
    }

    public static void main(String[] args) {
        System.out.println(maxOfThree(3, 9, 4));
    }
}
```
hint: Start with int max = a; then replace it with b or c if they're bigger.
:::

:::exercise BMI
Write `static double bmi(double weightKg, double heightM)` returning `weight / height²`, and `static String bmiCategory(double bmi)` returning `"underweight"` (below 18.5), `"normal"` (below 25), `"overweight"` (below 30) or `"obese"`.
```java starter
public class Main {
    static double bmi(double weightKg, double heightM) {
        return 0;
    }

    static String bmiCategory(double bmi) {
        return "";
    }

    public static void main(String[] args) {
        double b = bmi(70, 1.75);
        System.out.printf("%.1f %s%n", b, bmiCategory(b));
    }
}
```
```java check
near(22.857142857, call("bmi", 70.0, 1.75), "bmi(70, 1.75)");
String[][] cases = {{"17.0", "underweight"}, {"18.5", "normal"}, {"24.9", "normal"}, {"25.0", "overweight"}, {"29.9", "overweight"}, {"30.0", "obese"}};
for (String[] c : cases) eq(c[1], call("bmiCategory", Double.parseDouble(c[0])), "bmiCategory(" + c[0] + ")");
```
```java solution
public class Main {
    static double bmi(double weightKg, double heightM) {
        return weightKg / (heightM * heightM);
    }

    static String bmiCategory(double bmi) {
        if (bmi < 18.5) {
            return "underweight";
        }
        if (bmi < 25) {
            return "normal";
        }
        if (bmi < 30) {
            return "overweight";
        }
        return "obese";
    }

    public static void main(String[] args) {
        double b = bmi(70, 1.75);
        System.out.printf("%.1f %s%n", b, bmiCategory(b));
    }
}
```
hint: bmi: return weightKg / (heightM * heightM). bmiCategory: a chain of if (bmi < ...) return ...; from low to high.
:::

:::quiz
? What does a `void` method return?
+ Nothing
- 0
- null
= `void` means the method doesn't hand back a value.

? Why does "missing return statement" appear?
+ Some path through a non-void method doesn't return a value
- The method has too many returns
- `return` must be the first line
= Every possible path must end in a `return` (or throw an exception).

? In `int area(int w, int h)`, what are `w` and `h`?
+ Parameters
- Arguments
- Return types
= Parameters are in the definition; arguments are the values in a call.
:::

@@@ lesson
id: overloading-and-scope
title: Overloading, scope and pass-by-value
minutes: 12
summary: Give methods the same name with different parameters, understand where variables live, and how arguments are passed.
---
### Overloading

Several methods can share a name if their **parameter lists differ**. Java picks the right one from the arguments you pass. `System.out.println` is overloaded for every type, which is why it prints ints, doubles and strings alike.

```java
public class Main {
    static int add(int a, int b) {
        return a + b;
    }

    static double add(double a, double b) {
        return a + b;
    }

    static int add(int a, int b, int c) {
        return a + b + c;
    }

    public static void main(String[] args) {
        System.out.println(add(2, 3));
        System.out.println(add(2.5, 3.1));
        System.out.println(add(1, 2, 3));
    }
}
```

The return type alone isn't enough to overload: two methods that differ only in return type won't compile.

### Scope: where variables live

A variable exists only inside the **block** `{ }` where it's declared. Variables declared inside a method are **local** to that method.

```java
public class Main {
    static int counter = 0;               // a static field: visible to every method in the class

    static void increment() {
        counter++;
        int temp = 5;                     // local to increment()
    }

    public static void main(String[] args) {
        increment();
        increment();
        System.out.println(counter);

        for (int i = 0; i < 2; i++) {
            int squared = i * i;          // exists only inside this loop body
        }
        // System.out.println(squared);  // would not compile: squared is out of scope
    }
}
```

Keep variables in the smallest scope that works. Fewer variables in view means fewer surprises.

### Pass-by-value

Java always passes **copies** of arguments. For primitives, the method gets its own copy, so changing it doesn't affect the caller:

```java
public class Main {
    static void tryToChange(int x) {
        x = 100;
    }

    static void changeArray(int[] arr) {
        arr[0] = 100;             // changes the array the caller also sees
    }

    static void replaceArray(int[] arr) {
        arr = new int[]{7, 7};    // only changes the local copy of the reference
    }

    public static void main(String[] args) {
        int n = 5;
        tryToChange(n);
        System.out.println(n);

        int[] data = {1, 2};
        changeArray(data);
        System.out.println(data[0]);
        replaceArray(data);
        System.out.println(data[0]);
    }
}
```

For arrays and objects, the copied value is a **reference**. The method can change the object it points to, but pointing its own copy at a new object doesn't affect the caller.

### Variable arguments

`int... nums` lets a method take any number of ints; inside, `nums` is an array:

```java
public class Main {
    static int sum(int... nums) {
        int total = 0;
        for (int n : nums) {
            total += n;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(sum());
        System.out.println(sum(4));
        System.out.println(sum(1, 2, 3, 4));
    }
}
```

:::exercise Describe overloads
Write two overloaded methods named `describe`: `describe(int n)` returns `"int: "` followed by the number, and `describe(String s)` returns `"text: "` followed by the text in uppercase.
```java starter
public class Main {

    public static void main(String[] args) {
        // System.out.println(describe(42));
        // System.out.println(describe("hi"));
    }
}
```
```java check
eq("int: 42", call("describe", 42), "describe(42)");
eq("text: HI", call("describe", "hi"), "describe(\"hi\")");
```
```java solution
public class Main {
    static String describe(int n) {
        return "int: " + n;
    }

    static String describe(String s) {
        return "text: " + s.toUpperCase();
    }

    public static void main(String[] args) {
        System.out.println(describe(42));
        System.out.println(describe("hi"));
    }
}
```
hint: Write static String describe(int n) { ... } and static String describe(String s) { ... } next to main.
:::

:::exercise Average of any count
Write `static double average(double... values)` that returns the average of any number of values, or `0` when called with none.
```java starter
public class Main {
    static double average(double... values) {
        return 0;
    }

    public static void main(String[] args) {
        System.out.println(average(1, 2, 3, 4));
    }
}
```
```java check
near(2.5, call("average", (Object) new double[]{1, 2, 3, 4}), "average(1, 2, 3, 4)");
near(7, call("average", (Object) new double[]{7}), "average(7)");
near(0, call("average", (Object) new double[]{}), "average()");
sourceHas("double...", "Use a varargs parameter: double... values");
```
```java solution
public class Main {
    static double average(double... values) {
        if (values.length == 0) {
            return 0;
        }
        double total = 0;
        for (double v : values) {
            total += v;
        }
        return total / values.length;
    }

    public static void main(String[] args) {
        System.out.println(average(1, 2, 3, 4));
    }
}
```
hint: Inside the method, values is an array. Check values.length == 0 first, then add them up and divide.
:::

:::quiz
? Can two methods differ only in their return type?
- Yes
+ No, the parameter lists must differ
= Java chooses an overload by its arguments, so the parameters must differ.

? After `void f(int x) { x = 9; }` and `int n = 1; f(n);`, what is `n`?
+ 1
- 9
= Java passes a copy of the value; the method changes only its copy.

? A method receives an array and sets `arr[0] = 5`. Does the caller see it?
+ Yes, both refer to the same array
- No, arrays are copied
= The reference is copied, but it points to the same array object.
:::

@@@ lesson
id: recursion
title: Recursion
minutes: 12
summary: Methods that call themselves, base cases, the call stack and StackOverflowError.
---
A **recursive** method calls itself to solve a smaller version of the same problem. It needs:

1. A **base case** that answers directly, without recursing.
2. A **recursive case** that moves towards the base case.

```java
public class Main {
    static void countdown(int n) {
        if (n == 0) {                 // base case
            System.out.println("Liftoff!");
            return;
        }
        System.out.println(n);
        countdown(n - 1);             // recursive case: a smaller problem
    }

    public static void main(String[] args) {
        countdown(3);
    }
}
```

### Factorial

`n! = n × (n-1) × … × 1`, and `n! = n × (n-1)!`, a recursive definition:

```java
public class Main {
    static long factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }

    public static void main(String[] args) {
        System.out.println(factorial(5));
        System.out.println(factorial(20));
    }
}
```

Each call waits on the **call stack** for the smaller call to finish; then the results multiply back up. `long` is used because 20! is too big for an `int`.

### Forgetting the base case

Without a base case the calls never stop, and the stack overflows:

```java error
public class Main {
    static int forever(int n) {
        return forever(n + 1);
    }

    public static void main(String[] args) {
        System.out.println(forever(0));
    }
}
```

### Recursion for divide and conquer

Recursion shines when a problem splits into smaller copies of itself, like **binary search** on a sorted array: look at the middle, then search only the half that can contain the target.

```java
public class Main {
    static int search(int[] a, int target, int low, int high) {
        if (low > high) {
            return -1;                          // not found
        }
        int mid = (low + high) / 2;
        if (a[mid] == target) {
            return mid;
        }
        if (a[mid] < target) {
            return search(a, target, mid + 1, high);
        }
        return search(a, target, low, mid - 1);
    }

    public static void main(String[] args) {
        int[] sorted = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
        System.out.println(search(sorted, 23, 0, sorted.length - 1));
        System.out.println(search(sorted, 7, 0, sorted.length - 1));
    }
}
```

Many recursive methods can also be written as loops, which use less memory. Use recursion when it makes the code clearer: trees, nested structures and divide-and-conquer algorithms.

:::exercise Sum of digits
Write a **recursive** `static int digitSum(int n)` for non-negative `n`. `digitSum(1234)` is `10`. The last digit is `n % 10`; the rest is `n / 10`.
```java starter
public class Main {
    static int digitSum(int n) {
        return 0;
    }

    public static void main(String[] args) {
        System.out.println(digitSum(1234));
    }
}
```
```java check
int[][] cases = {{0, 0}, {7, 7}, {1234, 10}, {99999, 45}, {1000000, 1}};
for (int[] c : cases) eq(c[1], call("digitSum", c[0]), "digitSum(" + c[0] + ")");
check(source().split("digitSum\\(", -1).length - 1 >= 3, "digitSum should call itself.");
sourceLacks("while", "Solve it with recursion instead of a loop.");
```
```java solution
public class Main {
    static int digitSum(int n) {
        if (n < 10) {
            return n;
        }
        return n % 10 + digitSum(n / 10);
    }

    public static void main(String[] args) {
        System.out.println(digitSum(1234));
    }
}
```
hint: Base case: if n < 10, return n. Otherwise return n % 10 + digitSum(n / 10).
:::

:::exercise Power
Write a recursive `static long power(long base, int exp)` for `exp >= 0`, without `Math.pow`.
```java starter
public class Main {
    static long power(long base, int exp) {
        return 1;
    }

    public static void main(String[] args) {
        System.out.println(power(2, 10));
    }
}
```
```java check
eq(1024L, call("power", 2L, 10), "power(2, 10)");
eq(1L, call("power", 3L, 0), "power(3, 0)");
eq(125L, call("power", 5L, 3), "power(5, 3)");
eq(100000L, call("power", 10L, 5), "power(10, 5)");
sourceLacks("Math.pow", "Don't use Math.pow.");
```
```java solution
public class Main {
    static long power(long base, int exp) {
        if (exp == 0) {
            return 1;
        }
        return base * power(base, exp - 1);
    }

    public static void main(String[] args) {
        System.out.println(power(2, 10));
    }
}
```
hint: Anything to the power 0 is 1. Otherwise base^exp = base * power(base, exp - 1).
:::

:::quiz
? What happens if a recursive method never reaches a base case?
+ It throws StackOverflowError
- It returns 0
- It runs forever without error
= Each call uses stack memory; eventually the stack runs out.

? Why is `factorial` declared to return `long`?
+ Factorials grow beyond the range of int quickly
- Recursion requires long
- It makes it faster
= 13! already exceeds int's maximum of about 2.1 billion.
:::
