@@@ part
id: 1
title: First Steps
level: Beginner
blurb: Write and run your first Java programs. Learn how Java turns your code into bytecode, and how to work with variables, numbers, text and input.

@@@ lesson
id: how-java-runs
title: How Java runs your code
minutes: 10
summary: What a Java program looks like, what the compiler and the JVM do, and how to read your first error.
---
A **program** is a list of instructions for a computer. Here is a complete Java program. Press **Run** and watch the output panel.

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
        System.out.println("I am learning Java.");
    }
}
```

That's a lot of words for two lines of output. Don't worry about all of them yet; each one is explained over the next few lessons. For now:

- `public class Main` creates a **class** named `Main`. In Java, all code lives inside classes.
- `public static void main(String[] args)` is the **main method**: the place where the program starts.
- `System.out.println(...)` prints a line of text.
- Every statement ends with a semicolon `;`, and curly braces `{ }` group code into blocks.

### Compile, then run

Java runs your code in two steps:

1. **Compile.** The Java compiler (`javac`) reads your source code, checks it for mistakes, and translates it into **bytecode**: compact instructions stored in a `.class` file.
2. **Run.** The **Java Virtual Machine (JVM)** loads the bytecode and runs it. The JVM translates bytecode into instructions for the real processor, and speeds up frequently used code with a **just-in-time (JIT) compiler**.

Because the bytecode targets the JVM rather than a particular processor, the same compiled program runs on Windows, macOS, Linux or, as in this course, inside your web browser. This idea is often summarised as "write once, run anywhere".

Open the **Bytecode** tab after running a program to see the bytecode the compiler produced for it. You won't need to read bytecode to write Java, but it's good to know it's there.

The bundle you install to write Java is called the **JDK** (Java Development Kit). It contains the compiler, the JVM and the standard library.

### Your first error

The compiler is strict, and that's a good thing: it finds many mistakes before your program ever runs. Run this and read the message:

```java error
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello")
    }
}
```

The compiler tells you the file, the line number, and what it expected: a `;`. Add the semicolon and run it again.

There are two kinds of errors you'll meet:

- **Compile errors** happen before the program runs: a missing semicolon, a misspelled name, a type mismatch.
- **Runtime errors (exceptions)** happen while it runs: dividing a whole number by zero, or using a position that doesn't exist in a list.

### How to use this course

- Every code block has a **Run** button that loads it into the editor. Change the code and run it again.
- The first run takes a while (around 20 seconds) because the Java compiler itself has to load. After that, runs take a second or two.
- Each lesson ends with **exercises**. Write your answer in the editor and press **Check**.

:::exercise Say hello
Change the program so it prints exactly these two lines:

```output
Hello, Java!
Let's learn together.
```
```java starter
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```
```java check
outputIs("Hello, Java!\nLet's learn together.");
```
```java solution
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
        System.out.println("Let's learn together.");
    }
}
```
hint: Use two System.out.println(...) lines. Each one needs the text in double quotes and a semicolon at the end.
:::

:::quiz
? What does the Java compiler (`javac`) produce?
- Machine code for your processor
+ Bytecode in `.class` files
- A web page
= The compiler turns source code into bytecode. The JVM then runs that bytecode.

? Where does a Java program start running?
- At the first line of the file
+ In the `main` method
- In the last class of the file
= The JVM looks for `public static void main(String[] args)` and starts there.

? When is a missing semicolon reported?
+ When the code is compiled, before it runs
- Only when that line runs
- Never; semicolons are optional
= It's a compile error, so the program doesn't run at all until you fix it.
:::

@@@ lesson
id: hello-world
title: Printing, comments and structure
minutes: 10
summary: println vs print, escape sequences, comments, and the rules for writing Java statements.
---
### println and print

`System.out.println(x)` prints `x` and then moves to a new line. `System.out.print(x)` prints `x` and stays on the same line.

```java
public class Main {
    public static void main(String[] args) {
        System.out.print("Loading");
        System.out.print("...");
        System.out.println(" done!");
        System.out.println("Next line");
        System.out.println();
        System.out.println("After a blank line");
    }
}
```

You can join text and numbers with `+`:

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Apples: " + 5);
        System.out.println("Total: " + 5 * 2 + " dollars");
    }
}
```

