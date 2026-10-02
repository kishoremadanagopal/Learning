@@@ part
id: 7
title: Advanced Java
level: Advanced
blurb: Read and write files, run work in parallel safely, reason about performance with Big-O, and build a complete application.

@@@ lesson
id: files-and-io
title: Files and I/O
minutes: 15
summary: Read and write text files with java.nio.file, process lines, and parse CSV-style data.
---
Programs often load data from files and save results back. The modern API lives in **`java.nio.file`**: `Path` names a file and `Files` does the work. In this sandbox, files are stored in your browser, so the examples really run.

### Writing and reading a whole file

```java
import java.io.IOException;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Path notes = Path.of("notes.txt");
        Files.writeString(notes, "first line\nsecond line\n");
        Files.writeString(notes, "third line\n", StandardOpenOption.APPEND);

        String all = Files.readString(notes);
        System.out.print(all);

        List<String> lines = Files.readAllLines(notes);
        System.out.println(lines.size() + " lines, first: " + lines.get(0));
        System.out.println("exists: " + Files.exists(notes) + ", size: " + Files.size(notes) + " bytes");
    }
}
```

File operations throw the **checked** `IOException`, so `main` declares `throws IOException`. In a real application you'd catch it and show a helpful message.

### Processing lines one at a time

For large files, don't load everything at once. `Files.lines` streams lines lazily; use try-with-resources so the file is closed:

```java
import java.io.IOException;
import java.nio.file.*;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) throws IOException {
        Path log = Path.of("app.log");
        Files.writeString(log, "INFO start\nERROR disk full\nINFO retry\nERROR timeout\n");

        try (Stream<String> lines = Files.lines(log)) {
            lines.filter(l -> l.startsWith("ERROR"))
                 .map(l -> l.substring(6))
                 .forEach(System.out::println);
        }
    }
}
```

### Buffered readers and writers

`BufferedReader` and `BufferedWriter` give fine-grained control, and work with any source, including text in memory, which makes them easy to test:

```java
import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Path out = Path.of("report.txt");
        try (BufferedWriter w = Files.newBufferedWriter(out)) {
            for (int i = 1; i <= 3; i++) {
                w.write("Row " + i);
                w.newLine();
            }
        }

        try (BufferedReader r = Files.newBufferedReader(out)) {
            String line;
            while ((line = r.readLine()) != null) {
                System.out.println("> " + line);
            }
        }

        BufferedReader fromText = new BufferedReader(new StringReader("a\nb"));
        System.out.println(fromText.readLine() + fromText.readLine());
    }
}
```

### Parsing CSV data

```java
import java.io.IOException;
import java.nio.file.*;
import java.util.*;

record Sale(String product, int qty, double price) {
    double total() { return qty * price; }
}

public class Main {
    public static void main(String[] args) throws IOException {
        Path csv = Path.of("sales.csv");
        Files.writeString(csv, """
            product,qty,price
            pen,10,1.50
            book,2,12.99
            pen,4,1.50
            """);

        List<Sale> sales = new ArrayList<>();
        List<String> lines = Files.readAllLines(csv);
        for (String line : lines.subList(1, lines.size())) {      // skip the header
            String[] f = line.split(",");
            sales.add(new Sale(f[0], Integer.parseInt(f[1]), Double.parseDouble(f[2])));
        }

        Map<String, Double> byProduct = new TreeMap<>();
        for (Sale s : sales) {
            byProduct.merge(s.product(), s.total(), Double::sum);
        }
        byProduct.forEach((p, t) -> System.out.printf("%-5s %6.2f%n", p, t));
    }
}
```

Simple `split(",")` breaks on values that contain commas inside quotes. For real CSV files, use a library such as OpenCSV or Apache Commons CSV.

### Paths and directories

```java
import java.io.IOException;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Path dir = Path.of("data", "2026");
        Files.createDirectories(dir);
        Path file = dir.resolve("summary.txt");
        Files.writeString(file, "ok");
        System.out.println(file + " -> " + file.getFileName() + " in " + file.getParent());
        try (var listing = Files.list(dir)) {
            listing.forEach(p -> System.out.println("found " + p.getFileName()));
        }
        Files.delete(file);
        System.out.println(Files.exists(file));
    }
}
```

