@@ level
id: basics
title: First Steps
part: 1
lessons: 1–6
---
? Print a line of text, ending with a new line.
```java
System.out.___("Hello, Java!");
```
= println
hint: print adds no new line; its sibling does.

? Declare a whole-number variable.
```java
___ age = 30;
```
= int || var
hint: The primitive type for whole numbers.

? Declare a text variable.
```java
___ name = "Ada";
```
= String || var
hint: Text is an object type, so it starts with a capital letter.

? Store the letter A as a single character.
```java
char grade = ___;
```
= 'A'
hint: Characters use single quotes.

? Make the division keep its decimals.
```java
int total = 7, count = 2;
double avg = (___) total / count;
```
= double
hint: Cast one side to the decimal type before dividing.

? Test whether n is even.
```java
int n = 4;
boolean even = n ___ 2 == 0;
```
= %
hint: The remainder operator.

? Make TAX a constant that can't be reassigned.
```java
___ double TAX = 0.08;
```
= final
hint: The keyword that locks a variable after its first assignment.

? Get the number of characters in a string.
```java
String word = "Java";
int len = word.___();
```
= length
hint: For strings it's a method with parentheses.

? Compare the text of two strings.
```java
String a = "hi", b = "hi";
boolean same = a.___(b);
```
= equals
hint: Never use == for strings.

? Take the first three characters.
```java
String s = "Python";
String first3 = s.___(0, 3);
```
= substring
hint: (start, end) with end excluded.

? Turn the text "42" into an int.
```java
int n = Integer.___("42");
```
= parseInt
hint: Integer.p...

? Print pi with exactly two decimal places.
```java
System.out.printf("%___%n", Math.PI);
```
= .2f
hint: A dot, the number of decimals, then the letter for floating-point.

@@ level
id: control-flow
title: Control Flow
part: 2
lessons: 7–11
---
? Run the block only when age is at least 18.
```java
int age = 20;
if (age ___ 18) {
    System.out.println("adult");
}
```
= >=
hint: "At least" includes 18 itself.

? Both conditions must be true.
```java
boolean hasTicket = true;
int age = 20;
boolean ok = hasTicket ___ age >= 18;
```
= &&
hint: Logical AND.

? At least one condition must be true.
```java
boolean vip = false, staff = true;
boolean allowed = vip ___ staff;
```
= ||
hint: Logical OR.

? Add a second condition to try when the first fails.
```java
int score = 85;
String grade;
if (score >= 90) {
    grade = "A";
} ___ (score >= 80) {
    grade = "B";
} else {
    grade = "C";
}
```
= else if
hint: Two words.

? Choose between two values in one expression.
```java
int n = 7;
String kind = n % 2 == 0 ___ "even" : "odd";
```
= ?
hint: The ternary operator: condition ? a : b

? Use the modern arrow form in a switch.
```java
String day = "SAT";
String type = switch (day) {
    case "SAT", "SUN" ___ "weekend";
    default -> "weekday";
};
```
= ->
hint: A hyphen and a greater-than sign.

? Return a value from a block in a switch expression.
```java
int size = 2;
double price = switch (size) {
    case 1 -> 2.5;
    default -> {
        double base = 3.0;
        ___ base + 0.5;
    }
};
```
= yield
hint: Not return: the switch-expression keyword.

? Repeat while count is below 5.
```java
int count = 0;
___ (count < 5) {
    count++;
}
```
= while
hint: The loop that checks before each pass.

? Write a loop that runs its body at least once.
```java
int n = 0;
___ {
    n++;
} while (n < 3);
```
= do
hint: do { ... } while (...);

? Complete a for loop that counts 0 to 9.
```java
for (int i = 0; i ___ 10; i++) {
    System.out.println(i);
}
```
= <
hint: Stop before 10.

? Visit every element without an index.
```java
String[] fruits = {"apple", "fig"};
for (String fruit ___ fruits) {
    System.out.println(fruit);
}
```
= :
hint: The enhanced for loop uses a colon.

? Skip the rest of this iteration.
```java
for (int i = 0; i < 10; i++) {
    if (i % 3 == 0) {
        ___;
    }
    System.out.println(i);
}
```
= continue
hint: Not break: keep looping.

@@ level
id: arrays-methods
title: Arrays and Methods
part: 3
lessons: 12–16
---
? Create an int array with room for 5 numbers.
```java
int[] nums = ___ int[5];
```
= new
hint: The keyword that creates objects and arrays.

? Get the size of an array.
```java
int[] a = {3, 1, 2};
int size = a.___;
```
= length
hint: For arrays it's a field: no parentheses.

