@@@ part
id: 6
title: Object-Oriented Python
level: Intermediate
blurb: Model real things with classes, share behaviour through inheritance, and make your objects feel built in with special methods and dataclasses.

@@@ lesson
id: classes-and-objects
title: Classes and objects
minutes: 15
summary: Define classes, create objects, and use attributes, methods and self.
---
So far you've used Python's built-in types: `str`, `list`, `dict`. A **class** lets you create your own type. An **object** (or **instance**) is one particular value of that type.

Think of a class as a blueprint and objects as houses built from it. Every house has the same layout, but each has its own paint colour and furniture.

```python
class Dog:
    def __init__(self, name, age):
        self.name = name        # attributes: data stored on the object
        self.age = age

    def bark(self):             # method: a function that belongs to the class
        return f"{self.name} says woof!"

rex = Dog("Rex", 3)
fido = Dog("Fido", 7)
print(rex.bark())
print(fido.name, fido.age)
```

![The class Dog is a blueprint; Dog("Rex", 3) and Dog("Fido", 7) build two objects, each with its own name and age](figures/class-objects.svg)

### What's going on

- `class Dog:` defines a new type. Class names use **CamelCase**.
- `__init__` is the **initializer**. Python calls it automatically when you create an object with `Dog(...)`.
- `self` is the object being created or used. `self.name = name` stores the value **on that object**.
- `rex.bark()` calls the method; Python passes `rex` as `self` automatically.

### Objects keep their own state

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

ana = BankAccount("Ana", 100)
ben = BankAccount("Ben")
ana.deposit(50)
ben.deposit(20)
ana.withdraw(30)
print(ana.owner, ana.balance)
print(ben.owner, ben.balance)
```

This is the core idea of **object-oriented programming (OOP)**: bundle data together with the functions that work on it, and protect the data's rules (like "no negative balance") inside the methods.

### Class attributes vs instance attributes

Attributes set on `self` belong to one object. Attributes defined directly in the class body are shared by all instances:

```python
class Circle:
    pi = 3.14159              # class attribute, shared

    def __init__(self, radius):
        self.radius = radius  # instance attribute, per object

    def area(self):
        return Circle.pi * self.radius ** 2

small, big = Circle(1), Circle(10)
print(small.area(), big.area())
```

### Class methods and static methods

A `@classmethod` receives the class itself (`cls`) instead of an instance. It's often used for alternative constructors. A `@staticmethod` receives neither; it's just a function grouped with the class.

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, f):
        return cls((f - 32) * 5 / 9)

    @staticmethod
    def is_freezing(celsius):
        return celsius <= 0

t = Temperature.from_fahrenheit(212)
print(t.celsius, Temperature.is_freezing(t.celsius))
```

### Checking types

```python
class Cat:
    pass

tom = Cat()
print(isinstance(tom, Cat), isinstance(tom, str))
print(type(tom).__name__)
```

:::exercise Rectangle class
Create a class `Rectangle` with:

- `__init__(self, width, height)` storing both values
- `area()` returning width × height
- `perimeter()` returning 2 × (width + height)
- `is_square()` returning `True` when width equals height
```python starter
class Rectangle:
    pass

r = Rectangle(3, 4)
print(r.area(), r.perimeter(), r.is_square())
```
```python check
r = Rectangle(3, 4)
assert r.width == 3 and r.height == 4, "Store width and height as attributes"
assert r.area() == 12, f"area() should be 12 but was {r.area()}"
assert r.perimeter() == 14, f"perimeter() should be 14 but was {r.perimeter()}"
assert r.is_square() is False
assert Rectangle(5, 5).is_square() is True
```
```python solution
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height

r = Rectangle(3, 4)
print(r.area(), r.perimeter(), r.is_square())
```
hint: Every method takes self as its first parameter. Inside, use self.width and self.height.
:::

