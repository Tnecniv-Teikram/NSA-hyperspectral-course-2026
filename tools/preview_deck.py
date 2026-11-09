"""Render a generated deck to PNG contact sheets, without PowerPoint.

PowerPoint's AppleScript export times out on this machine, and LibreOffice is not installed,
so this redraws each slide from the shapes python-pptx can see: filled rectangles, text boxes
at their real position, size and colour, tables, and the embedded images themselves. Fonts
are substituted, so treat it as a layout proof — enough to catch an image that overflows, a
title that collides with a figure, or a slide that is mostly empty.

    python tools/preview_deck.py slides/w1b_intro_hyperspectral_eo.pptx
    python tools/preview_deck.py slides/w1b_intro_hyperspectral_eo.pptx --per-sheet 6

Writes ``<deck name>_preview_N.png`` into ``slides/previews/``.
"""
import argparse
import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pptx import Presentation
from pptx.util import Emu

ROOT = Path(__file__).resolve().parents[1]
W_IN, H_IN = 13.333, 7.5


def _rgb(color):
    try:
        if color and color.type is not None and color.rgb is not None:
            return "#" + str(color.rgb)
    except Exception:
        pass
    return None


def _align(paragraph):
    a = str(paragraph.alignment or "")
    return "center" if "CENTER" in a else ("right" if "RIGHT" in a else "left")


def draw_slide(ax, slide):
    ax.set_xlim(0, W_IN)
    ax.set_ylim(H_IN, 0)            # y grows downward, like a slide
    ax.axis("off")
    ax.set_aspect("equal")

    for shape in slide.shapes:
        x, y = Emu(shape.left).inches, Emu(shape.top).inches
        w, h = Emu(shape.width).inches, Emu(shape.height).inches

        if shape.shape_type == 13:                       # picture
            try:
                img = plt.imread(io.BytesIO(shape.image.blob))
                ax.imshow(img, extent=(x, x + w, y + h, y), zorder=3, aspect="auto")
            except Exception:
                ax.add_patch(Rectangle((x, y), w, h, facecolor="#DDDDDD", zorder=3))
            continue

        if shape.has_table:
            tbl = shape.table
            nrows = len(tbl.rows)
            rh = h / max(nrows, 1)
            for r_i, row in enumerate(tbl.rows):
                cx = x
                for c_i, cell in enumerate(row.cells):
                    cw = Emu(tbl.columns[c_i].width).inches
                    ax.add_patch(Rectangle((cx, y + r_i * rh), cw, rh, zorder=3,
                                           facecolor="#0A2342" if r_i == 0 else "white",
                                           edgecolor="#C9D6E0", linewidth=0.5))
                    ax.text(cx + 0.06, y + r_i * rh + rh / 2, cell.text[:38],
                            fontsize=11, va="center", zorder=4,
                            color="white" if r_i == 0 else "#1A1A1A")
                    cx += cw
            continue

        fill = None
        try:
            if shape.fill.type is not None and str(shape.fill.type) != "MSO_FILL_TYPE.BACKGROUND":
                fill = _rgb(shape.fill.fore_color)
        except Exception:
            pass
        if fill:
            ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor="none",
                                   zorder=1 if (w > W_IN * 0.95 and h > H_IN * 0.95) else 2))

        if not shape.has_text_frame or not shape.text_frame.text.strip():
            continue

        cursor = y + 0.06
        for p in shape.text_frame.paragraphs:
            if not p.runs:
                cursor += 0.12
                continue
            size = max((r.font.size.pt if r.font.size else 18) for r in p.runs)
            bold = any(r.font.bold for r in p.runs)
            color = next((_rgb(r.font.color) for r in p.runs if _rgb(r.font.color)), "#1A1A1A")
            text = "".join(r.text for r in p.runs)
            per_line = max(8, int(w * 72 / (size * 0.52)))
            lines = [text[i:i + per_line] for i in range(0, len(text), per_line)] or [""]
            ha = _align(p)
            tx = x + 0.06 if ha == "left" else (x + w / 2 if ha == "center" else x + w - 0.06)
            for line in lines:
                cursor += size * 1.28 / 72
                ax.text(tx, cursor, line, fontsize=size, ha=ha, va="baseline",
                        color=color, fontweight="bold" if bold else "normal", zorder=5)
            cursor += 0.04


def render_one(slide, dpi):
    """One slide, in a figure the exact size of the slide, so 1 pt of text = 1/72 in."""
    fig = plt.figure(figsize=(W_IN, H_IN))
    ax = fig.add_axes([0, 0, 1, 1])
    draw_slide(ax, slide)
    buf = io.BytesIO()
    fig.savefig(buf, dpi=dpi, facecolor="white")
    plt.close(fig)
    buf.seek(0)
    from PIL import Image
    return Image.open(buf).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--per-sheet", type=int, default=6)
    ap.add_argument("--dpi", type=int, default=74)
    args = ap.parse_args()

    from PIL import Image, ImageDraw

    path = Path(args.deck)
    path = path if path.is_absolute() else ROOT / path
    prs = Presentation(path)
    slides = list(prs.slides)
    out_dir = ROOT / "slides" / "previews"
    out_dir.mkdir(parents=True, exist_ok=True)

    cols, pad, label = 2, 16, 18
    written = []
    for start in range(0, len(slides), args.per_sheet):
        chunk = slides[start:start + args.per_sheet]
        tiles = [render_one(s, args.dpi) for s in chunk]
        tw, th = tiles[0].size
        rows = (len(tiles) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad,
                                  rows * (th + label) + (rows + 1) * pad), "white")
        draw = ImageDraw.Draw(sheet)
        for k, tile in enumerate(tiles):
            r, c = divmod(k, cols)
            x = pad + c * (tw + pad)
            y = pad + r * (th + label + pad)
            draw.text((x, y), f"slide {start + k + 1}", fill="#5A6B7B")
            sheet.paste(tile, (x, y + label))
            draw.rectangle([x, y + label, x + tw - 1, y + label + th - 1], outline="#9AA7B4")
        name = out_dir / f"{path.stem}_preview_{start // args.per_sheet + 1}.png"
        sheet.save(name)
        written.append(name)
        print(f"  {name.relative_to(ROOT)}")
    print(f"{len(slides)} slides \u2192 {len(written)} sheet(s)")


if __name__ == "__main__":
    main()
