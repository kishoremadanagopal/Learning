# Java syntax cheat sheet

Everything from the course on one page. The number in brackets is the lesson where it's taught.

## Program structure

```java
import java.util.*;                       // bring in library classes           [6]

public class Main {                       // public class name = file name      [1]
    public static void main(String[] args) {
        System.out.println("Hello");      // print a line                       [2]
        System.out.print("no newline");   //                                    [2]
        System.out.printf("%s is %d%n", "Ada", 36);   // formatted              [5]
    }
}
// comment      /* block */      /** Javadoc */                                 [2]
```

## Types and variables

| Type | Example | Notes |
|---|---|---|
| `int` | `42`, `1_000_000` | whole numbers, about ±2.1 billion [3] |
| `long` | `9_000_000_000L` | bigger whole numbers [3] |
| `double` | `3.14` | decimals (approximate) [3] |
| `boolean` | `true`, `false` | [3] |
| `char` | `'A'` | one character, single quotes [3] |
| `String` | `"text"`, `"""text block"""` | a class; immutable [3, 34] |

```java
int count = 3;  final double TAX = 0.08;  var name = "Ada";        // [3]
double avg = (double) total / n;          // cast before dividing      [4]
int whole = (int) 3.99;                   // 3 (truncates)             [4]
long big = (long) Integer.MAX_VALUE + 1;  // avoid overflow            [4]
```

## Operators

| Operator | Meaning |
|---|---|
| `+ - * / %` | arithmetic; `7 / 2` is `3`, `7 % 2` is `1` [4] |
| `+= -= *= ++ --` | update in place [4] |
| `== != < > <= >=` | compare primitives [7] |
| `&& \|\| !` | and, or, not (short-circuit) [7] |
| `cond ? a : b` | choose a value [7] |

## Strings [5]

```java
s.length()  s.charAt(0)  s.substring(1, 3)  s.indexOf("x")  s.contains("x")
s.toUpperCase()  s.strip()  s.replace("a", "b")  s.split(",")  s.repeat(3)
s.equals(t)  s.equalsIgnoreCase(t)  s.compareTo(t)  s.isBlank()
String.join("-", parts)  String.valueOf(42)  String.format("%.2f", x)
Integer.parseInt("42")  Double.parseDouble("2.5")                         // [6]
new StringBuilder().append("a").append(1).reverse().toString()          // [25]
```

Always compare strings with `equals`, never `==`.

## Input [6]

```java
Scanner in = new Scanner(System.in);
String line = in.nextLine();
int n = Integer.parseInt(in.nextLine());   // safer than nextInt() + nextLine()
```

## Decisions

```java
if (x > 0) { ... } else if (x < 0) { ... } else { ... }                  // [7]

String type = switch (day) {                                              // [8]
    case "SAT", "SUN" -> "weekend";
    default -> "weekday";
};
```

## Loops

```java
while (cond) { ... }                       do { ... } while (cond);       // [9]
for (int i = 0; i < n; i++) { ... }                                       // [10]
for (String s : list) { ... }              // enhanced for                 [10]
break;  continue;  outer: for (...) { ... break outer; }                  // [11]
```

## Arrays [12, 13]

```java
int[] a = {3, 1, 2};    int[] b = new int[5];    a.length
int[][] grid = new int[3][4];    grid[row][col]
Arrays.toString(a)  Arrays.sort(a)  Arrays.fill(b, 7)  Arrays.copyOf(a, n)
Arrays.equals(a, b)  Arrays.deepToString(grid)  a.clone()
```

## Methods [14–16]

```java
static int add(int a, int b) { return a + b; }           // static method
static double add(double a, double b) { ... }            // overload
static int sum(int... nums) { ... }                      // varargs
static long factorial(int n) { return n <= 1 ? 1 : n * factorial(n - 1); }   // recursion
```

## Classes [17–20]

```java
class Account {
    private static int created = 0;          // shared by all objects   [20]
    private final String owner;              // per object               [19]
    private double balance;

    Account(String owner) {                  // constructor              [18]
        this(owner, 0);                      // chain to another one
    }
    Account(String owner, double balance) {
        this.owner = owner;
        this.balance = balance;
        created++;
    }
    public double getBalance() { return balance; }        // getter     [19]
    @Override public String toString() { return owner + ": " + balance; }   // [17]
}
Account a = new Account("Ana");                          // [17]
```