### Escape sequences

Inside text, a backslash starts an **escape sequence**:

| Sequence | Meaning |
|---|---|
| `\n` | new line |
| `\t` | tab |
| `\"` | a double quote |
| `\\` | a backslash |

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Line one\nLine two");
        System.out.println("Name:\tAda");
        System.out.println("She said \"hi\"");
        System.out.println("C:\\Users\\ada");
    }
}
```

### Comments

Comments are notes for people; the compiler ignores them.

```java
public class Main {
    // A single-line comment starts with two slashes.

    /*
     * A block comment can span
     * several lines.
     */

    /** A Javadoc comment documents classes and methods. */
    public static void main(String[] args) {
        System.out.println("Comments don't print"); // comments can end a line too
    }
}
```

Write comments that explain *why* the code does something. Good names usually explain *what* it does.

### The rules of the layout

- Java is **case-sensitive**: `System` works, `system` doesn't.
- Statements end with `;`. Blocks are wrapped in `{ }`.
- Whitespace and indentation don't change the meaning, but consistent 4-space indentation makes code readable. Every Java programmer expects it.
- The public class name must match the file name: `public class Main` lives in `Main.java`.

:::exercise Receipt
Print this receipt exactly, using `\t` between each item and its price:

```output
Coffee	3.50
Muffin	2.25
Total	5.75
```
```java starter
public class Main {
    public static void main(String[] args) {

    }
}
```
```java check
outputIs("Coffee\t3.50\nMuffin\t2.25\nTotal\t5.75");
sourceHas("\\t", "Use the \\t escape sequence for the tab.");
```
```java solution
public class Main {
    public static void main(String[] args) {
        System.out.println("Coffee\t3.50");
        System.out.println("Muffin\t2.25");
        System.out.println("Total\t5.75");
    }
}
```
hint: System.out.println("Coffee\t3.50"); and so on for each line.
:::

:::exercise One line, three prints
Use **three** `System.out.print` calls (not `println`) followed by one empty `System.out.println()` to print `3... 2... 1...` on one line.
```java starter
public class Main {
    public static void main(String[] args) {
        System.out.println("3...");
        System.out.println("2...");
        System.out.println("1...");
    }
}
```
```java check
outputIs("3... 2... 1...");
check(source().split("System.out.print\\(", -1).length - 1 == 3, "Use exactly three System.out.print( calls.");
```
```java solution
public class Main {
    public static void main(String[] args) {
        System.out.print("3... ");
        System.out.print("2... ");
        System.out.print("1...");
        System.out.println();
    }
}
```
hint: print doesn't add a new line, so put a space at the end of the first two pieces of text.
:::

:::quiz
? What does `System.out.print("A"); System.out.print("B");` print?
+ AB
- A then B on separate lines
- A B
= `print` never adds a new line or a space.

? Which line is a valid Java comment?
- `# total price`
+ `// total price`
- `<!-- total price -->`
= Java uses `//` for single-line comments and `/* ... */` for blocks.

? What does `System.out.println("Sum: " + 2 + 3);` print?
- Sum: 5
+ Sum: 23
- An error
= Java works left to right. `"Sum: " + 2` is text, then `+ 3` adds the text "3". Write `"Sum: " + (2 + 3)` to get 5.
:::

@@@ lesson
id: variables-and-types
title: Variables and primitive types
minutes: 14
summary: Declare variables, choose between int, double, boolean, char and String, use final and var.
---
A **variable** is a named box that holds a value. In Java, every variable has a **type** that decides what it can hold, and you declare the type when you create the variable.

