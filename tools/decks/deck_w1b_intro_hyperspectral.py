"""Week 1 · Session 2 — Introduction to hyperspectral Earth observation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("Introduction to hyperspectral Earth observation",
         "Week 1 · Session 2",
         notebook="10_spectral_signatures_and_libraries.ipynb",
         subtitle="From three colours to 426 — what a continuous spectrum buys you",
         week="Week 1 · 2–5 November 2026")

d.objectives([
    "Explain what makes a sensor *hyperspectral*, and why band count alone is not the definition",
    "Describe the electromagnetic quantities we measure: radiance, reflectance, emissivity",
    "Name the main spaceborne imaging spectrometers and their trade-offs",
    "Say what Tanager-1 measures, at what spectral and spatial sampling",
    "Judge when hyperspectral data is worth the extra cost and complexity",
], notes="Set expectations: today is conceptual, the practical starts after lunch with notebook 10. "
         "Ask the room who has used Sentinel-2 before — calibrate depth accordingly.")

d.section("1. What is hyperspectral?", "Sampling the spectrum instead of summarising it")

d.callout("A multispectral sensor summarises the spectrum.\nA hyperspectral sensor samples it.",
          "Sentinel-2 gives you 13 numbers per pixel, each averaging tens to hundreds of nanometres. "
          "Tanager gives you 426 numbers, each ~5 nm wide — a curve you can interpret physically.",
          kicker="the one-sentence definition",
          notes="This is the slide to repeat at the end of the day. Everything else follows from it.")

d.bullets("The three defining properties", [
    "**Contiguous** bands: no gaps between them, so the result is a spectrum, not a set of samples",
    "**Narrow** bands: 3–10 nm, narrow enough to resolve real absorption features",
    "**Many** bands: 100–500, which is a consequence of the first two, not the definition itself",
    ("A 20-band sensor with wide, scattered bands is multispectral; a 100-band sensor "
     "sampling 400–1000 nm continuously is hyperspectral", 1),
], kicker="definition",
   notes="Students often answer 'more than X bands' in the quiz. Push back: contiguity and width matter more.")

d.figure_bullets("What the sensors actually see",
                 "10_spectral_signatures_and_libraries/03_4_2_spectral_response_functions_tanager_.png",
                 ["Each curve is one band's spectral response function",
                  "Sentinel-2 B12 is ~175 nm wide — it averages the whole SWIR-2 region",
                  "Tanager samples that same region with ~40 bands",
                  "**Consequence:** features narrower than a band can never be recovered"],
                 caption="Spectral response functions, same wavelength axis",
                 notes="Point at the SWIR-2 region: this is exactly where clay, carbonate and methane sit.")

d.section("2. What we measure", "Radiance, reflectance, and why the difference matters")

d.bullets("From photons to a number you can interpret", [
    "The sensor measures **at-sensor radiance** — W m⁻² sr⁻¹ µm⁻¹ — which includes the atmosphere",
    "**Atmospheric correction** removes scattering and gas absorption to give **surface reflectance**",
    "Reflectance is unitless (0–1): the fraction of incident light the surface returns",
    "Only reflectance is comparable between dates, places and sensors",
    ("Tanager open data ships both: `ortho_radiance_hdf5` and `ortho_sr_hdf5` — we use the latter", 1),
], kicker="physical quantities",
   notes="Analogy: radiance is the photo as taken, reflectance is the photo after removing the "
         "lighting and the haze. Retrievals of gases (methane) work on radiance, not reflectance.")

d.bullets("Why a leaf looks the way it does", [
    "**Blue and red** absorbed by chlorophyll a/b → low reflectance, hence green appearance",
    "**Red edge** (~690–750 nm): the steepest slope in nature, position shifts with chlorophyll content",
    "**NIR plateau** (750–1300 nm): scattering at cell wall–air interfaces, sensitive to leaf structure",
    "**SWIR** (1400–2500 nm): dominated by liquid water absorption at ~1450 and ~1940 nm",
    "**Dry matter** (cellulose, lignin) absorbs near 2100 nm — visible only once the leaf dries",
], kicker="vegetation",
   notes="Draw the shape on the whiteboard as you talk. Students remember the drawing, not the slide.")

d.figure("Real Tanager spectra, grouped by material",
         "10_spectral_signatures_and_libraries/00_2_the_library_one_material_group_at_a_ti.png",
         caption="Median spectra of homogeneous areas in the course scenes (data/spectral_library)",
         kicker="the course reference library",
         notes="These are measured, not textbook, spectra — built from the same scenes the students "
               "will analyse. Ask: which curve is water, and how do you know?")

d.section("3. The missions", "Airborne heritage, today's satellites, what is coming")

d.table("Spaceborne imaging spectrometers", ["Mission", "Agency", "Since", "Bands / range", "GSD"], [
    ["Hyperion (EO-1)", "NASA", "2000–2017", "220 · 400–2500 nm", "30 m"],
    ["DESIS (ISS)", "DLR/Teledyne", "2018", "235 · 400–1000 nm", "30 m"],
    ["PRISMA", "ASI (Italy)", "2019", "239 · 400–2500 nm", "30 m"],
    ["EnMAP", "DLR (Germany)", "2022", "224 · 420–2450 nm", "30 m"],
    ["EMIT (ISS)", "NASA", "2022", "285 · 380–2500 nm", "60 m"],
    ["Tanager-1", "Planet", "2024", "426 · 380–2500 nm", "30 m"],
    ["CHIME / SBG", "ESA / NASA", "planned", "continuous VSWIR", "~30 m"],
], kicker="who flies what",
   notes="Note the pattern: all VSWIR spectrometers sit at 30 m or coarser. Spectral detail costs "
         "spatial detail and swath — that is the fundamental trade-off of the next slide.")

d.bullets("The trade-off triangle", [
    "Every photon is divided between **spectral**, **spatial** and **radiometric** resolution",
    "Splitting light into 426 narrow bands leaves less energy per band → larger pixels keep SNR up",
    "Narrow swaths (Tanager ~18 km) mean **targeted tasking**, not global daily coverage",
    "**Practical consequence:** hyperspectral complements Sentinel-2, it does not replace it",
], kicker="why 30 m and not 10 m",
   notes="Pre-empt the common project mistake: planning a study that needs weekly hyperspectral "
         "coverage of a whole country. Tasked scenes, not wall-to-wall time series.")

d.figure("Tanager-1 open data: six of the course scenes",
         "12_processing_workflow/01_4_batch_processing_all_course_scenes.png",
         caption="Malibu · Korba · El Salvador · Ho Chi Minh City · Al Dhafra · Konya",
         kicker="what you will work with",
         notes="Every scene here is CC-BY-4.0 open data from Planet's STAC catalogue, and all six are "
               "already on the course machines.")

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

d.bullets("The six challenge themes, seen spectrally", [
    "**Agriculture** — red edge, leaf water, cellulose: stress before it is visible",
    "**Land cover and urban** — material discrimination: roof and pavement types, not just 'built-up'",
    "**Air quality and GHG** — gas absorption in the SWIR, the 2300 nm methane window",
    "**Disasters** — char and ash signatures, burn severity, flood extent",
    "**Blue carbon** — mangrove species, submerged vegetation, pigment detail",
    "**Water quality** — chlorophyll-a, phycocyanin, sediment, all in narrow visible bands",
], kicker="from physics to applications",
   notes="Each bullet maps to one theme notebook (01–06). Students pick a theme this week.")

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
   notes="Close by returning to the one-sentence definition slide.")

d.references([
    "Goetz, A.F.H. et al. (1985). Imaging spectrometry for Earth remote sensing. Science 228, 1147–1153.",
    "Clark, R.N. (1999). Spectroscopy of rocks and minerals, and principles of spectroscopy. In: Manual of Remote Sensing, Vol. 3.",
    "Guanter, L. et al. (2015). The EnMAP spaceborne imaging spectroscopy mission. Remote Sensing 7, 8830–8857.",
    "Thompson, D.R. et al. (2015). Real-time remote detection and measurement for airborne imaging spectroscopy. AMT 8, 4383–4397.",
    "Planet (2024). Tanager-1 open data and STAC catalogue — www.planet.com/data/stac",
    "USGS Spectral Library Version 7 — www.usgs.gov/labs/spectroscopy-lab",
])

d.save("w1b_intro_hyperspectral_eo.pptx")
