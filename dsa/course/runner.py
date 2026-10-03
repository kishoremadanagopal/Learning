"""Runs learner code and exercise checks. Used by the browser sandbox (Pyodide) and by build.py --test,
so lessons are tested with exactly the same rules they run under in the browser."""
import base64
import builtins
import io
import os
import re
import sys
import traceback
import warnings

os.environ.setdefault("MPLBACKEND", "Agg")

_SETUP_DONE = False
DATA = {}          # filename -> bytes, restored before every run so lessons always start from clean files


def setup(data_files=None):
    """Configure pandas/matplotlib once. data_files: {name: bytes} copied into the working folder before each run."""
    global _SETUP_DONE
    if data_files:
        DATA.update(data_files)
    if _SETUP_DONE:
        return
    warnings.filterwarnings("ignore", message=".*non-interactive.*")
    warnings.filterwarnings("ignore", message=".*as_object_map.*")   # Pyodide-internal notice from threadpoolctl
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    try:
        import pandas as pd
        pd.set_option("display.width", 100)
        pd.set_option("display.max_columns", 12)
        pd.set_option("display.max_rows", 20)
        pd.set_option("display.min_rows", 10)
        pd.set_option("display.max_colwidth", 30)
    except ImportError:
        pass
    _SETUP_DONE = True


def _restore_data():
    """Start every run from a clean folder: remove files earlier runs created, restore the practice files."""
    if DATA:
        for name in os.listdir("."):
            if name not in DATA and os.path.isfile(name):
                os.remove(name)
    for name, blob in DATA.items():
        with open(name, "wb") as f:
            f.write(blob)


def _matplotlib_loaded():
    return "matplotlib.pyplot" in sys.modules


def _prepare_plots():
    if not _matplotlib_loaded():
        return
    import matplotlib.pyplot as plt
    plt.close("all")
    plt.show = lambda *a, **k: None


def _collect_figures(encode):
    if not _matplotlib_loaded():
        return []
    import matplotlib.pyplot as plt
    figs = []
    for num in plt.get_fignums():
        fig = plt.figure(num)
        if not fig.axes:
            continue
        if encode:
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
            figs.append(base64.b64encode(buf.getvalue()).decode("ascii"))
        else:
            figs.append("figure")
    return figs


HINTS = {
    "KeyError": "Hint: a KeyError means that key isn't in the dictionary. Check with `key in d`, or use d.get(key, default).",
    "IndexError": "Hint: an index is past the end. A list of length n has indexes 0 to n - 1; check your loop bounds and empty inputs.",
    "RecursionError": "Hint: the recursion never stops (or goes too deep). Check that every path reaches a base case.",
    "ZeroDivisionError": "Hint: something was divided by zero. Is a count or length 0 for an empty input?",
    "ModuleNotFoundError": "Hint: the sandbox has Python's standard library (collections, heapq, bisect, functools, itertools…) plus numpy and matplotlib.",
    "FileNotFoundError": "Hint: check the file name. The practice files are listed in the Data files tab.",
    "SettingWithCopyWarning": "",
}


MESSAGE_HINTS = [
    ("'NoneType' object", "Hint: something is None. Did a function forget to `return` its result, or does a variable point to nothing (like the end of a linked list)?"),
    ("maximum recursion depth", "Hint: the recursion never stops (or goes too deep). Check that every path reaches a base case."),
]


def _report(e, src, err):
    src_lines = src.splitlines()
    frames = [fr for fr in traceback.extract_tb(e.__traceback__) if fr.filename == "main.py"]
    parts = []
    if frames:
        parts.append("Traceback (most recent call last):\n")
        for fr in frames:
            parts.append(f'  File "main.py", line {fr.lineno}, in {fr.name}\n')
            line = fr.line or (src_lines[fr.lineno - 1] if fr.lineno and 0 < fr.lineno <= len(src_lines) else "")
            if line:
                parts.append("    " + line.strip() + "\n")
    e.__context__ = None
    msg = "".join(traceback.format_exception_only(type(e), e))
    parts.append(msg)
    hint = HINTS.get(type(e).__name__)
    text = str(e)
    for needle, h in MESSAGE_HINTS:
        if needle in text:
            hint = h
            break
    if hint:
        parts.append(hint + "\n")
    err.append("".join(parts))