```java
public class Main {
    public static void main(String[] args) {
        int age = 36;
        double height = 1.68;
        boolean isStudent = false;
        char grade = 'A';
        String name = "Ada";

        System.out.println(name + " is " + age + " years old");
        System.out.println("Height: " + height + ", grade: " + grade + ", student: " + isStudent);
    }
}
```

Java is **statically typed**: the type is checked when you compile. Putting text into an `int` is a compile error, which catches many bugs early.

### The primitive types

Java has eight **primitive types** that hold simple values directly:

| Type | Holds | Example |
|---|---|---|
| `int` | whole numbers (about ±2.1 billion) | `42` |
| `long` | bigger whole numbers | `9_000_000_000L` |
| `double` | decimal numbers | `3.14` |
| `float` | less precise decimals | `3.14f` |
| `boolean` | `true` or `false` | `true` |
| `char` | one character, in single quotes | `'A'` |
| `byte`, `short` | small whole numbers | `(byte) 7` |

Most of the time you'll use `int`, `double`, `boolean` and `char`.

`String` is not a primitive; it's a **class** (that's why it starts with a capital letter). Strings use double quotes, chars use single quotes: `"A"` is a String, `'A'` is a char.

### Declaring, assigning, changing

```java
public class Main {
    public static void main(String[] args) {
        int score;          // declare
        score = 10;         // assign
        score = score + 5;  // change: read the old value, add 5, store it back
        System.out.println(score);

        int a = 1, b = 2;   // several at once
        int temp = a;       // swap two values with a temporary variable
        a = b;
        b = temp;
        System.out.println(a + " " + b);
    }
}
```

Java won't let you use a local variable before it has a value. That's another compile error that prevents bugs.

### Constants with final

`final` means the variable can't be changed after it's set. By convention, constants use UPPER_SNAKE_CASE:

```java
public class Main {
    public static void main(String[] args) {
        final double TAX_RATE = 0.08;
        double price = 50;
        System.out.println("Tax: " + price * TAX_RATE);
    }
}
```

### Naming conventions

- Variables and methods use **camelCase**: `firstName`, `totalPrice`.
- Classes use **PascalCase**: `Main`, `BankAccount`.
- Constants use **UPPER_SNAKE_CASE**: `MAX_SIZE`.
- Names can't start with a digit or be keywords like `class` or `int`.

### var: let the compiler infer the type

Since Java 10, you can write `var` for local variables when the type is obvious from the value. The variable still has a fixed type; the compiler just works it out for you.

```java
public class Main {
    public static void main(String[] args) {
        var count = 3;          // int
        var price = 4.99;       // double
        var city = "London";    // String
        System.out.println(count + " " + price + " " + city);
    }
}
```

:::exercise Profile card
Create these variables with the right types: `name` set to `"Grace"`, `year` set to `1906`, `height` set to `1.62`, and `isProgrammer` set to `true`. Then print them on one line separated by single spaces: `Grace 1906 1.62 true`.
```java starter
public class Main {
    public static void main(String[] args) {
        // declare the four variables here

    }
}
```
```java check
outputIs("Grace 1906 1.62 true");
sourceHas("String name", "Declare name as a String.");
sourceHas("int year", "Declare year as an int.");
sourceHas("double height", "Declare height as a double.");
sourceHas("boolean isProgrammer", "Declare isProgrammer as a boolean.");
```
```java solution
public class Main {
    public static void main(String[] args) {
        String name = "Grace";
        int year = 1906;
        double height = 1.62;
        boolean isProgrammer = true;
        System.out.println(name + " " + year + " " + height + " " + isProgrammer);
    }
}
```
hint: String name = "Grace"; int year = 1906; ... then print them joined with + " " + between each.
:::

:::quiz
? Which declaration is correct?
- `int price = 4.99;`
+ `double price = 4.99;`
- `char price = "4.99";`
= An `int` can't hold decimals, and a `char` holds one character in single quotes.

