# Teaching plan — how the material fills the days

**Space Academy 2026 · Hyperspectral course · 9–26 November 2026 · three weeks, Monday to Thursday**

| Week | Dates | Sessions |
|------|-------|:--------:|
| 1 | Mon 9 – Thu 12 Nov | 6 |
| 2 | Mon 16 – Thu 19 Nov | 5 |
| 3 | Mon 23 – Thu 26 Nov | 4 |

**Audience assumed:** experienced in multispectral EO, new to hyperspectral and new to GeoAI/ML, mixed Python
ability. Two short on-ramps exist for exactly that profile: `09_numpy_for_hyperspectral.ipynb` (pre-work) and
the `w2d0_ml_primer_for_eo` deck (20 minutes before the first classification session).

**Assessment is the mini project, and nothing else.** It is introduced on day one, scoped in week 2, built
through week 3 and presented in the final session. The quizzes are formative and ungraded. The three weekly
assignment briefs in `assignments/` are **not used** in this three-week run — they are kept in the repository
for a future longer course.

A teaching day looks like this:

| Block | Duration | Material |
|-------|----------|----------|
| Lecture | 1.5–2 h | the session's `slides/*.pptx` deck (20–40 slides, with speaker notes) |
| Practical | 2–2.5 h | the session's notebook, walked through together |
| Exercises / project | 1.5–2 h | the notebook's "Your turn", `exercises/`, or mini-project work |
| **Total** | **5.5–6.5 h** | |

---

## Week 1 · Mon 9 – Thu 12 Nov — six sessions in four days

The densest week: two of the four days carry two sessions. Monday's pair is largely administrative, and
Tuesday's pair is two lectures served by a single practical, so both work — but Monday and Tuesday have no
slack, and setup problems are what eat it.

| Day | Sessions | Lecture | Practical | Homework |
|-----|----------|---------|-----------|----------|
| **Mon 9 Nov** | 1. Kickoff, opening speech, course orientation and objectives · 2. Course objectives + mini project, introduction to the gIQ platform and the course platform | `w1a_course_orientation.pptx` (22) · *session 2 is run by its own presenter — no deck in this repository* | Environment setup, Colab-first (see below) | **`09_numpy_for_hyperspectral.ipynb` for anyone not fluent in numpy** |
| **Tue 10 Nov** | 3. Introduction to hyperspectral Earth observation · 4. Spectral signatures, sensor concepts and hyperspectral use cases | `w1b_intro_hyperspectral_eo.pptx` (23) · `w1c_spectral_signatures_sensors.pptx` (31) | `10_spectral_signatures_and_libraries.ipynb` — it serves both lectures | quiz W1a · finish notebook 10's "Your turn" |
| **Wed 11 Nov** | 5. Hyperspectral data access, visualization and exploration | `w1d_data_access_exploration.pptx` (22) | `00_EO_data_quickstart_notebook.ipynb` (skim the Sentinel-2 half), then one or two theme notebooks `01`–`06` chosen by interest | the matching `exercises/ex_01`–`ex_06` · **pick your mini-project theme** |
| **Thu 12 Nov** | 6. Preprocessing concepts for hyperspectral data | `w1e_preprocessing.pptx` (35) | `11_preprocessing.ipynb` — the fullest notebook of the week | quiz W1b |

**If Monday overruns,** push the environment setup into Tuesday morning rather than cutting into notebook 10.
Setup is the one thing that can quietly cost half a week, and Wednesday is the natural buffer: a single theme
notebook teaches the same lesson as two.

### Monday's setup session — run it Colab-first

Sequence the morning so nobody is stuck:

1. **Everyone on Colab first (15 min).** Open the repository README, click the Colab badge on
   `09_numpy_for_hyperspectral`, run the first cell. It clones the course and installs what Colab lacks. This
   works on any laptop with a browser and gives the whole room an identical environment.
2. **Local installs in parallel, with you in the room.** Anyone who wants a local environment follows the
   README's Option 2. Do it while you can hand over the CA-bundle fix in person.
3. **Warn about scene downloads.** About 1 GB each. On Colab they come from Google Cloud Storage in a couple of
   minutes; on hotel wifi they do not. Participants working locally should pull what they need in advance.

### Optional: field spectrometer session

Not one of the fifteen sessions, so it is not scheduled above. If you do run it, **Tuesday 10 November** is the
day — the lectures that morning are about spectral signatures, absorption features and spectral sampling, and
the instrument makes all of it physical. Run it near solar noon so illumination is stable between targets.

