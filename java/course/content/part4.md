@@@ part
id: 4
title: Object-Oriented Java
level: Intermediate
blurb: Model real things with classes and objects, protect their data, reuse code through inheritance, and design flexible programs with polymorphism, interfaces, enums and records.

@@@ lesson
id: classes-and-objects
title: Classes and objects
minutes: 15
summary: Define a class with fields and methods, create objects with new, and understand references and null.
---
A **class** is a blueprint for a new type. An **object** (or **instance**) is one thing built from that blueprint. A `Dog` class describes what every dog has and can do; `rex` and `fido` are two separate dog objects.

```java
class Dog {
    String name;            // fields: data each object holds
    int age;

    String bark() {         // method: behaviour that uses the object's data
        return name + " says woof!";
    }
}

public class Main {
    public static void main(String[] args) {
        Dog rex = new Dog();
        rex.name = "Rex";
        rex.age = 3;

        Dog fido = new Dog();
        fido.name = "Fido";
        fido.age = 7;

        System.out.println(rex.bark());
        System.out.println(fido.name + " is " + fido.age);
    }
}
```

- **Fields** (also called instance variables) are declared in the class body. Each object gets its own copy.
- **Methods** without `static` are **instance methods**: you call them on an object, `rex.bark()`, and they can use that object's fields.
- `new Dog()` creates an object and returns a **reference** to it.

A file can hold several classes, but only one `public` class, which must match the file name. That's why `Main` is public here and `Dog` isn't.

### Objects keep their own state

```java
class Counter {
    int count;

    void increment() {
        count++;
    }
}

public class Main {
    public static void main(String[] args) {
        Counter a = new Counter();
        Counter b = new Counter();
        a.increment();
        a.increment();
        b.increment();
        System.out.println(a.count + " " + b.count);
    }
}
```

### References

A variable of a class type holds a **reference** (an arrow pointing at the object), not the object itself. Copying the variable copies the arrow:

```java
class Box {
    int value;
}

public class Main {
    public static void main(String[] args) {
        Box first = new Box();
        first.value = 1;
        Box second = first;          // same object, two names
        second.value = 99;
        System.out.println(first.value);
        System.out.println(first == second);
    }
}
```

### null

A reference that points at nothing is `null`. Calling a method on `null` throws the most famous exception in Java, `NullPointerException`:

```java error
class Dog {
    String name;
}

public class Main {
    public static void main(String[] args) {
        Dog d = null;
        System.out.println(d.name);
    }
}
```

Fields of object type start as `null` too, so check before use: `if (d != null) { ... }`.

### toString

When you print an object, Java calls its `toString()` method. By default it prints something like `Dog@1b6d3586`. Write your own to get useful output:

```java
class Point {
    int x;
    int y;

    @Override
    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}

public class Main {
    public static void main(String[] args) {
        Point p = new Point();
        p.x = 3;
        p.y = 4;
        System.out.println(p);
        System.out.println("Point: " + p);
    }
}
```

`@Override` tells the compiler you mean to replace an inherited method; it's explained in the Inheritance lesson.

:::exercise Rectangle
Create a class `Rectangle` (not public) with `double` fields `width` and `height`, and instance methods `area()`, `perimeter()` and `isSquare()`. The checker creates rectangles with `new Rectangle()` and sets the fields directly.
```java starter
class Rectangle {

}

public class Main {
    public static void main(String[] args) {
        Rectangle r = new Rectangle();
        r.width = 3;
        r.height = 4;
        System.out.println(r.area());
    }
}
```
```java check
Object r = make("Rectangle");
setField(r, "width", 3.0);
setField(r, "height", 4.0);
near(12, callOn(r, "area"), "area() of a 3 x 4 rectangle");
near(14, callOn(r, "perimeter"), "perimeter() of a 3 x 4 rectangle");
eq(false, callOn(r, "isSquare"), "isSquare() of a 3 x 4 rectangle");
setField(r, "height", 3.0);
eq(true, callOn(r, "isSquare"), "isSquare() of a 3 x 3 rectangle");
```
```java solution
class Rectangle {
    double width;
    double height;

    double area() {
        return width * height;
    }

    double perimeter() {
        return 2 * (width + height);
    }

    boolean isSquare() {
        return width == height;
    }
}

public class Main {
    public static void main(String[] args) {
        Rectangle r = new Rectangle();
        r.width = 3;
        r.height = 4;
        System.out.println(r.area());
    }
}
```
hint: Declare double width; double height; then three methods without static, each using the fields directly.
:::

:::quiz
? What does `new` do?
+ Creates an object and returns a reference to it
- Declares a new class
- Copies an existing object
= `new Dog()` builds a fresh Dog object.

? After `Box b2 = b1; b2.value = 5;`, what is `b1.value`?
+ 5
- The old value
- An error
= Both variables refer to the same object.

? Calling a method on a variable that is `null` throws…
+ NullPointerException
- ClassCastException
- Nothing happens
= There's no object to call the method on.
:::