? What's the difference between `'A'` and `"A"`?
+ `'A'` is a char, `"A"` is a String
- They are identical
- `'A'` is a String, `"A"` is a char
= Single quotes make a `char`; double quotes make a `String`.

? What does `final int MAX = 5; MAX = 6;` do?
- Sets MAX to 6
+ Causes a compile error
- Causes a runtime error
= A `final` variable can only be assigned once, and the compiler enforces it.
:::

@@@ lesson
id: operators-and-math
title: Operators and math
minutes: 14
summary: Arithmetic, integer division, remainders, casting between types, the Math class and overflow.
---
### Arithmetic operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` `-` `*` | add, subtract, multiply | `7 * 2` | `14` |
| `/` | divide | `7 / 2` | `3` (both ints!) |
| `%` | remainder | `7 % 2` | `1` |

```java
public class Main {
    public static void main(String[] args) {
        System.out.println(7 / 2);
        System.out.println(7.0 / 2);
        System.out.println(7 % 2);
        System.out.println(2 + 3 * 4);
        System.out.println((2 + 3) * 4);
    }
}
```

### Integer division

When **both** sides of `/` are integers, Java does **integer division**: it throws away the decimal part. `7 / 2` is `3`, not `3.5`. This is one of the most common beginner bugs. If either side is a `double`, you get a decimal result.

```java
public class Main {
    public static void main(String[] args) {
        int total = 7;
        int people = 2;
        System.out.println(total / people);             // 3
        System.out.println((double) total / people);    // 3.5
        System.out.println(total / 2.0);                // 3.5
    }
}
```

### Casting

A **cast** converts a value to another type: `(double) total`. Converting to a "bigger" type (int to double) happens automatically. Converting to a "smaller" type (double to int) needs an explicit cast, because information can be lost: the decimals are cut off, not rounded.

```java
public class Main {
    public static void main(String[] args) {
        double price = 9.99;
        int whole = (int) price;
        long rounded = Math.round(price);
        System.out.println(whole + " " + rounded);

        char letter = 'A';
        int code = letter;              // chars are numbers underneath
        System.out.println(code + " " + (char) (code + 1));
    }
}
```

### Shortcut operators

```java
public class Main {
    public static void main(String[] args) {
        int x = 10;
        x += 5;   // x = x + 5
        x -= 3;   // x = x - 3
        x *= 2;   // x = x * 2
        x++;      // add 1
        x--;      // subtract 1
        System.out.println(x);
    }
}
```

### The Math class

```java
public class Main {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(81));
        System.out.println(Math.pow(2, 10));
        System.out.println(Math.abs(-5));
        System.out.println(Math.max(3, 9) + " " + Math.min(3, 9));
        System.out.println(Math.round(2.5) + " " + Math.floor(2.7) + " " + Math.ceil(2.1));
        System.out.println(Math.PI);
    }
}
```

### Overflow and floating-point surprises

An `int` can only hold values up to 2,147,483,647. Going past that **overflows** and wraps around to a negative number, silently. Use `long` for big numbers.

```java
public class Main {
    public static void main(String[] args) {
        int big = Integer.MAX_VALUE;
        System.out.println(big + 1);
        long safe = (long) big + 1;
        System.out.println(safe);
        System.out.println(0.1 + 0.2);
    }
}
```

`0.1 + 0.2` isn't exactly `0.3` because computers store decimals in binary. For money in real applications, use `java.math.BigDecimal`.

:::exercise Split the bill
Three friends share a bill of `127` dollars plus a `15%` tip. Set `each` to the amount per person and print it with exactly two decimals using `System.out.printf("%.2f%n", each);`. The output should be `48.68`.
```java starter
public class Main {
    public static void main(String[] args) {
        int bill = 127;
        double tipRate = 0.15;
        int people = 3;
        double each = 0;
        System.out.printf("%.2f%n", each);
    }
}
```
```java check
outputIs("48.68");
```
```java solution
public class Main {
    public static void main(String[] args) {
        int bill = 127;
        double tipRate = 0.15;
        int people = 3;
        double each = bill * (1 + tipRate) / people;
        System.out.printf("%.2f%n", each);
    }
}
```
hint: The total with tip is bill * (1 + tipRate). Divide that by people. Because tipRate is a double, the result is a double.
:::

