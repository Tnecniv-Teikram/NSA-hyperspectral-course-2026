"""
Cut small, shareable subsets out of full Tanager scenes.

A full Tanager ortho surface-reflectance HDF5 is ~1 GB. For online sessions and
exercises a 256 × 256 pixel window (7.7 × 7.7 km) is usually enough and is ~30 MB
(int16 reflectance × 10 000, gzip). ``hsi_utils.TanagerScene`` reads a subset exactly
like a full scene, and ``hsi_utils.get_scene()`` picks up ``<scene_id>_subset.h5``
automatically when the full file is not present.

Usage (from the course folder):
    python tools/make_subsets.py                       # default course windows
    python tools/make_subsets.py 20250608_091605_90_4001 200 456 300 556
    python tools/make_subsets.py --uncertainty ...     # also keep the uncertainty cube (2× size)

Output: data/subsets/<scene_id>_subset.h5
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hsi_utils as hu  # noqa: E402

# (row_start, row_stop, col_start, col_stop) — windows with a good mix of cover types
DEFAULT_WINDOWS = {
    "20241215_185916_33_4001": (100, 356, 250, 506),   # Malibu: Franklin burn scar + chaparral + coast
    "20250219_053251_31_4001": (480, 736, 250, 506),   # Korba: Kusmunda / Gevra coal mines
    "20250223_165546_32_4001": (250, 506, 250, 506),   # El Salvador: mangroves + estuary
    "20250407_035509_25_4001": (300, 556, 150, 406),   # Ho Chi Minh City: urban + industry + river
    "20250511_074311_00_4001": (350, 606, 450, 706),   # Al Dhafra: shallow water + sabkha
    "20250608_091605_90_4001": (200, 456, 300, 556),   # Konya: irrigated fields + bare soil
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scene_id", nargs="?")
    ap.add_argument("window", nargs="*", type=int, help="row_start row_stop col_start col_stop")
    ap.add_argument("--uncertainty", action="store_true", help="also store surface_reflectance_uncertainty")
    ap.add_argument("--out-dir", default=str(hu.DATA_DIR / "subsets"))
    args = ap.parse_args()

    if args.scene_id:
        if len(args.window) != 4:
            ap.error("give a window as: row_start row_stop col_start col_stop")
        jobs = {args.scene_id: tuple(args.window)}
    else:
        jobs = DEFAULT_WINDOWS

    out_dir = Path(args.out_dir)
    for sid, win in jobs.items():
        path = hu.find_local(sid)
        if path is None or path.name.endswith("_subset.h5"):
            print(f"skip {sid}: full scene not found locally (download it with hu.get_scene first)")
            continue
        with hu.TanagerScene(path) as scene:
            out = hu.write_subset(scene, out_dir / f"{sid}_subset.h5", win, include_uncertainty=args.uncertainty)
        print(f"{sid}  window={win}  →  {out}  ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