@@@ lesson
id: constructors
title: Constructors and this
minutes: 12
summary: Initialise objects with constructors, use this, overload constructors and chain them.
---
Setting every field by hand after `new` is tedious and easy to forget. A **constructor** runs automatically when an object is created and sets it up properly.

```java
class Dog {
    String name;
    int age;

    Dog(String name, int age) {      // constructor: same name as the class, no return type
        this.name = name;
        this.age = age;
    }

    String describe() {
        return name + " (" + age + ")";
    }
}

public class Main {
    public static void main(String[] args) {
        Dog rex = new Dog("Rex", 3);
        System.out.println(rex.describe());
    }
}
```

### this

Inside a constructor or instance method, `this` means "the current object". `this.name = name;` copies the **parameter** `name` into the **field** `name`. Without `this`, `name = name;` would just assign the parameter to itself.

### Overloaded constructors and chaining

A class can have several constructors with different parameters. One constructor can call another with `this(...)`, which must be its first statement:

```java
class Coffee {
    String size;
    int shots;

    Coffee(String size, int shots) {
        this.size = size;
        this.shots = shots;
    }

    Coffee(String size) {
        this(size, 1);            // reuse the main constructor
    }

    Coffee() {
        this("medium");
    }

    @Override
    public String toString() {
        return size + " with " + shots + " shot(s)";
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Coffee("large", 3));
        System.out.println(new Coffee("small"));
        System.out.println(new Coffee());
    }
}
```

### The default constructor

If you write **no** constructor, Java provides an empty one, which is why `new Dog()` worked in the previous lesson. As soon as you write any constructor, that free default disappears:

```java error
class Dog {
    String name;

    Dog(String name) {
        this.name = name;
    }
}

public class Main {
    public static void main(String[] args) {
        Dog d = new Dog();
        System.out.println(d.name);
    }
}
```

### Validating in the constructor

Constructors are the perfect place to reject bad data, so invalid objects can never exist:

```java
class Temperature {
    double celsius;

    Temperature(double celsius) {
        if (celsius < -273.15) {
            throw new IllegalArgumentException("Below absolute zero: " + celsius);
        }
        this.celsius = celsius;
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Temperature(21.5).celsius);
        try {
            new Temperature(-300);
        } catch (IllegalArgumentException e) {
            System.out.println("Rejected: " + e.getMessage());
        }
    }
}
```

`throw` and `try/catch` are covered in detail in Part 5.

:::exercise Book
Create a class `Book` with fields `title`, `author` and `pages`, and two constructors: `Book(String title, String author, int pages)` and `Book(String title, String author)` which sets `pages` to `100` by calling the first one with `this(...)`. Add a `toString()` returning like `Dune by Frank Herbert (412 pages)`.
```java starter
class Book {

}

public class Main {
    public static void main(String[] args) {
        // System.out.println(new Book("Dune", "Frank Herbert", 412));
    }
}
```
```java check
Object b = make("Book", "Dune", "Frank Herbert", 412);
eq("Dune by Frank Herbert (412 pages)", b.toString(), "toString() of Book(\"Dune\", \"Frank Herbert\", 412)");
Object c = make("Book", "Notes", "Ada");
eq(100, field(c, "pages"), "pages of a Book made with two arguments");
eq("Notes by Ada (100 pages)", c.toString(), "toString() of Book(\"Notes\", \"Ada\")");
sourceHas("this(", "Call the three-argument constructor with this(...).");
```
```java solution
class Book {
    String title;
    String author;
    int pages;

    Book(String title, String author, int pages) {
        this.title = title;
        this.author = author;
        this.pages = pages;
    }

    Book(String title, String author) {
        this(title, author, 100);
    }

    @Override
    public String toString() {
        return title + " by " + author + " (" + pages + " pages)";
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Book("Dune", "Frank Herbert", 412));
    }
}
```
hint: The two-argument constructor's body is just this(title, author, 100); and toString() must be declared public.
:::

:::quiz
? What is special about a constructor's declaration?
+ It has the class's name and no return type
- It must be static
- It must be called init
= `Dog(String name) { ... }`: same name as the class, no return type, not even void.

? In `this.name = name;`, what does `this.name` refer to?
+ The object's field
- The parameter
- A local variable
= `this.` picks the field; the plain `name` is the parameter.

? When does Java provide a default no-argument constructor?
+ Only if the class declares no constructors at all
- Always
- Never
= Writing any constructor removes the automatic default one.
:::

@@@ lesson
id: encapsulation
title: Encapsulation
minutes: 12
summary: Hide fields with private, expose behaviour with methods, and keep objects valid.
---
**Encapsulation** means an object protects its own data. Other code shouldn't reach in and set fields to invalid values; it should ask the object through methods, and the object enforces its rules.

### Access modifiers

| Modifier | Visible to |
|---|---|
| `private` | only the same class |
| *(none)* | the same package |
| `protected` | the same package and subclasses |
| `public` | everyone |

The usual design: fields `private`, methods that others need `public`.

