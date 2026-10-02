@@ how-java-runs
topics: what a Java program looks like, `javac` and the JVM, bytecode, compile vs runtime errors
terms:
- **Program:** a list of instructions for a computer.
- **Source code:** the Java text you write, saved in `.java` files.
- **Compiler (`javac`):** checks your source code and translates it into bytecode.
- **Bytecode:** compact instructions in `.class` files that the JVM runs.
- **JVM (Java Virtual Machine):** the program that loads and runs bytecode on any platform.
- **JIT compiler:** the part of the JVM that turns frequently used bytecode into fast machine code while the program runs.
- **JDK (Java Development Kit):** the bundle you install to write Java: compiler, JVM and standard library.
- **Compile error:** a mistake found before the program runs, such as a missing semicolon.
- **Runtime error (exception):** a problem that happens while the program runs.
mistakes:
- Forgetting the semicolon at the end of a statement.
- Mismatched braces: every `{` needs a `}`. Consistent indentation makes it easy to spot.
- Writing `system.out.println` or `Main.Java`: Java is case-sensitive.
- Panicking at red text. Read the first error message: it names the file, the line and what was expected.

@@ hello-world
topics: `println` vs `print`, escape sequences, comments, statements and blocks
terms:
- **Statement:** one instruction, ending with a semicolon.
- **Block:** statements grouped in curly braces.
- **println / print:** print with or without moving to a new line afterwards.
- **Escape sequence:** a backslash code inside a string, such as `\n` (new line) or `\"` (a quote).
- **Comment:** text the compiler ignores: `// ...`, `/* ... */` or a Javadoc `/** ... */`.
- **Concatenation:** joining text with `+`.
mistakes:
- Expecting `print` to add a new line. Only `println` does.
- `"Sum: " + 2 + 3` prints `Sum: 23`. Add parentheses: `"Sum: " + (2 + 3)`.
- Writing a quote inside a string without escaping it: use `\"`.
- Naming the file differently from its public class.

@@ variables-and-types
topics: declaring variables, `int`, `double`, `boolean`, `char`, `String`, `final`, `var`
terms:
- **Variable:** a named box holding a value of a fixed type.
- **Declaration:** creating a variable with its type, like `int age;`.
- **Primitive type:** one of Java's eight built-in value types: `int`, `long`, `double`, `float`, `boolean`, `char`, `byte`, `short`.
- **int / double:** whole numbers / decimal numbers.
- **boolean:** `true` or `false`.
- **char:** a single character in single quotes, like `'A'`.
- **String:** text in double quotes; a class, not a primitive.
- **final:** makes a variable a constant that can't be reassigned.
- **var:** lets the compiler infer a local variable's type (Java 10+).
- **Static typing:** every variable's type is fixed and checked at compile time.
- **camelCase:** the naming style for variables and methods, like `totalPrice`.
mistakes:
- Putting a decimal into an `int`: `int price = 4.99;` doesn't compile.
- Mixing up `'A'` (a char) and `"A"` (a String).
- Using a local variable before giving it a value.
- Capitalising `string` or `Int`. It's `String` and `int`.

@@ operators-and-math
topics: arithmetic, integer division, `%`, casting, `Math`, overflow
terms:
- **Operator:** a symbol such as `+`, `*` or `%` that computes a value.
- **Integer division:** dividing two ints, which drops the decimal part.
- **Modulo (`%`):** the remainder after division.
- **Cast:** converting a value to another type, like `(double) total`.
- **Widening / narrowing:** converting to a bigger type (automatic) / a smaller one (needs a cast).
- **Overflow:** a value too big for its type wraps around to the other end of the range.
- **Math class:** built-in math helpers like `Math.sqrt`, `Math.pow`, `Math.round`.
mistakes:
- Expecting `7 / 2` to be `3.5`. Make one side a double: `7 / 2.0`.
- Casting after dividing: `(double) (a / b)` is still integer division. Write `(double) a / b`.
- Assuming `(int) 3.9` rounds. It cuts off the decimals and gives `3`.
- Using `int` for values that can exceed about 2.1 billion. Use `long`.

