"""
mangrove_product.py — the example "product" of notebook 31.

The same code is used three ways:
  * from the notebook            (`import mangrove_product as mp; mp.run_pipeline(...)`)
  * from the command line        (`python app/mangrove_product.py --scene <id> --window r0 r1 c0 c1`)
  * from the Streamlit viewer    (`streamlit run app/streamlit_app.py`)

That is the point: a product is code that runs the same way every time, writes its outputs and
its provenance to disk, and can be scheduled or called by someone who never opens your notebook.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hsi_utils as hu  # noqa: E402

MODEL_PATH = hu.OUTPUT_DIR / "31" / "mangrove_rf.joblib"

# Features the model sees. Keeping them few and named makes the product explainable and fast.
FEATURE_NAMES = ["NDVI", "NDWI", "NDMI", "NDRE", "brightness", "swir_ratio"]


def compute_features(scene, window, use_cloud_mask=True):
    """Return (features (6, rows, cols), valid mask) for one window of a scene."""
    b = {name: scene.read_band(nm, window, cloud=use_cloud_mask)
         for name, nm in dict(green=560, red=665, rededge=720, nir=860, swir1=1650, swir2=2200).items()}
    feats = np.stack([
        hu.nd(b["nir"], b["red"]),                                    # NDVI  — greenness
        hu.nd(b["green"], b["nir"]),                                  # NDWI  — open water
        hu.nd(b["nir"], b["swir1"]),                                  # NDMI  — canopy water
        hu.nd(b["nir"], b["rededge"]),                                # NDRE  — chlorophyll
        np.mean(np.stack([b["green"], b["red"], b["nir"]]), axis=0),  # brightness (NaN if any band is NaN)
        b["swir1"] / (b["swir2"] + 1e-6),                             # SWIR ratio — soil/leaf water
    ]).astype("float32")
    return feats, np.all(np.isfinite(feats), axis=0)


def minimum_mapping_unit(mask, min_pixels=5):
    """Drop connected patches smaller than ``min_pixels`` (a 5-pixel patch is ~0.45 ha at 30 m)."""
    from scipy import ndimage
    lab, n = ndimage.label(mask)
    if n == 0:
        return mask
    sizes = ndimage.sum(mask, lab, index=np.arange(1, n + 1))
    keep = np.zeros(n + 1, bool)
    keep[1:] = sizes >= min_pixels
    return keep[lab]


def run_pipeline(scene_id, window=None, model_path=MODEL_PATH, out_dir=None, min_pixels=5,
                 use_cloud_mask=True, verbose=True):
    """Map mangrove extent for one scene window and write the product to disk.

    Writes: <out_dir>/<run_id>/{mangrove.tif, quicklook.png, metadata.json, report.html}
    Returns the metadata dictionary.
    """
    import joblib
    # Figure/FigureCanvasAgg instead of pyplot: writing a PNG from a library must not change
    # the caller's matplotlib backend (that would stop figures rendering inside a notebook).
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    t0 = time.time()
    model = joblib.load(model_path)
    scene = hu.get_scene(scene_id)
    feats, valid = compute_features(scene, window, use_cloud_mask)

    proba = np.full(valid.shape, np.nan, dtype="float32")
    if valid.any():
        X = feats[:, valid].T
        proba[valid] = model.predict_proba(X)[:, 1]
    mangrove = minimum_mapping_unit(np.nan_to_num(proba) >= 0.5, min_pixels)

    px_ha = scene.res_x * scene.res_y / 1e4
    area_ha = float(mangrove.sum() * px_ha)
    coverage = float(valid.mean())

    run_id = f"{scene_id}_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
    out = Path(out_dir or (hu.OUTPUT_DIR / "31")) / run_id
    out.mkdir(parents=True, exist_ok=True)

    hu.save_geotiff(out / "mangrove.tif",
                    np.stack([mangrove.astype("uint8"), (np.nan_to_num(proba) * 100).astype("uint8")]),
                    scene.transform(window), scene.crs, nodata=None,
                    band_names=["mangrove_mask", "probability_percent"])

    fig = Figure(figsize=(11, 5)); FigureCanvasAgg(fig)
    ax = fig.subplots(1, 2)
    ax[0].imshow(scene.rgb(window)); ax[0].set_title(f"{scene_id}\ntrue colour")
    ax[1].imshow(scene.rgb(window))
    ax[1].imshow(np.ma.masked_where(~mangrove, mangrove), cmap="spring", alpha=0.65, vmin=0, vmax=1)
    ax[1].set_title(f"mangrove extent — {area_ha:,.0f} ha")
    for a in ax:
        a.axis("off")
    fig.tight_layout(); fig.savefig(out / "quicklook.png", dpi=110, bbox_inches="tight")

    west, south, east, north = scene.bounds_lonlat() if window is None else _window_bounds(scene, window)
    meta = {
        "product": "mangrove_extent_v1",
        "run_id": run_id,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scene_id": scene_id,
        "scene_datetime": scene.info.get("place"),
        "window": list(window) if window else None,
        "crs": scene.crs,
        "bbox_lonlat": [round(v, 5) for v in (west, south, east, north)],
        "pixel_size_m": round(scene.res_x, 2),
        "model": {"path": str(Path(model_path).name), "features": FEATURE_NAMES,
                  "type": type(model).__name__, "threshold": 0.5, "min_pixels": min_pixels},
        "results": {"mangrove_area_ha": round(area_ha, 1),
                    "mangrove_pixels": int(mangrove.sum()),
                    "valid_pixel_fraction": round(coverage, 4),
                    "mean_probability_in_mangrove": round(float(np.nanmean(proba[mangrove])), 3) if mangrove.any() else None},
        "quality_flags": _quality_flags(coverage, area_ha, use_cloud_mask),
        "runtime_seconds": round(time.time() - t0, 1),
        "software": {"python": platform.python_version(), "numpy": np.__version__},
        "attribution": hu.attribution(scene_id),
    }
    (out / "metadata.json").write_text(json.dumps(meta, indent=2))
    (out / "report.html").write_text(_html_report(meta))
    if verbose:
        print(f"{run_id}: {area_ha:,.0f} ha mangrove, {coverage * 100:.1f}% usable pixels, "
              f"{meta['runtime_seconds']} s → {out}")
    return meta


def _window_bounds(scene, window):
    from rasterio.warp import transform_bounds
    r0, r1, c0, c1 = window
    x0, y0 = scene.xy(r0, c0)
    x1, y1 = scene.xy(r1, c1)
    return transform_bounds(scene.crs, "EPSG:4326", min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def _quality_flags(coverage, area_ha, use_cloud_mask):
    """Simple, explicit rules so a user can see when not to trust a run."""
    flags = []
    if coverage < 0.6:
        flags.append("LOW_COVERAGE: more than 40% of the window is cloud/no-data")
    if area_ha == 0:
        flags.append("NO_DETECTION: no mangrove pixels found")
    if not use_cloud_mask:
        flags.append("CLOUD_MASK_OFF: run made without the cloud mask (check for bright-surface flags)")
    return flags or ["OK"]


def _html_report(meta):
    r = meta["results"]
    rows = "".join(f"<tr><td>{k.replace('_', ' ')}</td><td><b>{v}</b></td></tr>" for k, v in r.items())
    flags = "".join(f"<li>{f}</li>" for f in meta["quality_flags"])
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Mangrove extent — {meta['run_id']}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#222}}
table{{border-collapse:collapse;margin:1rem 0}}td{{border:1px solid #ddd;padding:.4rem .8rem}}
img{{max-width:100%;border:1px solid #eee}}code{{background:#f5f5f5;padding:.1rem .3rem}}</style></head><body>
<h1>Mangrove extent</h1>
<p>Scene <code>{meta['scene_id']}</code> · generated {meta['generated_utc']} · product {meta['product']}</p>
<img src="quicklook.png" alt="quicklook">
<h2>Results</h2><table>{rows}</table>
<h2>Quality flags</h2><ul>{flags}</ul>
<h2>How it was made</h2>
<p>Model: {meta['model']['type']} on {', '.join(meta['model']['features'])};
probability threshold {meta['model']['threshold']}, minimum mapping unit {meta['model']['min_pixels']} pixels
({meta['pixel_size_m']} m pixels). Runtime {meta['runtime_seconds']} s.</p>
<p style="color:#666;font-size:.9em">{meta['attribution']}</p>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Map mangrove extent from a Tanager scene.")
    ap.add_argument("--scene", required=True, help="Tanager scene ID")
    ap.add_argument("--window", nargs=4, type=int, metavar=("R0", "R1", "C0", "C1"),
                    help="pixel window; omit for the whole scene")
    ap.add_argument("--model", default=str(MODEL_PATH))
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--min-pixels", type=int, default=5)
    ap.add_argument("--no-cloud-mask", action="store_true")
    args = ap.parse_args()
    meta = run_pipeline(args.scene, tuple(args.window) if args.window else None, args.model,
                        args.out_dir, args.min_pixels, not args.no_cloud_mask)
    print(json.dumps(meta["results"], indent=2))


if __name__ == "__main__":
    main()
