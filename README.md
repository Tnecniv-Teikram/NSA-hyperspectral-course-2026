# 🛰️ Space Academy 2026 — Hyperspectral Earth Observation

**Participant handbook · three weeks · 9–26 November 2026**

Welcome. This page is the one you keep open. It tells you what to install, what happens each day, what
you have to hand in, and where to look when something breaks.

All practical work uses **real Planet Tanager satellite imagery** — 426 spectral bands from 380 to 2500 nm at
30 m, open data under CC-BY-4.0. No API keys, no logins, no paid accounts.

---

## What you will be able to do by the end

You already work with multispectral imagery. By the final week you will be able to:

- Read a spectrum and name the physical cause of every bend in it
- Open, mask, subset and preprocess a hyperspectral cube in Python
- Reduce 400+ bands to the handful of features your question actually needs
- Detect a specific material against an unknown background, and unmix a pixel
- Train, tune and **honestly validate** both a classical and a deep-learning classifier
- Say when hyperspectral data is worth it — and when Sentinel-2 would have done
- Turn a notebook into something a colleague can run: a tested pipeline with a map coming out of it

---

## What is in this repository

```
NSA-hyperspectral-course-2026/
├── README.md                 ← you are here
├── INSTRUCTOR.md                every syllabus session mapped to its materials
├── teaching_plan.md             the day-by-day plan, with timings
│
├── 09_numpy_for_hyperspectral.ipynb  …  31_from_notebook_to_product.ipynb
│                                the 13 course notebooks, in teaching order
├── hsi_utils.py                 the shared helpers every notebook imports
│
├── exercises/                   one exercise set per challenge theme (with solutions)
├── quizzes/                     four ungraded lecture quizzes (with answers)
├── assignments/                 the three weekly assignments + the final project brief
├── templates/                   scoping canvas, project skeleton, checklists, rubric
├── slides/                      one lecture deck per session
├── data/                        land-cover labels, spectral library, EnMAP subset, scene index
├── app/                         an example product and a Streamlit viewer
└── tests/  tools/               test suite and the scripts that build the material
```