:::exercise Clock time
Convert `int seconds = 7384;` into hours, minutes and seconds using `/` and `%`, and print `2h 3m 4s`.
```java starter
public class Main {
    public static void main(String[] args) {
        int seconds = 7384;

    }
}
```
```java check
outputIs("2h 3m 4s");
sourceHas("%", "Use the % operator to get the remainders.");
```
```java solution
public class Main {
    public static void main(String[] args) {
        int seconds = 7384;
        int hours = seconds / 3600;
        int minutes = seconds % 3600 / 60;
        int secs = seconds % 60;
        System.out.println(hours + "h " + minutes + "m " + secs + "s");
    }
}
```
hint: An hour has 3600 seconds: hours = seconds / 3600. What's left is seconds % 3600; divide that by 60 for the minutes.
:::

:::quiz
? What is `9 / 2` in Java?
+ 4
- 4.5
- 5
= Both are ints, so Java uses integer division and drops the .5.

? What is `(int) 3.99`?
+ 3
- 4
- A compile error
= Casting to int cuts off the decimal part. Use `Math.round` to round.

? What is `17 % 5`?
- 3
+ 2
- 3.4
= 5 goes into 17 three times (15) with 2 left over.
:::

@@@ lesson
id: strings
title: Strings
minutes: 15
summary: Work with text: length, characters, substrings, searching, comparing with equals, and formatting.
---
A `String` holds text. Strings are **objects**, so you use their **methods** with a dot.

```java
public class Main {
    public static void main(String[] args) {
        String word = "Python";
        System.out.println(word.length());
        System.out.println(word.charAt(0));
        System.out.println(word.toUpperCase());
        System.out.println(word.substring(0, 2));
        System.out.println(word.indexOf("th"));
        System.out.println(word.contains("yth"));
        System.out.println(word.replace("P", "J"));
    }
}
```

### Indexes start at 0

Each character has a position (an **index**), starting at **0**. The last index is `length() - 1`.

```output
 J  a  v  a
 0  1  2  3
```

`substring(start, end)` returns the characters from `start` up to, but **not including**, `end`. `substring(start)` goes to the end.

```java
public class Main {
    public static void main(String[] args) {
        String s = "Hello, World";
        System.out.println(s.substring(7));
        System.out.println(s.substring(0, 5));
        System.out.println(s.charAt(s.length() - 1));
    }
}
```

`charAt(12)` on a 12-character string throws a `StringIndexOutOfBoundsException` at runtime.

### Strings can't be changed

Strings are **immutable**: methods like `toUpperCase()` return a **new** string and leave the original alone.

```java
public class Main {
    public static void main(String[] args) {
        String name = "ada";
        name.toUpperCase();              // result thrown away
        System.out.println(name);
        name = name.toUpperCase();       // keep the result
        System.out.println(name);
    }
}
```

### Comparing strings: equals, not ==

This is one of the most important rules in Java. `==` checks whether two variables refer to the **same object**. `equals` checks whether two strings contain the **same text**. Always use `equals` for strings.

```java
public class Main {
    public static void main(String[] args) {
        String a = "hello";
        String b = new String("hello");
        System.out.println(a == b);              // false: different objects
        System.out.println(a.equals(b));         // true: same text
        System.out.println("HELLO".equalsIgnoreCase(a));
        System.out.println("apple".compareTo("banana") < 0);  // alphabetical order
    }
}
```

### Useful methods

| Method | Result |
|---|---|
| `s.trim()` / `s.strip()` | remove surrounding whitespace |
| `s.isEmpty()` / `s.isBlank()` | empty? only whitespace? |
| `s.startsWith(x)` / `s.endsWith(x)` | true/false |
| `s.split(",")` | array of parts |
| `String.join("-", parts)` | glue parts together |
| `s.repeat(3)` | repeat the text |
| `String.valueOf(42)` | turn anything into a String |