| Minutes | Block |
|---|---|
| 0–20 | Instrument tour: fore-optic and field of view, integration time, what the instrument records (counts, not reflectance) |
| 20–35 | **White reference** — measure the panel, then a target; repeat the panel after ten minutes and watch the spectrum drift. This *is* the radiance-to-reflectance step |
| 35–95 | Measure in pairs: vegetation (sunlit and shaded leaves of the same plant), bare soil, concrete or a bright roof, water, one mineral or sand target. Three replicates each, panel re-measured between targets |
| 95–110 | Metadata discipline: target, time, sun angle, panel time, photo, GPS — and why a spectrum without metadata is worthless later |
| 110–120 | Back inside: load the spectra, overlay them on `data/spectral_library/`, identify the same absorption features |

---

## Week 2 · Mon 16 – Thu 19 Nov — five sessions in four days

The method week. Thursday carries two sessions, which works because the afternoon one is a workshop rather
than a lecture.

| Day | Session | Lecture | Practical | Homework |
|-----|---------|---------|-----------|----------|
| **Mon 16 Nov** | 7. Hyperspectral image processing workflows | `w2a_processing_workflows.pptx` (29) | `12_processing_workflow.ipynb` | — |
| **Tue 17 Nov** | 8. Feature extraction and dimensionality reduction | `w2b_feature_extraction.pptx` (36) | `13_feature_extraction_dim_reduction.ipynb` | quiz W2 |
| **Wed 18 Nov** | 9. Material discrimination and target detection | `w2c_material_discrimination_detection.pptx` (36) | `14_material_discrimination_target_detection.ipynb` | — |
| **Thu 19 Nov** | 10. Classification approaches for hyperspectral data · 11. Project scoping and use case definition | morning: **`w2d0_ml_primer_for_eo.pptx` (20 min)** then `w2d_classification.pptx` (34) · afternoon: `w2e_project_scoping.pptx` (22) | morning: `15_classification_classical.ipynb` (start at its §0 translation table) · afternoon: `16_scene_finder.ipynb`, then fill in `templates/project_scoping_template.md` | **mini-project scoping canvas due Mon 23** |

---

## Week 3 · Mon 23 – Thu 26 Nov — four sessions in four days

The lightest week by session count, deliberately: the mini project has to be built somewhere, and this is
where the time comes from.

| Day | Session | Lecture | Practical | Project |
|-----|---------|---------|-----------|---------|
| **Mon 23 Nov** | 12. GeoAI methods for hyperspectral applications | `w3a_geoai_methods.pptx` (40) — includes the "how a network actually learns" mechanics section | reading plus the lecture sections of `20_geoai_deep_learning.ipynb` | **scoping canvas due** · quiz W3 |
| **Tue 24 Nov** | 13. AI-assisted hyperspectral classification and mapping | `w3b_ai_assisted_mapping.pptx` (22) | `20_geoai_deep_learning.ipynb` — training and inference (~6 min runtime on CPU) | teams apply the method to their own scene |
| **Wed 25 Nov** | 14. Validation methods and accuracy assessment | `w3c_validation_accuracy.pptx` (34) | `21_validation_accuracy_assessment.ipynb` in the morning | **afternoon is project build time** — instructors circulate, `templates/project_template.ipynb` |
| **Thu 26 Nov** | 15. Final graduation project submission and presentation | `w4c_presentation_and_evaluation.pptx` (21) | — | morning: finalise and submit (`templates/submission_checklist.md`) · afternoon: 12-minute presentations + 5 minutes of questions, scored with `templates/evaluation_rubric.md`, then the feedback round |

**The project has one scheduled build afternoon.** That is the main risk in this plan. Teams that have not
chosen a theme by Wednesday of week 1 and scoped it by Thursday of week 2 will not finish. Two levers if it
looks tight: give Tuesday 24 November's afternoon to project work as well, since notebook 20's practical
compresses comfortably, or shorten Wednesday's validation practical to its §1–4 and set §5 as reading.

---

## Material not taught in this run

Kept in the repository, unchanged, and worth pointing participants at:

