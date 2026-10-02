@@@ part
id: 5
title: The Core Library
level: Intermediate
blurb: Handle errors with exceptions, write type-safe generic code, and store data in lists, sets and maps from Java's collections framework.

@@@ lesson
id: stringbuilder-and-wrappers
title: StringBuilder and wrapper classes
minutes: 12
summary: Build strings efficiently, convert between primitives and objects, and avoid the Integer == trap.
---
### StringBuilder

Strings are immutable, so `s = s + x` in a loop creates a brand-new string every time. For building text piece by piece, use a **StringBuilder**, which can change in place:

```java
public class Main {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= 5; i++) {
            sb.append(i);
            if (i < 5) {
                sb.append(", ");
            }
        }
        System.out.println(sb.toString());

        StringBuilder word = new StringBuilder("stressed");
        System.out.println(word.reverse());
        word.reverse().insert(0, "[").append("]").setCharAt(1, 'S');
        System.out.println(word);
        System.out.println(word.length() + " " + word.indexOf("ss"));
    }
}
```

Most methods return the same builder, so calls can be **chained**. Call `toString()` when you need a real `String`.

### Wrapper classes

Every primitive has a **wrapper class** that represents it as an object:

| Primitive | Wrapper |
|---|---|
| `int` | `Integer` |
| `double` | `Double` |
| `boolean` | `Boolean` |
| `char` | `Character` |
| `long` | `Long` |

Wrappers matter because collections like `ArrayList` can only hold objects: you write `ArrayList<Integer>`, never `ArrayList<int>`. They also hold handy static methods:

```java
public class Main {
    public static void main(String[] args) {
        int n = Integer.parseInt("123");
        double d = Double.parseDouble("4.5");
        System.out.println(n + d);
        System.out.println(Integer.MAX_VALUE + " " + Integer.MIN_VALUE);
        System.out.println(Integer.toBinaryString(10) + " " + Integer.toHexString(255));
        System.out.println(Character.isDigit('7') + " " + Character.isLetter('x') + " " + Character.toUpperCase('q'));
        System.out.println(Integer.compare(3, 7) + " " + Double.isNaN(0.0 / 0.0));
    }
}
```

### Autoboxing

Java converts between primitives and wrappers automatically. Primitive to wrapper is **autoboxing**; wrapper to primitive is **unboxing**:

```java
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ArrayList<Integer> list = new ArrayList<>();
        list.add(5);                 // int 5 autoboxed to Integer
        int first = list.get(0);     // unboxed back to int
        System.out.println(first * 2);

        Integer maybe = null;        // a wrapper can be null; a primitive can't
        System.out.println(maybe == null);
    }
}
```

Unboxing a `null` wrapper throws a `NullPointerException`.

### The Integer == trap

`==` on wrapper objects compares **references**, just like with strings. Java caches small Integer values (−128 to 127), so `==` *seems* to work for small numbers and then silently fails for big ones:

```java
public class Main {
    public static void main(String[] args) {
        Integer a = 100, b = 100;
        Integer c = 1000, d = 1000;
        System.out.println(a == b);        // true, thanks to the cache
        System.out.println(c == d);        // false!
        System.out.println(c.equals(d));   // true: always use equals
    }
}
```

Rule: compare wrapper objects with `equals`, or unbox them to primitives first.

:::exercise Join with a builder
Write `static String joinNumbers(int[] nums, String sep)` using a `StringBuilder`, returning the numbers separated by `sep`. `joinNumbers(new int[]{1, 2, 3}, "-")` returns `"1-2-3"`; an empty array gives `""`.
```java starter
public class Main {
    static String joinNumbers(int[] nums, String sep) {
        return "";
    }

    public static void main(String[] args) {
        System.out.println(joinNumbers(new int[]{1, 2, 3}, "-"));
    }
}
```
```java check
eq("1-2-3", call("joinNumbers", new int[]{1, 2, 3}, "-"), "joinNumbers({1, 2, 3}, \"-\")");
eq("42", call("joinNumbers", new int[]{42}, ", "), "joinNumbers({42}, \", \")");
eq("", call("joinNumbers", new int[]{}, ","), "joinNumbers({}, \",\")");
eq("7 | 8", call("joinNumbers", new int[]{7, 8}, " | "), "joinNumbers({7, 8}, \" | \")");
sourceHas("StringBuilder", "Use a StringBuilder.");
```
```java solution
public class Main {
    static String joinNumbers(int[] nums, String sep) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < nums.length; i++) {
            if (i > 0) {
                sb.append(sep);
            }
            sb.append(nums[i]);
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println(joinNumbers(new int[]{1, 2, 3}, "-"));
    }
}
```
hint: Append the separator before every number except the first (if (i > 0) sb.append(sep);), then append the number.
:::

:::quiz
? Why prefer StringBuilder for building text in a loop?
+ It changes in place instead of creating a new String each time
- Strings can't be concatenated in loops
- StringBuilder is the only way to add numbers to text
= Repeated `+` on Strings copies the text every time.