## Inheritance and interfaces [21–23]

```java
class Dog extends Animal {
    Dog(String name) { super(name); }
    @Override String speak() { return "Woof"; }
}
abstract class Shape { abstract double area(); }
interface Payable { double amountDue(); default String note() { return ""; } }
class Invoice implements Payable, Comparable<Invoice> { ... }
if (animal instanceof Dog d) { d.fetch(); }               // pattern matching   [22]
```

## Enums and records [24]

```java
enum Size { SMALL, MEDIUM, LARGE }        Size.values()   Size.valueOf("SMALL")
record Point(int x, int y) {
    Point { if (x < 0) throw new IllegalArgumentException(); }     // compact constructor
}
p.x()   // accessor
```

## Exceptions [26]

```java
try {
    risky();
} catch (NumberFormatException | ArithmeticException e) {
    System.out.println(e.getMessage());
} finally {
    cleanUp();
}
throw new IllegalArgumentException("bad value: " + x);
void load() throws IOException { ... }                    // checked: declare or catch
try (BufferedReader r = Files.newBufferedReader(path)) { ... }   // closes automatically
class MyException extends Exception { MyException(String m) { super(m); } }
```

## Generics [27]

```java
class Box<T> { private T value; T get() { return value; } }
static <T extends Comparable<T>> T max(List<T> items) { ... }
double sum(List<? extends Number> nums) { ... }
```

## Collections [28–30]

```java
List<String> list = new ArrayList<>();  list.add(x); list.get(0); list.remove(x);
List.of(1, 2, 3)                          // unmodifiable
Set<String> set = new HashSet<>();        // TreeSet = sorted, LinkedHashSet = insertion order
Map<String, Integer> map = new HashMap<>();
map.put(k, v);  map.get(k);  map.getOrDefault(k, 0);  map.merge(k, 1, Integer::sum);
for (Map.Entry<String, Integer> e : map.entrySet()) { e.getKey(); e.getValue(); }
list.sort(Comparator.comparing(Person::age).thenComparing(Person::name).reversed());
Collections.sort(list);  Collections.max(list);  list.removeIf(x -> x < 0);
```

| Need | Use |
|---|---|
| ordered list | `ArrayList` |
| unique values | `HashSet` (`TreeSet` sorted) |
| key → value lookup | `HashMap` (`TreeMap` sorted) |
| queue / stack | `ArrayDeque` |
| thread-safe map | `ConcurrentHashMap` |

## Lambdas and streams [31–33]

```java
Function<String, Integer> len = s -> s.length();     Predicate<Integer> pos = n -> n > 0;
Supplier<List<String>> make = ArrayList::new;          Consumer<String> show = System.out::println;

list.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .sorted()
    .toList();
nums.stream().mapToInt(Integer::intValue).sum();
words.stream().collect(Collectors.groupingBy(String::length, TreeMap::new, Collectors.toList()));
words.stream().collect(Collectors.joining(", "));
Optional<String> first = list.stream().findFirst();   first.orElse("none");
```

## Files [35]

```java
Files.writeString(Path.of("a.txt"), "text");
String all = Files.readString(Path.of("a.txt"));
List<String> lines = Files.readAllLines(Path.of("a.txt"));
try (Stream<String> s = Files.lines(path)) { ... }
```

## Concurrency [36]

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
Future<Integer> f = pool.submit(() -> compute());   int result = f.get();
pool.shutdown();
AtomicInteger counter = new AtomicInteger();   counter.incrementAndGet();
synchronized void safe() { ... }
CompletableFuture.supplyAsync(() -> load()).thenApply(x -> x * 2).join();
```

## Big-O at a glance [37]

| Operation | ArrayList | HashMap / HashSet | TreeMap / TreeSet |
|---|---|---|---|
| get / lookup | O(1) by index | O(1) | O(log n) |
| contains | O(n) | O(1) | O(log n) |
| add | O(1) at the end | O(1) | O(log n) |
| sort | O(n log n) | n/a | always sorted |
