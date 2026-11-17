# Mini project (one-week sprint) — brief

**Space Academy 2026 · Hyperspectral course** · teams of 3–5 · **Thu 19 Nov → Thu 26 Nov** · **100 % of the course grade**

This replaces the three-week project in [`final_project_brief.md`](final_project_brief.md). You get **one scene, one
question, one validated map and one page for a decision-maker**, built with AI tools in about a week.
Total effort: roughly **12–16 team hours** (3–4 hours per person in a team of four).

> **The idea in one sentence:** use what you learned in weeks 1–2 to answer *one* question about *one* scene,
> let AI assistants speed up the coding, and spend your saved time **checking that the answer is right**.

## What you build

A **validated map from one Tanager scene**, comparing three things:

| | What | Why |
|---|---|---|
| **A. Baseline** | a simple index or threshold (e.g. NDVI, NBR, a band ratio) | the thing to beat |
| **B. Multispectral view** | your best method restricted to Sentinel-2-like bands (`hsi_utils.resample_to_sensor`) | shows what the extra bands add (or don't) |
| **C. Hyperspectral AI model** | a classifier on the full good-band spectrum (random forest, or the 1D-CNN from notebook 20) | your main result |

Then you **validate all three on spatially independent reference data** and tell the decision-maker, in one page,
what they can trust and what they can't.

An honest result of "the baseline was nearly as good" is a **valid and good** finding if you show it properly.

## Pick a track

Every scene is already in the course, every one has ESA WorldCover labels on its grid, and each has an exercise
(`exercises/ex_0x_*.ipynb`) with a worked solution to start from. Reading the matching exercise solution is allowed
and encouraged — your job is a *different* question, a better validation, or both.

| # | Track | Scene | Example question | Start from |
|---|---|---|---|---|
| 1 | Agriculture | `20250608_091605_90_4001` Konya | Which areas are active irrigated crops vs bare/dry land? | `ex_01`, notebook 13 |
| 2 | Urban change | `20250407_035509_25_4001` Ho Chi Minh City | Where is built-up land vs vegetation vs water? | `ex_02` |
| 3 | Mines / GHG | `20250219_053251_31_4001` Korba | Which pixels are mine/bare surface vs vegetation? | `ex_03`, notebook 14 |
| 4 | Fire | `20241215_185916_33_4001` Malibu | Where is the burn scar, and how sure are we? | `ex_04` |
| 5 | Blue carbon | `20250223_165546_32_4001` El Salvador | Where are the mangroves? | `ex_05`, notebook 20 |
| 6 | Water / coast | `20250511_074311_00_4001` Al Dhafra | Where are water, bare ground and built-up along the coast? | `ex_06` |

Your own question inside the track is welcome. Your own scene is **not** part of the sprint, unless you tell an
instructor by Thursday 19 Nov, because finding and checking data would use most of your week.

**Labels.** Tracks 1, 2, 3, 5 and 6 use `hu.load_labels()` (WorldCover, 2021). Check which classes actually occur in
your window and merge them into **at most 4 classes**. The **fire** track has no burn class in WorldCover, so you
digitise **≥ 100 reference points** yourselves from a SWIR false-colour image, in at least 4 separate spatial
blocks. WorldCover is 2021, so label noise is part of the story: name it in your limitations.

## The AI part (required, and graded under Validity)

AI assistants are **encouraged**: Claude, ChatGPT, Gemini in Colab, Copilot, anything you like. Three rules:

1. **Give the assistant context.** Paste `hsi_utils.py`'s function list and `templates/project_template.ipynb` into the
   chat, so it uses the course's functions instead of inventing its own.
2. **Keep an AI use log** (a table at the end of your notebook, 5–10 rows):
   *prompt → what the AI produced → what you checked → what you changed or rejected.*
3. **You must be able to explain every line you submit**, and at the presentation anyone in the team may be asked.

**Check AI-written hyperspectral code for these classic mistakes** (this is where marks are won or lost):

- [ ] **Random pixel split.** Neighbouring pixels are near-identical, so a random split leaks. Split by spatial block.
- [ ] **Bad bands left in.** Water-vapour bands and the noisy edges must be removed (`read_cube(bands="good")`).
- [ ] **Wavelength vs band number.** "Band 50" is not 860 nm. Use `hu.band_index(wl, 860)`.
- [ ] **Invented function names.** If a `hypercoast` or `hsi_utils` call doesn't exist, the AI made it up; check the source.
- [ ] **Accuracy alone.** Overall accuracy hides a bad minority class. Report per-class precision/recall and the confusion matrix.
- [ ] **Clouds and nodata** used as training pixels.
- [ ] **A "great" score that appeared at the first attempt.** Be suspicious; look for leakage before you celebrate.

## Day plan

Sessions stay as in the course timetable. The sprint runs *inside* them plus your own time.

| When | Goal | Output |
|---|---|---|
| **Thu 19 Nov** (scoping session) | Choose track and question; fill the **one-page canvas** (below); **start downloading your scene** (~1 GB; ask for the 256 × 256 subset if bandwidth is short) | canvas (hand in at the end of the session) |
| Fri 20 – Sun 22 | No work required. Optional: scene downloaded, environment working | — |
| **Mon 23 Nov** | Load scene, quality-check, make a false-colour picture; build **baseline A** and plan labels/validation split *before* seeing results | notebook sections 1–5 run |
| **Tue 24 Nov** | Build **B** (multispectral) and **C** (hyperspectral AI model) with your AI assistant; start the AI use log | three maps |
| **Wed 25 Nov** (morning, then **build afternoon** with instructors) | Validate A, B, C on a spatial split; error analysis (3 failure cases); draft the one-pager | validation table + figures |
| **Thu 26 Nov** (morning) | Freeze the notebook, *Restart & Run All*, submit | submission folder |
| **Thu 26 Nov** (afternoon) | **8-minute presentation + 4 minutes of questions** | slides |

## Scoping canvas (one page, Thu 19 Nov)

1. **Team and roles** — who does data/QC, modelling, validation, communication (everyone codes a little; roles are a lead, not a monopoly).
2. **Track, scene and window** — scene ID, window (≤ 1000 × 1000 px is plenty), the 3–4 classes.
3. **User and decision** — one named user, one decision, one sentence each (e.g. *"a municipal planner deciding where to inspect for illegal construction"*).
4. **Hyperspectral hypothesis** — which wavelength range or feature should help, and **where B (multispectral) is expected to fail.**
5. **Validation plan** — where the labels come from, how you split into blocks (write it **before** you see results).
6. **Risk** — the one thing most likely to go wrong and your plan B.

## Deliverables (Thu 26 Nov, morning)

One folder `team_<name>_mini_project/`:

```
├── README.md          ← the one-page brief for the decision-maker (see below)
├── project.ipynb      ← from templates/project_template.ipynb; sections 1–8, executed, runs top to bottom
├── outputs/           ← the three maps as GeoTIFF (hu.save_geotiff) + figures (PNG)
├── validation/        ← metrics table (CSV) + confusion matrices
└── presentation.pdf   ← ≤ 6 slides
```

- **Do not submit raw HDF5 scenes**; list the scene IDs.
- You can **skip** template sections 9 and 10 (product output, next steps) and the interim QA checklist.

### The one-page brief (`README.md`)

1. **Question and user** (2–3 lines).
2. **Result**: the map, a one-line "what we found", and the key number.
3. **Table**: A vs B vs C — overall accuracy **and** per-class precision/recall, on the spatial test set.
4. **What hyperspectral added** — or honestly, what it did not.
5. **How far to trust it**: the 3 failure cases, label limitations, uncertainty (a confidence map **or** a bootstrap confidence interval on accuracy).
6. **AI use**: two lines on what the AI got wrong and how you caught it. The full log is in the notebook.

### The 8-minute presentation

Problem → data → three methods → results (one comparison figure) → where it fails → "so what" for the user.
Slides: ≤ 6. Use `templates/presentation_template.md`, shortened.

## Definition of done

**To pass (about a "3" on every criterion):**

- [ ] Baseline, multispectral version and hyperspectral AI model all run and are compared on the same test pixels.
- [ ] **Spatially independent** train/test split, written down before the results.
- [ ] Metrics: confusion matrix, per-class precision and recall, overall accuracy.
- [ ] **Random vs spatial split compared** in one line (it takes five minutes and shows the leakage effect).
- [ ] Three failure cases explained.
- [ ] One-page brief, AI use log, notebook runs top to bottom.

**Stretch (this is where a "4" comes from, pick at most one):**

- A per-pixel **confidence map** or bootstrap confidence intervals on every metric.
- A sensitivity test (threshold, number of bands, training-set size, spectral resampling).
- An **absorption-feature** analysis (continuum removal, `hu.band_depth`) showing a physical reason for what C finds.
- A second date or scene to test whether the model transfers.

## Grading

Same five criteria and weights as `templates/evaluation_rubric.md` (**Validity 30 · Relevance 20 · Impact 20 ·
Creativity 15 · Presentation 15**), read at one-week scale:

- **Validity** counts the most: the spatial split, per-class metrics, baseline comparison and honest limits.
  The AI log and the checks above belong here.
- **Relevance**: a complete, reproducible workflow for the stated question; *not* a broad question.
- **Impact**: a named user and decision, and a believable statement of what they'd do with the result.
  You do not need a prototype app or a scaling plan.
- **Creativity**: specific spectral features, and a convincing A/B/C comparison.
- **Presentation**: a clear story in 8 minutes.

## Rules and good practice

- Credit every dataset (Tanager: CC-BY-4.0 © Planet Labs PBC; ESA WorldCover: CC-BY 4.0). `hu.attribution(scene_id)` prints the text.
- Teams keep ownership of their work.
- Keep it small: one scene, ≤ 4 classes, one model. A narrow question answered properly beats a broad one answered loosely.
- Stuck for more than 30 minutes? Ask an instructor or the assistant, then **verify the answer**.