```java
class BankAccount {
    private final String owner;
    private double balance;

    public BankAccount(String owner, double opening) {
        if (opening < 0) {
            throw new IllegalArgumentException("Opening balance can't be negative");
        }
        this.owner = owner;
        this.balance = opening;
    }

    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit must be positive");
        }
        balance += amount;
    }

    public boolean withdraw(double amount) {
        if (amount <= 0 || amount > balance) {
            return false;
        }
        balance -= amount;
        return true;
    }

    public double getBalance() {
        return balance;
    }

    public String getOwner() {
        return owner;
    }
}

public class Main {
    public static void main(String[] args) {
        BankAccount acct = new BankAccount("Ana", 100);
        acct.deposit(50);
        System.out.println(acct.withdraw(500));
        System.out.println(acct.withdraw(30));
        System.out.println(acct.getOwner() + ": " + acct.getBalance());
        // acct.balance = 1_000_000;   // won't compile: balance is private
    }
}
```

Because `balance` is private, the only way to change it is through `deposit` and `withdraw`, so it can never go negative.

### Getters and setters

A **getter** returns a field (`getBalance()`); a **setter** changes one (`setName(...)`). Don't add a setter for every field automatically. Add one only when changing the field makes sense, and validate in it:

```java
class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        setAge(age);
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("Unrealistic age: " + age);
        }
        this.age = age;
    }

    public String getName() {
        return name;
    }
}

public class Main {
    public static void main(String[] args) {
        Person p = new Person("Grace", 85);
        p.setAge(86);
        System.out.println(p.getName() + " is " + p.getAge());
    }
}
```

By convention, a boolean getter is named `isSomething()`, like `isEmpty()`.

### Immutable objects

An object whose state can't change after construction is **immutable**: make the fields `private final` and provide no setters. `String` works this way. Immutable objects are simple to reason about and safe to share.

:::exercise Thermostat
Create a class `Thermostat` with a **private** `double` field `target`, a constructor `Thermostat(double target)`, `getTarget()`, and `setTarget(double t)` that throws `IllegalArgumentException` unless `t` is between `10` and `30` inclusive. The constructor should use the same rule.
```java starter
class Thermostat {
    double target;
}

public class Main {
    public static void main(String[] args) {
        // Thermostat t = new Thermostat(21);
    }
}
```
```java check
check(fieldIsPrivate("Thermostat", "target"), "Make the field target private.");
Object t = make("Thermostat", 21.0);
near(21, callOn(t, "getTarget"), "getTarget() after new Thermostat(21)");
callOn(t, "setTarget", 25.5);
near(25.5, callOn(t, "getTarget"), "getTarget() after setTarget(25.5)");
expectThrows("IllegalArgumentException", () -> callOn(t, "setTarget", 31.0), "setTarget(31)");
expectThrows("IllegalArgumentException", () -> callOn(t, "setTarget", 9.5), "setTarget(9.5)");
near(25.5, callOn(t, "getTarget"), "The target after a rejected setTarget call");
expectThrows("IllegalArgumentException", () -> make("Thermostat", 5.0), "new Thermostat(5)");
```
```java solution
class Thermostat {
    private double target;

    public Thermostat(double target) {
        setTarget(target);
    }

    public double getTarget() {
        return target;
    }

    public void setTarget(double t) {
        if (t < 10 || t > 30) {
            throw new IllegalArgumentException("Target must be between 10 and 30");
        }
        target = t;
    }
}

public class Main {
    public static void main(String[] args) {
        Thermostat t = new Thermostat(21);
        t.setTarget(25.5);
        System.out.println(t.getTarget());
    }
}
```
hint: Make target private. In setTarget, throw new IllegalArgumentException(...) when t < 10 || t > 30. Have the constructor call setTarget(target) so the rule lives in one place.
:::

:::quiz
? Which modifier hides a field from every other class?
+ private
- protected
- public
= `private` members are visible only inside their own class.

? Why make `balance` private and offer `deposit`/`withdraw`?
+ So the account can enforce its rules, like never going negative
- Private fields are faster
- It's required for doubles
= Methods can validate every change; direct field access can't.
:::

@@@ lesson
id: static-members
title: Static fields and methods
minutes: 10
summary: Understand what belongs to the class versus each object, and when to use static.
---
Everything you've declared without `static` belongs to **each object**. A `static` member belongs to the **class itself** and is shared by all objects.

```java
class Ticket {
    private static int nextNumber = 1;    // shared by every Ticket
    private final int number;             // each Ticket has its own

    Ticket() {
        number = nextNumber;
        nextNumber++;
    }

    int getNumber() {
        return number;
    }

    static int issued() {                 // called on the class: Ticket.issued()
        return nextNumber - 1;
    }
}

public class Main {
    public static void main(String[] args) {
        Ticket a = new Ticket();
        Ticket b = new Ticket();
        Ticket c = new Ticket();
        System.out.println(a.getNumber() + " " + b.getNumber() + " " + c.getNumber());
        System.out.println("Issued: " + Ticket.issued());
    }
}
```

### When to use static

- **Constants**: `static final double TAX = 0.08;`, like `Math.PI`.
- **Utility methods** that only work on their parameters: `Math.max`, `Integer.parseInt`, `Arrays.sort`.
- **Shared counters or caches**, like `nextNumber` above.

