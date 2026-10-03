# JavaScript, TypeScript and JSON

A hands-on course that starts from zero: 8 lessons on JavaScript (the language of the web), working with data and JSON, asynchronous code, building interactive pages, TypeScript, and Node.js tooling, ending with interview topics and a final project.

JavaScript runs every web page, and with Node.js it runs servers and tools too. JSON is how almost every API, including every LLM API, sends data. TypeScript adds types on top of JavaScript and is now the default for serious projects. Together they're essential for full-stack and AI engineers, and useful for analysts who build dashboards and automations.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/learning/javascript/)

The sandbox runs your JavaScript right in your browser, in a separate thread, so even an endless loop can be stopped. Nothing to install and no sign-up.

- every lesson, with **45 examples** you can run and change
- **16 exercises** with hidden tests, each with an approach, hints and a walkthrough
- **32 quiz questions**, with explanations
- your progress and code saved in your own browser

**Before you start:** nothing. Programming experience helps but isn't needed. If you already know Python, you'll move quickly: the lessons point out where JavaScript differs.

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 8 lessons, each with key terms, examples, common mistakes, exercises, walkthroughs and a quiz |
| 📖 [Glossary](glossary.md) | every term used in the course, defined in plain English |
| 🧾 [Cheat sheet](cheatsheet.md) | the syntax and patterns on one page, and every concept at a glance |

## How to use this course

1. Read a lesson, here on GitHub or in the sandbox. Start with its **Key terms**.
2. Run the examples in the sandbox and change them to see what happens.
3. Try each exercise before opening help; press **Check** to run the hidden tests.
4. Stuck? Open **How to approach it**, then the hints one at a time, and the **walkthrough** only after a real attempt.

## Lessons

### Part 1: JavaScript Basics (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 1 | [What JavaScript is](lessons/01-what-is-javascript.md) | what JavaScript is, where it runs (browsers, Node.js, Deno, Bun), runtimes and their extras, ECMAScript, TC39 and yearly editions, console.log, statements, semicolons and automatic semicolon insertion, comments, JavaScript compared with Python, how the sandbox runs code, reading error messages | 1–2 |
| 2 | [Variables and types](lessons/02-variables-and-types.md) | let and const, why not var, naming rules and camelCase, primitive types and objects, typeof and its quirks, Array.isArray, dynamic typing, converting with Number, String, Boolean, parseInt and parseFloat, NaN and Number.isNaN, implicit conversion, undefined versus null, strict mode | 3–4 |
| 3 | [Strings and template literals](lessons/03-strings.md) | single, double and backtick quotes, template literals and ${…}, multi-line strings, escape sequences, length, indexes and at(), immutability, trim, case, includes, startsWith, endsWith, indexOf, slice, replace and replaceAll, padStart, repeat, split and join, comparing strings, UTF-16 and emoji length | 5–6 |
| 4 | [Numbers and maths](lessons/04-numbers.md) | the number type and floating point, arithmetic operators and precedence, compound assignment and ++, remainder and integer division, 0.1 + 0.2, comparing with a tolerance, Math functions, rounding, toFixed, Number.isInteger, MAX_SAFE_INTEGER and BigInt, Infinity and NaN, money in whole cents, Intl.NumberFormat | 7–8 |
| 5 | [Comparisons and conditions](lessons/05-conditions.md) | comparison operators, strict and loose equality, comparing objects by identity, truthy and falsy values, logical operators and short-circuiting, defaults with \|\| and ??, nullish assignment ??=, optional chaining ?., if / else if / else, the conditional (ternary) operator, switch and fall-through | 9–10 |
| 6 | [Loops](lessons/06-loops.md) | for…of over arrays and strings, the classic for loop, while and do…while, break and continue, for…in over object keys, accumulators, running maximums, nested loops, off-by-one errors, endless loops and how to avoid them | 11–12 |
| 7 | [Functions](lessons/07-functions.md) | function declarations, function expressions, arrow functions and implicit return, parameters and arguments, return and undefined, default parameters, rest parameters and spread, hoisting, functions as values, callbacks, higher-order functions, throwing errors for bad input, writing small single-purpose functions | 13–14 |
| 8 | [Scope and closures](lessons/08-scope-and-closures.md) | lexical scope, global, function and block scope, the scope chain, shadowing, var versus let and const, hoisting and the temporal dead zone, closures, private state, function factories, counters, once and memoize, the loop-closure bug | 15–16 |

## Running it on your own computer

Every example also runs in [Node.js](https://nodejs.org) 26 or newer (`node file.js`) or in your browser's developer console. A few lessons use the newest JavaScript features; they say so, and which browsers support them.

## Editing the course

Lessons are generated from the Markdown sources in [`course/`](course/). See [course/README.md](course/README.md).
