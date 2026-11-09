"""Week 1 · Session 1 — Course orientation and hyperspectral course objectives."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("Course orientation and objectives",
         "Week 1 · Session 1",
         subtitle="Four weeks from spectra to a validated, deliverable product",
         week="Space Academy 2026 · Hyperspectral course")

d.objectives([
    "Describe how the four weeks fit together and what is expected each week",
    "Find your way around the course material: notebooks, exercises, quizzes, templates",
    "Set up the toolchain and open your first Tanager scene",
    "State how you will be assessed, and what the final project must contain",
], notes="Keep this session short and practical. The goal is that nobody is blocked on setup "
         "tomorrow morning. Finish with everyone having run notebook 00 at least once.")

d.section("1. Why this course", "Imaging spectroscopy is arriving in the region")

d.callout("Most satellites tell you how bright a surface is.\nAn imaging spectrometer tells you what it is made of.",
          "That shift — from brightness to composition — is what the next four weeks are about, and it is "
          "why the UAE and its partners are investing in hyperspectral missions.",
          kicker="the premise",
          notes="Anchor the course in a concrete example: two fields can have identical NDVI while one is "
                "water-stressed and the other is not. Ask the room for examples from their own work.")

d.bullets("Who this course is for", [
    "Researchers and engineers new to imaging spectroscopy, but comfortable with Python basics",
    "Domain specialists — agriculture, water, urban, environment — who need more than an index",
    "Data scientists who know machine learning but not the physics of a spectrum",
    "**No prior remote sensing experience is assumed.** Every concept is introduced from scratch",
    ("Teams of 3–5 for the project; mixed backgrounds work best", 1),
], kicker="audience",
   notes="Ask for a show of hands: who has used Sentinel-2, who has trained a classifier, who has "
         "worked with field spectra. Use the answers to calibrate the depth of the next two sessions.")

d.table("The four weeks", ["Week", "Dates", "Mode", "Focus"], [
    ["1", "2–5 Nov 2026", "onsite + online", "Concepts, data access, preprocessing"],
    ["2", "9–12 Nov 2026", "online", "Workflows, features, detection, classification, project scoping"],
    ["3", "16–19 Nov 2026", "online", "GeoAI, validation, project development, interim review"],
    ["4", "23–26 Nov 2026", "onsite + online", "Advanced analytics, implementation, presentation, evaluation"],
], kicker="shape of the course",
   notes="Weeks 2 and 3 are one session per day; weeks 1 and 4 are denser, with five sessions across "
         "four days, Monday to Thursday. Warn students that project work runs in parallel from week 2 onwards.")

d.bullets("By the end you will be able to", [
    "Explain hyperspectral principles and read a spectrum physically, not just statistically",
    "Prepare a scene properly: masks, bad bands, subsets, exports",
    "Extract features and apply detection, unmixing and classification methods",
    "Apply AI and GeoAI methods, and know when a simpler baseline is enough",
    "**Validate** results honestly and communicate them to a non-technical user",
], kicker="learning outcomes",
   notes="These are the syllabus outcomes in plain language. Point out that 'validate honestly' carries "
         "the heaviest weight in the final rubric — 30 of 100 marks.")

d.section("2. The material", "Two notebook families, plus everything around them")

d.bullets("How the material is organised", [
    "**Theme notebooks 00–06** — one per challenge theme: data access and first indices",
    "**Method notebooks 10–31** — the techniques, in the order the syllabus teaches them",
    "**exercises/** — graded tasks for each theme notebook, with worked solutions",
    "**quizzes/** — short concept checks after the lecture sessions",
    "**templates/** — scoping canvas, project notebook, checklists, rubric, slide outline",
    "**hsi_utils.py** — the shared helper module every method notebook imports",
    ("Methods by week: 10–11 · 12–16 · 20–21 · 30–31, one notebook per session", 1),
], kicker="folder map",
   notes="Stress that hsi_utils is meant to be read, not treated as a black box: it is only a few hundred "
         "lines and it is where the file handling, masking and export conventions live. Each method "
         "notebook is the practical half of one session: two to three hours of lab, plus exercises.")

d.figure("Where the course data comes from",
         "16_scene_finder/01_3_a_world_view.png",
         caption="153 unique Tanager open-data scenes, September 2024 to October 2025",
         kicker="the archive",
         notes="Planet's Tanager open data is a tasked archive, not wall-to-wall coverage: 153 unique "
               "scenes worldwide so far. Project areas must be chosen from what actually exists.")

d.figure_bullets("The seven course scenes",
                 "12_processing_workflow/01_4_batch_processing_all_course_scenes.png",
                 ["**Malibu** — the Franklin fire scar, plus a second date after the Palisades fire",
                  "**Korba, India** — open-cast coal mines and minerals",
                  "**Usulután, El Salvador** — mangroves and estuary; our classification testbed",
                  "**Ho Chi Minh City** — urban materials and industrial roofs",
                  "**Al Dhafra, UAE** — sabkha and shallow coastal water",
                  "**Konya, Türkiye** — irrigated agriculture on a dry plain"],
                 caption="True-colour quicklooks of the course scenes",
                 image_left=True, kicker="what you will analyse",
                 notes="All seven are already on the course machines. The UAE scene teaches the hardest "
                       "lesson of week 1: the cloud mask flags bright sabkha as cloud under a clear sky.")

d.section("3. Tools and setup", "What you install, and what you only need to know exists")

d.bullets("The toolchain", [
    "**Python + Jupyter** — the main working environment for the whole course",
    "**numpy, xarray, rasterio, scikit-learn, PyTorch** — the analysis stack",
    "**hsi_utils.py** — course helpers for reading, masking and exporting Tanager data",
    "**QGIS with EnMAP-Box and HyperCoast** — the desktop GIS session later in the course",
    "**Space42 gIQ** — the professional platform, where access is provided",
    ("Everything in the course runs on a laptop CPU; no GPU is required", 1),
], kicker="what you will use",
   notes="Reassure students about hardware: the heaviest notebook trains two small CNNs on CPU in about "
         "six minutes. Nobody needs a workstation.")

d.code("Setting up, start to finish", """
# 1. install the dependencies (once)
pip install -r requirements.txt

