@@@ part
id: 2
title: Control Flow
level: Beginner
blurb: Make decisions with if and switch, and repeat work with while, do-while and for loops.

@@@ lesson
id: conditions
title: Booleans and if statements
minutes: 14
summary: Compare values, combine conditions with && || !, and choose between branches with if, else if and else.
---
A **boolean** expression is either `true` or `false`. Comparison operators produce booleans:

| Operator | Meaning |
|---|---|
| `==` | equal (for primitives) |
| `!=` | not equal |
| `<` `>` `<=` `>=` | less / greater (or equal) |

```java
public class Main {
    public static void main(String[] args) {
        int age = 20;
        System.out.println(age >= 18);
        System.out.println(age == 21);
        System.out.println(age != 21);
    }
}
```

Remember from the Strings lesson: compare **strings** with `equals`, not `==`.

### if, else if, else

```java
public class Main {
    public static void main(String[] args) {
        int score = 82;
        String grade;
        if (score >= 90) {
            grade = "A";
        } else if (score >= 80) {
            grade = "B";
        } else if (score >= 70) {
            grade = "C";
        } else {
            grade = "F";
        }
        System.out.println("Score " + score + " gets " + grade);
    }
}
```

- The condition goes in **parentheses**, and the code to run goes in **braces**.
- Java checks the branches from top to bottom and runs **only the first** that is true. That's why `score >= 90` must come before `score >= 80`.
- The `else` branch is optional and runs when nothing else matched.

Braces are technically optional for a single statement, but always use them. Leaving them out is a classic source of bugs when someone later adds a second line.

### Combining conditions

- `a && b` (and) is true only if **both** are true.
- `a || b` (or) is true if **at least one** is true.
- `!a` (not) flips true and false.

```java
public class Main {
    public static void main(String[] args) {
        boolean hasTicket = true;
        boolean isVip = false;
        int age = 16;

        if (hasTicket && age >= 18) {
            System.out.println("Welcome in");
        } else if (hasTicket || isVip) {
            System.out.println("Welcome to the family area");
        }
        System.out.println(!isVip);
    }
}
```

`&&` and `||` **short-circuit**: if the left side already decides the answer, the right side isn't evaluated. That makes checks like `name != null && name.length() > 3` safe.

### The ternary operator

For choosing between two values, `condition ? valueIfTrue : valueIfFalse` is a compact form:

```java
public class Main {
    public static void main(String[] args) {
        int n = 7;
        String kind = (n % 2 == 0) ? "even" : "odd";
        System.out.println(n + " is " + kind);
    }
}
```

:::exercise Ticket price
Write `static int ticketPrice(int age)` returning `0` for under 3, `8` for ages 3 to 12, `15` for 13 to 64, and `10` for 65 and over.
```java starter
public class Main {
    static int ticketPrice(int age) {
        return 15;
    }

    public static void main(String[] args) {
        System.out.println(ticketPrice(10));
    }
}
```
```java check
int[][] cases = {{0, 0}, {2, 0}, {3, 8}, {12, 8}, {13, 15}, {64, 15}, {65, 10}, {90, 10}};
for (int[] c : cases) eq(c[1], call("ticketPrice", c[0]), "ticketPrice(" + c[0] + ")");
```
```java solution
public class Main {
    static int ticketPrice(int age) {
        if (age < 3) {
            return 0;
        } else if (age <= 12) {
            return 8;
        } else if (age <= 64) {
            return 15;
        } else {
            return 10;
        }
    }

    public static void main(String[] args) {
        System.out.println(ticketPrice(10));
    }
}
```
hint: Check from youngest to oldest: if (age < 3) ... else if (age <= 12) ... else if (age <= 64) ... else ...
:::

