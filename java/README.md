# Learn Java from scratch

A complete, hands-on Java course for beginners: 38 lessons from your first `System.out.println` to generics, streams, concurrency and a final project, with a practice sandbox that compiles and runs real Java in your browser and checks your answers.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/learning/java/)

The sandbox runs the real Java compiler and a Java 17 virtual machine inside your browser. Nothing to install, no sign-up.

- every lesson, with **152 examples** you can run and change
- **57 exercises**, numbered by lesson, that test your code and tell you what's off
- **103 quiz questions**, with explanations
- a **Bytecode** tab that shows what the compiler turns your code into
- **[Java Quest](https://kishoremadanagopal.github.io/learning/java/game.html)**, an arcade game for drilling syntax: fill in the missing code before the timer runs out
- your progress and code saved in your own browser

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 38 lessons, each with key terms, examples, common mistakes, exercises, answers and a quiz |
| 📖 [Glossary](glossary.md) | every Java term used in the course, defined in plain English |
| 🧾 [Syntax cheat sheet](cheatsheet.md) | the whole language on one page, with lesson numbers |
| 🎮 [Java Quest](https://kishoremadanagopal.github.io/learning/java/game.html) | timed fill-in-the-code challenges for every part of the course |

## How to use this course

1. Read a lesson, here on GitHub or in the sandbox. Start with its **Key terms**.
2. Run the examples in the sandbox and change them to see what happens.
3. Do the lesson's exercises in the sandbox and press **Check**.
4. Only then open the **Answers** section at the bottom of the lesson.
5. Play the matching **Java Quest** level to make the syntax automatic.

Each lesson has a **Common mistakes** section. Read it: these are the errors beginners hit most often, and you'll recognise them when they happen to you.

## Lessons

### Part 1: First Steps (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 1 | [How Java runs your code](lessons/01-how-java-runs.md) | what a Java program looks like, `javac` and the JVM, bytecode, compile vs runtime errors | 1 |
| 2 | [Printing, comments and structure](lessons/02-hello-world.md) | `println` vs `print`, escape sequences, comments, statements and blocks | 2–3 |
| 3 | [Variables and primitive types](lessons/03-variables-and-types.md) | declaring variables, `int`, `double`, `boolean`, `char`, `String`, `final`, `var` | 4 |
| 4 | [Operators and math](lessons/04-operators-and-math.md) | arithmetic, integer division, `%`, casting, `Math`, overflow | 5–6 |
| 5 | [Strings](lessons/05-strings.md) | `length`, `charAt`, `substring`, `indexOf`, immutability, `equals`, `printf` | 7–8 |
| 6 | [Reading input with Scanner](lessons/06-scanner-input.md) | `Scanner`, `nextLine`, `nextInt`, the newline trap, `Integer.parseInt` | 9 |

### Part 2: Control Flow (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 7 | [Booleans and if statements](lessons/07-conditions.md) | comparisons, `&&` `\|\|` `!`, `if` / `else if` / `else`, the ternary operator | 10–11 |
| 8 | [switch statements and expressions](lessons/08-switch.md) | arrow-form `switch`, switch expressions, `yield`, classic switch and fall-through | 12 |
| 9 | [while and do-while loops](lessons/09-while-loops.md) | `while`, `do-while`, counters, accumulators, infinite loops | 13–14 |
| 10 | [for loops](lessons/10-for-loops.md) | `for`, counting patterns, looping over strings, the enhanced for loop, nested loops | 15–16 |
| 11 | [break, continue and loop patterns](lessons/11-break-continue.md) | `break`, `continue`, search flags, labeled break, `while (true)` | 17 |

### Part 3: Arrays and Methods (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 12 | [Arrays](lessons/12-arrays.md) | creating arrays, indexing, `length`, default values, `Arrays.toString`, `Arrays.sort` | 18–19 |
| 13 | [2D arrays](lessons/13-two-d-arrays.md) | arrays of arrays, `grid[row][col]`, nested loops, `Arrays.deepToString`, jagged arrays | 20 |
| 14 | [Methods](lessons/14-methods.md) | defining methods, parameters, return types, `void`, `static`, print vs return | 21–22 |
| 15 | [Overloading, scope and pass-by-value](lessons/15-overloading-and-scope.md) | overloading, scope, pass-by-value, varargs | 23–24 |
| 16 | [Recursion](lessons/16-recursion.md) | base case, recursive case, the call stack, `StackOverflowError`, divide and conquer | 25–26 |

### Part 4: Object-Oriented Java (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 17 | [Classes and objects](lessons/17-classes-and-objects.md) | classes, objects, fields, instance methods, `new`, references, `null`, `toString` | 27 |
| 18 | [Constructors and this](lessons/18-constructors.md) | constructors, `this`, overloaded constructors, `this(...)` chaining, validation | 28 |
| 19 | [Encapsulation](lessons/19-encapsulation.md) | `private` fields, access modifiers, getters and setters, validation, immutability | 29 |
| 20 | [Static fields and methods](lessons/20-static-members.md) | static fields, static methods, constants, utility classes | 30 |
| 21 | [Inheritance](lessons/21-inheritance.md) | `extends`, `super`, `@Override`, `protected`, `Object`, single inheritance | 31 |
| 22 | [Polymorphism and casting](lessons/22-polymorphism.md) | parent-type variables, dynamic dispatch, `instanceof` patterns, casting | 32 |
| 23 | [Abstract classes and interfaces](lessons/23-abstract-and-interfaces.md) | abstract classes, abstract methods, interfaces, `implements`, default methods | 33 |
| 24 | [Enums and records](lessons/24-enums-and-records.md) | enums, enum fields and methods, `values()`, records, compact constructors | 34–35 |

### Part 5: The Core Library (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 25 | [StringBuilder and wrapper classes](lessons/25-stringbuilder-and-wrappers.md) | `StringBuilder`, wrapper classes, autoboxing, `parseInt`, the `Integer` == trap | 36 |
| 26 | [Exceptions](lessons/26-exceptions.md) | `try`/`catch`/`finally`, checked vs unchecked, `throw`, `throws`, custom exceptions, try-with-resources | 37–38 |
| 27 | [Generics](lessons/27-generics.md) | type parameters, generic classes and methods, the diamond, bounded types, wildcards | 39 |
| 28 | [Lists](lessons/28-lists.md) | `ArrayList`, `List.of`, add/get/set/remove, iteration, `removeIf`, `ArrayList` vs `LinkedList` | 40–41 |
| 29 | [Sets and maps](lessons/29-sets-and-maps.md) | `HashSet`, `TreeSet`, `HashMap`, `TreeMap`, `getOrDefault`, `merge`, `equals` and `hashCode` | 42–43 |
| 30 | [Sorting with Comparable and Comparator](lessons/30-sorting-and-comparators.md) | `Comparable`, `compareTo`, `Comparator.comparing`, `thenComparing`, `reversed` | 44 |

### Part 6: Modern Java (Advanced)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 31 | [Lambdas and functional interfaces](lessons/31-lambdas.md) | lambda syntax, functional interfaces, `Function`, `Predicate`, method references | 45–46 |
| 32 | [Streams](lessons/32-streams.md) | `stream()`, `filter`, `map`, `sorted`, `reduce`, `collect`, `groupingBy` | 47–48 |
| 33 | [Optional and null safety](lessons/33-optional.md) | `Optional`, `orElse`, `map`, `ifPresent`, null-safety helpers | 49 |
| 34 | [Modern Java features (10–17)](lessons/34-modern-java-features.md) | `var`, text blocks, pattern matching for `instanceof`, records, sealed classes | 50–51 |

### Part 7: Advanced Java (Advanced)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 35 | [Files and I/O](lessons/35-files-and-io.md) | `Path`, `Files.readString`/`writeString`, `Files.lines`, buffered readers, CSV parsing | 52 |
| 36 | [Concurrency basics](lessons/36-concurrency.md) | threads, `ExecutorService`, futures, race conditions, `synchronized`, atomics, `CompletableFuture` | 53 |
| 37 | [Algorithms and Big-O](lessons/37-algorithms-and-big-o.md) | Big-O, choosing collections, binary search, merge sort, operation costs | 54–55 |
| 38 | [Capstone: a library system](lessons/38-capstone.md) | records, enums, encapsulation, exceptions, Optional and streams in one program | 56–57 |

## Which Java is this?

The sandbox compiles your code with the OpenJDK 17 compiler and runs it on [CheerpJ](https://cheerpj.com), a Java 17 virtual machine that runs in the browser. Everything in the lessons is standard Java 17 and works the same with a JDK on your own computer. A few things differ in the sandbox:

- The first run downloads and starts the compiler, so it takes around 20 seconds. Later runs take a second or two.
- `Scanner(System.in)` reads from the **Input** box under the editor, one line per value.
- An endless loop freezes the page. Reload it; your progress is kept.
- Programs can't open windows (Swing/JavaFX) or connect to the internet.

## Five habits that prevent most bugs

1. Compare strings with `.equals()`, never `==`.
2. `7 / 2` is `3`: dividing two ints drops the decimals. Make one side a `double` when you need them.
3. Valid indexes run from `0` to `length - 1`. Loop with `i < length`, not `i <= length`.
4. Read compiler errors from the **first** one down: later errors are often caused by the first.
5. Check for `null` before calling a method on something that might be missing.

## Credits

The in-browser Java runtime is [CheerpJ](https://cheerpj.com) by Leaning Technologies, used under its free Community License. The compiler and `javap` are from OpenJDK 17 (GPL v2 with the Classpath Exception).

## Editing the course

Lessons are generated from the Markdown sources in [`course/`](course/). See [course/README.md](course/README.md) to edit lessons or add new ones.