# 2. open a scene — finds the local file, or downloads it from Planet's STAC
import hsi_utils as hu
scene = hu.get_scene("20250608_091605_90_4001")
print(scene.summary())

# 3. read a window of good bands: (bands, rows, cols) + wavelengths in nm
cube, wl = scene.read_cube(window=(200, 400, 300, 500))
""", caption="If step 2 prints a scene summary, your environment is correct.",
   notes="Do this live and let them follow. The common failure is a corporate proxy blocking the "
         "download — for that case the scenes are already on the shared drive.")

d.bullets("Ground rules", [
    "**Reproducibility:** a notebook that only runs on your machine does not count as a result",
    "**Attribution:** credit every dataset — Tanager is CC-BY-4.0 © Planet Labs PBC",
    "**AI assistants are allowed** — but you must understand and be able to explain every line you submit",
    "**Ask early.** If you are stuck for more than fifteen minutes, ask; the sessions build on each other",
    ("Teams keep ownership of their work, as in the 813 Challenge", 1),
], kicker="how we work",
   notes="The AI rule is worth dwelling on: in the final evaluation you will ask teams to explain their "
         "own code, and that is where unexplained generated code becomes obvious.")

d.section("4. Assessment and the project", "What you hand in, and how it is marked")

d.table("Assessment", ["Component", "When", "Weight"], [
    ["Assignment W1 — scene exploration report", "start of week 2", "10 %"],
    ["Assignment W2 — detection and classification", "start of week 3", "15 %"],
    ["Assignment W3 — a validated AI map", "interim review, week 3", "15 %"],
    ["Final graduation project", "25 November", "60 %"],
    ["Quizzes", "after lecture sessions", "formative, not graded"],
], col_widths=[4, 2, 1], kicker="marks",
   notes="Point out that the three assignments are stepping stones to the project, not extra work: each "
         "one produces a component the final submission needs anyway.")

d.table("How the final project is marked", ["Criterion", "Weight", "The question it asks"], [
    ["Validity", "30", "Is the result scientifically sound and properly validated?"],
    ["Relevance", "20", "Does it answer the problem, completely and reproducibly?"],
    ["Impact", "20", "Who benefits, and by how much?"],
    ["Creativity", "15", "Does it use hyperspectral information in a meaningful way?"],
    ["Presentation", "15", "Is the story clear and the delivery convincing?"],
], col_widths=[2, 1, 4], kicker="the rubric",
   notes="These are the five 813 Challenge criteria. Tell students to read templates/evaluation_rubric.md "
         "in week 2, not in week 4 — the level descriptors tell them exactly what 'excellent' looks like.")

d.bullets("Project milestones", [
    "**Week 2, Thu 12 Nov** — scoping canvas: problem, user, area, data, validation plan",
    "**Week 3, Tue–Wed** — working method on one scene, in the project notebook template",
    "**Week 3, Thu 19 Nov** — interim review: first validated map plus the QA checklist",
    "**Week 4, Mon–Tue** — refinement, uncertainty, pipeline, tests, product mock-up",
    "**Week 4, Thu 26 Nov** — submission and a 12-minute presentation",
], kicker="from idea to submission",
   notes="Emphasise that scoping happens in week 2, not week 4. Teams that pick their area and check data "
         "availability early are the ones that finish.")

d.handover("00_EO_data_quickstart_notebook.ipynb", [
    "Install the requirements and check that `import hsi_utils` works",
    "Open one of the seven course scenes and print its summary",
    "Run notebook 00 to see a STAC search, a quicklook and your first spectral index",
    "Skim `README.md` so you know where the exercises, quizzes and templates live",
], minutes=45,
   notes="Circulate and fix environments. Anyone finishing early can start exercises/ex_00, which is the "
         "companion exercise set for this notebook.")

d.recap([
    "Four weeks: concepts and preprocessing, methods, GeoAI and validation, then the project",
    "Theme notebooks 00–06 for applications; method notebooks 10–31 for techniques",
    "Everything runs on a laptop; `hsi_utils.py` handles the file plumbing",
    "60 % of the mark is the project — and **validity carries the most weight**",
    "Scoping starts in week 2: pick your problem and check the data early",
], next_up="Session 2 — Introduction to hyperspectral Earth observation",
   notes="Close by asking each person to name, in one sentence, a problem from their own work that they "
         "would like to attack. Those sentences become project ideas in week 2.")

d.references([
    "Course README and folder map — README.md (instructor detail: INSTRUCTOR.md)",
    "Final project brief — assignments/final_project_brief.md",
    "Evaluation rubric — templates/evaluation_rubric.md",
    "Project scoping canvas — templates/project_scoping_template.md",
    "Planet Tanager open data (CC-BY-4.0) — www.planet.com/data/stac",
    "Arab Youth Space Hackathon: 813 Challenge — spaceacademy-hackathons.space.gov.ae",
])

d.save("w1a_course_orientation.pptx")
