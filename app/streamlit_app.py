"""
streamlit_app.py — a small viewer for the products written by notebook 31.

Run it from the course folder:

    streamlit run app/streamlit_app.py

It reads the runs in ``outputs/31/`` (each run = one folder with mangrove.tif, quicklook.png,
metadata.json and report.html) and lets a non-technical user browse results, inspect a pixel
and download the GeoTIFF. It is deliberately simple: the point is that the product, not the
notebook, is what reaches the user.
"""
import json
import sys
from pathlib import Path

import numpy as np
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hsi_utils as hu  # noqa: E402

RUNS_DIR = hu.OUTPUT_DIR / "31"

st.set_page_config(page_title="Mangrove extent viewer", page_icon="🌿", layout="wide")
st.title("🌿 Mangrove extent viewer")
st.caption("Space Academy 2026 · hyperspectral course · example product from notebook 31")


@st.cache_data(show_spinner=False)
def list_runs(runs_dir: str):
    p = Path(runs_dir)
    return sorted([d for d in p.glob("*/") if (d / "metadata.json").exists()], reverse=True) if p.exists() else []


@st.cache_data(show_spinner=False)
def load_product(run_dir: str):
    """Read one run: metadata, mangrove mask and probability."""
    import rasterio
    run = Path(run_dir)
    meta = json.loads((run / "metadata.json").read_text())
    with rasterio.open(run / "mangrove.tif") as src:
        mask = src.read(1).astype(bool)
        proba = src.read(2).astype("float32") / 100.0
        bounds = src.bounds
    return meta, mask, proba, tuple(bounds)


runs = list_runs(str(RUNS_DIR))
if not runs:
    st.warning(f"No product runs found in `{RUNS_DIR}`. Run notebook 31 (or "
               "`python app/mangrove_product.py --scene 20250223_165546_32_4001`) first.")
    st.stop()

run_dir = st.sidebar.selectbox("Product run", runs, format_func=lambda p: Path(p).name)
meta, mask, proba, bounds = load_product(str(run_dir))
threshold = st.sidebar.slider("Probability threshold", 0.05, 0.95, float(meta["model"]["threshold"]), 0.05)
show = st.sidebar.radio("Layer", ["Quicklook", "Mangrove mask", "Probability"])

shown_mask = proba >= threshold
area_ha = float(shown_mask.sum()) * (meta["pixel_size_m"] ** 2) / 1e4

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mangrove area", f"{area_ha:,.0f} ha", f"{area_ha - meta['results']['mangrove_area_ha']:+,.0f} vs product")
c2.metric("Usable pixels", f"{meta['results']['valid_pixel_fraction'] * 100:.0f} %")
c3.metric("Pixel size", f"{meta['pixel_size_m']:.0f} m")
c4.metric("Runtime", f"{meta['runtime_seconds']} s")

flags = meta["quality_flags"]
(st.success if flags == ["OK"] else st.warning)("Quality flags: " + ", ".join(flags))

left, right = st.columns([3, 2])
with left:
    if show == "Quicklook":
        st.image(str(Path(run_dir) / "quicklook.png"), use_container_width=True)
    elif show == "Mangrove mask":
        st.image(np.where(shown_mask, 1.0, 0.15), clamp=True, use_container_width=True,
                 caption=f"Mangrove mask at threshold {threshold:.2f}")
    else:
        import matplotlib.cm as cm
        st.image(cm.viridis(np.nan_to_num(proba))[..., :3], use_container_width=True,
                 caption="Mangrove probability")

with right:
    st.subheader("Where")
    w, s, e, n = meta["bbox_lonlat"]
    st.map({"lat": [(s + n) / 2], "lon": [(w + e) / 2]}, zoom=8)
    st.subheader("Pixel inspector")
    row = st.number_input("row", 0, mask.shape[0] - 1, mask.shape[0] // 2)
    col = st.number_input("column", 0, mask.shape[1] - 1, mask.shape[1] // 2)
    st.write(f"probability **{proba[row, col]:.2f}** → "
             f"{'mangrove' if proba[row, col] >= threshold else 'not mangrove'}")
    if st.checkbox("Show the pixel's spectrum (needs the scene HDF5)"):
        try:
            scene = hu.get_scene(meta["scene_id"], download_if_missing=False)
            r0, c0 = (meta["window"] or [0, 0, 0, 0])[0], (meta["window"] or [0, 0, 0, 0])[2]
            spec, wl = scene.read_pixel(r0 + int(row), c0 + int(col))
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(5, 2.6))
            hu.plot_spectrum(ax, wl, spec)
            ax.set(xlabel="wavelength (nm)", ylabel="reflectance"); ax.grid(alpha=.3)
            st.pyplot(fig, use_container_width=True)
        except FileNotFoundError:
            st.info("The scene HDF5 is not available locally, so the spectrum cannot be shown.")

with st.expander("Product metadata (provenance)"):
    st.json(meta)

st.download_button("⬇️ Download GeoTIFF", (Path(run_dir) / "mangrove.tif").read_bytes(),
                   file_name=f"{meta['run_id']}_mangrove.tif", mime="image/tiff")
st.caption(meta["attribution"])