? Print an array readably.
```java
int[] a = {3, 1, 2};
System.out.println(Arrays.___(a));
```
= toString
hint: Arrays.t...

? Sort an array in place.
```java
int[] a = {3, 1, 2};
Arrays.___(a);
```
= sort
hint: The obvious name.

? Read row 1, column 2 of a grid.
```java
int[][] grid = {{1, 2, 3}, {4, 5, 6}};
int value = grid[1]___;
```
= [2]
hint: A second pair of square brackets.

? Declare a method that returns nothing.
```java
static ___ greet(String name) {
    System.out.println("Hi " + name);
}
```
= void
wrap: member
hint: The "no return value" type.

? Send the result back to the caller.
```java
static int square(int x) {
    ___ x * x;
}
```
= return
wrap: member
hint: The keyword that hands back a value.

? Accept any number of int arguments.
```java
static int sum(int___ nums) {
    int total = 0;
    for (int n : nums) total += n;
    return total;
}
```
= ...
wrap: member
hint: Three dots: varargs.

? Complete the base case of factorial.
```java
static long factorial(int n) {
    if (n <= 1) {
        return ___;
    }
    return n * factorial(n - 1);
}
```
= 1
wrap: member
hint: 0! and 1! are both...

? Let main call this helper without creating an object.
```java
___ int twice(int x) {
    return 2 * x;
}
```
= static
wrap: member
hint: Belongs to the class, not to an object.

? Copy an array instead of sharing it.
```java
int[] a = {1, 2, 3};
int[] b = a.___();
```
= clone
hint: Arrays have a method that makes a copy.

@@ level
id: objects
title: Classes and Objects
part: 4
lessons: 17–20
---
? Create a new Dog object.
```java
class Dog {
    String name;
}

class Kennel {
    Dog adopt() {
        Dog d = ___ Dog();
        return d;
    }
}
```
= new
wrap: file
hint: The keyword that builds objects.

? Store the parameter in the field with the same name.
```java
class Dog {
    String name;

    Dog(String name) {
        ___.name = name;
    }
}
```
= this
wrap: file
hint: The reference to the current object.

? Hide the field from other classes.
```java
class Account {
    ___ double balance;
}
```
= private
wrap: file
hint: The most restrictive access modifier.

? Complete the getter.
```java
class Account {
    private double balance;

    public double getBalance() {
        return ___;
    }
}
```
= balance || this.balance
wrap: file
hint: Return the field.

? Chain to the other constructor.
```java
class Coffee {
    String size;

    Coffee(String size) {
        this.size = size;
    }

    Coffee() {
        ___("medium");
    }
}
```
= this
wrap: file
hint: One constructor calling another of the same class.

? Share one counter between all objects.
```java
class Ticket {
    ___ int issued = 0;

    Ticket() {
        issued++;
    }
}
```
= static
wrap: file
hint: Belongs to the class, not each object.

? Override toString correctly.
```java
class Point {
    int x, y;

    @Override
    ___ String toString() {
        return "(" + x + ", " + y + ")";
    }
}
```
= public
wrap: file
hint: Object's toString is public, and an override can't be less visible.

? Avoid a NullPointerException.
```java
String name = null;
if (name ___ null) {
    System.out.println(name.length());
}
```
= !=
hint: Only use it when it isn't null.

? Declare a constant shared by the class.
```java
class Shop {
    static ___ double TAX = 0.08;
}
```
= final
wrap: file
hint: Constants are static and...

? Which value do object fields start with?
```java
class Box {
    String label;

    boolean isUnlabelled() {
        return label == ___;
    }
}
```
= null
wrap: file
hint: Object references start as "nothing".

@@ level
id: inheritance
title: Inheritance and Interfaces
part: 4
lessons: 21–24
---
? Make Dog a subclass of Animal.
```java
class Animal { }

class Dog ___ Animal { }
```
= extends
wrap: file
hint: The inheritance keyword.

? Call the parent's constructor.
```java
class Animal {
    String name;
    Animal(String name) { this.name = name; }
}

class Dog extends Animal {
    Dog(String name) {
        ___(name);
    }
}
```
= super
wrap: file
hint: Refers to the parent class.

? Ask the compiler to check you're overriding.
```java
class Animal {
    String speak() { return "..."; }
}

class Cat extends Animal {
    ___
    String speak() { return "Meow"; }
}
```
= @Override
wrap: file
hint: An annotation starting with @.

? Make the class fulfil an interface.
```java
interface Payable {
    double amountDue();
}

class Invoice ___ Payable {
    public double amountDue() { return 99; }
}
```
= implements
wrap: file
hint: Classes extend classes but ... interfaces.

