@@@ part
id: 1
title: JavaScript Basics
level: Beginner
blurb: The core of the language: printing output, variables and types, strings, numbers, comparisons and conditions, loops, functions, and scope and closures.

@@@ lesson
id: what-is-javascript
title: What JavaScript is
minutes: 18
summary: Where JavaScript runs (browsers, Node.js and other runtimes), ECMAScript and its yearly editions, how JavaScript compares with Python, statements, semicolons and comments, printing with console.log, and how this sandbox runs your code.
---
**JavaScript** is the programming language of the web. Every interactive web page runs it, and since **Node.js** arrived in 2009 it also runs servers, command-line tools and build systems. It's one of the most widely used languages in the world.

### Where JavaScript runs

![JavaScript code in the middle, with arrows to the places that run it: web browsers (Chrome, Edge, Firefox, Safari), server and command-line runtimes (Node.js, Deno, Bun), and other hosts such as desktop apps built with Electron and serverless platforms](figures/where-js-runs.svg)

A program that runs JavaScript is a **runtime** (or **host**). Each provides the same core language plus its own extras:

| Runtime | Extras it adds |
|---|---|
| a web browser | the page (`document`), clicks and other events, `fetch`, storage |
| **Node.js** | files, networking, processes; the npm package ecosystem |
| Deno, Bun | modern alternatives to Node.js, with TypeScript built in |

The core language is standardised as **ECMAScript** by a committee called **TC39**. A new edition comes out every June: ECMAScript 2015 (often called **ES6**) modernised the language, and ECMAScript 2026 is the latest. Browsers add new features as they're agreed, so code that works in the newest Chrome may need a recent version of Safari too. This course points out the few places where that matters.

### Your first program

```js
console.log("Hello, world!");
console.log("JavaScript can do maths:", 6 * 7);
console.log("Text and numbers:", "3" + 4, 3 + 4);
```

`console.log(...)` prints its arguments, separated by spaces. In a browser it prints to the developer console (press F12, or Cmd+Option+J on a Mac); in Node.js it prints to the terminal; here it prints to the output panel.

### Statements, semicolons and comments

```js
// A comment runs to the end of the line.
/* A block comment
   can span several lines. */

let total = 2 + 3;     // a statement; the semicolon ends it
total = total * 10
console.log(total)     // works without semicolons too
```

JavaScript inserts missing semicolons for you (**automatic semicolon insertion**), so most code works either way. This course writes them, like most style guides; tools such as Prettier (Part 7) add them automatically.

### If you know Python

| Python | JavaScript |
|---|---|
| `print("hi")` | `console.log("hi");` |
| indentation makes blocks | `{ }` make blocks; indentation is only for readability |
| `x = 5` | `let x = 5;` or `const x = 5;` |
| `True`, `False`, `None` | `true`, `false`, `null` (and `undefined`) |
| `and`, `or`, `not` | `&&`, `\|\|`, `!` |
| `# comment` | `// comment` |
| `def add(a, b):` | `function add(a, b) { … }` |

### How this sandbox runs your code

Your code runs in your own browser, in a separate thread (a **Web Worker**), so an endless loop can't freeze the page: press **Stop**. Two details:

- Code runs in **strict mode**, as in modern JavaScript modules: a few old, error-prone features are switched off, and some silent mistakes become real errors (Lesson 2).
- You can use `await` at the top level (Part 4), and timers like `setTimeout` finish before the output is shown.

```js error
console.log("This line runs.");
console.log(messag);            // a typo: there's no variable called messag
console.log("This one doesn't.");
```

When something goes wrong, you get the line, the error and a hint. Read errors from the top: the **error type** (`ReferenceError`) and its message usually say exactly what's wrong.

:::exercise Print a receipt
Print exactly these three lines with `console.log`:

```text
Bike shop
Inner tube: 6
Total: 12
```

Compute the total as `2 * 6` in the code rather than typing `12`.
```js starter
// Print the three lines here.
```
```js check
const lines = __output__.trim().split("\n");
if (lines.length !== 3) throw new AssertionError(`Print exactly 3 lines; your code printed ${lines.length}.`);
same(lines, ["Bike shop", "Inner tube: 6", "Total: 12"], "Your printed lines");
if (!/2\s*\*\s*6/.test(__source__)) throw new AssertionError("Compute the total with 2 * 6 in your code.");
```
```js solution
console.log("Bike shop");
console.log("Inner tube:", 6);
console.log("Total:", 2 * 6);
```
hint: Each `console.log` call prints one line.
hint: `console.log("Inner tube:", 6)` prints the text, a space, then the number.
hint: The last line is `console.log("Total:", 2 * 6);`.
approach:
1. **Understand:** three lines of output, exact text; the total must be calculated.
2. **Examples:** `console.log("Total:", 2 * 6)` prints `Total: 12`.
3. **Brute force:** typing `"Total: 12"` works but skips the calculation.
4. **Pattern:** **one `console.log` per line**, with several arguments separated by spaces.
5. **Plan:** three calls in order.
6. **Code and test:** run it and compare the output with the target, character by character.
walkthrough:
**Line by line**

- `console.log("Bike shop")` prints the text as it is.
- With several arguments, `console.log` joins them with single spaces, so `"Inner tube:", 6` prints `Inner tube: 6`.
- `2 * 6` is evaluated first, then printed: `Total: 12`.

**Common wrong approach:** `console.log("Total: " + 2 * 6)` also works (the multiplication happens before the `+`), but `console.log("Total: " + 2 + 6)` prints `Total: 26`: once one side of `+` is text, `+` joins text. Lesson 3 covers this.
:::

:::exercise Fix the program
This program has three mistakes. Fix them so it prints `Welcome, Ada!` and then `You have 3 messages.`
```js starter
consol.log("Welcome, Ada!")
let count = 3;
console.log("You have", count "messages.");
console.log("Done);
```
```js check
const lines = __output__.trim().split("\n");
same(lines.slice(0, 2), ["Welcome, Ada!", "You have 3 messages."], "Your first two printed lines");
```
```js solution
console.log("Welcome, Ada!");
let count = 3;
console.log("You have", count, "messages.");
console.log("Done");
```
hint: Read the error message: which name isn't defined, or what couldn't be read?
hint: `consol` is a typo. Arguments must be separated by commas. Every string needs both quotes.
hint: Fix `consol.log` → `console.log`, add the comma after `count`, and close the quote in `"Done"`.
approach:
1. **Understand:** the code must run and print the two required lines first.
2. **Examples:** a missing quote is a `SyntaxError`, reported before anything runs.
3. **Brute force:** rewrite everything from scratch: works, but practise reading the errors instead.
4. **Pattern:** **fix one error at a time**: run, read the message, fix, run again.
5. **Plan:** syntax errors first (quote, comma), then the misspelt name.
6. **Code and test:** run after each fix.
walkthrough:
**Line by line**

- `"Done);` has no closing quote, so JavaScript can't read the program at all: a `SyntaxError` stops everything before any line runs.
- `count "messages."` is missing a comma between two arguments: another syntax error.
- `consol.log` is a `ReferenceError`: there's no variable called `consol`. That only shows once the syntax errors are fixed, because syntax is checked before anything runs.

**Common wrong approach:** fixing only the line in the first error message and assuming it was the only problem. JavaScript reports one syntax error at a time.
:::

:::quiz
? Who standardises the core JavaScript language?
+ TC39, as the ECMAScript specification
- Google
- Each browser separately
= A new ECMAScript edition comes out every June.
? What does console.log("a", 1, true) print?
+ a 1 true
- a,1,true
- "a" 1 true
= Arguments are printed separated by spaces; strings without quotes at the top level.
? Which runtime lets JavaScript read files and run servers?
+ Node.js
- A web browser tab
- ECMAScript
= Node.js adds files, networking and processes to the language.
? Are semicolons required at the end of statements?
+ Usually not, thanks to automatic semicolon insertion, but most style guides use them
- Yes, always
- No, they're an error
= Formatters such as Prettier add them for you.
:::

@@@ lesson
id: variables-and-types
title: Variables and types
minutes: 24
summary: Declaring variables with let and const (and why not var), naming rules and conventions, the seven primitive types and objects, typeof and its quirks, dynamic typing, converting between types with Number, String and Boolean, NaN, and undefined versus null.
---
A **variable** is a name for a value. JavaScript has two modern ways to declare one:

```js
const shop = "Spoke & Chain";   // const: the name can't be reassigned
let stock = 12;                 // let: the name can be reassigned
stock = stock - 1;
console.log(shop, "has", stock, "inner tubes");
```

**Use `const` by default**, and `let` only when the value really has to change. Readers then know at a glance which names stay fixed. You'll also see the old keyword **`var`** in older code: it has confusing scoping rules (Lesson 8), so don't use it in new code.

```js error
const vat = 0.2;
vat = 0.25;          // TypeError: assignment to a constant variable
```

`const` stops the **name** being reassigned; it doesn't freeze the value. A `const` array can still have items added (Part 2).

### Names

- Letters, digits, `_` and `$`; not starting with a digit; case-sensitive (`total` and `Total` differ).
- Convention: **camelCase** for variables and functions (`orderTotal`), **PascalCase** for classes (`Order`), **UPPER_SNAKE_CASE** for fixed settings (`MAX_ITEMS`).
- Reserved words such as `let`, `class` and `function` can't be names.

### Types

Every value has a **type**. There are seven **primitive** (simple, unchangeable) types, and everything else is an **object**:

| Type | Examples | Notes |
|---|---|---|
| string | `"hi"`, `'hi'`, `` `hi` `` | text (Lesson 3) |
| number | `42`, `3.14`, `-0`, `NaN`, `Infinity` | one type for whole and decimal numbers (Lesson 4) |
| bigint | `9007199254740993n` | whole numbers of any size |
| boolean | `true`, `false` | |
| undefined | `undefined` | "no value has been given" |
| null | `null` | "deliberately empty" |
| symbol | `Symbol("id")` | unique keys; rarely needed day to day |
| object | `{ name: "Ada" }`, `[1, 2]`, functions, dates | everything else (Part 2) |

