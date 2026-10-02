# Python glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **2D array** | An array whose elements are arrays, used for grids and tables. [13] |
| **Abstract class** | A class that can't be instantiated and may declare abstract methods. [23] |
| **Abstract method** | A method without a body that subclasses must implement. [23] |
| **Access modifier** | `private`, package-private (none), `protected` or `public`. [19] |
| **Accessor** | A record's method for reading a component, like `p.x()`. [24] |
| **Accumulator** | A variable that builds up a result, like a running total. [9] |
| **Algorithm** | A step-by-step method for solving a problem. [37] |
| **Amortised cost** | The average cost per operation over many operations. [37] |
| **Argument** | The value passed in a call. [14] |
| **Array** | A fixed-size sequence of values of one type. [12] |
| **ArrayIndexOutOfBoundsException** | Thrown when using an index outside 0 to length - 1. [12] |
| **ArrayList** | A resizable list backed by an array. [28] |
| **Arrays class** | Helpers like `toString`, `sort`, `fill`, `copyOf` and `equals`. [12] |
| **Arrays.deepToString** | Prints nested arrays readably. [13] |
| **Arrow case (`->`)** | A modern case that runs only its own code, with no fall-through. [8] |
| **Atomic variable** | A variable with thread-safe single operations, like `AtomicInteger`. [36] |
| **Autoboxing / unboxing** | Automatic conversion between primitives and wrappers. [25] |
| **Base case** | The condition where the method answers without recursing. [16] |
| **Big-O notation** | How running time grows with input size. [37] |
| **Binary search** | Finds a value in sorted data by halving the range each step: O(log n). [37] |
| **Block** | Statements grouped in curly braces. [2] |
| **boolean** | `true` or `false`. [3] |
| **Boolean expression** | An expression that is `true` or `false`. [7] |
| **Bounded type** | A type parameter with a limit, like `<T extends Comparable<T>>`. [27] |
| **break** | Leaves the innermost loop immediately. [11] |
| **BufferedReader / BufferedWriter** | Read and write text efficiently, line by line. [35] |
| **Build tool** | Software such as Maven or Gradle that compiles, tests and packages projects. [38] |
| **Bytecode** | Compact instructions in `.class` files that the JVM runs. [1] |
| **Call stack** | The chain of method calls waiting to finish. [16] |
| **camelCase** | The naming style for variables and methods, like `totalPrice`. [3] |
| **Capstone project** | A project that combines everything you've learned. [38] |
| **Cast** | Converting a value to another type, like `(double) total`. [4] |
| **char** | A single character in single quotes, like `'A'`. [3] |
| **Checked exception** | Must be caught or declared, like `IOException`. [26] |
| **Class** | A blueprint that defines a new type. [17] |
| **ClassCastException** | Thrown by an invalid downcast. [22] |
| **Collector** | A recipe for gathering stream results, such as `groupingBy` or `joining`. [32] |
| **Comment** | Text the compiler ignores: `// ...`, `/* ... */` or a Javadoc `/** ... */`. [2] |
| **Compact constructor** | A record constructor without a parameter list, used for validation. [24] |
| **Comparable** | An interface giving a class its natural order through `compareTo`. [30] |
| **Comparator** | A separate object that compares two values. [30] |
| **compareTo** | Returns negative, zero or positive to order two objects. [30] |
| **Comparison operators** | `==`, `!=`, `<`, `>`, `<=`, `>=`. [7] |
| **Compile error** | A mistake found before the program runs, such as a missing semicolon. [1] |
| **Compiler (`javac`)** | Checks your source code and translates it into bytecode. [1] |
| **CompletableFuture** | A future you can chain asynchronous steps onto. [36] |
| **Concatenation** | Joining text with `+`. [2] |
| **ConcurrentModificationException** | Thrown when a collection changes while being iterated. [28] |
| **Constant** | A `static final` value, named in UPPER_SNAKE_CASE. [20] |
| **Constructor** | Special code that initialises a new object; it has the class's name and no return type. [18] |
| **Constructor chaining** | One constructor calling another with `this(...)`. [18] |
| **continue** | Skips the rest of the current iteration. [11] |
| **CSV** | Comma-separated values, a simple text format for tables. [35] |
| **Declaration** | Creating a variable with its type, like `int age;`. [3] |
| **Declared type / actual type** | The variable's type / the object's real class. [22] |
| **default** | The branch used when no case matches. [8] |
| **Default constructor** | The empty constructor Java adds only when a class declares none. [18] |
| **Default method** | An interface method with a body. [23] |
| **Default value** | What new array elements start as: 0, false or null. [12] |
| **Diamond (`<>`)** | Lets the compiler infer type arguments: `new ArrayList<>()`. [27] |
| **Divide and conquer** | Splitting a problem into parts, solving each, and combining the results. [16] |
| **Domain model** | The classes that represent the real-world things a program deals with. [38] |
| **do-while** | Runs the body first, then checks the condition, so it runs at least once. [9] |
| **Dynamic dispatch** | The object's actual class decides which overridden method runs. [22] |
| **Effectively final** | A local variable that's never reassigned, so lambdas can use it. [31] |
| **Element** | One value in an array. [12] |
| **Encapsulation** | Hiding an object's data and controlling access through methods. [19] |
| **Enhanced for (for-each)** | `for (Type item : collection)` visits each element. [10] |
| **Enum** | A type with a fixed set of named constants. [24] |
| **equals** | Compares the text of two strings. [5] |
| **Escape sequence** | A backslash code inside a string, such as `\n` (new line) or `\"` (a quote). [2] |
| **Exception** | An object signalling that something went wrong at runtime. [26] |
| **ExecutorService** | A managed pool of threads that runs submitted tasks. [36] |
| **Fall-through** | In a classic switch, running into the next case when `break` is missing. [8] |
| **Field (instance variable)** | Data that each object stores. [17] |
| **Files** | Utility methods for reading, writing and managing files. [35] |
| **final** | Makes a variable a constant that can't be reassigned. [3] |
| **finally** | A block that always runs, used for cleanup. [26] |
| **Flag** | A boolean that records whether something was found. [11] |
| **for loop** | A loop with start, condition and update in one header. [10] |
| **Functional interface** | An interface with exactly one abstract method. [31] |
| **Function / Predicate / Consumer / Supplier** | Built-in functional interfaces for common shapes. [31] |
| **Future** | A handle to a result that will be available later. [36] |
| **Generics** | Classes and methods that take type parameters, like `List<String>`. [27] |
| **getOrDefault / merge** | Read with a fallback / combine a new value with an existing one. [29] |
| **Getter / setter** | Methods that read / change a field. [19] |
| **hashCode** | A number used by hash collections to locate objects quickly. [29] |
| **HashSet / HashMap** | Fast, unordered implementations. [29] |
| **if / else if / else** | Run the first branch whose condition is true. [7] |
| **Immutable** | Can't be changed; String methods return new strings. [5] |
| **Immutable object** | An object whose state can't change after construction. [19] |
| **implements** | Declares that a class fulfils an interface. [23] |
| **import** | Tells the compiler where a class lives, like `java.util.Scanner`. [6] |
| **Index** | A character's position, starting at 0. [5] |
| **Infinite loop** | A loop whose condition never becomes false. [9] |
| **Inheritance** | A class reusing and extending another with `extends`. [21] |
| **InputMismatchException** | Thrown when `nextInt` meets something that isn't a number. [6] |
| **Instance method** | A method called on an object, which can use its fields. [17] |
| **instanceof** | Checks whether an object is of a type; `x instanceof Dog d` also casts. [22] |
| **int / double** | Whole numbers / decimal numbers. [3] |
| **Integer cache** | Java reuses Integer objects from -128 to 127. [25] |
| **Integer division** | Dividing two ints, which drops the decimal part. [4] |
| **Interface** | A set of methods a class promises to provide. [23] |
| **Intermediate operation** | A lazy step such as `filter` or `map` that returns a stream. [32] |
| **IntStream** | A stream of primitive ints with `sum`, `average` and `range`. [32] |
| **Invariant** | A rule an object always keeps true, like "balance is never negative". [19] |
| **IOException** | The checked exception for input/output failures. [35] |
| **Iteration** | One pass through a loop. [9] |
| **Iterator** | An object that walks a collection and can remove items safely. [28] |
| **Jagged array** | A 2D array whose rows have different lengths. [13] |
| **JDK (Java Development Kit)** | The bundle you install to write Java: compiler, JVM and standard library. [1] |
| **JIT compiler** | The part of the JVM that turns frequently used bytecode into fast machine code while the program runs. [1] |
| **JVM (Java Virtual Machine)** | The program that loads and runs bytecode on any platform. [1] |
| **Key extractor** | A function that picks the value to sort by, like `Person::age`. [30] |
| **Label** | A name on a loop so `break label;` can leave an outer loop. [11] |
| **Lambda** | A short anonymous function: `(params) -> expression`. [31] |
| **length** | An array's size (a field, so no parentheses). [12] |
| **LinkedHashSet / LinkedHashMap** | Keep insertion order. [29] |
| **List** | An ordered collection that allows duplicates. [28] |
| **List.of** | Creates an unmodifiable list. [28] |
| **Local variable** | A variable declared inside a method or block. [15] |
| **Logical operators** | `&&` (and), `\|\|` (or), `!` (not). [7] |
| **Loop** | Code that repeats. [9] |
| **Loop variable** | The counter declared in the for header; it exists only inside the loop. [10] |
| **Map** | A collection of key-value pairs with unique keys. [29] |
| **Math class** | Built-in math helpers like `Math.sqrt`, `Math.pow`, `Math.round`. [4] |
| **Merge sort** | A divide-and-conquer sort running in O(n log n). [37] |
| **Method** | A named, reusable block of code. [14] |
| **Method reference** | Shorthand for a lambda that calls one method, like `String::length`. [31] |
| **Method signature** | A method's name and parameter types. [14] |
| **Modulo (`%`)** | The remainder after division. [4] |
| **Nested loop** | A loop inside another loop. [10] |
| **nextLine / nextInt / nextDouble** | Read a whole line / a whole number / a decimal. [6] |
| **null** | A reference that points to nothing. [17] |
| **NullPointerException** | Thrown when using a null reference. [17] |
| **NumberFormatException** | Thrown when text can't be parsed as a number. [6] |
| **Object** | The class every class ultimately extends. [21] |
| **Object (instance)** | One value created from a class with `new`. [17] |
| **Objects.requireNonNull** | Fails fast with a clear message when a value is null. [33] |
| **Off-by-one error** | Looping one time too many or too few. [10] |
| **Operator** | A symbol such as `+`, `*` or `%` that computes a value. [4] |
| **Optional** | A container that holds a value or is empty. [33] |
| **Optional.ofNullable** | Wraps a value that might be null. [33] |
| **orElse / orElseGet / orElseThrow** | Get the value or fall back. [33] |
| **Overflow** | A value too big for its type wraps around to the other end of the range. [4] |
| **Overloading** | Several methods with the same name and different parameter lists. [15] |
| **Override** | A subclass redefining an inherited method. [21] |
| **@Override** | Asks the compiler to confirm a method really overrides one. [21] |
| **Parameter** | A variable in the method header that receives a value. [14] |
| **Parsing** | Converting text into a number with `Integer.parseInt` or `Double.parseDouble`. [6] |
| **Pass-by-value** | Java passes copies of arguments; for objects, a copy of the reference. [15] |
| **Path** | Names a file or folder. [35] |
| **Pattern matching** | Testing a type and binding a variable in one step: `o instanceof String s`. [34] |
| **permits** | The clause naming a sealed type's allowed subclasses. [34] |
| **Polymorphism** | One variable type referring to objects of many subclasses. [22] |
| **Primitive type** | One of Java's eight built-in value types: `int`, `long`, `double`, `float`, `boolean`, `char`, `byte`, `short`. [3] |
| **printf / String.format** | Fill placeholders like `%s`, `%d` and `%.2f` in a template. [5] |
| **println / print** | Print with or without moving to a new line afterwards. [2] |
| **Program** | A list of instructions for a computer. [1] |
| **protected** | Visible to subclasses and the same package. [21] |
| **Race condition** | A bug where the result depends on how threads interleave. [36] |
| **Record** | A concise, immutable data class with generated constructor, accessors, `equals`, `hashCode` and `toString`. [24] |
| **Recursion** | A method calling itself on a smaller version of the problem. [16] |
| **Recursive case** | The part that calls the method again with a smaller input. [16] |
| **Reference** | A variable's link to an object, such as an array. [12, 17] |
| **return** | Hands a value back and ends the method. [14] |
| **Return type** | The type of value a method gives back; `void` means none. [14] |
| **Row / column** | The first and second index in `grid[row][col]`. [13] |
| **Runtime error (exception)** | A problem that happens while the program runs. [1] |
| **Scanner** | A class that reads text and numbers from input. [6] |
| **Scope** | The region of code where a variable exists. [15] |
| **Sealed class / interface** | A type that lists exactly which classes may extend it. [34] |
| **Sentinel value** | A special input meaning "stop", like `quit`. [11] |
| **Set** | A collection of unique values. [29] |
| **Short-circuit evaluation** | `&&` and `\|\|` skip the right side when the left side decides the result. [7] |
| **Source code** | The Java text you write, saved in `.java` files. [1] |
| **Stable sort** | A sort that keeps the original order of equal elements. [30] |
| **StackOverflowError** | Thrown when calls go too deep, usually because a base case is missing. [16] |
| **Stack trace** | The list of method calls shown when an exception isn't caught. [26] |
| **Statement** | One instruction, ending with a semicolon. [2] |
| **static field** | One shared value that belongs to the class. [20] |
| **static method** | A method that belongs to the class and can be called without an object. [14, 20] |
| **Static typing** | Every variable's type is fixed and checked at compile time. [3] |
| **Stream** | A pipeline that processes a sequence of elements. [32] |
| **String** | Text in double quotes; a class, not a primitive. [3, 5] |
| **StringBuilder** | A changeable string for building text efficiently. [25] |
| **substring(start, end)** | The characters from start up to, but not including, end. [5] |
| **super** | Calls the parent's constructor (`super(...)`) or methods (`super.m()`). [21] |
| **Superclass / subclass** | The parent / the child class. [21] |
| **switch** | Chooses a branch by comparing one value against several cases. [8] |
| **Switch expression** | A switch that produces a value. [8] |
| **synchronized** | Lets only one thread at a time run a block for a given lock. [36] |
| **Terminal operation** | A step such as `toList` or `count` that produces a result and runs the pipeline. [32] |
| **Ternary operator** | `condition ? a : b` chooses between two values. [7] |
| **Text block** | A multi-line string written with triple quotes. [34] |
| **this** | A reference to the current object. [18] |
| **Thread** | An independent path of execution. [36] |
| **throw / throws** | Raise an exception / declare that a method may throw one. [26] |
| **toString()** | The method Java calls to turn an object into text. [17] |
| **TreeSet / TreeMap** | Sorted implementations. [29] |
| **try / catch** | Run code and handle specific exceptions. [26] |
| **try-with-resources** | Closes resources declared in `try (...)` automatically. [26] |
| **Type parameter** | A placeholder type such as `T` in `class Box<T>`. [27] |
| **Unchecked exception** | A `RuntimeException`, usually a programming bug. [26] |
| **Unit test** | A small automated check of one piece of code, usually written with JUnit. [38] |
| **Upcast / downcast** | Treating an object as its parent type / converting back to a subclass. [22] |
| **Utility class** | A class of static helper methods, like `Math`. [20] |
| **values()** | Returns all the constants of an enum. [24] |
| **var** | Lets the compiler infer a local variable's type (Java 10+). [3] |
| **Varargs** | A parameter like `int... nums` that accepts any number of arguments as an array. [15] |
| **Variable** | A named box holding a value of a fixed type. [3] |
| **while** | Repeats while a condition is true, checking it before each pass. [9] |
| **Widening / narrowing** | Converting to a bigger type (automatic) / a smaller one (needs a cast). [4] |
| **Wildcard** | `?` for an unknown type, as in `List<? extends Number>`. [27] |
| **Wrapper class** | An object version of a primitive, such as `Integer` or `Double`. [25] |
| **yield** | Returns a value from a block inside a switch expression. [8] |
