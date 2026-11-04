"""
hsi_utils.py — shared helpers for the Space Academy 2026 hyperspectral course.

Every course notebook repeats the same handful of steps: find a Tanager scene,
download it, read a few bands, mask bad pixels, drop bad bands, plot spectra and
export results. This module collects those steps in one place so the notebooks
can focus on the science.

Quick start
-----------
>>> import hsi_utils as hu
>>> scene = hu.get_scene("20250608_091605_90_4001")        # finds or downloads the HDF5
>>> cube, wl = scene.read_cube(window=(200, 400, 300, 500))  # (bands, rows, cols), nm
>>> ndvi = hu.nd(scene.read_band(860), scene.read_band(665))

Conventions used throughout the course
--------------------------------------
* Cubes are numpy arrays shaped ``(bands, rows, cols)`` in float32 reflectance (0–1).
* Invalid pixels (no-data, cloud, cirrus, fill values) are set to ``NaN``.
* A *window* is a tuple ``(row_start, row_stop, col_start, col_stop)`` in pixel units.
* Wavelengths are always in nanometres.

Tanager data: CC-BY-4.0 © Planet Labs PBC.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

import h5py
import numpy as np

# --------------------------------------------------------------------------------------
# Paths and catalogue
# --------------------------------------------------------------------------------------
COURSE_DIR = Path(__file__).resolve().parent
DATA_DIR = COURSE_DIR / "data"
LABEL_DIR = DATA_DIR / "labels"
LIBRARY_DIR = DATA_DIR / "spectral_library"
OUTPUT_DIR = COURSE_DIR / "outputs"

STAC_ROOT = "https://www.planet.com/data/stac/tanager-core-imagery"
COLLECTIONS = [
    "agriculture", "coastal-water-bodies", "energy-mining", "fire", "GHG-plumes",
    "natural-lands", "snow-ice", "urban", "ROCX2025",
]

H5_ROOT = "HDFEOS/GRIDS/HYP/Data Fields"

# Scenes used in the course notebooks. The theme notebooks (00–06) already use the first six.
SCENES = {
    "20241215_185916_33_4001": dict(collection="fire", place="Malibu, California, USA",
                                    theme="Wildfire — Franklin fire burn scar (Dec 2024)"),
    "20250123_185518_92_4001": dict(collection="fire", place="Santa Monica Mountains, California, USA",
                                    theme="Wildfire — after the Palisades fire (Jan 2025)"),
    "20250219_053251_31_4001": dict(collection="GHG-plumes", place="Korba, Chhattisgarh, India",
                                    theme="Coal mining, power plants, GHG"),
    "20250223_165546_32_4001": dict(collection="coastal-water-bodies", place="Usulután, El Salvador",
                                    theme="Mangroves, estuary, coast, sugar cane"),
    "20250407_035509_25_4001": dict(collection="urban", place="Ho Chi Minh City, Vietnam",
                                    theme="Urban fabric, industry, river, vegetation"),
    "20250511_074311_00_4001": dict(collection="coastal-water-bodies", place="Al Dhafra coast, UAE",
                                    theme="Shallow coastal water, sabkha, salt ponds"),
    "20250608_091605_90_4001": dict(collection="agriculture", place="Konya, Türkiye",
                                    theme="Irrigated agriculture, dry steppe"),
}


def data_dirs() -> list[Path]:
    """Folders searched (in order) for Tanager HDF5 files.

    1. ``$TANAGER_DATA_DIR`` (one or more folders separated by ``os.pathsep``)
    2. ``<course>/data``
    3. ``<course>/../notebooks`` (where the theme notebooks store their downloads)
    4. the current working directory
    """
    dirs = []
    env = os.environ.get("TANAGER_DATA_DIR")
    if env:
        dirs += [Path(p) for p in env.split(os.pathsep) if p]
    dirs += [DATA_DIR, DATA_DIR / "subsets"]
    # Sibling folders that hold the Tanager scenes. The starter-notebook folder has been called
    # both "notebooks" and "Starting_notebooks", so also pick up any sibling that actually
    # contains scene files — renaming the folder should not break every notebook.
    parent = COURSE_DIR.parent
    dirs += [parent / "notebooks", parent / "Starting_notebooks"]
    if parent.is_dir():
        dirs += sorted(d for d in parent.iterdir()
                       if d.is_dir() and any(d.glob("*_ortho_sr_hdf5.h5")))
    dirs.append(Path.cwd())
    seen, out = set(), []
    for d in dirs:
        d = d.resolve()
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def download_dir() -> Path:
    """Where new downloads go: the first ``$TANAGER_DATA_DIR`` entry, else ``<course>/data``."""
    env = os.environ.get("TANAGER_DATA_DIR")
    d = Path(env.split(os.pathsep)[0]) if env else DATA_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def find_local(scene_id: str, product: str = "ortho_sr_hdf5", allow_subset: bool = True) -> Path | None:
    """Return the path of a locally available HDF5 for ``scene_id``, or ``None``.

    Full scenes are preferred. A subset made with ``tools/make_subsets.py``
    (``data/subsets/<scene_id>_subset.h5``) is only returned when no full scene exists —
    note that its pixel coordinates start at (0, 0) of the subset window.
    """
    for d in data_dirs():
        p = d / f"{scene_id}_{product}.h5"
        if p.exists():
            return p
    if allow_subset:
        for d in data_dirs() + [DATA_DIR / "subsets"]:
            p = d / f"{scene_id}_subset.h5"
            if p.exists():
                return p
    return None


# --------------------------------------------------------------------------------------
# STAC access
# --------------------------------------------------------------------------------------
def _get_json(url: str, timeout: int = 60) -> dict:
    import requests
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


def fetch_item(scene_id: str, collection: str | None = None) -> dict:
    """Fetch the STAC item (as a dict) for a Tanager scene.

    If ``collection`` is not given we look it up in ``SCENES`` and otherwise try every
    collection in the static catalogue until the item is found.
    """
    candidates = [collection] if collection else []
    if not candidates and scene_id in SCENES:
        candidates = [SCENES[scene_id]["collection"]]
    candidates += [c for c in COLLECTIONS if c not in candidates]
    last_err = None
    for col in candidates:
        url = f"{STAC_ROOT}/{col}/{scene_id}/{scene_id}.json"
        try:
            return _get_json(url)
        except Exception as err:  # noqa: BLE001 — try the next collection
            last_err = err
    raise FileNotFoundError(f"Scene {scene_id} not found in any collection ({last_err})")


def download(url: str, dest: Path | str, chunk_mb: int = 1, verbose: bool = True) -> Path:
    """Stream ``url`` to ``dest`` (skips the download if the file already exists)."""
    import requests
    dest = Path(dest)
    if dest.exists():
        if verbose:
            print(f"Already downloaded: {dest}")
        return dest
    tmp = dest.with_suffix(dest.suffix + ".part")
    if verbose:
        print(f"Downloading {url}\n  → {dest}  (Tanager HDF5 files are ~1 GB, be patient)")
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        done, next_report = 0, 0.0
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_mb * 1024 * 1024):
                f.write(chunk)
                done += len(chunk)
                if verbose and total and done / total >= next_report:
                    print(f"  {done / 1e6:8.0f} / {total / 1e6:.0f} MB")
                    next_report += 0.1
    tmp.rename(dest)
    return dest


CATALOG_INDEX = DATA_DIR / "tanager_catalog_index.geojson"


def build_catalog_index(out_path=None, collections=None, max_workers: int = 8, verbose: bool = True):
    """Crawl the static Tanager STAC catalogue and save one GeoJSON feature per scene.

    Planet publishes Tanager open data as a *static* catalogue (JSON files, no search API),
    so to search by area or date we first build our own index. Takes 1–3 minutes.
    """
    from concurrent.futures import ThreadPoolExecutor
    out_path = Path(out_path) if out_path else CATALOG_INDEX
    collections = collections or COLLECTIONS
    links = []
    for col in collections:
        cj = _get_json(f"{STAC_ROOT}/{col}/collection.json")
        links += [(col, l["href"]) for l in cj["links"] if l.get("rel") == "item"]
    if verbose:
        print(f"{len(links)} items in {len(collections)} collections — fetching metadata…")

    def _feature(arg):
        col, href = arg
        it = _get_json(href)
        p = it.get("properties", {})
        a = it.get("assets", {})
        return {"type": "Feature", "geometry": it.get("geometry"), "properties": {
            "id": it["id"], "collection": col, "datetime": p.get("datetime"),
            "location": p.get("location_description"), "cloud_percent": p.get("cloud_percent"),
            "light_haze_percent": p.get("light_haze_percent"), "off_nadir": p.get("view:off_nadir"),
            "sun_elevation": p.get("view:sun_elevation"), "gsd": p.get("gsd"),
            "item_url": href, "sr_url": a.get("ortho_sr_hdf5", {}).get("href"),
            "thumbnail": a.get("thumbnail", {}).get("href"), "visual": a.get("ortho_visual", {}).get("href"),
        }}

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        feats = list(ex.map(_feature, links))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"type": "FeatureCollection", "features": feats}))
    if verbose:
        print(f"Saved {len(feats)} scenes to {out_path}")
    return out_path


def load_catalog_index(refresh: bool = False):
    """The Tanager scene index as a GeoDataFrame (builds it first if missing)."""
    import geopandas as gpd
    if refresh or not CATALOG_INDEX.exists():
        build_catalog_index()
    gdf = gpd.read_file(CATALOG_INDEX)
    gdf["datetime"] = gdf["datetime"].astype("datetime64[ns, UTC]")
    return gdf.sort_values("datetime").reset_index(drop=True)


def get_scene_path(scene_id: str, product: str = "ortho_sr_hdf5", download_if_missing: bool = True,
                   collection: str | None = None) -> Path:
    """Local path of a scene HDF5, downloading it from the Planet STAC catalogue if needed."""
    p = find_local(scene_id, product)
    if p is not None:
        return p
    if not download_if_missing:
        raise FileNotFoundError(f"{scene_id} not found in {[str(d) for d in data_dirs()]}")
    item = fetch_item(scene_id, collection)
    url = item["assets"][product]["href"]
    return download(url, download_dir() / f"{scene_id}_{product}.h5")


def get_scene(scene_id: str, **kwargs) -> "TanagerScene":
    """Open a Tanager scene by ID (finds a local copy or downloads it)."""
    return TanagerScene(get_scene_path(scene_id, **kwargs))


# --------------------------------------------------------------------------------------
# Band helpers
# --------------------------------------------------------------------------------------
WATER_VAPOUR_NM = ((1340.0, 1445.0), (1790.0, 1970.0))
SWIR_EDGE_NM = 2450.0
MIN_WL_NM = 400.0  # below ~400 nm Tanager's median SNR drops under 10 (see notebook 11)


def good_band_mask(wavelengths, file_flags=None, swir_edge: float = SWIR_EDGE_NM,
                   min_wl: float = MIN_WL_NM, extra_bad=()) -> np.ndarray:
    """Boolean mask of bands worth keeping.

    Removes the two atmospheric water-vapour windows, the low-SNR bands below ``min_wl``,
    the noisy detector edge beyond ``swir_edge`` nm and any ``extra_bad`` (start, stop)
    ranges. If the per-band ``good_wavelengths`` flags from the HDF5 file are passed,
    those are honoured too.
    """
    wl = np.asarray(wavelengths, dtype=float)
    keep = (wl <= swir_edge) & (wl >= min_wl)
    for lo, hi in tuple(WATER_VAPOUR_NM) + tuple(extra_bad):
        keep &= ~((wl >= lo) & (wl <= hi))
    if file_flags is not None:
        keep &= np.asarray(file_flags).astype(bool)
    return keep


def band_index(wavelengths, target_nm: float) -> int:
    """Index of the band whose centre is closest to ``target_nm``."""
    return int(np.argmin(np.abs(np.asarray(wavelengths) - target_nm)))


def nd(a, b, eps: float = 1e-6):
    """Normalised difference (a − b) / (a + b)."""
    return (a - b) / (a + b + eps)


# --------------------------------------------------------------------------------------
# The scene reader
# --------------------------------------------------------------------------------------
class TanagerScene:
    """Lightweight reader for Tanager ortho surface-reflectance HDF5 files.

    Nothing is loaded into memory until you ask for it, so you can open a 1 GB file and
    read just one band, one pixel or one small window.
    """

    def __init__(self, path):
        self.path = Path(path)
        self.scene_id = self.path.name[:23]
        self.info = SCENES.get(self.scene_id, {})
        self._f = h5py.File(self.path, "r")
        grp = self._f["HDFEOS/GRIDS/HYP"]
        self._fields = grp["Data Fields"]
        sr = self._fields["surface_reflectance"]
        self.wavelengths = np.asarray(sr.attrs["wavelengths"], dtype=float)
        self.fwhm = np.asarray(sr.attrs["fwhm"], dtype=float)
        self.file_good_flags = np.asarray(sr.attrs.get("good_wavelengths", np.ones(sr.shape[0])), bool)
        self.good_bands = good_band_mask(self.wavelengths, self.file_good_flags)
        self.shape = sr.shape  # (bands, rows, cols)
        self._scale = float(sr.attrs.get("scale_factor", 1.0))
        self._fill = float(np.asarray(sr.attrs.get("_FillValue", -9999.0)).ravel()[0])
        self.epsg = int(grp.attrs["epsg_code"])
        self.crs = f"EPSG:{self.epsg}"
        self._parse_grid()

    # ---- georeferencing -------------------------------------------------------------
    def _parse_grid(self):
        sm = self._f["HDFEOS INFORMATION/StructMetadata.0"][()]
        sm = sm.decode() if isinstance(sm, bytes) else str(sm)
        ul = re.search(r"UpperLeftPointMtrs=\(([-\d.]+),([-\d.]+)\)", sm).groups()
        lr = re.search(r"LowerRightMtrs=\(([-\d.]+),([-\d.]+)\)", sm).groups()
        self.ul_x, self.ul_y = float(ul[0]), float(ul[1])
        lr_x, lr_y = float(lr[0]), float(lr[1])
        self.res_x = (lr_x - self.ul_x) / self.shape[2]
        self.res_y = (self.ul_y - lr_y) / self.shape[1]
        self.bounds = (self.ul_x, lr_y, lr_x, self.ul_y)  # (left, bottom, right, top)

    def transform(self, window=None, stride: int = 1):
        """Affine geotransform (rasterio style) for the full grid or a window."""
        from affine import Affine
        r0, _, c0, _ = self._window(window)
        return Affine(self.res_x * stride, 0.0, self.ul_x + c0 * self.res_x,
                      0.0, -self.res_y * stride, self.ul_y - r0 * self.res_y)

    def xy(self, row, col):
        """Map coordinates (scene CRS, pixel centre) of a pixel."""
        return (self.ul_x + (np.asarray(col) + 0.5) * self.res_x,
                self.ul_y - (np.asarray(row) + 0.5) * self.res_y)

    def rowcol_to_lonlat(self, row, col):
        from rasterio.warp import transform as warp
        x, y = self.xy(row, col)
        lon, lat = warp(self.crs, "EPSG:4326", np.atleast_1d(x).tolist(), np.atleast_1d(y).tolist())
        return np.array(lon), np.array(lat)

    def lonlat_to_rowcol(self, lon, lat):
        from rasterio.warp import transform as warp
        x, y = warp("EPSG:4326", self.crs, np.atleast_1d(lon).tolist(), np.atleast_1d(lat).tolist())
        col = ((np.array(x) - self.ul_x) / self.res_x).astype(int)
        row = ((self.ul_y - np.array(y)) / self.res_y).astype(int)
        return row, col

    def bounds_lonlat(self):
        """(west, south, east, north) of the grid in degrees."""
        from rasterio.warp import transform_bounds
        return transform_bounds(self.crs, "EPSG:4326", *self.bounds)

    # ---- low level ------------------------------------------------------------------
    def _window(self, window):
        if window is None:
            return 0, self.shape[1], 0, self.shape[2]
        r0, r1, c0, c1 = window
        return max(0, r0), min(self.shape[1], r1), max(0, c0), min(self.shape[2], c1)

    def read_field(self, name: str, window=None, stride: int = 1) -> np.ndarray:
        """Read a 2-D auxiliary field, e.g. ``'column_water_vapour'`` or ``'sun_zenith'``."""
        r0, r1, c0, c1 = self._window(window)
        ds = self._fields[name]
        arr = ds[r0:r1:stride, c0:c1:stride]
        fill = ds.attrs.get("_FillValue", None)
        if fill is not None and arr.dtype.kind == "f":
            arr = np.where(arr == np.asarray(fill).ravel()[0], np.nan, arr)
        return arr

    @property
    def field_names(self):
        return list(self._fields.keys())

    # ---- masks ----------------------------------------------------------------------
    def masks(self, window=None, stride: int = 1) -> dict:
        """Boolean masks (True = flagged) for no-data, cloud and cirrus."""
        out = {}
        for key, name in (("nodata", "nodata_pixels"), ("cloud", "beta_cloud_mask"),
                          ("cirrus", "beta_cirrus_mask")):
            if name in self._fields:
                m = self.read_field(name, window, stride)
                out[key] = (m == 1) | (m == 255)
        return out

    def valid_mask(self, window=None, stride: int = 1, cloud: bool = True, cirrus: bool = True):
        """True where a pixel is usable (not no-data, and optionally not cloud/cirrus)."""
        m = self.masks(window, stride)
        valid = ~m["nodata"]
        if cloud and "cloud" in m:
            valid &= ~m["cloud"]
        if cirrus and "cirrus" in m:
            valid &= ~m["cirrus"]
        return valid

    # ---- reflectance ----------------------------------------------------------------
    def _clean(self, arr):
        """Raw values → float32 reflectance with fill values as NaN (handles int16 subsets)."""
        bad = arr == self._fill
        arr = arr.astype("float32")
        if self._scale != 1.0:
            arr *= self._scale
        arr[bad] = np.nan
        return arr

    def band_index(self, target_nm: float) -> int:
        return band_index(self.wavelengths, target_nm)

    def read_band(self, target_nm: float, window=None, stride: int = 1, mask: bool = True,
                  cloud: bool = True) -> np.ndarray:
        """Read the band closest to ``target_nm`` as a 2-D float32 array (invalid → NaN)."""
        r0, r1, c0, c1 = self._window(window)
        b = self.band_index(target_nm)
        arr = self._clean(self._fields["surface_reflectance"][b, r0:r1:stride, c0:c1:stride])
        if mask:
            arr[~self.valid_mask(window, stride, cloud=cloud)] = np.nan
        return arr

    def read_cube(self, window=None, bands="good", stride: int = 1, mask: bool = True,
                  cloud: bool = True, dataset: str = "surface_reflectance"):
        """Read a spectral cube.

        Parameters
        ----------
        window : (row_start, row_stop, col_start, col_stop) or None for the whole scene.
        bands  : ``"good"`` (default, bad bands removed), ``"all"``, or an array of band
                 indices / a boolean mask.
        stride : read every n-th row and column (quick previews of the full scene).
        mask   : set no-data / cloud / cirrus pixels to NaN.
        dataset: ``"surface_reflectance"`` or ``"surface_reflectance_uncertainty"``.

        Returns
        -------
        cube : float32 array (bands, rows, cols)
        wl   : wavelengths (nm) of the returned bands
        """
        r0, r1, c0, c1 = self._window(window)
        if isinstance(bands, str):
            sel = self.good_bands if bands == "good" else np.ones(self.shape[0], bool)
        else:
            sel = np.asarray(bands)
            if sel.dtype != bool:
                tmp = np.zeros(self.shape[0], bool)
                tmp[sel] = True
                sel = tmp
        # Reading all bands and subsetting in numpy is faster than h5py fancy indexing.
        raw = self._fields[dataset][:, r0:r1:stride, c0:c1:stride]
        cube = self._clean(raw[sel])
        if mask:
            cube[:, ~self.valid_mask(window, stride, cloud=cloud)] = np.nan
        return cube, self.wavelengths[sel]

    def read_pixel(self, row: int, col: int, bands="good"):
        """Spectrum of a single pixel → (spectrum, wavelengths)."""
        cube, wl = self.read_cube((row, row + 1, col, col + 1), bands=bands, mask=False)
        return cube[:, 0, 0], wl

    def rgb(self, window=None, stride: int = 1, wl=(640, 550, 460), p=(2, 98), mask: bool = True):
        """True-colour (or any 3-band) composite, percentile-stretched to 0–1."""
        bands = [self.read_band(w, window, stride, mask=mask, cloud=False) for w in wl]
        return stretch(np.dstack(bands), p)

    def to_xarray(self, window=None, bands="good", stride: int = 1, mask: bool = True):
        """The cube as an ``xarray.DataArray`` with wavelength/y/x coordinates and a CRS."""
        import xarray as xr
        cube, wl = self.read_cube(window, bands, stride, mask)
        r0, r1, c0, c1 = self._window(window)
        rows = np.arange(r0, r1, stride)
        cols = np.arange(c0, c1, stride)
        x, _ = self.xy(np.zeros_like(cols), cols)
        _, y = self.xy(rows, np.zeros_like(rows))
        da = xr.DataArray(cube, dims=("wavelength", "y", "x"),
                          coords={"wavelength": wl, "y": y, "x": x},
                          name="reflectance", attrs={"scene_id": self.scene_id, "units": "reflectance"})
        try:
            import rioxarray  # noqa: F401 — registers the .rio accessor
            da = da.rio.write_crs(self.crs)
        except ImportError:
            da.attrs["crs"] = self.crs
        return da

    def summary(self) -> str:
        valid = self.valid_mask(stride=4)
        m = self.masks(stride=4)
        lines = [
            f"Scene      : {self.scene_id}  ({self.info.get('place', 'unknown place')})",
            f"File       : {self.path}",
            f"Cube       : {self.shape[0]} bands × {self.shape[1]} rows × {self.shape[2]} cols",
            f"Wavelengths: {self.wavelengths.min():.0f}–{self.wavelengths.max():.0f} nm, "
            f"FWHM {self.fwhm.min():.1f}–{self.fwhm.max():.1f} nm",
            f"Good bands : {self.good_bands.sum()} of {self.shape[0]}",
            f"Grid       : {self.crs}, {self.res_x:.0f} m pixels",
            f"No-data    : {m['nodata'].mean() * 100:.1f}%   cloud flag: {m['cloud'].mean() * 100:.1f}%   "
            f"cirrus flag: {m['cirrus'].mean() * 100:.1f}%   usable: {valid.mean() * 100:.1f}%",
        ]
        return "\n".join(lines)

    def __repr__(self):
        return f"TanagerScene({self.scene_id}, {self.shape[1]}×{self.shape[2]} px, {self.shape[0]} bands)"

    def close(self):
        self._f.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


# --------------------------------------------------------------------------------------
# Array helpers
# --------------------------------------------------------------------------------------
def stretch(img, p=(2, 98)):
    """Percentile stretch to 0–1 (per band for 3-D arrays shaped rows × cols × bands)."""
    img = np.asarray(img, dtype="float32")
    if img.ndim == 2:
        lo, hi = np.nanpercentile(img, p)
        return np.clip((img - lo) / (hi - lo + 1e-12), 0, 1)
    out = np.empty_like(img)
    for i in range(img.shape[-1]):
        out[..., i] = stretch(img[..., i], p)
    return out


def rgb_from_cube(cube, wl, bands=(640, 550, 460), p=(2, 98)):
    """Composite from an in-memory cube (bands, rows, cols). NaN pixels become white."""
    idx = [band_index(wl, b) for b in bands]
    rgb = stretch(np.dstack([cube[i] for i in idx]), p)
    rgb[np.isnan(rgb)] = 1.0
    return rgb


def cube_to_pixels(cube):
    """(bands, rows, cols) → (pixels, bands) matrix of *complete* spectra plus a 2-D mask.

    Pixels with any NaN band are dropped; use ``pixels_to_image`` to put results back.
    """
    b, h, w = cube.shape
    X = cube.reshape(b, -1).T
    ok = np.all(np.isfinite(X), axis=1)
    return X[ok], ok.reshape(h, w)


def pixels_to_image(values, mask, fill=np.nan):
    """Inverse of ``cube_to_pixels``: scatter per-pixel values back onto the 2-D grid."""
    values = np.asarray(values)
    if values.ndim == 1:
        out = np.full(mask.shape, fill, dtype=np.result_type(values.dtype, np.float32))
        out[mask] = values
        return out
    out = np.full((values.shape[1],) + mask.shape, fill, dtype="float32")
    out[:, mask] = values.T
    return out


def plot_spectrum(ax, wl, spectrum, gap_nm: float = 20.0, **kwargs):
    """Plot a spectrum, breaking the line where bands were removed (e.g. water vapour)."""
    wl = np.asarray(wl, float)
    s = np.asarray(spectrum, float)
    breaks = np.where(np.diff(wl) > gap_nm)[0]
    wl_p = np.insert(wl, breaks + 1, (wl[breaks] + wl[breaks + 1]) / 2)
    s_p = np.insert(s, breaks + 1, np.nan)
    return ax.plot(wl_p, s_p, **kwargs)


def shade_bad_regions(ax, color="0.85"):
    """Grey bands over the water-vapour windows and the SWIR edge."""
    for lo, hi in WATER_VAPOUR_NM:
        ax.axvspan(lo, hi, color=color, zorder=0)
    ax.axvspan(SWIR_EDGE_NM, 2510, color=color, zorder=0)


# --------------------------------------------------------------------------------------
# Spectral operations
# --------------------------------------------------------------------------------------
# Sentinel-2A MSI, approximated with Gaussian response functions (centre, FWHM in nm).
# Real spectral response functions are published by ESA; the Gaussian version is close
# enough to show what multispectral sensors "see".
SENTINEL2_BANDS = {
    "B01": (442.7, 21), "B02": (492.4, 66), "B03": (559.8, 36), "B04": (664.6, 31),
    "B05": (704.1, 15), "B06": (740.5, 15), "B07": (782.8, 20), "B08": (832.8, 106),
    "B8A": (864.7, 21), "B09": (945.1, 20), "B11": (1613.7, 91), "B12": (2202.4, 175),
}
# Landsat 8/9 OLI (approximate Gaussian).
LANDSAT8_BANDS = {
    "B1": (443, 16), "B2": (482, 60), "B3": (561, 57), "B4": (655, 37),
    "B5": (865, 28), "B6": (1609, 85), "B7": (2201, 187),
}
# EnMAP: 224 bands, VNIR ~6.5 nm sampling (420–1000 nm) and SWIR ~10 nm (900–2450 nm).
# Nominal grid for teaching; use the band centres from the EnMAP metadata for real work.
ENMAP_APPROX = {
    "centers": np.concatenate([np.linspace(420, 1000, 91), np.linspace(900, 2450, 133)]),
    "fwhm": np.concatenate([np.full(91, 8.0), np.full(133, 10.0)]),
}


def resample_to_sensor(wl, spectra, centers, fwhms):
    """Convolve hyperspectral spectra with Gaussian band responses.

    ``spectra`` may be 1-D (bands,) or 2-D (n_spectra, bands). NaN bands are ignored
    (weights are renormalised over the bands that are available).
    """
    wl = np.asarray(wl, float)
    S = np.atleast_2d(np.asarray(spectra, float))
    centers = np.asarray(centers, float)
    sigma = np.asarray(fwhms, float) / (2 * np.sqrt(2 * np.log(2)))
    W = np.exp(-0.5 * ((wl[None, :] - centers[:, None]) / sigma[:, None]) ** 2)  # (out, in)
    W[W < 1e-4] = 0.0
    finite = np.isfinite(S)
    S0 = np.where(finite, S, 0.0)
    num = S0 @ W.T
    den = finite.astype(float) @ W.T
    out = np.where(den > 0.5 * W.sum(axis=1)[None, :], num / np.maximum(den, 1e-12), np.nan)
    return out[0] if np.ndim(spectra) == 1 else out


def spectral_angle(X, ref):
    """Spectral angle (radians) between each row of ``X`` (n, bands) and ``ref`` (bands,)."""
    X = np.atleast_2d(X)
    ref = np.asarray(ref, float)
    cos = (X @ ref) / (np.linalg.norm(X, axis=1) * np.linalg.norm(ref) + 1e-12)
    return np.arccos(np.clip(cos, -1, 1))


def continuum_removed(wl, spectrum):
    """Divide a spectrum by its upper convex hull (continuum removal).

    Absorption features become dips below 1.0 whose depth is comparable between
    bright and dark materials.
    """
    wl = np.asarray(wl, float)
    s = np.asarray(spectrum, float)
    ok = np.isfinite(s)
    x, y = wl[ok], s[ok]
    hull = [0]
    for i in range(1, len(x)):  # monotone-chain upper hull
        while len(hull) >= 2:
            x1, y1 = x[hull[-2]], y[hull[-2]]
            x2, y2 = x[hull[-1]], y[hull[-1]]
            if (x2 - x1) * (y[i] - y1) - (y2 - y1) * (x[i] - x1) >= 0:
                hull.pop()
            else:
                break
        hull.append(i)
    cont = np.interp(wl, x[hull], y[hull])
    return s / cont


def band_depth(wl, spectrum, left, center, right):
    """Depth of an absorption feature: 1 − R(center) / continuum(center).

    ``left``/``right`` are the shoulder wavelengths; the continuum is the straight
    line between the shoulders. Works on 1-D spectra and on cubes (bands first).
    """
    wl = np.asarray(wl)
    iL, iC, iR = band_index(wl, left), band_index(wl, center), band_index(wl, right)
    rL, rC, rR = spectrum[iL], spectrum[iC], spectrum[iR]
    t = (wl[iC] - wl[iL]) / (wl[iR] - wl[iL])
    cont = rL + t * (rR - rL)
    return 1.0 - rC / (cont + 1e-12)


# --------------------------------------------------------------------------------------
# Export
# --------------------------------------------------------------------------------------
def save_geotiff(path, array, transform, crs, nodata=None, band_names=None, cog: bool = True):
    """Write a 2-D or 3-D (bands, rows, cols) array as a GeoTIFF (Cloud-Optimised by default)."""
    import rasterio
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = np.asarray(array)
    if arr.ndim == 2:
        arr = arr[None]
    if nodata is None:
        nodata = np.nan if arr.dtype.kind == "f" else None
    profile = dict(count=arr.shape[0], height=arr.shape[1], width=arr.shape[2], dtype=arr.dtype,
                   crs=crs, transform=transform, nodata=nodata, compress="deflate")
    if cog:
        profile.update(driver="COG", blocksize=256)
    else:
        profile.update(driver="GTiff", tiled=True)
    try:
        with rasterio.open(path, "w", **profile) as dst:
            dst.write(arr)
            if band_names:
                for i, n in enumerate(band_names, start=1):
                    dst.set_band_description(i, str(n))
    except Exception:
        if not cog:
            raise
        return save_geotiff(path, array, transform, crs, nodata, band_names, cog=False)
    return path


# --------------------------------------------------------------------------------------
# Subsets (small, shareable copies of a scene window)
# --------------------------------------------------------------------------------------
def write_subset(scene: TanagerScene, out_path, window, include_uncertainty: bool = False):
    """Save a window of a scene as a small HDF5 with the same layout as the original.

    Reflectance is stored as int16 × 10 000 (0.0001 precision) with gzip compression, which
    makes a 256 × 256 window roughly 20× smaller than the source file. ``TanagerScene``
    reads the subset exactly like a full scene.
    """
    r0, r1, c0, c1 = scene._window(window)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    src = scene._fields
    with h5py.File(out_path, "w") as f:
        grp = f.create_group("HDFEOS/GRIDS/HYP")
        for k, v in scene._f["HDFEOS/GRIDS/HYP"].attrs.items():
            grp.attrs[k] = v
        grp.attrs["subset_of"] = scene.path.name
        grp.attrs["subset_window"] = np.array([r0, r1, c0, c1])
        fields = grp.create_group("Data Fields")
        names = ["surface_reflectance"] + (["surface_reflectance_uncertainty"] if include_uncertainty else [])
        for name in names:
            data = src[name][:, r0:r1, c0:c1]
            fill = data == scene._fill
            scaled = np.clip(np.round(data * 10000), -32767, 32767).astype("int16")
            scaled[fill] = -32768
            chunks = tuple(min(c, n) for c, n in zip((16, 64, 64), scaled.shape))
            ds = fields.create_dataset(name, data=scaled, chunks=chunks, compression="gzip",
                                       compression_opts=6, shuffle=True)
            for k, v in src[name].attrs.items():
                if k != "_FillValue":
                    ds.attrs[k] = v
            ds.attrs["scale_factor"] = 1e-4
            ds.attrs["_FillValue"] = np.int16(-32768)
        for name in src:
            if src[name].ndim == 2:
                ds = fields.create_dataset(name, data=src[name][r0:r1, c0:c1], compression="gzip")
                for k, v in src[name].attrs.items():
                    ds.attrs[k] = v
        ulx = scene.ul_x + c0 * scene.res_x
        uly = scene.ul_y - r0 * scene.res_y
        lrx = ulx + (c1 - c0) * scene.res_x
        lry = uly - (r1 - r0) * scene.res_y
        sm = (f"GROUP=GridStructure\n\tGROUP=GRID_1\n\t\tGridName=\"HYP\"\n\t\tXDim={c1 - c0}\n"
              f"\t\tYDim={r1 - r0}\n\t\tUpperLeftPointMtrs=({ulx:.2f},{uly:.2f})\n"
              f"\t\tLowerRightMtrs=({lrx:.2f},{lry:.2f})\n\tEND_GROUP=GRID_1\nEND_GROUP=GridStructure\n")
        f.create_dataset("HDFEOS INFORMATION/StructMetadata.0", data=np.bytes_(sm))
    return out_path


# --------------------------------------------------------------------------------------
# Reference labels (ESA WorldCover) aligned to a Tanager grid
# --------------------------------------------------------------------------------------
WORLDCOVER_CLASSES = {
    10: ("Tree cover", "#006400"), 20: ("Shrubland", "#ffbb22"), 30: ("Grassland", "#ffff4c"),
    40: ("Cropland", "#f096ff"), 50: ("Built-up", "#fa0000"), 60: ("Bare / sparse vegetation", "#b4b4b4"),
    70: ("Snow and ice", "#f0f0f0"), 80: ("Permanent water", "#0064c8"), 90: ("Herbaceous wetland", "#0096a0"),
    95: ("Mangroves", "#00cf75"), 100: ("Moss and lichen", "#fae6a0"),
}


def label_path(scene_id: str) -> Path:
    return LABEL_DIR / f"{scene_id}_worldcover2021_30m.tif"


def make_worldcover_labels(scene: TanagerScene, out_path=None) -> Path:
    """Download ESA WorldCover 2021 (10 m) from Microsoft Planetary Computer and aggregate it
    onto the Tanager 30 m grid.

    The output GeoTIFF has two bands:
      1. majority WorldCover class of the nine 10 m cells inside each 30 m pixel
      2. purity — how many of those nine cells (0–9) agree with the majority class

    Requires internet plus ``pystac-client``, ``planetary-computer`` and ``rasterio``.
    """
    import planetary_computer
    import pystac_client
    import rasterio
    from rasterio.warp import Resampling, reproject

    out_path = Path(out_path) if out_path else label_path(scene.scene_id)
    catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1",
                                        modifier=planetary_computer.sign_inplace)
    items = list(catalog.search(collections=["esa-worldcover"], bbox=scene.bounds_lonlat(),
                                query={"esa_worldcover:product_version": {"eq": "2.0.0"}}).items())
    if not items:
        raise RuntimeError("No WorldCover tiles found for this scene")
    from affine import Affine
    fine_t = Affine(scene.res_x / 3, 0, scene.ul_x, 0, -scene.res_y / 3, scene.ul_y)
    h, w = scene.shape[1] * 3, scene.shape[2] * 3
    fine = np.zeros((h, w), dtype="uint8")
    for it in items:
        with rasterio.open(it.assets["map"].href) as src:
            tmp = np.zeros((h, w), dtype="uint8")
            reproject(rasterio.band(src, 1), tmp, dst_transform=fine_t, dst_crs=scene.crs,
                      resampling=Resampling.nearest, src_nodata=0, dst_nodata=0)
            fine = np.where(fine == 0, tmp, fine)
    blocks = fine.reshape(scene.shape[1], 3, scene.shape[2], 3).transpose(0, 2, 1, 3).reshape(
        scene.shape[1], scene.shape[2], 9)
    classes = np.array(sorted(WORLDCOVER_CLASSES))
    counts = np.stack([(blocks == c).sum(-1) for c in classes], axis=-1)
    majority = classes[np.argmax(counts, axis=-1)].astype("uint8")
    purity = counts.max(-1).astype("uint8")
    majority[purity == 0] = 0
    save_geotiff(out_path, np.stack([majority, purity]), scene.transform(), scene.crs, nodata=0,
                 band_names=["worldcover_class", "purity_of_9"], cog=False)
    return out_path


def load_labels(scene_id: str, window=None, min_purity: int = 0, download_if_missing: bool = False):
    """Load the WorldCover label raster aligned to a scene → (classes, purity).

    Pixels with purity below ``min_purity`` (0–9) are set to 0 (= unlabelled).
    """
    import rasterio
    p = label_path(scene_id)
    if not p.exists():
        if not download_if_missing:
            raise FileNotFoundError(f"{p} not found — run hu.make_worldcover_labels(scene) first")
        make_worldcover_labels(get_scene(scene_id))
    with rasterio.open(p) as src:
        lab, pur = src.read(1), src.read(2)
    if window is not None:
        r0, r1, c0, c1 = window
        lab, pur = lab[r0:r1, c0:c1], pur[r0:r1, c0:c1]
    lab = lab.copy()
    lab[pur < min_purity] = 0
    return lab, pur


def label_cmap(classes=None):
    """Matplotlib colormap, norm and legend handles for WorldCover class codes."""
    from matplotlib.colors import BoundaryNorm, ListedColormap
    from matplotlib.patches import Patch
    codes = sorted(int(c) for c in (classes if classes is not None else WORLDCOVER_CLASSES) if c in WORLDCOVER_CLASSES)
    cmap = ListedColormap([WORLDCOVER_CLASSES[c][1] for c in codes])
    cmap.set_bad("white")
    # One colour bin per class code: bin edges halfway between consecutive codes.
    edges = [codes[0] - 1] + [(a + b) / 2 for a, b in zip(codes[:-1], codes[1:])] + [codes[-1] + 1]
    norm = BoundaryNorm(edges, cmap.N)
    handles = [Patch(color=WORLDCOVER_CLASSES[c][1], label=WORLDCOVER_CLASSES[c][0]) for c in codes]
    return cmap, norm, handles


# --------------------------------------------------------------------------------------
# Spectral library
# --------------------------------------------------------------------------------------
def load_library(path=None):
    """Load the course reference library → (wavelengths, dict name → spectrum, metadata list).

    The library (``data/spectral_library/tanager_reference_library.csv``) holds median
    spectra of homogeneous areas in the course scenes, built by
    ``tools/build_reference_library.py`` (see notebook 10). Removed bands are NaN.
    """
    import pandas as pd
    path = Path(path) if path else LIBRARY_DIR / "tanager_reference_library.csv"
    df = pd.read_csv(path)
    wl = df["wavelength_nm"].to_numpy()
    spectra = {c: df[c].to_numpy() for c in df.columns if c != "wavelength_nm"}
    meta_path = LIBRARY_DIR / "tanager_reference_library.json" if path.name.startswith(
        "tanager_reference_library") else path.with_suffix(".json")
    meta = json.loads(meta_path.read_text()).get("entries", []) if meta_path.exists() else []
    return wl, spectra, meta


def load_usgs_ascii(spectrum_file, wavelength_file):
    """Read one USGS Spectral Library Version 7 (splib07) ASCII spectrum.

    Download the ASCII archive from https://www.usgs.gov/labs/spectroscopy-lab/usgs-spectral-library
    (e.g. ``ASCIIdata_splib07a``). Each spectrum file has a one-line header followed by
    one reflectance value per line; the matching wavelength file (µm) sits in the same
    archive. Deleted channels are stored as −1.23e34 and returned as NaN.
    """
    def _read(p):
        vals = np.loadtxt(p, skiprows=1)
        vals[vals < -1e30] = np.nan
        return vals
    wl_nm = _read(wavelength_file) * 1000.0
    return wl_nm, _read(spectrum_file)


# --------------------------------------------------------------------------------------
# Misc
# --------------------------------------------------------------------------------------
def attribution(scene_id: str | None = None) -> str:
    year = scene_id[:4] if scene_id else "2025"
    return f"Tanager STAC Data, available at www.planet.com/data/stac © {year} Planet Labs PBC. CC-BY-4.0"


def ensure_output_dir(sub: str = "") -> Path:
    d = OUTPUT_DIR / sub if sub else OUTPUT_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d
