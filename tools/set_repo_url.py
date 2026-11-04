"""
Point the Colab badges and bootstrap cells at your GitHub repository.

After you create the repository, run this once:

    python tools/set_repo_url.py your-org/your-repo [--branch main]

It rewrites the repository slug in every notebook badge, in every Colab bootstrap
cell, and in the README, so the "Open in Colab" buttons resolve to your copy.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG_RE = re.compile(r"(github\.com/)[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
COLAB_RE = re.compile(r"(colab\.research\.google\.com/github/)[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
REPO_CONST_RE = re.compile(r'(REPO\s*=\s*")[^"]+(")')
BRANCH_RE = re.compile(r"(/blob/)[A-Za-z0-9_.\-/]+?(/)")


def rewrite(text, slug, branch):
    text = COLAB_RE.sub(rf"\g<1>{slug}", text)
    text = SLUG_RE.sub(rf"\g<1>{slug}", text)
    text = REPO_CONST_RE.sub(rf"\g<1>{slug}\g<2>", text)
    text = BRANCH_RE.sub(rf"\g<1>{branch}\g<2>", text)
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", help="owner/repository, e.g. space42/hyperspectral-course-2026")
    ap.add_argument("--branch", default="main")
    args = ap.parse_args()
    if "/" not in args.slug:
        sys.exit("slug must look like owner/repository")

    changed = 0
    for path in list(ROOT.rglob("*.ipynb")) + [ROOT / "README.md", ROOT / "teaching_plan.md"]:
        if ".ipynb_checkpoints" in str(path) or not path.exists():
            continue
        before = path.read_text()
        after = rewrite(before, args.slug, args.branch)
        if after != before:
            if path.suffix == ".ipynb":
                json.loads(after)          # refuse to write a notebook we just broke
            path.write_text(after)
            changed += 1
    print(f"updated {changed} files → https://github.com/{args.slug} (branch {args.branch})")


if __name__ == "__main__":
    main()