### What static code can't do

A static method has no `this`, because there's no current object. So it can't use instance fields or call instance methods directly:

```java error
class Dog {
    String name = "Rex";

    static void bark() {
        System.out.println(name + " says woof");
    }
}

public class Main {
    public static void main(String[] args) {
        Dog.bark();
    }
}
```

That's why `main`, which is static, has been calling other static methods: it needs an object before it can call instance methods.

### A utility class

```java
final class Temperatures {
    private Temperatures() { }        // no objects needed

    static double toFahrenheit(double c) {
        return c * 9 / 5 + 32;
    }

    static double toCelsius(double f) {
        return (f - 32) * 5 / 9;
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(Temperatures.toFahrenheit(100));
        System.out.println(Temperatures.toCelsius(212));
    }
}
```

The private constructor prevents anyone from creating pointless `Temperatures` objects.

:::exercise Instance counter
Create a class `Player` with a `name` field, a constructor `Player(String name)`, and a **static** method `count()` that returns how many `Player` objects have been created so far.
```java starter
class Player {
    String name;

    Player(String name) {
        this.name = name;
    }
}

public class Main {
    public static void main(String[] args) {
        new Player("Ana");
        new Player("Ben");
        // System.out.println(Player.count());
    }
}
```
```java check
int before = (Integer) callStatic("Player", "count");
make("Player", "X");
make("Player", "Y");
make("Player", "Z");
eq(before + 3, callStatic("Player", "count"), "Player.count() after creating 3 more players");
```
```java solution
class Player {
    private static int created = 0;
    String name;

    Player(String name) {
        this.name = name;
        created++;
    }

    static int count() {
        return created;
    }
}

public class Main {
    public static void main(String[] args) {
        new Player("Ana");
        new Player("Ben");
        System.out.println(Player.count());
    }
}
```
hint: Add private static int created = 0; increase it in the constructor, and return it from static int count().
:::

:::quiz
? How many copies of a static field exist?
+ One, shared by the class
- One per object
- One per method
= Static members belong to the class, not to individual objects.

? Why can't a static method use `this`?
+ It isn't called on any particular object
- `this` is a reserved word
- It can, always
= There's no current object inside a static method.
:::

@@@ lesson
id: inheritance
title: Inheritance
minutes: 15
summary: Extend classes, override methods with @Override, call super, and use protected.
---
**Inheritance** lets a class (the **subclass** or child) reuse and extend another class (the **superclass** or parent) with `extends`. The relationship is "is a": a `Dog` **is an** `Animal`.

```java
class Animal {
    protected String name;

    Animal(String name) {
        this.name = name;
    }

    String speak() {
        return "...";
    }

    String introduce() {
        return "I am " + name + " and I say " + speak();
    }
}

class Dog extends Animal {
    Dog(String name) {
        super(name);                // run Animal's constructor
    }

    @Override
    String speak() {
        return "Woof";
    }
}

class Cat extends Animal {
    Cat(String name) {
        super(name);
    }

    @Override
    String speak() {
        return "Meow";
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Dog("Rex").introduce());
        System.out.println(new Cat("Tom").introduce());
    }
}
```

`Dog` didn't write `introduce()`; it **inherited** it. It only **overrode** `speak()`, the part that differs.

### super

- `super(...)` calls the parent's constructor. It must be the first line of the child's constructor.
- `super.method()` calls the parent's version of an overridden method, so you can extend it rather than replace it.

```java
class Employee {
    protected String name;
    protected double salary;

    Employee(String name, double salary) {
        this.name = name;
        this.salary = salary;
    }

    String describe() {
        return name + " earns " + salary;
    }
}

class Manager extends Employee {
    private final int reports;

    Manager(String name, double salary, int reports) {
        super(name, salary);
        this.reports = reports;
    }

    @Override
    String describe() {
        return super.describe() + " and manages " + reports + " people";
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Manager("Ana", 120000, 4).describe());
    }
}
```

### @Override catches mistakes

`@Override` asks the compiler to confirm you're really overriding a parent method. A typo then becomes a compile error instead of a silent bug:

```java error
class Animal {
    String speak() { return "..."; }
}

class Dog extends Animal {
    @Override
    String speek() { return "Woof"; }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Dog().speak());
    }
}
```

### Every class extends Object

A class without `extends` implicitly extends `java.lang.Object`. That's where `toString()`, `equals()` and `hashCode()` come from.

### Rules worth knowing

- A class can extend only **one** class (single inheritance). Interfaces (two lessons ahead) cover multiple-type needs.
- `final class` can't be extended; a `final` method can't be overridden.
- `private` members aren't visible to subclasses; `protected` ones are.
- Prefer **composition** (a field holding another object) for "has a" relationships. A `Car` has an `Engine`; it isn't one.