@@ strings
topics: `length`, `charAt`, `substring`, `indexOf`, immutability, `equals`, `printf`
terms:
- **String:** an immutable sequence of characters.
- **Index:** a character's position, starting at 0.
- **substring(start, end):** the characters from start up to, but not including, end.
- **Immutable:** can't be changed; String methods return new strings.
- **equals:** compares the text of two strings.
- **printf / String.format:** fill placeholders like `%s`, `%d` and `%.2f` in a template.
mistakes:
- Comparing strings with `==` instead of `.equals()`.
- Forgetting that `substring`'s end index is excluded.
- Calling `s.toUpperCase();` and expecting `s` to change. Write `s = s.toUpperCase();`.
- Using `charAt(s.length())`: the last index is `length() - 1`.

@@ scanner-input
topics: `Scanner`, `nextLine`, `nextInt`, the newline trap, `Integer.parseInt`
terms:
- **Scanner:** a class that reads text and numbers from input.
- **import:** tells the compiler where a class lives, like `java.util.Scanner`.
- **nextLine / nextInt / nextDouble:** read a whole line / a whole number / a decimal.
- **Parsing:** converting text into a number with `Integer.parseInt` or `Double.parseDouble`.
- **NumberFormatException:** thrown when text can't be parsed as a number.
- **InputMismatchException:** thrown when `nextInt` meets something that isn't a number.
mistakes:
- Calling `nextLine()` right after `nextInt()` and getting an empty string. Read lines and parse them instead.
- Forgetting `import java.util.Scanner;`.
- Parsing `"4.5"` with `Integer.parseInt`. Use `Double.parseDouble`.

@@ conditions
topics: comparisons, `&&` `||` `!`, `if` / `else if` / `else`, the ternary operator
terms:
- **Boolean expression:** an expression that is `true` or `false`.
- **Comparison operators:** `==`, `!=`, `<`, `>`, `<=`, `>=`.
- **Logical operators:** `&&` (and), `||` (or), `!` (not).
- **Short-circuit evaluation:** `&&` and `||` skip the right side when the left side decides the result.
- **if / else if / else:** run the first branch whose condition is true.
- **Ternary operator:** `condition ? a : b` chooses between two values.
mistakes:
- Writing `=` (assignment) instead of `==` (comparison) in a condition.
- Putting a broad condition before a narrow one, so the narrow branch never runs.
- Leaving out braces and later adding a second line that isn't inside the if.
- Comparing strings with `==` in a condition.

@@ switch
topics: arrow-form `switch`, switch expressions, `yield`, classic switch and fall-through
terms:
- **switch:** chooses a branch by comparing one value against several cases.
- **Arrow case (`->`):** a modern case that runs only its own code, with no fall-through.
- **Switch expression:** a switch that produces a value.
- **yield:** returns a value from a block inside a switch expression.
- **Fall-through:** in a classic switch, running into the next case when `break` is missing.
- **default:** the branch used when no case matches.
mistakes:
- Forgetting `break` in a classic switch, which falls through into the next case.
- Leaving out `default` in a switch expression that doesn't cover every value.
- Trying to switch on a `double` or `boolean`, which isn't allowed.

@@ while-loops
topics: `while`, `do-while`, counters, accumulators, infinite loops
terms:
- **Loop:** code that repeats.
- **Iteration:** one pass through a loop.
- **while:** repeats while a condition is true, checking it before each pass.
- **do-while:** runs the body first, then checks the condition, so it runs at least once.
- **Accumulator:** a variable that builds up a result, like a running total.
- **Infinite loop:** a loop whose condition never becomes false.
mistakes:
- Forgetting to update the loop variable, creating an infinite loop.
- Off-by-one conditions: `< 10` stops at 9; `<= 10` includes 10.
- Declaring the accumulator inside the loop, so it resets every pass.

