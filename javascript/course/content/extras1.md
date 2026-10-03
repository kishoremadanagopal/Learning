@@ what-is-javascript
topics: what JavaScript is, where it runs (browsers, Node.js, Deno, Bun), runtimes and their extras, ECMAScript, TC39 and yearly editions, console.log, statements, semicolons and automatic semicolon insertion, comments, JavaScript compared with Python, how the sandbox runs code, reading error messages
terms:
- **JavaScript:** the programming language of the web, also used for servers and tools.
- **Runtime (host):** a program that runs JavaScript and adds its own features, such as a browser or Node.js.
- **Node.js:** a runtime for running JavaScript outside the browser: servers, scripts and tools.
- **ECMAScript:** the official standard that defines the JavaScript language, with a new edition each year.
- **TC39:** the committee that develops the ECMAScript standard.
- **Statement:** one instruction in a program, usually ending with a semicolon.
- **Automatic semicolon insertion:** JavaScript's rule for adding missing semicolons at line ends.
- **Web Worker:** a background thread in the browser; the sandbox runs your code in one.
mistakes:
- Forgetting a closing quote or bracket, so nothing runs at all.
- Misspelling a name such as `console`, giving a `ReferenceError`.
- Reading only the last line of an error message instead of its type and message.
- Joining text and numbers with `+` and getting text instead of a sum.

glance:
- Print values | console.log(a, b, …) joins them with spaces | O(n) | O(n)
- Comment | // to end of line, or /* … */ | — | —
- Find an error | read the type and message, then the line | — | —

@@ variables-and-types
topics: let and const, why not var, naming rules and camelCase, primitive types and objects, typeof and its quirks, Array.isArray, dynamic typing, converting with Number, String, Boolean, parseInt and parseFloat, NaN and Number.isNaN, implicit conversion, undefined versus null, strict mode
terms:
- **Variable:** a name that refers to a value.
- **`const`:** declares a name that can't be reassigned.
- **`let`:** declares a name that can be reassigned.
- **Primitive:** a simple, unchangeable value: string, number, bigint, boolean, undefined, null or symbol.
- **Object:** any value that isn't a primitive, such as plain objects, arrays and functions.
- **`typeof`:** an operator that returns a value's type as a string.
- **Dynamic typing:** types belong to values, not variables, and are checked as the code runs.
- **`NaN`:** "not a number", the result of a failed numeric operation.
- **`undefined`:** the value of something that hasn't been given a value.
- **`null`:** a value meaning "deliberately empty".
- **Strict mode:** a stricter version of JavaScript that turns some silent mistakes into errors.
mistakes:
- Using `let` (or `var`) for values that never change.
- Testing for null with `typeof value === "null"`.
- Comparing with `=== NaN`, which is always false.
- Trusting `Number(text)` to validate input (`Number("")` is 0).
- Assigning to a misspelt variable name and expecting a new variable.

glance:
- Declare | const by default; let if reassigned | O(1) | O(1)
- Check a type | typeof, plus === null and Array.isArray | O(1) | O(1)
- Text to number | validate the format, then Number(text) | O(n) | O(1)