? What does `Integer x = 500, y = 500; x == y` usually give?
+ false
- true
- A compile error
= `==` compares references; values outside −128..127 aren't cached. Use `equals`.

? Why does `ArrayList<int>` not compile?
+ Generic types need objects, so you write `ArrayList<Integer>`
- ArrayList can only hold Strings
- It does compile
= Wrappers let primitives live in collections.
:::

@@@ lesson
id: exceptions
title: Exceptions
minutes: 18
summary: Catch and throw exceptions, understand checked vs unchecked, write custom exceptions, and clean up with try-with-resources.
---
An **exception** is an object that signals something went wrong while the program runs. If nothing handles it, the program stops and prints a stack trace.

### try and catch

```java
public class Main {
    public static void main(String[] args) {
        String[] inputs = {"42", "3.5", "abc"};
        for (String text : inputs) {
            try {
                int n = Integer.parseInt(text);
                System.out.println("Got " + n);
            } catch (NumberFormatException e) {
                System.out.println("'" + text + "' is not a whole number: " + e.getMessage());
            }
        }
        System.out.println("The program keeps going");
    }
}
```

When an exception is thrown inside `try`, Java jumps to the first matching `catch`. Catch **specific** exceptions; catching everything hides real bugs.

### Several catches and finally

```java
public class Main {
    static int divide(String a, String b) {
        try {
            return Integer.parseInt(a) / Integer.parseInt(b);
        } catch (NumberFormatException e) {
            System.out.println("Not a number");
            return 0;
        } catch (ArithmeticException e) {
            System.out.println("Can't divide by zero");
            return 0;
        } finally {
            System.out.println("-- done --");      // always runs, even after return
        }
    }

    public static void main(String[] args) {
        System.out.println(divide("10", "2"));
        System.out.println(divide("10", "0"));
        System.out.println(divide("ten", "2"));
    }
}
```

You can also catch several types in one block: `catch (NumberFormatException | ArithmeticException e)`.

### The exception hierarchy

```output
Throwable
├── Error                      serious JVM problems (OutOfMemoryError); don't catch
└── Exception
    ├── IOException, ...       checked: must be handled or declared
    └── RuntimeException       unchecked: usually programming bugs
        ├── NullPointerException
        ├── IllegalArgumentException
        ├── IndexOutOfBoundsException
        └── ArithmeticException
```

### Checked vs unchecked

- **Unchecked** exceptions (`RuntimeException` and its subclasses) usually mean a bug: a null reference, a bad index. You don't have to declare them.
- **Checked** exceptions (other `Exception`s, like `IOException`) represent problems outside your control, such as a missing file. The compiler forces you to either **catch** them or **declare** them with `throws`:

```java
import java.io.IOException;

public class Main {
    static String readConfig(boolean exists) throws IOException {
        if (!exists) {
            throw new IOException("config.txt not found");
        }
        return "theme=dark";
    }

    public static void main(String[] args) {
        try {
            System.out.println(readConfig(true));
            System.out.println(readConfig(false));
        } catch (IOException e) {
            System.out.println("Using defaults because: " + e.getMessage());
        }
    }
}
```

### Throwing your own

`throw` raises an exception. Use it to reject invalid input early, with a clear message:

```java
public class Main {
    static double sqrt(double x) {
        if (x < 0) {
            throw new IllegalArgumentException("Can't take the square root of " + x);
        }
        return Math.sqrt(x);
    }

    public static void main(String[] args) {
        System.out.println(sqrt(16));
        try {
            sqrt(-4);
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
```

### Custom exceptions

For your own application errors, extend `Exception` (checked) or `RuntimeException` (unchecked):

```java
class InsufficientFundsException extends Exception {
    private final double shortfall;

    InsufficientFundsException(double shortfall) {
        super("Need " + shortfall + " more");
        this.shortfall = shortfall;
    }

    double getShortfall() {
        return shortfall;
    }
}

public class Main {
    static double withdraw(double balance, double amount) throws InsufficientFundsException {
        if (amount > balance) {
            throw new InsufficientFundsException(amount - balance);
        }
        return balance - amount;
    }

    public static void main(String[] args) {
        try {
            System.out.println(withdraw(100, 30));
            System.out.println(withdraw(100, 130));
        } catch (InsufficientFundsException e) {
            System.out.println("Declined: " + e.getMessage() + " (short by " + e.getShortfall() + ")");
        }
    }
}
```

### try-with-resources

Resources like files and network connections must be closed. A **try-with-resources** block closes them automatically, even if an exception happens. Anything that implements `AutoCloseable` works:

```java
class Connection implements AutoCloseable {
    Connection() { System.out.println("open"); }
    void send(String msg) { System.out.println("send " + msg); }
    @Override public void close() { System.out.println("close"); }
}

public class Main {
    public static void main(String[] args) {
        try (Connection c = new Connection()) {
            c.send("hello");
            throw new IllegalStateException("network hiccup");
        } catch (IllegalStateException e) {
            System.out.println("caught: " + e.getMessage());
        }
    }
}
```

