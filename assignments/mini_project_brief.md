# Mini project (one-week sprint) — brief

**Space Academy 2026 · Hyperspectral course (Course 3)** · **Thu 19 Nov → Thu 26 Nov** · **100 % of the course grade**

This replaces the three-week project in [`final_project_brief.md`](final_project_brief.md) and matches the slide deck
`mini_project/course3_capstone_project_requirements_2026.pptx`.

There are two kinds of team:

| Team | What you do |
|---|---|
| **Course 3 teams** | Build **one Google Colab notebook** that takes Planet Tanager data from search to results, using AI tools such as **Gemini in Colab**. |
| **Hackathon teams** | Show **clear progress on your app** and **how you applied the course knowledge in it**. |

> **The idea in one sentence:** check what the Planet Tanager STAC catalogue holds, pick a theme, find the scenes that fit,
> and answer **one research question** with them. Let AI assistants speed up the coding, and spend the time you save
> **checking that the answer is right**.

Effort: roughly **12–16 team hours**.

## Course 3 teams: the notebook

**Data:** the [Planet Tanager Core Imagery STAC catalogue](https://www.planet.com/data/stac/browser/tanager-core-imagery/catalog.json).
It is a *static* catalogue (a tree of JSON files, no search API), so you explore it with `16_scene_finder.ipynb`.
You may choose any scene in it.

**Other data sources are welcome.** For example, [Sentinel-2 L2A](https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a)
(via the Microsoft Planetary Computer, as in the course notebooks) can give you a second date, a multispectral comparison
or reference labels. ESA WorldCover works too. Credit every source.

**Your research question.** Write one question that your data can answer, for example *"Can SWIR bands tell snow
from cloud in these scenes?"* or *"How well does a narrow-band index map burn severity compared with Sentinel-2?"*.
A narrow question that you answer properly beats a broad one answered loosely.

Your notebook follows six steps:

| # | Step | What to show | Course material |
|---|---|---|---|
| 1 | **Explore the data** | Check what the catalogue holds: collections, places, dates, cloud cover | `16_scene_finder` |
| 2 | **Pick a theme** | Choose a theme (see the case studies below) and write your research question | — |
| 3 | **Find your scenes** | Filter for scenes that fit the theme, check thumbnails and cloud cover, justify your choice; add other data if useful | `16_scene_finder` |
| 4 | **Download and pre-process** | Get the scene with `hu.get_scene()` (about 1 GB), read a small window to test your code, remove bad bands, apply masks | `00_EO_data_quickstart`, `11_preprocessing`, `12_processing_workflow` |
| 5 | **Analyse and plot** | Spectral indices, PCA, classification or target detection, **plus a simple baseline** to compare with. Maps with legends, spectra, confusion matrix or histograms; each figure readable on its own, with a short interpretation | `13`, `14`, `15`, `21`; `20` for deep learning |
| 6 | **Next steps** | Limitations, what you could not test, what would improve the result, how it could grow into an app | — |

Start the notebook from `templates/project_template.ipynb` if you like, or build your own in Colab.

### Example case studies

Pick a theme, then find scenes in the matching catalogue collection. The scene counts come from the course index
(`data/tanager_catalog_index.geojson`, 276 entries), so they may differ if you refresh it.

| Theme | Collection | Example research question |
|---|---|---|
| Fire burn mapping | `fire` (11 scenes) | Which areas burned, and how severely? Compare dates in Los Angeles (Dec 2024 to Apr 2025). |
| Agriculture | `agriculture` (44) | Can narrow bands separate crop types or irrigated fields better than NDVI? |
| Snow and ice | `snow-ice` (7) | Can SWIR bands tell snow and ice from cloud? Check cloud cover first (Nunavut, Chukotka, Alaska, Greenland). |
| Coastal water | `coastal-water-bodies` (43) | Can you map mangroves, shallow water or turbidity (e.g. El Salvador, Vietnam)? |
| Mining and minerals | `energy-mining` (17) | Which surface materials can you tell apart around a mine (e.g. Nevada)? |
| Urban land cover | `urban` (58) | Which classes can you map in a city, and where are they confused? |

Also in the catalogue: `GHG-plumes` (8, harder: target detection), `natural-lands` (72) and `ROCX2025` (16 repeat scenes
over Rochester, NY, July and August 2025, good for change over time). Some scenes have high cloud cover, so always check it first.

### Using AI tools (required, and judged)

AI assistants are encouraged: **Gemini in Google Colab**, Claude, ChatGPT, Copilot, anything you like.

1. **Give the assistant context.** Paste the function list from `hsi_utils.py` so it uses the course functions instead of inventing its own.
2. **Keep a short AI log** at the end of the notebook (5–10 rows): *prompt → what the AI produced → what you checked → what you changed or rejected.*
3. **Every team member must be able to explain the notebook and the results.**

**Check AI-written hyperspectral code for these classic mistakes:**

- [ ] **Random pixel split** if you train a model. Neighbouring pixels are near-identical, so it leaks. Split by spatial block.
- [ ] **Bad bands left in.** Water-vapour bands and the noisy edges must be removed.
- [ ] **Wavelength vs band number.** "Band 50" is not 860 nm. Use `hu.band_index(wl, 860)`.
- [ ] **Invented function names.** If a `hypercoast` or `hsi_utils` call does not exist, the AI made it up; check the source.
- [ ] **Accuracy alone.** It hides a bad minority class. Show per-class results and a confusion matrix.
- [ ] **Clouds and nodata** treated as real pixels.
- [ ] **A score that is great on the first try.** Look for leakage before you celebrate.

### Notebook rules

- Share it as a Colab link set to **"Anyone with the link can view"**, and open it in a private window to test it.
- **Restart and run all** must work on a clean runtime. Install packages in the first cell.
- Do **not** save raw scenes (about 1 GB each) in your Drive. List the scene IDs.
- No API keys or personal credentials in the notebook.
- Credit the data: `hu.attribution(scene_id)` prints the Planet Labs PBC / CC-BY-4.0 text.

### Starting from a course scene (optional)

If you want a head start, seven Tanager scenes come with the course. Six of them have ESA WorldCover labels on the scene
grid (`hu.load_labels()`) and an exercise with a worked solution: Konya `20250608_091605_90_4001` (`ex_01`),
Ho Chi Minh City `20250407_035509_25_4001` (`ex_02`), Korba `20250219_053251_31_4001` (`ex_03`), Malibu
`20241215_185916_33_4001` (`ex_04`), El Salvador `20250223_165546_32_4001` (`ex_05`) and Al Dhafra
`20250511_074311_00_4001` (`ex_06`). WorldCover has no burn class, so for fire you digitise your own reference points.
Aim for a different question or a better check than the exercise.

## Hackathon teams: app progress

Your presentation must **clearly demonstrate progress on your app** and **how you implemented the course knowledge in it**:

- the current state of the app (screenshots or a live demo);
- which course topics you applied, and where in the app (search, pre-processing, indices, classification, validation, ...);
- what changed in the app because of the course;
- how Tanager scenes reach your app (the data flow);
- what you will build next, and which AI tools you used.

## Deadlines and presentation

| When | What |
|---|---|
| **Thu 19 Nov** (scoping session) | Explore the data, pick a theme and a research question (Course 3 teams), or confirm your app plan (hackathon teams). Start downloading your scene (about 1 GB; ask for the 256 × 256 subset if bandwidth is short). |
| Mon 23 – Wed 25 Nov | Build. Wednesday afternoon is build time with instructors. |
| **Wed 25 Nov, 8:00 PM (GST)** | **Send your presentation (PDF) and the link to your notebook** to vincent.markiet@space42.ai and ali.alhammadi@Space42.ai |
| **Thu 26 Nov** | **Final presentations**, 5–10 minutes per team. Time to be confirmed. |

All times are UAE local time (GST, UTC+4).

### Presentation outline (Course 3 teams)

1. Research question: what you asked and who needs the answer.
2. Data: Tanager scenes, other sources, study area and date.
3. Streaming, download and pre-processing steps.
4. Analysis: method, parameters and AI tools used.
5. Results: plots and what they mean for users.
6. Limitations: errors, challenges and lessons learned.
7. Next steps: improvements and future potential.

## Grading

Both team types are judged with the criteria in the last slide of the deck:

| Criterion | Weight |
|---|:--:|
| Problem definition: significance and relevance | 15 % |
| Technical execution and method (data access, pre-processing, analysis, use of AI tools; for hackathon teams, app progress) | 20 % |
| Results and interpretation | 20 % |
| Learning and reflection (including how course knowledge was applied) | 10 % |
| Presentation quality (slides, notebook or app demo) | 15 % |
| Long-term vision | 15 % |
| Scientific evaluation | 10 % |
| Team relevant expertise | 10 % |

*The weights add up to 115 %, exactly as in the original table. Normalise or adjust them before scoring.*

Each criterion is scored 1–5 using the descriptors in the deck.

## Rules and good practice

- Credit every dataset (Tanager: CC-BY-4.0 © Planet Labs PBC; Sentinel-2 and any other source you use).
- Teams keep ownership of their work.
- Stuck for more than 30 minutes? Ask an instructor or the assistant, then **verify the answer**.