class _Sink(io.TextIOBase):
    def __init__(self, parts, kind):
        self.parts, self.kind = parts, kind

    def write(self, s):
        s = str(s)
        if s:
            if self.parts and self.parts[-1][0] == self.kind:
                self.parts[-1][1] += s
            else:
                self.parts.append([self.kind, s])
        return len(s)

    def flush(self):
        pass


def _execute(src, stdin_text=""):
    setup()
    _restore_data()
    _prepare_plots()
    parts = []
    lines = iter(stdin_text.split("\n")) if stdin_text else iter(())

    def _input(prompt=""):
        sys.stdout.write(str(prompt))
        try:
            value = next(lines)
        except StopIteration:
            raise EOFError("input() ran out of lines. Add one per call in the Input box.") from None
        sys.stdout.write(value + "\n")
        return value

    saved = (sys.stdout, sys.stderr, builtins.input)
    sys.stdout, sys.stderr = _Sink(parts, "out"), _Sink(parts, "err")
    builtins.input = _input
    ns = {"__name__": "__main__", "input": _input}
    ok = True
    err = []
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            exec(compile(src, "main.py", "exec"), ns)
    except SystemExit:
        pass
    except BaseException as e:  # noqa: BLE001
        ok = False
        _report(e, src, err)
    finally:
        sys.stdout, sys.stderr, builtins.input = saved
    if err:
        parts.append(["err", err[0]])
    return ok, ns, parts


def run(src, stdin_text="", encode_figures=True):
    """Run learner code. Returns {ok, parts: [[kind, text], ...], figures: [png base64, ...]}."""
    ok, _, parts = _execute(src, stdin_text)
    return {"ok": ok, "parts": parts, "figures": _collect_figures(encode_figures)}


# ---------------------------------------------------------------- check helpers

_MISSING = object()


def _short(value, limit=600):
    text = repr(value) if not hasattr(value, "to_string") else value.to_string(max_rows=12, max_cols=8)
    return text if len(text) <= limit else text[:limit] + " …"