:::exercise Shopping cart
Create a class `Cart` that starts empty. `add(item, price, qty=1)` adds an item; `total()` returns the sum of price × qty; `count()` returns the total number of units.
```python starter
class Cart:
    def __init__(self):
        pass

cart = Cart()
cart.add("pen", 1.5, 4)
cart.add("book", 12.0)
print(cart.total(), cart.count())
```
```python check
c = Cart()
assert c.total() == 0 and c.count() == 0, "A new cart should be empty"
c.add("pen", 1.5, 4)
c.add("book", 12.0)
assert c.total() == 18.0, f"total() should be 18.0 but was {c.total()}"
assert c.count() == 5, f"count() should be 5 but was {c.count()}"
d = Cart()
assert d.count() == 0, "Each cart must have its own items (create the list inside __init__)"
```
```python solution
class Cart:
    def __init__(self):
        self.items = []

    def add(self, item, price, qty=1):
        self.items.append((item, price, qty))

    def total(self):
        return sum(price * qty for _, price, qty in self.items)

    def count(self):
        return sum(qty for _, _, qty in self.items)

cart = Cart()
cart.add("pen", 1.5, 4)
cart.add("book", 12.0)
print(cart.total(), cart.count())
```
hint: In __init__, set self.items = []. add() appends a tuple (item, price, qty). total() and count() loop over self.items.
:::

:::quiz
? What is `self` in a method?
+ The object the method was called on
- The class
- A reserved keyword you can't rename
= Python passes the instance automatically. `self` is a convention, not a keyword.

? When does `__init__` run?
- When the class is defined
+ Each time a new object is created
- When the program ends
= `Dog("Rex", 3)` creates an object and immediately calls `__init__` on it.
:::

@@@ lesson
id: inheritance
title: Inheritance and polymorphism
minutes: 15
summary: Build specialised classes from general ones, override methods, use super(), and write code that works with many types.
---
**Inheritance** lets a new class (the **child** or subclass) reuse and extend an existing class (the **parent** or base class).

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def introduce(self):
        return f"I am {self.name} and I say {self.speak()}"

class Dog(Animal):          # Dog inherits from Animal
    def speak(self):        # override the parent's method
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"

for pet in [Dog("Rex"), Cat("Tom"), Animal("Generic")]:
    print(pet.introduce())
```

`Dog` and `Cat` didn't define `__init__` or `introduce`; they inherited them. They only changed what's different.

![Dog and Cat inherit from Animal: they get name and introduce() from Animal and replace speak() with their own](figures/inheritance-tree.svg)

### super(): extending the parent's behaviour

When a child needs extra setup, call the parent's version with `super()` and then add to it:

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def describe(self):
        return f"{self.name} earns {self.salary:,}"

class Manager(Employee):
    def __init__(self, name, salary, reports):
        super().__init__(name, salary)    # reuse the parent's setup
        self.reports = reports

    def describe(self):
        base = super().describe()
        return f"{base} and manages {len(self.reports)} people"

m = Manager("Ana", 120000, ["Ben", "Cy"])
print(m.describe())
print(isinstance(m, Employee))
```

### Polymorphism

**Polymorphism** means "many forms": different classes respond to the same method call in their own way. The loop above called `introduce()` without caring which animal it had.

Python goes further with **duck typing**: "if it walks like a duck and quacks like a duck, it's a duck." Objects don't even need a shared parent, only the methods you call:

```python
class Robot:
    def speak(self):
        return "Beep"

class Parrot:
    def speak(self):
        return "Hello!"

for thing in [Robot(), Parrot()]:
    print(thing.speak())
```

### Abstract base classes

To force subclasses to implement a method, use `abc.ABC` and `@abstractmethod`. You can't create an instance of a class that still has abstract methods:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        ...

    def describe(self):
        return f"{type(self).__name__} with area {self.area():.2f}"

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

print(Square(3).describe())
try:
    Shape()
except TypeError as e:
    print("TypeError:", e)
```

### Composition: often better than inheritance

Inheritance means "is a" (a Manager **is an** Employee). When the relationship is "has a", store another object as an attribute instead. A `Car` **has an** `Engine`; it isn't one.

```python
class Engine:
    def start(self):
        return "vroom"

