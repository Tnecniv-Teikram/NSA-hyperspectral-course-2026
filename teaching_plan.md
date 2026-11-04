# Teaching plan — how the material fills the days

**Space Academy 2026 · Hyperspectral course · 3–25 November 2026**

**Audience assumed:** experienced in multispectral EO, new to hyperspectral and new to GeoAI/ML, mixed Python
ability. Two short on-ramps exist for exactly that profile and are built into the plan below:
`09_numpy_for_hyperspectral.ipynb` (pre-work) and the `w2d0_ml_primer_for_eo` deck (20 minutes before the first
classification session).

This plan answers one question: *is a notebook enough for a day of teaching?*

**No — one notebook is the practical core of a session, not a whole day.** Measured across the eleven
course notebooks, a guided walkthrough takes **0.8–1.6 h** of pure reading and running, which becomes
**2–3 h** in a classroom once you stop for questions and let people type. The built-in exercises add
**0.5–1 h**, and notebook 30 alone is closer to a day and a half.

A teaching day therefore looks like this:

| Block | Duration | Material |
|-------|----------|----------|
| Lecture | 1.5–2 h | the session's `slides/*.pptx` deck (26–36 slides, with speaker notes) |
| Practical | 2–2.5 h | the session's notebook, walked through together |
| Exercises / project | 1.5–2 h | the notebook's "Your turn", `exercises/`, or project work |
| **Total** | **5.5–6.5 h** | |

---

## Week 1 · 2–5 Nov (onsite and online) — five sessions in four days

The only week where everyone is in the room together, so it carries the two things that need a room: the
spectrometer session and the first hands-on setup.

| Day | Sessions | Lecture | Practical | Homework |
|-----|----------|---------|-----------|----------|
| **Mon 2 Nov** | Orientation · Introduction to hyperspectral EO | `w1a_course_orientation.pptx` (22) · `w1b_intro_hyperspectral_eo.pptx` (20) | Environment setup (see below); `00_EO_data_quickstart_notebook.ipynb` (skim the Sentinel-2 half) | `exercises/ex_00_data_exploration.ipynb` · quiz W1a · **`09_numpy_for_hyperspectral.ipynb` for anyone not fluent in numpy** |
| **Tue 3 Nov** | Spectral signatures, sensor concepts and use cases | `w1c_spectral_signatures_sensors.pptx` (31) | `10_spectral_signatures_and_libraries.ipynb` (90 min) · **field spectrometer session (2 h — see below)** | finish notebook 10's "Your turn" |
| **Wed 4 Nov** | Hyperspectral data access, visualization and exploration | `w1d_data_access_exploration.pptx` (22) | one or two theme notebooks `01`–`06`, chosen by interest; then load yesterday's field spectra and overlay them on the course library | the matching `exercises/ex_01`–`ex_06` |
| **Thu 5 Nov** | Preprocessing concepts | `w1e_preprocessing.pptx` (35) | `11_preprocessing.ipynb` (2–2.5 h — the fullest notebook of the week) | quiz W1b · start **assignment W1** (due Mon 9 Nov) |

**If you are short of time:** shorten Wednesday to a single theme notebook rather than cutting preprocessing,
which everything later depends on. Wednesday is also the natural buffer if the weather forced the spectrometer
session to move.

### Monday's setup session — run it Colab-first

Setup is the one thing that can quietly cost you half of week 1, and the corporate network makes it worse:
TLS interception breaks `pip` and GDAL without a CA bundle, and qgis.org, the OSGeo mirrors and the conda
channel are all blocked from inside. Sequence the morning so nobody is stuck:

1. **Everyone on Colab first (15 min).** Open the repository README, click the Colab badge on
   `09_numpy_for_hyperspectral`, run the first cell. It clones the course and installs what Colab lacks. This
   works on any laptop with a browser and gives the whole room an identical environment, so the rest of the day
   can start on time.
2. **Local installs in parallel, with you in the room.** Anyone who wants a local environment follows the
   README's Option 2. Do this onsite in week 1 — it is the only week you can hand over the CA-bundle fix in
   person. Keep the environment out of OneDrive.
3. **Hand out the QGIS installer on a USB stick.** The desktop session later needs QGIS 3.40 or 3.44 LTR plus
   the EnMAP-Box plugin, and the download is blocked on this network. Distribute it physically while everyone
   is in the room, and have them install the plugin before they leave.
4. **Warn about scene downloads.** Each Tanager scene is about 1 GB. On Colab they come from Google Cloud
   Storage and arrive in a couple of minutes; on a laptop over hotel wifi they do not. Participants working
   locally should pull the scenes they need before the online weeks begin.

### Field spectrometer session — Tuesday 3 Nov, ~11:30–13:30

This is the right day for it: the morning lecture and notebook 10 are about spectral signatures, absorption
features, FWHM and spectral sampling, and the spectrometer makes all of it physical. Run it **near solar noon**
(roughly 10:00–14:00) so illumination is stable between targets; if the forecast is poor, swap it with the
notebook block rather than moving it to another day.