:::exercise Count words in a file
Write `static int countWords(Path file) throws IOException` that reads the file and returns the number of words (split each line on whitespace and ignore blank lines). The checker writes a test file and calls your method.
```java starter
import java.io.IOException;
import java.nio.file.*;

public class Main {
    static int countWords(Path file) throws IOException {
        return 0;
    }

    public static void main(String[] args) throws IOException {
        Path p = Path.of("poem.txt");
        Files.writeString(p, "roses are red\nviolets are blue\n");
        System.out.println(countWords(p));
    }
}
```
```java check
java.nio.file.Path p = java.nio.file.Path.of("check-words.txt");
java.nio.file.Files.writeString(p, "one two  three\n\n   four\nfive six\n");
eq(6, call("countWords", p), "countWords on a file with 6 words");
java.nio.file.Files.writeString(p, "\n\n");
eq(0, call("countWords", p), "countWords on a file with only blank lines");
```
```java solution
import java.io.IOException;
import java.nio.file.*;

public class Main {
    static int countWords(Path file) throws IOException {
        int count = 0;
        for (String line : Files.readAllLines(file)) {
            if (!line.isBlank()) {
                count += line.trim().split("\\s+").length;
            }
        }
        return count;
    }

    public static void main(String[] args) throws IOException {
        Path p = Path.of("poem.txt");
        Files.writeString(p, "roses are red\nviolets are blue\n");
        System.out.println(countWords(p));
    }
}
```
hint: Loop over Files.readAllLines(file). Skip blank lines; for the others add line.trim().split("\\s+").length.
:::

:::quiz
? Why does `Files.readString` need `throws IOException` or a try/catch?
+ IOException is a checked exception
- It always fails
- Files is a deprecated class
= The compiler requires checked exceptions to be handled or declared.

? Why use try-with-resources with `Files.lines(...)`?
+ So the file is closed when you're done
- It makes reading faster
- It's required to filter lines
= The stream holds the file open until it's closed.
:::

@@@ lesson
id: concurrency
title: Concurrency basics
minutes: 18
summary: Run tasks in parallel with threads and executors, avoid race conditions with synchronized and atomics, and compose async work.
---
**Concurrency** means several tasks making progress at the same time: downloading while the UI stays responsive, or splitting heavy work across processor cores.

### Threads

A **thread** is an independent path of execution. You give it a `Runnable` (often a lambda) and `start()` it:

```java
public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread worker = new Thread(() -> {
            for (int i = 1; i <= 3; i++) {
                System.out.println("worker step " + i);
            }
        });
        worker.start();                  // runs alongside main
        System.out.println("main keeps going");
        worker.join();                   // wait for it to finish
        System.out.println("worker finished");
    }
}
```

The order of output from different threads isn't guaranteed. Call `start()`, not `run()`; `run()` would just execute the code on the current thread.

### Executors and futures

Creating threads by hand is low-level. An **ExecutorService** manages a pool of threads; you submit tasks and get back **Futures** for their results:

```java
import java.util.*;
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(4);
        List<Future<Long>> results = new ArrayList<>();
        for (int chunk = 0; chunk < 4; chunk++) {
            final long start = chunk * 250_000L;
            results.add(pool.submit(() -> {
                long sum = 0;
                for (long n = start; n < start + 250_000; n++) {
                    sum += n;
                }
                return sum;
            }));
        }
        long total = 0;
        for (Future<Long> f : results) {
            total += f.get();            // waits for each task's result
        }
        pool.shutdown();
        System.out.println("Sum 0..999,999 = " + total);
    }
}
```

Always `shutdown()` an executor when you're done; its threads otherwise keep the program alive.

### Race conditions

When threads **share** changeable data, updates can interleave and get lost. `count++` is really three steps (read, add, write), and two threads can read the same old value:

```java
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    static int unsafeCount = 0;
    static int safeCount = 0;
    static final AtomicInteger atomicCount = new AtomicInteger();

    static synchronized void safeIncrement() {
        safeCount++;
    }

    public static void main(String[] args) throws InterruptedException {
        List<Thread> threads = new ArrayList<>();
        for (int t = 0; t < 4; t++) {
            Thread th = new Thread(() -> {
                for (int i = 0; i < 10_000; i++) {
                    unsafeCount++;
                    safeIncrement();
                    atomicCount.incrementAndGet();
                }
            });
            threads.add(th);
            th.start();
        }
        for (Thread th : threads) {
            th.join();
        }
        System.out.println("synchronized: " + safeCount);
        System.out.println("atomic:       " + atomicCount.get());
        System.out.println("unsafe:       " + unsafeCount + " (may be less than 40000 on a multi-core JVM)");
    }
}
```