? Declare a method that subclasses must implement.
```java
abstract class Shape {
    ___ double area();
}
```
= abstract
wrap: file
hint: A method with no body.

? Test the type and cast in one step.
```java
Object o = "hello";
if (o instanceof String ___) {
    System.out.println(s.length());
}
```
= s
hint: Give the pattern variable the name used inside the if.

? Declare a fixed set of named values.
```java
___ Size { SMALL, MEDIUM, LARGE }
```
= enum
wrap: file
hint: Short for enumeration.

? Declare a concise immutable data class.
```java
___ Point(int x, int y) { }
```
= record
wrap: file
hint: Java 16 feature.

? Read the x component of a record.
```java
record Point(int x, int y) { }

class Use {
    int read(Point p) {
        return p.___;
    }
}
```
= x()
wrap: file
hint: Record accessors are named after the component and have parentheses.

? Give an interface method a body.
```java
interface Greeter {
    String name();

    ___ String greet() {
        return "Hello, " + name();
    }
}
```
= default
wrap: file
hint: The keyword for interface methods with an implementation.

@@ level
id: exceptions-generics
title: Exceptions and Generics
part: 5
lessons: 25–27
---
? Start a block that might throw.
```java
___ {
    int n = Integer.parseInt("abc");
} catch (NumberFormatException e) {
    System.out.println("not a number");
}
```
= try
hint: Try it and see.

? Handle the exception.
```java
try {
    int n = Integer.parseInt("abc");
} ___ (NumberFormatException e) {
    System.out.println(e.getMessage());
}
```
= catch
hint: The partner of try.

? Run cleanup code no matter what.
```java
try {
    System.out.println("work");
} ___ {
    System.out.println("cleanup");
}
```
= finally
hint: It always runs.

? Reject a bad argument.
```java
int qty = 5;
if (qty < 1) {
    ___ new IllegalArgumentException("qty must be positive");
}
```
= throw
hint: Not throws: this one raises the exception.

? Declare that the method may throw a checked exception.
```java
static String load() ___ IOException {
    throw new IOException("missing");
}
```
= throws
wrap: member
hint: The declaration keyword ends in s.

? Append to a StringBuilder.
```java
StringBuilder sb = new StringBuilder();
sb.___("Hello");
```
= append
hint: Add to the end.

? Compare two Integer objects safely.
```java
Integer a = 1000, b = 1000;
boolean same = a.___(b);
```
= equals
hint: == compares references.

? Declare a generic class with a type parameter.
```java
class Box___ {
    private T value;
    T get() { return value; }
}
```
= <T>
wrap: file
hint: Angle brackets with a single capital letter.

? Let the compiler infer the type arguments.
```java
List<String> names = new ArrayList___();
```
= <>
hint: The diamond.

? Close the reader automatically.
```java
___ (BufferedReader r = new BufferedReader(new StringReader("hi"))) {
    System.out.println(r.readLine());
}
```
= try
hint: try-with-resources.

@@ level
id: collections
title: Collections
part: 5
lessons: 28–30
---
? Create an empty, growable list of strings.
```java
List<String> list = new ___<>();
```
= ArrayList || LinkedList
hint: The list backed by an array.

? Add an element to the end.
```java
List<String> list = new ArrayList<>();
list.___("milk");
```
= add
hint: The most common list method.

? Read the first element.
```java
List<String> list = List.of("a", "b");
String first = list.___(0);
```
= get
hint: By index.

? Count the elements in a list.
```java
List<String> list = List.of("a", "b");
int n = list.___();
```
= size
hint: Collections use size(), not length.

? Store a key-value pair.
```java
Map<String, Integer> stock = new HashMap<>();
stock.___("apples", 10);
```
= put
hint: Maps put; lists add.

? Read a value with a fallback.
```java
Map<String, Integer> stock = new HashMap<>();
int n = stock.___("kiwis", 0);
```
= getOrDefault
hint: get... with a default.

? Count occurrences in one call.
```java
Map<String, Integer> counts = new HashMap<>();
counts.___("word", 1, Integer::sum);
```
= merge
hint: Combine the new value with the old one.

? Use a set that keeps elements sorted.
```java
Set<Integer> sorted = new ___<>(List.of(5, 1, 4));
```
= TreeSet
hint: Tree-based collections are sorted.

? Loop over a map's keys and values.
```java
Map<String, Integer> m = Map.of("a", 1);
for (Map.Entry<String, Integer> e : m.___()) {
    System.out.println(e.getKey() + "=" + e.getValue());
}
```
= entrySet
hint: A set of entries.

