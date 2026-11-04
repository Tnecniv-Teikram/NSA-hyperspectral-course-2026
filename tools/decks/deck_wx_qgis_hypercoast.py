"""Optional session — Hyperspectral data in HyperCoast and QGIS."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("Hyperspectral data in HyperCoast and QGIS",
         "Optional session · Week 2",
         notebook="17_hypercoast_tanager_enmap.ipynb + qgis_lab_hyperspectral.md",
         subtitle="One API for many sensors, and your cube on the desktop",
         week="Space Academy 2026 · Hyperspectral course")

d.objectives([
    "Read Tanager **and** EnMAP with one library, and know when to prefer it over `hsi_utils`",
    "Pull a spectrum by latitude/longitude instead of row and column",
    "Compare two sensors that sample the same spectrum differently",
    "Export a cube so QGIS and the EnMAP-Box show wavelengths, not band numbers",
    "Run the desktop workflow: profiles, spectral library, index, classification, print layout",
], notes="This session exists because most colleagues and clients live in a desktop GIS, not in Jupyter. "
         "Ask who has used QGIS before — it changes how much of part 2 you demonstrate versus let them explore.")

d.section("1. Another library: HyperCoast", "hypercoast.org · Liu & Wu (2024), JOSS 9(100), 7025")

d.table("Two libraries, two jobs", ["", "hsi_utils (this course)", "hypercoast"], [
    ["Scope", "Tanager, written for teaching", "EMIT, PACE, AVIRIS, NEON, DESIS, PRISMA, EnMAP, Tanager, Wyvern"],
    ["Reading", "windows, strides, chosen bands", "whole cube to xarray (or chosen bands)"],
    ["Masks", "QA masks applied for you", "raw data, you apply masks"],
    ["Visuals", "matplotlib", "interactive map, click-to-plot spectra, 3-D cube"],
    ["Desktop", "—", "a QGIS plugin with the same readers"],
], kicker="not a competition", col_widths=[1, 2, 3],
   notes="The honest summary: hsi_utils for control and memory, HyperCoast for exploration and breadth. "
         "Students should be able to justify which they used in their project.")

d.callout("A whole-cube reader is a memory trap.",
          "read_tanager() loads float64 and keeps a second alias of the same array: one Tanager scene becomes "
          "about 4 GB of RAM. Pass bands=… and it reads only those bands from disk — 88 bands is ~0.7 GB.",
          kicker="the first thing to teach",
          notes="Show the numbers in the notebook rather than asserting them. This is the most common way a "
                "student's laptop dies in week 2.")

d.figure_bullets("Spectra by coordinate, not by pixel index",
                 "17_hypercoast_tanager_enmap/00_3_spectra_at_a_coordinate.png",
                 ["`extract_tanager(ds, latitude, longitude, delta)` averages a small neighbourhood",
                  "The dataset carries per-pixel **latitude/longitude** arrays",
                  "Useful when your reference data is a list of GPS points",
                  "Three targets here: mangrove, estuary water, cropland"],
                 caption="El Salvador scene, three coordinates",
                 notes="Contrast with hsi_utils, where you convert lon/lat to row/col yourself. Field teams "
                       "think in coordinates; this is the bridge.")

d.figure("The same scene through two sensors",
         "17_hypercoast_tanager_enmap/04_6_tanager_vs_enmap_on_the_same_target.png",
         caption="A Tanager spectrum, and the same spectrum resampled to EnMAP's band centres and widths",
         kicker="sampling, not truth",
         notes="Ask: which sensor would you choose for a red-edge indicator, and does the difference matter "
               "for the decision your project supports? Often it does not — say so when it does not.")

d.bullets("Real products fight back", [
    "Official EnMAP L2A ships as **ENVI BSQ + .hdr**, not GeoTIFF",
    "`read_enmap()` on a BSQ fails: *the new name 'wavelength' conflicts* — the header already defines it",
    "Convert to GeoTIFF first, and keep `*METADATA.XML` **beside** the file so wavelengths are found",
    "The documented `wavelengths=` argument raises `UnboundLocalError` in 0.27.0 — do not rely on it",
    ("Lesson: budget time for data plumbing, and read the library source when the error makes no sense", 1),
], kicker="what the notebook hits",
   notes="This is deliberately in the course. Students meet exactly these problems in their projects and "
         "think they did something wrong. Normalise reading library source code.")

d.section("2. Getting a cube into QGIS", "Metadata is the deliverable")

d.bullets("QGIS shows any raster — but a spectrum needs metadata", [
    "A 352-band GeoTIFF opens fine, and *Identify* returns 352 anonymous numbers",
    "The **EnMAP-Box** turns those into a spectrum by reading GDAL's **ENVI metadata domain**",
    "It needs `wavelength`, `wavelength_units`, and ideally `fwhm` and `bbl` (bad-band list)",
    "An ENVI `.hdr` carries them natively; a GeoTIFF can carry the same domain",
    "**Band descriptions** (`\"665.0 nm\"`) help humans, but are not the metadata the tools read",
], kicker="the gap",
   notes="Ask what happens if you export with rasterio defaults: a stack of anonymous bands. The metadata is "
         "the difference between a picture and a measurement.")

d.code("tools/export_for_qgis.py writes all three", '''
# ENVI: the safest option for the EnMAP-Box
with rasterio.open(path, "w", driver="ENVI", interleave="bsq", **profile) as dst:
    dst.write(data)                                   # int16, reflectance x 10000
    dst.update_tags(ns="ENVI", wavelength="{401.29, 406.26, ...}",
                    wavelength_units="Nanometers", fwhm="{...}", bbl="{...}")
    for i, w in enumerate(wl, start=1):
        dst.set_band_description(i, f"{w:.1f} nm")     # what the QGIS band list shows
''', kicker="the export in five lines",
   notes="Walk the three consumers: EnMAP-Box reads the ENVI domain, HyperCoast reads dataset metadata or the "
         "METADATA.XML, and the QGIS band list shows descriptions. Write all three and you are safe.")

d.callout("Building an interactive map breaks later file writes.",
          "leafmap sets GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR to speed up remote tiles. GDAL can then no longer "
          "create the sidecar files a new ENVI or GeoTIFF needs, and every write fails with "
          "\"SystemError: Unknown GDAL Error\" — in that kernel and in any subprocess it spawns. "
          "One line fixes it: os.environ.pop(\"GDAL_DISABLE_READDIR_ON_OPEN\", None).",
          kicker="a genuinely nasty trap",
          notes="This cost real debugging time while building the course. It is worth five minutes: the lesson "
                "is that libraries mutate global state, and an unhelpful error is often environmental.")

d.section("3. The desktop lab", "qgis_lab_hyperspectral.md · about 3 hours")

d.table("What the lab covers", ["Step", "Tool", "Output"], [
    ["Load cube, band composites by wavelength", "EnMAP-Box map view", "RGB, false colour, SWIR views"],
    ["Click spectra, build a library", "Spectral profile + library view", "`.gpkg`/`.sli` spectral library"],
    ["Compare Tanager with EnMAP", "two map views, one library plot", "a sampling comparison"],
    ["Spectral index without code", "Spectral Index Creator", "NDVI/NBR raster"],
    ["Random forest classification", "Processing → EnMAP-Box", "classified map"],
    ["Raw scene, no conversion", "HyperCoast plugin", "spectra exported to CSV"],
    ["Python results back in", "COGs from notebooks 15 and 20", "print layout PDF"],
], kicker="the run sheet", col_widths=[3, 2, 2],
   notes="Timings are in the lab document. If short of time, drop the index step (section 4) — it is the one "
         "students can most easily do alone afterwards.")

d.bullets("Requirements that bite", [
    "**QGIS 3.40 or 3.44 LTR** — the EnMAP-Box does not support QGIS 4.x yet",
    "HyperCoast needs **Python ≥ 3.11**, stricter than the rest of the course",
    "Copy data to a **local disk**: GDAL over OneDrive or a network share feels broken",
    "Set no-data to **−32768** or the swath edges render as valid dark pixels",
    "Build overviews before class, or statistics over 352 bands will stall the room",
], kicker="prepare before the session",
   notes="Install QGIS and both plugins on the teaching machines the week before. Plugin installation needs "
         "outbound access to plugins.qgis.org, which is exactly what a corporate network tends to block.")

d.handover("17_hypercoast_tanager_enmap.ipynb → qgis_lab_hyperspectral.md", [
    "Notebook: read Tanager and EnMAP, extract spectra by coordinate, compare sampling",
    "Notebook: export the cube for QGIS and inspect the ENVI header it wrote",
    "Lab: profiles and a spectral library, an index, a classification, a print layout",
    "Hand in: your spectral library, a two-sensor profile screenshot, and the map PDF",
], minutes=180,
   notes="Pair students who know QGIS with those who do not. The deliverable is deliberately a map PDF — most "
         "of them will need exactly that for the final presentation.")

d.recap([
    "One library reads many sensors — and the same readers exist as a **QGIS plugin**",
    "Ask for the bands you need; whole-cube reads are a memory trap",
    "Wavelengths live in the **ENVI metadata domain**: without them QGIS shows band numbers",
    "Desktop GIS is where your result meets the people who will use it",
    "Expect data plumbing: formats, metadata locations and library quirks are part of the job",
], next_up="Project scoping — choose the scenes you will actually work on",
   notes="Close on the practical point: their final deliverable is a map someone else can open.")

d.references([
    "Liu, B. & Wu, Q. (2024). HyperCoast: A Python package for visualizing and analyzing hyperspectral data. JOSS 9(100), 7025.",
    "HyperCoast documentation — https://hypercoast.org · QGIS plugin — https://plugins.qgis.org/plugins/hypercoast/",
    "EnMAP-Box 3 documentation — https://enmap-box.readthedocs.io",
    "HYPERedu / EO College free EnMAP teaching material — https://eo-college.org",
    "EnMAP example data — https://www.enmap.org/data/example_data/",
    "Tanager open data and STAC catalogue — https://www.planet.com/data/stac",
])

d.save("wx_qgis_hypercoast.pptx")