- `synchronized` lets only one thread at a time run the method (or block) for a given lock.
- **Atomic** classes (`AtomicInteger`, `AtomicLong`) do single updates safely without locks.
- In the browser, Java threads take turns on one core, so the race rarely shows up here. On a real multi-core machine, the unsafe count is often wrong.

### Thread-safe collections

`ArrayList` and `HashMap` aren't safe for concurrent changes. Use `ConcurrentHashMap`, `CopyOnWriteArrayList`, or a `BlockingQueue` for producer/consumer setups:

```java
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        ConcurrentHashMap<String, Integer> hits = new ConcurrentHashMap<>();
        ExecutorService pool = Executors.newFixedThreadPool(3);
        for (String page : new String[]{"home", "about", "home", "home", "about"}) {
            pool.submit(() -> hits.merge(page, 1, Integer::sum));
        }
        pool.shutdown();
        pool.awaitTermination(5, TimeUnit.SECONDS);
        System.out.println(new java.util.TreeMap<>(hits));
    }
}
```

### CompletableFuture: composing async work

`CompletableFuture` chains steps that run asynchronously, without blocking until you need the result:

```java
import java.util.concurrent.*;

public class Main {
    static String fetchUser(int id) {
        sleep(100);
        return "user" + id;
    }

    static int fetchScore(String user) {
        sleep(100);
        return user.length() * 10;
    }

    static void sleep(long ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public static void main(String[] args) {
        CompletableFuture<String> pipeline = CompletableFuture
            .supplyAsync(() -> fetchUser(7))
            .thenApply(Main::fetchScore)
            .thenApply(score -> "score=" + score);

        CompletableFuture<String> other = CompletableFuture.supplyAsync(() -> fetchUser(8));
        System.out.println(pipeline.join() + " " + other.join());
    }
}
```

### Rules of thumb

- Prefer executors over raw threads, and immutable data over shared mutable data.
- Protect shared mutable state with `synchronized`, locks or atomic classes.
- Never call `Thread.sleep` to "fix" a race condition.
- Java 21 added **virtual threads** for handling huge numbers of concurrent tasks cheaply.

:::exercise Parallel sum
Write `static long parallelSum(int[] nums, int parts)` that splits the array into `parts` chunks, sums each chunk in a task on an `ExecutorService`, and adds up the results. Shut the executor down before returning.
```java starter
import java.util.*;
import java.util.concurrent.*;

public class Main {
    static long parallelSum(int[] nums, int parts) throws Exception {
        long sum = 0;
        for (int n : nums) {
            sum += n;
        }
        return sum;
    }

    public static void main(String[] args) throws Exception {
        int[] data = new int[1000];
        for (int i = 0; i < data.length; i++) {
            data[i] = i + 1;
        }
        System.out.println(parallelSum(data, 4));
    }
}
```
```java check
int[] data = new int[1000];
for (int i = 0; i < data.length; i++) data[i] = i + 1;
eq(500500L, call("parallelSum", data, 4), "parallelSum(1..1000, 4)");
eq(500500L, call("parallelSum", data, 3), "parallelSum(1..1000, 3)");
eq(6L, call("parallelSum", new int[]{1, 2, 3}, 5), "parallelSum({1, 2, 3}, 5)");
sourceHas("submit", "Submit the chunk sums as tasks to an ExecutorService.");
sourceHas("shutdown", "Shut the executor down.");
```
```java solution
import java.util.*;
import java.util.concurrent.*;

public class Main {
    static long parallelSum(int[] nums, int parts) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(parts);
        try {
            List<Future<Long>> futures = new ArrayList<>();
            int chunk = (nums.length + parts - 1) / parts;
            for (int start = 0; start < nums.length; start += chunk) {
                final int from = start;
                final int to = Math.min(start + chunk, nums.length);
                futures.add(pool.submit(() -> {
                    long sum = 0;
                    for (int i = from; i < to; i++) {
                        sum += nums[i];
                    }
                    return sum;
                }));
            }
            long total = 0;
            for (Future<Long> f : futures) {
                total += f.get();
            }
            return total;
        } finally {
            pool.shutdown();
        }
    }

    public static void main(String[] args) throws Exception {
        int[] data = new int[1000];
        for (int i = 0; i < data.length; i++) {
            data[i] = i + 1;
        }
        System.out.println(parallelSum(data, 4));
    }
}
```
hint: Compute a chunk size of (nums.length + parts - 1) / parts. For each chunk, submit a lambda that sums from..to and returns a Long. Collect the Futures, add up f.get(), and call shutdown() in a finally block.
:::

