# Assignment W1 — Scene exploration report

**Space Academy 2026 · Hyperspectral course · Week 1** · individual · due at the start of Week 2 · 10 % of the course grade

> **Not used in the 2026 three-week course.** Assessment is the mini project alone — see
> [`final_project_brief.md`](final_project_brief.md). This brief is kept for reference and for a
> future longer run, and is still a good self-directed exercise.

**Goal:** show that you can access, quality-check and interpret a hyperspectral scene.
**Builds on:** notebooks `00`, `10_spectral_signatures_and_libraries`, `11_preprocessing`.

## Task

Choose **one** Tanager scene: one of the course scenes, or any scene from `16_scene_finder.ipynb` over the Arab region.
Hand in a notebook (`w1_<yourname>.ipynb`, executed with outputs) that contains:

1. **Scene card** (markdown table): scene ID, date, place, collection, CRS, size, % usable pixels, % cloud flag.
2. **Quality control**: a true-colour quicklook and the no-data, cloud and cirrus masks. Look for mask errors
   (false positives or missed clouds) and write 2–3 sentences on what you found.
3. **Bad bands**: plot the median spectrum of the scene with the removed regions shaded, and explain
   in your own words why each region is removed.
4. **Three materials**: pick three visibly different materials (e.g. water, vegetation, bare soil/urban). Plot one
   representative spectrum of each (average a 3×3 window) and annotate **at least four absorption features**
   with their cause.
5. **One index map** relevant to a challenge theme, with a sentence on the exact wavelengths used.
6. **Multispectral comparison**: resample your three spectra to Sentinel-2 (`hu.resample_to_sensor`) and name
   one feature that disappears.
7. **Reflection** (≤ 150 words): what would you need to trust this scene for a real application?

## Grading

| Component | Points |
|-----------|:------:|
| Scene card + QC with an honest mask discussion | 25 |
| Bad-band explanation | 15 |
| Material spectra + correctly explained absorption features | 30 |
| Index map + Sentinel-2 comparison | 20 |
| Clarity (labels, units, markdown), reflection | 10 |

*Tip: a spectrum plot without axis labels and units cannot receive full marks.*