? Sort people by age.
```java
record Person(String name, int age) { }

class Sorter {
    void sort(List<Person> people) {
        people.sort(Comparator.___(Person::age));
    }
}
```
= comparingInt || comparing
wrap: file
hint: Comparator.comparing...

? Break ties by name.
```java
record Person(String name, int age) { }

class Sorter {
    void sort(List<Person> people) {
        people.sort(Comparator.comparingInt(Person::age).___(Person::name));
    }
}
```
= thenComparing
wrap: file
hint: then...

@@ level
id: modern
title: Lambdas and Streams
part: 6
lessons: 31–34
---
? Complete the lambda arrow.
```java
Function<Integer, Integer> doubleIt = x ___ x * 2;
```
= ->
hint: Parameters, arrow, expression.

? Refer to an existing method instead of writing a lambda.
```java
List.of("a", "b").forEach(System.out___println);
```
= ::
hint: Two colons.

? Keep only the long words.
```java
List<String> words = List.of("java", "stream");
List<String> longOnes = words.stream().___(w -> w.length() > 4).toList();
```
= filter
hint: Keep the matching elements.

? Transform every element.
```java
List<String> words = List.of("java", "map");
List<Integer> lengths = words.stream().___(String::length).toList();
```
= map
hint: Map each element to something new.

? Finish the pipeline into a list.
```java
List<Integer> nums = List.of(3, 1, 2);
List<Integer> sorted = nums.stream().sorted().___();
```
= toList
hint: The Java 16 shortcut for collecting to a list.

? Sum an IntStream.
```java
List<Integer> nums = List.of(1, 2, 3);
int total = nums.stream().mapToInt(Integer::intValue).___();
```
= sum
hint: The obvious name.

? Group words by length.
```java
List<String> words = List.of("hi", "cat", "ox");
Map<Integer, List<String>> byLen = words.stream().collect(Collectors.___(String::length));
```
= groupingBy
hint: Collectors.grouping...

? Fall back when an Optional is empty.
```java
Optional<String> name = Optional.empty();
String shown = name.___("guest");
```
= orElse
hint: or...

? Test a value with a Predicate.
```java
Predicate<Integer> positive = n -> n > 0;
boolean ok = positive.___(5);
```
= test
hint: Predicates test.

? Let the compiler infer a local variable's type.
```java
___ names = new ArrayList<String>();
```
= var
hint: Java 10's three-letter keyword.

? Allow only these two classes to implement the interface.
```java
sealed interface Result ___ Ok, Err { }
record Ok(int value) implements Result { }
record Err(String message) implements Result { }
```
= permits
wrap: file
hint: Sealed types list who...

@@ level
id: advanced
title: Files and Concurrency
part: 7
lessons: 35–37
---
? Read a whole file into a String.
```java
Path p = Path.of("notes.txt");
Files.writeString(p, "hi");
String text = Files.___(p);
```
= readString
hint: The partner of writeString.

? Name a file path.
```java
Path p = Path.___("data.csv");
```
= of
hint: Path.of(...)

? Read every line into a list.
```java
Path p = Path.of("lines.txt");
Files.writeString(p, "a\nb");
List<String> lines = Files.___(p);
```
= readAllLines
hint: read all ...

? Start a new thread.
```java
Thread t = new Thread(() -> System.out.println("hi"));
t.___();
```
= start
hint: Not run().

? Wait for a thread to finish.
```java
Thread t = new Thread(() -> { });
t.start();
t.___();
```
= join
hint: Join it.

? Submit a task to a thread pool.
```java
ExecutorService pool = Executors.newFixedThreadPool(2);
Future<Integer> f = pool.___(() -> 6 * 7);
System.out.println(f.get());
pool.shutdown();
```
= submit
hint: Hand the task over.

? Stop the pool's threads once the work is done.
```java
ExecutorService pool = Executors.newFixedThreadPool(2);
pool.___();
```
= shutdown
hint: shut...

? Increase an atomic counter safely.
```java
AtomicInteger counter = new AtomicInteger();
counter.___();
```
= incrementAndGet || getAndIncrement
hint: increment...

? Let only one thread at a time run this method.
```java
static int count = 0;

static ___ void increment() {
    count++;
}
```
= synchronized
wrap: member
hint: The locking keyword.

? Use the O(1) structure for membership tests.
```java
Set<Integer> seen = new ___<>();
boolean added = seen.add(5);
```
= HashSet
hint: Hash-based collections give constant-time lookups.