| Material | Was | Now |
|---|---|---|
| `17_hypercoast_tanager_enmap.ipynb` + `qgis_lab_hyperspectral.md` + `wx_qgis_hypercoast.pptx` | optional extra day | self-study |
| `30_advanced_analytics.ipynb` + `w4a_advanced_analytics.pptx` | week 4 | self-study — change detection, uncertainty, scaling |
| `31_from_notebook_to_product.ipynb` + `w4b_implementation_and_testing.pptx` | week 4 | self-study — packaging, tests, the Streamlit app |
| `w3d_project_workshop_qa.pptx` + `templates/interim_qa_checklist.md` | week 3 workshop and interim review | not scheduled; the QA checklist is still a good self-check before submission |
| `assignments/assignment_w1`–`w3` | graded, 40 % between them | not used — the mini project is the whole assessment |

Tell participants on day one that these exist. The advanced analytics notebook in particular is the natural
next step for anyone who wants to go further after the course.

---

## Notebook sizing at a glance

| Notebook | Walkthrough | Exercises | Fits a session? |
|----------|------------:|----------:|-----------------|
| `09_numpy_for_hyperspectral` | ~0.8 h | 5 | pre-work, not a session |
| `10_spectral_signatures_and_libraries` | ~0.8 h | 7 | yes — serves both Tuesday lectures |
| `11_preprocessing` | ~1.1 h | 6 | yes — a full one |
| `12_processing_workflow` | ~0.9 h | 4 | yes |
| `13_feature_extraction_dim_reduction` | ~1.2 h | 3 | yes — a full one |
| `14_material_discrimination_target_detection` | ~1.2 h | 6 | yes — a full one |
| `15_classification_classical` | ~0.9 h | 4 | yes |
| `16_scene_finder` | ~0.8 h | 3 | yes, leaves room for the scoping canvas |
| `17_hypercoast_tanager_enmap` | ~0.9 h | 5 | self-study in this run |
| `20_geoai_deep_learning` | ~1.1 h + 6 min compute | 6 | spans two sessions (lecture + practical) |
| `21_validation_accuracy_assessment` | ~1.0 h | 4 | yes |
| `30_advanced_analytics` | ~1.6 h | 6 | self-study in this run |
| `31_from_notebook_to_product` | ~0.7 h | 5 | self-study in this run |

## Preparation checklist for the instructor

- [ ] **Ask participants about Python on day one.** One question is enough: *can you read and adapt numpy array
      code (slicing, axes, boolean masks)?* Anyone who hesitates should work through
      `09_numpy_for_hyperspectral.ipynb` before Tuesday 10 November — it is the difference between following the
      course and watching it.
- [ ] Run the `w2d0_ml_primer_for_eo` deck before the first classification practical, even if the room looks
      confident. The vocabulary (features, labels, train/test, overfitting, hyperparameters) is assumed by every
      notebook from 15 onwards.

- [ ] **Check a Colab badge actually opens**, from a machine that is *not* yours. The course is published at
      `github.com/Tnecniv-Teikram/NSA-hyperspectral-course-2026` and the theme notebooks `00`–`06` at
      `github.com/Tnecniv-Teikram/813-hyperspectral-hackathon`; participants use both.
- [ ] Scenes downloaded on every machine before the session (1 GB each; `tools/make_subsets.py` cuts 30 MB
      versions for laptops or weak connections).
- [ ] `pip install -r requirements.txt` verified on the room's machines — including `torch` before Monday 23 November
      and `hypercoast` (Python ≥ 3.11) for anyone taking the HyperCoast notebook as self-study.
- [ ] Notebook 20 run once in advance on the teaching machine: 6 minutes on CPU is fine to show live, but not
      to discover for the first time in front of a class.
- [ ] Decks reviewed and rebranded (`tools/decks/*.py` regenerate them; the palette lives in `tools/deckbuild.py`).
- [ ] Decide when to point participants at `quizzes/answers/` and `exercises/solutions/` — the repository is
      public, so they are available from day one.
- [ ] **If you run the optional field spectrometer session (Tue 10 Nov):** charge batteries and check the instrument the day
      before; bring the white reference panel, a spare, and something to shade the laptop screen; check the
      forecast on Monday and be ready to swap the morning and afternoon blocks; agree the target list in advance
      so the measurements map onto the course library classes.
- [ ] The QGIS lab is self-study in this run. Anyone attempting it needs QGIS 3.40 LTR or newer **with the
      EnMAP-Box plugin**, and the exports from `tools/export_for_qgis.py` on a local disk (not a synced OneDrive
      folder — GDAL is slow over it).
