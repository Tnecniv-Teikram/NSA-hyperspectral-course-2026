"""Week 4 · Sessions 3–5 — Presentation preparation, submission and final evaluation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("Presenting, submitting and being evaluated",
         "Week 4 · Sessions 3–5",
         notebook="templates/presentation_template.md",
         subtitle="Twelve minutes to convince a room that your map can be trusted and used",
         week="Week 4 · 23–26 November 2026")

d.objectives([
    "Structure a 12-minute technical presentation that a mixed audience can follow",
    "Present a map and a validation table so a non-specialist draws the right conclusion",
    "Answer the three questions every Earth observation project is asked",
    "Submit a complete, reproducible project folder",
    "Read the rubric the way the evaluators will read your work",
], notes="Sessions 3 to 5 in one deck: rehearsal, submission, evaluation. Most of these days is teams "
         "rehearsing — keep this to about 40 minutes and then start the run-throughs.")

d.section("1. The story arc", "Problem → data → method → result → so what")

d.callout("The audience decides in the first two minutes\nwhether your result matters.",
          "Start with the problem and the person who has it. A presentation that opens with the sensor "
          "specification has already lost half the room.",
          kicker="how technical talks fail",
          notes="Ask who in the audience of the final evaluation is not a remote sensing specialist — "
                "usually most of the panel. They judge relevance and impact, not your code.")

d.table("Twelve slides, twelve minutes", ["#", "Slide", "Time"], [
    ["1–3", "Title · the problem · today's solution and its gap", "2:00"],
    ["4", "Why hyperspectral — one spectrum, key wavelengths marked", "1:00"],
    ["5–6", "Data · method (a diagram, not code)", "2:20"],
    ["7", "The result — one large, readable map", "1:30"],
    ["8", "Does it work? Validation, baseline, uncertainty", "1:30"],
    ["9–10", "Limitations · from notebook to product", "2:10"],
    ["11–12", "Impact and next steps · credits", "1:00"],
], kicker="templates/presentation_template.md", col_widths=[1, 5, 1],
   notes="The timings add to about 11:30, leaving buffer. Teams that skip the limitations slide to save time "
         "invariably get asked about limitations first.")

d.bullets("Titles that do the work for you", [
    "Write the **takeaway** as the slide title, as a full sentence",
    "'Mangrove loss concentrates near shrimp ponds' — not 'Results'",
    "One message per slide; if it needs two, it is two slides",
    "The audience reads the title before you speak — make that sentence count",
], kicker="slide titles",
   notes="Have each team rewrite their results slide title as a sentence during the session. It is the "
         "fastest single improvement to most decks.")

d.figure_bullets("The slide that convinces a sceptic",
                 "10_spectral_signatures_and_libraries/00_2_the_library_one_material_group_at_a_ti.png",
                 ["Show a **spectrum**, not a specification table",
                  "Mark the two or three wavelengths your method actually uses",
                  "Say in one sentence what the feature is caused by",
                  "This is where you earn the Creativity mark for using hyperspectral properly"],
                 caption="Annotated spectra make the hyperspectral argument in seconds",
                 kicker="slide 4",
                 notes="A spectrum with three annotated features does more for credibility than any amount of "
                       "text about band counts. It also pre-empts the 'why not Sentinel-2' question.")

d.section("2. Showing results honestly", "Maps and numbers a non-specialist can read")

d.figure_bullets("How to present a map",
                 "20_geoai_deep_learning/05_8_from_model_to_map.png",
                 ["Give context: where is this, how big, what am I looking at",
                  "Legend in plain words — 'mangrove', not 'class 95'",
                  "Keep the true-colour image beside the map for reference",
                  "Same colours for the same classes on every slide",
                  "Scale bar and north arrow; state the pixel size"],
                 caption="Reference image, labels and model output side by side",
                 kicker="slide 7",
                 notes="Point out how much easier the map is to judge with the true-colour panel next to it. "
                       "Panels without context invite the question 'is that a river or a road?'")

d.figure_bullets("How to present validation",
                 "21_validation_accuracy_assessment/04_5_3_analysis_area_weighted_error_matrix_.png",
                 ["Lead with the **honest** number and its uncertainty: 'OA 0.60 ± 0.04'",
                  "Put the per-class table on the slide; name the weakest class",
                  "Show the **baseline** beside your model so the gain is visible",
                  "Translate it: 'we miss one mangrove pixel in eight, at the water edge'",
                  "Never show accuracy from a random pixel split"],
                 caption="Area-adjusted accuracy and area, with 95 % confidence intervals",
                 kicker="slide 8",
   notes="The translation bullet is the one that lands with non-specialists. Practise it: every team should "
         "have one sentence that converts their metric into an operational consequence.")

d.bullets("Limitations without undermining yourself", [
    "Two or three real limitations, each with what you would do about it",
    "Frame as **scope**, not failure: 'validated for this estuary, not yet for Gulf mangroves'",
    "Name the data limits: single date, 30 m mixed pixels, 2021 reference labels",
    "A team that names its limitations is trusted more, not less",
], kicker="slide 9",
   notes="Contrast two phrasings out loud: 'our model does not work on other sites' versus 'validated here, "
         "the next step is a second site'. Same fact, very different impression.")

d.section("3. The three questions", "Every team gets asked these")

d.bullets("Prepare an answer for each, and rehearse it", [
    "**How do you know it is right?** → sampling design, independent test data, the CI, the baseline",
    "**Why not just use Sentinel-2?** → name the feature and its width; show the resampled comparison",
    "**What would operational use take?** → repeat coverage, runtime, cost, who runs it, how often",
    ("If multispectral genuinely would do, say so and explain what hyperspectral adds beyond it", 1),
    "Every team member should be able to answer all three, not just the presenter",
], kicker="panel questions",
   notes="Run these as a drill in the rehearsal: pick a team member at random and ask one of the three. "
         "Thirty seconds, no slides.")

d.section("4. Rehearse, submit, be evaluated", "Wednesday and Thursday of the final week")

d.bullets("Rehearsal discipline", [
    "Time it twice, out loud, standing — silent reading is always faster than speaking",
    "Cut, do not speed up: at 12 minutes something must go, and it is never the validation",
    "Decide who speaks when, and how you hand over",
    "Fonts at least 18 pt; no screenshots of code; figures readable from the back",
    "Bring a PDF on a USB stick and a copy online; record a demo video as a fallback",
], kicker="two run-throughs minimum",
   notes="Insist on standing and speaking aloud. Teams that rehearse silently are routinely three minutes "
         "over on the day.")

d.code("The submission folder", """
team_<name>_hyperspectral_project/
├── README.md              # problem, data, method, key results, how to run
├── project.ipynb          # executed, runs top to bottom
├── outputs/               # *.tif (COG) + *_metadata.json + figures/
├── validation/            # metrics tables, confusion matrix, plots
├── presentation.pdf
└── requirements.txt       # anything beyond the course requirements
""", kicker="templates/submission_checklist.md",
   caption="No raw HDF5 files — scene IDs are enough for anyone to re-download them",
   notes="Walk the tree quickly. The two items teams forget are the metadata JSON and the validation folder, "
         "and both are explicitly in the rubric.")

d.table("How the rubric scores you", ["Criterion", "Weight", "What a top mark looks like"], [
    ["Validity", "30", "Independent validation, CIs, baseline, failure cases explained"],
    ["Relevance", "20", "Complete reproducible workflow with a path to operational use"],
    ["Impact", "20", "Named user and decision, benefit quantified"],
    ["Creativity", "15", "Uses spectral features only hyperspectral can resolve"],
    ["Presentation", "15", "Clear story, readable figures, confident answers"],
], kicker="each scored 1–4 · Σ (score/4 × weight)", col_widths=[2, 1, 4],
   notes="Show the worked example from the rubric: 3/4/3/2/3 gives 76.25. It makes the weighting concrete "
         "and shows that a weak Creativity score is survivable, while weak Validity is not.")

d.bullets("After the course", [
    "The top teams continue into the incubation phase, from proof of concept towards an MVP",
    "Keep the project **reproducible** — future you, or a new team member, needs to rerun it",
    "Keep data attributions intact if you publish or present the work elsewhere",
    "Consider releasing the notebook openly; it is a strong portfolio piece",
], kicker="what happens next",
   notes="Mention that several themes map onto real regional needs, and that a reproducible repository is "
         "what turns a course project into something an employer or partner can evaluate.")

d.handover("templates/presentation_template.md", [
    "Draft the twelve slides, writing each title as a full-sentence takeaway",
    "Rehearse twice, timed and standing, then cut to fit",
    "Drill the three questions with a teammate answering at random",
    "Complete templates/submission_checklist.md and fix anything unticked",
], minutes=150,
   notes="Book rehearsal slots with an instructor present; the feedback is worth more than another hour "
         "of slide polishing.")

d.recap([
    "Open with the problem and the person who has it, not the sensor",
    "Titles are sentences; one message per slide",
    "Show a spectrum, show a readable map, show the honest number with its uncertainty",
    "Limitations framed as scope build trust",
    "Rehearse aloud, twice; submit a folder that runs without you",
], next_up="Final evaluation and feedback — then the incubation pathway",
   notes="Close the course by thanking them and reminding them the rubric rewards honesty over polish.")

d.references([
    "templates/presentation_template.md · templates/submission_checklist.md · templates/evaluation_rubric.md (this course)",
    "Schimel, J. (2012). Writing Science: How to Write Papers That Get Cited and Proposals That Get Funded. OUP.",
    "Duarte, N. (2010). Resonate: Present Visual Stories that Transform Audiences. Wiley.",
    "Tufte, E.R. (2001). The Visual Display of Quantitative Information, 2nd ed. Graphics Press.",
    "Crameri, F. et al. (2020). The misuse of colour in science communication. Nature Communications 11, 5444.",
])

d.save("w4c_presentation_and_evaluation.pptx")