"close" prints before "caught": the resource is closed first, then the exception is handled.

:::exercise Safe parse
Write `static int parseOrDefault(String text, int fallback)` that returns the parsed integer, or `fallback` if `text` isn't a valid whole number (including `null`). Use try/catch, not string checks.
```java starter
public class Main {
    static int parseOrDefault(String text, int fallback) {
        return Integer.parseInt(text);
    }

    public static void main(String[] args) {
        System.out.println(parseOrDefault("42", 0) + " " + parseOrDefault("x", -1));
    }
}
```
```java check
eq(42, call("parseOrDefault", "42", 0), "parseOrDefault(\"42\", 0)");
eq(-7, call("parseOrDefault", "-7", 0), "parseOrDefault(\"-7\", 0)");
eq(-1, call("parseOrDefault", "abc", -1), "parseOrDefault(\"abc\", -1)");
eq(5, call("parseOrDefault", "4.5", 5), "parseOrDefault(\"4.5\", 5)");
eq(9, call("parseOrDefault", null, 9), "parseOrDefault(null, 9)");
sourceHas("catch", "Use try/catch.");
```
```java solution
public class Main {
    static int parseOrDefault(String text, int fallback) {
        try {
            return Integer.parseInt(text);
        } catch (NumberFormatException e) {
            return fallback;
        }
    }

    public static void main(String[] args) {
        System.out.println(parseOrDefault("42", 0) + " " + parseOrDefault("x", -1));
    }
}
```
hint: Wrap the parseInt call in try { ... } catch (NumberFormatException e) { return fallback; }. Integer.parseInt(null) also throws NumberFormatException.
:::

:::exercise Validated quantity
Write `static int validateQuantity(int qty)` that returns `qty` if it's between 1 and 100, and otherwise throws an `IllegalArgumentException` whose message contains the bad value.
```java starter
public class Main {
    static int validateQuantity(int qty) {
        return qty;
    }

    public static void main(String[] args) {
        System.out.println(validateQuantity(5));
    }
}
```
```java check
eq(1, call("validateQuantity", 1), "validateQuantity(1)");
eq(100, call("validateQuantity", 100), "validateQuantity(100)");
for (int bad : new int[]{0, 101, -3}) {
    Throwable t = expectThrows("IllegalArgumentException", () -> call("validateQuantity", bad), "validateQuantity(" + bad + ")");
    check(t.getMessage() != null && t.getMessage().contains(String.valueOf(bad)), "The exception message should mention the bad value " + bad);
}
```
```java solution
public class Main {
    static int validateQuantity(int qty) {
        if (qty < 1 || qty > 100) {
            throw new IllegalArgumentException("Quantity must be 1 to 100, got " + qty);
        }
        return qty;
    }

    public static void main(String[] args) {
        System.out.println(validateQuantity(5));
    }
}
```
hint: if (qty < 1 || qty > 100) throw new IllegalArgumentException("... " + qty);
:::

:::quiz
? Which must be caught or declared with `throws`?
+ Checked exceptions like IOException
- RuntimeExceptions like NullPointerException
- Errors like OutOfMemoryError
= The compiler enforces handling only for checked exceptions.

? When does a `finally` block run?
+ Always, whether or not an exception occurred
- Only after an exception
- Only if there's no exception
= It's for cleanup that must always happen.

? What does try-with-resources do?
+ Closes the resource automatically at the end of the block
- Retries the code if it fails
- Hides all exceptions
= Anything AutoCloseable declared in `try (...)` is closed for you.
:::

@@@ lesson
id: generics
title: Generics
minutes: 12
summary: Write classes and methods that work with any type, safely, using type parameters.
---
**Generics** let you write code that works with many types while the compiler still checks them. You've used them already: `ArrayList<String>` is a list that only holds Strings.

### Why generics?

Without generics, a container would hold plain `Object`s, and you'd need casts that can fail at runtime. With generics, mistakes become compile errors:

```java error
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();
        names.add("Ada");
        names.add(42);          // compile error: not a String
    }
}
```

### A generic class

A **type parameter** like `<T>` is a placeholder for a real type, filled in when you use the class:

```java
class Box<T> {
    private T value;

    Box(T value) {
        this.value = value;
    }

    T get() {
        return value;
    }

    boolean isEmpty() {
        return value == null;
    }
}

class Pair<A, B> {
    final A first;
    final B second;

    Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public String toString() {
        return "(" + first + ", " + second + ")";
    }
}

public class Main {
    public static void main(String[] args) {
        Box<String> name = new Box<>("Ada");
        Box<Integer> age = new Box<>(36);
        String n = name.get();          // no cast needed
        int a = age.get();
        System.out.println(n + " " + a);
        System.out.println(new Pair<>("Ada", 1815));
    }
}
```

`new Box<>(...)` uses the **diamond** `<>`: the compiler infers the type from the variable.