```java
public class Main {
    public static void main(String[] args) {
        String csv = "red,green,blue";
        String[] parts = csv.split(",");
        System.out.println(parts.length + " colors, first is " + parts[0]);
        System.out.println(String.join(" | ", parts));
        System.out.println("ha".repeat(3));
        System.out.println("  padded  ".strip() + "!");
    }
}
```

### Formatting with printf and String.format

`printf` fills placeholders in a template: `%s` for text, `%d` for whole numbers, `%f` for decimals, and `%n` for a new line.

```java
public class Main {
    public static void main(String[] args) {
        String item = "Notebook";
        int qty = 3;
        double price = 4.5;
        System.out.printf("%s x%d costs $%.2f%n", item, qty, qty * price);
        String line = String.format("[%-8s|%5d]", "left", 42);
        System.out.println(line);
        System.out.printf("%,d%n", 1234567);
    }
}
```

`%.2f` means two decimal places, `%-8s` pads text to 8 characters aligned left, `%5d` pads a number to 5 characters, and `%,d` adds thousands separators.

:::exercise Initials
Given `first = "grace"` and `last = "hopper"`, build `"G.H."` and print it. Use `charAt` and `Character.toUpperCase`, or `substring` and `toUpperCase`.
```java starter
public class Main {
    public static void main(String[] args) {
        String first = "grace";
        String last = "hopper";
        String initials = "";
        System.out.println(initials);
    }
}
```
```java check
outputIs("G.H.");
```
```java solution
public class Main {
    public static void main(String[] args) {
        String first = "grace";
        String last = "hopper";
        String initials = first.substring(0, 1).toUpperCase() + "." + last.substring(0, 1).toUpperCase() + ".";
        System.out.println(initials);
    }
}
```
hint: first.substring(0, 1) is "g". Uppercase it, add ".", and do the same for last.
:::

:::exercise Is it a palindrome?
Write a method `static boolean isPalindrome(String s)` that returns true if `s` reads the same forwards and backwards, **ignoring case**. You can reverse a string with `new StringBuilder(s).reverse().toString()`.
```java starter
public class Main {
    static boolean isPalindrome(String s) {
        return false;
    }

    public static void main(String[] args) {
        System.out.println(isPalindrome("Racecar"));
    }
}
```
```java check
eq(true, call("isPalindrome", "Racecar"), "isPalindrome(\"Racecar\")");
eq(true, call("isPalindrome", "noon"), "isPalindrome(\"noon\")");
eq(false, call("isPalindrome", "Java"), "isPalindrome(\"Java\")");
eq(true, call("isPalindrome", ""), "isPalindrome(\"\")");
```
```java solution
public class Main {
    static boolean isPalindrome(String s) {
        String lower = s.toLowerCase();
        String reversed = new StringBuilder(lower).reverse().toString();
        return lower.equals(reversed);
    }

    public static void main(String[] args) {
        System.out.println(isPalindrome("Racecar"));
    }
}
```
hint: Lowercase the string first, reverse it, then compare the two with equals (not ==).
:::

:::quiz
? Why should you compare strings with `equals` instead of `==`?
+ `==` checks if they are the same object; `equals` checks the text
- `==` doesn't compile for strings
- `equals` is faster
= Two strings with the same text can be different objects, so `==` can be false.

? What is `"Java".substring(1, 3)`?
- "Jav"
+ "av"
- "ava"
= It starts at index 1 ('a') and stops before index 3.

? After `String s = "hi"; s.toUpperCase();`, what is `s`?
+ "hi"
- "HI"
= Strings are immutable. Write `s = s.toUpperCase();` to keep the change.
:::