class Car:
    def __init__(self):
        self.engine = Engine()    # composition

    def drive(self):
        return f"Engine goes {self.engine.start()}"

print(Car().drive())
```

A good rule of thumb: prefer composition, and use inheritance for genuine "is a" relationships.

:::exercise Shape hierarchy
Complete the classes so that `Circle(radius)` and `Rect(w, h)` both inherit from `Shape` and implement `area()`. Then write `total_area(shapes)` that returns the sum of all areas. Use `math.pi` for circles.
```python starter
import math

class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    pass

class Rect(Shape):
    pass

def total_area(shapes):
    return 0

print(round(total_area([Circle(1), Rect(2, 3)]), 2))
```
```python check
import math as _m
assert issubclass(Circle, Shape) and issubclass(Rect, Shape), "Circle and Rect must inherit from Shape"
assert abs(Circle(2).area() - _m.pi * 4) < 1e-9, "Circle(2).area() should be pi * 4"
assert Rect(2, 3).area() == 6, "Rect(2, 3).area() should be 6"
assert abs(total_area([Circle(1), Rect(2, 3)]) - (_m.pi + 6)) < 1e-9, "total_area is wrong"
assert total_area([]) == 0
```
```python solution
import math

class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

class Rect(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

def total_area(shapes):
    return sum(shape.area() for shape in shapes)

print(round(total_area([Circle(1), Rect(2, 3)]), 2))
```
hint: Each subclass needs its own __init__ to store its measurements and its own area(). total_area can be sum(s.area() for s in shapes).
:::

:::exercise Savings account
Given the `Account` class, create `SavingsAccount(Account)` that takes an extra `rate` argument and has `add_interest()`, which increases the balance by `balance * rate`. Use `super().__init__`.
```python starter
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

class SavingsAccount(Account):
    pass

s = SavingsAccount("Ana", 1000, 0.05)
s.add_interest()
print(s.owner, s.balance)
```
```python check
s = SavingsAccount("Ana", 1000, 0.05)
assert s.owner == "Ana" and s.rate == 0.05, "Store owner (via super) and rate"
s.add_interest()
assert abs(s.balance - 1050) < 1e-9, f"Balance should be 1050 after interest, got {s.balance}"
assert isinstance(s, Account)
assert "super()" in __source__, "Call super().__init__(...)"
```
```python solution
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

class SavingsAccount(Account):
    def __init__(self, owner, balance, rate):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        self.balance += self.balance * self.rate

s = SavingsAccount("Ana", 1000, 0.05)
s.add_interest()
print(s.owner, s.balance)
```
hint: def __init__(self, owner, balance, rate): super().__init__(owner, balance); self.rate = rate
:::

:::quiz
? What does `super().__init__(...)` do?
+ Runs the parent class's initializer
- Creates a new parent object
- Deletes the child's attributes
= It lets the child reuse the parent's setup before adding its own.

? A Library *has* many Books. What's the better design?
- `class Library(Book)`
+ A Library with a `books` list attribute
- `class Book(Library)`
= That's a "has a" relationship, so composition fits better than inheritance.
:::

@@@ lesson
id: special-methods
title: Special (dunder) methods
minutes: 15
summary: Make your classes print nicely, compare, add, have a length and work with for loops.
---
Methods with double underscores, like `__init__`, are called **special** or **dunder** methods. Python calls them for you when you use built-in syntax. Implementing them makes your objects behave like built-in types.

### __str__ and __repr__: how objects print

```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):          # for users: print(), str(), f-strings
        return f"{self.title} by {self.author}"

    def __repr__(self):         # for developers: the console, inside lists
        return f"Book({self.title!r}, {self.author!r})"

