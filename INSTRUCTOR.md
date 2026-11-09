# 🛰️ Space Academy 2026 — Hyperspectral course · instructor reference

*Participants start at [`README.md`](README.md); this page is the teaching-side detail.*

Course notebooks, **lecture slides**, exercises, quizzes, assignments, a **QGIS lab** and project templates for the
four-week **Space Academy 2026 hyperspectral course** (3–25 November 2026).
Start with **[`teaching_plan.md`](teaching_plan.md)** — it maps every session to its deck, notebook and homework,
with timings. They complement the theme starter notebooks `00`–`06` in
[`../Starting_notebooks`](../Starting_notebooks) (Arab Youth Space Hackathon: 813 Challenge), which cover data access and one
theme each. This folder covers the rest of the syllabus: preprocessing, feature extraction, target detection,
classification, GeoAI, validation, advanced analytics and the final project.

All material uses real **Planet Tanager** hyperspectral imagery (426 bands, 380–2500 nm, 30 m; CC-BY-4.0).

---

## Setup, data and the starter notebooks

All participant-facing setup — Colab, the local install, the kernel registration, the proxy CA bundle,
how scenes are fetched, and cloning the theme notebooks as `Starting_notebooks` — is in
[`README.md`](README.md). It is the page to send students to; keep edits there rather than here.

---

## Who this course is for, and what it assumes

The material is written for people who **already work with multispectral EO** (Sentinel-2, Landsat, QGIS, indices,
supervised classification in desktop software) and are **new to hyperspectral** and **new to GeoAI / machine
learning**. It never re-teaches what reflectance or NDVI is; it does teach, from zero, everything that is specific
to imaging spectroscopy and everything needed to train and validate a model.

| You need | Level | If you are short of it |
|---|---|---|
| Remote sensing fundamentals | Working knowledge — reflectance, atmospheric correction, band indices | The course assumes this; the theme notebooks 00–06 are a gentle refresher |
| **Python and numpy** | Able to read and adapt array code: slicing, axes, boolean masks, broadcasting | **Start with `09_numpy_for_hyperspectral.ipynb`** — 45–60 min, written for exactly this gap |
| Machine learning | None assumed | The `w2d0_ml_primer_for_eo` deck covers the vocabulary in 20 minutes before the classification session |
| Statistics | Comfortable with means, percentiles, a confusion matrix | Notebook 21 §5 (area-adjusted estimators) is marked as advanced/reference |

**Difficulty of each notebook** (⭐ follow along · ⭐⭐ requires attention · ⭐⭐⭐ advanced, has an optional deep-dive):

| Notebook | Level | Heaviest demand |
|---|---|---|
| `09_numpy_for_hyperspectral` | ⭐ | none — this is the on-ramp |
| `10_spectral_signatures_and_libraries` | ⭐ | reading plots |
| `11_preprocessing` | ⭐⭐ | numpy masking and axes |
| `12_processing_workflow` | ⭐⭐ | software-engineering patterns, not science |
| `13_feature_extraction_dim_reduction` | ⭐⭐⭐ | PCA/MNF — the maths is skippable, the MNF section says how |
| `14_material_discrimination_target_detection` | ⭐⭐⭐ | §1–2 are ⭐⭐; §3–4 (matched filter, unmixing) are the advanced part |
| `15_classification_classical` | ⭐⭐ | first real ML — do the primer deck first |
| `16_scene_finder` | ⭐ | familiar ground for anyone who has used a catalogue |
| `17_hypercoast_tanager_enmap` | ⭐ | lightest code in the course |
| `20_geoai_deep_learning` | ⭐⭐⭐ | PyTorch; needs the w3a mechanics slides first |
| `21_validation_accuracy_assessment` | ⭐⭐ | §1–4 essential, §5 advanced/reference |
| `30_advanced_analytics` | ⭐⭐⭐ | long; split it over two half-days |
| `31_from_notebook_to_product` | ⭐⭐ | packaging and testing |

## Course map: syllabus session → materials

📘 = lecture, 🔧 = practical. "Theme notebooks" are in `../Starting_notebooks`; everything else is in this folder.

### Week 1 · 2–5 Nov 2026 (onsite and online)

