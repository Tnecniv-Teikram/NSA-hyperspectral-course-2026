"""
Check the generated decks for layout risks that the builder's guards cannot see.

    python tools/lint_decks.py [slides/one_deck.pptx ...]

Estimates how tall each text box renders (characters per line from the box width and font size)
and flags boxes that overflow, tables that are too tall, very long titles, and content slides
without speaker notes. It is an approximation — it catches the cases worth looking at by eye.
"""
import math
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

ROOT = Path(__file__).resolve().parents[1]
SLIDE_H_IN = 7.5
CHAR_W = 0.50      # average glyph width as a fraction of font size
LINE_H = 1.28      # line height as a multiple of font size


def text_height_in(shape):
    """Rough rendered height of a text frame, in inches."""
    width_in = Emu(shape.width).inches - 0.2
    total = 0.0
    for p in shape.text_frame.paragraphs:
        size = max([(r.font.size.pt if r.font.size else 18) for r in p.runs], default=18)
        chars = sum(len(r.text) for r in p.runs)
        if chars == 0:
            total += size * LINE_H / 72
            continue
        per_line = max(8, int(width_in * 72 / (size * CHAR_W)))
        lines = math.ceil(chars / per_line)
        total += lines * size * LINE_H / 72 + (p.space_after.pt / 72 if p.space_after else 0)
    return total


def lint(path):
    prs = Presentation(path)
    issues, notes_missing = [], []
    for i, slide in enumerate(prs.slides, start=1):
        has_text, has_note = False, bool(
            slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip())
        for shape in slide.shapes:
            if shape.has_text_frame and shape.text_frame.text.strip():
                has_text = True
                top_in = Emu(shape.top).inches
                need = text_height_in(shape)
                avail = Emu(shape.height).inches
                if need > avail * 1.10 and top_in + need > SLIDE_H_IN - 0.45:
                    issues.append(f"  slide {i:2d}: text may overflow the slide "
                                  f"(needs ~{need:.1f}in from {top_in:.1f}in) — "
                                  f"{shape.text_frame.text.strip()[:45]!r}")
                first = shape.text_frame.paragraphs[0]
                size0 = max([(r.font.size.pt if r.font.size else 0) for r in first.runs], default=0)
                if size0 >= 25 and len(first.text) > 110:
                    issues.append(f"  slide {i:2d}: long title ({len(first.text)} chars) — "
                                  f"{first.text[:50]!r}")
            if shape.has_table:
                tbl = shape.table
                rows = len(tbl.rows)
                if Emu(shape.top).inches + rows * 0.42 > SLIDE_H_IN - 0.5:
                    issues.append(f"  slide {i:2d}: table with {rows} rows may run off the slide")
                for r_i, row in enumerate(tbl.rows):
                    for c_i, cell in enumerate(row.cells):
                        col_in = Emu(tbl.columns[c_i].width).inches - 0.2
                        per_line = max(8, int(col_in * 72 / (13 * CHAR_W)))
                        if math.ceil(len(cell.text) / per_line) > 3:
                            issues.append(f"  slide {i:2d}: table cell r{r_i}c{c_i} needs "
                                          f"{math.ceil(len(cell.text) / per_line)} lines in a "
                                          f"{col_in:.1f}in column")
        # Section dividers and the references slide carry no notes by design: a content slide is one
        # with a multi-paragraph body, a picture or a table.
        bodies = [sh for sh in slide.shapes if sh.has_text_frame
                  and len(sh.text_frame.paragraphs) > 1 and len(sh.text_frame.text) > 80]
        visual = any(sh.shape_type == 13 or sh.has_table for sh in slide.shapes)
        is_refs = slide.shapes[1].text_frame.text.startswith("References") if len(slide.shapes) > 1 and slide.shapes[1].has_text_frame else False
        if has_text and not has_note and i > 1 and (bodies or visual) and not is_refs:
            notes_missing.append(f"  slide {i:2d}: no speaker notes")
    return len(prs.slides._sldIdLst), issues, notes_missing


def main():
    paths = [Path(p) for p in sys.argv[1:]] or sorted((ROOT / "slides").glob("*.pptx"))
    total_issues = 0
    for p in paths:
        n, issues, notes_missing = lint(p)
        flag = "OK" if not issues else f"{len(issues)} layout issue(s)"
        extra = f" · {len(notes_missing)} content slide(s) without notes" if notes_missing else ""
        print(f"{p.name:46s} {n:3d} slides  {flag}{extra}")
        for line in issues + notes_missing:
            print(line)
        total_issues += len(issues)
    print(f"\n{len(paths)} decks, {total_issues} layout issue(s)")
    return 1 if total_issues else 0


if __name__ == "__main__":
    sys.exit(main())