`typeof` tells you a value's type, as a string, with two famous quirks:

```js
console.log(typeof "hi", typeof 42, typeof 10n, typeof true, typeof undefined);
console.log(typeof { a: 1 }, typeof [1, 2], typeof function () {});
console.log(typeof null);             // "object": a bug from 1995 that can never be fixed
console.log(Array.isArray([1, 2]));   // the reliable way to test for an array
```

- `typeof null` is `"object"`: test for null with `value === null`.
- Arrays are objects, so `typeof [1, 2]` is `"object"`: use `Array.isArray`.

### Dynamic typing

Variables don't have types; **values** do. The same `let` variable can hold a number and later a string. That's flexible, but it means type mistakes only show up when the code runs, which is the main reason TypeScript exists (Part 6).

### Converting between types

```js
console.log(Number("42"), Number("4.5"), Number(""), Number("12px"), Number(true));
console.log(parseInt("12px"), parseFloat("4.5kg"), parseInt("0.9"));
console.log(String(42), (255).toString(16), String(null));
console.log(Boolean(0), Boolean("0"), Boolean(""), Boolean("false"));
```

- `Number(text)` converts the **whole** string, or gives `NaN`. `Number("")` is `0`, a classic surprise.
- `parseInt` and `parseFloat` read as much of a number as they can from the start, and stop.
- `NaN` ("not a number") is the result of a failed number operation. It's the only value not equal to itself, so test it with `Number.isNaN(x)`.

JavaScript also converts types **automatically** in some operations, sometimes surprisingly: `"3" + 4` is `"34"` (text joining) while `"3" * 4` is `12`. Convert explicitly when you mean a number.

### undefined versus null

- **`undefined`**: the language's "nothing here yet": a declared variable with no value, a missing object property, a function with no `return`.
- **`null`**: your code's "deliberately empty": use it when you mean "no value on purpose".

```js
let middleName;
const user = { name: "Ada", phone: null };
console.log(middleName, user.phone, user.email);
```

### Strict mode catches silent mistakes

In old sloppy-mode JavaScript, assigning to a misspelt name silently created a new global variable. In strict mode (modules, classes, and this sandbox) it's an error:

```js error
let total = 10;
totl = total * 2;       // ReferenceError in strict mode
```

:::exercise Describe a value's type
Write `describe(value)` returning a string naming its type, fixing `typeof`'s quirks:

- `"null"` for `null` and `"array"` for arrays;
- `"nan"` for `NaN`;
- otherwise the result of `typeof` (`"string"`, `"number"`, `"bigint"`, `"boolean"`, `"undefined"`, `"symbol"`, `"function"` or `"object"`).
```js starter
function describe(value) {
  // your code here
}

console.log(describe(null), describe([1, 2]), describe(NaN), describe("hi"));
// null array nan string
```
```js check
test("describe", [
  [[null], "null", "null"],
  [[[1, 2]], "array", "an array"],
  [[[]], "array", "an empty array"],
  [[NaN], "nan", "NaN"],
  [["hi"], "string", "a string"],
  [[""], "string", "an empty string"],
  [[42], "number", "a number"],
  [[0], "number", "zero"],
  [[10n], "bigint", "a bigint"],
  [[false], "boolean", "false"],
  [[undefined], "undefined", "undefined"],
  [[{ a: 1 }], "object", "an object"],
  [[Infinity], "number", "Infinity is a number"],
], { show: "describe({0})" });
const d = need("describe", "function");
same(d(Symbol("x")), "symbol", "describe(Symbol('x'))");
same(d(() => 1), "function", "describe(() => 1)");
```
```js solution
function describe(value) {
  if (value === null) return "null";
  if (Array.isArray(value)) return "array";
  if (Number.isNaN(value)) return "nan";
  return typeof value;
}

console.log(describe(null), describe([1, 2]), describe(NaN), describe("hi"));
```
hint: Handle the special cases first, then fall back to `typeof value`.
hint: Test null with `value === null`, arrays with `Array.isArray(value)`, and NaN with `Number.isNaN(value)`.
hint: `if (value === null) return "null";` … then `return typeof value;` at the end.
approach:
1. **Understand:** like `typeof`, but with three special cases.
2. **Examples:** `typeof null` is `"object"`, but we want `"null"`.
3. **Brute force:** a long chain of `typeof` comparisons: unnecessary.
4. **Pattern:** **guard clauses** for special cases, then the general rule.
5. **Plan:** null → array → NaN → `typeof`.
6. **Code and test:** each type, plus `0`, `""` and `[]` (falsy or empty values that must still be described correctly).
walkthrough:
**Line by line**

- `value === null` is the only reliable null test, since `typeof null` is `"object"`.
- `Array.isArray` is true for arrays and nothing else.
- `Number.isNaN(value)` is true only for the number `NaN`. (The older global `isNaN("hi")` converts first and returns `true` for text, which is wrong here.)
- Everything else is exactly what `typeof` says.

**Trace:** `describe([])` → not null → `Array.isArray([])` is true → `"array"`.

**Common wrong approach:** `if (!value) return "null";`, which also catches `0`, `""`, `false` and `NaN`: all "falsy" (Lesson 5), but not null.
:::

