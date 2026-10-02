/* A module Web Worker that runs Python (Pyodide) off the main thread, so long runs never freeze the page and Stop can end them. */
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs";
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/";

let py = null;

async function start(files) {
  py = await loadPyodide({ indexURL: PYODIDE });
  await py.loadPackage(["numpy", "pandas", "scikit-learn"]);
  py.FS.mkdirTree("/home/pyodide/work");
  py.FS.chdir("/home/pyodide/work");
  const runnerSrc = await (await fetch("runner.py" + self.location.search)).text();
  py.FS.writeFile("/home/pyodide/runner.py", runnerSrc);
  const data = {};
  await Promise.all(files.map(async (name) => {
    const buf = await (await fetch("data/" + name + self.location.search)).arrayBuffer();
    data[name] = new Uint8Array(buf);
  }));
  py.globals.set("_files", py.toPy(data));
  await py.runPythonAsync(`
import sys
sys.path.insert(0, "/home/pyodide")
import runner, json
runner.setup({k: bytes(v) for k, v in _files.items()})
del _files
import pandas, numpy
`);
}

self.onmessage = async (e) => {
  const msg = e.data;
  try {
    if (msg.type === "init") {
      await start(msg.files);
      self.postMessage({ type: "ready" });
      return;
    }
    // Load matplotlib, scipy, scikit-learn... on first use.
    let loading = false;
    await py.loadPackagesFromImports(msg.code + "\n" + (msg.check || ""), {
      messageCallback: () => { if (!loading) { loading = true; self.postMessage({ type: "loading", id: msg.id }); } },
    });
    py.globals.set("_src", msg.code);
    py.globals.set("_check", msg.check || "");
    py.globals.set("_stdin", msg.stdin || "");
    const out = py.runPython(msg.type === "check"
      ? "json.dumps(runner.check(_src, _check, _stdin))"
      : "json.dumps(runner.run(_src, _stdin))");
    self.postMessage({ type: "result", id: msg.id, result: JSON.parse(out) });
  } catch (err) {
    self.postMessage({ type: "result", id: msg.id, result: { ok: false, parts: [["err", String(err && err.message || err)]], figures: [] } });
  }
};
