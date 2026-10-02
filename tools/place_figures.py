"""Insert ![alt](figures/name.svg) lines into course content files (part*.md).

plan entries: (lesson_id, mode, anchor, figure_name, alt)
  mode "before": insert just before the first line in the lesson that starts with anchor
  mode "after":  insert after the block that starts with anchor (a paragraph, a table, or a code
                 fence plus any output fences after it); for a heading, after the first block under it
  mode "after+1": the same, then skip one more block
Lines already containing the figure are skipped, so running twice is safe.
"""
import glob
from pathlib import Path


def _block_end(L, i):
    while L[i].strip() == "":
        i += 1
    if L[i].startswith("```"):
        while True:
            i += 1
            while not L[i].startswith("```"):
                i += 1
            i += 1
            j = i
            while j < len(L) and L[j].strip() == "":
                j += 1
            if j < len(L) and L[j].startswith("```output"):
                i = j
                continue
            return i
    while i < len(L) and L[i].strip() != "":
        i += 1
    return i


def place(content_dir, plan):
    files = {f: Path(f).read_text().split("\n") for f in sorted(glob.glob(str(Path(content_dir) / "part*.md")))}
    for lid, mode, anchor, fig, alt in plan:
        line = f"![{alt}](figures/{fig}.svg)"
        for f, L in files.items():
            if f"id: {lid}" not in L:
                continue
            start = L.index(f"id: {lid}")
            end = next((i for i in range(start + 1, len(L)) if L[i].startswith("@@@ lesson")), len(L))
            if any(f"(figures/{fig}.svg)" in x for x in L[start:end]):
                break
            h = next(i for i in range(start, end) if L[i].startswith(anchor))
            if mode == "before":
                L[h:h] = [line, ""]
            else:
                i = _block_end(L, h + 1) if L[h].startswith("#") else _block_end(L, h)
                if mode == "after+1":
                    i = _block_end(L, i)
                L[i:i] = ["", line]
            break
        else:
            raise SystemExit(f"lesson not found: {lid}")
    for f, L in files.items():
        Path(f).write_text("\n".join(L))
