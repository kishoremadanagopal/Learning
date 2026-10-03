# JavaScript, TypeScript and JSON glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **Accumulator** | A variable that builds up a result as a loop runs. [6] |
| **Arrow function** | A short function syntax, `(x) => x * 2`, which returns the expression automatically. [7] |
| **Automatic semicolon insertion** | JavaScript's rule for adding missing semicolons at line ends. [1] |
| **BigInt** | A type for exact whole numbers of any size, written with an `n` suffix. [4] |
| **Block scope** | Names that exist only inside the nearest `{ }`, as with `let` and `const`. [8] |
| **`break`** | Ends a loop immediately. [6] |
| **Callback** | A function passed to another function, to be called by it. [7] |
| **Closure** | A function bundled with the variables of the scope it was created in. [8] |
| **`const`** | Declares a name that can't be reassigned. [2] |
| **`continue`** | Skips the rest of the current pass and starts the next. [6] |
| **Default parameter** | A value used when an argument is missing or `undefined`. [7] |
| **Dynamic typing** | Types belong to values, not variables, and are checked as the code runs. [2] |
| **ECMAScript** | The official standard that defines the JavaScript language, with a new edition each year. [1] |
| **Escape sequence** | A backslash code for a special character, such as `\n` for a new line. [3] |
| **Factory function** | A function that creates and returns new objects or functions. [8] |
| **Fall-through** | In a switch, running on into the next case when there's no `break` or `return`. [5] |
| **Floating point** | The binary format numbers are stored in, exact for whole numbers but approximate for most decimals. [4] |
| **Function** | A reusable block of code that can take inputs and return a result. [7] |
| **Higher-order function** | A function that takes or returns another function. [7] |
| **Hoisting** | Function declarations can be called before their line in the code. [7] |
| **Immutable** | Can't be changed after it's created; string methods return new strings. [3] |
| **Index** | A position in a string or array, counting from 0. [3] |
| **Infinite loop** | A loop whose condition never becomes false. [6] |
| **`Infinity`** | A number value bigger than any other, such as the result of `1 / 0`. [4] |
| **Iterable** | A value `for…of` can loop over, such as an array, string, Map or Set. [6] |
| **JavaScript** | The programming language of the web, also used for servers and tools. [1] |
| **`let`** | Declares a name that can be reassigned. [2] |
| **Lexical scope** | Scopes decided by where code is written, not where it's called. [8] |
| **Loop** | Code that repeats a block while a condition holds or for each item. [6] |
| **Loose equality (`==`)** | Compares after converting types; best avoided. [5] |
| **Memoization** | Remembering a function's results so repeat calls are instant. [8] |
| **Method** | A function that belongs to a value, called with a dot: `text.trim()`. [3] |
| **`NaN`** | "not a number", the result of a failed numeric operation. [2] |
| **Node.js** | A runtime for running JavaScript outside the browser: servers, scripts and tools. [1] |
| **`null`** | A value meaning "deliberately empty". [2] |
| **Nullish coalescing (`??`)** | Gives the right-hand value only when the left is `null` or `undefined`. [5] |
| **Object** | Any value that isn't a primitive, such as plain objects, arrays and functions. [2] |
| **Off-by-one error** | A loop that runs one time too many or too few. [6] |
| **Operator precedence** | The rules for which operations happen first, such as `*` before `+`. [4] |
| **Optional chaining (`?.`)** | Reads a property or calls a method only if the value before it isn't `null` or `undefined`. [5] |
| **Parameter / argument** | The name in the definition, and the value passed in a call. [7] |
| **Primitive** | A simple, unchangeable value: string, number, bigint, boolean, undefined, null or symbol. [2] |
| **Remainder (`%`)** | What's left after division; its sign follows the left-hand number in JavaScript. [4] |
| **Rest parameter** | `...name`, collecting the remaining arguments into an array. [7] |
| **Runtime (host)** | A program that runs JavaScript and adds its own features, such as a browser or Node.js. [1] |
| **Safe integer** | A whole number small enough (up to 2⁵³ − 1) to be stored exactly. [4] |
| **Scope** | The part of a program where a name can be used. [8] |
| **Shadowing** | An inner variable hiding an outer one with the same name. [8] |
| **Short-circuiting** | `&&` and `\|\|` stop evaluating as soon as the result is known. [5] |
| **Spread syntax** | `...array`, expanding an array into separate values. [7] |
| **Statement** | One instruction in a program, usually ending with a semicolon. [1] |
| **Strict equality (`===`)** | True when both values have the same type and value. [5] |
| **Strict mode** | A stricter version of JavaScript that turns some silent mistakes into errors. [2] |
| **String** | A sequence of characters: text. [3] |
| **TC39** | The committee that develops the ECMAScript standard. [1] |
| **Template literal** | A string in backticks that can span lines and insert values with `${…}`. [3] |
| **Temporal dead zone** | The part of a block before a `let` or `const` declaration, where the name can't be used. [8] |
| **Ternary operator** | `condition ? a : b`, an expression that picks one of two values. [5] |
| **Tolerance** | How far apart two numbers may be and still count as equal. [4] |
| **Truthy / falsy** | How a value behaves when JavaScript needs true or false; falsy values are `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined` and `NaN`. [5] |
| **`typeof`** | An operator that returns a value's type as a string. [2] |
| **`undefined`** | The value of something that hasn't been given a value. [2] |
| **UTF-16 code unit** | The 16-bit unit JavaScript strings are made of; some characters need two. [3] |
| **Variable** | A name that refers to a value. [2] |
| **Web Worker** | A background thread in the browser; the sandbox runs your code in one. [1] |