:::exercise Read a quantity
A form gives you quantities as text. Write `toQuantity(text)` returning the quantity as a number, or `null` if the text isn't a whole number from 1 to 99. Surrounding spaces are fine (`" 3 "` → `3`); anything else (empty text, `"2.5"`, `"3 tubes"`, `"0"`, `"100"`) gives `null`.
```js starter
function toQuantity(text) {
  // your code here
}

console.log(toQuantity(" 3 "), toQuantity("2.5"), toQuantity(""), toQuantity("12"));
// 3 null null 12
```
```js check
test("toQuantity", [
  [[" 3 "], 3, "spaces around"],
  [["12"], 12, "two digits"],
  [["99"], 99, "the maximum"],
  [["1"], 1, "the minimum"],
  [["2.5"], null, "a decimal"],
  [[""], null, "empty text"],
  [["   "], null, "only spaces"],
  [["3 tubes"], null, "extra words"],
  [["0"], null, "zero"],
  [["100"], null, "too many"],
  [["-2"], null, "negative"],
  [["abc"], null, "not a number"],
  [["1e1"], null, "scientific notation"],
  [["0x10"], null, "hexadecimal"],
], { show: "toQuantity({0})" });
```
```js solution
function toQuantity(text) {
  const trimmed = text.trim();
  if (!/^\d+$/.test(trimmed)) return null;     // digits only
  const n = Number(trimmed);
  return n >= 1 && n <= 99 ? n : null;
}

console.log(toQuantity(" 3 "), toQuantity("2.5"), toQuantity(""), toQuantity("12"));
```
hint: `text.trim()` removes surrounding spaces. Then check the rest is only digits before converting.
hint: `Number("")` is `0` and `Number("1e1")` is `10`, so `Number` alone accepts too much. The regular expression `/^\d+$/` tests "one or more digits and nothing else".
hint: After the digit check, `const n = Number(trimmed)`, then return `n` if it's between 1 and 99, otherwise `null`.
approach:
1. **Understand:** validate the format first, then the range; anything doubtful is `null`.
2. **Examples:** `Number("2.5")` is 2.5 (not whole); `parseInt("3 tubes")` is 3 (but the text isn't a number).
3. **Brute force:** `parseInt(text)` and hope: accepts "3 tubes" and "2.5".
4. **Pattern:** **validate, then convert**.
5. **Plan:** trim → digits-only test → `Number` → range check.
6. **Code and test:** empty, spaces only, decimals, words, 0, 100, `"1e1"`, `"0x10"`.
walkthrough:
**Line by line**

- `trim()` handles the allowed spaces.
- `/^\d+$/` is a **regular expression** (Part 3): `^` start, `\d+` one or more digits, `$` end. It rejects `""`, `"2.5"`, `"-2"`, `"1e1"` and `"0x10"`, all of which `Number` would otherwise accept or misread.
- `Number(trimmed)` is now safe; the range check rejects 0 and 100.

**Trace:** `" 3 "` → `"3"` → digits only → 3 → in range → `3`.

**Common wrong approach:** relying on `Number(text)` alone. It accepts `"2.5"`, `"1e1"` (10) and `"0x10"` (16), and turns empty or all-space text into `0`. Validate the format first, then convert.
:::

:::quiz
? Which declaration should you use by default?
+ const
- let
- var
= Use let only when the name must be reassigned; avoid var.
? What does typeof null return?
+ "object"
- "null"
- "undefined"
= A historical bug; test with value === null.
? What is Number("")?
+ 0
- NaN
- null
= An empty (or all-space) string converts to 0, a common surprise.
? How do you reliably check whether x is NaN?
+ Number.isNaN(x)
- x === NaN
- typeof x === "NaN"
= NaN is the only value not equal to itself.
:::

@@@ lesson
id: strings
title: Strings and template literals
minutes: 24
summary: Single, double and backtick quotes, template literals with ${…}, escape sequences, length and indexing with at(), common string methods (slice, includes, indexOf, startsWith, toUpperCase, trim, padStart, replaceAll, split and join), immutability, comparing strings, and why emoji have length 2.
---
A **string** is text. You can write it with single quotes, double quotes or backticks:

```js
const a = 'single';
const b = "double";
const c = `backtick`;
console.log(a, b, c);
console.log("It's easy", 'Say "hi"', `Both ' and " work here`);
```

Single and double quotes are identical; pick one and be consistent (Prettier, Part 7, does this for you). Backticks are special: they make **template literals**.

### Template literals

Inside backticks, `${…}` inserts the value of any expression, and the string may span several lines:

```js
const item = "inner tube";
const price = 6;
const qty = 3;
console.log(`${qty} × ${item}: £${price * qty}`);
console.log(`Line one
Line two`);
```

Template literals are clearer than joining with `+`, and avoid the `"Total: " + 2 + 6` trap from Lesson 1.

### Escapes

| Escape | Means |
|---|---|
| `\n` | new line |
| `\t` | tab |
| `\\` | a backslash |
| `\'`, `\"`, `` \` `` | a quote character inside the same kind of quotes |
| `\u{1F6B2}` | a Unicode character by its code point (🚲) |

### Length and characters

```js
const word = "bicycle";
console.log(word.length);          // 7
console.log(word[0], word[6]);     // first and last characters
console.log(word.at(-1), word.at(-2));   // at() accepts negative positions, counting from the end
console.log(word[10]);             // undefined: no error
```

Positions (**indexes**) start at 0. `str.at(-1)` is the last character, like Python's `s[-1]`; plain `str[-1]` is `undefined` in JavaScript.

### Strings can't be changed

Strings are **immutable**: methods return a **new** string and leave the original alone.

```js
let name = "ada";
name.toUpperCase();          // makes "ADA", which is thrown away
console.log(name);           // still "ada"
name = name.toUpperCase();   // keep the result
console.log(name);
```

### Common methods

```js
const s = "  Spoke & Chain Bikes  ";
const t = s.trim();
console.log(`[${t}]`);
console.log(t.toLowerCase(), "|", t.toUpperCase());
console.log(t.includes("Chain"), t.startsWith("Spoke"), t.endsWith("s"));
console.log(t.indexOf("Chain"), t.indexOf("Wheel"));   // -1 means "not found"
console.log(t.slice(0, 5), "|", t.slice(-5));           // from 0 up to (not including) 5; the last 5
console.log(t.replace("Bikes", "Cycles"), "|", "a-b-c".replaceAll("-", "+"));
console.log("7".padStart(3, "0"), "ab".repeat(3));
console.log("red,green,blue".split(","), ["a", "b", "c"].join(" / "));
```

| Method | Does |
|---|---|
| `trim()`, `trimStart()`, `trimEnd()` | remove surrounding whitespace |
| `toLowerCase()`, `toUpperCase()` | change case |
| `includes(x)`, `startsWith(x)`, `endsWith(x)` | test for text; `true` or `false` |
| `indexOf(x)` | position of the first match, or `-1` |
| `slice(start, end)` | the part from `start` up to (not including) `end`; negative counts from the end |
| `replace(a, b)`, `replaceAll(a, b)` | replace the first match, or every match |
| `split(sep)`, `array.join(sep)` | text to an array of pieces, and back |
| `padStart(n, ch)`, `padEnd(n, ch)` | pad to length `n` |

### Comparing strings

`===` compares exactly, including case. `<` and `>` compare by character codes, so `"Zebra" < "apple"` is `true` (capital letters come first). To sort words the way people expect, use `a.localeCompare(b)` (Part 2).

### Emoji and other characters outside the basic range

JavaScript strings are sequences of **UTF-16 code units**. Most characters are one unit, but emoji and some rarer characters take two, so `.length` can surprise you:

```js
const bike = "🚲";
console.log(bike.length, [...bike].length);   // 2 code units, 1 character
console.log("café".length);
```

Spreading `[...text]` splits by real characters (code points). For user-facing text limits, count with `[...text].length`.

:::exercise Initials
Write `initials(fullName)` returning the upper-case first letter of each word, with no separators. Words are separated by one or more spaces, and there may be spaces at the start or end. An empty or all-space name gives `""`.
```js starter
function initials(fullName) {
  // your code here
}

console.log(initials("ada lovelace"), initials("  Grace  Brewster   Hopper "));
// AL GBH
```
```js check
test("initials", [
  [["ada lovelace"], "AL", "two words"],
  [["  Grace  Brewster   Hopper "], "GBH", "extra spaces"],
  [["alan"], "A", "one word"],
  [[""], "", "empty"],
  [["   "], "", "only spaces"],
  [["mary-jane watson"], "MW", "a hyphenated word is one word"],
  [["élodie durand"], "ÉD", "accented letters"],
], { show: "initials({0})" });
```
```js solution
function initials(fullName) {
  const words = fullName.trim().split(/\s+/).filter((w) => w !== "");
  return words.map((w) => w[0].toUpperCase()).join("");
}

console.log(initials("ada lovelace"), initials("  Grace  Brewster   Hopper "));
```
hint: Trim first, then split on runs of spaces. `split(/\s+/)` splits on one or more whitespace characters.
hint: `"".split(/\s+/)` gives `[""]`, one empty word, so drop empty strings before taking first letters.
hint: For each word take `word[0].toUpperCase()`, then `join("")` the letters (`map` makes a new array from each item: Part 2).
approach:
1. **Understand:** words → first letters → upper case → joined; tolerate extra spaces.
2. **Examples:** `"  Grace  Brewster   Hopper "` → words Grace, Brewster, Hopper → GBH.
3. **Brute force:** loop over characters, taking each letter that follows a space: works, with more edge cases.
4. **Pattern:** **split, transform, join**.
5. **Plan:** trim → split on whitespace → drop empties → first letter of each → upper case → join.
6. **Code and test:** one word, empty, only spaces, accents.
walkthrough:
**Line by line**

- `trim()` removes the outer spaces, so splitting doesn't create empty words at the ends.
- `/\s+/` is a regular expression meaning "one or more whitespace characters" (Part 3), so double spaces don't make empty words.
- `filter((w) => w !== "")` handles the empty-name case, where `split` still returns `[""]`.
- `map` takes each word's first character and upper-cases it; `join("")` glues the letters together.

**Trace:** `"ada lovelace"` → `["ada", "lovelace"]` → `["A", "L"]` → `"AL"`.

**Common wrong approach:** `fullName.split(" ")`, which makes empty strings for double spaces, and then `""[0]` is `undefined`, so `.toUpperCase()` throws a `TypeError`.
:::

:::exercise Make a URL slug
Write `slugify(title)` turning a title into a URL-friendly **slug**:

1. lower-case it;
2. replace every run of characters that aren't `a`–`z` or `0`–`9` with a single hyphen;
3. remove hyphens from the start and end.

For example `"  Tubeless Tyres: A Beginner's Guide!  "` → `"tubeless-tyres-a-beginner-s-guide"`.
```js starter
function slugify(title) {
  // your code here
}

console.log(slugify("  Tubeless Tyres: A Beginner's Guide!  "));
```
```js check
test("slugify", [
  [["  Tubeless Tyres: A Beginner's Guide!  "], "tubeless-tyres-a-beginner-s-guide", "punctuation and spaces"],
  [["Hello World"], "hello-world", "two words"],
  [["2026 Bike Review"], "2026-bike-review", "digits are kept"],
  [["--Already--hyphenated--"], "already-hyphenated", "hyphens at the ends"],
  [["!!!"], "", "nothing usable"],
  [[""], "", "empty"],
  [["Crème Brûlée"], "cr-me-br-l-e", "accented letters aren't a–z"],
  [["a  &  b"], "a-b", "a run of several characters becomes one hyphen"],
], { show: "slugify({0})" });
```
```js solution
function slugify(title) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")    // every run of other characters → one hyphen
    .replace(/^-+|-+$/g, "");       // trim hyphens at both ends
}

console.log(slugify("  Tubeless Tyres: A Beginner's Guide!  "));
```
hint: Methods can be chained: each returns a new string you can call the next method on.
hint: The regular expression `/[^a-z0-9]+/g` matches every run (`+`) of characters that are not (`^` inside brackets) lower-case letters or digits; the `g` flag means "all matches".
hint: `.replace(/[^a-z0-9]+/g, "-")` then `.replace(/^-+|-+$/g, "")` to remove hyphens at the start (`^-+`) or end (`-+$`).
approach:
1. **Understand:** a normalisation pipeline; every non-alphanumeric run collapses to one hyphen.
2. **Examples:** `": A "` is one run of three characters → one hyphen.
3. **Brute force:** loop over characters, tracking whether the last output was a hyphen: works, more code.
4. **Pattern:** **chained string transforms** with regular expressions.
5. **Plan:** lower-case → replace runs → trim hyphens.
6. **Code and test:** digits, hyphens at the ends, only punctuation, accents.
walkthrough:
**Line by line**

- `toLowerCase()` first, so the character class only needs `a-z`.
- `[^a-z0-9]+` with the `g` flag finds every run of other characters, including spaces, punctuation and accented letters, and replaces each run with a single `-`.
- `^-+|-+$` matches hyphens at the very start or end (the `|` means "or"); replacing them with `""` removes them.

**Trace:** `"Hello World"` → `"hello world"` → `"hello-world"` → no hyphens at the ends → `"hello-world"`.

**Common wrong approach:** `title.replaceAll(" ", "-")`, which keeps punctuation (`tyres:-a`) and turns double spaces into double hyphens. Real slug libraries also convert accented letters to plain ones first (`é` → `e`) with `normalize("NFD")` (Part 2).
:::

:::quiz
? What does `${a + b}` do inside backticks?
+ Inserts the value of a + b into the string
- Prints a dollar sign
- Creates a variable
= Template literals evaluate any expression inside ${…}.
? What does "bicycle".at(-1) return?
+ "e"
- undefined
- An error
= at() counts negative positions from the end; plain [-1] is undefined.
? Why does name.toUpperCase() alone not change name?
+ Strings are immutable; the method returns a new string
- toUpperCase only works on const strings
- It needs to be awaited
= Assign the result: name = name.toUpperCase().
? "🚲".length is 2. Why?
+ The emoji takes two UTF-16 code units
- Emoji are stored as two characters by mistake
- length counts bytes
= [..."🚲"].length counts real characters.
:::

@@@ lesson
id: numbers
title: Numbers and maths
minutes: 24
summary: JavaScript's single number type (64-bit floating point), why 0.1 + 0.2 isn't 0.3 and how to compare decimals, arithmetic operators and precedence, remainder and integer division, Math functions, rounding and toFixed, safe integers and BigInt, Infinity and NaN, and working with money in whole cents.
---
JavaScript has one main number type for whole numbers and decimals alike: a 64-bit **floating-point** number (the IEEE 754 standard, like Python's `float`). It also has **BigInt** for whole numbers of any size.

### Arithmetic

```js
console.log(7 + 2, 7 - 2, 7 * 2, 7 / 2);   // / always gives a decimal when needed
console.log(7 % 2, 2 ** 10);                // remainder, and power
console.log(2 + 3 * 4, (2 + 3) * 4);        // * before +; brackets first
let n = 5;
n += 2;      // n = n + 2
n *= 3;      // n = n * 3
n++;         // n = n + 1
console.log(n);
```

There's no integer-division operator. Use `Math.floor(a / b)` (rounds down) or `Math.trunc(a / b)` (drops the decimals, towards zero); they differ for negative numbers. The remainder `%` takes the sign of the left number: `-7 % 3` is `-1`, unlike Python's `-7 % 3 == 2`.

### Why 0.1 + 0.2 isn't 0.3

```js
console.log(0.1 + 0.2);
console.log(0.1 + 0.2 === 0.3);
console.log(Math.abs((0.1 + 0.2) - 0.3) < Number.EPSILON);   // fine near 1; the first exercise handles any size
```

Most decimals can't be stored exactly in binary, just as 1/3 can't be written exactly in decimal. The tiny errors are normal and happen in nearly every language. Two rules:

- **Never compare decimals with `===`**; check that they're close (the first exercise).
- **For money, count whole cents (or pence)** as integers, and only format as pounds or dollars for display.

### Math

```js
console.log(Math.round(2.5), Math.round(-2.5), Math.floor(-2.5), Math.ceil(2.1), Math.trunc(-2.9));
console.log(Math.max(3, 9, 4), Math.min(3, 9, 4), Math.abs(-7), Math.sqrt(16));
console.log(Math.PI.toFixed(2), (1234.5678).toFixed(1), typeof (1.5).toFixed(1));
console.log(Number.isInteger(5), Number.isInteger(5.5));
```

- `Math.round` rounds halves **up** (towards +∞): `Math.round(-2.5)` is `-2`.
- `toFixed(n)` returns a **string** with `n` decimals: perfect for display, wrong for further maths.
- `Math.random()` gives a random number from 0 (included) to 1 (not included).

### Very large and special numbers

```js
console.log(Number.MAX_SAFE_INTEGER);                    // 2⁵³ − 1
console.log(9007199254740992 + 1);                       // past the safe range: wrong!
console.log(9007199254740992n + 1n);                     // BigInt: exact
console.log(1 / 0, -1 / 0, 0 / 0);                       // Infinity, -Infinity, NaN
console.log(new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" }).format(1234.5));
```

- Integers are exact only up to `Number.MAX_SAFE_INTEGER` (about 9 quadrillion). IDs from databases or APIs can be bigger, which is why some APIs send them as strings.
- **BigInt** literals end in `n`. You can't mix BigInt and ordinary numbers in one operation without converting.
- Dividing by zero gives `Infinity`, not an error; `0 / 0` is `NaN`.
- `Intl.NumberFormat` formats numbers and currencies for any locale.

:::exercise Are two numbers close?
Write `isClose(a, b, tolerance = 1e-9)` returning `true` when the two numbers differ by at most `tolerance` **times the larger of their absolute values**, or by at most `tolerance` itself (so numbers near zero work too). `NaN` is never close to anything.
```js starter
function isClose(a, b, tolerance = 1e-9) {
  // your code here
}

console.log(isClose(0.1 + 0.2, 0.3), isClose(1, 1.1), isClose(1e20, 1e20 + 1e5));
// true false true
```
```js check
test("isClose", [
  [[0.1 + 0.2, 0.3], true, "0.1 + 0.2 and 0.3"],
  [[1, 1.1], false, "clearly different"],
  [[1e20, 1e20 + 1e5], true, "huge numbers with a tiny relative difference"],
  [[0, 1e-12], true, "near zero"],
  [[0, 1e-6], false, "not that close to zero"],
  [[5, 5], true, "equal"],
  [[NaN, NaN], false, "NaN"],
  [[1, 1.05, 0.1], true, "a looser tolerance"],
  [[100, 95, 0.01], false, "a 5% difference with a 1% tolerance"],
  [[-3, -3.0000000001], true, "negatives"],
], { show: "isClose({0}, {1})" });
```
```js solution
function isClose(a, b, tolerance = 1e-9) {
  if (Number.isNaN(a) || Number.isNaN(b)) return false;
  const diff = Math.abs(a - b);
  return diff <= tolerance * Math.max(Math.abs(a), Math.abs(b)) || diff <= tolerance;
}

console.log(isClose(0.1 + 0.2, 0.3), isClose(1, 1.1), isClose(1e20, 1e20 + 1e5));
```
hint: A fixed gap like `0.000001` is too strict for huge numbers and too loose for tiny ones. Scale it by the size of the numbers.
hint: Compute `diff = Math.abs(a - b)` and compare it with `tolerance * Math.max(Math.abs(a), Math.abs(b))`.
hint: Also accept `diff <= tolerance` for numbers near zero, and return `false` first if either is `NaN`.
approach:
1. **Understand:** a relative tolerance, plus an absolute one for values near zero.
2. **Examples:** 1e20 and 1e20 + 1e5 differ by 100,000, which is tiny compared with 1e20.
3. **Brute force:** `a === b`: fails on 0.1 + 0.2.
4. **Pattern:** **relative-plus-absolute tolerance**, as in Python's `math.isclose`.
5. **Plan:** NaN guard → difference → compare with both limits.
6. **Code and test:** near zero, huge values, negatives, NaN, custom tolerances.
walkthrough:
**Line by line**

- `NaN` comparisons are always false anyway, but the explicit guard documents the intent.
- `Math.abs(a - b)` is the size of the gap, whichever number is bigger.
- Multiplying the tolerance by the larger magnitude makes it **relative**: "within one part in a billion".
- `|| diff <= tolerance` handles values near zero, where a relative limit would be almost nothing.

**Trace:** `isClose(0, 1e-12)` → diff 1e-12; relative limit 1e-9 × 1e-12 is tiny, but 1e-12 ≤ 1e-9 → `true`.

**Common wrong approach:** `Math.abs(a - b) < Number.EPSILON`. `Number.EPSILON` (about 2.2e-16) is the gap between 1 and the next number; for values like 1000 the real rounding errors are far bigger, so the check fails when it shouldn't.
:::

:::exercise Format pence as pounds
Prices are stored as whole pence. Write `formatPence(pence)` returning text like `"£12.50"`:

- always two decimal places;
- a thousands separator for big amounts: `123456` → `"£1,234.56"`;
- negative amounts as `"-£3.05"`.

Do the arithmetic with whole numbers (no `toFixed` on a divided value).
```js starter
function formatPence(pence) {
  // your code here
}

console.log(formatPence(1250), formatPence(5), formatPence(123456), formatPence(-305));
// £12.50 £0.05 £1,234.56 -£3.05
```
```js check
test("formatPence", [
  [[1250], "£12.50", "a simple price"],
  [[5], "£0.05", "under a pound"],
  [[0], "£0.00", "zero"],
  [[100], "£1.00", "exactly a pound"],
  [[123456], "£1,234.56", "thousands"],
  [[100000000], "£1,000,000.00", "a million"],
  [[-305], "-£3.05", "negative"],
  [[99], "£0.99", "99p"],
], { show: "formatPence({0})" });
if (/toFixed/.test(__source__.replace(/\/\/.*$/gm, ""))) throw new AssertionError("Use whole-number arithmetic (Math.floor and %) rather than toFixed.");
```
```js solution
function formatPence(pence) {
  const sign = pence < 0 ? "-" : "";
  const abs = Math.abs(pence);
  const pounds = Math.floor(abs / 100);
  const rest = abs % 100;
  const withCommas = String(pounds).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return `${sign}£${withCommas}.${String(rest).padStart(2, "0")}`;
}

console.log(formatPence(1250), formatPence(5), formatPence(123456), formatPence(-305));
```
hint: Work with the absolute value and remember the sign separately. Pounds are `Math.floor(abs / 100)`, pence are `abs % 100`.
hint: Pad the pence to two digits with `String(rest).padStart(2, "0")`.
hint: For commas, either loop from the right adding a comma every three digits, or use `pounds.toLocaleString("en-GB")`, or the regular expression `/\B(?=(\d{3})+(?!\d))/g`.
approach:
1. **Understand:** integer pence → sign, pounds, two-digit pence, commas.
2. **Examples:** 123456 → 1234 pounds and 56 pence → "1,234" + ".56".
3. **Brute force:** divide by 100 and use `toFixed(2)`: works for these values but relies on floating point, which bites with larger amounts and further arithmetic.
4. **Pattern:** **split an integer into units** with division and remainder.
5. **Plan:** sign → absolute value → pounds and pence → commas → padded pence → assemble.
6. **Code and test:** zero, under a pound, exact pounds, millions, negatives.
walkthrough:
**Line by line**

- Taking the sign first means the maths only deals with positive numbers, avoiding `%` surprises with negatives.
- `Math.floor(abs / 100)` and `abs % 100` split pence into pounds and remainder exactly, since both are integers.
- The regular expression inserts a comma at every position followed by groups of exactly three digits to the end (regular expressions are in Part 3); `toLocaleString("en-GB")` is the everyday alternative.
- `padStart(2, "0")` turns 5 into `"05"`.

**Trace:** −305 → sign "-", abs 305 → 3 pounds, 5 pence → "-£3.05".

**Common wrong approach:** `"£" + pence / 100`, which prints `£12.5` for 1250 and `£0.05` only by luck. In real apps, `new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" }).format(pence / 100)` formats safely for display.
:::

:::quiz
? Why should you avoid comparing decimals with ===?
+ Most decimals aren't stored exactly, so tiny rounding errors appear
- === doesn't work on numbers
- Decimals are strings in JavaScript
= Compare with a tolerance instead.
? What type does (1.5).toFixed(1) return?
+ string
- number
- bigint
= toFixed is for display; it returns text.
? What is -7 % 3 in JavaScript?
+ -1
- 2
- 1
= The remainder takes the sign of the left-hand number.
? Why store money as whole pence or cents?
+ Integers are exact, so sums don't pick up rounding errors
- It uses less memory
- JavaScript can't store decimals
= Convert to pounds only when displaying.
:::

@@@ lesson
id: conditions
title: Comparisons and conditions
minutes: 26
summary: Comparison operators, strict (===) versus loose (==) equality, truthy and falsy values, the logical operators &&, || and !, the nullish operators ?? and ??=, optional chaining with ?., if / else if / else, the conditional (ternary) operator, and switch.
---
Programs make decisions by comparing values and branching on the result.

### Comparisons

| Operator | Means |
|---|---|
| `===`, `!==` | strictly equal / not equal: same type **and** same value |
| `==`, `!=` | loosely equal: converts types first (avoid) |
| `<`, `>`, `<=`, `>=` | ordering |

```js
console.log(5 === 5, 5 === "5", 5 == "5");
console.log(0 == "", null == undefined, null === undefined);
console.log("10" < "9", 10 < 9);       // strings compare character by character
```

**Always use `===` and `!==`.** Loose `==` converts types by complicated rules (`0 == ""` is `true`!). The one common exception some style guides allow is `x == null`, which is true for both `null` and `undefined`.

Objects (including arrays) compare by **identity**, not contents: `[1] === [1]` is `false`, because they're two different arrays (Part 2).

### Truthy and falsy

Anywhere JavaScript expects a true/false value, it converts. Exactly these values are **falsy**:

`false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`

Everything else is **truthy**, including `"0"`, `"false"`, `[]` and `{}`.

```js
const answers = [0, "", "0", [], null, "hi", NaN];
for (const v of answers) {
  const shown = typeof v === "string" ? `"${v}"` : v;
  console.log(shown, v ? "truthy" : "falsy");
}
```

### Logical operators

`&&` (and), `||` (or) and `!` (not) combine conditions. They **short-circuit**: the right side runs only if needed, and the result is one of the operands, not necessarily `true` or `false`:

```js
console.log(true && "yes", 0 && "yes");       // && gives the first falsy value, or the last value
console.log("" || "default", "set" || "default");   // || gives the first truthy value
console.log(!true, !!"text");                 // !! converts to a boolean
```

### Defaults: `||` versus `??`

`a || b` falls back for **any** falsy `a`, including `0` and `""`, which are often real values. The **nullish coalescing** operator `a ?? b` falls back only when `a` is `null` or `undefined`:

```js
const order = { quantity: 0, note: "" };
console.log(order.quantity || 1, order.quantity ?? 1);   // 1 versus 0
console.log(order.note || "(none)", order.note ?? "(none)");
let discount;
discount ??= 0.1;              // assign only if null or undefined
console.log(discount);
```

### Optional chaining: `?.`

Reading a property of `undefined` throws a `TypeError`. `?.` stops early and gives `undefined` instead:

```js
const customer = { name: "Ada", address: null };
console.log(customer.address?.city);           // undefined, no error
console.log(customer.address?.city ?? "unknown city");
console.log(customer.greet?.());               // call a method only if it exists
```

### if, else if, else

```js
function shippingCost(total) {
  if (total >= 50) {
    return 0;
  } else if (total >= 20) {
    return 2.99;
  } else {
    return 4.99;
  }
}
console.log(shippingCost(65), shippingCost(30), shippingCost(5));
```

Conditions are checked top to bottom, and the first true branch wins, so put the most specific conditions first. Always use braces `{ }`, even for one-line branches; it prevents a classic bug when a second line is added later.

### The conditional (ternary) operator

`condition ? a : b` is an **expression** that picks a value, handy inside template literals and assignments:

```js
const stock = 0;
console.log(`Status: ${stock > 0 ? "in stock" : "sold out"}`);
```

Keep ternaries short; nested ones are hard to read, so use `if` instead.

### switch

`switch` compares one value against several cases with `===`:

```js
function sizeLabel(code) {
  switch (code) {
    case "S":
      return "Small";
    case "M":
      return "Medium";
    case "L":
    case "XL":                 // two cases sharing one result
      return "Large";
    default:
      return "Unknown size";
  }
}
console.log(sizeLabel("M"), sizeLabel("XL"), sizeLabel("XXL"));
```

Without `return` or `break`, execution **falls through** into the next case. Forgetting `break` is a common bug; returning from each case, as above, avoids it.

:::exercise Grade a score
Write `grade(score)` returning a letter: `"A"` for 90–100, `"B"` for 80–89.99…, `"C"` for 70 up to 80, `"D"` for 60 up to 70, and `"F"` below 60. Scores outside 0–100, or anything that isn't a number (including `NaN`), give `"invalid"`.
```js starter
function grade(score) {
  // your code here
}

console.log(grade(95), grade(80), grade(79.5), grade(12), grade(101), grade("90"));
// A B C F invalid invalid
```
```js check
test("grade", [
  [[95], "A", "95"], [[90], "A", "exactly 90"], [[100], "A", "100"],
  [[89.99], "B", "89.99"], [[80], "B", "exactly 80"],
  [[79.5], "C", "79.5"], [[70], "C", "70"],
  [[69], "D", "69"], [[60], "D", "60"],
  [[59.9], "F", "59.9"], [[0], "F", "zero"],
  [[-1], "invalid", "negative"], [[101], "invalid", "over 100"],
  [["90"], "invalid", "a string"], [[NaN], "invalid", "NaN"], [[undefined], "invalid", "undefined"],
], { show: "grade({0})" });
```
```js solution
function grade(score) {
  if (typeof score !== "number" || Number.isNaN(score) || score < 0 || score > 100) {
    return "invalid";
  }
  if (score >= 90) return "A";
  if (score >= 80) return "B";
  if (score >= 70) return "C";
  if (score >= 60) return "D";
  return "F";
}

console.log(grade(95), grade(80), grade(79.5), grade(12), grade(101), grade("90"));
```
hint: Reject invalid input first, then check the bands from the top down.
hint: `typeof score !== "number"` rejects strings and `undefined`; `NaN` is a number, so test it with `Number.isNaN`.
hint: With the invalid cases gone, `if (score >= 90) return "A"; if (score >= 80) return "B"; …` works because each check only runs if the ones above failed.
approach:
1. **Understand:** five bands plus an invalid case; boundaries belong to the higher grade.
2. **Examples:** exactly 80 → B; 79.5 → C.
3. **Brute force:** each band with both bounds (`score >= 80 && score < 90`): works, but repetitive.
4. **Pattern:** **guard clause, then ordered thresholds**.
5. **Plan:** validate → test thresholds from highest down → default F.
6. **Code and test:** every boundary, decimals, strings, NaN, undefined.
walkthrough:
**Line by line**

- The guard combines all invalid cases; `"90"` is rejected even though `"90" >= 90` would be `true` (JavaScript would convert it).
- Returning early means each later `if` only needs a lower bound: if `score >= 90` failed, the score is below 90.
- The final `return "F"` covers 0 up to 60.

**Trace:** `grade(79.5)` → valid → not ≥ 90, not ≥ 80, ≥ 70 → `"C"`.

**Common wrong approach:** checking `score > 90` instead of `>=`, so exactly 90 drops to B. Boundary values are where grading bugs live: always test them.
:::

:::exercise Delivery details with defaults
An order object may be missing details. Write `deliveryLabel(order)` returning `"<name>: <city> (<days> days)"` where:

- `name` is `order.customer.name`, or `"Guest"` if the customer or name is missing;
- `city` is `order.customer.address.city`, or `"no address"` if any part is missing;
- `days` is `order.days`, defaulting to `3` **only** when it's `null` or `undefined` (0 is a valid number of days).
```js starter
function deliveryLabel(order) {
  // your code here
}

console.log(deliveryLabel({ customer: { name: "Ada", address: { city: "Bristol" } }, days: 0 }));
// Ada: Bristol (0 days)
console.log(deliveryLabel({}));
// Guest: no address (3 days)
```
```js check
test("deliveryLabel", [
  [[{ customer: { name: "Ada", address: { city: "Bristol" } }, days: 0 }], "Ada: Bristol (0 days)", "0 days is kept"],
  [[{}], "Guest: no address (3 days)", "an empty order"],
  [[{ customer: { name: "Bo" }, days: 2 }], "Bo: no address (2 days)", "no address"],
  [[{ customer: { address: { city: "Leeds" } } }], "Guest: Leeds (3 days)", "no name"],
  [[{ customer: null, days: null }], "Guest: no address (3 days)", "null customer and days"],
  [[{ customer: { name: "", address: { city: "York" } }, days: 1 }], ": York (1 days)", "an empty name is still a name"],
  [[{ customer: { name: "Cy", address: null }, days: 5 }], "Cy: no address (5 days)", "null address"],
], { show: "deliveryLabel({0})" });
```
```js solution
function deliveryLabel(order) {
  const name = order.customer?.name ?? "Guest";
  const city = order.customer?.address?.city ?? "no address";
  const days = order.days ?? 3;
  return `${name}: ${city} (${days} days)`;
}

console.log(deliveryLabel({ customer: { name: "Ada", address: { city: "Bristol" } }, days: 0 }));
console.log(deliveryLabel({}));
```
hint: Optional chaining `?.` reads nested properties without crashing when something along the way is `null` or `undefined`.
hint: Use `??` (not `||`) for defaults, so `0` days and an empty-string name are kept.
hint: `const city = order.customer?.address?.city ?? "no address";`, then build the string with a template literal.
approach:
1. **Understand:** safe nested reads, and defaults only for missing values.
2. **Examples:** `days: 0` must stay 0; `days: null` becomes 3.
3. **Brute force:** nested `if (order.customer && order.customer.address && …)` checks: works, but long.
4. **Pattern:** **optional chaining plus nullish coalescing**.
5. **Plan:** three safe reads with defaults → template literal.
6. **Code and test:** each missing level, null versus undefined, falsy-but-valid values.
walkthrough:
**Line by line**

- `order.customer?.name` gives `undefined` (instead of throwing) when `customer` is `null` or `undefined`.
- `?? "Guest"` applies only when the result is `null` or `undefined`; an empty name `""` is kept, as the specification says.
- `order.days ?? 3` keeps `0`, where `order.days || 3` would wrongly replace it.

**Trace:** `{ customer: null, days: null }` → name: `null?.name` → `undefined` → "Guest"; city likewise → "no address"; days: `null ?? 3` → 3.

**Common wrong approach:** `order.days || 3`, which turns a same-day order (0 days) into 3 days. Use `||` only when every falsy value should be replaced.
:::

:::quiz
? Why prefer === over ==?
+ === doesn't convert types, so there are no surprising matches like 0 == ""
- === is faster to type
- == doesn't work on strings
= Use === and !== everywhere.
? Which of these is truthy?
+ "0"
- 0
- ""
- null
= Any non-empty string is truthy, even "0" and "false".
? What does 0 ?? 5 evaluate to?
+ 0
- 5
- null
= ?? only falls back for null and undefined.
? What happens if a switch case has no break or return?
+ Execution falls through into the next case
- JavaScript adds a break automatically
- It's a syntax error
= Return from each case, or add break.
:::

@@@ lesson
id: loops
title: Loops
minutes: 24
summary: Repeating work with for, while and do…while, looping over values with for…of and over keys with for…in, break and continue, loop counters and accumulators, nested loops, avoiding off-by-one and endless loops, and a first look at array methods as an alternative.
---
A **loop** repeats a block of code. JavaScript has several kinds; you'll mostly use `for…of` and the classic `for`.

### for…of: each value

```js
const parts = ["frame", "wheels", "saddle"];
for (const part of parts) {
  console.log(`Checking the ${part}`);
}
for (const ch of "hey") {
  console.log(ch);
}
```

`for…of` works on anything **iterable**: arrays, strings, Maps, Sets and more (Part 3). Use `const` for the loop variable unless you reassign it inside the loop.

### The classic for loop: counting

```js
for (let i = 0; i < 5; i++) {
  console.log("i is", i);
}
for (let i = 10; i > 0; i -= 3) {
  console.log("countdown", i);
}
```

The three parts in the brackets are: start (`let i = 0`), keep going while (`i < 5`), and step (`i++`, run after each pass). Use it when you need the position, a different step, or to go backwards.

### while and do…while

```js
let balance = 100;
let years = 0;
while (balance < 200) {
  balance *= 1.07;      // 7% growth a year
  years++;
}
console.log(`Doubles after ${years} years: £${balance.toFixed(2)}`);

let tries = 0;
do {
  tries++;
} while (tries < 0);    // the body runs once even though the condition is false
console.log("tries:", tries);
```

Use `while` when you don't know in advance how many passes you need. Make sure something in the body moves towards the end: a loop whose condition never becomes false runs forever (press **Stop**).

### break and continue

```js
const temps = [12, 15, -3, 18, 99, 20];
for (const t of temps) {
  if (t < 0) continue;       // skip this value, go on with the next
  if (t > 50) break;         // stop the loop entirely
  console.log(t);
}
```

### for…in: an object's keys

```js
const stock = { tubes: 12, tyres: 4, bells: 0 };
for (const item in stock) {
  console.log(item, stock[item]);
}
```

`for…in` loops over an object's **keys**. Don't use it on arrays: it gives the indexes as strings and can include extra properties. For arrays use `for…of`; for objects, `Object.entries` (Part 2) is often clearer.

### Accumulators

Many loops build a result step by step in an **accumulator** variable:

```js
const prices = [6, 12.5, 30];
let total = 0;
let most = -Infinity;
for (const p of prices) {
  total += p;
  if (p > most) most = p;
}
console.log("total", total, "most expensive", most);
```

Part 2 shows array methods (`reduce`, `map`, `filter`) that express many such loops in one line. Loops remain clearer when the logic has several steps or needs `break`.

### Off-by-one errors

The most common loop bug is running one time too many or too few. With `for (let i = 0; i < n; i++)`, `i` goes from `0` to `n − 1`, which is exactly the valid indexes of an array of length `n`. Writing `i <= n` reads one past the end (and gives `undefined`, not an error).

:::exercise Count the vowels
Write `countVowels(text)` returning how many vowels (`a`, `e`, `i`, `o`, `u`, in either case) the text contains.
```js starter
function countVowels(text) {
  // your code here
}

console.log(countVowels("Spoke & Chain"), countVowels("RHYTHM"), countVowels(""));
// 4 0 0
```
```js check
test("countVowels", [
  [["Spoke & Chain"], 4, "mixed case"],
  [["RHYTHM"], 0, "no vowels"],
  [[""], 0, "empty"],
  [["AEIOUaeiou"], 10, "every vowel"],
  [["queueing"], 5, "repeated vowels"],
  [["bike 2026!"], 2, "digits and punctuation"],
], { show: "countVowels({0})" });
```
```js solution
function countVowels(text) {
  let count = 0;
  for (const ch of text.toLowerCase()) {
    if ("aeiou".includes(ch)) count++;
  }
  return count;
}

console.log(countVowels("Spoke & Chain"), countVowels("RHYTHM"), countVowels(""));
```
hint: Loop over the characters with `for (const ch of text)`, and keep a counter.
hint: Lower-case the text first, so you only need to check five letters.
hint: `if ("aeiou".includes(ch)) count++;`
approach:
1. **Understand:** count characters that are vowels, ignoring case.
2. **Examples:** "Spoke & Chain" → o, e, a, i = 4.
3. **Brute force:** five separate counts, one per vowel: works, more code.
4. **Pattern:** **accumulator loop with a membership test**.
5. **Plan:** counter = 0 → loop over lower-cased characters → add 1 for each vowel.
6. **Code and test:** upper case, empty text, no vowels, punctuation.
walkthrough:
**Line by line**

- `text.toLowerCase()` once, before the loop, rather than for every character.
- `for…of` over a string gives one character per pass.
- `"aeiou".includes(ch)` asks whether the character is one of the five vowels.

**Trace:** "RHYTHM" → "rhythm" → no character is in "aeiou" → 0.

**Common wrong approach:** `for (let i = 0; i <= text.length; i++)`, which reads `text[text.length]`, an `undefined` one past the end. Here `"aeiou".includes(undefined)` happens to be false, which hides the bug; in other loops it causes errors.
:::

:::exercise How many years to a target?
Savings grow by `rate` per year (0.05 means 5%), compounded yearly. Write `yearsToTarget(start, rate, target)` returning how many **whole years** it takes for the balance to reach at least `target`. If `start` already reaches the target, return `0`. If the balance can never reach it (`rate <= 0` and `start < target`), return `-1` instead of looping forever.
```js starter
function yearsToTarget(start, rate, target) {
  // your code here
}

console.log(yearsToTarget(100, 0.07, 200), yearsToTarget(500, 0.05, 400), yearsToTarget(100, 0, 200));
// 11 0 -1
```
```js check
test("yearsToTarget", [
  [[100, 0.07, 200], 11, "doubling at 7%"],
  [[500, 0.05, 400], 0, "already there"],
  [[100, 0, 200], -1, "no growth"],
  [[100, -0.1, 200], -1, "shrinking"],
  [[100, 0.1, 110], 1, "exactly one year (allowing for rounding)"],
  [[1000, 0.03, 1000], 0, "start equals the target"],
  [[1, 1, 1024], 10, "doubling every year"],
  [[100, 0.5, 100.01], 1, "just above"],
], { show: "yearsToTarget({0}, {1}, {2})" });
```
```js solution
function yearsToTarget(start, rate, target) {
  if (start >= target) return 0;
  if (rate <= 0) return -1;            // it would never get there
  let balance = start;
  let years = 0;
  while (balance < target - 1e-9) {     // a tiny allowance for floating-point rounding
    balance *= 1 + rate;
    years++;
  }
  return years;
}

console.log(yearsToTarget(100, 0.07, 200), yearsToTarget(500, 0.05, 400), yearsToTarget(100, 0, 200));
```
hint: You don't know the number of years in advance, so use a `while` loop that runs while the balance is below the target.
hint: Handle the two special cases before the loop: already at the target (0), and a rate of 0 or less (−1).
hint: Each pass: `balance *= 1 + rate; years++;`. Compare with a tiny allowance (`balance < target - 1e-9`), because 100 × 1.1 is 110.00000000000001… or sometimes just under.
approach:
1. **Understand:** repeat a growth step until a condition holds, counting the steps; guard against endless loops.
2. **Examples:** 100 at 7%: 107, 114.49, … reaches 200 after 11 years (196.72 after 10).
3. **Brute force:** loop up to a large fixed number of years: hides the "never" case.
4. **Pattern:** **while loop with a counter and guard clauses**.
5. **Plan:** start ≥ target → 0; rate ≤ 0 → −1; loop.
6. **Code and test:** already there, no growth, shrinking, exact boundaries.
walkthrough:
**Line by line**

- The first guard returns 0 without looping when there's nothing to do.
- The second guard is what prevents an endless loop: with no growth, `balance < target` would stay true forever.
- `balance *= 1 + rate` applies one year's growth; `years++` counts it.
- The `- 1e-9` allowance means a balance that should equal the target exactly (110 after one year at 10%) isn't missed because of a rounding error in the last decimal place.

**Trace:** (1, 1, 1024) → balance doubles: 2, 4, …, 1024 after 10 passes → 10.

**Common wrong approach:** no guard for `rate <= 0`. The loop runs forever and the page (or here, the sandbox) hangs. Every `while` loop needs a reason to be sure it ends.
:::

:::quiz
? Which loop is the simplest way to visit every item of an array?
+ for (const item of items)
- for (const item in items)
- do … while
= for…in gives keys (indexes as strings), not values.
? With for (let i = 0; i < arr.length; i++), what is the last value of i inside the loop?
+ arr.length - 1
- arr.length
- arr.length + 1
= Exactly the last valid index.
? What does continue do?
+ Skips the rest of this pass and moves to the next one
- Ends the loop
- Restarts the loop from the beginning
= break ends the loop; continue skips one pass.
? What must every while loop have?
+ Something in the body that eventually makes the condition false
- A counter called i
- A break statement
= Otherwise it runs forever.
:::

@@@ lesson
id: functions
title: Functions
minutes: 26
summary: Function declarations, function expressions and arrow functions, parameters and arguments, return values and undefined, default and rest parameters, spreading arguments, hoisting, functions as values, callbacks and higher-order functions, and writing small, single-purpose functions.
---
A **function** is a named, reusable block of code. You give it inputs (**parameters**), it does some work, and it can **return** a result.

### Three ways to write a function

```js
// 1. A function declaration
function vatOf(net) {
  return net * 0.2;
}

// 2. A function expression stored in a const
const withVat = function (net) {
  return net + vatOf(net);
};

// 3. An arrow function: shorter, and common for small functions
const formatPrice = (amount) => `£${amount.toFixed(2)}`;

console.log(vatOf(50), withVat(50), formatPrice(withVat(50)));
```

Arrow functions have a short form: with a single expression and no braces, the value is returned automatically. With braces you need `return`:

```js
const double = (n) => n * 2;          // returns n * 2
const triple = (n) => { n * 3; };     // braces and no return: returns undefined!
const square = (n) => { return n * n; };
console.log(double(4), triple(4), square(4));
```

Arrow functions also treat `this` differently (Part 3); for now, use declarations for named, top-level functions and arrows for short callbacks.

### Parameters, arguments and return

```js
function greet(name, greeting = "Hello") {      // a default value
  return `${greeting}, ${name}!`;
}
console.log(greet("Ada"));
console.log(greet("Grace", "Welcome"));
console.log(greet());                          // a missing argument is undefined
function noReturn() {}
console.log(noReturn());                       // no return statement gives undefined
```

- JavaScript doesn't check the number of arguments: missing ones are `undefined`, extra ones are ignored.
- A **default parameter** is used when the argument is missing or `undefined` (but not when it's `null`).
- `return` ends the function immediately.

### Any number of arguments: rest and spread

```js
function total(...prices) {        // rest parameter: collects the arguments into an array
  let sum = 0;
  for (const p of prices) sum += p;
  return sum;
}
console.log(total(), total(5), total(5, 10, 2.5));

const basket = [6, 12, 30];
console.log(total(...basket));     // spread: turns an array into separate arguments
console.log(Math.max(...basket));
```

### Hoisting

Function **declarations** are **hoisted**: you can call them before the line where they appear. Function expressions and arrow functions stored in `const` or `let` can't be used before their line.

```js error
console.log(early(2));            // works: declarations are hoisted
function early(n) { return n + 1; }

console.log(late(2));             // ReferenceError: can't use before initialisation
const late = (n) => n + 1;
```

### Functions are values

Functions can be stored in variables, put in arrays and objects, passed to other functions and returned from them. A function passed to another function is a **callback**; a function that takes or returns functions is a **higher-order function**.

```js
function applyTwice(fn, value) {
  return fn(fn(value));
}
const addTen = (n) => n + 10;
console.log(applyTwice(addTen, 1));
console.log(applyTwice((s) => s + "!", "Hi"));

const prices = [12, 5, 30];
console.log(prices.map((p) => p * 2));          // map calls the callback for every item (Part 2)
setTimeout(() => console.log("a callback, run later"), 10);
```

### Good functions

- **Do one thing**, and name it with a verb for what it does: `calculateTotal`, `formatPrice`, `isValidEmail`.
- **Return values** instead of printing them; the caller decides what to do with the result (and tests can check it).
- Keep them **short**: if you need a comment to explain a section, it may want to be its own function.

:::exercise A discount calculator
Write `applyDiscount(price, percent = 10)` returning the price after taking off `percent` per cent, **rounded to 2 decimal places**. If `percent` is outside 0–100, throw a `RangeError` with any message (`throw new RangeError("…")`).
```js starter
function applyDiscount(price, percent = 10) {
  // your code here
}

console.log(applyDiscount(50), applyDiscount(19.99, 25), applyDiscount(80, 0));
// 45 14.99 80
```
```js check
test("applyDiscount", [
  [[50], 45, "the default 10%"],
  [[19.99, 25], 14.99, "25% off, rounded"],
  [[80, 0], 80, "no discount"],
  [[80, 100], 0, "free"],
  [[9.99, 33], 6.69, "rounding 6.6933"],
  [[0.1, 50], 0.05, "small amounts"],
], { show: "applyDiscount({0}, …)" });
const f = need("applyDiscount", "function");
for (const bad of [-5, 101, 150]) {
  let threw = null;
  try { f(10, bad); } catch (e) { threw = e; }
  if (!(threw instanceof RangeError)) throw new AssertionError(`applyDiscount(10, ${bad}) should throw a RangeError.`);
}
```
```js solution
function applyDiscount(price, percent = 10) {
  if (percent < 0 || percent > 100) {
    throw new RangeError(`percent must be between 0 and 100, not ${percent}`);
  }
  const discounted = price * (1 - percent / 100);
  return Math.round(discounted * 100) / 100;
}

console.log(applyDiscount(50), applyDiscount(19.99, 25), applyDiscount(80, 0));
```
hint: A default parameter is written `percent = 10` in the parameter list, so you only handle the calculation.
hint: To round to 2 decimal places as a number: `Math.round(x * 100) / 100` (`toFixed` would return a string).
hint: Before calculating: `if (percent < 0 || percent > 100) throw new RangeError("…");`
approach:
1. **Understand:** validate the percentage, apply it, round to pence.
2. **Examples:** 19.99 × 0.75 = 14.9925 → 14.99.
3. **Brute force:** `toFixed(2)` returns text, so the result wouldn't be a number.
4. **Pattern:** **guard clause + calculation + rounding**.
5. **Plan:** check range → multiply by (1 − p/100) → round.
6. **Code and test:** default, 0%, 100%, rounding cases, invalid percentages.
walkthrough:
**Line by line**

- The default parameter supplies 10 when the caller passes only a price.
- `throw new RangeError(...)` stops the function and signals bad input; Part 3 shows how callers can catch it.
- `price * (1 - percent / 100)` keeps the calculation in one step.
- `Math.round(x * 100) / 100` rounds to the nearest hundredth and stays a number.

**Trace:** `applyDiscount(9.99, 33)` → 9.99 × 0.67 = 6.6933 → 669.33 → 669 → 6.69.

**Common wrong approach:** printing the result with `console.log` instead of returning it: the function then returns `undefined`, and nothing else can use the value. (In real shops, prices are kept in whole pence to avoid rounding drift: Lesson 4.)
:::

:::exercise Run a function n times
Write `repeatCall(fn, times)` that calls `fn` the given number of times, passing the call number (starting at 1) each time, and returns an **array of the results**. `times` of 0 or less gives `[]`.
```js starter
function repeatCall(fn, times) {
  // your code here
}

console.log(repeatCall((n) => n * n, 4));       // [ 1, 4, 9, 16 ]
console.log(repeatCall(() => "hi", 2));         // [ 'hi', 'hi' ]
```
```js check
test("repeatCall", [
  [[(n) => n * n, 4], [1, 4, 9, 16], "squares"],
  [[() => "hi", 2], ["hi", "hi"], "a function that ignores its argument"],
  [[(n) => n, 0], [], "zero times"],
  [[(n) => n, -3], [], "negative"],
  [[(n) => `#${n}`, 3], ["#1", "#2", "#3"], "labels"],
], { show: "repeatCall(fn, {1})" });
const r = need("repeatCall", "function");
let calls = 0;
r(() => calls++, 5);
same(calls, 5, "The number of times your function called fn");
```
```js solution
function repeatCall(fn, times) {
  const results = [];
  for (let i = 1; i <= times; i++) {
    results.push(fn(i));
  }
  return results;
}

console.log(repeatCall((n) => n * n, 4));
console.log(repeatCall(() => "hi", 2));
```
hint: `fn` is a function like any other: call it with `fn(i)`.
hint: Start with an empty array, and add each result with `results.push(value)`.
hint: `for (let i = 1; i <= times; i++) results.push(fn(i));` — when `times` is 0 or negative, the loop doesn't run at all.
approach:
1. **Understand:** call a passed-in function repeatedly and collect what it returns.
2. **Examples:** n × n for n = 1…4 → [1, 4, 9, 16].
3. **Brute force:** this is already one loop.
4. **Pattern:** **higher-order function**: a function that receives another function.
5. **Plan:** empty array → loop 1…times → push fn(i) → return.
6. **Code and test:** zero, negative, functions that ignore the argument, count the calls.
walkthrough:
**Line by line**

- `fn` is just a parameter whose value happens to be a function, so `fn(i)` calls it.
- The loop starts at 1 because the call numbers start at 1; `i <= times` includes the last call.
- For `times` ≤ 0 the condition is false at once, so the empty array comes back without a special case.

**Trace:** `repeatCall((n) => n * n, 4)` → i = 1, 2, 3, 4 → push 1, 4, 9, 16.

**Common wrong approach:** `results.push(fn)`, which stores the function itself four times instead of calling it. The parentheses are what make a call.
:::

:::quiz
? What does const f = (n) => { n * 2; }; return?
+ undefined, because braces need an explicit return
- n * 2
- An error
= Without braces, (n) => n * 2 returns the value.
? A function is called with fewer arguments than it has parameters. What happens?
+ The missing parameters are undefined (or their default value)
- A TypeError is thrown
- JavaScript refuses to run the code
= JavaScript doesn't check argument counts.
? Which can be called before the line where it's defined?
+ A function declaration: function f() {}
- const f = () => {}
- let f = function () {}
= Declarations are hoisted.
? What does ...prices in a parameter list do?
+ Collects the remaining arguments into an array
- Copies an object
- Makes the parameter optional
= Rest parameters gather arguments; spread does the opposite.
:::

@@@ lesson
id: scope-and-closures
title: Scope and closures
minutes: 26
summary: Global, function and block scope, shadowing, why let and const replaced var, the temporal dead zone, closures (functions that remember their surroundings), private state with closures, counters, once and memoize patterns, and the classic loop-closure bug.
---
**Scope** is where a name can be seen. JavaScript finds a variable by looking in the current block, then the block around it, and so on outwards: a chain of scopes, decided by where the code is **written** (lexical scope).

### Block, function and global scope

```js
const shop = "Spoke & Chain";          // global (top-level) scope

function report() {
  const items = 3;                     // function scope: only inside report
  if (items > 0) {
    const message = `${shop} has ${items} items`;   // block scope: only inside these braces
    console.log(message);
  }
  // console.log(message);  would be a ReferenceError here
}
report();
```

`let` and `const` are **block-scoped**: they exist only inside the nearest `{ }`. An inner scope can read outer names, but not the other way round.

### Shadowing

An inner variable with the same name as an outer one **shadows** it inside the block:

```js
const price = 10;
{
  const price = 99;      // a different variable, only in this block
  console.log("inner", price);
}
console.log("outer", price);
```

Legal, but confusing; linters (Part 7) can warn about it.

### Why not var?

`var` is **function-scoped**, not block-scoped, and is hoisted with the value `undefined`, so mistakes go unnoticed:

```js
function example() {
  console.log(early);       // undefined, not an error: var is hoisted
  var early = 1;
  if (true) {
    var leaked = "visible outside the block";
  }
  console.log(leaked);
}
example();
```

`let` and `const` are also hoisted, but they can't be used before their line: that zone is the **temporal dead zone**, and using them there is a `ReferenceError`, which is what you want.

### Closures

A function keeps access to the variables of the scope it was **created** in, even after that scope has finished running. That combination of a function and its remembered variables is a **closure**:

![A diagram of makeCounter. The call to makeCounter creates a scope containing count = 0. The inner function increment is returned and stored as counterA; it keeps a link to that scope. A second call creates a separate scope with its own count, linked to counterB. Calling counterA twice raises its count to 2 while counterB's count stays independent](figures/closure.svg)

```js
function makeCounter() {
  let count = 0;                     // private: nothing outside can touch it directly
  return () => {
    count++;
    return count;
  };
}
const counterA = makeCounter();
const counterB = makeCounter();
console.log(counterA(), counterA(), counterA());   // 1 2 3
console.log(counterB());                           // 1: its own count
```

Each call to `makeCounter` creates a new `count`, and the returned arrow function closes over it. Closures give you **private state** without classes, and they're everywhere in JavaScript: event handlers, callbacks, React hooks and more.

### Patterns built from closures

```js
function makeGreeter(greeting) {
  return (name) => `${greeting}, ${name}!`;     // remembers greeting
}
const hello = makeGreeter("Hello");
const hola = makeGreeter("Hola");
console.log(hello("Ada"), hola("Grace"));

function memoize(fn) {
  const cache = new Map();                      // remembered between calls
  return (n) => {
    if (!cache.has(n)) cache.set(n, fn(n));
    return cache.get(n);
  };
}
const slowSquare = (n) => { console.log(`computing ${n}…`); return n * n; };
const fastSquare = memoize(slowSquare);
console.log(fastSquare(9), fastSquare(9));      // computes only once
```

### The loop-closure bug (and why `let` fixes it)

```js
const withVar = [], withLet = [];
for (var i = 0; i < 3; i++) withVar.push(() => i);
for (let j = 0; j < 3; j++) withLet.push(() => j);
console.log(withVar.map((f) => f()));   // [ 3, 3, 3 ]: one shared i
console.log(withLet.map((f) => f()));   // [ 0, 1, 2 ]: a new j for every pass
```

With `var`, every function closes over the **same** variable, which is 3 by the time they run. `let` creates a fresh binding for each pass of the loop. One more reason to never use `var`.

:::exercise A function that runs once
Write `once(fn)` returning a new function that calls `fn` (with whatever arguments it receives) the **first** time it's called, and on every later call returns that first result without calling `fn` again.
```js starter
function once(fn) {
  // your code here
}

const init = once((name) => { console.log("setting up", name); return 42; });
console.log(init("db"), init("cache"), init());
// setting up db
// 42 42 42
```
```js check
const o = need("once", "function");
let calls = 0;
const f = o((a, b) => { calls++; return a + b; });
same(f(2, 3), 5, "The first call's result");
same(f(10, 10), 5, "A later call's result");
same(f(), 5, "A call with no arguments");
same(calls, 1, "The number of times fn ran");
let calls2 = 0;
const g = o(() => { calls2++; return undefined; });
g(); g(); g();
same(calls2, 1, "How many times fn ran when it returns undefined");
const h1 = o(() => "first"), h2 = o(() => "second");
same([h1(), h2(), h1()], ["first", "second", "first"], "Two separate once-functions");
```
```js solution
function once(fn) {
  let called = false;
  let result;
  return (...args) => {
    if (!called) {
      called = true;
      result = fn(...args);
    }
    return result;
  };
}

const init = once((name) => { console.log("setting up", name); return 42; });
console.log(init("db"), init("cache"), init());
```
hint: The returned function needs to remember two things between calls: whether `fn` has run, and its result. Keep them in variables inside `once`.
hint: Use a separate boolean (`called`) rather than checking `result === undefined`, because `fn` might genuinely return `undefined`.
hint: `return (...args) => { if (!called) { called = true; result = fn(...args); } return result; };`
approach:
1. **Understand:** a wrapper that remembers state across calls: has it run, and what did it return?
2. **Examples:** the second `init("cache")` returns 42 without printing.
3. **Brute force:** a global flag: breaks as soon as you make two once-functions.
4. **Pattern:** **closure over private state**.
5. **Plan:** `called` and `result` in once's scope → returned function checks and updates them.
6. **Code and test:** arguments passed through, a function returning undefined, two independent wrappers.
walkthrough:
**Line by line**

- `called` and `result` live in the scope of each `once(...)` call, so every wrapper has its own pair.
- `(...args)` collects whatever arguments the wrapper receives, and `fn(...args)` passes them on.
- Setting `called = true` **before** calling `fn` means that even if `fn` somehow calls the wrapper again, it won't run twice.
- Later calls skip straight to `return result`.

**Trace:** `f(2, 3)` → called false → set true, result 5 → 5; `f(10, 10)` → called true → 5.

**Common wrong approach:** `if (result === undefined)`, which calls `fn` again every time when its real result is `undefined` (common for setup functions that just do something).
:::

:::exercise A running average
Write `makeAverager()` returning a function `add(n)` that records the number and returns the **average of all numbers added so far** through that function. Each averager keeps its own numbers.
```js starter
function makeAverager() {
  // your code here
}

const avg = makeAverager();
console.log(avg(10), avg(20), avg(60));   // 10 15 30
```
```js check
const m = need("makeAverager", "function");
const a = m();
same([a(10), a(20), a(60)], [10, 15, 30], "The averages after 10, 20, 60");
const b = m();
same(b(5), 5, "A new averager's first average");
same(a(10), 25, "The first averager after adding 10 more");
const c = m();
same([c(0.1), c(0.2)], [0.1, 0.15], "Decimals (within rounding)");
same([c(-0.3)], [0], "A negative number");
```
```js solution
function makeAverager() {
  let total = 0;
  let count = 0;
  return (n) => {
    total += n;
    count++;
    return total / count;
  };
}

const avg = makeAverager();
console.log(avg(10), avg(20), avg(60));
```
hint: Like the counter in the lesson: keep state in variables inside `makeAverager`, and return an arrow function that updates them.
hint: You don't need to store every number: a running `total` and a `count` are enough.
hint: Inside the returned function: `total += n; count++; return total / count;`
approach:
1. **Understand:** a factory that makes independent stateful functions.
2. **Examples:** after 10, 20, 60 the total is 90 over 3 numbers → 30.
3. **Brute force:** store every number in an array and average it each time: O(n) per call, still correct.
4. **Pattern:** **closure with running totals** (O(1) per call).
5. **Plan:** total and count in the factory's scope → returned function updates and divides.
6. **Code and test:** several averagers at once, decimals, negatives.
walkthrough:
**Line by line**

- Each `makeAverager()` call creates a new `total` and `count`, so averagers don't interfere.
- The returned arrow function closes over both variables and updates them on every call.
- `total / count` is the mean of everything so far, without keeping a list.

**Trace:** `avg(10)` → 10/1; `avg(20)` → 30/2 = 15; `avg(60)` → 90/3 = 30.

**Common wrong approach:** declaring `total` and `count` outside `makeAverager` (at the top level). It works for one averager, but every averager then shares the same totals.
:::

:::quiz
? Where can a const declared inside an if block be used?
+ Only inside that block
- Anywhere in the function
- Anywhere in the file
= let and const are block-scoped.
? What is a closure?
+ A function together with the variables from the scope where it was created
- A function that has finished running
- A way to close the browser
= Closures let functions keep private state.
? Why does the var loop example print [3, 3, 3]?
+ All the functions share one var variable, which is 3 when they run
- var counts in steps of 3
- map changes the values
= let creates a new binding for each pass.
? What is the temporal dead zone?
+ The part of a block before a let or const declaration, where using the name is an error
- A part of the code that never runs
- The time a promise takes to resolve
= It turns use-before-declaration into a clear ReferenceError.
:::
