"""Week 1 · Session 4 — Hyperspectral data access, visualisation and exploration (practical)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("Data access, visualisation and exploration",
         "Week 1 · Session 4",
         notebook="00_EO_data_quickstart_notebook.ipynb",
         subtitle="From a public catalogue to a spectrum on your screen",
         week="Week 1 · 2–5 November 2026")

d.objectives([
    "Navigate a STAC catalogue: collection, item, asset",
    "Say what is inside a Tanager HDF5 file and find the wavelengths",
    "Preview a scene cheaply before downloading a gigabyte",
    "Read a window or a subset of bands instead of the whole cube",
    "Choose a scene for your own project using real availability",
], notes="This session is mostly hands-on. Keep the slides brisk — about 30 minutes — and spend the rest "
         "of the time in the notebooks with people running things on their own machines.")

d.section("1. Finding data", "STAC, the industry standard catalogue")

d.bullets("STAC in one slide", [
    "**SpatioTemporal Asset Catalog** — a JSON convention for describing Earth observation data",
    "**Catalog** → the top level, links to collections",
    "**Collection** → a themed group of scenes, e.g. `fire`, `urban`, `GHG-plumes`",
    "**Item** → one acquisition: geometry, datetime, cloud cover, plus metadata",
    "**Asset** → one downloadable file belonging to that item",
    ("Planet's Tanager catalogue is *static*: plain JSON files, no server, no account, no API key", 1),
], kicker="the vocabulary",
   notes="Static catalogues are the simplest possible case: a URL returns JSON, and you follow links. "
         "Contrast with Planetary Computer, which has a search API — notebook 00 uses both.")

d.code("Fetching one scene's metadata", """
import requests

base = "https://www.planet.com/data/stac/tanager-core-imagery"
item = requests.get(f"{base}/agriculture/20250608_091605_90_4001/"
                    "20250608_091605_90_4001.json").json()

print(item["properties"]["location_description"])   # Çumra, Konya, Türkiye
print(item["properties"]["cloud_percent"])          # 2
print(sorted(item["assets"]))                       # what you can download
""", caption="No authentication, no SDK — the catalogue is just JSON over HTTPS.",
   notes="Run this live. It is the moment students realise satellite data access is not gated behind a "
         "complicated portal, at least for open data.")

d.figure_bullets("What is actually in the archive",
                 "16_scene_finder/00_2_what_s_in_the_archive.png",
                 ["**153 unique scenes**, from 25 Sep 2024 to 29 Oct 2025",
                  "276 catalogue entries — 123 scenes appear in more than one collection",
                  "Nine themed collections, from `agriculture` to `snow-ice`",
                  "Scene footprints span 322–879 km², median **394 km²**"],
                 caption="Tanager open data by collection and over time",
                 kicker="the Tanager open archive",
                 notes="Set expectations early: this is a tasked demonstration archive, not a global "
                       "mapping mission. Deduplicate by scene ID, or you will double-count.")

d.figure("Where the scenes are",
         "16_scene_finder/01_3_a_world_view.png",
         caption="Footprint centroids, coloured by collection",
         kicker="global coverage is sparse",
         notes="The United States dominates with 52 scenes, then Argentina with 15 and the Netherlands "
               "with 9. Ask students what that means for a project over their own country.")

d.section("2. Inside a Tanager scene", "One HDF5 file, many layers")

d.table("What the surface reflectance file contains", ["Layer", "Shape", "What it is for"], [
    ["surface_reflectance", "426 × rows × cols", "The data cube itself"],
    ["surface_reflectance_uncertainty", "426 × rows × cols", "Per-pixel, per-band uncertainty → SNR"],
    ["nodata_pixels", "rows × cols", "Outside the swath after orthorectification"],
    ["beta_cloud_mask / beta_cirrus_mask", "rows × cols", "Cloud screening — always inspect it"],
    ["column_water_vapour, aerosol_optical_depth", "rows × cols", "Atmospheric correction inputs"],
    ["sun / sensor zenith and azimuth", "rows × cols", "Illumination and viewing geometry"],
], col_widths=[3, 2, 3], kicker="HDFEOS/GRIDS/HYP/Data Fields",
   notes="The uncertainty cube is unusual and valuable — most missions do not ship one. It is what lets "
         "us measure SNR per band in notebook 11 rather than guessing.")

d.bullets("Where the wavelengths live", [
    "Attached to the `surface_reflectance` dataset as attributes, not as a separate file",
    "**wavelengths** — 426 band centres in nanometres (376–2499 nm)",
    "**fwhm** — the width of each band (5.2–6.8 nm)",
    "**good_wavelengths** — a flag marking bands the provider considers unusable",
    "The grid (CRS, corner coordinates, pixel size) is in `HDFEOS INFORMATION/StructMetadata.0`",
    ("The STAC item also carries wavelengths, as `eo:center_wavelength` in micrometres", 1),
], kicker="metadata that matters",
   notes="Warn about the unit trap: the STAC metadata is in micrometres, the file attributes in "
         "nanometres. Mixing them silently gives nonsense band selections.")

d.table("The assets, and when to use each", ["Asset", "Size", "Use it for"], [
    ["thumbnail", "kilobytes", "Deciding whether a scene is worth a closer look"],
    ["ortho_visual", "megabytes", "A true-colour COG you can stream into a map"],
    ["ortho_sr_hdf5", "~1 GB", "The surface reflectance cube — the real analysis product"],
    ["ortho_radiance_hdf5", "~1 GB", "At-sensor radiance, needed for gas retrievals"],
    ["ortho_beta_udm", "megabytes", "Usable-data mask as a GeoTIFF"],
], col_widths=[3, 1, 4], kicker="pick the cheapest asset that answers your question",
   notes="'Basic' variants are the unprojected versions. For this course we always use the 'ortho' "
         "products, which are already on a map grid.")

d.callout("Never download a gigabyte to find out the scene is cloudy.",
          "The thumbnail is a few kilobytes and the visual COG streams. Look first, download second — "
          "and when you do download, read only the window and the bands you need.",
          kicker="the workflow rule of the day",
          notes="This is the habit that separates a smooth project from one that spends week 3 waiting "
                "for downloads on a conference-centre wifi.")

d.section("3. Reading efficiently", "Windows, strides and bands")

d.code("Three ways to read less", """
import hsi_utils as hu
scene = hu.get_scene("20250608_091605_90_4001")   # local file, or downloads it

