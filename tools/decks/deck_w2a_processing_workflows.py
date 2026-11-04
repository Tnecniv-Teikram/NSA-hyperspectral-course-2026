"""Week 2 · Session 1 — Hyperspectral image processing workflows."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("Hyperspectral image processing workflows",
         "Week 2 · Session 1",
         notebook="12_processing_workflow.ipynb",
         subtitle="From a pile of cells to a pipeline you can rerun, batch and defend",
         week="Week 2 · 9–12 November 2026")

d.objectives([
    "Describe the standard processing chain and the role of each step",
    "Drive an analysis from a **configuration**, so no parameter is buried in code",
    "Export analysis-ready products: a Cloud-Optimised GeoTIFF plus a provenance sidecar",
    "Batch-process many scenes and read the summary table like a quality analyst",
    "Process a full scene **tile by tile** with bounded memory, and know when to reach for dask",
    "Apply the reproducibility checklist that the interim review will hold you to",
], notes="This session is the hinge of the course: week 1 was about understanding the data, weeks 2–4 are about "
         "building something. Ask who has ever tried to rerun an analysis from three months ago and failed.")

d.section("1. Why a workflow", "The difference between an analysis and a result")

d.callout("A result you cannot reproduce is not a result.",
          "It is an anecdote with a colour bar. The same is true of a map whose parameters exist only in the "
          "scroll history of a notebook nobody else can run.",
          kicker="the standard to hold yourself to",
          notes="Set the tone early. The project rubric puts 30 % on Validity, and reproducibility is the first "
                "thing a reviewer checks. This is also what makes work transferable to a colleague or a client.")

d.bullets("Symptoms of a pile of cells", [
    "The same twelve steps copy-pasted into six notebooks, each slightly different",
    "A threshold changed in one place but not another",
    "A mask applied in one notebook and forgotten in the next",
    "Cells run out of order, so the file no longer describes what actually happened",
    "Nobody can say which version of the code produced the figure in the report",
], kicker="how irreproducible results start",
   notes="The theme notebooks 00–06 are deliberately written this way — repetition is good for learning. "
         "The moment you start a project, that repetition becomes a liability.")

d.table("What makes it a workflow", ["Property", "In practice"], [
    ["Parameterised", "everything that can change lives in one configuration object, not scattered in code"],
    ["Modular", "each step is a function with clear inputs and outputs, so it can be tested and replaced"],
    ["Traceable", "every output records how it was made: scene, parameters, software versions, date"],
], col_widths=[1, 3.2], kicker="three properties",
   notes="These three map onto three concrete artefacts you will produce today: a CONFIG dict, a set of step_ "
         "functions, and a JSON sidecar next to every GeoTIFF.")

d.bullets("The course processing chain", [
    "**1. Find / load** — STAC or local HDF5 · `hu.get_scene`",
    "**2. QA masks** — no-data, cloud, cirrus · `scene.masks`, `scene.valid_mask`",
    "**3. Bad bands** — water vapour, SWIR edge, low SNR · `hu.good_band_mask`",
    "**4. Subset** — window or tiles · `read_cube(window=…)`",
    "**5. Analyse** — indices, SAM, classification · `hu.nd`, `hu.spectral_angle`",
    "**6. Export** — COG plus JSON sidecar · `hu.save_geotiff`",
], kicker="six steps, every time",
   notes="Point out that steps 1–4 are identical for every project in the room; only step 5 differs. "
         "That is exactly why they belong in a shared module rather than in each student's notebook.")

d.bullets("Library code and notebook code", [
    "**`hsi_utils.py`** holds the reusable chain: loading, masking, bands, export, spectral helpers",
    "The **notebook** tells the story: why these parameters, what the figures show",
    "Later, `app/mangrove_product.py` takes the final method out of the notebook entirely",
    "A notebook cannot be imported, scheduled, unit-tested or reviewed line by line",
    "**Rule of thumb:** if you have pasted it twice, it belongs in a module",
], kicker="where does code live?",
   notes="Preview week 4: the same function is then called by the notebook, a command-line tool and a Streamlit app. "
         "Writing it once in a module is what makes that possible.")

d.section("2. Anatomy of a pipeline", "Configuration, steps, gates, outputs")

d.code("One dictionary holds every choice", """
CONFIG = {
    "scene_id": "20250608_091605_90_4001",   # Konya, Türkiye
    "window": (300, 500, 400, 600),          # None = whole scene
    "mask_cloud": True,
    "min_valid_fraction": 0.5,               # QA gate
    "indices": {                             # name: (band_a_nm, band_b_nm)
        "NDVI": (860, 665), "NDRE": (860, 705),
        "NDWI": (560, 860), "NDMI": (860, 1650), "NBR": (860, 2200),
    },
    "output_dir": hu.OUTPUT_DIR / "12",
    "overwrite": True,
}
""", kicker="config, not constants",
   caption="To process another area you change the configuration, not the code. In a project, keep it in YAML or JSON under version control.",
   notes="Ask the room where the wavelengths of their indices currently live. Usually: hard-coded in three cells. "
         "The config also becomes the first half of the provenance record.")

d.bullets("Steps as functions, with a gate", [
    "Each step takes the config plus the previous result, and returns something the next step can use",
    "The **QA step is a gate**: if too few pixels are usable, the pipeline stops with a clear message",
    "A window in the no-data corner gave `valid_fraction = 0.011` and was rejected at the 50 % gate",
    "Failing loudly beats quietly producing a map of NaNs",
    "Gates belong wherever an assumption could silently break downstream",
], kicker="fail loudly, fail early",
   notes="This is a transferable software habit: assert your assumptions at the boundary. "
         "In week 4 the same idea returns as quality flags on the product and as pytest assertions.")

d.bullets("Logging instead of print", [
    "A pipeline that runs unattended needs a **time-stamped log**, on screen and in a file",
    "Log the scene, the QA fractions, what was computed, what was written, and how long it took",
    "Log **skips** too: a scene not on disk, an output that already exists",
    "`logging` gives you levels — INFO for progress, WARNING for a QA gate that stopped a run",
    "The log is the first thing you read when a batch of 50 scenes finishes overnight",
], kicker="what happened while you slept",
   notes="Show the notebook's log lines: pipeline start, load, QA, indices, write, done in 0.4 s. "
         "The whole run is auditable from six lines of text.")

d.figure("Re-open what you wrote, and look at it",
         "12_processing_workflow/00_3_3_check_the_outputs.png",
         caption="The exported COG read back: 5 bands × 200 × 200, EPSG:32636, band names NDVI · NDRE · NDWI · NDMI · NBR",
         kicker="verify the export",
         notes="A good habit: never trust that a write succeeded. Re-open the file, check CRS, transform and band "
               "names, and plot it. Half of all 'the map looks wrong' problems are caught here in ten seconds.")

d.bullets("Analysis-ready output = data + provenance", [
    "A **Cloud-Optimised GeoTIFF**: internally tiled with overviews, streamable by QGIS and web maps",
    "**Band names** written into the file, so nobody has to guess what band 3 is",
    "A **JSON sidecar** with scene ID, acquisition time, CRS, geotransform and the exact band centres used",
    "Plus QA fractions, software versions, a hash of `hsi_utils.py`, and the data attribution",
    "Months later, that sidecar is the difference between a reusable product and a mystery raster",
], kicker="what to write next to the pixels",
   notes="Note the band-centre detail: the config asks for 860 nm, the file records that 861.26 nm was actually used. "
         "That distinction matters when someone tries to reproduce your index with another sensor.")

d.code("The sidecar that travels with the product", """
{
  "scene_id": "20250608_091605_90_4001",
  "acquired_utc": "2025-06-08T09:16:05+00:00",
  "crs": "EPSG:32636",
  "band_centres_used_nm": {"665": 665.87, "860": 861.26, "1650": 1647.66},
  "qa": {"valid_fraction": 0.999, "cloud_flag_fraction": 0.001},
  "software": {"python": "3.13.13", "numpy": "2.5.3",
               "hsi_utils_sha256": "5efdf1ca2448"},
  "attribution": "Tanager STAC Data ... (c) 2025 Planet Labs PBC. CC-BY-4.0"
}
""", kicker="provenance in practice",
   notes="Every field here answers a question a reviewer will ask. The hash of hsi_utils.py ties the result to the "
         "exact helper code that produced it, which version numbers alone cannot do.")

d.bullets("Idempotent re-runs", [
    "Running the same step twice with the same input should give the same result",
    "…and should not redo expensive work unless you ask for it",
    "With `overwrite=False` the export step sees the file and skips it: 0.4 s becomes 0.1 s",
    "This is what makes a 50-scene batch restartable after a crash",
    "It also stops you silently overwriting the figure that is already in your report",
], kicker="safe to run again",
   notes="Ask who has ever lost a result by rerunning a cell. Idempotency is cheap insurance, and it is the "
         "property that makes scheduling possible in week 4.")

d.section("3. Scaling up", "Memory, tiles and where the time actually goes")

d.bullets("Do the memory arithmetic first", [
    "Konya scene: 426 bands × 673 × 776 px × 4 bytes = **0.89 GB** as float32",
    "The larger Malibu scene: 426 × 1063 × 957 = **1.73 GB**",
    "NumPy often makes one or two temporary copies during a calculation",
    "A 256 × 256 tile of all bands is only **112 MB**",
    "Free Colab gives you ~12 GB of RAM — a stack of scenes will not fit",
], kicker="how big is a cube?",
   notes="Have them compute this for their own project scene before they start. Most 'my kernel died' messages "
         "in week 3 come from loading a full cube and then making two copies of it.")

d.figure_bullets("Tiling: full resolution, bounded memory",
                 "12_processing_workflow/02_5_tiled_processing_full_resolution_witho.png",
                 ["A generator yields one window at a time: 12 tiles of up to 256 × 256 px",
                  "Full-resolution spectral angle in **4.7 s**, peak memory ≈ **368 MB**",
                  "Two empty tiles skipped by a cheap validity check first",
                  "Notebook 30 does the same over a 1,063 × 957 scene: 8.3 s, **0.24 GB** peak",
                  "Small angles (yellow) pick out every irrigated field"],
                 caption="True colour · strided preview · tiled full resolution, with tile boundaries",
                 kicker="the standard pattern",
                 notes="SAM is a per-pixel operation, so the tiles leave no seams. Tiling also parallelises "
                       "trivially later, which is exactly what dask automates.")

d.bullets("Two surprises worth knowing", [
    "**Striding does not save time.** Tanager HDF5 is stored in compressed chunks of 14 bands × 44 × 49 px",
    "Reading every 4th pixel still decompresses every chunk: 3.0 s strided vs 4.7 s at full resolution",
    "Striding saves **memory**, not disk I/O — for fast previews use the `ortho_visual` COG or a subset",
    "**Neighbourhood operations need a halo.** Filters, texture, MNF noise, CNN patches",
    "Without overlapping tiles you get visible seams at every tile boundary",
], kicker="chunks and halos",
   notes="The chunk shape is a property of how the file was written, and it dictates what a fast read looks like. "
         "This is the single most useful thing to know about working with HDF5 and COG data.")

d.bullets("When to reach for xarray and dask", [
    "**xarray** attaches coordinates and a CRS: select by *wavelength*, not band index",
    "`da.sel(wavelength=665, method=\"nearest\")` instead of remembering band 58",
    "**dask** builds a lazy graph and processes chunk by chunk, in parallel if you have cores",
    "Full-scene mean reflectance computed lazily in **4.4 s**, identical to the tiled result",
    "Use them when the data no longer fits, or when you want the tiling done for you",
], kicker="optional, but useful",
   notes="Be balanced: dask is not free — the graph has overhead and debugging is harder. For a single 1 GB scene, "
         "hand-written tiling is clearer. For a stack of scenes or a cluster, dask earns its place.")

d.section("4. Batch and reproducibility", "Many scenes, and the habits that make them trustworthy")

d.figure("Seven scenes, one loop, one table",
         "12_processing_workflow/01_4_batch_processing_all_course_scenes.png",
         caption="Batch quicklooks with the cloud-flag percentage under each scene",
         kicker="batch processing",
         notes="The batch skips scenes that are not on disk with a log message rather than triggering surprise "
               "1 GB downloads — a small design decision that saves a classroom's bandwidth.")

d.bullets("Read the batch table like a QA analyst", [
    "One row jumps out: **Al Dhafra** has a very high cloud-flag percentage",
    "Its quicklook is almost cloud-free — the beta mask confuses bright sabkha with cloud",
    "A pipeline that trusted the mask would silently delete half the land in that scene",
    "Strided reads are fine for **statistics**; you do not need full resolution for a summary",
    "**Always** pair the table with quicklooks before trusting a batch result",
], kicker="what the summary reveals",
   notes="This closes the loop with yesterday's preprocessing session. The point is structural: batch summaries "
         "surface problems that single-scene work hides, which is why you run them early.")

d.table("The reproducibility checklist", ["Practice", "How"], [
    ["Pin versions", "requirements.txt, and store the versions in the sidecar"],
    ["Seed randomness", "np.random.default_rng(SEED), random_state=SEED, torch.manual_seed"],
    ["Config, not constants", "one config dict or file per run, saved next to the output"],
    ["Provenance", "JSON sidecar: scene, parameters, versions, date, attribution"],
    ["Log", "one log file per run; warnings for skips and QA failures"],
    ["Idempotent", "rerunning does not change or duplicate outputs"],
    ["Restart & Run All", "before every submission, on a clean kernel"],
    ["Relative paths", "hu.DATA_DIR and hu.OUTPUT_DIR, never /Users/yourname/…"],
], col_widths=[1.2, 3], kicker="eight habits",
   notes="This table reappears as section A of templates/interim_qa_checklist.md in week 3. "
         "Tell them the peer review will check it item by item, so adopting it now costs nothing later.")

d.bullets("Determinism is testable", [
    "Run the same computation twice with the same seed and compare a hash of the result",
    "Same seed → identical digest; different seed → a different sample, as expected",
    "If a 'deterministic' step gives two answers, you have an unseeded random call or thread non-determinism",
    "Cheap to write, and it catches a class of bug that is otherwise invisible",
], kicker="prove it, do not assume it",
   notes="This is the seed of the testing session in week 4, where the same idea becomes a regression test on "
         "the product's mapped area.")

d.handover("12_processing_workflow.ipynb", [
    "Run the pipeline on a window, inspect the COG and the sidecar it wrote",
    "Trigger the QA gate deliberately with a no-data window and read the message",
    "Batch all local scenes and find the anomaly in the summary table",
    "Process a full scene tile by tile and compare time and memory with a strided read",
    "Exercise 3: add a halo so a neighbourhood operation has no seams",
], minutes=120,
   notes="The halo exercise is the one that teaches the most. Let them hit the seams first, then fix it — "
         "the visible artefact makes the lesson stick.")

d.recap([
    "A workflow is **parameterised, modular and traceable** — config, functions, provenance",
    "Export **analysis-ready** products: COG with band names plus a JSON sidecar",
    "**Gate** your assumptions and **log** what happened; make reruns idempotent",
    "Tiling keeps memory at one tile: 0.89 GB cube processed with 368 MB peak",
    "Striding saves memory, not I/O — compressed chunks are read whole",
    "Neighbourhood operations need a **halo**; dask automates the chunking when you outgrow a laptop",
    "Reproducibility is a checklist, not a talent: seeds, versions, logs, relative paths",
], next_up="Session 2 — Feature extraction and dimensionality reduction: what to compute inside step 5",
   notes="End with the project instruction: build your analysis as run_pipeline(config) from day one. "
         "At the interim review you should be able to regenerate every figure from a config and one command.")

d.references([
    "Wilson, G. et al. (2017). Good enough practices in scientific computing. PLOS Computational Biology 13, e1005510.",
    "Sandve, G.K. et al. (2013). Ten simple rules for reproducible computational research. PLOS Computational Biology 9, e1003285.",
    "Rocklin, M. (2015). Dask: parallel computation with blocked algorithms and task scheduling. SciPy 2015.",
    "Hoyer, S. & Hamman, J. (2017). xarray: N-D labeled arrays and datasets in Python. JORS 5, 10.",
    "Cloud-Optimised GeoTIFF specification — cogeo.org",
    "Course material: notebook 12_processing_workflow.ipynb · hsi_utils.py · templates/interim_qa_checklist.md",
])

d.save("w2a_processing_workflows.pptx")