:::exercise Leap year
Write `static boolean isLeapYear(int year)`. A year is a leap year if it's divisible by 4, **except** years divisible by 100, which are leap years only if they're also divisible by 400.
```java starter
public class Main {
    static boolean isLeapYear(int year) {
        return year % 4 == 0;
    }

    public static void main(String[] args) {
        System.out.println(isLeapYear(2024));
    }
}
```
```java check
eq(true, call("isLeapYear", 2024), "isLeapYear(2024)");
eq(false, call("isLeapYear", 2023), "isLeapYear(2023)");
eq(false, call("isLeapYear", 1900), "isLeapYear(1900)");
eq(true, call("isLeapYear", 2000), "isLeapYear(2000)");
```
```java solution
public class Main {
    static boolean isLeapYear(int year) {
        return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
    }

    public static void main(String[] args) {
        System.out.println(isLeapYear(2024));
    }
}
```
hint: return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
:::

:::quiz
? With `int x = 5;`, what does `if (x > 3) {...} else if (x > 1) {...}` run?
+ Only the first branch
- Both branches
- Only the second branch
= Only the first true branch runs; the rest are skipped.

? What is `true || (1 / 0 == 0)`?
+ true, and the division never happens
- An ArithmeticException
- false
= `||` short-circuits: the left side is already true, so the right side isn't evaluated.

? What does `x > 0 ? "pos" : "non-pos"` give when x is 0?
- "pos"
+ "non-pos"
= `0 > 0` is false, so the value after the colon is used.
:::

@@@ lesson
id: switch
title: switch statements and expressions
minutes: 12
summary: Compare one value against many options with classic switch, and with modern arrow-style switch expressions.
---
When you compare one value against several fixed options, `switch` is clearer than a long `if/else if` chain.

### Modern switch (Java 14+)

The arrow form is the one to use in new code. Each `case` runs only its own code, so there's no fall-through, and several values can share a case:

```java
public class Main {
    public static void main(String[] args) {
        String day = "SAT";
        switch (day) {
            case "SAT", "SUN" -> System.out.println("Weekend!");
            case "FRI" -> System.out.println("Almost there");
            default -> System.out.println("Weekday");
        }
    }
}
```

### switch as an expression

A switch can also **produce a value**. Every possible input must be covered, which is why `default` is required here:

```java
public class Main {
    public static void main(String[] args) {
        int month = 2;
        int days = switch (month) {
            case 4, 6, 9, 11 -> 30;
            case 2 -> 28;
            default -> 31;
        };
        System.out.println(days);

        String size = "M";
        double price = switch (size) {
            case "S" -> 2.50;
            case "M" -> 3.00;
            case "L" -> {
                double base = 3.00;
                yield base + 0.75;      // yield returns a value from a block
            }
            default -> throw new IllegalArgumentException("Unknown size: " + size);
        };
        System.out.println(price);
    }
}
```

### Classic switch and fall-through

You'll see the older colon form in existing code. Its trap: without `break`, execution **falls through** into the next case.

```java
public class Main {
    public static void main(String[] args) {
        int level = 2;
        switch (level) {
            case 1:
                System.out.println("Bronze");
                break;
            case 2:
                System.out.println("Silver");
                // missing break: falls through!
            case 3:
                System.out.println("Gold");
                break;
            default:
                System.out.println("None");
        }
    }
}
```

That prints both "Silver" and "Gold". Prefer the arrow form, which never falls through.

switch works with `int`, `char`, `String` and enums (Part 4), but not with `double` or `boolean`.

:::exercise Day type
Write `static String dayType(String day)` using a **switch expression**: return `"weekend"` for `"SAT"` and `"SUN"`, `"weekday"` for `"MON"` to `"FRI"`, and `"invalid"` for anything else.
```java starter
public class Main {
    static String dayType(String day) {
        return "weekday";
    }

    public static void main(String[] args) {
        System.out.println(dayType("SUN"));
    }
}
```
```java check
eq("weekend", call("dayType", "SAT"), "dayType(\"SAT\")");
eq("weekend", call("dayType", "SUN"), "dayType(\"SUN\")");
eq("weekday", call("dayType", "WED"), "dayType(\"WED\")");
eq("weekday", call("dayType", "FRI"), "dayType(\"FRI\")");
eq("invalid", call("dayType", "XYZ"), "dayType(\"XYZ\")");
sourceHas("->", "Use the arrow form of switch.");
```
```java solution
public class Main {
    static String dayType(String day) {
        return switch (day) {
            case "SAT", "SUN" -> "weekend";
            case "MON", "TUE", "WED", "THU", "FRI" -> "weekday";
            default -> "invalid";
        };
    }

    public static void main(String[] args) {
        System.out.println(dayType("SUN"));
    }
}
```
hint: return switch (day) { case "SAT", "SUN" -> "weekend"; case "MON", "TUE", "WED", "THU", "FRI" -> "weekday"; default -> "invalid"; };
:::

