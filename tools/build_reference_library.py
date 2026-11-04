"""
Build the course reference spectral library from the Tanager course scenes.

Laboratory libraries (USGS splib07, ECOSTRESS) are the gold standard, but they are
large downloads and are measured under lab conditions. For teaching we also want
*image-derived* reference spectra: the median spectrum of a homogeneous area of a known
material, measured by the same sensor we analyse.

Each entry below combines a scene, a WorldCover class filter (pure 30 m pixels only)
and a simple spectral rule. The median spectrum of the selected pixels becomes one
library entry; the 10th and 90th percentiles are stored as well so you can see how
variable the material is.

Run from the course folder:
    python tools/build_reference_library.py
Output:
    data/spectral_library/tanager_reference_library.csv   (median spectra)
    data/spectral_library/tanager_reference_library_p10.csv / _p90.csv
    data/spectral_library/tanager_reference_library.json   (how each entry was built)
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hsi_utils as hu  # noqa: E402

MAX_PIXELS = 400
RNG = np.random.default_rng(42)

# name, scene, WorldCover classes (None = any), rule(ix) -> bool mask, description
# ``ix`` is a dict of simple indices computed on the full scene.
ENTRIES = [
    ("mangrove", "20250223_165546_32_4001", [95], lambda ix: ix["ndvi"] > 0.75,
     "Dense mangrove forest, Jiquilisco Bay, El Salvador"),
    ("tropical_tree_cover", "20250223_165546_32_4001", [10], lambda ix: ix["ndvi"] > 0.75,
     "Tropical tree cover inland of the mangroves, El Salvador"),
    ("sugarcane_cropland", "20250223_165546_32_4001", [40], lambda ix: ix["ndvi"] > 0.6,
     "Green cropland (mostly sugar cane), El Salvador"),
    ("turbid_estuary_water", "20250223_165546_32_4001", [80],
     lambda ix: (ix["ndwi"] > 0.2) & (ix["red"] > np.nanpercentile(ix["red"][ix["water"]], 75)),
     "Sediment-rich estuary water, El Salvador"),
    ("sand_beach", "20250223_165546_32_4001", [60, 30],
     lambda ix: (ix["ndvi"] < 0.15) & (ix["ndwi"] < 0) & (ix["albedo"] > 0.2),
     "Bright sand beach / barrier island, El Salvador"),
    ("irrigated_crop", "20250608_091605_90_4001", [40], lambda ix: ix["ndvi"] > 0.7,
     "Irrigated, fully green crop field, Konya plain, Türkiye"),
    ("dry_bare_soil", "20250608_091605_90_4001", [40, 60],
     lambda ix: (ix["ndvi"] < 0.12) & (ix["albedo"] > np.nanpercentile(ix["albedo"], 50)),
     "Bare, dry agricultural soil, Konya plain"),
    ("dry_steppe_grassland", "20250608_091605_90_4001", [30],
     lambda ix: (ix["ndvi"] > 0.12) & (ix["ndvi"] < 0.25),
     "Senescent steppe grassland, Konya"),
    ("dense_urban", "20250407_035509_25_4001", [50],
     lambda ix: (ix["ndvi"] < 0.15) & (ix["ndwi"] < 0),
     "Dense built-up area, Ho Chi Minh City"),
    ("bright_industrial_roof", "20250407_035509_25_4001", [50],
     lambda ix: (ix["ndvi"] < 0.1) & (ix["albedo"] > np.nanpercentile(ix["albedo"][ix["land"]], 99)),
     "Bright industrial roofs (warehouses), Ho Chi Minh City"),
    ("river_water", "20250407_035509_25_4001", [80], lambda ix: ix["ndwi"] > 0.1,
     "Saigon / Dong Nai river water, Ho Chi Minh City"),
    ("chaparral_unburned", "20241215_185916_33_4001", [20, 10], lambda ix: ix["nbr"] > 0.3,
     "Unburned chaparral / shrubland, Santa Monica Mountains"),
    ("burn_scar", "20241215_185916_33_4001", [20, 10, 30], lambda ix: ix["nbr"] < -0.15,
     "Fresh burn scar of the Franklin fire (Dec 2024), Malibu"),
    ("clear_ocean", "20241215_185916_33_4001", [80],
     lambda ix: (ix["ndwi"] > 0.3) & (ix["nir"] < 0.01),
     "Clear open ocean, Santa Monica Bay"),
    ("coal_mine_surface", "20250219_053251_31_4001", [60],
     lambda ix: (ix["albedo"] < np.nanpercentile(ix["albedo"][ix["land"]], 10)) & (ix["ndwi"] < 0),
     "Dark open-cast coal mine surface, Korba coalfield, India"),
    ("mine_spoil_bright", "20250219_053251_31_4001", [60],
     lambda ix: ix["albedo"] > np.nanpercentile(ix["albedo"][ix["land"]], 90),
     "Bright overburden / spoil heaps, Korba coalfield"),
    ("sabkha_salt_flat", "20250511_074311_00_4001", [60],
     lambda ix: ix["albedo"] > np.nanpercentile(ix["albedo"][ix["land"]], 75),
     "Bright coastal sabkha (salt flat), Al Dhafra, UAE"),
    ("desert_sand", "20250511_074311_00_4001", [60],
     lambda ix: (ix["albedo"] > np.nanpercentile(ix["albedo"][ix["land"]], 20))
     & (ix["albedo"] < np.nanpercentile(ix["albedo"][ix["land"]], 50)),
     "Desert sand / gravel plain, Al Dhafra, UAE"),
    ("shallow_coastal_water", "20250511_074311_00_4001", [80],
     lambda ix: (ix["ndwi"] > 0) & (ix["green"] > np.nanpercentile(ix["green"][ix["water"]], 80)),
     "Shallow, bright-bottomed coastal water, Arabian Gulf"),
]


def scene_indices(scene):
    """A few simple indices for the whole scene (cloud mask off: it flags bright sabkha)."""
    valid = scene.valid_mask(cloud=False)
    b = {k: scene.read_band(w, cloud=False) for k, w in
         dict(blue=480, green=560, red=665, nir=860, swir1=1650, swir2=2200).items()}
    ix = dict(b)
    ix["ndvi"] = hu.nd(b["nir"], b["red"])
    ix["ndwi"] = hu.nd(b["green"], b["nir"])
    ix["nbr"] = hu.nd(b["nir"], b["swir2"])
    ix["albedo"] = np.nanmean(np.stack([b["blue"], b["green"], b["red"], b["nir"], b["swir1"]]), axis=0)
    ix["water"] = valid & (ix["ndwi"] > 0.1)
    ix["land"] = valid & (ix["ndwi"] <= 0)
    ix["valid"] = valid
    return ix


def main():
    out_dir = hu.LIBRARY_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    med, p10, p90, meta = {}, {}, {}, []
    wl_ref = None
    cache = {}
    for name, sid, classes, rule, desc in ENTRIES:
        scene = hu.get_scene(sid, download_if_missing=False)
        if sid not in cache:
            cache[sid] = scene_indices(scene)
        ix = cache[sid]
        lab, pur = hu.load_labels(sid)
        sel = ix["valid"] & (pur == 9) & rule(ix)
        if classes is not None:
            sel &= np.isin(lab, classes)
        rows, cols = np.nonzero(sel)
        if len(rows) < 20:
            print(f"!! {name}: only {len(rows)} pixels, skipped")
            continue
        pick = RNG.choice(len(rows), size=min(MAX_PIXELS, len(rows)), replace=False)
        rows, cols = rows[pick], cols[pick]
        # read spectra pixel by pixel from a bounding window (cheap for a few hundred pixels)
        r0, r1, c0, c1 = rows.min(), rows.max() + 1, cols.min(), cols.max() + 1
        cube, wl = scene.read_cube((r0, r1, c0, c1), bands="all", mask=False)
        spectra = cube[:, rows - r0, cols - c0].T  # (n, bands)
        wl_ref = wl if wl_ref is None else wl_ref
        # all scenes share the nominal band set but centre wavelengths differ slightly: resample
        if not np.allclose(wl, wl_ref, atol=0.01):
            spectra = np.array([np.interp(wl_ref, wl, s) for s in spectra])
        spectra[:, ~hu.good_band_mask(wl_ref)] = np.nan
        med[name] = np.nanmedian(spectra, axis=0)
        p10[name] = np.nanpercentile(spectra, 10, axis=0)
        p90[name] = np.nanpercentile(spectra, 90, axis=0)
        lon, lat = scene.rowcol_to_lonlat(int(np.median(rows)), int(np.median(cols)))
        meta.append(dict(name=name, scene_id=sid, place=scene.info.get("place"), description=desc,
                         worldcover_classes=classes, n_pixels_available=int(sel.sum()),
                         n_pixels_used=int(len(rows)), median_lon=round(float(lon[0]), 5),
                         median_lat=round(float(lat[0]), 5)))
        print(f"{name:24s} {sel.sum():7d} px available, {len(rows)} used")

    for tag, d in (("", med), ("_p10", p10), ("_p90", p90)):
        df = pd.DataFrame({"wavelength_nm": np.round(wl_ref, 2)})
        for k, v in d.items():
            df[k] = np.round(v, 5)
        df.to_csv(out_dir / f"tanager_reference_library{tag}.csv", index=False)
    (out_dir / "tanager_reference_library.json").write_text(json.dumps(
        {"source": hu.attribution(), "labels": "ESA WorldCover 2021 v200 (CC-BY 4.0) purity = 9/9",
         "entries": meta}, indent=2))
    print("Saved library to", out_dir)


if __name__ == "__main__":
    main()
