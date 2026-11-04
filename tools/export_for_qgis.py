"""
Export a Tanager scene (or window) to a file QGIS and the EnMAP-Box can read *with* wavelengths.

QGIS shows any multi-band raster, but a hyperspectral cube is only useful there if the
per-band wavelengths travel with the data — otherwise the EnMAP-Box spectral profile tool
plots "band number" instead of a spectrum. Wavelength metadata is carried in GDAL's **ENVI
metadata domain** (`wavelength`, `wavelength_units`, `fwhm`, `bbl`), which both an ENVI
`.hdr` file and a GeoTIFF can hold.

    python tools/export_for_qgis.py                                   # default lab exports
    python tools/export_for_qgis.py --scene 20250219_053251_31_4001 --window 480 780 250 550
    python tools/export_for_qgis.py --scene ... --format gtiff --all-bands

Output (in data/qgis/):
    <scene>_<r0>_<c0>_bsq.hdr / .bsq     ENVI — the safest option for the EnMAP-Box
    <scene>_<r0>_<c0>.tif                GeoTIFF with the same metadata in the ENVI domain
    <scene>_<r0>_<c0>_rgb.tif            8-bit true-colour COG, for a quick backdrop

Reflectance is stored as int16 × 10000 (the same convention as EnMAP L2A products).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import rasterio

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hsi_utils as hu  # noqa: E402

SCALE = 10000
NODATA = -32768

# Windows chosen for the QGIS lab: a coastal/mangrove scene and a mining/mineral scene.
DEFAULT_EXPORTS = [
    ("20250223_165546_32_4001", (150, 500, 150, 500)),   # El Salvador: mangrove, water, crops
    ("20250219_053251_31_4001", (450, 750, 230, 530)),   # Korba: coal mines, spoil, water
]


def _envi_list(values, fmt="{:.2f}"):
    return "{" + ", ".join(fmt.format(v) for v in values) + "}"


def export(scene_id, window, out_dir, fmt="envi", all_bands=False, rgb=True, verbose=True):
    scene = hu.get_scene(scene_id)
    bands = "all" if all_bands else "good"
    cube, wl = scene.read_cube(window, bands=bands, mask=False)
    keep = np.ones(len(wl), bool) if all_bands else scene.good_bands
    fwhm = scene.fwhm[keep]
    bbl = np.ones(len(wl), int)          # every exported band is good; bbl kept for completeness

    data = np.where(np.isfinite(cube), np.clip(cube * SCALE, -32767, 32767), NODATA).astype("int16")
    r0, r1, c0, c1 = scene._window(window)
    transform = scene.transform(window)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{scene_id}_{r0}_{c0}"
    written = []

    profile = dict(width=data.shape[2], height=data.shape[1], count=data.shape[0], dtype="int16",
                   crs=scene.crs, transform=transform, nodata=NODATA)
    envi_tags = {
        "wavelength": _envi_list(wl),
        "wavelength_units": "Nanometers",
        "fwhm": _envi_list(fwhm),
        "bbl": _envi_list(bbl, "{:d}"),
        "reflectance_scale_factor": str(SCALE),
    }

    if fmt in ("envi", "both"):
        path = out_dir / f"{stem}_bsq.bsq"
        with rasterio.open(path, "w", driver="ENVI", interleave="bsq", **profile) as dst:
            dst.write(data)
            dst.update_tags(ns="ENVI", **envi_tags)
            for i, w in enumerate(wl, start=1):
                dst.set_band_description(i, f"{w:.1f} nm")
        _patch_envi_header(path.with_suffix(".hdr"), wl, fwhm, bbl, scene_id)
        written.append(path)

    if fmt in ("gtiff", "both"):
        path = out_dir / f"{stem}.tif"
        with rasterio.open(path, "w", driver="GTiff", tiled=True, compress="deflate",
                           interleave="band", **profile) as dst:
            dst.write(data)
            dst.update_tags(ns="ENVI", **envi_tags)
            for i, w in enumerate(wl, start=1):
                dst.set_band_description(i, f"{w:.1f} nm")
                dst.update_tags(i, wavelength=f"{w:.2f}", wavelength_units="nm", fwhm=f"{fwhm[i-1]:.2f}")
        written.append(path)

    if rgb:
        path = out_dir / f"{stem}_rgb.tif"
        rgb_arr = (hu.stretch(np.dstack([cube[hu.band_index(wl, b)] for b in (640, 550, 460)]),
                              (2, 98)) * 255)
        rgb_arr = np.nan_to_num(rgb_arr).astype("uint8").transpose(2, 0, 1)
        hu.save_geotiff(path, rgb_arr, transform, scene.crs, nodata=0,
                        band_names=["red 640 nm", "green 550 nm", "blue 460 nm"])
        written.append(path)

    if verbose:
        for p in written:
            print(f"  {p.name}  ({p.stat().st_size / 1e6:.1f} MB)")
        print(f"  {data.shape[0]} bands · {data.shape[1]}×{data.shape[2]} px · "
              f"{wl.min():.0f}–{wl.max():.0f} nm · int16 × {SCALE}")
    return written


def _parse_envi_header(text):
    """ENVI header → ordered list of (key, value); values may span several lines inside { }."""
    items, lines = [], text.splitlines()
    i = 1 if lines and lines[0].strip().upper() == "ENVI" else 0
    while i < len(lines):
        line = lines[i]
        if "=" not in line:
            i += 1
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if value.startswith("{") and not value.endswith("}"):
            while i + 1 < len(lines) and not value.endswith("}"):
                i += 1
                value += " " + lines[i].strip()
        items.append((key.strip().lower(), value))
        i += 1
    return items


def _patch_envi_header(hdr_path, wl, fwhm, bbl, scene_id):
    """Rewrite the ENVI header so wavelength/FWHM/bad-band metadata is present exactly once.

    GDAL writes a usable header, but we replace the spectral fields with our own values and
    drop its auto-generated description, so the file opens cleanly in the EnMAP-Box.
    """
    replaced = {"description", "wavelength", "wavelength units", "fwhm", "bbl", "band names",
                "reflectance scale factor"}
    kept = [(k, v) for k, v in _parse_envi_header(hdr_path.read_text()) if k not in replaced]
    kept += [
        ("description", "{Planet Tanager surface reflectance x10000 - scene " + scene_id + "}"),
        ("wavelength units", "Nanometers"),
        ("reflectance scale factor", str(SCALE)),
        ("band names", "{" + ", ".join(f"{w:.1f} nm" for w in wl) + "}"),
        ("wavelength", _envi_list(wl)),
        ("fwhm", _envi_list(fwhm)),
        ("bbl", _envi_list(bbl, "{:d}")),
    ]
    out = ["ENVI"] + [f"{k} = {v}" for k, v in kept]
    hdr_path.write_text("\n".join(out) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scene")
    ap.add_argument("--window", nargs=4, type=int, metavar=("R0", "R1", "C0", "C1"))
    ap.add_argument("--format", choices=["envi", "gtiff", "both"], default="both")
    ap.add_argument("--all-bands", action="store_true", help="keep water-vapour and edge bands too")
    ap.add_argument("--out-dir", default=str(hu.DATA_DIR / "qgis"))
    args = ap.parse_args()

    jobs = [(args.scene, tuple(args.window) if args.window else None)] if args.scene else DEFAULT_EXPORTS
    for scene_id, window in jobs:
        print(f"{scene_id} window={window}")
        export(scene_id, window, args.out_dir, args.format, args.all_bands)


if __name__ == "__main__":
    main()