def _helpers(ns, output, source):
    import copy
    import math
    import time
    np = sys.modules.get("numpy")          # only if the learner's code imported it (keeps the sandbox light)
    pd = sys.modules.get("pandas")

    def need(name, kind=None):
        """Return the learner's variable `name`, failing with a friendly message if it's missing or the wrong type."""
        value = ns.get(name, _MISSING)
        if value is _MISSING:
            raise AssertionError(f"Create a variable called `{name}`.")
        if kind is not None and not isinstance(value, kind):
            kinds = kind if isinstance(kind, tuple) else (kind,)
            names = " or ".join(getattr(k, "__name__", str(k)) for k in kinds)
            raise AssertionError(f"`{name}` should be a {names}, but it's a {type(value).__name__}.")
        return value

    def same(actual, expected, what="Your result", ignore_index=False, ignore_order=False, ignore_dtype=True, tol=1e-6):
        """Assert that actual equals expected (numbers, arrays, Series, DataFrames, lists...)."""
        fail = None
        if pd is not None and isinstance(expected, (pd.DataFrame, pd.Series)):
            if not isinstance(actual, type(expected)):
                raise AssertionError(f"{what} should be a {type(expected).__name__}, but it's a {type(actual).__name__}.")
            a, b = actual, expected
            if isinstance(b, pd.DataFrame) and list(a.columns) != list(b.columns):
                if sorted(map(str, a.columns)) == sorted(map(str, b.columns)) and ignore_order:
                    a = a[list(b.columns)]
                else:
                    raise AssertionError(f"{what} should have the columns {list(b.columns)}, but has {list(a.columns)}.")
            if len(a) != len(b):
                raise AssertionError(f"{what} should have {len(b)} rows, but has {len(a)}.")
            if ignore_order:
                key = list(b.columns) if isinstance(b, pd.DataFrame) else None
                if key is not None:
                    a = a.sort_values(key).reset_index(drop=ignore_index)
                    b = b.sort_values(key).reset_index(drop=ignore_index)
                else:
                    a = a.sort_values().reset_index(drop=ignore_index)
                    b = b.sort_values().reset_index(drop=ignore_index)
            if ignore_index:
                a, b = a.reset_index(drop=True), b.reset_index(drop=True)
            try:
                if isinstance(b, pd.DataFrame):
                    pd.testing.assert_frame_equal(a, b, check_dtype=not ignore_dtype, check_exact=False, rtol=tol,
                                                  check_names=False, check_index_type=False, check_column_type=False)
                else:
                    pd.testing.assert_series_equal(a, b, check_dtype=not ignore_dtype, check_exact=False, rtol=tol,
                                                   check_names=False, check_index_type=False)
            except AssertionError:
                fail = True
        elif np is not None and isinstance(expected, np.ndarray):
            arr = np.asarray(actual)
            if arr.shape != expected.shape:
                raise AssertionError(f"{what} should have shape {expected.shape}, but has shape {arr.shape}.")
            try:
                fail = not np.allclose(arr, expected, rtol=tol, equal_nan=True) if expected.dtype.kind in "fiub" else not (arr == expected).all()
            except TypeError:
                fail = True
        elif isinstance(expected, float) or isinstance(actual, float):
            try:
                fail = abs(float(actual) - float(expected)) > max(tol * abs(float(expected)), 1e-9)
            except (TypeError, ValueError):
                fail = True
        else:
            if hasattr(actual, "item") and not isinstance(actual, (list, dict, str)):
                try:
                    actual = actual.item()
                except (ValueError, AttributeError):
                    pass
            fail = actual != expected
        if fail:
            raise AssertionError(f"{what} isn't right yet.\nExpected:\n{_short(expected)}\nGot:\n{_short(actual)}")
        return True

    def printed(*texts):
        """True if every text appears in what the learner printed."""
        return all(str(t) in output for t in texts)

    def _code_only():
        return "\n".join(re.sub(r"#.*$", "", ln) for ln in source.splitlines())

    def uses(*snippets):
        """True if every snippet appears in the learner's code (comments ignored)."""
        code = _code_only()
        return all(s in code for s in snippets)

    def chart():
        """Return the Axes of the learner's chart (the most recent figure)."""
        if not _matplotlib_loaded():
            raise AssertionError("Draw a chart with matplotlib (import matplotlib.pyplot as plt).")
        import matplotlib.pyplot as plt
        nums = [n for n in plt.get_fignums() if plt.figure(n).axes]
        if not nums:
            raise AssertionError("No chart was drawn. Create one with plt.subplots() or df.plot().")
        return plt.figure(nums[-1]).axes[0]

    # ---- function tests (hidden test cases, like coding-interview sites) ----

    def _func(name):
        if callable(name):
            return name, getattr(name, "__name__", "your function")
        f = ns.get(name, _MISSING)
        if f is _MISSING:
            raise AssertionError(f"Define a function called `{name}` (it starts with `def {name}(`).")
        if not callable(f):
            raise AssertionError(f"`{name}` should be a function, but it's a {type(f).__name__}.")
        return f, name

    def _show(value, limit=90):
        text = repr(value)
        return text if len(text) <= limit else text[:limit] + " …"

    def _eq(got, expected):
        if isinstance(expected, float) or isinstance(got, float):
            try:
                return math.isclose(float(got), float(expected), rel_tol=1e-9, abs_tol=1e-9)
            except (TypeError, ValueError):
                return False
        return got == expected

    def _verdict_ok(got, expected, args, valid, key):
        if valid is not None:
            return bool(valid(got, *copy.deepcopy(args)))
        if key is not None:
            try:
                return key(got) == key(expected)
            except Exception:  # noqa: BLE001
                return False
        return _eq(got, expected)

    def test(name, cases, valid=None, key=None, show=None):
        """Run the learner's function on hidden test cases: [(args, expected, "label"), ...].
        args is a tuple of arguments (a single non-tuple value is one argument).
        valid(got, *args) -> bool checks answers that have several right forms; key normalises both sides (e.g. sorted).
        show is an optional format string for the call shown on failure, e.g. "max_depth(build({0}))"."""
        f, fname = _func(name)
        total = len(cases)
        for done, case in enumerate(cases):
            args, expected = case[0], case[1]
            label = case[2] if len(case) > 2 else f"test {done + 1}"
            if not isinstance(args, tuple):
                args = (args,)
            shown = [_show(a, 60) for a in args]
            call = show.format(*shown) if show else f"{fname}({', '.join(shown)})"
            head = f"Passed {done} of {total} tests. Fails on {label}:\n  {call}\n"
            try:
                got = f(*copy.deepcopy(args))
            except RecursionError:
                raise AssertionError(head + "hit RecursionError: the recursion goes too deep or never reaches its base case.") from None
            except Exception as e:  # noqa: BLE001
                raise AssertionError(head + f"raised {type(e).__name__}: {e}") from None
            if not _verdict_ok(got, expected, args, valid, key):
                msg = head + (f"returned {_show(got)}, which isn't a correct answer (for example, {_show(expected)} is)." if valid
                              else f"should return {_show(expected)}, but returned {_show(got)}.")
                if got is None and expected is not None:
                    msg += "\nDid you forget to `return` the answer? Printing it isn't the same as returning it."
                raise AssertionError(msg)
        return True

    def _fresh(value):
        """A copy safe to hand to a function that might change it; fast for big flat lists of numbers or strings."""
        if isinstance(value, tuple):
            return tuple(_fresh(v) for v in value)
        if isinstance(value, list):
            if not value or not isinstance(value[0], (list, dict, set)):
                return list(value)
            return copy.deepcopy(value)
        if isinstance(value, (dict, set)):
            return copy.deepcopy(value)
        return value

    def speed(name, make_args, reference, sizes=(1_000, 10_000, 100_000), what="items", tip=None,
              valid=None, key=None, factor=30, floor=0.3):
        """Time the learner's function against a reference solution on growing inputs.
        Fails with a friendly "too slow" message as soon as it takes more than max(floor, factor x reference time)."""
        f, fname = _func(name)
        for n in sizes:
            args = make_args(n)
            if not isinstance(args, tuple):
                args = (args,)
            a_ref, a_you = _fresh(args), _fresh(args)
            t0 = time.perf_counter()
            expected = reference(*a_ref)
            t_ref = time.perf_counter() - t0
            t0 = time.perf_counter()
            try:
                got = f(*a_you)
            except RecursionError:
                raise AssertionError(f"With {n:,} {what}, your function hit RecursionError: the recursion is too deep for "
                                     "Python's limit (about 1,000 nested calls).\n" + (tip or "Use a loop instead.")) from None
            t = time.perf_counter() - t0
            if not _verdict_ok(got, expected, args, valid, key):
                raise AssertionError(f"Your function passes the small tests but gives a wrong answer on a big input ({n:,} {what}).")
            budget = max(floor, factor * t_ref)
            if t > budget:
                ref_txt = f"{t_ref * 1000:.0f} ms" if t_ref >= 0.001 else "under 1 ms"
                raise AssertionError(f"Correct, but too slow: with {n:,} {what} your function took {t:.2f} s; "
                                     f"a fast solution takes {ref_txt}.\n" + (tip or "Look for a way to avoid repeating work, such as a loop inside a loop."))
        return True

    return {"need": need, "same": same, "printed": printed, "uses": uses, "chart": chart, "test": test, "speed": speed}


def check(src, check_src, stdin_text="", encode_figures=True):
    """Run learner code, then the exercise's check code. Returns run() fields plus verdict {ok, msg}."""
    ok, ns, parts = _execute(src, stdin_text)
    figures = _collect_figures(encode_figures)
    if not ok:
        return {"ok": False, "parts": parts, "figures": figures,
                "verdict": {"ok": False, "msg": "Your code raised an error (see above). Fix it and check again."}}
    output = "".join(t for k, t in parts if k == "out")
    env = dict(ns)
    env.update({"__output__": output, "__source__": src})
    env.update(_helpers(ns, output, src))
    saved = sys.stdout
    sys.stdout = io.StringIO()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(compile(check_src, "check.py", "exec"), env)
        verdict = {"ok": True, "msg": "All checks passed."}
    except AssertionError as e:
        verdict = {"ok": False, "msg": str(e) or "One of the checks failed."}
    except Exception as e:  # noqa: BLE001
        verdict = {"ok": False, "msg": f"Checking stopped with {type(e).__name__}: {e}"}
    finally:
        sys.stdout = saved
    return {"ok": True, "parts": parts, "figures": figures, "verdict": verdict}