:::quiz
? What happens in a classic `case` without `break`?
+ Execution continues into the next case
- A compile error
- The switch ends anyway
= That's fall-through, the classic switch's biggest trap.

? Why does a switch *expression* need a `default`?
+ It must produce a value for every possible input
- It's optional
- Only for strings
= An expression always has to return something, so every case must be covered.
:::

@@@ lesson
id: while-loops
title: while and do-while loops
minutes: 10
summary: Repeat code while a condition holds, use counters and accumulators, and avoid infinite loops.
---
A `while` loop repeats its body as long as its condition is `true`. The condition is checked **before** each pass.

```java
public class Main {
    public static void main(String[] args) {
        int count = 1;
        while (count <= 5) {
            System.out.println("Count is " + count);
            count++;
        }
        System.out.println("Done!");
    }
}
```

### Loops with an unknown number of steps

`while` is the natural choice when you don't know in advance how many passes you need:

```java
public class Main {
    public static void main(String[] args) {
        double balance = 1000;
        int years = 0;
        while (balance < 2000) {
            balance *= 1.07;
            years++;
        }
        System.out.printf("Doubled after %d years: $%.2f%n", years, balance);
    }
}
```

### Accumulators

```java
public class Main {
    public static void main(String[] args) {
        int n = 1;
        int total = 0;
        while (n <= 100) {
            total += n;
            n++;
        }
        System.out.println("Sum of 1..100 = " + total);
    }
}
```

### do-while: run at least once

A `do-while` checks its condition **after** the body, so the body always runs at least once. It's handy for "ask until valid" input:

```java stdin=-3|0|7
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n;
        do {
            System.out.print("Enter a positive number: ");
            n = Integer.parseInt(in.nextLine());
            System.out.println(n);
        } while (n <= 0);
        System.out.println("Thanks!");
    }
}
```

### Infinite loops

If the condition never becomes false, the loop never ends. Forgetting `count++` above would do it. In this browser editor an infinite loop freezes the page; reload it if that happens (your progress is saved).

:::exercise Digit counter
Write `static int countDigits(int n)` that returns how many digits a non-negative number has, using a `while` loop that divides by 10. `countDigits(0)` should be `1`.
```java starter
public class Main {
    static int countDigits(int n) {
        return 0;
    }

    public static void main(String[] args) {
        System.out.println(countDigits(12345));
    }
}
```
```java check
int[][] cases = {{0, 1}, {7, 1}, {10, 2}, {12345, 5}, {1000000, 7}};
for (int[] c : cases) eq(c[1], call("countDigits", c[0]), "countDigits(" + c[0] + ")");
sourceHas("while", "Use a while loop.");
```
```java solution
public class Main {
    static int countDigits(int n) {
        int digits = 1;
        while (n >= 10) {
            n /= 10;
            digits++;
        }
        return digits;
    }

    public static void main(String[] args) {
        System.out.println(countDigits(12345));
    }
}
```
hint: Start at 1 digit. While n >= 10, divide n by 10 and add one to the count.
:::

:::exercise Collatz steps
Write `static int collatzSteps(int n)`: if `n` is even, halve it; if odd, make it `3 * n + 1`. Count the steps until `n` reaches 1. `collatzSteps(6)` is `8`.
```java starter
public class Main {
    static int collatzSteps(int n) {
        int steps = 0;
        return steps;
    }

    public static void main(String[] args) {
        System.out.println(collatzSteps(6));
    }
}
```
```java check
int[][] cases = {{1, 0}, {2, 1}, {6, 8}, {7, 16}, {27, 111}};
for (int[] c : cases) eq(c[1], call("collatzSteps", c[0]), "collatzSteps(" + c[0] + ")");
```
```java solution
public class Main {
    static int collatzSteps(int n) {
        int steps = 0;
        while (n != 1) {
            if (n % 2 == 0) {
                n = n / 2;
            } else {
                n = 3 * n + 1;
            }
            steps++;
        }
        return steps;
    }

    public static void main(String[] args) {
        System.out.println(collatzSteps(6));
    }
}
```
hint: Loop while (n != 1). Inside, use if/else to update n, then steps++.
:::

