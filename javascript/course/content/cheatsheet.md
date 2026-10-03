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