@@ for-loops
topics: `for`, counting patterns, looping over strings, the enhanced for loop, nested loops
terms:
- **for loop:** a loop with start, condition and update in one header.
- **Loop variable:** the counter declared in the for header; it exists only inside the loop.
- **Enhanced for (for-each):** `for (Type item : collection)` visits each element.
- **Nested loop:** a loop inside another loop.
- **Off-by-one error:** looping one time too many or too few.
mistakes:
- Using `i <= s.length()` instead of `i < s.length()`, which goes past the last index.
- Changing a collection while a for-each loop walks over it.
- Reusing the same counter name in nested loops.

@@ break-continue
topics: `break`, `continue`, search flags, labeled break, `while (true)`
terms:
- **break:** leaves the innermost loop immediately.
- **continue:** skips the rest of the current iteration.
- **Flag:** a boolean that records whether something was found.
- **Label:** a name on a loop so `break label;` can leave an outer loop.
- **Sentinel value:** a special input meaning "stop", like `quit`.
mistakes:
- Expecting `break` in an inner loop to leave the outer loop as well.
- Placing `break` outside the `if`, so the loop always stops after one pass.
- Writing `while (true)` with no reachable `break`.

@@ arrays
topics: creating arrays, indexing, `length`, default values, `Arrays.toString`, `Arrays.sort`
terms:
- **Array:** a fixed-size sequence of values of one type.
- **Element:** one value in an array.
- **length:** an array's size (a field, so no parentheses).
- **Default value:** what new array elements start as: 0, false or null.
- **ArrayIndexOutOfBoundsException:** thrown when using an index outside 0 to length - 1.
- **Arrays class:** helpers like `toString`, `sort`, `fill`, `copyOf` and `equals`.
- **Reference:** a variable's link to an object, such as an array.
mistakes:
- Printing an array directly and getting `[I@1b6d3586`. Use `Arrays.toString`.
- Writing `arr.length()` (that's for strings) instead of `arr.length`.
- Expecting `b = a` to copy an array. Use `a.clone()` or `Arrays.copyOf`.
- Comparing arrays with `==` instead of `Arrays.equals`.

@@ two-d-arrays
topics: arrays of arrays, `grid[row][col]`, nested loops, `Arrays.deepToString`, jagged arrays
terms:
- **2D array:** an array whose elements are arrays, used for grids and tables.
- **Row / column:** the first and second index in `grid[row][col]`.
- **Jagged array:** a 2D array whose rows have different lengths.
- **Arrays.deepToString:** prints nested arrays readably.
mistakes:
- Swapping row and column indexes.
- Using `grid.length` for the number of columns. That's `grid[row].length`.
- Printing a 2D array with `Arrays.toString` instead of `deepToString`.

@@ methods
topics: defining methods, parameters, return types, `void`, `static`, print vs return
terms:
- **Method:** a named, reusable block of code.
- **Parameter:** a variable in the method header that receives a value.
- **Argument:** the value passed in a call.
- **Return type:** the type of value a method gives back; `void` means none.
- **return:** hands a value back and ends the method.
- **Method signature:** a method's name and parameter types.
- **static method:** a method that belongs to the class and can be called without an object.
mistakes:
- Printing a result instead of returning it, then trying to use it in a calculation.
- "missing return statement": some path through a non-void method doesn't return.
- Calling an instance method from `static main` without an object.
- Writing code after a `return`, which never runs.

@@ overloading-and-scope
topics: overloading, scope, pass-by-value, varargs
terms:
- **Overloading:** several methods with the same name and different parameter lists.
- **Scope:** the region of code where a variable exists.
- **Local variable:** a variable declared inside a method or block.
- **Pass-by-value:** Java passes copies of arguments; for objects, a copy of the reference.
- **Varargs:** a parameter like `int... nums` that accepts any number of arguments as an array.
mistakes:
- Trying to overload by return type alone.
- Using a variable outside the block where it was declared.
- Expecting a method to change the caller's primitive variable.
- Reassigning an array parameter and expecting the caller's array to change.

@@ recursion
topics: base case, recursive case, the call stack, `StackOverflowError`, divide and conquer
terms:
- **Recursion:** a method calling itself on a smaller version of the problem.
- **Base case:** the condition where the method answers without recursing.
- **Recursive case:** the part that calls the method again with a smaller input.
- **Call stack:** the chain of method calls waiting to finish.
- **StackOverflowError:** thrown when calls go too deep, usually because a base case is missing.
- **Divide and conquer:** splitting a problem into parts, solving each, and combining the results.
mistakes:
- Missing or unreachable base case.
- Calling `f(n)` instead of `f(n - 1)`, so the problem never shrinks.
- Forgetting to `return` the recursive call's result.

@@ classes-and-objects
topics: classes, objects, fields, instance methods, `new`, references, `null`, `toString`
terms:
- **Class:** a blueprint that defines a new type.
- **Object (instance):** one value created from a class with `new`.
- **Field (instance variable):** data that each object stores.
- **Instance method:** a method called on an object, which can use its fields.
- **Reference:** a variable's pointer to an object.
- **null:** a reference that points to nothing.
- **NullPointerException:** thrown when using a null reference.
- **toString():** the method Java calls to turn an object into text.
mistakes:
- Calling a method on a variable that is still `null`.
- Expecting `b = a` to copy an object; both names refer to the same object.
- Declaring two public classes in one file.
- Forgetting `public` on `toString()`.

@@ constructors
topics: constructors, `this`, overloaded constructors, `this(...)` chaining, validation
terms:
- **Constructor:** special code that initialises a new object; it has the class's name and no return type.
- **this:** a reference to the current object.
- **Default constructor:** the empty constructor Java adds only when a class declares none.
- **Constructor chaining:** one constructor calling another with `this(...)`.
mistakes:
- Writing `name = name;` instead of `this.name = name;`.
- Giving a constructor a return type such as `void`, which turns it into a method.
- Calling `new Dog()` after defining only `Dog(String name)`.
- Putting `this(...)` anywhere other than the first line.

@@ encapsulation
topics: `private` fields, access modifiers, getters and setters, validation, immutability
terms:
- **Encapsulation:** hiding an object's data and controlling access through methods.
- **Access modifier:** `private`, package-private (none), `protected` or `public`.
- **Getter / setter:** methods that read / change a field.
- **Invariant:** a rule an object always keeps true, like "balance is never negative".
- **Immutable object:** an object whose state can't change after construction.
mistakes:
- Making fields public, so any code can put the object into an invalid state.
- Adding a setter for every field by reflex.
- Setters that don't validate their input.

@@ static-members
topics: static fields, static methods, constants, utility classes
terms:
- **static field:** one shared value that belongs to the class.
- **static method:** a method called on the class, with no `this`.
- **Constant:** a `static final` value, named in UPPER_SNAKE_CASE.
- **Utility class:** a class of static helper methods, like `Math`.
mistakes:
- Using an instance field inside a static method.
- Making everything static to avoid creating objects.
- Expecting each object to have its own copy of a static field.

@@ inheritance
topics: `extends`, `super`, `@Override`, `protected`, `Object`, single inheritance
terms:
- **Inheritance:** a class reusing and extending another with `extends`.
- **Superclass / subclass:** the parent / the child class.
- **Override:** a subclass redefining an inherited method.
- **super:** calls the parent's constructor (`super(...)`) or methods (`super.m()`).
- **@Override:** asks the compiler to confirm a method really overrides one.
- **protected:** visible to subclasses and the same package.
- **Object:** the class every class ultimately extends.
mistakes:
- Forgetting `super(...)` when the parent has no no-argument constructor.
- Misspelling an overridden method without `@Override`, silently creating a new method.
- Using inheritance for "has a" relationships instead of composition.

@@ polymorphism
topics: parent-type variables, dynamic dispatch, `instanceof` patterns, casting
terms:
- **Polymorphism:** one variable type referring to objects of many subclasses.
- **Dynamic dispatch:** the object's actual class decides which overridden method runs.
- **Declared type / actual type:** the variable's type / the object's real class.
- **Upcast / downcast:** treating an object as its parent type / converting back to a subclass.
- **instanceof:** checks whether an object is of a type; `x instanceof Dog d` also casts.
- **ClassCastException:** thrown by an invalid downcast.
mistakes:
- Downcasting without checking the type first.
- Calling a subclass-only method on a parent-type variable.
- Long `instanceof` chains where an overridden method would be simpler.

@@ abstract-and-interfaces
topics: abstract classes, abstract methods, interfaces, `implements`, default methods
terms:
- **Abstract class:** a class that can't be instantiated and may declare abstract methods.
- **Abstract method:** a method without a body that subclasses must implement.
- **Interface:** a set of methods a class promises to provide.
- **implements:** declares that a class fulfils an interface.
- **Default method:** an interface method with a body.
mistakes:
- Trying to `new` an abstract class or interface.
- Forgetting `public` on methods that implement an interface.
- Using an abstract class where an interface would allow more flexibility.

@@ enums-and-records
topics: enums, enum fields and methods, `values()`, records, compact constructors
terms:
- **Enum:** a type with a fixed set of named constants.
- **values():** returns all the constants of an enum.
- **Record:** a concise, immutable data class with generated constructor, accessors, `equals`, `hashCode` and `toString`.
- **Accessor:** a record's method for reading a component, like `p.x()`.
- **Compact constructor:** a record constructor without a parameter list, used for validation.
mistakes:
- Using strings or ints where an enum would catch typos at compile time.
- Calling `getX()` on a record. The accessor is `x()`.
- Trying to change a record's field after creation.

@@ stringbuilder-and-wrappers
topics: `StringBuilder`, wrapper classes, autoboxing, `parseInt`, the `Integer` == trap
terms:
- **StringBuilder:** a changeable string for building text efficiently.
- **Wrapper class:** an object version of a primitive, such as `Integer` or `Double`.
- **Autoboxing / unboxing:** automatic conversion between primitives and wrappers.
- **Integer cache:** Java reuses Integer objects from -128 to 127.
mistakes:
- Comparing `Integer` objects with `==`. Use `equals` or compare as ints.
- Concatenating strings in a large loop instead of using a StringBuilder.
- Unboxing a `null` wrapper, which throws NullPointerException.

@@ exceptions
topics: `try`/`catch`/`finally`, checked vs unchecked, `throw`, `throws`, custom exceptions, try-with-resources
terms:
- **Exception:** an object signalling that something went wrong at runtime.
- **try / catch:** run code and handle specific exceptions.
- **finally:** a block that always runs, used for cleanup.
- **throw / throws:** raise an exception / declare that a method may throw one.
- **Checked exception:** must be caught or declared, like `IOException`.
- **Unchecked exception:** a `RuntimeException`, usually a programming bug.
- **Stack trace:** the list of method calls shown when an exception isn't caught.
- **try-with-resources:** closes resources declared in `try (...)` automatically.
mistakes:
- Catching `Exception` everywhere and hiding real bugs.
- An empty `catch` block that silently swallows errors.
- Throwing exceptions without a helpful message.
- Forgetting to close files and connections. Use try-with-resources.

@@ generics
topics: type parameters, generic classes and methods, the diamond, bounded types, wildcards
terms:
- **Generics:** classes and methods that take type parameters, like `List<String>`.
- **Type parameter:** a placeholder type such as `T` in `class Box<T>`.
- **Diamond (`<>`):** lets the compiler infer type arguments: `new ArrayList<>()`.
- **Bounded type:** a type parameter with a limit, like `<T extends Comparable<T>>`.
- **Wildcard:** `?` for an unknown type, as in `List<? extends Number>`.
mistakes:
- Using raw types like `List` instead of `List<String>`, which loses type checking.
- Expecting `List<Integer>` to be accepted where `List<Number>` is required.
- Trying to use primitives as type arguments: `List<int>`.

@@ lists
topics: `ArrayList`, `List.of`, add/get/set/remove, iteration, `removeIf`, `ArrayList` vs `LinkedList`
terms:
- **List:** an ordered collection that allows duplicates.
- **ArrayList:** a resizable list backed by an array.
- **List.of:** creates an unmodifiable list.
- **Iterator:** an object that walks a collection and can remove items safely.
- **ConcurrentModificationException:** thrown when a collection changes while being iterated.
mistakes:
- Calling `add` on a `List.of(...)` list.
- `remove(1)` on a `List<Integer>` removes index 1, not the value 1.
- Removing items inside a for-each loop over the same list.
- Declaring variables as `ArrayList` instead of the `List` interface.

@@ sets-and-maps
topics: `HashSet`, `TreeSet`, `HashMap`, `TreeMap`, `getOrDefault`, `merge`, `equals` and `hashCode`
terms:
- **Set:** a collection of unique values.
- **Map:** a collection of key-value pairs with unique keys.
- **HashSet / HashMap:** fast, unordered implementations.
- **TreeSet / TreeMap:** sorted implementations.
- **LinkedHashSet / LinkedHashMap:** keep insertion order.
- **getOrDefault / merge:** read with a fallback / combine a new value with an existing one.
- **hashCode:** a number used by hash collections to locate objects quickly.
mistakes:
- Calling `map.get(key)` and using the result without checking for `null`.
- Putting your own objects in a HashSet without overriding `equals` and `hashCode`.
- Expecting a `HashMap` to keep insertion or sorted order.

@@ sorting-and-comparators
topics: `Comparable`, `compareTo`, `Comparator.comparing`, `thenComparing`, `reversed`
terms:
- **Comparable:** an interface giving a class its natural order through `compareTo`.
- **compareTo:** returns negative, zero or positive to order two objects.
- **Comparator:** a separate object that compares two values.
- **Key extractor:** a function that picks the value to sort by, like `Person::age`.
- **Stable sort:** a sort that keeps the original order of equal elements.
mistakes:
- Writing `return a - b;` in `compareTo`, which can overflow.
- Trying to sort an unmodifiable `List.of(...)` in place.
- Forgetting `.reversed()` for highest-first order.

@@ lambdas
topics: lambda syntax, functional interfaces, `Function`, `Predicate`, method references
terms:
- **Lambda:** a short anonymous function: `(params) -> expression`.
- **Functional interface:** an interface with exactly one abstract method.
- **Function / Predicate / Consumer / Supplier:** built-in functional interfaces for common shapes.
- **Method reference:** shorthand for a lambda that calls one method, like `String::length`.
- **Effectively final:** a local variable that's never reassigned, so lambdas can use it.
mistakes:
- Changing a captured local variable inside a lambda.
- Writing a block-bodied lambda without `return`.
- Using a lambda where the target type isn't a functional interface.

@@ streams
topics: `stream()`, `filter`, `map`, `sorted`, `reduce`, `collect`, `groupingBy`
terms:
- **Stream:** a pipeline that processes a sequence of elements.
- **Intermediate operation:** a lazy step such as `filter` or `map` that returns a stream.
- **Terminal operation:** a step such as `toList` or `count` that produces a result and runs the pipeline.
- **Collector:** a recipe for gathering stream results, such as `groupingBy` or `joining`.
- **IntStream:** a stream of primitive ints with `sum`, `average` and `range`.
mistakes:
- Forgetting the terminal operation, so nothing runs.
- Reusing a stream after it has been consumed.
- Changing outside variables from inside a stream.

@@ optional
topics: `Optional`, `orElse`, `map`, `ifPresent`, null-safety helpers
terms:
- **Optional:** a container that holds a value or is empty.
- **Optional.ofNullable:** wraps a value that might be null.
- **orElse / orElseGet / orElseThrow:** get the value or fall back.
- **Objects.requireNonNull:** fails fast with a clear message when a value is null.
mistakes:
- Calling `get()` without checking that a value is present.
- Using Optional for fields or parameters.
- Returning `null` from a method that returns Optional.

@@ modern-java-features
topics: `var`, text blocks, pattern matching for `instanceof`, records, sealed classes
terms:
- **Text block:** a multi-line string written with triple quotes.
- **Pattern matching:** testing a type and binding a variable in one step: `o instanceof String s`.
- **Sealed class / interface:** a type that lists exactly which classes may extend it.
- **permits:** the clause naming a sealed type's allowed subclasses.
mistakes:
- Using `var` where the type isn't obvious to a reader.
- Using a pattern variable outside the scope where the match is guaranteed.
- Forgetting that subclasses of a sealed type must be final, sealed or non-sealed.

@@ files-and-io
topics: `Path`, `Files.readString`/`writeString`, `Files.lines`, buffered readers, CSV parsing
terms:
- **Path:** names a file or folder.
- **Files:** utility methods for reading, writing and managing files.
- **IOException:** the checked exception for input/output failures.
- **BufferedReader / BufferedWriter:** read and write text efficiently, line by line.
- **CSV:** comma-separated values, a simple text format for tables.
mistakes:
- Not handling or declaring `IOException`.
- Forgetting to close streams from `Files.lines`. Use try-with-resources.
- Reading huge files entirely into memory instead of line by line.
- Splitting quoted CSV values with a plain `split(",")`.

@@ concurrency
topics: threads, `ExecutorService`, futures, race conditions, `synchronized`, atomics, `CompletableFuture`
terms:
- **Thread:** an independent path of execution.
- **ExecutorService:** a managed pool of threads that runs submitted tasks.
- **Future:** a handle to a result that will be available later.
- **Race condition:** a bug where the result depends on how threads interleave.
- **synchronized:** lets only one thread at a time run a block for a given lock.
- **Atomic variable:** a variable with thread-safe single operations, like `AtomicInteger`.
- **CompletableFuture:** a future you can chain asynchronous steps onto.
mistakes:
- Calling `run()` instead of `start()` on a thread.
- Sharing mutable data between threads without synchronization.
- Forgetting to `shutdown()` an executor.
- Using `Thread.sleep` to hide a race condition.

@@ algorithms-and-big-o
topics: Big-O, choosing collections, binary search, merge sort, operation costs
terms:
- **Algorithm:** a step-by-step method for solving a problem.
- **Big-O notation:** how running time grows with input size.
- **Binary search:** finds a value in sorted data by halving the range each step: O(log n).
- **Merge sort:** a divide-and-conquer sort running in O(n log n).
- **Amortised cost:** the average cost per operation over many operations.
mistakes:
- Calling `list.contains` inside a loop over large data. Use a HashSet.
- Running binary search on unsorted data.
- Optimising before measuring.

@@ capstone
topics: records, enums, encapsulation, exceptions, Optional and streams in one program
terms:
- **Capstone project:** a project that combines everything you've learned.
- **Domain model:** the classes that represent the real-world things a program deals with.
- **Build tool:** software such as Maven or Gradle that compiles, tests and packages projects.
- **Unit test:** a small automated check of one piece of code, usually written with JUnit.
mistakes:
- Putting all the logic in `main` instead of small classes and methods.
- Exposing internal collections that callers can modify.
- Using exceptions for normal control flow instead of expected checks.
