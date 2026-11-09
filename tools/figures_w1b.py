"""Purpose-built figures for the week 1 · session 2 deck (w1b).

The other decks illustrate themselves with figures lifted out of the notebooks
(``tools/extract_figures.py``). The introductory session needs a few pictures that no
notebook produces, because they explain the *idea* rather than a result: the data cube,
the difference between summarising and sampling a spectrum, the anatomy of a vegetation
spectrum, where the missions sit, and the trade-off that forces 30 m pixels.

    python tools/figures_w1b.py            # all five figures
    python tools/figures_w1b.py cube       # just one

Figures land in ``slides/figures/w1b/`` and are referenced from
``tools/decks/deck_w1b_intro_hyperspectral.py``.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle
from matplotlib.transforms import Affine2D

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hsi_utils as hu  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "slides" / "figures" / "w1b"

# The deck palette, so the figures and the slides are obviously the same deck.
NAVY, TEAL, SAND, INK, MUTED = "#0A2342", "#2CA6A4", "#E8C46A", "#1A1A1A", "#5A6B7B"
GREY = "#C9D6E0"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Calibri", "Helvetica", "DejaVu Sans"],
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.titlesize": 13,
    "savefig.facecolor": "white",
})

CUBE_SCENE = "20250223_165546_32_4001"      # Usulután, El Salvador — mangrove, estuary, coast


def _save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  {path.relative_to(Path(__file__).resolve().parents[1])}")
    return path


# ----------------------------------------------------------------------------- 1. the cube
def fig_cube():
    """The iconic data cube: a map on top, wavelength going back into the page."""
    scene = hu.get_scene(CUBE_SCENE)
    win = (300, 540, 300, 540)
    cube, wl = scene.read_cube(window=win, bands="good")
    rgb = scene.rgb(window=win)

    # Faces of the cube: spectral slices along the far row and the far column.
    front = cube[:, -1, :]                      # (bands, cols)
    side = cube[:, :, -1]                       # (bands, rows)
    front = np.where(np.isfinite(front), front, np.nan)
    side = np.where(np.isfinite(side), side, np.nan)
    vmin, vmax = np.nanpercentile(np.concatenate([front.ravel(), side.ravel()]), [2, 98])

    # Pick a vegetated pixel, so the spectrum beside the cube is the classic green curve
    # rather than whatever happened to sit under a fixed coordinate.
    nir, red = cube[hu.band_index(wl, 860)], cube[hu.band_index(wl, 660)]
    with np.errstate(invalid="ignore", divide="ignore"):
        ndvi = (nir - red) / (nir + red)
    inner = np.full(ndvi.shape, False)
    inner[20:-20, 20:-20] = True                 # keep the marker away from the cube edges
    ndvi = np.where(inner, ndvi, np.nan)
    r, c = np.unravel_index(np.nanargmax(np.where(np.isfinite(ndvi), ndvi, -9)), ndvi.shape)
    spec = cube[:, r, c]
    px, py = c / cube.shape[2], 1 - r / cube.shape[1]

    fig = plt.figure(figsize=(14.5, 6.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.52, 1], wspace=0.14)
    ax = fig.add_subplot(gs[0, 0])
    axs = fig.add_subplot(gs[0, 1])
    ax.set_xlim(-0.10, 1.70)
    ax.set_ylim(-0.26, 1.72)
    ax.axis("off")
    ax.set_aspect("equal")

    dx, dy = 0.52, 0.42                          # how far the top face recedes

    # top face — the true-colour map
    t_top = Affine2D.from_values(1, 0, dx, dy, 0, 1) + ax.transData
    ax.imshow(rgb, extent=(0, 1, 0, 1), transform=t_top, zorder=3, interpolation="bilinear")

    # front face — wavelength (down) × columns (right)
    t_front = Affine2D.from_values(1, 0, 0, 1, 0, 0) + ax.transData
    ax.imshow(front, extent=(0, 1, 0, 1), transform=t_front, cmap="magma",
              vmin=vmin, vmax=vmax, aspect="auto", zorder=3, interpolation="bilinear")

    # right face — wavelength (down) × rows (receding)
    t_side = Affine2D.from_values(dx, dy, 0, 1, 1, 0) + ax.transData
    ax.imshow(side[:, ::-1], extent=(0, 1, 0, 1), transform=t_side, cmap="magma",
              vmin=vmin, vmax=vmax, aspect="auto", zorder=3, interpolation="bilinear")

    # cube edges
    for pts in ([(0, 1), (1, 1), (1 + dx, 1 + dy), (dx, 1 + dy)],      # top
                [(0, 0), (1, 0), (1, 1), (0, 1)],                      # front
                [(1, 0), (1 + dx, dy), (1 + dx, 1 + dy), (1, 1)]):     # right
        ax.add_patch(Polygon(pts, closed=True, fill=False, edgecolor="white",
                             linewidth=1.6, zorder=4))

    # the marker for that pixel, on the top face
    mx, my = px + dx * py, 1 + dy * py
    ax.plot([mx], [my], marker="s", ms=11, mfc="none", mec=SAND, mew=2.6, zorder=6)
    ax.annotate("one pixel", xy=(mx, my), xytext=(0.04, 1.56), color=NAVY, fontsize=13.5,
                fontweight="bold", zorder=6,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.6,
                                connectionstyle="arc3,rad=-0.25"))

    # axis labels for the cube itself
    # "space (y)" runs along the bottom-right edge, clear of the cube itself
    ax.annotate("", xy=(1.06 + dx, -0.04 + dy), xytext=(1.06, -0.04),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.4))
    ax.text(1.06 + dx / 2, -0.14 + dy / 2, "space (y)", color=MUTED, fontsize=11.5,
            rotation=np.degrees(np.arctan2(dy, dx)), ha="center", va="top")
    ax.text(dx / 2 + 0.5, 1.03 + dy, "space (x)", color=MUTED, fontsize=11.5, ha="center")
    ax.annotate("", xy=(-0.045, 0.12), xytext=(-0.045, 0.88),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.4))
    ax.text(-0.085, 0.5, "wavelength", color=MUTED, fontsize=11.5, rotation=90,
            va="center", ha="center")
    ax.set_title("A hyperspectral image is a cube", fontsize=15, color=NAVY,
                 fontweight="bold", pad=12, loc="left", x=-0.02)

    # the spectrum that one pixel holds — its own panel, so nothing sits over the cube
    wlp, sp = np.asarray(wl, float).copy(), np.asarray(spec, float).copy()
    gaps = np.where(np.diff(wlp) > 20)[0]        # the two water-vapour windows
    wlp, sp = np.insert(wlp, gaps + 1, np.nan), np.insert(sp, gaps + 1, np.nan)
    axs.plot(wlp, sp, color=NAVY, lw=1.8)
    axs.set_xlabel("wavelength (nm)", fontsize=12)
    axs.set_ylabel("reflectance", fontsize=12)
    axs.tick_params(labelsize=10)
    axs.set_xlim(380, 2500)
    axs.set_ylim(0, np.nanmax(sp) * 1.18)
    for s in ("top", "right"):
        axs.spines[s].set_visible(False)
    axs.grid(color=GREY, lw=0.6, alpha=0.5)
    axs.set_axisbelow(True)
    axs.set_title(f"…holds {len(scene.wavelengths)} numbers, not 3",
                  fontsize=15, color=NAVY, fontweight="bold", pad=12, loc="left")
    axs.text(0.0, -0.165, f"Tanager · Usulután, El Salvador · {len(wl)} of "
                          f"{len(scene.wavelengths)} bands survive bad-band removal — "
                          "the two gaps are water vapour",
             transform=axs.transAxes, ha="left", va="top", fontsize=9.5,
             color=MUTED, style="italic")
    return _save(fig, "01_datacube.png")


# -------------------------------------------------------------- 2. summarise vs sample
def fig_band_comb():
    """Sentinel-2's 12 wide boxes against Tanager's ~5 nm sampling, over one real spectrum."""
    wl, spectra, _ = hu.load_library()
    veg = spectra["irrigated_crop"]
    ok = np.isfinite(veg)

    centers = np.array([c for c, _ in hu.SENTINEL2_BANDS.values()])
    fwhms = np.array([f for _, f in hu.SENTINEL2_BANDS.values()])
    s2 = hu.resample_to_sensor(wl, veg, centers, fwhms)

    fig, axes = plt.subplots(2, 1, figsize=(11, 6.4), sharex=True,
                             gridspec_kw=dict(height_ratios=[1, 1], hspace=0.16))

    for ax, title, color in zip(
            axes,
            ["Sentinel-2:  12 bands  —  the spectrum summarised",
             "Tanager:  426 bands at ~5 nm  —  the spectrum sampled"],
            [SAND, TEAL]):
        ax.plot(wl, veg, color=GREY, lw=2.2, zorder=1,
                label="the real surface spectrum")
        ax.set_ylim(0, np.nanmax(veg) * 1.25)
        ax.set_title(title, fontsize=13, color=NAVY, fontweight="bold", loc="left", pad=6)
        ax.set_ylabel("reflectance", fontsize=11)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    # top panel: each Sentinel-2 band as a box of its real width
    for (name, (c, f)), value in zip(hu.SENTINEL2_BANDS.items(), s2):
        if not np.isfinite(value):
            continue
        axes[0].add_patch(Rectangle((c - f / 2, 0), f, value, facecolor=SAND,
                                    edgecolor="#B8923F", lw=0.8, alpha=0.95, zorder=2))
    axes[0].plot(centers, s2, "o", color="#8A6D1F", ms=5, zorder=3,
                 label="one number per band")
    axes[0].legend(loc="upper left", fontsize=10, frameon=False)
    axes[0].annotate("B12 is 175 nm wide:\neverything in here becomes one number",
                     xy=(2202, np.nanmax(s2[-1]) * 0.55), xytext=(1500, np.nanmax(veg) * 1.05),
                     fontsize=10.5, color="#8A6D1F",
                     arrowprops=dict(arrowstyle="->", color="#8A6D1F", lw=1.4))

    # bottom panel: the Tanager samples themselves
    axes[1].vlines(wl[ok], 0, veg[ok], color=TEAL, lw=0.6, alpha=0.75, zorder=2)
    axes[1].plot(wl, veg, color=NAVY, lw=1.4, zorder=3, label="one number every ~5 nm")
    axes[1].legend(loc="upper left", fontsize=10, frameon=False)
    axes[1].set_xlabel("wavelength (nm)", fontsize=11)
    axes[1].annotate("the same region, resolved",
                     xy=(2202, veg[np.argmin(np.abs(wl - 2202))]), xytext=(1500, np.nanmax(veg) * 1.05),
                     fontsize=10.5, color=NAVY,
                     arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4))

    return _save(fig, "02_summarise_vs_sample.png")


# ------------------------------------------------------------ 3. anatomy of a leaf spectrum
def fig_leaf_anatomy():
    """One real vegetation spectrum, with every feature named."""
    wl, spectra, _ = hu.load_library()
    veg = spectra["irrigated_crop"]
    ok = np.isfinite(veg)

    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    # Plot with the NaNs in place: matplotlib breaks the line at the two water-vapour
    # windows, which is exactly where Tanager has no usable bands.
    ax.plot(wl, veg, color=NAVY, lw=2.4, zorder=3)
    top = np.nanmax(veg)
    ax.set_ylim(0, top * 1.58)
    ax.set_xlim(380, 2500)
    ax.set_xlabel("wavelength (nm)", fontsize=12)
    ax.set_ylabel("reflectance", fontsize=12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    # the regions behind the curve
    for x0, x1, label, color in [
            (400, 700, "visible\npigments absorb", "#E8EEF4"),
            (700, 1300, "near infrared\nleaf structure", "#E7F3F0"),
            (1300, 2500, "shortwave infrared\nwater and dry matter", "#F6EFE1")]:
        ax.axvspan(x0, x1, color=color, zorder=0)
        ax.text((x0 + x1) / 2, top * 1.46, label, ha="center", va="center",
                fontsize=11.5, color=MUTED, linespacing=1.3)

    def mark(text, xy, xytext, ha="center", rad=0.0):
        ax.annotate(text, xy=xy, xytext=xytext, ha=ha, fontsize=11.5,
                    color=NAVY, fontweight="bold", linespacing=1.25, zorder=5,
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5,
                                    connectionstyle=f"arc3,rad={rad}"))

    # Short labels only — the slide beside the figure carries the explanation.
    mark("chlorophyll absorbs\nblue and red", (490, top * 0.09), (410, top * 0.66),
         ha="left", rad=0.12)
    ax.annotate("", xy=(672, top * 0.13), xytext=(585, top * 0.62),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5,
                                connectionstyle="arc3,rad=-0.2"), zorder=5)
    mark("green peak", (557, top * 0.18), (575, top * 0.30), ha="left", rad=-0.25)
    mark("red edge", (716, top * 0.48), (800, top * 0.60), ha="left", rad=-0.2)
    mark("NIR plateau", (1080, top * 1.00), (1080, top * 1.22))
    mark("water", (1450, top * 0.16), (1430, top * 0.62), rad=0.15)
    mark("water", (1945, top * 0.07), (1950, top * 0.56), rad=-0.15)
    mark("cellulose\nand lignin", (2210, top * 0.17), (2270, top * 0.62), ha="center", rad=-0.2)

    ax.set_title("Every bend in this curve has a physical cause — and a band narrow enough to see it",
                 fontsize=14, color=NAVY, fontweight="bold", loc="left", pad=10)
    ax.text(0.995, -0.16, "Tanager, irrigated crop · course reference library",
            transform=ax.transAxes, ha="right", fontsize=9.5, color=MUTED, style="italic")
    return _save(fig, "03_leaf_anatomy.png")


# ----------------------------------------------------------------- 4. the mission landscape
def fig_missions():
    """Where the spaceborne imaging spectrometers sit: bands, era, pixel size."""
    missions = [
        # name, year, bands, gsd, hero, label offset in points, alignment
        ("Hyperion (EO-1)", 2000, 220, 30, False, (0, 38), "center"),
        ("DESIS (ISS)", 2018, 235, 30, False, (-34, -34), "right"),
        ("PRISMA", 2019, 239, 30, False, (0, 38), "center"),
        ("EnMAP", 2022, 224, 30, False, (6, -44), "left"),
        ("EMIT (ISS)", 2022, 285, 60, False, (0, 44), "center"),
        ("Tanager-1", 2024, 426, 30, True, (0, 40), "center"),
        ("CHIME / SBG\n(planned)", 2029, 300, 30, False, (0, -52), "center"),
    ]
    fig, ax = plt.subplots(figsize=(11, 5.8))

    # the multispectral baseline, for scale
    ax.axhline(13, color=SAND, lw=2.4, ls="--", zorder=1)
    ax.text(1998.6, 24, "Sentinel-2:  13 bands", color="#8A6D1F", fontsize=11.5,
            fontweight="bold", va="bottom")

    for name, year, bands, gsd, hero, (ox, oy), ha in missions:
        color = TEAL if hero else NAVY
        ax.scatter(year, bands, s=gsd * 26, color=color, alpha=0.9 if hero else 0.45,
                   edgecolor=color, linewidth=2, zorder=3)
        ax.annotate(name, xy=(year, bands), xytext=(ox, oy), textcoords="offset points",
                    ha=ha, va="center", fontsize=11.5, color=color,
                    fontweight="bold" if hero else "normal", linespacing=1.2, zorder=4)

    ax.set_ylim(0, 540)
    ax.set_xlim(1998, 2031.5)
    ax.set_xlabel("first light", fontsize=12)
    ax.set_ylabel("number of bands", fontsize=12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color=GREY, lw=0.6, alpha=0.6)
    ax.set_axisbelow(True)

    # bubble legend, parked in the empty middle-left of the plot
    ax.text(2008.1, 158, "bubble = pixel size", fontsize=10.5, color=MUTED, ha="center")
    for i, (gsd, label) in enumerate([(30, "30 m"), (60, "60 m")]):
        ax.scatter(2006.8 + i * 2.6, 108, s=gsd * 26, color=MUTED, alpha=0.3,
                   edgecolor=MUTED, linewidth=1.5)
        ax.text(2006.8 + i * 2.6, 64, label, va="center", ha="center",
                fontsize=10.5, color=MUTED)

    ax.set_title("Every spaceborne imaging spectrometer sits at 30 m or coarser",
                 fontsize=14, color=NAVY, fontweight="bold", loc="left", pad=10)
    return _save(fig, "04_mission_landscape.png")


# --------------------------------------------------------------------- 5. the trade-off
def fig_tradeoff():
    """Why 426 bands forces a 30 m pixel and an 18 km swath."""
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.3)
    ax.axis("off")

    apex = [(2.9, 5.0), (0.75, 0.75), (5.05, 0.75)]
    ax.add_patch(Polygon(apex, closed=True, facecolor="#EAF4F3", edgecolor=TEAL, lw=2.4))
    ax.text(2.9, 2.35, "a fixed\nnumber of\nphotons", ha="center", va="center",
            fontsize=13, color=NAVY, fontweight="bold", linespacing=1.35)

    for (x, y), label, sub, va in [
            ((2.9, 5.28), "spectral", "426 narrow bands", "bottom"),
            ((1.05, 0.42), "spatial", "30 m pixels", "top"),
            ((5.28, 0.42), "radiometric", "usable SNR", "top")]:
        ax.text(x, y, label, ha="center", va=va, fontsize=13.5,
                color=TEAL, fontweight="bold")
        ax.text(x, y + (0.26 if va == "bottom" else -0.3), sub, ha="center", va=va,
                fontsize=11, color=MUTED)

    ax.add_patch(FancyArrowPatch((5.6, 2.9), (6.5, 2.9), arrowstyle="->",
                                 mutation_scale=22, color=MUTED, lw=2))

    ax.text(6.75, 4.55, "What that buys you", fontsize=13.5, color=NAVY, fontweight="bold")
    lines = [
        ("Split the light 426 ways", "and each band gets less of it"),
        ("Keep the pixels large", "so every band still beats the noise"),
        ("Keep the swath narrow", "Tanager sees ~18 km, not 290 km"),
        ("So: tasked scenes", "not wall-to-wall, not daily"),
    ]
    for i, (head, tail) in enumerate(lines):
        y = 3.85 - i * 0.82
        ax.text(6.75, y, head, fontsize=12, color=NAVY, fontweight="bold")
        ax.text(6.75, y - 0.3, tail, fontsize=11, color=MUTED)

    ax.add_patch(Rectangle((6.6, 0.18), 3.3, 0.62, facecolor=NAVY, edgecolor="none"))
    ax.text(8.25, 0.49, "Hyperspectral complements\nSentinel-2 — it does not replace it",
            ha="center", va="center", fontsize=11, color="white", fontweight="bold",
            linespacing=1.3)

    ax.set_title("Spectral detail is paid for in pixel size and swath",
                 fontsize=14, color=NAVY, fontweight="bold", loc="left", pad=6)
    return _save(fig, "05_tradeoff.png")


# ------------------------------------------------------------ 6. the six themes, spectrally
def fig_theme_fingerprints():
    """One panel per challenge theme: the material, and the region that gives it away."""
    wl, spectra, _ = hu.load_library()

    panels = [
        ("Agriculture", [("irrigated_crop", TEAL), ("dry_steppe_grassland", "#B8923F")],
         (690, 760), "red edge moves with crop health"),
        ("Land cover and urban", [("dense_urban", NAVY), ("bright_industrial_roof", "#C25E5E")],
         (2050, 2400), "roof and pavement materials differ in the SWIR"),
        ("Air quality and GHG", [("dry_bare_soil", "#8A6D1F"), ("desert_sand", SAND)],
         (2200, 2400), "methane absorbs here, over bright ground"),
        ("Disasters", [("burn_scar", "#6B3F3F"), ("chaparral_unburned", "#4F8F5B")],
         (2000, 2350), "char and ash vs living vegetation"),
        ("Blue carbon", [("mangrove", "#1F7A5A"), ("tropical_tree_cover", "#7FBF9B")],
         (700, 1300), "mangrove vs other canopy: NIR structure"),
        ("Water quality", [("turbid_estuary_water", "#9A7B4F"), ("clear_ocean", "#2E6F9E")],
         (400, 700), "pigments and sediment, all in the visible"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(14.5, 6.4))
    for ax, (theme, curves, (x0, x1), note) in zip(axes.ravel(), panels):
        ax.axvspan(x0, x1, color=TEAL, alpha=0.12, zorder=0)
        for name, color in curves:
            ax.plot(wl, spectra[name], color=color, lw=1.7,
                    label=name.replace("_", " "), zorder=2)
        ax.set_xlim(380, 2500)
        ax.set_ylim(0, None)
        ax.set_title(theme, fontsize=13, color=NAVY, fontweight="bold", loc="left", pad=6)
        ax.text(0.5, -0.30, note, transform=ax.transAxes, ha="center", va="top",
                fontsize=10, color=MUTED, style="italic")
        ax.legend(fontsize=8.5, frameon=False, loc="upper left", handlelength=1.2,
                  borderpad=0.1, labelspacing=0.2)
        ax.tick_params(labelsize=9)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    for ax in axes[1]:
        ax.set_xlabel("wavelength (nm)", fontsize=10.5)
    for ax in axes[:, 0]:
        ax.set_ylabel("reflectance", fontsize=10.5)

    fig.suptitle("Six themes, six places in the spectrum to look",
                 fontsize=15, color=NAVY, fontweight="bold", x=0.009, ha="left", y=1.005)
    fig.tight_layout(h_pad=3.4, w_pad=2.0)
    return _save(fig, "06_theme_fingerprints.png")


FIGURES = {"cube": fig_cube, "comb": fig_band_comb, "leaf": fig_leaf_anatomy,
           "missions": fig_missions, "tradeoff": fig_tradeoff,
           "themes": fig_theme_fingerprints}

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(FIGURES)
    print(f"writing to {OUT}")
    for key in wanted:
        if key not in FIGURES:
            raise SystemExit(f"unknown figure {key!r} — choose from {list(FIGURES)}")
        FIGURES[key]()
