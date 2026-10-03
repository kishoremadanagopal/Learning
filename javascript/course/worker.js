/* A module Web Worker that runs the learner's JavaScript off the main thread, so a long or endless loop never
   freezes the page and Stop can end it. The same runner.js is used by the Node.js test harness. */
const loading = import("./runner.js" + self.location.search);   // versioned like the page's other files

self.addEventListener("unhandledrejection", async (e) => { e.preventDefault(); (await loading).reportUnhandled(e.reason); });
self.addEventListener("error", async (e) => { e.preventDefault(); (await loading).reportUnhandled(e.error || new Error(e.message)); });

self.onmessage = async (e) => {
  const msg = e.data;
  let R;
  try {
    R = await loading;
  } catch (err) {
    self.postMessage({ type: "failed", error: String(err && err.message || err) });
    return;
  }
  if (msg.type === "init") {
    self.postMessage({ type: "ready" });
    return;
  }
  let result;
  try {
    result = msg.type === "check"
      ? await R.check(msg.code, msg.check || "", msg.stdin || "")
      : await R.run(msg.code, msg.stdin || "");
  } catch (err) {
    result = { ok: false, parts: [["err", String(err && err.message || err)]], figures: [] };
  }
  self.postMessage({ type: "result", id: msg.id, result });
};
