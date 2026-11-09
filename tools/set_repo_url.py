"""
Point the Colab badges and bootstrap cells at your GitHub repository.

After you create (or rename) the repository, run this once:

    python tools/set_repo_url.py your-org/your-repo [--branch main]

It finds the slug the material currently uses — read from the Colab badges, so there is
nothing to keep in sync by hand — and replaces exactly that slug in every notebook badge,
every Colab bootstrap cell, the README and the teaching plan.

Only that one slug is touched. An earlier version rewrote *every* ``github.com/<owner>/<repo>``
it found, which also silently rewrote the link to the companion hackathon repository and to
third-party projects such as ``banesullivan/localtileserver``. Pass ``--from`` if the badges
are missing and the current slug cannot be detected.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"
BADGE_RE = re.compile(rf"colab\.research\.google\.com/github/({SLUG})")


def files():
    for path in sorted(ROOT.rglob("*.ipynb")):
        if ".ipynb_checkpoints" not in str(path):
            yield path
    for name in ("README.md", "teaching_plan.md"):
        if (ROOT / name).exists():
            yield ROOT / name


def detect_slug():
    """The slug the material uses today, taken from the Colab badges."""
    found = set()
    for path in files():
        found.update(BADGE_RE.findall(path.read_text()))
    if len(found) > 1:
        sys.exit(f"the badges disagree: {', '.join(sorted(found))} — rerun with --from <slug>")
    return found.pop() if found else None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", help="owner/repository, e.g. space42/hyperspectral-course-2026")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--from", dest="old", default=None,
                    help="the slug to replace (default: detected from the Colab badges)")
    args = ap.parse_args()
    if "/" not in args.slug:
        sys.exit("slug must look like owner/repository")

    old = args.old or detect_slug()
    if not old:
        sys.exit("no Colab badge found, so the current slug cannot be detected — "
                 "pass it explicitly with --from <owner>/<repo>")
    if old == args.slug:
        print(f"already pointing at {args.slug} — nothing to do")
        return

    # Only the blob/<branch> of our own badge URLs, so other /blob/ links are left alone.
    branch_re = re.compile(rf"(github/{re.escape(args.slug)}/blob/)[A-Za-z0-9_.\-/]+?(/)")

    changed = 0
    for path in files():
        before = path.read_text()
        after = branch_re.sub(rf"\g<1>{args.branch}\g<2>", before.replace(old, args.slug))
        if after == before:
            continue
        if path.suffix == ".ipynb":
            json.loads(after)              # refuse to write a notebook we just broke
        path.write_text(after)
        changed += 1

    print(f"updated {changed} files: {old} → {args.slug} (branch {args.branch})")


if __name__ == "__main__":
    main()
