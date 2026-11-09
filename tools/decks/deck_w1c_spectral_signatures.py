"""Week 1 · Session 3 — Spectral signatures, sensor concepts, and hyperspectral use cases."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

LIB = "10_spectral_signatures_and_libraries"

d = Deck("Spectral signatures and sensor concepts",
         "Week 1 · Session 3",
         notebook="10_spectral_signatures_and_libraries.ipynb",
         subtitle="Why materials absorb where they do, and what the sensor does to that signal",
         week="Week 1 · 9–12 November 2026")

d.objectives([
    "Explain the two physical mechanisms that produce absorption features in the 400–2500 nm range",
    "Identify diagnostic features of vegetation, water, soils, minerals and burnt surfaces by wavelength",
    "Use continuum removal and band depth to compare features between bright and dark materials",
    "Define band centre, FWHM, spectral sampling, SNR and ground sampling distance, and say why each matters",
    "Judge whether two materials remain separable once a spectrum is resampled to a multispectral sensor",
], notes="This is the deepest conceptual session of week 1. Tell students that everything they do later — "
         "indices, detection, unmixing, classification — depends on understanding this slide deck's "
         "wavelengths. The practical afterwards is notebook 10.")

d.section("1. Why materials have spectra", "Electrons and molecular bonds")

d.bullets("Two mechanisms, one spectrum", [
    "**Electronic transitions** — an electron absorbs a photon and jumps to a higher energy level",
    ("Strong, broad features; dominate the visible and near-infrared (400–1000 nm)", 1),
    "**Vibrational transitions** — molecular bonds stretch and bend at characteristic frequencies",
    ("Fundamental vibrations lie in the mid-infrared; what we see in the SWIR are their "
     "*overtones* and *combination bands* — weaker, but narrow and diagnostic", 1),
    "Everything between 400 and 2500 nm is one of these two, plus scattering",
], kicker="the physics in one slide",
   notes="The key insight for students: features in the SWIR are weak echoes of much stronger mid-infrared "
         "vibrations. That is exactly why you need narrow bands to see them — they are shallow.")

d.bullets("Electronic transitions: colour and iron", [
    "**Chlorophyll a and b** absorb strongly near 430 and 460 nm (blue) and 640 and 680 nm (red)",
    ("The gap between them is why healthy vegetation looks green", 1),
    "**Iron** dominates soil and rock colour: Fe³⁺ crystal-field absorption near 850–900 nm",
    ("Charge-transfer absorption in the blue and ultraviolet makes iron-rich soils red", 1),
    "Other pigments: carotenoids (~450–500 nm), anthocyanins (~530–550 nm), phycocyanin (~620 nm)",
    "These features are **broad** — a multispectral sensor can often see them",
], kicker="400–1000 nm",
   notes="Phycocyanin at 620 nm is the one to flag for the water-quality theme: it distinguishes "
         "cyanobacteria from other algae, and Sentinel-2 has no band there.")

d.bullets("Vibrational overtones: what the SWIR reveals", [
    "**O–H in liquid water** — strong at ~1450 and ~1940 nm, weaker at ~970 and ~1200 nm",
    "**Al–OH in clays** — ~2200 nm; kaolinite shows a characteristic doublet near 2160 and 2206 nm",
    "**Mg–OH** — ~2300–2350 nm, in chlorites and serpentines",
    "**CO₃ in carbonates** — ~2340 nm, with a secondary feature near 2160 nm",
    "**C–H in cellulose, lignin and hydrocarbons** — ~1700, ~2100 and ~2300 nm",
    "**Gypsum** — hydrated sulphate, with features near 1450, 1750 and 1940 nm",
    ("Methane absorbs near 2300 nm — the same window, which is why it competes with clay features", 1),
], kicker="1000–2500 nm",
   notes="Point out the collision: methane, Mg–OH, carbonate and C–H all sit between 2200 and 2350 nm. "
         "Discriminating them is a shape problem, not a brightness problem — hence hyperspectral.")

d.callout("A spectrum is an inventory of bonds and electrons.",
          "Read it that way and the features stop being curve shapes to memorise: each dip names a "
          "molecule or a mineral that is present in the pixel.",
          kicker="how to read a spectrum",
          notes="Encourage students to always ask 'what bond is doing that?' when they see a dip. It is the "
                "habit that separates interpretation from curve-fitting.")

d.section("2. The diagnostic features", "Wavelength by wavelength, material by material")

d.figure(f"The course reference library",
         f"{LIB}/00_2_the_library_one_material_group_at_a_ti.png",
         caption="19 image-derived spectra from the seven course scenes, grouped by material family",
         kicker="measured, not textbook",
         notes="These were extracted from the same scenes students will analyse, using only pure ESA "
               "WorldCover pixels. Ask them to name the family of each panel before you reveal it.")

d.table("Diagnostic features to memorise", ["Wavelength", "Feature", "Tells you about"], [
    ["430 / 460, 640 / 680 nm", "Chlorophyll absorption", "Photosynthetic activity, pigment content"],
    ["690–750 nm", "Red edge", "Chlorophyll concentration, stress, species"],
    ["850–900 nm", "Fe³⁺ crystal field", "Iron oxides in soils and spoil"],
    ["970, 1200 nm", "Weak liquid water", "Leaf and canopy water content"],
    ["1450, 1940 nm", "Strong liquid water", "Moisture (also atmospheric water vapour)"],
    ["~1700, 2100 nm", "C–H, cellulose and lignin", "Dry plant matter, crop residue"],
    ["2160 / 2206 nm", "Al–OH doublet", "Clay mineralogy (kaolinite, illite, smectite)"],
    ["~2340 nm", "CO₃ and Mg–OH", "Carbonates, altered minerals"],
], col_widths=[2, 2, 3], kicker="the cheat sheet",
   notes="Tell students to photograph this slide. It is the reference they will use in every practical, "
         "and the quiz for this session tests exactly these associations.")

d.bullets("Vegetation: the most structured spectrum in nature", [
    "Low reflectance in blue and red (pigment absorption), a small green peak near 550 nm",
    "**Red edge** — the steep rise between about 690 and 750 nm",
    ("Its inflection point shifts to **longer** wavelengths as chlorophyll increases "
     "(Guyot & Baret 1988 give a four-point linear estimate)", 1),
    "NIR plateau (750–1300 nm): multiple scattering at cell wall–air interfaces, set by leaf structure",
    "SWIR troughs at 1450 and 1940 nm deepen as canopy water increases",
    "As a leaf dries, water features weaken and **cellulose and lignin near 2100 nm** emerge",
], kicker="vegetation",
   notes="The drying sequence is the key teaching point: senescence moves the signal from water features "
         "to dry-matter features. That is the physical basis of the residue and fuel-load applications.")

d.bullets("Water: darkness with structure", [
    "Water absorbs increasingly towards the NIR — beyond ~900 nm, clear water is essentially black",
    "**All the information is in the visible**, where light penetrates and returns",
    "**Chlorophyll-a** in phytoplankton: absorption near 440 and 665 nm, fluorescence peak near 685 nm",
    "**Phycocyanin** near 620 nm marks cyanobacteria — a public-health signal",
    "**Suspended sediment** raises reflectance across the visible and shifts the peak towards red",
    "**Shallow water** adds bottom reflectance — sand, seagrass and coral mix into the signal",
], kicker="water",
   notes="Remind them that SWIR reflectance near zero over water is physically correct, and that slightly "
         "negative retrieved values are noise around zero — notebook 11 revisits this.")

d.bullets("Soils, minerals and man-made surfaces", [
    "Bare soil rises smoothly from blue to SWIR; the **slope** is set by iron and organic matter",
    "Superimposed on that slope: narrow Al–OH, Mg–OH and CO₃ features that name the mineralogy",
    "**Evaporites** — sabkha, salt flats, gypsum — are bright with hydration features",
    "**Burnt surfaces**: char and ash collapse the NIR plateau and raise SWIR reflectance",
    ("This inversion is what NBR measures, and why burn scars are unmistakable in the SWIR", 1),
    "**Man-made materials** — concrete, asphalt, metal and plastic roofing — have their own signatures",
], kicker="soils, minerals, materials",
   notes="The Korba coal scene and the Ho Chi Minh City roofs in notebook 14 are the practical versions of "
         "this slide. Mention that roofing plastics have C–H features, like dry vegetation.")

d.figure_bullets("Continuum removal: comparing features fairly",
                 f"{LIB}/01_3_zooming_into_absorption_features_conti.png",
                 ["Divide the spectrum by its upper convex hull",
                  "Brightness differences cancel; only the **feature shape** remains",
                  "**Band depth** = 1 − R(centre) / R(continuum)",
                  "Now a dark coal surface and a bright spoil heap can be compared directly"],
                 caption="Raw spectra (left) and their continuum-removed form (right)",
                 kicker="the standard tool",
                 notes="Clark and Roush (1984) introduced this as the standard way to compare spectra. "
                       "Stress that band depth is the quantitative output: it is a number you can map.")

d.table("Band depths measured in the course library", ["Material", "Chl 680", "Al–OH 2200", "CO₃ 2340"], [
    ["Mangrove", "0.891", "−0.204", "0.070"],
    ["Irrigated crop", "0.784", "−0.150", "0.015"],
    ["Chaparral, unburned", "0.669", "−0.120", "0.019"],
    ["Mine spoil, bright", "0.030", "0.094", "−0.001"],
    ["Sand beach", "0.024", "0.044", "0.024"],
    ["Sabkha salt flat", "−0.027", "−0.027", "0.094"],
], col_widths=[3, 1, 1, 1], kicker="real numbers from notebook 10",
   notes="Two lessons here. Vegetation has deep chlorophyll absorption and no clay feature; mine spoil is "
         "the reverse. And the sabkha's carbonate depth of 0.094 is the strongest in the library.")

d.section("3. What the sensor does to the signal", "Band centre, FWHM, SNR, pixel size")

d.figure_bullets("Band centre, sampling and resolution",
                 f"{LIB}/02_4_1_band_centres_spectral_sampling_and_s.png",
                 ["**Band centre** — the wavelength a band is tuned to",
                  "**Spectral sampling** — the spacing between adjacent centres (Tanager ≈ 5 nm)",
                  "**Spectral resolution** — the width of one band's response, its **FWHM** (≈ 5.2–6.8 nm)",
                  "Sampling and resolution are different numbers, and both matter"],
                 caption="Tanager band centres and their widths",
                 kicker="three numbers people confuse",
                 notes="The classic exam mistake is treating sampling and FWHM as the same thing. A sensor "
                       "can sample every 5 nm with 30 nm wide bands and still blur every narrow feature.")

d.figure_bullets("The same scene through four sensors",
                 f"{LIB}/04_4_2_spectral_response_functions_tanager_.png",
                 ["Each curve is a band's spectral response function",
                  "Tanager: 426 bands · EnMAP: 224 · Sentinel-2: 13 · Landsat 8/9: 7 reflective",
                  "Sentinel-2 B12 spans about 175 nm — the whole Al–OH and CO₃ region in one number",
                  "**A feature narrower than a band cannot be recovered afterwards**"],
                 caption="Spectral response functions on a common axis",
                 kicker="why band width decides what you can ask",
                 notes="Link forward: this is why the clay-versus-carbonate question in the quiz has only "
                       "one defensible answer.")

d.figure_bullets("Signal-to-noise: not all bands are equal",
                 f"{LIB}/06_4_4_signal_to_noise_ratio_snr_per_band.png",
                 ["SNR is highest where solar irradiance and surface reflectance are high",
                  "It collapses below ~400 nm: little solar energy, weak detector response",
                  "It collapses inside the water-vapour windows: the photons never reach the ground",
                  "It falls at the SWIR detector edge beyond ~2450 nm",
                  "**Consequence:** we drop those bands before analysis, as notebook 11 shows"],
                 caption="Per-band SNR estimated from the Tanager uncertainty layer",
                 kicker="which bands can you trust",
                 notes="Tanager ships a per-pixel uncertainty cube, so SNR can be measured rather than "
                       "assumed — a luxury most datasets do not give you.")

d.figure_bullets("One pixel, several materials",
                 f"{LIB}/05_4_3_spatial_resolution_and_mixed_pixels.png",
                 ["At 30 m, most pixels mix several materials",
                  "Mixing is approximately **linear in area fraction** for side-by-side materials",
                  "A measured pixel of NDVI 0.44 turned out to be **9 % mangrove, 91 % water**",
                  "Indices mislead on mixed pixels; **unmixing** estimates the fractions instead"],
                 caption="A mixed pixel decomposed into its endmembers",
                 kicker="the mixed-pixel problem",
                 notes="This example is measured in notebook 10, not invented. It is the strongest argument "
                       "for the unmixing session in week 2.")

d.bullets("The trade-offs you cannot escape", [
    "Splitting light into 426 narrow bands leaves fewer photons per band → larger pixels preserve SNR",
    "**Ground sampling distance:** Tanager and EnMAP both sit at 30 m for this reason",
    "**Swath:** narrow (tens of kilometres), so acquisitions are **tasked**, not continuous",
    "**Revisit:** irregular — the Tanager open archive holds 153 unique scenes so far",
    "**Plan projects around what was acquired**, not around what you wish had been",
], kicker="spectral, spatial, radiometric",
   notes="Repeat the planning message from session 1: check data availability before committing to an "
         "area. Notebook 16 is the tool for that, and it is used in the week 2 scoping session.")

d.section("4. Libraries, resampling and separability", "Can you still tell the materials apart?")

d.bullets("Two kinds of spectral library", [
    "**Laboratory libraries** — USGS splib07, ECOSTRESS: pure samples, controlled illumination",
    ("Ideal reference shapes, but no atmosphere, no mixing, no canopy structure", 1),
    "**Image-derived libraries** — mean spectra of homogeneous areas in your own scene",
    ("Same sensor, same atmosphere, same mixing — directly comparable to your pixels", 1),
    "The course ships an image-derived library of 19 materials, built from pure WorldCover pixels",
    "Use lab spectra to *identify*, image spectra to *classify*",
], kicker="reference spectra",
   notes="Mention the practical catch: a lab spectrum must be convolved to the sensor's response "
         "functions before you compare it with satellite data. Notebook 10 has the function for that.")

d.figure_bullets("What Sentinel-2 would see",
                 f"{LIB}/07_5_what_does_sentinel_2_see_resampling_th.png",
                 ["Convolve each library spectrum with Sentinel-2's response functions",
                  "The broad shape survives: vegetation still looks like vegetation",
                  "The **narrow features vanish** — the clay doublet becomes a single number",
                  "This is the honest test of whether your project needs hyperspectral data"],
                 caption="Library spectra before and after resampling to Sentinel-2",
                 kicker="resampling",
                 notes="Have students predict which features will survive before you show the result. "
                       "Most guess correctly for water, and are surprised by the SWIR minerals.")

d.figure_bullets("Separability: the spectral angle",
                 f"{LIB}/08_5_1_spectral_separability_with_the_spect.png",
                 ["The angle between two spectra treated as vectors",
                  "Insensitive to brightness — it compares **shape**, not magnitude",
                  "Small angle = hard to tell apart; large angle = easily separable",
                  "Across all 171 library pairs, **71 % became less separable** after resampling to Sentinel-2"],
                 caption="Pairwise spectral angles within the course library",
                 kicker="a number for 'can I tell these apart'",
                 notes="The median pair retained 91 % of its angle, so the loss is real but not catastrophic "
                       "on average. The interesting cases are the extremes on the next slide.")

d.table("Which pairs lose the most", ["Material pair", "Tanager", "Sentinel-2", "Retained"], [
    ["Mangrove vs tropical tree cover", "10.44°", "7.24°", "69 %"],
    ["Sabkha vs desert sand", "2.91°", "1.97°", "68 %"],
    ["Irrigated crop vs sugar cane", "10.85°", "8.23°", "76 %"],
    ["Dense urban vs bright mine spoil", "2.83°", "2.49°", "88 %"],
    ["Coal mine surface vs burn scar", "12.69°", "17.35°", "137 %"],
], col_widths=[4, 1, 1, 1], kicker="measured in notebook 10",
   notes="Note the last row honestly: a few pairs become *more* separable, because broad bands can average "
         "away noise. Good science means reporting that, not hiding it.")

d.figure_bullets("Matching a real pixel to the library",
                 f"{LIB}/09_6_matching_real_pixels_to_the_library_sa.png",
                 ["Pick a pixel, compute the angle to every library spectrum, take the smallest",
                  "Mangrove pixel matched *mangrove* at **0.9°**; the burn scar matched *burn_scar* at 1.6°",
                  "The second-best match tells you how confident the identification is",
                  "This is Spectral Angle Mapper — the basis of the week 2 detection session"],
                 caption="Nearest library match for six hand-picked pixels",
                 kicker="identification in practice",
                 notes="Emphasise the second-best match: a 0.9° first and 7.1° second is a confident "
                       "identification; two matches within a degree of each other is not.")

d.bullets("So when do you actually need a spectrum?", [
    "**Yes** — identifying materials: minerals, roofing, crop residue, algal pigments",
    "**Yes** — detecting gases: the methane window at 2300 nm",
    "**Yes** — sub-pixel work: unmixing fractions rather than mapping a dominant class",
    "**Maybe** — stress detection: narrow red-edge bands beat broad ones, but not always decisively",
    "**No** — mapping obvious extent: vegetation, water, built-up; Sentinel-2 is cheaper and more frequent",
    ("Say so in your project when multispectral would do — the rubric rewards honesty", 1),
], kicker="use-case triage",
   notes="This slide is deliberately the last before the practical. Students who internalise it write much "
         "stronger scoping canvases in week 2.")

d.handover("10_spectral_signatures_and_libraries.ipynb", [
    "Plot the library by material family and find the features from the cheat-sheet table",
    "Apply continuum removal and measure band depths for clay, carbonate and chlorophyll",
    "Compare Tanager, EnMAP, Sentinel-2 and Landsat response functions and SNR",
    "Resample the library to Sentinel-2 and compute how much separability is lost",
    "Match real pixels to the library with the spectral angle",
], minutes=90,
   notes="Common sticking point: the difference between spectral sampling and FWHM. Second one: students "
         "expect resampling to destroy everything, and are surprised that broad shapes survive.")

d.recap([
    "Features come from **electronic transitions** (VNIR) and **vibrational overtones** (SWIR)",
    "Learn the wavelengths: 680 chlorophyll · red edge · 970/1200/1450/1940 water · 2100 cellulose · 2200 Al–OH · 2340 CO₃",
    "**Continuum removal and band depth** make features comparable between bright and dark materials",
    "Sampling, FWHM, SNR and GSD decide which questions the data can answer",
    "Resampling to Sentinel-2 cost separability in **71 % of library pairs** — that is the value of narrow bands",
], next_up="Session 4 — Hyperspectral data access, visualisation and exploration",
   notes="Point students at quizzes/quiz_w1a_intro_spectral_signatures.md, which covers sessions 2 and 3.")

d.references([
    "Clark, R.N. & Roush, T.L. (1984). Reflectance spectroscopy: quantitative analysis. JGR 89(B7), 6329–6340.",
    "Clark, R.N. (1999). Spectroscopy of rocks and minerals, and principles of spectroscopy. Manual of Remote Sensing, Vol. 3.",
    "Guyot, G. & Baret, F. (1988). Utilisation de la haute résolution spectrale pour suivre l'état des couverts végétaux.",
    "Kruse, F.A. et al. (1993). The Spectral Image Processing System (SIPS) — the Spectral Angle Mapper. RSE 44, 145–163.",
    "Kokaly, R.F. et al. (2017). USGS Spectral Library Version 7. USGS Data Series 1035.",
    "Meerdink, S.K. et al. (2019). The ECOSTRESS spectral library version 1.0. RSE 230, 111196.",
])

d.save("w1c_spectral_signatures_sensors.pptx")
