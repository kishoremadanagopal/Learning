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
    "KeyError": "Hint: a KeyError usually means a column or label doesn't exist. Check the spelling and capitals; print(df.columns) lists them all.",
    "ModuleNotFoundError": "Hint: the sandbox has numpy, pandas and matplotlib. Other packages need Python on your own computer.",
    "FileNotFoundError": "Hint: the practice files are sales.csv, customers.csv, products.csv, employees_messy.csv, weather.csv, students.csv and movies.json. Check the name.",
    "SettingWithCopyWarning": "",
}


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
    import numpy as np
    try:
        import pandas as pd
    except ImportError:  # pragma: no cover
        pd = None

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
        elif isinstance(expected, np.ndarray):
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

    return {"need": need, "same": same, "printed": printed, "uses": uses, "chart": chart}


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