| Session | Type | Slides | Notebook(s) | Exercises / quiz / assignment |
|---------|:----:|--------|-------------|-------------------------------|
| Course orientation and objectives | 📘 | `w1a_course_orientation` | this README · `assignments/final_project_brief.md` | — |
| Introduction to hyperspectral Earth observation | 📘 | `w1b_intro_hyperspectral_eo` | `10_spectral_signatures_and_libraries.ipynb` (§1–2) | `quizzes/quiz_w1a_intro_spectral_signatures.md` |
| Spectral signatures, sensor concepts, and use cases | 📘 | `w1c_spectral_signatures_sensors` | `10_spectral_signatures_and_libraries.ipynb` | `quizzes/quiz_w1a_…` |
| Hyperspectral data access, visualization, and exploration | 🔧 | `w1d_data_access_exploration` | `00_EO_data_quickstart_notebook.ipynb` (Mon, skim the Sentinel-2 half) + theme notebooks `01`–`06` (Wed); `09_numpy_for_hyperspectral.ipynb` as pre-work | `exercises/ex_00_…`, `exercises/ex_01`–`ex_06` |
| Preprocessing concepts for hyperspectral data | 📘🔧 | `w1e_preprocessing` | `11_preprocessing.ipynb` | `quizzes/quiz_w1b_preprocessing.md` · **`assignments/assignment_w1_scene_exploration.md`** |

*Every week runs **Monday to Thursday** — there are no Friday sessions. A 2-hour **field spectrometer session**
sits on Tuesday 3 Nov alongside notebook 10; see `teaching_plan.md` for the run sheet.*

### Week 2 · 9–12 Nov 2026 (online)

| Session | Type | Slides | Notebook(s) | Exercises / quiz / assignment |
|---------|:----:|--------|-------------|-------------------------------|
| Hyperspectral image processing workflows | 📘🔧 | `w2a_processing_workflows` | `12_processing_workflow.ipynb` · `hsi_utils.py` | "Your turn" in notebook |
| Feature extraction and dimensionality reduction | 📘 | `w2b_feature_extraction` | `13_feature_extraction_dim_reduction.ipynb` | `quizzes/quiz_w2_features_detection_classification.md` |
| Material discrimination and target detection | 📘🔧 | `w2c_material_discrimination_detection` | `14_material_discrimination_target_detection.ipynb` | "Your turn" in notebook |
| Classification approaches for hyperspectral data | 📘🔧 | `w2d0_ml_primer_for_eo` (20 min) + `w2d_classification` | `15_classification_classical.ipynb` | **`assignments/assignment_w2_detection_classification.md`** |
| Project scoping and use case definition | 🔧 | `w2e_project_scoping` | `16_scene_finder.ipynb` | `templates/project_scoping_template.md` |
| *(optional extra day)* Hyperspectral data in HyperCoast and QGIS | 📘🔧 | `wx_qgis_hypercoast` | `17_hypercoast_tanager_enmap.ipynb` + `qgis_lab_hyperspectral.md` | "Your turn" in notebook |

### Week 3 · 16–19 Nov 2026 (online)

| Session | Type | Slides | Notebook(s) | Exercises / quiz / assignment |
|---------|:----:|--------|-------------|-------------------------------|
| GeoAI methods for hyperspectral applications | 📘 | `w3a_geoai_methods` | `20_geoai_deep_learning.ipynb` (§ overview) | `quizzes/quiz_w3_geoai_validation.md` |
| AI-assisted hyperspectral classification and mapping | 🔧 | `w3b_ai_assisted_mapping` | `20_geoai_deep_learning.ipynb` | "Your turn" in notebook |
| Validation methods and accuracy assessment | 📘🔧 | `w3c_validation_accuracy` | `21_validation_accuracy_assessment.ipynb` | `quizzes/quiz_w3_…` |
| Applied project development workshop | 🔧 | `w3d_project_workshop_qa` | `templates/project_template.ipynb` | **`assignments/assignment_w3_validated_map.md`** |
| Interim project feedback and quality assurance | 📘🔧 | `w3d_project_workshop_qa` | — | `templates/interim_qa_checklist.md` |

### Week 4 · 23–26 Nov 2026 (onsite and online)

