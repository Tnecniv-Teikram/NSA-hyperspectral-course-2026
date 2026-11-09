# Final graduation project — brief

**Space Academy 2026 · Hyperspectral course · Weeks 2–4** · teams of 3–5 · 60 % of the course grade

## What you build

An **applied hyperspectral solution** for one of the six challenge themes (see `../../Starting_notebooks/README.md`):
precision agriculture · land use and urban change · air quality and GHG plumes · climate-induced disasters ·
ecosystem health and blue carbon · water quality.

The solution must:
1. address a **named user and decision**;
2. use **hyperspectral-specific information** (narrow-band features, full-spectrum models, detection or unmixing) and
   show what it adds compared with multispectral data;
3. include a **validated** output (map, estimate or alert) with its uncertainty;
4. be **reproducible** (notebook runs top to bottom) and **deliverable** (COG + metadata + product mock-up).

## Milestones

| When | Session | Deliverable | Template |
|------|---------|-------------|----------|
| Week 2 (Thu 12 Nov) | Project scoping and use case definition | Scoping canvas (1–2 pages) | `templates/project_scoping_template.md`, `16_scene_finder.ipynb` |
| Week 3 (Tue–Wed) | Applied project development workshop | Working method on one scene | `templates/project_template.ipynb` |
| Week 3 (Thu 19 Nov) | Interim project feedback and QA | Assignment W3 + self-QA checklist | `assignments/assignment_w3_validated_map.md`, `templates/interim_qa_checklist.md` |
| Week 4 (Mon 23 Nov) | Advanced analytics and solution refinement | Refined method, uncertainty, error analysis | `30_advanced_analytics.ipynb` |
| Week 4 (Tue 24 Nov) | Final implementation and testing | Pipeline, tests, product mock-up | `31_from_notebook_to_product.ipynb` |
| Week 4 (Wed 25 Nov) | Presentation preparation and rehearsal | Slides, timed rehearsal | `templates/presentation_template.md` |
| Week 4 (Thu 26 Nov) | Final graduation project submission | Submission folder | `templates/submission_checklist.md` |
| Week 4 (Thu 26 Nov) | Final evaluation and feedback | 12 min presentation + Q&A | `templates/evaluation_rubric.md` |

*All four weeks run Monday to Thursday: 2–5 Nov, 9–12 Nov, 16–19 Nov and 23–26 Nov. There are no Friday sessions.*

## Grading

The final project is assessed with `templates/evaluation_rubric.md`: Validity 30, Relevance 20, Impact 20,
Creativity 15, Presentation 15. Individual contributions are listed in the submission README and can be moderated
with peer feedback.

## Rules and good practice

- Credit every dataset (Tanager: CC-BY-4.0 © Planet Labs PBC; ESA WorldCover: CC-BY 4.0; etc.).
- Do not submit raw HDF5 files; list scene IDs instead.
- Using AI coding assistants is allowed; you must understand and be able to explain every line you submit.
- Teams keep ownership of their work (as in the 813 Challenge).