:::exercise Savings account
Given `Account`, create `SavingsAccount extends Account` with a constructor `SavingsAccount(String owner, double balance, double rate)` that calls `super`, and a method `addInterest()` that increases the balance by `balance * rate`. Override `toString()` to append ` @ 5.0%` for a rate of 0.05 (use `rate * 100`).
```java starter
class Account {
    protected String owner;
    protected double balance;

    Account(String owner, double balance) {
        this.owner = owner;
        this.balance = balance;
    }

    @Override
    public String toString() {
        return owner + ": " + balance;
    }
}

class SavingsAccount {

}

public class Main {
    public static void main(String[] args) {
        // SavingsAccount s = new SavingsAccount("Ana", 1000, 0.05);
        // s.addInterest();
        // System.out.println(s);
    }
}
```
```java check
check(isSubclass("SavingsAccount", "Account"), "SavingsAccount should extend Account.");
Object s = make("SavingsAccount", "Ana", 1000.0, 0.05);
callOn(s, "addInterest");
near(1050, field(s, "balance"), "balance after addInterest() on 1000 at 5%");
eq("Ana: 1050.0 @ 5.0%", s.toString(), "toString()");
sourceHas("super(", "Call the parent constructor with super(...).");
```
```java solution
class Account {
    protected String owner;
    protected double balance;

    Account(String owner, double balance) {
        this.owner = owner;
        this.balance = balance;
    }

    @Override
    public String toString() {
        return owner + ": " + balance;
    }
}

class SavingsAccount extends Account {
    private final double rate;

    SavingsAccount(String owner, double balance, double rate) {
        super(owner, balance);
        this.rate = rate;
    }

    void addInterest() {
        balance += balance * rate;
    }

    @Override
    public String toString() {
        return super.toString() + " @ " + rate * 100 + "%";
    }
}

public class Main {
    public static void main(String[] args) {
        SavingsAccount s = new SavingsAccount("Ana", 1000, 0.05);
        s.addInterest();
        System.out.println(s);
    }
}
```
hint: class SavingsAccount extends Account { ... }. The constructor starts with super(owner, balance); toString() returns super.toString() + " @ " + rate * 100 + "%".
:::

:::quiz
? What does `super(name)` do in a constructor?
+ Runs the parent class's constructor
- Creates a second object
- Calls the overridden method
= It lets the parent initialise its part of the object; it must come first.

? How many classes can a Java class extend directly?
+ One
- Two
- Any number
= Java has single inheritance for classes. Interfaces fill the gap.

? Why write `@Override`?
+ The compiler checks that a parent method is really being overridden
- It makes the method faster
- It's required for every method
= A misspelled method name becomes a compile error instead of a silent bug.
:::

@@@ lesson
id: polymorphism
title: Polymorphism and casting
minutes: 12
summary: Use parent-type variables for child objects, rely on dynamic dispatch, and check types with instanceof.
---
**Polymorphism** ("many forms") means a variable of a parent type can hold any subclass object, and calling a method runs the **object's** version.

```java
class Shape {
    double area() { return 0; }
    String name() { return "shape"; }
}

class Circle extends Shape {
    private final double r;
    Circle(double r) { this.r = r; }
    @Override double area() { return Math.PI * r * r; }
    @Override String name() { return "circle"; }
}

class Square extends Shape {
    private final double side;
    Square(double side) { this.side = side; }
    @Override double area() { return side * side; }
    @Override String name() { return "square"; }
}

public class Main {
    public static void main(String[] args) {
        Shape[] shapes = {new Circle(1), new Square(2), new Circle(0.5)};
        double total = 0;
        for (Shape s : shapes) {
            System.out.printf("%-7s %.2f%n", s.name(), s.area());
            total += s.area();
        }
        System.out.printf("total   %.2f%n", total);
    }
}
```

The loop doesn't know or care which shape it has. Java picks the right `area()` at runtime; this is called **dynamic dispatch**. Adding a `Triangle` later needs no change to the loop.

### Declared type vs actual type

In `Shape s = new Circle(1);` the **declared type** is `Shape` and the **actual type** is `Circle`:

- The **declared type** decides which methods you're *allowed* to call (checked at compile time).
- The **actual type** decides which version *runs* (at runtime).

### instanceof and casting

Sometimes you need a subclass-only method. Check the type with `instanceof`, then **cast**. Java 16 added **pattern matching**, which does both in one step:

```java error
class Animal { }
class Dog extends Animal {
    String fetch() { return "fetching!"; }
}
class Cat extends Animal { }

public class Main {
    public static void main(String[] args) {
        Animal[] animals = {new Dog(), new Cat()};
        for (Animal a : animals) {
            if (a instanceof Dog d) {          // test and cast in one go
                System.out.println("Dog is " + d.fetch());
            } else {
                System.out.println(a.getClass().getSimpleName() + " can't fetch");
            }
        }

        Animal x = new Cat();
        Dog old = (Dog) x;                     // a wrong cast compiles but fails at runtime
    }
}
```

That last line compiles but throws `ClassCastException`, because a `Cat` isn't a `Dog`. Frequent `instanceof` checks often mean a method belongs in the parent class instead.

### Overloading vs overriding

| | Overloading | Overriding |
|---|---|---|
| What | same name, different parameters | same signature in a subclass |
| Chosen | at compile time, by argument types | at runtime, by the object's type |
| Example | `add(int, int)` / `add(double, double)` | `Dog.speak()` replacing `Animal.speak()` |