@@ strings
topics: single, double and backtick quotes, template literals and ${…}, multi-line strings, escape sequences, length, indexes and at(), immutability, trim, case, includes, startsWith, endsWith, indexOf, slice, replace and replaceAll, padStart, repeat, split and join, comparing strings, UTF-16 and emoji length
terms:
- **String:** a sequence of characters: text.
- **Template literal:** a string in backticks that can span lines and insert values with `${…}`.
- **Escape sequence:** a backslash code for a special character, such as `\n` for a new line.
- **Index:** a position in a string or array, counting from 0.
- **Immutable:** can't be changed after it's created; string methods return new strings.
- **Method:** a function that belongs to a value, called with a dot: `text.trim()`.
- **UTF-16 code unit:** the 16-bit unit JavaScript strings are made of; some characters need two.
mistakes:
- Calling a string method without keeping its result.
- Using `str[-1]` for the last character (it's `undefined`; use `str.at(-1)`).
- Splitting on a single space when words may be separated by several.
- Treating `indexOf` returning 0 as "not found" (not found is -1).
- Counting emoji with `.length`.

glance:
- Insert values into text | `${value}` in a template literal | O(n) | O(n)
- Find text | includes, indexOf (−1 if absent) | O(n·m) | O(1)
- Words of a sentence | trim().split(/\s+/) | O(n) | O(n)
- Count characters | [...text].length | O(n) | O(n)

@@ numbers
topics: the number type and floating point, arithmetic operators and precedence, compound assignment and ++, remainder and integer division, 0.1 + 0.2, comparing with a tolerance, Math functions, rounding, toFixed, Number.isInteger, MAX_SAFE_INTEGER and BigInt, Infinity and NaN, money in whole cents, Intl.NumberFormat
terms:
- **Floating point:** the binary format numbers are stored in, exact for whole numbers but approximate for most decimals.
- **Operator precedence:** the rules for which operations happen first, such as `*` before `+`.
- **Remainder (`%`):** what's left after division; its sign follows the left-hand number in JavaScript.
- **Tolerance:** how far apart two numbers may be and still count as equal.
- **Safe integer:** a whole number small enough (up to 2⁵³ − 1) to be stored exactly.
- **BigInt:** a type for exact whole numbers of any size, written with an `n` suffix.
- **`Infinity`:** a number value bigger than any other, such as the result of `1 / 0`.
mistakes:
- Comparing decimal results with `===`.
- Doing arithmetic on the string returned by `toFixed`.
- Storing money as decimal pounds instead of whole pence.
- Expecting `-7 % 3` to be 2, as in Python.
- Mixing BigInt and ordinary numbers in one expression.

glance:
- Compare decimals | Math.abs(a − b) ≤ tolerance × the larger magnitude | O(1) | O(1)
- Integer division | Math.floor(a / b) or Math.trunc(a / b) | O(1) | O(1)
- Money | integer pence; format only for display | O(digits) | O(digits)
- Huge whole numbers | BigInt (123n) | O(digits) | O(digits)

@@ conditions
topics: comparison operators, strict and loose equality, comparing objects by identity, truthy and falsy values, logical operators and short-circuiting, defaults with || and ??, nullish assignment ??=, optional chaining ?., if / else if / else, the conditional (ternary) operator, switch and fall-through
terms:
- **Strict equality (`===`):** true when both values have the same type and value.
- **Loose equality (`==`):** compares after converting types; best avoided.
- **Truthy / falsy:** how a value behaves when JavaScript needs true or false; falsy values are `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined` and `NaN`.
- **Short-circuiting:** `&&` and `||` stop evaluating as soon as the result is known.
- **Nullish coalescing (`??`):** gives the right-hand value only when the left is `null` or `undefined`.
- **Optional chaining (`?.`):** reads a property or calls a method only if the value before it isn't `null` or `undefined`.
- **Ternary operator:** `condition ? a : b`, an expression that picks one of two values.
- **Fall-through:** in a switch, running on into the next case when there's no `break` or `return`.
mistakes:
- Using `==` and getting surprising matches such as `0 == ""`.
- Defaulting with `||` and losing valid values like `0` or `""`.
- Reading a nested property without `?.` and crashing on `undefined`.
- Forgetting `break` in a `switch`.
- Writing `if (x = 5)` (assignment) instead of `if (x === 5)`.

glance:
- Default for missing values | value ?? fallback | O(1) | O(1)
- Safe nested read | a?.b?.c | O(depth) | O(1)
- Ranges | guard invalid input, then thresholds from the top | O(cases) | O(1)
- Many exact cases | switch with return in each case | O(cases) | O(1)

@@ loops
topics: for…of over arrays and strings, the classic for loop, while and do…while, break and continue, for…in over object keys, accumulators, running maximums, nested loops, off-by-one errors, endless loops and how to avoid them
terms:
- **Loop:** code that repeats a block while a condition holds or for each item.
- **Iterable:** a value `for…of` can loop over, such as an array, string, Map or Set.
- **Accumulator:** a variable that builds up a result as a loop runs.
- **`break`:** ends a loop immediately.
- **`continue`:** skips the rest of the current pass and starts the next.
- **Off-by-one error:** a loop that runs one time too many or too few.
- **Infinite loop:** a loop whose condition never becomes false.
mistakes:
- Using `for…in` on arrays (it gives string indexes).
- Writing `i <= arr.length` and reading past the end.
- Forgetting to update the variable a `while` condition depends on.
- Declaring the loop variable with `var` (closures then share it).
- Resetting the accumulator inside the loop.

glance:
- Each value | for (const x of items) | O(n) | O(1)
- Each index | for (let i = 0; i < n; i++) | O(n) | O(1)
- Unknown number of steps | while (condition) with progress in the body | O(steps) | O(1)
- Object keys | for (const key in obj), or Object.entries | O(keys) | O(1)

@@ functions
topics: function declarations, function expressions, arrow functions and implicit return, parameters and arguments, return and undefined, default parameters, rest parameters and spread, hoisting, functions as values, callbacks, higher-order functions, throwing errors for bad input, writing small single-purpose functions
terms:
- **Function:** a reusable block of code that can take inputs and return a result.
- **Parameter / argument:** the name in the definition, and the value passed in a call.
- **Arrow function:** a short function syntax, `(x) => x * 2`, which returns the expression automatically.
- **Default parameter:** a value used when an argument is missing or `undefined`.
- **Rest parameter:** `...name`, collecting the remaining arguments into an array.
- **Spread syntax:** `...array`, expanding an array into separate values.
- **Hoisting:** function declarations can be called before their line in the code.
- **Callback:** a function passed to another function, to be called by it.
- **Higher-order function:** a function that takes or returns another function.
mistakes:
- Using braces in an arrow function and forgetting `return`.
- Printing a result instead of returning it.
- Pushing or passing `fn` when you meant to call `fn()`.
- Calling a `const` arrow function before its line.
- Expecting a default parameter to replace `null`.

glance:
- Short function | const f = (x) => expression | O(1) | O(1)
- Any number of arguments | function f(...args) | O(n) | O(n)
- Array as arguments | f(...array) | O(n) | O(n)
- Pass behaviour in | callback parameter, called as fn(value) | O(1) per call | O(1)

@@ scope-and-closures
topics: lexical scope, global, function and block scope, the scope chain, shadowing, var versus let and const, hoisting and the temporal dead zone, closures, private state, function factories, counters, once and memoize, the loop-closure bug
terms:
- **Scope:** the part of a program where a name can be used.
- **Lexical scope:** scopes decided by where code is written, not where it's called.
- **Block scope:** names that exist only inside the nearest `{ }`, as with `let` and `const`.
- **Shadowing:** an inner variable hiding an outer one with the same name.
- **Temporal dead zone:** the part of a block before a `let` or `const` declaration, where the name can't be used.
- **Closure:** a function bundled with the variables of the scope it was created in.
- **Factory function:** a function that creates and returns new objects or functions.
- **Memoization:** remembering a function's results so repeat calls are instant.
mistakes:
- Using `var`, which leaks out of blocks and shares one variable across loop passes.
- Keeping per-instance state in a global variable instead of a closure.
- Shadowing an outer variable by accident.
- Checking `result === undefined` to see if something has already run.

glance:
- Private state | variables inside a factory, returned function uses them | O(1) | O(state)
- Run once | flag + saved result in a closure | O(1) | O(1)
- Memoize | Map cache in a closure | O(1) per repeat | O(distinct inputs)