### Generic methods

A method can declare its own type parameter before the return type:

```java
import java.util.List;

public class Main {
    static <T> T firstOrDefault(List<T> items, T fallback) {
        return items.isEmpty() ? fallback : items.get(0);
    }

    static <T extends Comparable<T>> T largest(List<T> items) {
        T best = items.get(0);
        for (T item : items) {
            if (item.compareTo(best) > 0) {
                best = item;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(firstOrDefault(List.of("x", "y"), "none"));
        System.out.println(firstOrDefault(List.<String>of(), "none"));
        System.out.println(largest(List.of(3, 9, 4)));
        System.out.println(largest(List.of("pear", "apple", "zucchini")));
    }
}
```

`<T extends Comparable<T>>` is a **bounded type parameter**: T can be any type that can compare itself to another T, which is what `compareTo` needs.

### Wildcards

`List<?>` means "a list of some type". `List<? extends Number>` accepts a `List<Integer>` or a `List<Double>`, which a plain `List<Number>` parameter wouldn't:

```java
import java.util.List;

public class Main {
    static double sum(List<? extends Number> nums) {
        double total = 0;
        for (Number n : nums) {
            total += n.doubleValue();
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(sum(List.of(1, 2, 3)));
        System.out.println(sum(List.of(1.5, 2.5)));
    }
}
```

Type parameter names are single capital letters by convention: `T` (type), `E` (element), `K`/`V` (key/value), `R` (result).

:::exercise Generic stack
Create a generic class `Stack<T>` backed by an `ArrayList<T>`, with `void push(T item)`, `T pop()` (removes and returns the top item; throw `IllegalStateException` if empty), `T peek()`, `boolean isEmpty()` and `int size()`.
```java starter
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        // Stack<String> s = new Stack<>();
        // s.push("a"); s.push("b");
        // System.out.println(s.pop());
    }
}
```
```java check
Object s = make("Stack");
eq(true, callOn(s, "isEmpty"), "isEmpty() on a new stack");
callOn(s, "push", "a");
callOn(s, "push", "b");
callOn(s, "push", "c");
eq(3, callOn(s, "size"), "size() after 3 pushes");
eq("c", callOn(s, "peek"), "peek()");
eq("c", callOn(s, "pop"), "first pop()");
eq("b", callOn(s, "pop"), "second pop()");
eq(1, callOn(s, "size"), "size() after 2 pops");
callOn(s, "pop");
expectThrows("IllegalStateException", () -> callOn(s, "pop"), "pop() on an empty stack");
check(cls("Stack").getTypeParameters().length == 1, "Stack should be generic: class Stack<T>");
```
```java solution
import java.util.ArrayList;

class Stack<T> {
    private final ArrayList<T> items = new ArrayList<>();

    void push(T item) {
        items.add(item);
    }

    T pop() {
        if (items.isEmpty()) {
            throw new IllegalStateException("Stack is empty");
        }
        return items.remove(items.size() - 1);
    }

    T peek() {
        if (items.isEmpty()) {
            throw new IllegalStateException("Stack is empty");
        }
        return items.get(items.size() - 1);
    }

    boolean isEmpty() {
        return items.isEmpty();
    }

    int size() {
        return items.size();
    }
}

public class Main {
    public static void main(String[] args) {
        Stack<String> s = new Stack<>();
        s.push("a");
        s.push("b");
        System.out.println(s.pop());
    }
}
```
hint: class Stack<T> { private final ArrayList<T> items = new ArrayList<>(); ... } The top of the stack is the last element: items.get(items.size() - 1).
:::

:::quiz
? What does `<T>` in `class Box<T>` declare?
+ A type parameter, filled in when Box is used
- A field named T
- An interface
= `Box<String>` replaces T with String.

? What is `new ArrayList<>()` called?
+ The diamond operator; the type is inferred
- A raw type
- A wildcard
= The compiler infers the element type from the variable.

? Why does `List<? extends Number>` accept a `List<Integer>`?
+ The wildcard allows any subtype of Number
- Integer and Number are the same
- It doesn't
= `List<Integer>` isn't a `List<Number>`, but it fits `List<? extends Number>`.
:::

@@@ lesson
id: lists
title: Lists
minutes: 15
summary: Use ArrayList and List.of, add, get, remove and search, iterate safely, and choose between ArrayList and LinkedList.
---
A **List** is an ordered collection that can grow and shrink. `List` is an interface; `ArrayList` is the implementation you'll use most.

```java
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> tasks = new ArrayList<>();
        tasks.add("email");
        tasks.add("code review");
        tasks.add(0, "coffee");                  // insert at a position
        System.out.println(tasks);
        System.out.println(tasks.size() + " tasks, first is " + tasks.get(0));

        tasks.set(1, "reply to email");          // replace
        tasks.remove("code review");             // remove by value
        String done = tasks.remove(0);           // remove by index, returns it
        System.out.println("Done: " + done + ", left: " + tasks);
        System.out.println(tasks.contains("reply to email") + " " + tasks.indexOf("lunch"));
    }
}
```