| Session | Type | Slides | Notebook(s) | Exercises / quiz / assignment |
|---------|:----:|--------|-------------|-------------------------------|
| Advanced hyperspectral analytics and solution refinement | 📘🔧 | `w4a_advanced_analytics` | `30_advanced_analytics.ipynb` | "Your turn" in notebook |
| Final project implementation and testing | 🔧 | `w4b_implementation_and_testing` | `31_from_notebook_to_product.ipynb` · `app/streamlit_app.py` · `tests/` | — |
| Presentation preparation and project rehearsal | 🔧 | `w4c_presentation_and_evaluation` | — | `templates/presentation_template.md` |
| Final graduation project submission | 🔧 | `w4c_presentation_and_evaluation` | — | `templates/submission_checklist.md` |
| Final evaluation and feedback | 📘 | `w4c_presentation_and_evaluation` | — | `templates/evaluation_rubric.md` |

**Assessment:** assignment W1 10 % · W2 15 % · W3 15 % · final project 60 % (see `assignments/final_project_brief.md`).
Quizzes are formative and ungraded.

---

## Folder structure

```
hyperspectral_course_notebooks/
├── README.md                     ← the participant handbook (the repository front page)
├── INSTRUCTOR.md                 ← you are here
├── requirements.txt
├── .gitignore                    ← keeps scenes, outputs and decks out of git
├── hsi_utils.py                  ← shared helpers used by every notebook (read it, it is documented)
│
├── 09_numpy_for_hyperspectral.ipynb             Week 1 (optional on-ramp for the Python/numpy gap)
├── 10_spectral_signatures_and_libraries.ipynb   Week 1
├── 11_preprocessing.ipynb                       Week 1
├── 12_processing_workflow.ipynb                 Week 2
├── 13_feature_extraction_dim_reduction.ipynb    Week 2
├── 14_material_discrimination_target_detection.ipynb   Week 2
├── 15_classification_classical.ipynb            Week 2
├── 16_scene_finder.ipynb                        Week 2
├── 17_hypercoast_tanager_enmap.ipynb            Week 2 (optional session, pairs with the QGIS lab)
├── 20_geoai_deep_learning.ipynb                 Week 3
├── 21_validation_accuracy_assessment.ipynb      Week 3
├── 30_advanced_analytics.ipynb                  Week 4
├── 31_from_notebook_to_product.ipynb            Week 4
│
├── teaching_plan.md  ← day-by-day plan: which deck, notebook and homework per session
├── qgis_lab_hyperspectral.md  ← 3-hour desktop lab (EnMAP-Box + HyperCoast plugin)
│
├── slides/           18 PowerPoint decks (one per session) + figures/ extracted from the notebooks
├── exercises/        ex_00 … ex_06 for the theme notebooks (+ solutions/, instructor copy)
├── quizzes/          four lecture quizzes (+ answers/, instructor copy)
├── assignments/      weekly assignments + final project brief
├── templates/        scoping canvas, project notebook, QA checklist, submission checklist, rubric, slides
├── app/              mangrove_product.py (the example product + CLI) · streamlit_app.py (viewer)
├── tests/            test_hsi_utils.py — 23 pytest tests (`pytest tests/ -q`, ~1 s)
├── tools/            build_reference_library.py · make_subsets.py · export_for_qgis.py ·
│                     extract_figures.py · figures_w1b.py · deckbuild.py + decks/
│                     lint_decks.py · preview_deck.py
├── data/
│   ├── labels/                    ESA WorldCover 2021 labels aggregated to each Tanager grid (class + purity)
│   ├── enmap/                     EnMAP L2A subset over Groningen + official METADATA.XML (23 MB)
│   ├── spectral_library/          19 image-derived reference spectra (median, p10, p90) + metadata
│   └── tanager_catalog_index.geojson   index of all 276 Tanager open-data STAC items
└── outputs/          created by the notebooks (GeoTIFFs, reports); safe to delete
```

## Slides

`slides/` holds **19 PowerPoint decks** (515 slides in total) — one per syllabus session, plus a short ML primer, each with
**speaker notes** on every content slide and figures lifted straight from the executed notebooks, so what you
show matches what students run.

- Rebuild or edit them in Python: `python tools/decks/deck_<name>.py` (the scripts are readable and diffable).
- Restyle the whole course by changing the palette at the top of `tools/deckbuild.py`, or simply apply your
  own PowerPoint theme to the generated files — they are ordinary `.pptx`.