# 1. a spatial window: (row_start, row_stop, col_start, col_stop)
cube, wl = scene.read_cube(window=(200, 400, 300, 500))

# 2. a strided preview of the whole scene — every 4th row and column
preview, wl = scene.read_cube(stride=4)

# 3. one band, by wavelength in nm
nir = scene.read_band(860)
""", caption="A full cube is ~950 MB in memory; a 200 × 200 window is about 55 MB.",
   notes="Stress that read_cube returns good bands only by default, with invalid pixels as NaN. The "
         "conventions are documented at the top of hsi_utils.py.")

d.bullets("Two habits worth forming now", [
    "**Preview with a stride, analyse in a window.** Full-resolution full-scene reads are rarely needed",
    "**Check the masks before trusting any number** — no-data, cloud and cirrus",
    ("Around 20–30 % of every Tanager grid is no-data: the swath is rotated inside a north-up grid", 1),
    "Invalid pixels come back as NaN, so use `np.nanmean` and friends throughout",
    "If your statistic looks strange, map the mask first — it is usually the explanation",
], kicker="working practice",
   notes="The Al Dhafra scene is the cautionary tale: its cloud mask flags bright sabkha under a clear "
         "sky. Session 5 goes into this properly.")

d.figure("Six scenes, six very different problems",
         "12_processing_workflow/01_4_batch_processing_all_course_scenes.png",
         caption="True-colour quicklooks of the course scenes (stride 3)",
         kicker="your working data",
         notes="Walk through them: burn scar, coal mines, mangrove estuary, megacity, sabkha coast, "
               "irrigated desert agriculture. Ask which theme each student's interest maps onto.")

d.section("4. Choosing a scene for your project", "Availability decides feasibility")

d.bullets("What to filter on", [
    "**Cloud cover** — `cloud_percent` in the item properties, but verify with the thumbnail",
    "**Off-nadir angle** — large angles distort geometry and change illumination",
    "**Sun elevation** — low sun means long shadows, a problem in terrain",
    "**Date** — does it match the phenology or the event you care about?",
    "**Repeat coverage** — change detection needs two scenes over the same place",
    ("Six Tanager scenes cover Malibu, which is why the fire change-detection example exists", 1),
], kicker="selection criteria",
   notes="Point out that cloud_percent is a scene-wide number: a scene can be 10 % cloudy overall and "
         "100 % cloudy over your area of interest.")

d.table("Availability over the Arab region", ["Query", "Result"], [
    ["Scenes intersecting the region box", "14"],
    ["Of those, in Arab League countries", "8"],
    ["Countries represented", "Syria, Sudan, UAE, Saudi Arabia, Algeria, Egypt"],
    ["Remaining after a ≤ 20 % cloud filter", "5"],
], col_widths=[3, 4], kicker="a real search, from notebook 16",
   notes="This is the reality check for project scoping: the regional archive is thin, so most teams will "
         "work on a course scene or extend to EnMAP and Sentinel-2. Better to learn that now than in week 3.")

d.handover("00_EO_data_quickstart_notebook.ipynb", [
    "Search a STAC catalogue and inspect an item's properties and assets",
    "Display a thumbnail and stream a visual COG onto an interactive map",
    "Open the HDF5, read the wavelengths, and plot a full 426-band spectrum",
    "Compute your first indices and check them against the quality masks",
    "Then pick one theme notebook (01–06) that matches your interest and run it",
], minutes=120,
   notes="Pair people by theme interest — it seeds the project teams that form in week 2. The exercise "
         "sets exercises/ex_00 to ex_06 are the homework for anyone who finishes early.")

d.recap([
    "STAC: catalog → collection → item → asset; Tanager's is static, open and needs no account",
    "The HDF5 holds the cube, the masks, the uncertainty and the **wavelengths as attributes**",
    "Preview with thumbnails and strides; download and read full resolution only when you must",
    "Always inspect the masks before trusting a statistic",
    "**Check availability before committing to an area** — notebook 16 does this in one cell",
], next_up="Session 5 — Preprocessing concepts for hyperspectral data",
   notes="Ask everyone to leave today with a scene ID they are curious about. That is the seed of the "
         "scoping canvas in week 2.")

d.references([
    "STAC specification — stacspec.org",
    "Planet Tanager open data catalogue (CC-BY-4.0) — www.planet.com/data/stac",
    "Planet Tanager product documentation — docs.planet.com/data/imagery/tanager",
    "Course notebooks: 00_EO_data_quickstart_notebook.ipynb, 16_scene_finder.ipynb",
    "Scoping canvas — templates/project_scoping_template.md",
])

d.save("w1d_data_access_exploration.pptx")