Declaring the variable as `List<String>` (the interface) rather than `ArrayList<String>` is good practice: the code then works with any kind of list.

### Common methods

| Method | What it does |
|---|---|
| `add(x)` / `add(i, x)` | append / insert |
| `get(i)` / `set(i, x)` | read / replace |
| `remove(i)` / `remove(x)` | by index / by value |
| `size()`, `isEmpty()` | count, empty? |
| `contains(x)`, `indexOf(x)` | search (uses `equals`) |
| `clear()` | remove everything |
| `addAll(other)` | append another collection |

### Creating lists quickly

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> fixed = List.of(3, 1, 2);          // immutable
        List<Integer> nums = new ArrayList<>(fixed);      // a modifiable copy
        Collections.sort(nums);
        System.out.println(nums);
        Collections.reverse(nums);
        System.out.println(nums + " max=" + Collections.max(nums));
        List<String> fromArray = new ArrayList<>(Arrays.asList("b", "a"));
        fromArray.sort(null);                             // natural order
        System.out.println(fromArray);
    }
}
```

`List.of(...)` creates an **unmodifiable** list. Calling `add` on it throws `UnsupportedOperationException`. Wrap it in `new ArrayList<>(...)` when you need to change it.

### The remove(int) trap with Integer lists

For a `List<Integer>`, `remove(1)` removes **index** 1, not the value 1. Use `remove(Integer.valueOf(1))` for the value:

```java
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> nums = new ArrayList<>(List.of(10, 1, 20, 1));
        nums.remove(1);                       // removes the element at index 1
        System.out.println(nums);
        nums.remove(Integer.valueOf(1));      // removes the value 1
        System.out.println(nums);
    }
}
```

### Removing while iterating

Changing a list while a for-each loop walks over it throws `ConcurrentModificationException`. Use `removeIf`, or an explicit `Iterator`:

```java
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> nums = new ArrayList<>(List.of(1, 2, 3, 4, 5, 6));
        nums.removeIf(n -> n % 2 == 0);       // a lambda; Part 6 explains them
        System.out.println(nums);

        Iterator<Integer> it = nums.iterator();
        while (it.hasNext()) {
            if (it.next() > 3) {
                it.remove();
            }
        }
        System.out.println(nums);
    }
}
```

### ArrayList or LinkedList?

`ArrayList` stores elements in an array: `get(i)` is instant, but inserting at the front shifts everything. `LinkedList` links nodes: adding and removing at the ends is fast, but `get(i)` walks the chain. In practice `ArrayList` is the right choice almost every time; for a queue, use `ArrayDeque`.

:::exercise Shopping list
Write `static List<String> shoppingList()` that builds and returns a **modifiable** list by: adding `"bread"` and `"milk"`, inserting `"coffee"` at the front, adding `"eggs"`, removing `"milk"`, and finally sorting it alphabetically. The result is `[bread, coffee, eggs]`.
```java starter
import java.util.*;

public class Main {
    static List<String> shoppingList() {
        List<String> cart = new ArrayList<>();
        return cart;
    }

    public static void main(String[] args) {
        System.out.println(shoppingList());
    }
}
```
```java check
List<?> cart = (List<?>) call("shoppingList");
eq(List.of("bread", "coffee", "eggs"), cart, "shoppingList()");
sourceHas(".remove(", "Remove milk with remove().");
```
```java solution
import java.util.*;

public class Main {
    static List<String> shoppingList() {
        List<String> cart = new ArrayList<>();
        cart.add("bread");
        cart.add("milk");
        cart.add(0, "coffee");
        cart.add("eggs");
        cart.remove("milk");
        Collections.sort(cart);
        return cart;
    }

    public static void main(String[] args) {
        System.out.println(shoppingList());
    }
}
```
hint: cart.add("bread"); cart.add("milk"); cart.add(0, "coffee"); cart.add("eggs"); cart.remove("milk"); Collections.sort(cart);
:::

:::exercise Remove duplicates, keep order
Write `static List<Integer> unique(List<Integer> nums)` returning a **new** list with duplicates removed, keeping the first occurrence order. `unique([3, 1, 3, 2, 1])` → `[3, 1, 2]`.
```java starter
import java.util.*;

public class Main {
    static List<Integer> unique(List<Integer> nums) {
        return nums;
    }

    public static void main(String[] args) {
        System.out.println(unique(List.of(3, 1, 3, 2, 1)));
    }
}
```
```java check
eq(List.of(3, 1, 2), call("unique", List.of(3, 1, 3, 2, 1)), "unique([3, 1, 3, 2, 1])");
eq(List.of(), call("unique", List.of()), "unique([])");
eq(List.of(1000, 7), call("unique", List.of(1000, 1000, 7, 1000)), "unique([1000, 1000, 7, 1000])");
List<Integer> input = new ArrayList<>(List.of(1, 1));
call("unique", input);
eq(List.of(1, 1), input, "The input list after calling unique (it shouldn't change)");
```
```java solution
import java.util.*;