:::exercise Payroll
Create a class `Employee` with a `String name` and a method `double pay()` returning `0`. Create `Salaried extends Employee` (constructor `Salaried(String name, double annual)`, `pay()` returns `annual / 12`) and `Hourly extends Employee` (constructor `Hourly(String name, double rate, double hours)`, `pay()` returns `rate * hours`). Then write `static double totalPayroll(Employee[] staff)` in `Main`.
```java starter
class Employee {
    String name;

    Employee(String name) {
        this.name = name;
    }

    double pay() {
        return 0;
    }
}

public class Main {
    static double totalPayroll(Employee[] staff) {
        return 0;
    }

    public static void main(String[] args) {
    }
}
```
```java check
check(isSubclass("Salaried", "Employee") && isSubclass("Hourly", "Employee"), "Salaried and Hourly should both extend Employee.");
Object s = make("Salaried", "Ana", 60000.0);
Object h = make("Hourly", "Ben", 20.0, 10.0);
near(5000, callOn(s, "pay"), "Salaried(\"Ana\", 60000).pay()");
near(200, callOn(h, "pay"), "Hourly(\"Ben\", 20, 10).pay()");
Object staff = java.lang.reflect.Array.newInstance(cls("Employee"), 2);
java.lang.reflect.Array.set(staff, 0, s);
java.lang.reflect.Array.set(staff, 1, h);
near(5200, call("totalPayroll", staff), "totalPayroll of both employees");
```
```java solution
class Employee {
    String name;

    Employee(String name) {
        this.name = name;
    }

    double pay() {
        return 0;
    }
}

class Salaried extends Employee {
    private final double annual;

    Salaried(String name, double annual) {
        super(name);
        this.annual = annual;
    }

    @Override
    double pay() {
        return annual / 12;
    }
}

class Hourly extends Employee {
    private final double rate;
    private final double hours;

    Hourly(String name, double rate, double hours) {
        super(name);
        this.rate = rate;
        this.hours = hours;
    }

    @Override
    double pay() {
        return rate * hours;
    }
}

public class Main {
    static double totalPayroll(Employee[] staff) {
        double total = 0;
        for (Employee e : staff) {
            total += e.pay();
        }
        return total;
    }

    public static void main(String[] args) {
        Employee[] staff = {new Salaried("Ana", 60000), new Hourly("Ben", 20, 10)};
        System.out.println(totalPayroll(staff));
    }
}
```
hint: Each subclass calls super(name) and overrides pay(). totalPayroll loops over the array and adds up e.pay(); dynamic dispatch picks the right version.
:::

:::quiz
? `Animal a = new Dog(); a.speak();` runs which `speak()`?
+ Dog's
- Animal's
- Both
= The object's actual type decides at runtime.

? What does `if (x instanceof Dog d)` do?
+ Checks the type and, if it matches, makes `d` a Dog variable
- Creates a new Dog
- Always casts, even if x isn't a Dog
= Pattern matching combines the type test and the cast.

? A wrong downcast like `(Dog) someCat` causes…
+ ClassCastException at runtime
- A compile error
- Nothing
= The compiler can't always know the actual type, so the check happens at runtime.
:::

@@@ lesson
id: abstract-and-interfaces
title: Abstract classes and interfaces
minutes: 15
summary: Force subclasses to fill in methods, define capabilities with interfaces, and use default methods.
---
### Abstract classes

An **abstract** class is a partial blueprint. It can't be instantiated, and it can declare **abstract methods** that every concrete subclass must implement:

```java
abstract class Shape {
    abstract double area();                 // no body: subclasses must provide one

    String describe() {                     // normal methods are fine too
        return getClass().getSimpleName() + String.format(" with area %.2f", area());
    }
}

class Circle extends Shape {
    private final double r;
    Circle(double r) { this.r = r; }
    @Override double area() { return Math.PI * r * r; }
}

class Rect extends Shape {
    private final double w, h;
    Rect(double w, double h) { this.w = w; this.h = h; }
    @Override double area() { return w * h; }
}

public class Main {
    public static void main(String[] args) {
        Shape[] shapes = {new Circle(1), new Rect(2, 3)};
        for (Shape s : shapes) {
            System.out.println(s.describe());
        }
        // new Shape();   // won't compile: Shape is abstract
    }
}
```

### Interfaces

An **interface** describes a **capability**: a set of methods a class promises to provide. A class `implements` an interface, and unlike `extends`, a class can implement **many** interfaces.

```java
interface Payable {
    double amountDue();
}

interface Describable {
    String describe();

    default String shout() {                 // default method: has a body
        return describe().toUpperCase() + "!";
    }
}

class Invoice implements Payable, Describable {
    private final double total;
    Invoice(double total) { this.total = total; }
    public double amountDue() { return total; }
    public String describe() { return "invoice for " + total; }
}

class Salary implements Payable {
    public double amountDue() { return 3000; }
}

public class Main {
    public static void main(String[] args) {
        Payable[] bills = {new Invoice(120.5), new Salary()};
        double sum = 0;
        for (Payable p : bills) {
            sum += p.amountDue();
        }
        System.out.println("Total due: " + sum);
        System.out.println(new Invoice(9).shout());
    }
}
```

