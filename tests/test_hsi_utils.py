"""
Tests for hsi_utils — run them with:  pytest tests/ -v

Why a course has tests: a validated map is worth nothing if the code that produced it
silently changes behaviour. These tests are small and fast (no downloads); the ones that
need a real scene skip themselves when no HDF5 file is available locally.

Use this file as a template for testing your own project code.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hsi_utils as hu


# --------------------------------------------------------------------------- pure helpers
def test_nd_basic():
    assert hu.nd(np.float64(3), np.float64(1)) == pytest.approx(0.5, abs=1e-6)
    assert hu.nd(np.float64(1), np.float64(1)) == pytest.approx(0.0, abs=1e-6)


def test_nd_is_safe_for_zero_pixels():
    # water in the SWIR can be 0/0 — must not raise or return inf
    assert np.isfinite(hu.nd(np.float64(0), np.float64(0)))


def test_band_index_picks_nearest():
    wl = np.array([400.0, 500.0, 600.0])
    assert hu.band_index(wl, 505) == 1
    assert hu.band_index(wl, 380) == 0
    assert hu.band_index(wl, 1000) == 2


def test_good_band_mask_drops_the_right_regions():
    wl = np.array([380.0, 500.0, 1400.0, 1600.0, 1900.0, 2200.0, 2480.0])
    keep = hu.good_band_mask(wl)
    assert keep.tolist() == [False, True, False, True, False, True, False]


def test_good_band_mask_honours_file_flags():
    wl = np.array([500.0, 600.0, 700.0])
    keep = hu.good_band_mask(wl, file_flags=np.array([1, 0, 1]))
    assert keep.tolist() == [True, False, True]


def test_stretch_maps_percentiles_into_unit_range():
    img = np.arange(100, dtype="float32").reshape(10, 10)
    out = hu.stretch(img, p=(0, 100))
    assert out.min() == pytest.approx(0.0) and out.max() == pytest.approx(1.0)
    assert np.all((out >= 0) & (out <= 1))


def test_stretch_ignores_nan():
    img = np.full((4, 4), np.nan, dtype="float32")
    img[0, 0], img[1, 1] = 0.0, 1.0
    assert np.isfinite(hu.stretch(img)[1, 1])


# --------------------------------------------------------------------------- cube <-> pixels
def test_cube_pixels_roundtrip_keeps_values_and_positions():
    rng = np.random.default_rng(0)
    cube = rng.random((5, 4, 3)).astype("float32")
    cube[:, 1, 1] = np.nan                       # one incomplete pixel
    X, mask = hu.cube_to_pixels(cube)
    assert X.shape == (11, 5) and mask.sum() == 11 and not mask[1, 1]
    back = hu.pixels_to_image(X, mask)
    assert np.allclose(back[:, mask], cube[:, mask])
    assert np.all(np.isnan(back[:, 1, 1]))


def test_pixels_to_image_handles_1d_values():
    mask = np.array([[True, False], [True, True]])
    out = hu.pixels_to_image(np.array([1.0, 2.0, 3.0]), mask)
    assert out[0, 0] == 1 and np.isnan(out[0, 1]) and out[1, 1] == 3


# --------------------------------------------------------------------------- spectral maths
def test_resample_to_sensor_is_exact_for_a_flat_spectrum():
    wl = np.arange(400.0, 2500.0, 5.0)
    flat = np.full(wl.size, 0.3)
    out = hu.resample_to_sensor(wl, flat, [500.0, 1600.0], [30.0, 90.0])
    assert np.allclose(out, 0.3, atol=1e-6)


def test_resample_to_sensor_averages_over_the_band_width():
    wl = np.arange(400.0, 800.0, 5.0)
    ramp = wl / 1000.0                                  # smooth ramp: mean ≈ value at the centre
    out = hu.resample_to_sensor(wl, ramp, [600.0], [40.0])
    assert out[0] == pytest.approx(0.6, abs=0.01)


def test_resample_to_sensor_returns_nan_where_bands_are_missing():
    wl = np.arange(400.0, 800.0, 5.0)
    spec = np.full(wl.size, 0.2)
    spec[(wl > 580) & (wl < 620)] = np.nan               # a gap under the output band
    assert np.isnan(hu.resample_to_sensor(wl, spec, [600.0], [20.0])[0])


def test_spectral_angle_zero_for_scaled_copies():
    ref = np.array([0.1, 0.4, 0.2, 0.5])
    ang = hu.spectral_angle(np.vstack([ref, 3 * ref, ref[::-1]]), ref)
    assert ang[0] == pytest.approx(0.0, abs=1e-4)
    assert ang[1] == pytest.approx(0.0, abs=1e-4)        # brightness-invariant
    assert ang[2] > 0.1


def test_continuum_removed_is_bounded_and_dips_at_the_absorption():
    wl = np.linspace(2000.0, 2400.0, 81)
    spec = 0.4 - 0.1 * np.exp(-0.5 * ((wl - 2200) / 20) ** 2)   # one Gaussian absorption
    cr = hu.continuum_removed(wl, spec)
    assert np.all(cr <= 1.0 + 1e-6) and cr.min() < 0.8
    assert wl[np.argmin(cr)] == pytest.approx(2200, abs=10)


def test_band_depth_matches_a_known_absorption():
    wl = np.linspace(2000.0, 2400.0, 81)
    spec = 0.4 - 0.1 * np.exp(-0.5 * ((wl - 2200) / 20) ** 2)
    assert hu.band_depth(wl, spec, 2100, 2200, 2300) == pytest.approx(0.25, abs=0.02)


# --------------------------------------------------------------------------- I/O
def test_save_geotiff_roundtrip(tmp_path):
    rasterio = pytest.importorskip("rasterio")
    from affine import Affine
    arr = np.arange(12, dtype="float32").reshape(3, 2, 2)
    path = hu.save_geotiff(tmp_path / "t.tif", arr, Affine(30, 0, 100, 0, -30, 200), "EPSG:32636",
                           band_names=["a", "b", "c"])
    with rasterio.open(path) as src:
        assert src.count == 3 and src.crs.to_string() == "EPSG:32636"
        assert src.descriptions == ("a", "b", "c")
        assert np.allclose(src.read(), arr)
        assert src.transform.a == 30 and src.transform.e == -30


def test_attribution_uses_the_scene_year():
    assert "2025 Planet Labs PBC" in hu.attribution("20250608_091605_90_4001")


# --------------------------------------------------------------------------- real-scene tests
SCENE_ID = "20250608_091605_90_4001"
scene_path = hu.find_local(SCENE_ID)
needs_scene = pytest.mark.skipif(scene_path is None, reason="no local Tanager scene to test against")


@pytest.fixture(scope="module")
def scene():
    with hu.TanagerScene(scene_path) as s:
        yield s


@needs_scene
def test_scene_metadata_is_sane(scene):
    assert scene.shape[0] == len(scene.wavelengths) == len(scene.fwhm)
    assert 370 < scene.wavelengths.min() < 400 and 2450 < scene.wavelengths.max() < 2550
    assert np.all(np.diff(scene.wavelengths) > 0)
    assert scene.res_x == pytest.approx(30, abs=1) and scene.res_y == pytest.approx(30, abs=1)
    assert 0 < scene.good_bands.sum() < scene.shape[0]


@needs_scene
def test_read_cube_shapes_and_masking(scene):
    win = (100, 120, 100, 130)
    cube, wl = scene.read_cube(win)
    assert cube.shape == (scene.good_bands.sum(), 20, 30) and len(wl) == cube.shape[0]
    assert cube.dtype == np.float32
    assert np.nanmax(cube) < 2.0                      # reflectance, not scaled integers
    sub, _ = scene.read_cube(win, stride=2)
    assert sub.shape[1:] == (10, 15)


@needs_scene
def test_read_band_matches_the_cube(scene):
    win = (100, 110, 100, 110)
    cube, wl = scene.read_cube(win, bands="all")
    band = scene.read_band(860, win)
    i = scene.band_index(860)
    both = np.isfinite(band) & np.isfinite(cube[i])
    assert both.any() and np.allclose(band[both], cube[i][both])


@needs_scene
def test_georeferencing_roundtrip(scene):
    row, col = 200, 300
    lon, lat = scene.rowcol_to_lonlat(row, col)
    r2, c2 = scene.lonlat_to_rowcol(lon, lat)
    assert int(r2[0]) == row and int(c2[0]) == col


@needs_scene
def test_window_transform_shifts_the_origin(scene):
    t_full, t_win = scene.transform(), scene.transform((10, 50, 20, 60))
    assert t_win.c == pytest.approx(t_full.c + 20 * scene.res_x)
    assert t_win.f == pytest.approx(t_full.f - 10 * scene.res_y)


@needs_scene
def test_subset_roundtrip_preserves_values_and_grid(scene, tmp_path):
    win = (100, 132, 100, 132)
    out = hu.write_subset(scene, tmp_path / "sub.h5", win)
    with hu.TanagerScene(out) as sub:
        assert sub.shape[1:] == (32, 32)
        assert sub.transform() == scene.transform(win)
        a, _ = scene.read_cube(win, mask=False)
        b, _ = sub.read_cube(mask=False)
        ok = np.isfinite(a) & np.isfinite(b)
        assert np.abs(a[ok] - b[ok]).max() < 1e-4     # int16 scaling keeps 4 decimals