:::quiz
? What's the difference between `thread.start()` and `thread.run()`?
+ `start()` runs the code on a new thread; `run()` runs it on the current thread
- They are the same
- `run()` starts two threads
= Only `start()` creates concurrency.

? Why can `count++` from several threads lose updates?
+ It's a read, an add and a write that can interleave
- Integers can't be shared
- Threads can't change static fields
= Two threads may read the same old value and both write old + 1.

? What should you call when you're done with an ExecutorService?
+ shutdown()
- stop()
- Nothing
= Otherwise its threads can keep the program running.
:::

@@@ lesson
id: algorithms-and-big-o
title: Algorithms and Big-O
minutes: 18
summary: Measure how code scales, pick the right data structure, and implement binary search and merge sort.
---
Two programs can produce the same answer while one takes milliseconds and the other takes hours. **Big-O notation** describes how running time grows as the input size `n` grows:

| Big-O | Name | Example | 1,000 → 1,000,000 items |
|---|---|---|---|
| O(1) | constant | `HashMap.get`, array index | same time |
| O(log n) | logarithmic | binary search, `TreeMap.get` | 10 steps → 20 steps |
| O(n) | linear | loop over a list, `ArrayList.contains` | 1,000× slower |
| O(n log n) | linearithmic | `Collections.sort`, merge sort | ~2,000× slower |
| O(n²) | quadratic | nested loops over the same data | 1,000,000× slower |

![Line chart of steps against number of items: O(1) and O(log n) stay almost flat, O(n) grows steadily, O(n log n) faster, and O(n squared) shoots up](figures/big-o.svg)

### The right data structure is the biggest win

`list.contains(x)` checks elements one by one: O(n). `set.contains(x)` uses hashing: O(1) on average. Watch the difference:

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        int n = 20_000;
        List<Integer> list = new ArrayList<>();
        for (int i = 0; i < n; i++) list.add(i);
        Set<Integer> set = new HashSet<>(list);

        long t = System.nanoTime();
        int hits = 0;
        for (int i = n - 2_000; i < n; i++) if (list.contains(i)) hits++;
        long listMs = (System.nanoTime() - t) / 1_000_000;

        t = System.nanoTime();
        for (int i = n - 2_000; i < n; i++) if (set.contains(i)) hits++;
        long setMs = (System.nanoTime() - t) / 1_000_000;

        System.out.println("list: " + listMs + " ms, set: " + setMs + " ms, hits: " + hits);
    }
}
```

### Spotting O(n²)

A loop inside a loop over the same data is the classic warning sign. A set often removes the inner loop:

```java
import java.util.*;

public class Main {
    static boolean hasDuplicateSlow(int[] a) {          // O(n²)
        for (int i = 0; i < a.length; i++) {
            for (int j = i + 1; j < a.length; j++) {
                if (a[i] == a[j]) return true;
            }
        }
        return false;
    }