b = Book("Dune", "Frank Herbert")
print(b)
print([b])
print(repr(b))
```

Always write a `__repr__`. A good one looks like the code that would recreate the object.

### Comparison: __eq__ and __lt__

By default, `==` checks whether two variables refer to the **same object**. Define `__eq__` to compare by value. Defining `__lt__` (less than) makes `sorted()` work:

```python
class Version:
    def __init__(self, text):
        self.parts = tuple(int(p) for p in text.split("."))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts

    def __repr__(self):
        return "v" + ".".join(map(str, self.parts))

print(Version("1.10.0") > Version("1.9.3"))
print(sorted([Version("2.0"), Version("1.10"), Version("1.2")]))
print(Version("3.1") == Version("3.1"))
```

Python works out `>` from your `__lt__` by swapping the sides. `functools.total_ordering` can fill in the rest (`<=`, `>=`) for you.

### Arithmetic: __add__ and friends

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(3, 4)
print(v + Vector(1, 1))
print(v * 2)
print(abs(v))
```

### Containers: __len__, __getitem__, __contains__, __iter__

```python
class Playlist:
    def __init__(self, *songs):
        self.songs = list(songs)

    def __len__(self):
        return len(self.songs)

    def __getitem__(self, index):
        return self.songs[index]

    def __contains__(self, song):
        return song in self.songs

    def __iter__(self):
        return iter(self.songs)

mix = Playlist("Intro", "Groove", "Outro")
print(len(mix), mix[1], "Groove" in mix)
for song in mix:
    print("-", song)
```

### A quick reference

| You write | Python calls |
|---|---|
| `str(x)`, `print(x)` | `x.__str__()` |
| `repr(x)` | `x.__repr__()` |
| `x == y` | `x.__eq__(y)` |
| `x < y` | `x.__lt__(y)` |
| `x + y` | `x.__add__(y)` |
| `len(x)` | `x.__len__()` |
| `x[i]` | `x.__getitem__(i)` |
| `item in x` | `x.__contains__(item)` |
| `for i in x` | `x.__iter__()` |
| `x()` | `x.__call__()` |
| `with x:` | `x.__enter__()` / `x.__exit__()` |

:::exercise Money class
Create a `Money` class holding `amount` and `currency`, with:

- `__repr__` returning like `Money(10.5, 'USD')`
- `__str__` returning like `10.50 USD`
- `__eq__` comparing amount and currency
- `__add__` that adds two Money values of the **same** currency and raises `ValueError` for different currencies
```python starter
class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

a = Money(10.5, "USD")
print(a, repr(a), a + Money(2, "USD"))
```
```python check
a = Money(10.5, "USD")
assert str(a) == "10.50 USD", f"str() should be '10.50 USD' but was {str(a)!r}"
assert repr(a) == "Money(10.5, 'USD')", f"repr() should be \"Money(10.5, 'USD')\" but was {repr(a)!r}"
assert Money(1, "EUR") == Money(1, "EUR"), "Equal amounts and currencies should be =="
assert Money(1, "EUR") != Money(1, "USD"), "Different currencies are not equal"
total = a + Money(2, "USD")
assert total == Money(12.5, "USD"), f"10.5 + 2 USD should be Money(12.5, 'USD'), got {total!r}"
try:
    a + Money(1, "EUR")
except ValueError:
    pass
else:
    raise AssertionError("Adding USD and EUR should raise ValueError")
```
```python solution
class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount!r}, {self.currency!r})"

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Can't add different currencies")
        return Money(self.amount + other.amount, self.currency)

a = Money(10.5, "USD")
print(a, repr(a), a + Money(2, "USD"))
```
hint: Use !r inside the f-string for repr: f"Money({self.amount!r}, {self.currency!r})". __add__ should return a new Money object.
:::

:::quiz
? Which method does `print(obj)` use first?
+ `__str__`
- `__repr__`
- `__print__`
= print uses `__str__`, falling back to `__repr__` if `__str__` isn't defined.

? Which method makes `len(obj)` work?
- `__length__`
+ `__len__`
- `__size__`
= `len()` calls `__len__`.

? Without `__eq__`, what does `a == b` compare for two objects?
+ Whether they're the same object
- All their attributes
- Their string forms
= The default equality is identity, like `a is b`.
:::

