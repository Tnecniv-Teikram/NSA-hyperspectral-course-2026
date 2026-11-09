"""Week 1 · Session 2 — Introduction to hyperspectral Earth observation.

Picture-led by design. The figures in ``slides/figures/w1b/`` are built for this deck by
``tools/figures_w1b.py`` — the notebook-derived figures in ``10_spectral_signatures…``
belong to session 3 (w1c), so reusing them here would spend that session's material a day
early. Regenerate with ``python tools/figures_w1b.py`` before rebuilding this deck.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("Introduction to hyperspectral Earth observation",
         "Week 1 · Session 2",
         notebook="10_spectral_signatures_and_libraries.ipynb",
         subtitle="From three colours to 426 — what a continuous spectrum buys you",
         week="Week 1 · 9–12 November 2026")

d.objectives([
    "Explain what makes a sensor *hyperspectral*, and why band count alone is not the definition",
    "Describe the electromagnetic quantities we measure: radiance, reflectance, emissivity",
    "Name the main spaceborne imaging spectrometers and their trade-offs",
    "Say what Tanager-1 measures, at what spectral and spatial sampling",
    "Judge when hyperspectral data is worth the extra cost and complexity",
], notes="Set expectations: today is conceptual, the practical starts after lunch with notebook 10. "
         "Ask the room who has used Sentinel-2 before — calibrate depth accordingly.")

d.section("1. What is hyperspectral?", "Sampling the spectrum instead of summarising it")

d.figure("You already know the picture. This is what is behind it.",
         "w1b/01_datacube.png",
         caption="Tanager-1 over Usulután, El Salvador — the top face is the image you would "
                 "recognise, the depth is wavelength",
         kicker="the mental model",
         notes="Start here, before any definition. Point at the top face: that is the Sentinel-2 "
               "view they already have. Then point into the cube: every pixel is a curve. "
               "The side faces are real slices — the dark horizontal bands are the water-vapour "
               "windows, which comes back in session 5 (preprocessing).")

d.callout("A multispectral sensor summarises the spectrum.\nA hyperspectral sensor samples it.",
          "Sentinel-2 gives you 13 numbers per pixel, each averaging tens to hundreds of nanometres. "
          "Tanager gives you 426 numbers, each ~5 nm wide — a curve you can interpret physically.",
          kicker="the one-sentence definition",
          notes="This is the slide to repeat at the end of the day. Everything else follows from it.")

d.figure("Summarising versus sampling, on one real spectrum",
         "w1b/02_summarise_vs_sample.png",
         caption="The same irrigated-crop spectrum, as Sentinel-2 records it and as Tanager records it",
         kicker="the definition, drawn",
         notes="The grey curve is identical in both panels — only the sampling changes. Ask them to "
               "find the 2200 nm dip in the top panel: they cannot, because B12 averages 175 nm. "
               "That single comparison is the whole argument for the course.")

d.bullets("The three defining properties", [
    "**Contiguous** — no gaps, so the result is a spectrum rather than a set of samples",
    "**Narrow** — 3–10 nm, enough to resolve a real absorption feature",
    "**Many** — 100–500 bands, which *follows* from the first two",
    ("So a 20-band sensor with wide, scattered bands is multispectral, and a 100-band sensor "
     "sampling 400–1000 nm continuously is hyperspectral", 1),
], kicker="definition",
   notes="Students often answer 'more than X bands' in the quiz. Push back: contiguity and width "
         "matter more. Band count is the symptom, not the definition.")

d.figure_bullets("What the sensors actually see",
                 "10_spectral_signatures_and_libraries/03_4_2_spectral_response_functions_tanager_.png",
                 ["Each curve is one band's spectral response function",
                  "Sentinel-2 B12 is ~175 nm wide — it averages the whole SWIR-2 region",
                  "Tanager samples that same region with ~40 bands",
                  "**Features narrower than a band can never be recovered**"],
                 caption="Spectral response functions, same wavelength axis",
                 notes="Point at the SWIR-2 region: this is exactly where clay, carbonate and "
                       "methane sit.")

d.section("2. What we measure", "Radiance, reflectance, and why the difference matters")

d.bullets("From photons to a number you can interpret", [
    "The sensor measures **at-sensor radiance** — it still contains the atmosphere",
    "**Atmospheric correction** removes scattering and gas absorption → **surface reflectance**",
    "Reflectance is unitless (0–1) and comparable between dates, places and sensors",
    ("Tanager ships both: `ortho_radiance_hdf5` and `ortho_sr_hdf5` — we use the latter, "
     "except for gas retrievals, which need radiance", 1),
], kicker="physical quantities",
   notes="Analogy: radiance is the photo as taken, reflectance is the photo after removing the "
         "lighting and the haze. Say explicitly that methane retrievals work on radiance — it "
         "pre-empts a question that always comes up in the GHG theme.")

d.figure("Why a leaf looks the way it does",
         "w1b/03_leaf_anatomy.png",
         caption="Pigments in the visible, cell structure in the NIR, water and dry matter in the SWIR",
         kicker="reading a spectrum",
         notes="Walk left to right and name the cause of each bend — do not read the labels out, "
               "ask the room what makes the dip. Draw the same shape on the whiteboard as you go; "
               "students remember the drawing, not the slide. The two gaps are the water-vapour "
               "windows where no band survives.")

d.figure_bullets("Real Tanager spectra, grouped by material",
                 "10_spectral_signatures_and_libraries/00_2_the_library_one_material_group_at_a_ti.png",
                 ["**Measured, not textbook** — every curve comes from the scenes you will analyse",
                  "Vegetation, water, soil, man-made and burnt surfaces, as five families",
                  "The grey columns are the water-vapour windows, where no band survives",
                  "You rebuild this library yourself in the practical",
                  ("Which curve is water, and how can you tell at a glance?", 1)],
                 caption="data/spectral_library",
                 kicker="the course reference library",
                 image_left=True,
                 notes="These are measured, not textbook, spectra — built from the same scenes the "
                       "students will analyse. Ask the question on the last bullet and wait: the "
                       "answer (near-zero in the NIR and SWIR) is the fastest way to teach that "
                       "water is dark everywhere except the visible.")

d.section("3. The missions", "Airborne heritage, today's satellites, what is coming")

d.figure("Where the imaging spectrometers sit",
         "w1b/04_mission_landscape.png",
         caption="Bubble size is pixel size; the dashed line is Sentinel-2's 13 bands for scale",
         kicker="who flies what",
         notes="Two things to draw out: the band counts are an order of magnitude above Sentinel-2, "
               "and nothing sits below 30 m. The second point is the whole of the next slide.")

d.table("The same missions, with the numbers", ["Mission", "Agency", "Since", "Bands / range", "GSD"], [
    ["Hyperion (EO-1)", "NASA", "2000–2017", "220 · 400–2500 nm", "30 m"],
    ["DESIS (ISS)", "DLR/Teledyne", "2018", "235 · 400–1000 nm", "30 m"],
    ["PRISMA", "ASI (Italy)", "2019", "239 · 400–2500 nm", "30 m"],
    ["EnMAP", "DLR (Germany)", "2022", "224 · 420–2450 nm", "30 m"],
    ["EMIT (ISS)", "NASA", "2022", "285 · 380–2500 nm", "60 m"],
    ["Tanager-1", "Planet", "2024", "426 · 380–2500 nm", "30 m"],
    ["CHIME / SBG", "ESA / NASA", "planned", "continuous VSWIR", "~30 m"],
], kicker="the reference table",
   notes="Leave this up while they write it down, then move on — the previous slide is the one "
         "that carries the message. Note DESIS stops at 1000 nm: no SWIR, so no minerals, no gases.")

d.figure("Why 30 m, and not 10 m",
         "w1b/05_tradeoff.png",
         caption="Spectral, spatial and radiometric resolution all draw on the same photons",
         kicker="the trade-off",
         notes="Pre-empt the most common project mistake: planning a study that needs weekly "
               "hyperspectral coverage of a whole country. Tasked scenes, not wall-to-wall time "
               "series. If anyone asks about sharpening to 10 m, that is 30_advanced_analytics, which is self-study.")

d.figure("Tanager-1 open data: the course scenes",
         "12_processing_workflow/01_4_batch_processing_all_course_scenes.png",
         caption="Malibu · Santa Monica · Korba · Usulután · Ho Chi Minh City · Al Dhafra · Konya",
         kicker="what you will work with",
         notes="Every scene here is CC-BY-4.0 open data from Planet's STAC catalogue, and all are "
               "already on the course machines. Each one anchors a challenge theme.")

d.section("4. When is it worth it?", "Matching the question to the sensor")

d.table("Does your question need a spectrum?", ["Question", "Multispectral", "Hyperspectral"], [
    ["Where is the vegetation?", "Yes — NDVI is enough", "Overkill"],
    ["Is this crop water-stressed?", "Partly (NDMI)", "Better: narrow water bands"],
    ["Which clay mineral is this?", "No", "Yes — 2200 nm feature shape"],
    ["Is there a methane plume?", "No", "Yes — 2300 nm absorption"],
    ["Which algal species bloomed?", "No", "Yes — pigment absorptions"],
    ["How much crop residue covers the soil?", "No", "Yes — cellulose at 2100 nm"],
], kicker="honest triage",
   notes="This table is the antidote to 'hyperspectral is always better'. Tell them the project "
         "rubric rewards an honest answer here, including 'multispectral would do'.")

d.figure("The six challenge themes, seen spectrally",
         "w1b/06_theme_fingerprints.png",
         caption="Each theme has a region of the spectrum that gives the answer away — shaded here",
         kicker="from physics to applications",
         notes="One panel per theme notebook (01–06); students pick a theme this week. Ask them to "
               "name the shaded window before you say it. Agriculture and blue carbon live in the "
               "VNIR, so Sentinel-2 gets part way; GHG and land cover live in the SWIR-2, where it "
               "has a single 175 nm band — that is the honest dividing line.")

d.handover("10_spectral_signatures_and_libraries.ipynb", [
    "Plot the course reference library and identify five absorption features by eye",
    "Compare Tanager, EnMAP, Sentinel-2 and Landsat response functions on the same axis",
    "Resample real spectra to Sentinel-2 and see which features survive",
    "Compute spectral-angle separability and find the pair that multispectral data cannot separate",
], minutes=90,
   notes="Circulate. The common sticking point is the difference between spectral sampling and FWHM.")

d.recap([
    "Hyperspectral = **contiguous, narrow** bands — a sampled spectrum, not a summary",
    "We analyse **surface reflectance**; gas retrievals work on **radiance**",
    "Absorption features have physical causes: pigments, water, minerals, gases",
    "Spectral detail is paid for in pixel size and swath — 30 m, tasked, not daily-global",
    "Use hyperspectral when the answer depends on a **feature's shape**, not just its brightness",
], next_up="Session 3 — Spectral signatures, sensor concepts and use cases (deeper into FWHM, SNR and mixed pixels)",
   notes="Close by returning to the one-sentence definition slide, and to the cube.")

d.references([
    "Goetz, A.F.H. et al. (1985). Imaging spectrometry for Earth remote sensing. Science 228, 1147–1153.",
    "Clark, R.N. (1999). Spectroscopy of rocks and minerals, and principles of spectroscopy. In: Manual of Remote Sensing, Vol. 3.",
    "Guanter, L. et al. (2015). The EnMAP spaceborne imaging spectroscopy mission. Remote Sensing 7, 8830–8857.",
    "Thompson, D.R. et al. (2015). Real-time remote detection and measurement for airborne imaging spectroscopy. AMT 8, 4383–4397.",
    "Planet (2024). Tanager-1 open data and STAC catalogue — www.planet.com/data/stac",
    "USGS Spectral Library Version 7 — www.usgs.gov/labs/spectroscopy-lab",
])

d.save("w1b_intro_hyperspectral_eo.pptx")