:::quiz
? What's the difference between `while` and `do-while`?
+ `do-while` always runs its body at least once
- `while` always runs at least once
- There is no difference
= `do-while` checks the condition after the body.

? How many times does `int i = 0; while (i < 3) { i++; }` run its body?
- 2
+ 3
- 4
= For i = 0, 1 and 2. When i is 3 the condition is false.
:::

@@@ lesson
id: for-loops
title: for loops
minutes: 12
summary: Count with for loops, loop over arrays and strings, and nest loops for grids.
---
A `for` loop puts the three parts of a counting loop in one line: **start**, **condition** and **update**.

```java
public class Main {
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) {
            System.out.println(i + " x 7 = " + i * 7);
        }
    }
}
```

Read it as: start with `i = 1`; while `i <= 5`, run the body, then do `i++`.

### Counting patterns

```java
public class Main {
    public static void main(String[] args) {
        for (int i = 0; i < 10; i += 3) System.out.print(i + " ");
        System.out.println();
        for (int i = 5; i > 0; i--) System.out.print(i + " ");
        System.out.println("Liftoff!");
    }
}
```

The loop variable `i` exists only inside the loop.

### Looping over a string

```java
public class Main {
    public static void main(String[] args) {
        String word = "banana";
        int count = 0;
        for (int i = 0; i < word.length(); i++) {
            if (word.charAt(i) == 'a') {
                count++;
            }
        }
        System.out.println("a appears " + count + " times");
    }
}
```

Notice `i < word.length()`, not `<=`. The last index is `length() - 1`; using `<=` causes an out-of-bounds error. This **off-by-one** mistake is extremely common.

### The enhanced for loop

When you just need each item and not its position, the **for-each** loop is simpler. It works on arrays (next part) and collections:

```java
public class Main {
    public static void main(String[] args) {
        String[] fruits = {"apple", "banana", "cherry"};
        for (String fruit : fruits) {
            System.out.println("I like " + fruit);
        }
        for (char c : "hey".toCharArray()) {
            System.out.print(c + "-");
        }
        System.out.println();
    }
}
```

### Nested loops

```java
public class Main {
    public static void main(String[] args) {
        for (int row = 1; row <= 3; row++) {
            for (int col = 1; col <= 4; col++) {
                System.out.printf("%4d", row * col);
            }
            System.out.println();
        }
    }
}
```

The inner loop runs completely for each pass of the outer loop: 3 rows × 4 columns = 12 numbers.

:::exercise Sum of multiples
Write `static int sumMultiples(int limit)` returning the sum of all numbers **below** `limit` that are multiples of 3 or 5. For 10 that's 3 + 5 + 6 + 9 = 23.
```java starter
public class Main {
    static int sumMultiples(int limit) {
        int total = 0;
        return total;
    }

    public static void main(String[] args) {
        System.out.println(sumMultiples(10));
    }
}
```
```java check
int[][] cases = {{10, 23}, {1, 0}, {16, 60}, {1000, 233168}};
for (int[] c : cases) eq(c[1], call("sumMultiples", c[0]), "sumMultiples(" + c[0] + ")");
```
```java solution
public class Main {
    static int sumMultiples(int limit) {
        int total = 0;
        for (int n = 0; n < limit; n++) {
            if (n % 3 == 0 || n % 5 == 0) {
                total += n;
            }
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(sumMultiples(10));
    }
}
```
hint: for (int n = 0; n < limit; n++) and add n to total when n % 3 == 0 || n % 5 == 0.
:::

:::exercise Triangle
Print a right triangle of `*` with 4 rows using nested loops:

