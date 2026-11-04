"""Week 3 · Sessions 4–5 — Applied project development workshop, and interim feedback / QA."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

d = Deck("Project workshop and interim quality assurance",
         "Week 3 · Sessions 4–5",
         notebook="templates/project_template.ipynb",
         subtitle="Building the first defensible version of your project, then tearing it apart on purpose",
         week="Week 3 · 16–19 November 2026")

d.objectives([
    "Structure your project notebook so a reviewer can follow it without you in the room",
    "Run your own work through the interim QA checklist before anyone else does",
    "Give and receive peer review that improves a project instead of bruising it",
    "Recognise the five failure patterns that sink Earth observation projects",
    "Arrive at the interim review with the right four things ready",
], notes="Two sessions in one deck: the workshop day, then the QA review. Keep the lecture part short — "
         "most of these two days is teams working while you circulate.")

d.section("1. The workshop day", "From scattered notebooks to one runnable project")

d.callout("By the review you need a result you can defend,\nnot a result you like.",
          "A rough map with an honest accuracy figure beats a beautiful map with no validation. "
          "The rubric rewards the first and punishes the second.",
          kicker="the week 3 standard",
          notes="Say this at the start of the workshop and repeat it when you circulate. Teams naturally "
                "spend their time making figures prettier instead of making results checkable.")

d.table("How the workshop day runs", ["Time", "What happens", "Output"], [
    ["09:00–09:30", "Stand-up: each team states its one blocking problem", "Blockers listed"],
    ["09:30–12:00", "Build: config, data, method — instructors circulate", "Notebook runs top to bottom"],
    ["13:00–15:00", "Validate: spatial split, metrics, baseline", "First honest numbers"],
    ["15:00–16:00", "Self-QA with the checklist", "Checklist filled in"],
    ["16:00–17:00", "Swap notebooks with another team, peer review", "Review returned"],
], kicker="a suggested timetable", col_widths=[1, 3, 2],
   notes="The self-QA slot is non-negotiable; teams that skip it arrive at the review with notebooks that "
         "do not run on another machine. Enforce the swap even if the work is unfinished.")

d.bullets("Use the project template, in its order", [
    "**1 Problem, user and decision** — copied from your scoping canvas, not reinvented",
    "**2 Configuration** — scene IDs, window, thresholds, seeds, all in one cell",
    "**3 Data and quality control** — quicklook, masks inspected, usable fraction stated",
    "**4 Preprocessing** — bad bands, and any extra step justified in one line",
    "**5 Features** → **6 Method** — always with a baseline next to the main method",
    "**7 Validation** → **8 Uncertainty and limitations** — the part reviewers read first",
    "**9 Product output** → **10 Conclusions** — COG plus metadata, then what it means",
], kicker="templates/project_template.ipynb",
   notes="The order is not decoration: it is the order a reviewer reads in, and it matches the rubric. "
         "Teams that invent their own order always lose the link between problem and result.")

d.figure_bullets("What 'finished' looks like",
                 "31_from_notebook_to_product/01_3_run_the_pipeline.png",
                 ["One command reproduces the map",
                  "The output is georeferenced and has metadata",
                  "A quicklook a non-specialist can read",
                  "A number with a unit, and its uncertainty",
                  "Quality flags that say when not to trust it"],
                 caption="Example product output from notebook 31",
                 kicker="the target for week 4",
                 notes="Show this early so teams aim at it. It is deliberately unglamorous: correct, "
                       "documented, repeatable.")

d.section("2. Quality assurance", "Check your own work before someone else does")

d.bullets("A — Reproducibility", [
    "*Restart & Run All* finishes on a clean kernel — the single most common failure",
    "No absolute paths; data found through `hu.get_scene()` or a relative folder",
    "One config cell holds scene IDs, windows, thresholds and seeds",
    "Random seeds fixed: `np.random.default_rng(42)`, `random_state=42`, `torch.manual_seed`",
    "Runtime is sane, or heavy steps are cached and clearly marked",
], kicker="interim_qa_checklist.md, section A",
   notes="Ask for a show of hands: who has actually restarted and run all today? The gap between 'it works' "
         "and 'it works from a clean kernel' is where most lost marks live.")

d.figure_bullets("B — Data and preprocessing",
                 "11_preprocessing/04_2_quality_masks_inspect_before_you_trust.png",
                 ["Every dataset credited, including the reference labels",
                  "QA masks applied **and inspected** — the sabkha flagged as cloud in Al Dhafra",
                  "Bad bands removed, and the choice explained in one sentence",
                  "Band choices state the wavelength used, e.g. 'NIR = 862 nm'",
                  "Negative reflectance over water understood, not silently deleted"],
                 caption="Inspecting the cloud mask before trusting it",
                 kicker="section B",
   notes="The mask point is worth a minute: three of the eight Arab-region scenes carry false cloud flags "
         "over bright desert. A team that masks blindly loses half its study area without noticing.")

d.figure_bullets("C — Method and validity",
                 "15_classification_classical/01_2_a_spatially_separated_train_test_split.png",
                 ["The method still matches the scoping canvas, or the change is explained",
                  "The hyperspectral advantage is demonstrated or honestly discussed",
                  "Train and test data are **spatially separated**",
                  "Metrics come with the error matrix, not as a lone number",
                  "A baseline shows what the complexity bought",
                  "Failure cases shown, uncertainty communicated"],
                 caption="A spatially separated train/test split (notebook 15)",
                 kicker="section C — the heaviest weighted part",
   notes="This maps one-to-one onto the Validity criterion, 30 % of the final mark. If a team can only fix "
         "one section before week 4, it is this one.")

d.bullets("D — Communication", [
    "Every figure has a title, axis labels with units, colour bar and legend",
    "Colour maps chosen sensibly — no rainbow for continuous data, categorical colours for classes",
    "Markdown explains *why* before each major step, not just what the code does",
    "Key numbers gathered in one results table",
    "The user-facing product is sketched, even if only as a mock-up",
], kicker="section D",
   notes="Quick exercise: put a figure from any team's notebook on screen and ask the room what the colour "
         "scale means. If nobody can say, the figure needs work.")

d.section("3. Peer review", "The cheapest way to find your own blind spots")

d.bullets("How to give a review that helps", [
    "Run the notebook **first**, before reading it — most findings come from that alone",
    "Mark each checklist item ✅ / ⚠️ / ❌ and add one line of evidence for every ⚠️ and ❌",
    "Separate **defects** (it does not run, the split leaks) from **preferences** (I would colour it differently)",
    "Lead with the one change that would most improve the project",
    "Be specific and kind: 'the test blocks touch the training blocks at row 200' beats 'validation is weak'",
], kicker="reviewer discipline",
   notes="Remind them they are reviewing the work, not the team. Also: a review that only praises is useless "
         "to the receiving team, and costs them marks later.")

d.bullets("How to receive one", [
    "Do not defend in the room — write the finding down and check it afterwards",
    "Anything that made the reviewer stumble is a real problem, even if you can explain it",
    "Triage into: fix now, fix before submission, document as a limitation",
    "Attach the completed checklist to your interim submission, including the ❌ items",
], kicker="and not take it personally",
   notes="The 'document as a limitation' route is legitimate and rewarded — the rubric asks for honest "
         "limitations, not perfection.")

d.table("Five ways Earth observation projects fail", ["Pattern", "Symptom", "Fix"], [
    ["Leakage", "Accuracy above 0.95 on a random pixel split", "Blocked split, buffer, re-measure"],
    ["No baseline", "Only the complex model is reported", "Add a threshold or index comparison"],
    ["Unvalidated map", "Beautiful figure, no numbers", "Sample the map, report UA/PA with CIs"],
    ["Map of nothing", "Pretty output, no user or decision", "Return to the scoping canvas"],
    ["Cherry-picked scene", "Works on one window only", "Test on a second area, report both"],
], kicker="recognise these early", col_widths=[1, 2, 2],
   notes="Ask each team which of the five is closest to their current risk. Most will recognise themselves "
           "in one, and naming it now is far cheaper than discovering it in the final evaluation.")

d.section("4. The interim review", "What to bring, and what happens")

d.bullets("Each team brings four things", [
    "The project notebook, executed, running top to bottom",
    "One map or result figure, and the numbers behind it",
    "The completed QA checklist, ❌ items included",
    "One question you want the panel to answer",
], kicker="10 minutes per team, plus 5 for feedback",
   notes="Keep the timing tight; the value is in the feedback, not the presentation. The 'one question' rule "
         "makes teams use the panel instead of performing for it.")

d.bullets("What 'done' means by the end of week 3", [
    "The notebook runs from a clean kernel on another machine",
    "There is a **first honest accuracy figure**, from a spatially independent design",
    "A baseline exists and the comparison is written down",
    "At least three failure cases are identified and explained",
    "The remaining work for week 4 is a list, not a hope",
], kicker="the bar for the interim milestone",
   notes="Week 4 is four days and ends with the presentation. Anything not on this list by Thursday "
         "becomes a week 4 emergency.")

d.handover("templates/project_template.ipynb", [
    "Restructure your work into the template's section order",
    "Fill in templates/interim_qa_checklist.md for your own notebook, honestly",
    "Swap with another team and review theirs against the same checklist",
    "Turn the findings into a prioritised fix list for week 4",
], minutes=180,
   notes="Circulate constantly during this block. The most useful intervention is usually asking a team to "
         "restart their kernel and run everything while you watch.")

d.recap([
    "The template's order is the reviewer's reading order — use it",
    "Self-QA before peer review; peer review before the panel",
    "Reproducibility failures are the cheapest marks to lose and the easiest to fix",
    "Name your failure pattern early: leakage, no baseline, unvalidated, no user, one scene",
    "Bring a defensible number to the review, not a beautiful picture",
], next_up="Week 4 — Advanced analytics and solution refinement, then final implementation",
   notes="End by scheduling the review slots so teams know their time before they leave.")

d.references([
    "templates/project_template.ipynb · templates/interim_qa_checklist.md (this course)",
    "assignments/assignment_w3_validated_map.md — the interim milestone deliverable",
    "Wilson, G. et al. (2017). Good enough practices in scientific computing. PLoS Comput Biol 13(6), e1005510.",
    "Sandve, G.K. et al. (2013). Ten simple rules for reproducible computational research. PLoS Comput Biol 9(10), e1003285.",
    "Rule, A. et al. (2019). Ten simple rules for writing and sharing computational analyses in Jupyter Notebooks. PLoS Comput Biol 15(7), e1007007.",
])

d.save("w3d_project_workshop_qa.pptx")