@@@ lesson
id: properties-and-dataclasses
title: Properties and dataclasses
minutes: 12
summary: Guard attributes with @property and cut boilerplate with @dataclass.
---
### Properties: attributes with rules

Sometimes setting an attribute should run a check, or an attribute should be calculated. A **property** looks like a plain attribute from the outside but runs a method behind the scenes.

```python
class Thermostat:
    def __init__(self, celsius):
        self.celsius = celsius          # goes through the setter below

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):               # read-only, calculated
        return self._celsius * 9 / 5 + 32

t = Thermostat(21)
t.celsius = 25
print(t.celsius, t.fahrenheit)
try:
    t.celsius = -300
except ValueError as e:
    print("Rejected:", e)
```

A leading underscore (`_celsius`) is a convention meaning "internal; don't touch from outside". Python doesn't enforce it, but other programmers respect it.

Start with plain attributes. You can switch to a property later without changing any code that uses the class. This is why Python code rarely has `get_x()` / `set_x()` methods.

### Dataclasses: less boilerplate

Many classes mostly hold data. Writing `__init__`, `__repr__` and `__eq__` by hand gets repetitive. The `@dataclass` decorator generates them from **type-annotated** class attributes:

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    tags: list = field(default_factory=list)   # a fresh list per object

    def discounted(self, percent):
        return round(self.price * (1 - percent / 100), 2)

p = Product("Lamp", 40.0)
p.tags.append("home")
print(p)
print(p == Product("Lamp", 40.0, ["home"]))
print(p.discounted(25))
```

`field(default_factory=list)` avoids the shared mutable default trap from Part 4.

### Useful dataclass options

```python
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int = 0

points = [Point(3, 1), Point(1, 5), Point(1, 2)]
print(sorted(points))           # order=True compares fields in order

p = Point(1, 2)
try:
    p.x = 10                    # frozen=True makes objects immutable
except Exception as e:
    print(type(e).__name__)
```

Frozen dataclasses can be used as dictionary keys and set members, just like tuples.

### __post_init__: validation in dataclasses

```python
from dataclasses import dataclass

@dataclass
class Order:
    item: str
    qty: int

    def __post_init__(self):
        if self.qty < 1:
            raise ValueError("qty must be at least 1")

print(Order("pen", 3))
try:
    Order("pen", 0)
except ValueError as e:
    print("Error:", e)
```

:::exercise Student record
Create a dataclass `Student` with `name: str` and `grades: list` (default: a new empty list). Add a property `average` that returns the mean grade, or `0` when there are no grades.
```python starter
from dataclasses import dataclass, field

class Student:
    pass

s = Student("Ana", [90, 80])
print(s, s.average)
```
```python check
import dataclasses
assert dataclasses.is_dataclass(Student), "Decorate Student with @dataclass"
s = Student("Ana", [90, 80])
assert s.average == 85, f"average should be 85 but was {s.average}"
assert Student("Ben").average == 0, "No grades should give an average of 0"
a, b = Student("A"), Student("B")
a.grades.append(100)
assert b.grades == [], "Each student needs their own list (use field(default_factory=list))"
assert Student("Ana", [1]) == Student("Ana", [1]), "Dataclasses should compare by value"
```
```python solution
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    grades: list = field(default_factory=list)

    @property
    def average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

s = Student("Ana", [90, 80])
print(s, s.average)
```
hint: Put @dataclass above the class, declare name: str and grades: list = field(default_factory=list), then add an @property method named average.
:::

:::quiz
? What does `@property` let you do?
+ Run a method when an attribute is read, while keeping attribute syntax
- Make an attribute private
- Speed up attribute access
= `t.fahrenheit` looks like an attribute but calls a method.

? Which methods does `@dataclass` generate by default?
+ `__init__`, `__repr__` and `__eq__`
- Only `__init__`
- `__str__` and `__hash__` only
= Those three are always generated; others depend on options like `order=True`.
:::