public class Main {
    static List<Integer> unique(List<Integer> nums) {
        List<Integer> result = new ArrayList<>();
        for (Integer n : nums) {
            if (!result.contains(n)) {
                result.add(n);
            }
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(unique(List.of(3, 1, 3, 2, 1)));
    }
}
```
hint: Build a new ArrayList. Loop over nums and add each number only if result doesn't already contain it. (A LinkedHashSet, from the next lesson, does this in one line.)
:::

:::quiz
? What does `List.of(1, 2).add(3)` do?
+ Throws UnsupportedOperationException
- Returns [1, 2, 3]
- Doesn't compile
= `List.of` lists are unmodifiable.

? For `List<Integer> list = [10, 20, 30]`, what does `list.remove(1)` remove?
+ 20 (the element at index 1)
- The value 1
- 10
= An int argument chooses `remove(int index)`. Use `remove(Integer.valueOf(1))` for the value.

? What happens if you remove from a list inside a for-each loop over it?
+ ConcurrentModificationException
- It works fine
- Elements are skipped silently, always
= Use `removeIf` or an `Iterator`'s `remove` instead.
:::

@@@ lesson
id: sets-and-maps
title: Sets and maps
minutes: 15
summary: Keep unique values in sets, look things up by key in maps, count with merge and getOrDefault, and know why equals and hashCode matter.
---
### Sets

A **Set** holds unique values: adding a duplicate does nothing. Membership tests (`contains`) are very fast.

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Set<String> tags = new HashSet<>();
        tags.add("java");
        tags.add("code");
        System.out.println(tags.add("java"));           // false: already there
        System.out.println(tags.size() + " " + tags.contains("code"));

        Set<String> ordered = new LinkedHashSet<>(List.of("pear", "apple", "pear", "fig"));
        System.out.println(ordered);                     // insertion order, no duplicates

        Set<Integer> sorted = new TreeSet<>(List.of(5, 1, 4, 1));
        System.out.println(sorted);                      // sorted order
    }
}
```

| Implementation | Order |
|---|---|
| `HashSet` | no particular order (fastest) |
| `LinkedHashSet` | insertion order |
| `TreeSet` | sorted order |

Set operations use `addAll` (union), `retainAll` (intersection) and `removeAll` (difference), which change the set they're called on, so work on a copy:

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Set<String> javaDevs = Set.of("Ana", "Ben", "Cy");
        Set<String> pythonDevs = Set.of("Ben", "Dee");

        Set<String> both = new TreeSet<>(javaDevs);
        both.retainAll(pythonDevs);
        Set<String> either = new TreeSet<>(javaDevs);
        either.addAll(pythonDevs);
        Set<String> javaOnly = new TreeSet<>(javaDevs);
        javaOnly.removeAll(pythonDevs);
        System.out.println(both + " " + either + " " + javaOnly);
    }
}
```

### Maps

A **Map** stores **key → value** pairs. Keys are unique; looking up a value by key is fast.

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, Integer> stock = new HashMap<>();
        stock.put("apples", 10);
        stock.put("pears", 4);
        stock.put("apples", 7);                          // replaces the old value
        System.out.println(stock.get("apples"));
        System.out.println(stock.get("kiwis"));          // null: missing key
        System.out.println(stock.getOrDefault("kiwis", 0));
        System.out.println(stock.containsKey("pears"));
        stock.remove("pears");
        System.out.println(stock);
    }
}
```

`HashMap` has no order, `LinkedHashMap` keeps insertion order, and `TreeMap` keeps keys sorted.

### Looping over a map

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, Integer> scores = new TreeMap<>(Map.of("Cy", 85, "Ana", 91, "Ben", 78));
        for (Map.Entry<String, Integer> e : scores.entrySet()) {
            System.out.println(e.getKey() + ": " + e.getValue());
        }
        System.out.println(scores.keySet() + " " + scores.values());
    }
}
```

### Counting with a map

Counting things is the classic map job. `merge` adds to an existing count or starts a new one:

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        String text = "the cat and the hat and the bat";
        Map<String, Integer> counts = new TreeMap<>();
        for (String word : text.split(" ")) {
            counts.merge(word, 1, Integer::sum);         // same as: put(word, getOrDefault(word, 0) + 1)
        }
        System.out.println(counts);

        Map<Character, List<String>> byLetter = new TreeMap<>();
        for (String word : List.of("apple", "avocado", "banana", "blueberry")) {
            byLetter.computeIfAbsent(word.charAt(0), k -> new ArrayList<>()).add(word);
        }
        System.out.println(byLetter);
    }
}
```

`Integer::sum` is a **method reference**, covered with lambdas in Part 6.

### equals and hashCode

Hash-based collections (`HashSet`, `HashMap`) use `hashCode()` to find the right bucket and `equals()` to compare. If you put your own objects in them, you must override **both**, consistently, or duplicates and lookups go wrong. Records do this for you, which is one more reason to use them for data:

