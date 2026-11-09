"""Week 2 · Session 5 — Project scoping and use case definition."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deckbuild import Deck  # noqa: E402

F = "16_scene_finder/"

d = Deck("Project scoping and use case definition",
         "Week 2 · Session 5",
         notebook="16_scene_finder.ipynb",
         subtitle="From an idea to a scope you can actually deliver in three weeks",
         week="Week 2 · 16–19 November 2026")

d.objectives([
    "Turn a broad idea into a problem statement with a named user and a named decision",
    "Apply the *why hyperspectral* test, and accept an honest negative answer",
    "Check that suitable imagery exists **before** committing to an area of interest",
    "Draft a validation plan before building anything",
    "Fill in the scoping canvas and name your risks and fallbacks",
], notes="This is the session that decides whether a team's project succeeds. Say plainly that most "
         "failed PoCs fail here, not in the modelling. Today ends with a completed canvas per team.")

d.section("1. What makes a good scope", "Narrow, useful, and provable")

d.callout("A scope is a promise you can keep in three weeks.",
          "Problem → user → decision → product. If you cannot name the person who acts on your output "
          "and the decision they take, you have a demo, not a project.",
          kicker="the test",
          notes="Repeat this framing whenever a team pitches a vague idea. Push for the name of a real "
                "organisation and a real recurring decision, even if fictional for the PoC.")

d.bullets("The four questions every scope must answer", [
    "**Problem** — who has what problem, where, and how big is it?",
    "**User** — which organisation and role receives the output?",
    "**Decision** — what will they do differently because of it?",
    "**Product** — in what form does it arrive: a map, a number, an alert, a report?",
    ("A good test: write the sentence *\"Every month, <user> opens <product> and decides "
     "<decision>\"*. If you cannot, narrow the scope", 1),
], kicker="problem · user · decision · product",
   notes="Have each team say their sentence out loud. The ones that stumble usually have two projects "
         "mixed together and need to drop one.")

d.bullets("The *why hyperspectral* test", [
    "Name the **specific spectral feature** you rely on, with wavelengths",
    "Ask whether Sentinel-2 could resolve it — if yes, hyperspectral is not the reason your idea works",
    "Notebook 15 measured the honest baseline: for broad land cover, 352 bands beat simulated "
    "Sentinel-2 bands by **0.3 points** of accuracy",
    "Notebooks 13 and 14 show where the spectrum wins decisively: mineral species, crop residue, "
    "pigments, gases, sub-pixel targets",
    "**\"Multispectral would do\"** is a creditable finding — write it down and pivot the added value",
], kicker="be honest early",
   notes="The evaluation rubric rewards this honesty under Validity and Creativity. A team that "
         "discovers this in the final week has a crisis; a team that discovers it now has a design decision.")

d.section("2. Does the data exist?", "Tasked archives are sparse — check first")

d.bullets("Hyperspectral archives are not Sentinel-2", [
    "Tanager is **tasked**: it images requested targets, it does not map the globe on a cycle",
    "The open archive is therefore **sparse and uneven** — most places have no scene at all",
    "Repeat coverage exists mainly at supersites, which constrains change-detection projects",
    "Plan around what exists, or pair one hyperspectral scene with a Sentinel-2 time series",
], kicker="the first reality check",
   notes="This surprises people used to Landsat or Sentinel. Say it before they fall in love with an AOI "
         "that has no imagery.")

d.figure("The Tanager open archive, worldwide",
         F + "01_3_a_world_view.png",
         caption="Scene footprints, September 2024 to October 2025",
         kicker="global coverage",
         notes="Ask the room to find their own country before you move on. The clustering around the "
               "United States and a few supersites makes the sparseness obvious.")

d.table("What the open catalogue actually contains",
        ["Property", "Value"],
        [["Catalogue entries", "276"],
         ["Unique scenes", "153 (123 appear in more than one collection)"],
         ["Thematic collections", "9 (agriculture, urban, fire, GHG-plumes, coastal …)"],
         ["Date range", "25 Sep 2024 – 29 Oct 2025"],
         ["Scene footprint", "322–879 km², median 394 km²"],
         ["Top countries", "United States 52, Argentina 15, Netherlands 9, Canada 7"]],
        col_widths=[1, 2], kicker="know the archive",
        notes="The 276-versus-153 gap is the deduplication trap: a naive count double-counts scenes that "
              "sit in several thematic collections. Students must deduplicate by scene ID.")

d.figure_bullets("Searching your own area",
                 F + "02_4_1_the_arab_region.png",
                 ["Search on **footprints**, not centroids — a centroid misses partial overlaps",
                  "In the Arab-region box: **14** catalogue entries, **8** unique scenes",
                  "Filter on cloud, off-nadir angle and sun elevation, then look at the thumbnails",
                  "Large off-nadir angles mean bigger pixels and different viewing geometry"],
                 caption="Tanager scenes intersecting the Arab region",
                 notes="Eight scenes for the whole Arab region is the honest picture today. Teams working "
                       "on UAE topics will often use the Al Dhafra scene from the course data.")

d.callout("Three of the eight Arab-region scenes are flagged 50–74 % cloudy.\nAll three thumbnails are clear.",
          "The provisional cloud mask confuses bright desert sand, gravel and sabkha with cloud: "
          "Riyadh 74 %, Al Mahrah 53 %, Al Dhafra 51 %. A strict max-cloud filter would have discarded "
          "three of your eight candidate scenes.",
          kicker="look before you trust the metadata",
          notes="This is the most practical slide in the deck. Notebook 11 shows the same failure pixel "
                "by pixel. Rule: filter loosely on metadata, then inspect thumbnails by eye.")

d.figure_bullets("Repeat coverage: can you do change detection?",
                 F + "03_5_repeat_coverage_and_overlapping_pairs.png",
                 ["Find **pairs** of scenes whose footprints overlap your area",
                  "Malibu has 6 scenes within ±3 km — one of the few dense supersites",
                  "Check the **time gap** and the **viewing geometry** of each pair",
                  "No pair over your AOI? Use Sentinel-2 for the time axis and Tanager for the detail"],
                 caption="Scenes with repeat coverage in the open archive",
                 image_left=True,
                 notes="Notebook 30 uses the Malibu pair for pre/post-fire change detection. Most AOIs "
                       "will not be this lucky, which is why this check belongs in the scope.")

d.bullets("Complementary data you should plan for", [
    "**EnMAP** (224 bands, 30 m) — free via DLR registration; delivery takes a few days, so request early",
    "**Sentinel-2 / Landsat** — the time axis your hyperspectral scene lacks",
    "**Reference data** for validation: field data, VHR interpretation, ESA WorldCover, national maps",
    "**Ancillary layers**: DEM, weather, infrastructure, administrative boundaries",
    ("Register for EnMAP **this week** if your project needs it — it is not an instant download", 1),
], kicker="do not rely on one source",
   notes="Chase this: a team that registers next week will not get their data in time. The EnMAP mission "
         "also publishes open example scenes that need no login, which we use in the QGIS session.")

d.section("3. Plan the proof before the build", "Validation, risks, milestones")

d.bullets("Write the validation plan before you write the model", [
    "Name the **reference data** and how it is independent of your training data",
    "Choose the **metrics** now: per-class F1 and a confusion matrix, or RMSE and bias, or detection "
    "rate at a fixed false-alarm rate",
    "Decide the **split**: spatial blocks, separate sites, or separate dates",
    "State a **success criterion** in advance, e.g. *F1 ≥ 0.8 for the mangrove class*",
    "If you cannot describe how you would be proven wrong, the project is not yet a project",
], kicker="section 8 of the canvas",
   notes="Pre-registering the criterion stops the familiar drift where the metric quietly changes until "
         "the result looks good. Notebook 21 supplies the machinery.")

d.table("Name your risks and your fallbacks now",
        ["Risk", "Fallback"],
        [["No cloud-free scene over the AOI", "Use another scene from the same collection, or another AOI"],
         ["Reference data never arrives", "Visual interpretation of VHR imagery, or cross-sensor consistency"],
         ["Classes are not separable", "Merge classes, add SWIR features, or switch to unmixing"],
         ["EnMAP order is delayed", "Use the open EnMAP example scenes, or Tanager only"],
         ["Model does not beat the baseline", "Report it honestly; the analysis is still a result"]],
        col_widths=[1, 1], kicker="section 10 of the canvas",
        notes="Teams find this depressing for about five minutes and then relieved. A named fallback "
              "converts a project-ending surprise into a planned branch.")

d.table("Milestones between here and the final presentation",
        ["When", "Deliverable"],
        [["Today, Thu 19 Nov", "Scoping canvas drafted, scenes identified and downloading"],
         ["Mon 23 Nov", "Scoping canvas due"],
         ["Tue 24 Nov", "Method applied to your own scene"],
         ["Wed 25 Nov, pm", "Build afternoon — validated result, instructors on hand"],
         ["Thu 26 Nov", "Submission in the morning, presentation in the afternoon"]],
        col_widths=[1, 2], kicker="one week, no slack",
        notes="Be blunt about the shape of this: one scheduled build afternoon, and five working days from "
              "today to the presentation. That is why the canvas has to be small enough to finish. A team "
              "still choosing a theme today is already behind.")

d.bullets("A worked example, in the canvas's own words", [
    "**Problem:** coastal sabkha and shallow-water habitats along the Al Dhafra coast are not mapped "
    "at habitat level",
    "**User and decision:** an environment agency deciding where to survey and protect",
    "**Why hyperspectral:** gypsum and carbonate absorption features separate sabkha types; "
    "narrow visible bands separate shallow benthic cover",
    "**Data:** one Tanager scene (`20250511_074311_00_4001`, 11 May 2025) — flagged 51 % cloud, "
    "confirmed clear by thumbnail",
    "**Limitation, stated openly:** a single date, so no change analysis; mitigated with Sentinel-2",
], kicker="honest and specific",
   notes="Notebook 16 contains this example in full. Reviewers reward the explicit limitation and "
         "mitigation far more than they punish the single date.")

d.handover("16_scene_finder.ipynb", [
    "Load the catalogue index and deduplicate to unique scenes",
    "Search your own area of interest by point or bounding box, with a date window",
    "Compare cloud metadata with the thumbnails before rejecting any scene",
    "Look for overlapping pairs if your idea needs change detection",
    "Fill in section 6 of templates/project_scoping_template.md with what you actually found",
], minutes=90,
   notes="Teams that find no data over their AOI should pivot today, not next week. Keep the six course "
         "scenes as a guaranteed fallback for any theme.")

d.recap([
    "Scope = **problem, user, decision, product** — in one sentence you can say out loud",
    "Apply the *why hyperspectral* test early; \"multispectral would do\" is a valid, creditable answer",
    "The archive is **sparse and tasked**: 153 unique scenes, 8 over the whole Arab region",
    "**Do not trust cloud metadata over deserts** — three of eight Arab-region scenes are false alarms",
    "Write the **validation plan and the fallbacks** before you write the model",
], next_up="Week 3 — GeoAI methods, then validation and accuracy assessment",
   notes="End by collecting one completed canvas per team, even in draft form. Review them before Week 3.")

d.references([
    "Course templates: templates/project_scoping_template.md, templates/evaluation_rubric.md",
    "Course notebooks: 16_scene_finder.ipynb (data availability), 21_validation_accuracy_assessment.ipynb (validation design)",
    "Planet (2024–2025). Tanager-1 open data STAC catalogue — www.planet.com/data/stac",
    "EnMAP data access and open example scenes — www.enmap.org/data_access",
    "Olofsson, P. et al. (2014). Good practices for estimating area and assessing accuracy of land change. RSE 148, 42–57.",
])

d.save("w2e_project_scoping.pptx")