**The Week 1 theme notebooks are in a separate repository.** The six challenge-theme notebooks `00`–`06`
live in [`813-hyperspectral-hackathon`](https://github.com/Tnecniv-Teikram/813-hyperspectral-hackathon). Clone it *beside* this one, named `Starting_notebooks`, so
the relative links resolve:

```bash
cd ..        # next to this repository
git clone https://github.com/Tnecniv-Teikram/813-hyperspectral-hackathon.git Starting_notebooks
```

Two repositories, two jobs. **`Starting_notebooks`** gets you to your first hyperspectral image and gives you
one notebook per application theme. **This** repository is the method: everything from preprocessing to a
validated AI map to a finished product.

---

## Day one — get your environment working

Do this **before** Monday afternoon if you can. Setup is the single thing most likely to cost you a day.

### Option 1 · Google Colab — recommended, nothing to install

Open any notebook and click the **Open in Colab** badge at the top, then run the first cell. It fetches the
course material and installs the few packages Colab lacks. You need nothing but a browser and a Google
account.

Colab is also the *faster* option for this course: it gives you a free GPU for the deep-learning session, and
the satellite scenes arrive in minutes because Planet hosts them on Google Cloud Storage — on hotel wifi a
single 1 GB scene can take an hour.

Two things to know:

- **A Colab session is temporary.** Download your edited notebook, or save it to Google Drive, before you
  close the tab.
- **Scenes are re-downloaded in every new session.** To avoid that, mount your Drive and point the course at
  it, once per session:

  ```python
  from google.colab import drive; drive.mount("/content/drive")
  import os; os.environ["TANAGER_DATA_DIR"] = "/content/drive/MyDrive/tanager"
  ```

### Option 2 · Your own machine

Worth it if you want the QGIS session, the Streamlit viewer, or you simply prefer local work. You need
**Python 3.11 or newer**.

```bash
git clone https://github.com/Tnecniv-Teikram/NSA-hyperspectral-course-2026.git
cd NSA-hyperspectral-course-2026

# create the environment OUTSIDE any synced folder
python -m venv ~/venvs/hsi2026
source ~/venvs/hsi2026/bin/activate          # Windows: %USERPROFILE%\venvs\hsi2026\Scripts\activate
pip install -r requirements.txt

# register the environment as a Jupyter kernel, and give it an obvious name
python -m ipykernel install --user --name hsi2026 --display-name "Hyperspectral course 2026"
jupyter lab
```

**Then pick the "Hyperspectral course 2026" kernel inside every notebook.** This matters more than it looks —
see the first entry under *When something breaks*.

Three local gotchas:

- **Never put the virtual environment inside OneDrive, Dropbox or iCloud.** Sync corrupts it, and it holds tens
  of thousands of small files.
- `torch` is about 2.5 GB and only the deep-learning notebook needs it. Delete that line from
  `requirements.txt` for a quick start, and install it before Week 3.
- If `pip` or any download fails with `SSL: CERTIFICATE_VERIFY_FAILED`, you are behind a TLS-inspecting
  corporate proxy. Point Python and GDAL at your organisation's CA bundle:
  `export REQUESTS_CA_BUNDLE=/path/ca.pem GDAL_CURL_CA_BUNDLE=/path/ca.pem`

### Are you fluent in numpy?

If slicing, axes, boolean masks and broadcasting are not second nature, start with
**`09_numpy_for_hyperspectral.ipynb`** — 45–60 minutes, written for exactly
this gap, using real cubes rather than toy arrays. It is the best hour you can spend before the course starts.
Everything else assumes you can read and adapt array code.

**Machine learning experience is not assumed.** The vocabulary — features, labels, train/test, overfitting,
confusion matrix — is taught from zero in a 20-minute primer before the first classification session.

### Day-one checklist

- [ ] A notebook opens and runs its first cell (Colab badge, or local kernel selected)
- [ ] `import hsi_utils` works
- [ ] One Tanager scene is on disk or reachable — try the first section of notebook 10
- [ ] Working locally? You have run the `ipykernel install` line above
- [ ] Coming to the desktop session? QGIS 3.40+ and the **EnMAP-Box** plugin are installed (get the installer
      from your instructor in Week 1 — the download is blocked on the venue network)

---

## The three weeks

Every week runs **Monday to Thursday**. There are no Friday sessions.
Each day is roughly: lecture (1.5–2 h) · guided notebook (2–2.5 h) · your own work (1.5–2 h).

### Week 1 · 9–12 Nov — seeing the spectrum

| Day | Session | You work on | Homework |
|---|---|---|---|
| **Mon 9** | Kickoff and orientation · Course objectives, the mini project, the gIQ and course platforms | environment setup — get Colab or a local install working today | **notebook 09 if numpy is new to you** |
| **Tue 10** | Introduction to hyperspectral EO · Spectral signatures, sensors and use cases | `10_spectral_signatures_and_libraries` | quiz W1a · finish notebook 10's "Your turn" |
| **Wed 11** | Data access, visualization and exploration | `00_EO_data_quickstart`, then one or two theme notebooks `01`–`06`, your choice | the matching `ex_01`–`ex_06` · **pick your mini-project theme** |
| **Thu 12** | Preprocessing concepts | `11_preprocessing` — the fullest notebook of the week | quiz W1b |

Monday and Tuesday each carry two sessions, so they are full days. Get your environment working on Monday —
it is the single thing most likely to cost you a day later.

### Week 2 · 16–19 Nov — from cube to answer

| Day | Session | You work on | Homework |
|---|---|---|---|
| **Mon 16** | Image processing workflows | `12_processing_workflow` · `hsi_utils.py` | — |
| **Tue 17** | Feature extraction and dimensionality reduction | `13_feature_extraction_dim_reduction` | quiz W2 |
| **Wed 18** | Material discrimination and target detection | `14_material_discrimination_target_detection` | — |
| **Thu 19** | ML primer + classification · Project scoping and use case definition | `15_classification_classical` · `16_scene_finder` + your scoping canvas | **scoping canvas due Mon 23** |

### Week 3 · 23–26 Nov — GeoAI, validation, and your project

| Day | Session | You work on | Project |
|---|---|---|---|
| **Mon 23** | GeoAI methods for hyperspectral | reading + the lecture sections of `20_geoai_deep_learning` | **scoping canvas due** · quiz W3 |
| **Tue 24** | AI-assisted classification and mapping | `20_geoai_deep_learning` — training and inference (~6 min on CPU) | apply the method to your own scene |
| **Wed 25** | Validation and accuracy assessment | `21_validation_accuracy_assessment` in the morning | **afternoon is project build time**, instructors on hand |
| **Thu 26** | **Final submission and presentations** | — | morning: finalise and submit · afternoon: 12 minutes + 5 minutes of questions |

A day-by-day run sheet with timings is in [`teaching_plan.md`](teaching_plan.md).

### Material we will not cover in class

It is all in this repository, and it is the natural next step if you want to go further:

- `17_hypercoast_tanager_enmap` and [`qgis_lab_hyperspectral.md`](qgis_lab_hyperspectral.md) — interactive maps and the QGIS/EnMAP-Box desktop lab
- `30_advanced_analytics` — change detection, uncertainty, harmonisation, scaling
- `31_from_notebook_to_product` — packaging a notebook into a tested pipeline and an app

## What you hand in

**One mini project. It is the whole assessment** — there are no graded weekly assignments.

| When | What |
|---|---|
| **Mon 9 Nov** | The mini project is introduced |
| **Wed 11 Nov** | Pick your theme |
| **Thu 19 Nov** | Scoping canvas drafted in the session — `templates/project_scoping_template.md` |
| **Mon 23 Nov** | Scoping canvas due |
| **Wed 25 Nov** | Build afternoon, with instructors on hand — `templates/project_template.ipynb` |
| **Thu 26 Nov** | Submit in the morning, present in the afternoon |

Read [`assignments/final_project_brief.md`](assignments/final_project_brief.md) in week 1, not week 3 — the
project runs through the whole course, and everything you do in the sessions feeds it.

You are marked with `templates/evaluation_rubric.md`: **Validity 30 · Relevance 20 · Impact 20 · Creativity 15
· Presentation 15**. Read it early. Validity carries the most weight, which means an honest, properly validated
result beats an impressive-looking one.

`templates/` also holds the submission checklist and the presentation outline. **Quizzes are ungraded** — they
exist so you can find out what did not land, before it matters.

Two rules worth stating plainly:

- **Do not submit raw HDF5 scenes.** List the scene IDs instead.
- **AI coding assistants are allowed.** You must understand and be able to explain every line you submit.

## Difficulty, so you can plan your week

⭐ follow along · ⭐⭐ needs attention · ⭐⭐⭐ advanced, with an optional deep-dive you may skip

| Notebook | Level | Heaviest demand |
|---|:--:|---|
| `09_numpy_for_hyperspectral` | ⭐ | none — this is the on-ramp |
| `10_spectral_signatures_and_libraries` | ⭐ | reading plots |
| `11_preprocessing` | ⭐⭐ | numpy masking and axes |
| `12_processing_workflow` | ⭐⭐ | software patterns, not science |
| `13_feature_extraction_dim_reduction` | ⭐⭐⭐ | PCA / MNF — the maths is skippable |
| `14_material_discrimination_target_detection` | ⭐⭐⭐ | §3–4 (matched filter, unmixing) are the hard part |
| `15_classification_classical` | ⭐⭐ | your first real ML — do the primer first |
| `16_scene_finder` | ⭐ | familiar if you have used a catalogue |
| `17_hypercoast_tanager_enmap` | ⭐ | the lightest code in the course |
| `20_geoai_deep_learning` | ⭐⭐⭐ | PyTorch |
| `21_validation_accuracy_assessment` | ⭐⭐ | §1–4 essential, §5 is reference only |
| `30_advanced_analytics` | ⭐⭐⭐ | length — it is split over a whole day |
| `31_from_notebook_to_product` | ⭐⭐ | packaging and testing |

The ⭐⭐⭐ notebooks mark their hard parts explicitly and tell you what you can skip on a first pass. Skipping a
marked deep-dive costs you nothing later.

---

## The data

Seven Tanager scenes carry the whole course. You never download them by hand:
`hsi_utils.get_scene("<scene id>")` looks for a scene on disk and fetches it from Planet's public catalogue if
it is missing — about 1 GB each, so do it on a connection you trust.

| Scene | Place | What it teaches |
|---|---|---|
| `20241215_185916_33_4001` | Malibu, California — Franklin fire scar | fire, change detection |
| `20250123_185518_92_4001` | Santa Monica Mountains — after the Palisades fire | change detection (self-study) |
| `20250219_053251_31_4001` | Korba / Kusmunda coal mines, India | minerals, target detection, greenhouse gases |
| `20250223_165546_32_4001` | Usulután, El Salvador — mangroves and estuary | classification, GeoAI, validation |
| `20250407_035509_25_4001` | Ho Chi Minh City, Vietnam | urban, target detection |
| `20250511_074311_00_4001` | Al Dhafra coast, UAE — sabkha and shallow water | preprocessing, water |
| `20250608_091605_90_4001` | Konya, Türkiye — irrigated agriculture | features, workflows |

**None of them ship with the repository** — they are about 1 GB each, so neither clone contains them.
`get_scene()` fetches whatever a notebook needs the first time you run it, and reuses it afterwards.

Smaller reference data ships with the material: ESA WorldCover land-cover labels on the Tanager grid, a
19-spectrum reference library built from these very scenes, an EnMAP subset over Groningen, and an index of
all 276 Tanager open-data scenes for when you go looking for your own.

**Working online and short of bandwidth?** Ask your instructor for the 256 × 256 pixel subsets — about 30 MB
instead of 1 GB each.

---

## When something breaks

**"ModuleNotFoundError: No module named 'matplotlib'" — and you definitely installed it.**
You are running the wrong kernel. Jupyter's default "Python 3" kernel often points at a different Python than
your course environment. Kernel → Change kernel → **Hyperspectral course 2026**. This is the single most
common setup failure; it is not your install that is wrong, it is the kernel.

**Downloads fail with `SSL: CERTIFICATE_VERIFY_FAILED`.**
TLS-inspecting proxy. Set `REQUESTS_CA_BUNDLE` and `GDAL_CURL_CA_BUNDLE` to your organisation's CA bundle, as
above. On Colab this never happens — another reason to prefer it on a restricted network.

**A scene "exists" but reading it hangs for ever.**
In OneDrive or Dropbox the file can be a 0-byte placeholder. Right-click the folder → *Always Keep on This
Device*, and wait for it to actually download.

**A GDAL write fails with "Unknown GDAL Error" right after you opened an interactive map.**
The map libraries set an environment variable that breaks GDAL writes. Restart the kernel, do your exports
first, and make the maps afterwards.

**The Indian Pines benchmark download fails in the deep-learning notebook.**
That dataset's host blocks some corporate and conference networks. The notebook is built to carry on without
it — that section is optional and nothing later depends on it.

**Everything is just slow.**
Once the scenes are on disk, most notebooks run in well under two minutes on a laptop CPU. The genuinely slow
ones are `20_geoai_deep_learning` (~6 minutes — it trains two small networks and runs inference over a whole
scene) and `30_advanced_analytics` (long, and it pulls one extra 1.3 GB scene the first time). If a notebook
you expected to be quick is not, you are almost certainly downloading a scene in the background.

Still stuck? Bring it to the next session — and bring the **full error message**, not a description of it.

---

## Where to look things up

| | |
|---|---|
| Detailed reference for every session | [`INSTRUCTOR.md`](INSTRUCTOR.md) |
| Day-by-day plan with timings | [`teaching_plan.md`](teaching_plan.md) |
| The six application themes | [`813-hyperspectral-hackathon`](https://github.com/Tnecniv-Teikram/813-hyperspectral-hackathon) |
| Lecture slides, all sessions | `slides/` |
| The shared helper functions you will use constantly | `hsi_utils.py` — it is documented; read it |
| QGIS / EnMAP-Box desktop lab | [`qgis_lab_hyperspectral.md`](qgis_lab_hyperspectral.md) |

---

## Credits and licence

Course material for the **Space Academy 2026** programme, an initiative of the **UAE Space Agency** and
**Space42**, and © 2026 both of them jointly. It is **not** open-source or open educational content — being
readable on GitHub grants no licence beyond the one in [`LICENSE`](LICENSE).

**As a participant you may** clone it, run it in Colab, modify it, and keep your copy for good. Anything you
write yourself is yours. **You may not** republish or mirror it, use it to teach others, or use it
commercially. Quoting extracts with attribution — in a thesis, report or paper — is fine and welcome.

The data has its own terms, which this licence does not override:

- **Tanager imagery** — *"Tanager STAC Data, available at www.planet.com/data/stac © 2025 Planet Labs PBC"*,
  CC-BY-4.0. Cite the acquisition year of the scene you used.
- **Land-cover labels** — ESA WorldCover 10 m 2021 v200, © ESA WorldCover project / contains modified
  Copernicus Sentinel data (2021), CC-BY-4.0.
- **EnMAP subset** — *"EnMAP data © DLR 2024 All rights reserved"*. For use inside this course only; do not
  redistribute it.
- **Laboratory spectra** — USGS Spectral Library Version 7, downloaded by you when a notebook asks for it.
