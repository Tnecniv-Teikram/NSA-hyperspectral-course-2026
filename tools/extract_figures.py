"""
Extract every figure from the executed course notebooks into slides/figures/, and write an
index so the slide decks (and you) can find them again.

    python tools/extract_figures.py

Output:
    slides/figures/<notebook>/<NN>_<slug>.png      one file per figure
    slides/figures/index.md                         table: notebook · section · file · size
"""
import base64
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "slides" / "figures"


def slug(text, n=40):
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return s[:n] or "figure"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    notebooks = sorted(ROOT.glob("*.ipynb")) + sorted((ROOT / "exercises" / "solutions").glob("*.ipynb"))
    for nb_path in notebooks:
        nb = json.loads(nb_path.read_text())
        stem = nb_path.stem
        folder = OUT / stem
        heading, n = "", 0
        for cell in nb["cells"]:
            src = "".join(cell["source"])
            if cell["cell_type"] == "markdown":
                for line in src.splitlines():
                    if line.startswith("#"):
                        heading = line.lstrip("#").strip()
                continue
            for output in cell.get("outputs", []):
                data = output.get("data", {})
                for mime, ext in (("image/png", "png"), ("image/jpeg", "jpg")):
                    if mime not in data:
                        continue
                    folder.mkdir(parents=True, exist_ok=True)
                    payload = data[mime]
                    raw = base64.b64decode(payload if isinstance(payload, str) else "".join(payload))
                    name = f"{n:02d}_{slug(heading)}.{ext}"
                    (folder / name).write_bytes(raw)
                    rows.append({"notebook": stem, "section": heading,
                                 "file": f"{stem}/{name}", "kb": len(raw) // 1024})
                    n += 1
    lines = ["# Figure index", "",
             f"{len(rows)} figures extracted from the executed notebooks. Paths are relative to `slides/figures/`.",
             "", "| notebook | section | file | size |", "|---|---|---|---|"]
    lines += [f"| {r['notebook']} | {r['section']} | `{r['file']}` | {r['kb']} kB |" for r in rows]
    (OUT / "index.md").write_text("\n".join(lines) + "\n")
    (OUT / "index.json").write_text(json.dumps(rows, indent=1))
    print(f"{len(rows)} figures → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