    static boolean hasDuplicateFast(int[] a) {          // O(n)
        Set<Integer> seen = new HashSet<>();
        for (int x : a) {
            if (!seen.add(x)) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        int[] data = {5, 3, 8, 1, 3};
        System.out.println(hasDuplicateSlow(data) + " " + hasDuplicateFast(data));
    }
}
```

### Binary search: O(log n)

On **sorted** data, compare with the middle element and discard half each step. A million items take at most 20 comparisons:

```java
import java.util.Arrays;

public class Main {
    static int binarySearch(int[] a, int target) {
        int low = 0, high = a.length - 1;
        while (low <= high) {
            int mid = (low + high) >>> 1;        // avoids overflow for huge arrays
            if (a[mid] == target) return mid;
            if (a[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] sorted = new int[143];
        for (int i = 0; i < sorted.length; i++) sorted[i] = i * 7;
        System.out.println(binarySearch(sorted, 693) + " " + binarySearch(sorted, 50));
        System.out.println(Arrays.binarySearch(sorted, 693));    // the library version
    }
}
```

### Merge sort: O(n log n)

Split the array in half, sort each half recursively, then merge the two sorted halves. It's a classic **divide and conquer** algorithm:

```java
import java.util.Arrays;

public class Main {
    static int[] mergeSort(int[] a) {
        if (a.length <= 1) return a;
        int mid = a.length / 2;
        int[] left = mergeSort(Arrays.copyOfRange(a, 0, mid));
        int[] right = mergeSort(Arrays.copyOfRange(a, mid, a.length));

        int[] merged = new int[a.length];
        int i = 0, j = 0, k = 0;
        while (i < left.length && j < right.length) {
            merged[k++] = (left[i] <= right[j]) ? left[i++] : right[j++];
        }
        while (i < left.length) merged[k++] = left[i++];
        while (j < right.length) merged[k++] = right[j++];
        return merged;
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(mergeSort(new int[]{38, 27, 43, 3, 9, 82, 10})));
    }
}
```

In real code, use `Arrays.sort` or `Collections.sort`, which are highly optimised. Knowing how sorting works trains your algorithmic thinking, and it's a favourite interview topic.

### Costs of common operations

| Operation | ArrayList | LinkedList | HashMap / HashSet | TreeMap / TreeSet |
|---|---|---|---|---|
| get by index / key | O(1) | O(n) | O(1) | O(log n) |
| contains | O(n) | O(n) | O(1) | O(log n) |
| add at end | O(1)* | O(1) | O(1) | O(log n) |
| insert / remove at front | O(n) | O(1) | n/a | n/a |

\* amortised: occasionally the backing array is resized.

:::exercise Two sum
Write `static int[] twoSum(int[] nums, int target)` returning the indexes `{i, j}` (with `i < j`) of two numbers that add up to `target`, or an empty array if there are none. Make it **O(n)** with a `HashMap` from value to index.
```java starter
import java.util.*;

public class Main {
    static int[] twoSum(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[]{i, j};
                }
            }
        }
        return new int[0];
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(twoSum(new int[]{2, 7, 11, 15}, 9)));
    }
}
```
```java check
eq(new int[]{0, 1}, call("twoSum", new int[]{2, 7, 11, 15}, 9), "twoSum({2, 7, 11, 15}, 9)");
eq(new int[]{1, 2}, call("twoSum", new int[]{3, 2, 4}, 6), "twoSum({3, 2, 4}, 6)");
eq(new int[]{0, 1}, call("twoSum", new int[]{5, 5}, 10), "twoSum({5, 5}, 10)");
eq(new int[0], call("twoSum", new int[]{1, 2, 3}, 100), "twoSum({1, 2, 3}, 100)");
String body = source().substring(source().indexOf("twoSum"));
check(body.split("for \\(", -1).length - 1 <= 1, "Use a single loop with a HashMap, not nested loops.");
sourceHas("Map", "Use a HashMap from value to index.");
```
```java solution
import java.util.*;

public class Main {
    static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int j = 0; j < nums.length; j++) {
            Integer i = seen.get(target - nums[j]);
            if (i != null) {
                return new int[]{i, j};
            }
            seen.put(nums[j], j);
        }
        return new int[0];
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(twoSum(new int[]{2, 7, 11, 15}, 9)));
    }
}
```
hint: Loop once. For each index j, look up target - nums[j] in a map of value → index. If it's there, return {thatIndex, j}; otherwise put nums[j] → j.
:::

:::exercise Insertion sort
Implement `static void insertionSort(int[] a)` that sorts the array in place without `Arrays.sort`: take each element and shift it left until it's in position.
```java starter
import java.util.Arrays;

public class Main {
    static void insertionSort(int[] a) {

    }