```java
import java.util.*;

record Point(int x, int y) { }

class OldPoint {
    final int x, y;
    OldPoint(int x, int y) { this.x = x; this.y = y; }
}

public class Main {
    public static void main(String[] args) {
        Set<Point> points = new HashSet<>(List.of(new Point(1, 2), new Point(1, 2)));
        System.out.println(points.size());               // 1: records compare by value

        Set<OldPoint> old = new HashSet<>(List.of(new OldPoint(1, 2), new OldPoint(1, 2)));
        System.out.println(old.size());                  // 2: no equals/hashCode
    }
}
```

:::exercise Word frequency
Write `static Map<String, Integer> wordCounts(String text)` that counts each **lowercased** word, splitting on whitespace with `text.trim().split("\\s+")`. Return an empty map for blank text.
```java starter
import java.util.*;

public class Main {
    static Map<String, Integer> wordCounts(String text) {
        return new HashMap<>();
    }

    public static void main(String[] args) {
        System.out.println(wordCounts("The cat saw the dog"));
    }
}
```
```java check
Map<?, ?> m = (Map<?, ?>) call("wordCounts", "The cat saw the dog");
eq(Map.of("the", 2, "cat", 1, "saw", 1, "dog", 1), m, "wordCounts(\"The cat saw the dog\")");
eq(Map.of("a", 3, "b", 1), call("wordCounts", "  a A   a b "), "wordCounts(\"  a A   a b \")");
eq(Map.of(), call("wordCounts", "   "), "wordCounts(\"   \")");
```
```java solution
import java.util.*;

public class Main {
    static Map<String, Integer> wordCounts(String text) {
        Map<String, Integer> counts = new HashMap<>();
        if (text.isBlank()) {
            return counts;
        }
        for (String word : text.trim().split("\\s+")) {
            counts.merge(word.toLowerCase(), 1, Integer::sum);
        }
        return counts;
    }

    public static void main(String[] args) {
        System.out.println(wordCounts("The cat saw the dog"));
    }
}
```
hint: Return early for blank text. Then loop over text.trim().split("\\s+") and use counts.merge(word.toLowerCase(), 1, Integer::sum).
:::

:::exercise Common friends
Write `static Set<String> common(List<String> a, List<String> b)` returning a **sorted** set (`TreeSet`) of names that appear in both lists.
```java starter
import java.util.*;

public class Main {
    static Set<String> common(List<String> a, List<String> b) {
        return new TreeSet<>();
    }

    public static void main(String[] args) {
        System.out.println(common(List.of("Cy", "Ana", "Ben"), List.of("Ben", "Dee", "Ana")));
    }
}
```
```java check
Object r = call("common", List.of("Cy", "Ana", "Ben", "Ana"), List.of("Ben", "Dee", "Ana"));
check(r instanceof TreeSet, "Return a TreeSet so the names are sorted.");
eq(List.of("Ana", "Ben"), new ArrayList<>((Set<?>) r), "common(...)");
eq(List.of(), new ArrayList<>((Set<?>) call("common", List.of("a"), List.of("b"))), "common with no overlap");
```
```java solution
import java.util.*;

public class Main {
    static Set<String> common(List<String> a, List<String> b) {
        Set<String> result = new TreeSet<>(a);
        result.retainAll(new HashSet<>(b));
        return result;
    }

    public static void main(String[] args) {
        System.out.println(common(List.of("Cy", "Ana", "Ben"), List.of("Ben", "Dee", "Ana")));
    }
}
```
hint: Start with new TreeSet<>(a), then call retainAll with b.
:::

:::quiz
? What does `set.add(x)` return if x is already in the set?
+ false
- true
- It throws an exception
= Sets ignore duplicates; `add` reports whether anything changed.

? Which map keeps its keys sorted?
- HashMap
- LinkedHashMap
+ TreeMap
= TreeMap is a sorted map.

? What must you override to use your own class as a HashMap key?
+ Both equals and hashCode
- Only equals
- Only toString
= Hash collections use hashCode to locate and equals to compare. Records do both for you.
:::

@@@ lesson
id: sorting-and-comparators
title: Sorting with Comparable and Comparator
minutes: 12
summary: Give classes a natural order with Comparable, and sort any way you like with Comparator.
---
Sorting numbers and strings just works because those classes know how to compare themselves. For your own classes you decide the order.

### Comparable: a natural order

Implement `Comparable<T>` and its `compareTo` method, which returns a **negative** number if this object comes first, **zero** if equal, and **positive** if it comes after:

```java
import java.util.*;

class Version implements Comparable<Version> {
    final int major, minor;

    Version(int major, int minor) {
        this.major = major;
        this.minor = minor;
    }

    @Override
    public int compareTo(Version other) {
        if (major != other.major) {
            return Integer.compare(major, other.major);
        }
        return Integer.compare(minor, other.minor);
    }

    @Override
    public String toString() {
        return major + "." + minor;
    }
}

public class Main {
    public static void main(String[] args) {
        List<Version> versions = new ArrayList<>(List.of(new Version(1, 10), new Version(1, 2), new Version(0, 9)));
        Collections.sort(versions);
        System.out.println(versions);
        System.out.println(Collections.max(versions));
    }
}
```

