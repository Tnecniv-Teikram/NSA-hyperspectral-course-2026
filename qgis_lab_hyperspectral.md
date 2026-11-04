# 🗺️ QGIS lab — hyperspectral data on the desktop

**Space Academy 2026 · Hyperspectral course · Practical (≈ 3 hours)**
**Pairs with:** `17_hypercoast_tanager_enmap.ipynb` (do the notebook first — it produces the files used here)

Python is where you build a method. A desktop GIS is where most colleagues will *look* at your result, digitise
training areas, and combine your map with roads, parcels and protected areas. This lab covers both directions:
hyperspectral cubes **into** QGIS, and your Python results **back out** to a map someone else can use.

> **Status note for the instructor.** The data side of this lab is verified: the files written by
> `tools/export_for_qgis.py` were checked to carry per-band wavelengths in GDAL's ENVI metadata domain, and the
> EnMAP subset in `data/enmap/` opens with its official metadata. The **GUI steps below were written from the
> EnMAP-Box 3.17 and QGIS 3.40 documentation and have not been clicked through on the course machine** — QGIS
> could not be installed here because the network blocks qgis.org, the OSGeo mirrors and the conda channel.
> Walk through it once on a machine with QGIS before teaching, and drop screenshots into the marked places.
> Menu labels move slightly between versions; the *concepts* and the file formats are stable.

---

## 0. What you need