Interface methods are `public` automatically, so the implementing methods must be `public` too.

### Abstract class or interface?

| | Abstract class | Interface |
|---|---|---|
| Relationship | "is a" (shared identity) | "can do" (a capability) |
| A class can have | one parent | many interfaces |
| Fields | any | only constants |
| Constructors | yes | no |

Prefer interfaces for capabilities like `Comparable`, `Runnable` or `Payable`; use an abstract class when subclasses share real state and code.

### Interfaces you'll use constantly

- `Comparable<T>`: objects that know how to compare themselves (Part 5).
- `Runnable`, `Comparator`, `Function`: often written as lambdas (Part 6).
- `List`, `Set`, `Map`: the collection types (Part 5) are interfaces.

:::exercise Shapes with an interface
Create an interface `HasArea` with `double area();`, and two classes implementing it: `Circle(double radius)` and `Rect(double width, double height)`. Then write `static double totalArea(HasArea[] items)` in `Main`.
```java starter
public class Main {
    static double totalArea(HasArea[] items) {
        return 0;
    }

    public static void main(String[] args) {
    }
}
```
```java check
check(cls("HasArea").isInterface(), "HasArea should be an interface.");
check(isSubclass("Circle", "HasArea") && isSubclass("Rect", "HasArea"), "Circle and Rect should implement HasArea.");
Object c = make("Circle", 2.0);
Object r = make("Rect", 2.0, 3.0);
near(Math.PI * 4, callOn(c, "area"), "new Circle(2).area()");
near(6, callOn(r, "area"), "new Rect(2, 3).area()");
Object arr = java.lang.reflect.Array.newInstance(cls("HasArea"), 2);
java.lang.reflect.Array.set(arr, 0, c);
java.lang.reflect.Array.set(arr, 1, r);
near(Math.PI * 4 + 6, call("totalArea", arr), "totalArea of both");
```
```java solution
interface HasArea {
    double area();
}

class Circle implements HasArea {
    private final double radius;

    Circle(double radius) {
        this.radius = radius;
    }

    public double area() {
        return Math.PI * radius * radius;
    }
}

class Rect implements HasArea {
    private final double width;
    private final double height;

    Rect(double width, double height) {
        this.width = width;
        this.height = height;
    }

    public double area() {
        return width * height;
    }
}

public class Main {
    static double totalArea(HasArea[] items) {
        double total = 0;
        for (HasArea item : items) {
            total += item.area();
        }
        return total;
    }

    public static void main(String[] args) {
        HasArea[] items = {new Circle(2), new Rect(2, 3)};
        System.out.println(totalArea(items));
    }
}
```
hint: interface HasArea { double area(); } then class Circle implements HasArea { ... public double area() { ... } }. The implementing methods must be public.
:::

:::quiz
? Can you create an object with `new` from an abstract class?
- Yes
+ No
= Abstract classes are partial; only concrete subclasses can be instantiated.

? How many interfaces can a class implement?
- One
+ Any number
- Two
= `class A implements X, Y, Z` is fine.

? Why must a method implementing an interface method be `public`?
+ Interface methods are implicitly public, and you can't reduce visibility
- It's a style rule only
- It doesn't have to be
= An override can't be less visible than the method it implements.
:::

@@@ lesson
id: enums-and-records
title: Enums and records
minutes: 12
summary: Represent fixed sets of values with enums, and immutable data with records.
---
### Enums

An **enum** is a type with a fixed set of named values. It's safer than using strings or ints for things like days, sizes or states: a typo becomes a compile error.

```java
enum Size {
    SMALL, MEDIUM, LARGE
}

public class Main {
    static double price(Size size) {
        return switch (size) {
            case SMALL -> 2.50;
            case MEDIUM -> 3.00;
            case LARGE -> 3.75;
        };
    }

    public static void main(String[] args) {
        Size s = Size.MEDIUM;
        System.out.println(s + " costs " + price(s));
        for (Size each : Size.values()) {
            System.out.println(each.ordinal() + " " + each.name().toLowerCase());
        }
        System.out.println(Size.valueOf("LARGE") == Size.LARGE);
    }
}
```

Notice the switch needs no `default`: the compiler knows all three values are covered.

### Enums with fields and methods

Enums are full classes, so each value can carry data:

```java
enum Planet {
    MERCURY(3.303e23, 2.4397e6),
    EARTH(5.976e24, 6.37814e6),
    JUPITER(1.9e27, 7.1492e7);

    private final double mass;      // kg
    private final double radius;    // m

    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }

    double surfaceGravity() {
        return 6.67300E-11 * mass / (radius * radius);
    }
}

public class Main {
    public static void main(String[] args) {
        for (Planet p : Planet.values()) {
            System.out.printf("%-8s %5.2f m/s²%n", p, p.surfaceGravity());
        }
    }
}
```