Use `Integer.compare(a, b)` rather than `a - b`; subtraction can overflow for large values.

### Comparator: any order you want

A `Comparator` is a separate object that compares two values. The `Comparator.comparing` factory methods build them from **key extractors** (lambdas and method references, covered fully in Part 6):

```java
import java.util.*;

record Person(String name, int age, String city) { }

public class Main {
    public static void main(String[] args) {
        List<Person> people = new ArrayList<>(List.of(
            new Person("Cy", 35, "Lima"),
            new Person("Ana", 31, "Oslo"),
            new Person("Ben", 31, "Lima")
        ));

        people.sort(Comparator.comparing(Person::name));
        System.out.println(people.stream().map(Person::name).toList());

        people.sort(Comparator.comparingInt(Person::age).thenComparing(Person::name));
        System.out.println(people.stream().map(Person::name).toList());

        people.sort(Comparator.comparing(Person::city).reversed());
        System.out.println(people.stream().map(Person::city).toList());

        List<String> words = new ArrayList<>(List.of("banana", "Kiwi", "apple", "fig"));
        words.sort(String.CASE_INSENSITIVE_ORDER);
        System.out.println(words);
        words.sort(Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder()));
        System.out.println(words);
    }
}
```

| Building block | Meaning |
|---|---|
| `Comparator.comparing(f)` | order by the key `f` returns |
| `comparingInt(f)` | the same for int keys, without boxing |
| `.thenComparing(g)` | tie-breaker |
| `.reversed()` | flip the order |
| `Comparator.naturalOrder()` | use `compareTo` |

### Sorting is stable

Java's object sorts are **stable**: elements that compare equal keep their original relative order. That's why sorting by a tie-breaker first and the main key second also works, though `thenComparing` states the intent more clearly.

:::exercise Leaderboard
Write `static List<String> leaderboard(List<Score> scores)` where `Score` is the record given. Return the names ordered by points **highest first**, breaking ties alphabetically by name.
```java starter
import java.util.*;

record Score(String name, int points) { }

public class Main {
    static List<String> leaderboard(List<Score> scores) {
        List<String> names = new ArrayList<>();
        for (Score s : scores) {
            names.add(s.name());
        }
        return names;
    }

    public static void main(String[] args) {
        System.out.println(leaderboard(List.of(new Score("Cy", 50), new Score("Ana", 70), new Score("Ben", 50))));
    }
}
```
```java check
List<Object> in = new ArrayList<>();
in.add(make("Score", "Cy", 50));
in.add(make("Score", "Ana", 70));
in.add(make("Score", "Ben", 50));
eq(List.of("Ana", "Ben", "Cy"), call("leaderboard", in), "leaderboard(Cy 50, Ana 70, Ben 50)");
List<Object> in2 = new ArrayList<>();
for (Object[] row : new Object[][]{{"Zed", 10}, {"Amy", 10}, {"Max", 99}, {"Bo", 1}}) in2.add(make("Score", row[0], row[1]));
eq(List.of("Max", "Amy", "Zed", "Bo"), call("leaderboard", in2), "leaderboard(Zed 10, Amy 10, Max 99, Bo 1)");
```
```java solution
import java.util.*;

record Score(String name, int points) { }

public class Main {
    static List<String> leaderboard(List<Score> scores) {
        List<Score> sorted = new ArrayList<>(scores);
        sorted.sort(Comparator.comparingInt(Score::points).reversed().thenComparing(Score::name));
        List<String> names = new ArrayList<>();
        for (Score s : sorted) {
            names.add(s.name());
        }
        return names;
    }

    public static void main(String[] args) {
        System.out.println(leaderboard(List.of(new Score("Cy", 50), new Score("Ana", 70), new Score("Ben", 50))));
    }
}
```
hint: Copy the list, then sort with Comparator.comparingInt(Score::points).reversed().thenComparing(Score::name). Copying matters because List.of(...) can't be sorted in place.
:::

:::quiz
? What should `a.compareTo(b)` return when a comes before b?
+ A negative number
- A positive number
- Zero
= Negative: a first. Zero: equal. Positive: b first.

? How do you sort people by age, then by name for equal ages?
+ `Comparator.comparingInt(Person::age).thenComparing(Person::name)`
- `Comparator.comparing(Person::name).thenComparing(Person::age)`
- Sort twice by age
= `thenComparing` adds a tie-breaker.

? Why use `Integer.compare(a, b)` instead of `a - b` in compareTo?
+ Subtraction can overflow for large values
- It's required by the interface
- `a - b` doesn't compile
= With large positive and negative ints, `a - b` can wrap around and flip the sign.
:::