```output
*
**
***
****
```
```java starter
public class Main {
    public static void main(String[] args) {

    }
}
```
```java check
outputIs("*\n**\n***\n****");
sourceLacks("\"**", "Build each row with a loop instead of typing the stars.");
```
```java solution
public class Main {
    public static void main(String[] args) {
        for (int row = 1; row <= 4; row++) {
            for (int i = 0; i < row; i++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
```
hint: The outer loop goes from 1 to 4. The inner loop prints row stars with print, then println() ends the line.
:::

:::quiz
? What does `for (int i = 0; i < 3; i++)` produce for `i`?
+ 0, 1, 2
- 1, 2, 3
- 0, 1, 2, 3
= It starts at 0 and stops before 3.

? When should you use the enhanced for loop?
+ When you need each item but not its index
- Only for strings
- When you need to change the index
= `for (String s : items)` reads cleaner when the position doesn't matter.
:::

@@@ lesson
id: break-continue
title: break, continue and loop patterns
minutes: 10
summary: Leave a loop early, skip iterations, search with flags, and break out of nested loops with labels.
---
### break: leave the loop now

```java
public class Main {
    public static void main(String[] args) {
        int[] numbers = {4, 7, 12, -1, 8};
        for (int n : numbers) {
            if (n < 0) {
                System.out.println("Found a negative number, stopping.");
                break;
            }
            System.out.println("Processing " + n);
        }
    }
}
```

### continue: skip to the next iteration

```java
public class Main {
    public static void main(String[] args) {
        for (int n = 1; n <= 10; n++) {
            if (n % 3 == 0) {
                continue;
            }
            System.out.print(n + " ");
        }
        System.out.println();
    }
}
```

### Searching with a flag

A common pattern: assume something, loop to look for a counterexample, and `break` as soon as you find one.

```java
public class Main {
    public static void main(String[] args) {
        int n = 91;
        boolean prime = n >= 2;
        for (int d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                prime = false;
                System.out.println(n + " is divisible by " + d);
                break;
            }
        }
        System.out.println(n + (prime ? " is prime" : " is not prime"));
    }
}
```

### Labeled break for nested loops

A plain `break` only leaves the innermost loop. To leave an outer loop, give it a **label**:

```java
public class Main {
    public static void main(String[] args) {
        int[][] grid = {{1, 2, 3}, {4, 42, 6}, {7, 8, 9}};
        search:
        for (int r = 0; r < grid.length; r++) {
            for (int c = 0; c < grid[r].length; c++) {
                if (grid[r][c] == 42) {
                    System.out.println("Found 42 at row " + r + ", column " + c);
                    break search;
                }
            }
        }
    }
}
```

Labels are rarely needed. Often, moving the loops into a method and using `return` is clearer.

### while (true) with break

```java stdin=hello|java|quit
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        while (true) {
            String line = in.nextLine();
            if (line.equals("quit")) {
                break;
            }
            System.out.println(line.toUpperCase());
        }
        System.out.println("Bye");
    }
}
```

:::exercise Is it prime?
Write `static boolean isPrime(int n)`. Numbers below 2 aren't prime. Test divisors only while `d * d <= n`, and stop as soon as you find one.
```java starter
public class Main {
    static boolean isPrime(int n) {
        return false;
    }

    public static void main(String[] args) {
        System.out.println(isPrime(97));
    }
}
```
```java check
int[] primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47};
java.util.Set<Integer> set = new java.util.HashSet<>();
for (int p : primes) set.add(p);
for (int n = -2; n < 50; n++) eq(set.contains(n), call("isPrime", n), "isPrime(" + n + ")");
eq(true, call("isPrime", 7919), "isPrime(7919)");
```
```java solution
public class Main {
    static boolean isPrime(int n) {
        if (n < 2) {
            return false;
        }
        for (int d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isPrime(97));
    }
}
```
hint: Return false for n < 2. Loop d from 2 while d * d <= n; if n % d == 0 return false. After the loop, return true.
:::

:::quiz
? What does `continue` do?
- Ends the loop
+ Skips the rest of this iteration
- Restarts from the first iteration
= `continue` jumps to the next iteration; `break` ends the loop.

? A `break` inside an inner loop leaves…
+ only the inner loop
- both loops
- the whole method
= Use a labeled break (or return) to leave an outer loop.
:::