| Minutes | Block |
|---|---|
| 0–20 | Instrument tour: fore-optic and field of view, integration time, what the instrument actually records (counts, not reflectance) |
| 20–35 | **White reference** — measure the panel, then a target; repeat the panel measurement after ten minutes and watch the spectrum drift. This *is* the radiance-to-reflectance step they meet on Wednesday morning |
| 35–95 | Measure in pairs: vegetation (sunlit and shaded leaves of the same plant), bare soil, concrete or a bright roof, water, and one mineral or sand target. Three replicates each, panel re-measured between targets |
| 95–110 | Metadata discipline: target, time, sun angle, panel time, photo, GPS — and why a spectrum without metadata is worthless later |
| 110–120 | Back inside: load the spectra, overlay them on the course library (`data/spectral_library/`), and identify the same absorption features they annotated in notebook 10 |

**Three things that make it stick**

1. **Measure what the satellite scenes contain.** Vegetation, soil, built material, water and a mineral target are
   the same classes as the course reference library, so the overlay in notebook 10 §2 is a direct comparison of
   their measurement with Tanager's.
2. **The white reference is the lesson, not the chore.** A deliberately stale calibration shows why atmospheric
   correction exists before Wednesday's lecture claims it.
3. **Resample their own spectra to the satellites.** `hu.resample_to_sensor()` convolves a ~1 nm field spectrum to
   Tanager (5 nm), EnMAP (~10 nm) and Sentinel-2 — watching their own measured absorption feature vanish into
   Sentinel-2's 175 nm SWIR band is the most convincing version of the course's central argument.

The spectra are worth keeping: they serve as reference signatures for the SAM and matched-filter work in
`14_material_discrimination_target_detection` the following week, which turns a field afternoon into data the
projects keep using.

---

## Week 2 · 9–12 Nov (online) — four days, five sessions

| Day | Session | Lecture | Practical | Homework |
|-----|---------|---------|-----------|----------|
| **Mon 9** | Image processing workflows | `w2a_processing_workflows.pptx` (29) | `12_processing_workflow.ipynb` | assignment W1 due |
| **Tue 10** | Feature extraction and dimensionality reduction | `w2b_feature_extraction.pptx` (36) | `13_feature_extraction_dim_reduction.ipynb` | quiz W2 |
| **Wed 11** | Material discrimination and target detection | `w2c_material_discrimination_detection.pptx` (36) | `14_material_discrimination_target_detection.ipynb` — use the field spectra from Week 1 as extra reference signatures | — |
| **Thu 12** | Classification approaches · Project scoping and use case definition | morning: **`w2d0_ml_primer_for_eo.pptx` (20 min)** then `w2d_classification.pptx` (34) · afternoon: `w2e_project_scoping.pptx` (22) | morning: `15_classification_classical.ipynb` (start at its §0 translation table) · afternoon: `16_scene_finder.ipynb` + fill in `templates/project_scoping_template.md` | **assignment W2** issued · scoping canvas due Mon 16 |

Thursday is the heaviest day of the week: a full morning of classification and an afternoon of team scoping. Keep
the afternoon genuinely hands-off — the teams need time to argue about their own problem, not more slides.

**Optional extra session — QGIS and HyperCoast.** If your timetable gains a day, insert
`17_hypercoast_tanager_enmap.ipynb` plus `qgis_lab_hyperspectral.md` after Tuesday. Otherwise offer it as
self-study; it is the most self-contained material in the course.

---

## Week 3 · 16–19 Nov (online) — four days, five sessions

| Day | Session | Lecture | Practical | Homework |
|-----|---------|---------|-----------|----------|
| **Mon 16** | GeoAI methods | `w3a_geoai_methods.pptx` (40) — includes the "how a network actually learns" mechanics section | reading + the lecture sections of `20_geoai_deep_learning.ipynb` | quiz W3 · scoping canvas due |
| **Tue 17** | AI-assisted classification and mapping | `w3b_ai_assisted_mapping.pptx` (22) | `20_geoai_deep_learning.ipynb` — training and inference (allow ~6 min runtime on CPU) | — |
| **Wed 18** | Validation and accuracy assessment | `w3c_validation_accuracy.pptx` (34) | `21_validation_accuracy_assessment.ipynb` | **assignment W3** issued |
| **Thu 19** | Applied project development workshop · Interim project feedback and QA | `w3d_project_workshop_qa.pptx` (22) — part 1 in the morning, part 2 before the reviews | morning: teams work, instructors circulate (`templates/project_template.ipynb`) · afternoon: peer review with `templates/interim_qa_checklist.md`, then 10-minute interim presentations | assignment W3 due at the review |

Thursday carries both the workshop and the interim review. That pairing works — teams fix things in the morning
and present what they have in the afternoon — but it only works if you protect the morning from lecturing.

