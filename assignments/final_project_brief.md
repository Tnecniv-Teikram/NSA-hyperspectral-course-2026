# Mini project — brief

**Space Academy 2026 · Hyperspectral course · weeks 1–3** · teams of 3–5 · **100 % of the course grade**

This is the only assessed work in the course. There are no graded weekly assignments; the quizzes are
formative. Everything you do in the sessions feeds this.

## What you build

An **applied hyperspectral solution** for one of the six challenge themes (see the
[theme notebooks](https://github.com/Tnecniv-Teikram/813-hyperspectral-hackathon)): precision agriculture ·
land use and urban change · air quality and GHG plumes · climate-induced disasters · ecosystem health and blue
carbon · water quality.

The solution must:

1. address a **named user and decision**;
2. use **hyperspectral-specific information** (narrow-band features, full-spectrum models, detection or
   unmixing) and show what it adds compared with multispectral data;
3. include a **validated** output (map, estimate or alert), with an honest statement of its uncertainty;
4. be **reproducible** — the notebook runs top to bottom.

It is a *mini* project: three weeks, with one scheduled build afternoon. Scope it so that a working, validated
result on **one scene** is achievable. A narrow question answered properly scores far better than a broad one
answered loosely — validity carries the most weight in the rubric.

## Milestones

| When | Session | Deliverable | Template |
|------|---------|-------------|----------|
| Mon 9 Nov | Course objectives + mini project | — (the brief is introduced) | this document |
| Wed 11 Nov | Data access, visualization and exploration | Theme and candidate scene chosen | `16_scene_finder.ipynb`, the theme notebooks |
| Thu 19 Nov | Project scoping and use case definition | Scoping canvas drafted in the session | `templates/project_scoping_template.md` |
| **Mon 23 Nov** | GeoAI methods | **Scoping canvas due** | `templates/project_scoping_template.md` |
| Tue 24 Nov | AI-assisted classification and mapping | Method applied to your own scene | `20_geoai_deep_learning.ipynb` |
| Wed 25 Nov | Validation and accuracy assessment | **Build afternoon** — validated result, instructors on hand | `21_validation_accuracy_assessment.ipynb`, `templates/project_template.ipynb` |
| **Thu 26 Nov** | Final submission and presentation | Morning: submission folder · afternoon: 12-minute presentation + 5 minutes of questions | `templates/submission_checklist.md`, `templates/presentation_template.md`, `templates/evaluation_rubric.md` |

*All three weeks run Monday to Thursday: 9–12 Nov, 16–19 Nov and 23–26 Nov. There are no Friday sessions.*

**Start early.** With one scheduled build afternoon, a team that has not chosen a theme by Wednesday of week 1
and scoped it by Thursday of week 2 will not finish. Most of the building happens in your own time.

## Grading

Assessed with `templates/evaluation_rubric.md`:

| Criterion | Weight |
|---|:--:|
| 🔬 Validity — scientific and technical rigour | **30** |
| 🎯 Relevance — fit to theme, completeness, feasibility | 20 |
| 🌍 Impact — who benefits and how much | 20 |
| 💡 Creativity — originality and use of hyperspectral information | 15 |
| 🎤 Presentation — clarity of storytelling and visuals | 15 |

Read the rubric in week 1, not the night before. Individual contributions are listed in the submission README
and can be moderated with peer feedback.

## Going further

Three sessions' worth of material is offered as optional homework rather than taught in class, and it is
exactly what a strong project draws on: `30_advanced_analytics.ipynb` (change detection, uncertainty,
scaling), `31_from_notebook_to_product.ipynb` (packaging and tests) and `templates/interim_qa_checklist.md`,
which is a good self-check before you submit. None of it is marked — but the first of the three is where the
marks in **Validity** and **Creativity** tend to come from.

## Rules and good practice

- Credit every dataset (Tanager: CC-BY-4.0 © Planet Labs PBC; ESA WorldCover: CC-BY 4.0; etc.).
- Do not submit raw HDF5 files; list scene IDs instead.
- Using AI coding assistants is allowed; you must understand and be able to explain every line you submit.
- Teams keep ownership of their work (as in the 813 Challenge).