    public static void main(String[] args) {
        int[] data = {5, 2, 9, 1, 5, 6};
        insertionSort(data);
        System.out.println(Arrays.toString(data));
    }
}
```
```java check
java.util.Random rnd = new java.util.Random(42);
for (int trial = 0; trial < 20; trial++) {
    int[] a = new int[rnd.nextInt(15)];
    for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(101) - 50;
    int[] expected = a.clone();
    java.util.Arrays.sort(expected);
    int[] original = a.clone();
    call("insertionSort", (Object) a);
    eq(expected, a, "insertionSort(" + java.util.Arrays.toString(original) + ")");
}
sourceLacks("Arrays.sort", "Don't use Arrays.sort.");
```
```java solution
import java.util.Arrays;

public class Main {
    static void insertionSort(int[] a) {
        for (int i = 1; i < a.length; i++) {
            int value = a[i];
            int j = i - 1;
            while (j >= 0 && a[j] > value) {
                a[j + 1] = a[j];
                j--;
            }
            a[j + 1] = value;
        }
    }

    public static void main(String[] args) {
        int[] data = {5, 2, 9, 1, 5, 6};
        insertionSort(data);
        System.out.println(Arrays.toString(data));
    }
}
```
hint: For each i from 1, remember value = a[i]. Move bigger elements to the left of it one step right (a[j + 1] = a[j]) while j >= 0 && a[j] > value, then put value at a[j + 1].
:::

:::quiz
? What's the Big-O of `HashSet.contains`?
+ O(1) on average
- O(n)
- O(log n)
= Hashing jumps straight to the right bucket.

? What does binary search require?
+ Sorted data
- A HashMap
- Unique values
= Discarding half only works if you know which side the target is on.

? Two nested loops over the same n items are usually…
- O(n)
+ O(n²)
- O(2n)
= For each of n items you do up to n more steps.
:::

@@@ lesson
id: capstone
title: "Capstone: a library system"
minutes: 30
summary: Combine records, enums, classes, collections, streams, exceptions and Optional into one complete program, then plan your next steps.
---
Time to put everything together. This program manages a small library: books, members and loans. Read it, run it, and change things; every part uses something from an earlier lesson.

```java
import java.util.*;
import java.util.stream.*;

enum Genre { FICTION, SCIENCE, HISTORY, TECH }

record Book(String isbn, String title, String author, Genre genre, int year) {
    Book {
        if (isbn == null || isbn.isBlank()) throw new IllegalArgumentException("ISBN required");
        if (year < 1450 || year > 2026) throw new IllegalArgumentException("Bad year: " + year);
    }
}

record Member(int id, String name) { }

class LibraryException extends Exception {
    LibraryException(String message) { super(message); }
}

class Library {
    private final Map<String, Book> books = new LinkedHashMap<>();
    private final Map<Integer, Member> members = new HashMap<>();
    private final Map<String, Integer> loans = new HashMap<>();          // isbn -> member id
    private final List<String> history = new ArrayList<>();

    void addBook(Book b) {
        books.put(b.isbn(), b);
    }

    void addMember(Member m) {
        members.put(m.id(), m);
    }

    void borrow(String isbn, int memberId) throws LibraryException {
        Book book = findBook(isbn).orElseThrow(() -> new LibraryException("No book with ISBN " + isbn));
        if (!members.containsKey(memberId)) throw new LibraryException("Unknown member " + memberId);
        if (loans.containsKey(isbn)) throw new LibraryException("'" + book.title() + "' is already on loan");
        long current = loans.values().stream().filter(id -> id == memberId).count();
        if (current >= 2) throw new LibraryException(members.get(memberId).name() + " already has 2 books");
        loans.put(isbn, memberId);
        history.add(members.get(memberId).name() + " borrowed " + book.title());
    }

    void giveBack(String isbn) throws LibraryException {
        Integer who = loans.remove(isbn);
        if (who == null) throw new LibraryException("That book isn't on loan");
        history.add(members.get(who).name() + " returned " + books.get(isbn).title());
    }

    Optional<Book> findBook(String isbn) {
        return Optional.ofNullable(books.get(isbn));
    }

    List<Book> available() {
        return books.values().stream().filter(b -> !loans.containsKey(b.isbn())).toList();
    }

    Map<Genre, Long> countByGenre() {
        return books.values().stream()
            .collect(Collectors.groupingBy(Book::genre, () -> new EnumMap<>(Genre.class), Collectors.counting()));
    }