| Item | Where it comes from |
|------|--------------------|
| **QGIS 3.40 LTR** or newer (3.44 LTR also fine) | [qgis.org/download](https://qgis.org/download/) — the EnMAP-Box requires QGIS ≥ 3.40 and < 4.0, so **do not** use QGIS 4.x for this lab |
| **EnMAP-Box 3.17+** plugin | QGIS → *Plugins → Manage and Install Plugins…* → search "EnMAP-Box" |
| **HyperCoast** plugin (optional) | same dialog, search "HyperCoast" ([plugin page](https://plugins.qgis.org/plugins/hypercoast/)) |
| Tanager export (ENVI + GeoTIFF + RGB) | `outputs/17/` — produced by notebook 17, or `python tools/export_for_qgis.py` |
| EnMAP L2A subset | `data/enmap/enmap_groningen_subset.tif` (+ its `METADATA.XML`) |

**Copy the data to a local folder first.** Reading a 44 MB BSQ from a synced OneDrive folder is slow and QGIS
will feel broken when it is only waiting for the file provider.

---

## 1. Why a plain GeoTIFF is not enough (10 min)

Open QGIS and drag in `20250223_165546_32_4001_150_150_rgb.tif` (the 3-band quicklook). It behaves like any
image: pan, zoom, identify.

Now drag in the 352-band cube `20250223_165546_32_4001_150_150.tif`. QGIS renders *a* band combination and the
band list shows `401.3 nm`, `406.3 nm`, … because the exporter wrote band descriptions. But plain QGIS has no
idea those names are wavelengths: *Identify Features* gives you 352 numbers in a list, not a spectrum.

That is the gap the **EnMAP-Box** fills. It reads the wavelength metadata (GDAL's ENVI domain: `wavelength`,
`wavelength_units`, `fwhm`, `bbl`) and turns those 352 numbers into a plot with nanometres on the x-axis.

> 💡 **Teaching point.** Ask the class what would happen if you exported the cube from Python with
> `rasterio` defaults and no metadata. Answer: exactly this — a stack of anonymous bands. The metadata *is*
> the deliverable.

*[screenshot: the band list showing "401.3 nm", "406.3 nm", …]*

---

## 2. Load the cube in the EnMAP-Box (25 min)

1. Start the box: *Raster → EnMAP-Box → EnMAP-Box* (or the toolbar icon).
2. *File → Add data source…* and choose **`…_bsq.bsq`** (the ENVI file — its `.hdr` carries the wavelengths).
   Add `data/enmap/enmap_groningen_subset.tif` as well.
3. Open a **Map View** (*View → Open Map View*) and drag the Tanager source into it.
4. Set a sensible composite: right-click the layer → *Properties → Symbology → Multiband color*, and choose
   bands near **665 nm (red), 560 nm (green), 490 nm (blue)**. The EnMAP-Box lets you type a wavelength instead
   of a band number — use that, and note how much easier it is than counting bands.
5. Switch to a false-colour infrared composite: **860 / 665 / 560 nm**. Vegetation turns red.
6. Try a SWIR composite: **2200 / 1650 / 860 nm**. Now the mine spoil, sabkha or burn scars stand out instead.

**Checkpoint:** you should have one map view with three saved composites you can flip between.

*[screenshot: EnMAP-Box with the Tanager cube in false colour]*

---

## 3. Read spectra: the profile tool and a spectral library (40 min)

1. Open a **Spectral Library View** (*View → Open Spectral Library View*).
2. Activate the **Identify → Spectral Profile** tool in the map view toolbar.
3. Click a pixel. Its spectrum appears in the library view, with wavelength on the x-axis. Click through:
   water, dense vegetation, bare soil, a bright roof or spoil heap.
4. **Save the interesting ones**: with a profile selected, use the library view's *add profile* button, then
   *Save as…* → `.gpkg` or ENVI `.sli`. You have just built a spectral library the same way the course library
   in `data/spectral_library/` was built — except there we did it in Python over hundreds of pixels.
5. Compare sensors: open the EnMAP subset in a second map view and click a vegetated field. Put the Tanager and
   EnMAP profiles in the *same* library plot and compare sampling — this is section 6 of notebook 17, done by hand.

> ⚠️ **Reflectance scaling.** Both files store reflectance as integers ×10 000 (the EnMAP L2A convention, which
> our Tanager export follows). The profile plot therefore runs to ~4 000, not 0.4. The ENVI header declares
> `reflectance scale factor = 10000`; if your plot shows raw integers, that is why.

**Questions for the class**
- Which features can you see in the Tanager profile that the EnMAP profile blurs, and vice versa?
- Find the water-vapour gaps. Why are those bands flat/missing in our export? (We removed them — `bbl` marks them.)

*[screenshot: spectral profile plot with two sensor profiles overlaid]*

---

## 4. A spectral index without writing code (20 min)

The EnMAP-Box ships a **Spectral Index Creator** (*Processing Toolbox → EnMAP-Box → Spectral Indices*, or
*Applications → Spectral Index Creator* depending on version). It knows several hundred published indices and
picks the right bands by wavelength.

1. Compute **NDVI** on the Tanager cube; then **NDMI** or **NBR**.
2. Style the result with a red-yellow-green ramp, min −0.2 max 0.9.
3. Compare with the NDVI you computed in notebook 12. They should agree to within rounding — if they do not,
   check which wavelengths each used.

> 💡 This is the honest argument for QGIS in a hyperspectral workflow: for *standard* products, a GUI with a
> wavelength-aware index library is faster and less error-prone than hand-written band arithmetic.

---

## 5. Classification inside QGIS (45 min)

The EnMAP-Box brings scikit-learn classifiers into the QGIS Processing framework, so you can run the workflow
of notebook 15 without code.

1. **Training data.** Either load the reference labels we already have
   (`data/labels/20250223_165546_32_4001_worldcover2021_30m.tif`), or digitise your own: *Layer → Create Layer →
   New GeoPackage Layer…*, polygon geometry, one text field `class`, then draw a handful of polygons per class
   over mangrove, water, cropland and bare ground.
2. *Processing Toolbox → EnMAP-Box → Classification → **Fit Random Forest Classifier***: raster = the Tanager
   cube, reference = your polygons/labels, field = `class`.
3. Then *Predict classification layer* with the fitted model and the cube.
4. Style the output with the WorldCover colours and compare it with the map notebook 15 produced.

**Discussion:** you have now built the same product twice. Which route would you hand to a colleague who does
not write Python — and which would you use to produce the same map for fifty scenes next month?

*[screenshot: RF classification result in the EnMAP-Box]*

---

## 6. The HyperCoast plugin (20 min)

The HyperCoast QGIS plugin ([docs](https://plugins.qgis.org/plugins/hypercoast/)) reads the same sensors as the
Python library — EMIT, PACE, DESIS, NEON, AVIRIS, PRISMA, **EnMAP**, **Tanager**, Wyvern — straight from their
native files, and adds click-to-plot spectra and band sliders.

1. Open it from the plugin toolbar, choose the **Tanager** reader and point it at a raw
   `*_ortho_sr_hdf5.h5` scene — no conversion step.
2. Pick RGB wavelengths with the sliders; click pixels to plot spectra; export the collected spectra to CSV.
3. Compare the workflow with section 4 of notebook 17. Same operations, different front end.

**When to use which:** the HyperCoast plugin is the quickest way to *look* at a raw scene; the EnMAP-Box is the
better place to *work* (libraries, indices, classifiers, accuracy assessment).

---

## 7. Bring a Python result back into QGIS (20 min)

Everything the course notebooks export is already a Cloud-Optimised GeoTIFF with a CRS, so it just opens:

1. Add `outputs/15/20250223_165546_32_4001_rf_classes.tif` (notebook 15's classification) and
   `outputs/20/..._hybridsn_classes.tif` (the CNN map from notebook 20).
2. Style them as *Paletted/Unique values* and assign the class colours.
3. Add `..._hybridsn_confidence.tif` and style it with a magma ramp — where is the model unsure?
4. Build a print layout (*Project → New Print Layout*): map, legend, scale bar, north arrow, data credit
   *"Tanager STAC Data © 2025 Planet Labs PBC (CC-BY-4.0)"*. Export it as a PDF for your final presentation.

**Deliverable for the day:** one PDF map of your classification, with a legend and the data credit.

---

## 8. Practical pitfalls (read before the class)

| Symptom | Cause and fix |
|---------|---------------|
| Layer draws grey/black, or statistics take forever | QGIS computes statistics over all 352 bands. Build overviews (*Raster → Miscellaneous → Build Overviews*), or work from the `_rgb.tif` for navigation and keep the cube for analysis. |
| Spectral profile shows "band number" instead of nanometres | The wavelength metadata is missing. Use the ENVI `.bsq` (its `.hdr` has `wavelength`), or re-export with `tools/export_for_qgis.py`. |
| Profile values in the thousands | Reflectance is scaled ×10 000. Divide, or set a scale factor in the layer properties. |
| Everything is slow | The file is on OneDrive/network storage. Copy it to a local disk. |
| EnMAP-Box missing from the plugin list | You are on QGIS 4.x — install the 3.40/3.44 LTR instead. |
| Black stripes / no-data shown as valid | Set the no-data value to **−32768** in *Layer Properties → Transparency*. |

## What to hand in

- The spectral library you built (`.gpkg` or `.sli`) with at least four named materials
- A screenshot of the Tanager and EnMAP profiles for the same material type, with one sentence on the difference
- The classification PDF map from section 7

---
> 📖 Data: Tanager — CC-BY-4.0 © Planet Labs PBC · EnMAP L2A example data © DLR 2022 via
> [enmap.org](https://www.enmap.org/data/example_data/) · EnMAP-Box: [enmap-box.readthedocs.io](https://enmap-box.readthedocs.io) ·
> HyperCoast: Liu & Wu (2024), *JOSS* 9(100), 7025 · free EnMAP-Box teaching material: [HYPERedu on EO College](https://eo-college.org)
