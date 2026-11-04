# Final presentation template (10–12 slides, 12 minutes + 5 minutes Q&A)

**Space Academy 2026 · Hyperspectral course · Week 4 — Presentation preparation and project rehearsal**

Build your slides in any tool (PowerPoint, Google Slides, Keynote, Quarto/reveal.js) and export them to PDF.
One message per slide. Titles are full sentences that state the takeaway, e.g. *"Mangrove loss is concentrated
near shrimp ponds"*, not *"Results"*.

| # | Slide | Content | Time |
|---|-------|---------|------|
| 1 | **Title** | Project name, team, theme, one-sentence value proposition | 0:20 |
| 2 | **The problem** | Who has the problem, where, how big (numbers, photo, map) | 1:00 |
| 3 | **Today's solution and its gap** | What users do now and why it falls short | 0:40 |
| 4 | **Why hyperspectral** | The spectral feature(s) you exploit: one spectrum plot with the key wavelengths marked | 1:00 |
| 5 | **Data** | Scenes (map of footprints, dates), reference data, preprocessing in one line each | 0:50 |
| 6 | **Method** | Processing chain diagram (boxes and arrows); the one idea that makes it work | 1:30 |
| 7 | **Result** | The main map, large and readable, with legend and scale | 1:30 |
| 8 | **Does it work? Validation** | Metrics table + confusion matrix or scatter plot; baseline comparison; uncertainty | 1:30 |
| 9 | **Limitations** | 2–3 honest limitations and how you would address them | 0:50 |
| 10 | **From notebook to product** | Mock-up or screenshot of the dashboard/API/alert; who pays, how often it runs | 1:20 |
| 11 | **Impact and next steps** | Quantified benefit; roadmap (more scenes, EnMAP/813 mission, pilot user) | 0:50 |
| 12 | **Thank you + credits** | Data attributions, team contacts | 0:10 |

## Rehearsal checklist

- [ ] Timed run-through under 12 minutes (rehearse at least twice).
- [ ] Every team member knows the answers to the three most likely questions:
  1. *How do you know your map is correct?*
  2. *Why not just use Sentinel-2?*
  3. *What would it take to run this operationally?*
- [ ] Figures readable from the back of the room: fonts ≥ 18 pt, no screenshots of code.
- [ ] Backup: PDF on a USB stick + online copy; a screen recording in case a live demo fails.
- [ ] Credits slide includes *"Tanager STAC Data © 2025 Planet Labs PBC (CC-BY-4.0)"* and all other data sources.

## Design tips

- One key figure per slide. Remove everything the audience does not need.
- Use the same colours for the same classes on every slide.
- Show a spectrum. It is the fastest way to convince people that hyperspectral data adds something.
- Put numbers in context: "92 % accuracy" means little; "misses 1 in 12 mangrove pixels, mostly at the water edge" means a lot.