---

## Week 4 · 23–26 Nov (onsite and online) — five sessions in four days

| Day | Sessions | Lecture | Practical | Notes |
|-----|----------|---------|-----------|-------|
| **Mon 23** | Advanced analytics and solution refinement | `w4a_advanced_analytics.pptx` (28) | `30_advanced_analytics.ipynb` — **split it over the day**: change detection before lunch, uncertainty + harmonisation + scaling after | the biggest notebook of the course; it now has a whole day, so use it |
| **Tue 24** | Final project implementation and testing | `w4b_implementation_and_testing.pptx` (25) | `31_from_notebook_to_product.ipynb` in the morning; teams implement and test their own pipeline after lunch | `templates/submission_checklist.md` issued |
| **Wed 25** | Presentation preparation and project rehearsal | `w4c_presentation_and_evaluation.pptx` (21, part 1) | teams build slides and rehearse; instructors give feedback on structure and on the validation story | `templates/presentation_template.md` |
| **Thu 26** | Final graduation project submission · Final evaluation and feedback | `w4c_…` (part 2) | submissions in the morning; final presentations after lunch (12 min + 5 min questions), scored with `templates/evaluation_rubric.md`, then the feedback round | submissions close before the presentations start |

Giving rehearsal its own day on Wednesday is the main gain from the four-day week: in the previous three-day
version, teams built slides and presented within 24 hours, and the validation story was always the casualty.

---

## Notebook sizing at a glance

| Notebook | Walkthrough | Exercises | Fits a session? |
|----------|------------:|----------:|-----------------|
| `09_numpy_for_hyperspectral` | ~0.8 h | 5 | pre-work, not a session |
| `10_spectral_signatures_and_libraries` | ~0.8 h | 7 | yes — leaves the afternoon for the spectrometer |
| `11_preprocessing` | ~1.1 h | 6 | yes — a full one |
| `12_processing_workflow` | ~0.9 h | 4 | yes |
| `13_feature_extraction_dim_reduction` | ~1.2 h | 3 | yes — a full one |
| `14_material_discrimination_target_detection` | ~1.2 h | 6 | yes — a full one |
| `15_classification_classical` | ~0.9 h | 4 | yes |
| `16_scene_finder` | ~0.8 h | 3 | yes, leaves room for the scoping canvas |
| `17_hypercoast_tanager_enmap` | ~0.9 h | 5 | pairs with the QGIS lab to make one day |
| `20_geoai_deep_learning` | ~1.1 h + 6 min compute | 6 | spans two sessions (lecture + practical) |
| `21_validation_accuracy_assessment` | ~1.0 h | 4 | yes |
| `30_advanced_analytics` | ~1.6 h | 6 | **no — split across two half-days** |
| `31_from_notebook_to_product` | ~0.7 h | 5 | yes, leaves room for team work |

## Preparation checklist for the instructor

- [ ] **Ask participants about Python before week 1.** One question is enough: *can you read and adapt numpy array
      code (slicing, axes, boolean masks)?* Anyone who hesitates should work through
      `09_numpy_for_hyperspectral.ipynb` before Tuesday of week 1 — it is the difference between following the
      course and watching it.
- [ ] Run the `w2d0_ml_primer_for_eo` deck before the first classification practical, even if the room looks
      confident. The vocabulary (features, labels, train/test, overfitting, hyperparameters) is assumed by every
      notebook from 15 onwards.

- [ ] **Publish the repository before week 1** and check that a Colab badge actually opens
      (`python tools/set_repo_url.py <owner>/<repo>` first). Test it from a machine that is *not* yours.
- [ ] Scenes downloaded on every machine before the session (1 GB each; `tools/make_subsets.py` cuts 30 MB
      versions for laptops or weak connections).
- [ ] `pip install -r requirements.txt` verified on the room's machines — including `torch` before Week 3
      and `hypercoast` (Python ≥ 3.11) before the QGIS session.
- [ ] Notebook 20 run once in advance on the teaching machine: 6 minutes on CPU is fine to show live, but not
      to discover for the first time in front of a class.
- [ ] Decks reviewed and rebranded (`tools/decks/*.py` regenerate them; the palette lives in `tools/deckbuild.py`).
- [ ] Quiz answer keys (`quizzes/answers/`) and exercise solutions (`exercises/solutions/`) removed from the
      student copy if you want to release them later.
- [ ] **For the field spectrometer session (Tue 3 Nov):** charge batteries and check the instrument the day
      before; bring the white reference panel, a spare, and something to shade the laptop screen; check the
      forecast on Monday and be ready to swap the morning and afternoon blocks; agree the target list in advance
      so the measurements map onto the course library classes.
- [ ] For the QGIS session: QGIS 3.40 LTR or newer installed **with the EnMAP-Box plugin**, and the exports from
      `tools/export_for_qgis.py` copied to a local disk (not a synced OneDrive folder — GDAL is slow over it).