- `python tools/extract_figures.py` refreshes `slides/figures/` (151 figures, indexed in `figures/index.md`).
- `python tools/figures_w1b.py` rebuilds the six figures that session 2 draws itself — the data cube,
  summarise-vs-sample, the annotated leaf spectrum, the mission landscape, the trade-off and the theme
  fingerprints. They live in `slides/figures/w1b/` and exist because the notebook-derived figures for that
  topic belong to session 3; run it before rebuilding `deck_w1b_intro_hyperspectral.py`.
- `python tools/preview_deck.py slides/<deck>.pptx` renders a deck to PNG contact sheets in
  `slides/previews/` so you can check layout without opening PowerPoint.
- `python tools/lint_decks.py` checks every deck for overflowing text, oversized tables and missing notes.

## Data

The notebooks use seven Tanager scenes. `hsi_utils.get_scene(scene_id)` looks for the HDF5 file in
`$TANAGER_DATA_DIR`, `data/`, `../Starting_notebooks/` (where the theme notebooks and their scenes live) and the current folder,
and **downloads it from Planet's STAC catalogue if it is missing** (~1 GB per scene).

| Scene ID | Place | Used for | In `../Starting_notebooks`? |
|----------|-------|----------|:------------------:|
| `20241215_185916_33_4001` | Malibu, California: Franklin fire scar | fire, change detection | ✅ |
| `20250123_185518_92_4001` | Santa Monica Mountains: after the Palisades fire | change detection (notebook 30) | ⬇️ downloaded on first use (1.3 GB) |
| `20250219_053251_31_4001` | Korba / Kusmunda coal mines, India | minerals, target detection, GHG | ✅ |
| `20250223_165546_32_4001` | Usulután, El Salvador: mangroves and estuary | classification, GeoAI, validation | ✅ |
| `20250407_035509_25_4001` | Ho Chi Minh City, Vietnam | urban, target detection | ✅ |
| `20250511_074311_00_4001` | Al Dhafra coast, UAE: sabkha and shallow water | preprocessing (mask QA), water | ✅ |
| `20250608_091605_90_4001` | Konya, Türkiye: irrigated agriculture | features, workflows | ✅ |

**Smaller files for online sessions:** `python tools/make_subsets.py` cuts 256 × 256 pixel windows (~30 MB each)
into `data/subsets/`. `get_scene()` uses a subset only when the full scene is not available. Subset pixel
coordinates start at the window corner, so notebooks with hard-coded windows need the full scenes.

**Reference labels:** `data/labels/<scene>_worldcover2021_30m.tif` holds, per 30 m pixel, the majority ESA WorldCover
2021 class of its nine 10 m cells (band 1) and how many of the nine agree (band 2, "purity"). WorldCover is from
2021 and the images from 2024–2025, so the labels contain some real change and error. The notebooks use this
deliberately to teach label noise. Regenerate or extend the labels with `hu.make_worldcover_labels(scene)`
(needs internet).

**Reference spectral library:** `data/spectral_library/` holds 19 median spectra of homogeneous areas (mangrove,
irrigated crop, sabkha, burn scar, coal-mine surface, industrial roof, …) selected with WorldCover purity and simple
spectral rules. Rebuild it with `python tools/build_reference_library.py`. For laboratory spectra, see the USGS
Spectral Library v7 (`hu.load_usgs_ascii`, notebook 10).

## Getting started