@@@ lesson
id: scanner-input
title: Reading input with Scanner
minutes: 12
summary: Read text and numbers with Scanner, avoid the nextInt/nextLine trap, and parse strings into numbers.
---
`Scanner` reads input. In this course, the **Input** box under the editor plays the keyboard: put one line for each value your program reads.

```java stdin=Ada
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        System.out.print("What is your name? ");
        String name = in.nextLine();
        System.out.println("Nice to meet you, " + name + "!");
    }
}
```

`import java.util.Scanner;` at the top tells the compiler where to find the `Scanner` class. Classes in `java.lang` (like `String`, `Math` and `System`) don't need importing.

### Reading numbers

| Method | Reads |
|---|---|
| `nextLine()` | the rest of the line, as a String |
| `next()` | the next word |
| `nextInt()` | the next whole number |
| `nextDouble()` | the next decimal number |
| `hasNextInt()` | true if the next thing is a whole number |

```java stdin=1990
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        System.out.print("Birth year? ");
        int year = in.nextInt();
        System.out.println("You are about " + (2026 - year) + " years old");
    }
}
```

If the user types something that isn't a number, `nextInt()` throws an `InputMismatchException`:

```java stdin=nineteen-ninety error
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int year = in.nextInt();
        System.out.println(year);
    }
}
```

### The nextInt / nextLine trap

`nextInt()` reads the number but **leaves the end of the line** behind. A `nextLine()` right after it reads that leftover empty line instead of waiting for new text:

```java stdin=36|Ada Lovelace
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int age = in.nextInt();
        String name = in.nextLine();        // reads the rest of the "36" line: ""
        System.out.println("[" + name + "] is " + age);

        // The fix: read whole lines and convert them yourself.
        Scanner in2 = new Scanner("36\nAda Lovelace\n");
        int age2 = Integer.parseInt(in2.nextLine());
        String name2 = in2.nextLine();
        System.out.println("[" + name2 + "] is " + age2);
    }
}
```

A reliable habit: read every line with `nextLine()`, then convert with `Integer.parseInt` or `Double.parseDouble`.

### Parsing strings into numbers

```java
public class Main {
    public static void main(String[] args) {
        int a = Integer.parseInt("42");
        double b = Double.parseDouble("2.5");
        String c = String.valueOf(a + b);
        System.out.println(a + b);
        System.out.println(c + "!");
    }
}
```

`Integer.parseInt("4.5")` and `Integer.parseInt("abc")` throw a `NumberFormatException`. You'll learn to catch exceptions in Part 5.

:::exercise Temperature converter
Read a temperature in Celsius (one line, possibly a decimal), convert it with `F = C * 9 / 5 + 32`, and print it with one decimal place: `Fahrenheit: 98.6`.

The checker types `37`.
```java starter
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);

    }
}
```
```java stdin
37
```
```java check
check(output().strip().endsWith("Fahrenheit: 98.6"), "The output should end with Fahrenheit: 98.6 but was:\n" + output());
check(runWith("100\n").strip().endsWith("Fahrenheit: 212.0"), "With input 100 the output should end with Fahrenheit: 212.0");
```
```java solution
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        double celsius = Double.parseDouble(in.nextLine());
        double fahrenheit = celsius * 9 / 5 + 32;
        System.out.printf("Fahrenheit: %.1f%n", fahrenheit);
    }
}
```
hint: Read the line with in.nextLine(), convert it with Double.parseDouble, then use printf with %.1f.
:::

:::quiz
? Why does `nextLine()` right after `nextInt()` often return an empty string?
+ `nextInt()` leaves the end of the line unread
- `nextLine()` only works once
- Scanner can't mix types
= The leftover newline is read as an empty line. Read whole lines and parse them instead.

? What does `Integer.parseInt("12") + 1` give?
+ 13
- "121"
- An error
= `parseInt` turns the text into the number 12.

? Which class needs an import?
+ `java.util.Scanner`
- `String`
- `Math`
= Classes in `java.lang` are available automatically; everything else needs an import.
:::