### Records

Many classes just hold data. Writing the constructor, getters, `equals`, `hashCode` and `toString` by hand is repetitive. A **record** (Java 16) generates all of them from one line:

```java
record Point(int x, int y) { }

public class Main {
    public static void main(String[] args) {
        Point a = new Point(3, 4);
        Point b = new Point(3, 4);
        System.out.println(a);
        System.out.println(a.x() + " " + a.y());       // accessor methods, not getX()
        System.out.println(a.equals(b));               // compares the data
        System.out.println(a == b);                    // still different objects
    }
}
```

Records are **immutable**: their fields are `final`. You can add methods, static factories and validation in a **compact constructor**:

```java
record Money(long cents, String currency) {
    Money {                                         // compact constructor
        if (cents < 0) {
            throw new IllegalArgumentException("Negative money");
        }
        currency = currency.toUpperCase();
    }

    Money plus(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("Different currencies");
        }
        return new Money(cents + other.cents, currency);
    }

    String formatted() {
        return String.format("%d.%02d %s", cents / 100, cents % 100, currency);
    }
}

public class Main {
    public static void main(String[] args) {
        Money a = new Money(1050, "usd");
        Money b = new Money(275, "USD");
        System.out.println(a.plus(b).formatted());
        System.out.println(a);
    }
}
```

Use a record whenever a class is "just data". Use a normal class when objects need to change or hide internal state.

:::exercise Traffic light
Create an enum `Light` with values `RED`, `YELLOW` and `GREEN`, and a method `Light next()` returning the next state in the cycle RED → GREEN → YELLOW → RED. Also add a method `int seconds()` returning 30 for RED, 25 for GREEN and 5 for YELLOW.
```java starter
public class Main {
    public static void main(String[] args) {
        // Light l = Light.RED;
        // System.out.println(l.next() + " " + l.seconds());
    }
}
```
```java check
Class<?> light = cls("Light");
check(light.isEnum(), "Light should be an enum.");
Object red = Enum.valueOf((Class) light, "RED");
Object green = Enum.valueOf((Class) light, "GREEN");
Object yellow = Enum.valueOf((Class) light, "YELLOW");
eq(green, callOn(red, "next"), "RED.next()");
eq(yellow, callOn(green, "next"), "GREEN.next()");
eq(red, callOn(yellow, "next"), "YELLOW.next()");
eq(30, callOn(red, "seconds"), "RED.seconds()");
eq(25, callOn(green, "seconds"), "GREEN.seconds()");
eq(5, callOn(yellow, "seconds"), "YELLOW.seconds()");
```
```java solution
enum Light {
    RED, YELLOW, GREEN;

    Light next() {
        return switch (this) {
            case RED -> GREEN;
            case GREEN -> YELLOW;
            case YELLOW -> RED;
        };
    }

    int seconds() {
        return switch (this) {
            case RED -> 30;
            case GREEN -> 25;
            case YELLOW -> 5;
        };
    }
}

public class Main {
    public static void main(String[] args) {
        Light l = Light.RED;
        System.out.println(l.next() + " " + l.seconds());
    }
}
```
hint: Inside an enum method, this is the current value, so you can switch (this) { case RED -> GREEN; ... }.
:::

:::exercise Student record
Create a record `Student(String name, int[] scores)` with a method `double average()`, and a compact constructor that throws `IllegalArgumentException` if `name` is blank.
```java starter
public class Main {
    public static void main(String[] args) {
        // Student s = new Student("Ana", new int[]{90, 80});
        // System.out.println(s.average());
    }
}
```
```java check
check(cls("Student").isRecord(), "Student should be a record.");
Object s = make("Student", "Ana", new int[]{90, 80, 70});
near(80, callOn(s, "average"), "average() of {90, 80, 70}");
eq("Ana", callOn(s, "name"), "name()");
expectThrows("IllegalArgumentException", () -> make("Student", "  ", new int[]{1}), "new Student(\"  \", ...)");
```
```java solution
record Student(String name, int[] scores) {
    Student {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name is required");
        }
    }

    double average() {
        if (scores.length == 0) {
            return 0;
        }
        int sum = 0;
        for (int s : scores) {
            sum += s;
        }
        return (double) sum / scores.length;
    }
}

public class Main {
    public static void main(String[] args) {
        Student s = new Student("Ana", new int[]{90, 80});
        System.out.println(s.average());
    }
}
```
hint: record Student(String name, int[] scores) { Student { if (name.isBlank()) throw new IllegalArgumentException("..."); } double average() { ... } }
:::

:::quiz
? What does a record generate automatically?
+ Constructor, accessors, equals, hashCode and toString
- Only a constructor
- Setters for every field
= Records are concise, immutable data carriers.

? For `record Point(int x, int y)`, how do you read x?
+ `p.x()`
- `p.getX()`
- `p.x` from outside the record
= Record accessors are named after the components.

? Why use an enum instead of strings like "SMALL"?
+ Typos become compile errors and the set of values is fixed
- Enums use less memory
- Strings can't be used in switch
= The compiler knows every valid value.
:::