```bash
cd hyperspectral_course_notebooks
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Open `10_spectral_signatures_and_libraries.ipynb`. Notebooks import `hsi_utils` from the same folder. On
**Google Colab**, upload `hsi_utils.py` (and the `data/` folder, if you need labels or the library) next to the
notebook, and run the `%pip install` line in the setup cell.

**Behind a corporate proxy?** If downloads fail with `SSL: CERTIFICATE_VERIFY_FAILED`, point Python and GDAL
to your organisation's CA bundle: `export REQUESTS_CA_BUNDLE=/path/ca.pem GDAL_CURL_CA_BUNDLE=/path/ca.pem`.

## Instructor notes

- **Publishing this repository.** `tools/set_repo_url.py <owner>/<repo>` rewrites every Colab badge and
  bootstrap cell in one go — run it once after creating the repository, then commit. `.gitignore` already keeps
  out the 1 GB scenes, `outputs/`, and the 46 MB of slide decks; the decks regenerate with
  `python tools/extract_figures.py` followed by the scripts in `tools/decks/`. Attach them to a GitHub Release
  if participants need them.
- **Check your scenes are really on disk.** In a OneDrive folder they can exist as 0-byte placeholders, and the
  first notebook run then stalls on a multi-gigabyte rehydration. In Finder: right-click the folder →
  *Always Keep on This Device*.
- **`outputs/` is example output** (93 MB), including the QGIS exports the lab uses. Delete it for a lean copy;
  the notebooks and `tools/export_for_qgis.py` regenerate everything.
- **The QGIS lab's GUI steps are written from the EnMAP-Box 3.17 / QGIS 3.40 documentation but were not
  clicked through on the build machine** (the network blocked every QGIS download). The data side *is* verified.
  Walk it once before teaching and add screenshots where marked.
- **Solutions and answer keys** are in `exercises/solutions/` and `quizzes/answers/`. Remove these folders
  before sharing the material with students if you want to release them later.
- The course notebooks ship **with outputs**, so students can read them before running them. The exercise student
  versions ship without outputs.
- Every notebook runs offline once the scenes are local, except `16_scene_finder.ipynb` (thumbnails, catalogue
  refresh), label regeneration, the methane box in notebook 14, and the optional cells flagged in the notebooks.
- Measured runtimes on a laptop CPU (10 cores, no GPU): notebooks 10–16, 21, 31 take 12 s – 1.5 min each;
  `30_advanced_analytics` 1.5 min (plus a one-off 1.3 GB download of the January Malibu scene);
  `20_geoai_deep_learning` about 6 minutes (it trains two small CNNs and runs tiled inference over a full scene).
- Everything was executed end to end before release: every notebook here ships with its outputs and no errors,
  and `pytest tests/ -q` passes (23 tests).
- **Results the notebooks are built around** (useful when planning a session):
  - 15 / 20: on El Salvador land cover, macro-F1 rises 0.861 (random forest) → 0.892 (1D-CNN) → 0.925 (patch CNN),
    but the same model scores ~0.3 on Ho Chi Minh City — the domain-shift lesson.
  - 15: the full 352-band spectrum barely beats simulated Sentinel-2 for broad land cover (0.912 vs 0.909);
    the hyperspectral gain shows up in the narrow-band work of notebooks 13 and 14 instead.
  - 14: in the implanted-target test, ACE detects 55 % of 10 %-fill targets at a 1 % false-alarm rate, SAM ~1 %.
  - 30: the December→January Malibu pair recovers the new (Palisades) burn scar, ~2 500 ha, and the refinement
    chain cuts false alarms from 4.7 % to 0 % while keeping ~90 % of the scar.
  - 11 / 16: Tanager's cloud mask has false positives over bright desert — Al Dhafra, Riyadh and Al Mahrah are all
    flagged 50–75 % "cloud" under a clear sky. Several notebooks therefore read those scenes with `cloud=False`.

- **Known issues in the theme notebooks (`../Starting_notebooks`)** were left untouched on purpose:
  - `06_ecosystem_health_water_qualityy.ipynb` (filename typo) is still largely a copy of `05`: same scenes and
    indices, and the figure title still reads "Ecosystem Health & Blue Carbon". The water-quality exercises in
    `exercises/ex_06_…` add the missing water masking and FAI.
  - `05` lists `20250223_165546_32_4001` twice in `item_ids`.
  - The theme README describes the `02` scene as Riyadh, but it is Ho Chi Minh City. It also refers to
    `00_data_exploration_starter.ipynb` and a `docs/` folder that do not exist.

## Data credits

- Tanager: *"Tanager STAC Data, available at www.planet.com/data/stac © 2025 Planet Labs PBC"*, CC-BY-4.0
  (use the acquisition year of each scene).
- ESA WorldCover 10 m 2021 v200, © ESA WorldCover project / contains modified Copernicus Sentinel data (2021),
  CC-BY 4.0, accessed via Microsoft Planetary Computer.