    List<Book> search(String text) {
        String q = text.toLowerCase();
        return books.values().stream()
            .filter(b -> b.title().toLowerCase().contains(q) || b.author().toLowerCase().contains(q))
            .sorted(Comparator.comparingInt(Book::year))
            .toList();
    }

    List<String> history() {
        return Collections.unmodifiableList(history);
    }
}

public class Main {
    public static void main(String[] args) {
        Library lib = new Library();
        lib.addBook(new Book("111", "Dune", "Frank Herbert", Genre.FICTION, 1965));
        lib.addBook(new Book("222", "A Brief History of Time", "Stephen Hawking", Genre.SCIENCE, 1988));
        lib.addBook(new Book("333", "Effective Java", "Joshua Bloch", Genre.TECH, 2018));
        lib.addBook(new Book("444", "Clean Code", "Robert C. Martin", Genre.TECH, 2008));
        lib.addMember(new Member(1, "Ana"));
        lib.addMember(new Member(2, "Ben"));

        String[][] actions = {
            {"borrow", "333", "1"}, {"borrow", "111", "1"}, {"borrow", "444", "1"},
            {"borrow", "333", "2"}, {"return", "333"}, {"borrow", "333", "2"}, {"borrow", "999", "2"}
        };
        for (String[] a : actions) {
            try {
                if (a[0].equals("borrow")) lib.borrow(a[1], Integer.parseInt(a[2]));
                else lib.giveBack(a[1]);
            } catch (LibraryException e) {
                System.out.println("Refused: " + e.getMessage());
            }
        }

        System.out.println("\nHistory:");
        lib.history().forEach(h -> System.out.println("  " + h));
        System.out.println("\nAvailable: " + lib.available().stream().map(Book::title).toList());
        System.out.println("By genre:  " + lib.countByGenre());
        System.out.println("Search 'code': " + lib.search("code").stream().map(Book::title).toList());
        System.out.println("Find 222: " + lib.findBook("222").map(Book::title).orElse("not found"));
    }
}
```

### What each part demonstrates

| Feature | Lesson |
|---|---|
| `enum Genre`, `EnumMap` | Enums and records, Sets and maps |
| `record Book` with a compact constructor | Enums and records |
| Custom checked `LibraryException` | Exceptions |
| `private` fields, small public methods | Encapsulation |
| `Optional<Book>` and `orElseThrow` | Optional |
| Streams with `filter`, `sorted`, `groupingBy` | Streams |
| `Comparator.comparingInt` | Sorting with Comparator |
| `Collections.unmodifiableList` | Lists, Encapsulation |

### Your turn

The exercises below extend the system. Each one is self-contained.

:::exercise Overdue fines
Write `static double totalFines(List<Loan> loans, int today)` where `Loan` is the given record. A loan is due 14 days after `borrowedDay`; each day past the due date costs `0.25`, capped at `5.00` per loan. Loans not yet overdue cost nothing.
```java starter
import java.util.*;

record Loan(String isbn, int borrowedDay) { }

public class Main {
    static double totalFines(List<Loan> loans, int today) {
        return 0;
    }

    public static void main(String[] args) {
        List<Loan> loans = List.of(new Loan("a", 0), new Loan("b", 10), new Loan("c", 100));
        System.out.println(totalFines(loans, 30));
    }
}
```
```java check
List<Object> loans = new ArrayList<>();
loans.add(make("Loan", "a", 0));
loans.add(make("Loan", "b", 10));
loans.add(make("Loan", "c", 100));
near(4.0 + 1.5, call("totalFines", loans, 30), "totalFines(day 30): a is 16 days late (4.00), b is 6 days late (1.50), c is not due yet");
near(15.0, call("totalFines", loans, 200), "totalFines(day 200): every loan is capped at 5.00");
near(0, call("totalFines", loans, 14), "totalFines(day 14): nothing overdue yet");
near(0.25, call("totalFines", List.of(make("Loan", "x", 0)), 15), "one loan 1 day late");
```
```java solution
import java.util.*;

record Loan(String isbn, int borrowedDay) { }

