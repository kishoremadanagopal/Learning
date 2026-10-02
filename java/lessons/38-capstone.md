# Lesson 38: Capstone: a library system

**You'll learn:** records, enums, encapsulation, exceptions, Optional and streams in one program.

▶ **Practise this lesson in the [sandbox](https://kishoremadanagopal.github.io/learning/java/#capstone)**: run every example and check your exercise answers.

## Key terms

- **Capstone project:** a project that combines everything you've learned.
- **Domain model:** the classes that represent the real-world things a program deals with.
- **Build tool:** software such as Maven or Gradle that compiles, tests and packages projects.
- **Unit test:** a small automated check of one piece of code, usually written with JUnit.

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

## What each part demonstrates

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

## Your turn

The exercises below extend the system. Each one is self-contained.

## Where to go next

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

## Common mistakes

- Putting all the logic in `main` instead of small classes and methods.
- Exposing internal collections that callers can modify.
- Using exceptions for normal control flow instead of expected checks.

## Exercises

### 1. Overdue fines

Write `static double totalFines(List<Loan> loans, int today)` where `Loan` is the given record. A loan is due 14 days after `borrowedDay`; each day past the due date costs `0.25`, capped at `5.00` per loan. Loans not yet overdue cost nothing.

Starter code:

```java
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

### 2. Most borrowed author

Write `static Optional<String> topAuthor(List<String> borrowedAuthors)` returning the author who appears most often in the list (break ties alphabetically), or an empty Optional for an empty list. Use a stream with `Collectors.groupingBy` and `Collectors.counting()`.

Starter code:

```java
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

**In the sandbox:** exercises 56–57. Press **Check** to test your answer.

<details>
<summary>Hints</summary>

1. daysLate = today - (borrowedDay + 14). Only positive values cost money; use Math.min(5.00, daysLate * 0.25) for each loan.
2. Count with groupingBy(a -> a, Collectors.counting()). Then stream the entries and pick the max by value; for ties, the alphabetically first name should win, so compare keys in reverse order inside max.

</details>

<details>
<summary>Answers</summary>

**1. Overdue fines**

```java
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

**2. Most borrowed author**

```java
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

</details>

## Quick quiz

1. Why does `Library.history()` return `Collections.unmodifiableList(history)`?
   - A) So callers can read the history but not change it
   - B) It's faster
   - C) Lists can't be returned directly

2. Why is `LibraryException` a checked exception?
   - A) Callers are forced to handle refused operations
   - B) Checked exceptions are faster
   - C) Unchecked exceptions can't have messages

<details>
<summary>Quiz answers</summary>

1. **A) So callers can read the history but not change it**: It protects the library's internal state, which is encapsulation.
2. **A) Callers are forced to handle refused operations**: A refused loan is an expected situation the caller should deal with.

</details>

---
Previous: [Lesson 37](37-algorithms-and-big-o.md) · Back to the [course home](../README.md)
