# JavaScript, TypeScript and JSON cheat sheet

The syntax and patterns of the course on one page. The number in brackets is the lesson. The table of every concept with its approach and cost is at the end.

## JavaScript basics [1–8]

```js
const name = "Ada";          // can't be reassigned (use by default)
let count = 0;               // can be reassigned
console.log("Hi", name);     // prints: Hi Ada
// comment    /* block comment */
```

| Check | Use |
|---|---|
| type of a value | `typeof x` (but `typeof null` is `"object"`) |
| null | `x === null` |
| array | `Array.isArray(x)` |
| NaN | `Number.isNaN(x)` |
| text → number | validate, then `Number(text)`; `parseInt` / `parseFloat` read a leading number |

### Strings and numbers [3–4]

```js
`${qty} × ${item}`             // template literal
s.trim()  s.toLowerCase()  s.includes("x")  s.slice(0, 5)  s.at(-1)
s.split(",")  arr.join(", ")  s.replaceAll("-", " ")  "7".padStart(3, "0")
0.1 + 0.2 === 0.3              // false: compare with a tolerance
Math.round(x * 100) / 100      // round to 2 places (a number); x.toFixed(2) gives a string
Math.floor(a / b)  a % b       // integer division and remainder
```

### Conditions and loops [5–6]

| Write | Not |
|---|---|
| `a === b`, `a !== b` | `a == b` |
| `value ?? fallback` (only null/undefined) | `value \|\| fallback` when 0 or "" are valid |
| `obj?.a?.b` | `obj.a.b` on data that may be missing |
| `for (const x of items)` | `for (const i in items)` on arrays |

Falsy values: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`. Everything else is truthy.

### Functions and closures [7–8]

```js
function add(a, b = 0) { return a + b; }       // declaration (hoisted), default parameter
const double = (n) => n * 2;                    // arrow: returns the expression
const sum = (...nums) => { let t = 0; for (const n of nums) t += n; return t; };
sum(...[1, 2, 3]);                              // spread an array into arguments
function makeCounter() { let c = 0; return () => ++c; }   // closure: private state
```

## Every concept at a glance

Generated from the **At a glance** table at the end of each lesson. The number in brackets links to the lesson.

| Concept | Approach | Time | Space | Lesson |
|---|---|---|---|---|
| Print values | console.log(a, b, …) joins them with spaces | O(n) | O(n) | [1](lessons/01-what-is-javascript.md) |
| Comment | // to end of line, or /* … */ | — | — | [1](lessons/01-what-is-javascript.md) |
| Find an error | read the type and message, then the line | — | — | [1](lessons/01-what-is-javascript.md) |
| Declare | const by default; let if reassigned | O(1) | O(1) | [2](lessons/02-variables-and-types.md) |
| Check a type | typeof, plus === null and Array.isArray | O(1) | O(1) | [2](lessons/02-variables-and-types.md) |
| Text to number | validate the format, then Number(text) | O(n) | O(1) | [2](lessons/02-variables-and-types.md) |
| Insert values into text | `${value}` in a template literal | O(n) | O(n) | [3](lessons/03-strings.md) |
| Find text | includes, indexOf (−1 if absent) | O(n·m) | O(1) | [3](lessons/03-strings.md) |
| Words of a sentence | trim().split(/\s+/) | O(n) | O(n) | [3](lessons/03-strings.md) |
| Count characters | [...text].length | O(n) | O(n) | [3](lessons/03-strings.md) |
| Compare decimals | Math.abs(a − b) ≤ tolerance × the larger magnitude | O(1) | O(1) | [4](lessons/04-numbers.md) |
| Integer division | Math.floor(a / b) or Math.trunc(a / b) | O(1) | O(1) | [4](lessons/04-numbers.md) |
| Money | integer pence; format only for display | O(digits) | O(digits) | [4](lessons/04-numbers.md) |
| Huge whole numbers | BigInt (123n) | O(digits) | O(digits) | [4](lessons/04-numbers.md) |
| Default for missing values | value ?? fallback | O(1) | O(1) | [5](lessons/05-conditions.md) |
| Safe nested read | a?.b?.c | O(depth) | O(1) | [5](lessons/05-conditions.md) |
| Ranges | guard invalid input, then thresholds from the top | O(cases) | O(1) | [5](lessons/05-conditions.md) |
| Many exact cases | switch with return in each case | O(cases) | O(1) | [5](lessons/05-conditions.md) |
| Each value | for (const x of items) | O(n) | O(1) | [6](lessons/06-loops.md) |
| Each index | for (let i = 0; i < n; i++) | O(n) | O(1) | [6](lessons/06-loops.md) |
| Unknown number of steps | while (condition) with progress in the body | O(steps) | O(1) | [6](lessons/06-loops.md) |
| Object keys | for (const key in obj), or Object.entries | O(keys) | O(1) | [6](lessons/06-loops.md) |
| Short function | const f = (x) => expression | O(1) | O(1) | [7](lessons/07-functions.md) |
| Any number of arguments | function f(...args) | O(n) | O(n) | [7](lessons/07-functions.md) |
| Array as arguments | f(...array) | O(n) | O(n) | [7](lessons/07-functions.md) |
| Pass behaviour in | callback parameter, called as fn(value) | O(1) per call | O(1) | [7](lessons/07-functions.md) |
| Private state | variables inside a factory, returned function uses them | O(1) | O(state) | [8](lessons/08-scope-and-closures.md) |
| Run once | flag + saved result in a closure | O(1) | O(1) | [8](lessons/08-scope-and-closures.md) |
| Memoize | Map cache in a closure | O(1) per repeat | O(distinct inputs) | [8](lessons/08-scope-and-closures.md) |