public class Main {
    static double totalFines(List<Loan> loans, int today) {
        double total = 0;
        for (Loan loan : loans) {
            int daysLate = today - (loan.borrowedDay() + 14);
            if (daysLate > 0) {
                total += Math.min(5.00, daysLate * 0.25);
            }
        }
        return total;
    }

    public static void main(String[] args) {
        List<Loan> loans = List.of(new Loan("a", 0), new Loan("b", 10), new Loan("c", 100));
        System.out.println(totalFines(loans, 30));
    }
}
```
hint: daysLate = today - (borrowedDay + 14). Only positive values cost money; use Math.min(5.00, daysLate * 0.25) for each loan.
:::

:::exercise Most borrowed author
Write `static Optional<String> topAuthor(List<String> borrowedAuthors)` returning the author who appears most often in the list (break ties alphabetically), or an empty Optional for an empty list. Use a stream with `Collectors.groupingBy` and `Collectors.counting()`.
```java starter
import java.util.*;
import java.util.stream.*;

public class Main {
    static Optional<String> topAuthor(List<String> borrowedAuthors) {
        return Optional.empty();
    }

    public static void main(String[] args) {
        System.out.println(topAuthor(List.of("Bloch", "Herbert", "Bloch", "Hawking")));
    }
}
```
```java check
eq(Optional.of("Bloch"), call("topAuthor", List.of("Bloch", "Herbert", "Bloch", "Hawking")), "topAuthor([Bloch, Herbert, Bloch, Hawking])");
eq(Optional.of("Austen"), call("topAuthor", List.of("Woolf", "Austen", "Woolf", "Austen")), "a tie between Woolf and Austen");
eq(Optional.empty(), call("topAuthor", List.of()), "topAuthor([])");
sourceHas("groupingBy", "Use Collectors.groupingBy.");
```
```java solution
import java.util.*;
import java.util.stream.*;

public class Main {
    static Optional<String> topAuthor(List<String> borrowedAuthors) {
        Map<String, Long> counts = borrowedAuthors.stream()
            .collect(Collectors.groupingBy(a -> a, TreeMap::new, Collectors.counting()));
        return counts.entrySet().stream()
            .max(Map.Entry.<String, Long>comparingByValue()
                .thenComparing(Map.Entry.comparingByKey(Comparator.reverseOrder())))
            .map(Map.Entry::getKey);
    }

    public static void main(String[] args) {
        System.out.println(topAuthor(List.of("Bloch", "Herbert", "Bloch", "Hawking")));
    }
}
```
hint: Count with groupingBy(a -> a, Collectors.counting()). Then stream the entries and pick the max by value; for ties, the alphabetically first name should win, so compare keys in reverse order inside max.
:::

### Where to go next

You now know the core of Java. To keep growing:

**1. Install a JDK and an IDE.** Get a JDK 17 or 21 build (for example from adoptium.net) and an editor such as IntelliJ IDEA Community or VS Code with the Java extensions. Compile and run from the terminal once, so you know what the IDE does for you:

```bash
javac Main.java
java Main
```

**2. Learn a build tool.** Real projects use **Maven** or **Gradle** to manage dependencies and run tests.

**3. Write tests.** **JUnit 5** is the standard. Writing tests first for tricky methods is a great habit.

**4. Pick a direction:**

| Direction | Technologies |
|---|---|
| Backend and web APIs | Spring Boot, Spring Data JPA, Hibernate, REST |
| Android apps | Kotlin and Java with Android Studio |
| Big data and streaming | Apache Kafka, Spark, Flink |
| Enterprise systems | Jakarta EE, microservices, Docker, Kubernetes |

**5. Practise.** Solve problems on Exercism's Java track, LeetCode or Advent of Code, and build small projects you care about. Put them on GitHub.

Congratulations on finishing the course. Come back to the playground whenever you want to try an idea, and play Java Quest to keep the syntax sharp.

:::quiz
? Why does `Library.history()` return `Collections.unmodifiableList(history)`?
+ So callers can read the history but not change it
- It's faster
- Lists can't be returned directly
= It protects the library's internal state, which is encapsulation.

? Why is `LibraryException` a checked exception?
+ Callers are forced to handle refused operations
- Checked exceptions are faster
- Unchecked exceptions can't have messages
= A refused loan is an expected situation the caller should deal with.
:::
