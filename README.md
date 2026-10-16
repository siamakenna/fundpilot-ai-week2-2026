# FundPilot AI

**Check public funding requirements before spending hours on an application.**
Paste an organizer's announcement, answer ordinary applicant questions, and use
local Gemma to help interpret the text. Python attaches exact source passages and
compares supported conditions with your declared facts. Download the evidence and
questions that still need the sponsor's answer.

[Code](https://github.com/siamakenna/fundpilot-ai-week2-2026) ·
[Official sources](docs/OFFICIAL_SOURCES.md) · [Measured results](docs/REAL_WORLD_EVALUATION.md) · [Evaluation rubric](evaluation/RUBRIC.md) ·
[Submission draft](docs/DEV_SUBMISSION_DRAFT.md)

## See the real application

![Live Gemma contradiction and Application Readiness Dossier](https://raw.githubusercontent.com/siamakenna/fundpilot-ai-week2-2026/main/evidence/usability/contradiction-overview.png)

[Authentic v0.3.2 dossier video](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.3.2/fundpilot-dossier-demo.webm) · [Contradiction dossier](evidence/usability/contradiction-dossier.md) · [Missing-fact dossier](evidence/usability/unknown-dossier.md) · [Historical restriction and deadline](evidence/usability/historical-exclusion-dossier.md) · [Release checks](docs/DOSSIER_RELEASE_QA.md)

Four genuine local Gemma analyses: three fictional applicant configurations on a short CNS excerpt, then historical GNS source excerpts with a passed deadline. The recording demonstrates preparation and review, not complete-call eligibility or a hosted service. The [v0.3.1 fallback video](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.3.1/fundpilot-onboarding-demo.webm) is preserved.

The optional guide explains the workflow and result labels. **Check local model** checks installation only when clicked; it does not install software or claim successful inference.

## Three-step workflow

1. Paste public eligibility text, including exclusions, amounts, dates and application
   instructions. Add the official URL for attribution; FundPilot does not fetch it.
   Or choose **Load sample public excerpt**: the verified CNS snapshot (2026-10-14)
   with fictional editable facts. It loads no predictions; Analyze runs real Gemma.
   The short excerpt neither covers the full award nor confirms applications are open.
2. Enter your career stage and Yes/No/Unknown facts. Leave unknown amounts blank.
   Suggested questions use incomplete keyword cues; **Show all questions** exposes every
   field. Hidden answers are retained and never silently changed to No.
   The form defaults to **Live local Gemma**; no JSON knowledge is needed.
3. Start with the compact overview: matching facts, potential problems, and missing
   information / unclear conditions. Provisional source flags stay separate. Open the
   **Application Readiness Dossier** for supported contradictions, missing
   facts, materials and dated milestones, grouped sponsor questions, and a prioritized
   checklist. Potential source issues are labeled separately from model findings.
   Detailed evidence is expandable. Follow passage links to exact evidence. Download the dossier and the separate,
   unchanged full evidence report. Inputs lock during analysis; editing them clears both.


MATCH means a supported textual comparison with a declared fact—not an independently
verified credential. Contradictions can be useful without claiming official
ineligibility. Every pasted passage requires scope review for additional conditions
and linked policies. No real-call report certifies eligibility or guarantees funding.

Fictional reference examples remain in a secondary tab labeled **legacy**. The
explicit **Rule baseline (NO AI)** option runs the same public text without a model;
it is never substituted automatically for a failed live request.

## Run locally

Requires Python 3.11+ and [Ollama](https://ollama.com/). Initial installation and model
download require internet. Inference uses the local runtime afterward.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m pytest -q
ollama pull gemma3:1b
```

Start Ollama in one terminal (skip if already running), then the application in another:

```bash
OLLAMA_NO_CLOUD=1 ollama serve
```

```bash
GRADIO_ANALYTICS_ENABLED=False python app.py
```

Open the localhost URL printed by Gradio. On the development Mac, the official
Ollama 0.40.4 binary is installed in `.tools/ollama/ollama` (ignored by Git).
The verified model is `gemma3:1b`, Q4_K_M. `requirements-tested.txt` records tested
Python packages. No hosted API key, subscription, authentication or payment service
is required. Installation still requires technical setup; a turnkey installer is
not claimed.

Developer reproduction of the real-call path:

```bash
python -m fundpilot.public_cli --source-file public-call.txt --mode gemma --output report.md --dossier-output dossier.md --audit model-labels.json
```

The CLI defaults to unknown applicant facts. Its optional `--profile-json` is for
developer reproduction; ordinary users use the form. Legacy `fundpilot.cli` retains
the original synthetic benchmark for reproducibility.

## Interpretation and safety boundaries

- Every nonblank paragraph/list item receives an ID and exact character offsets.
  Gemma classifies one passage at a time under a strict schema. Fixed Boolean
  criterion fields avoid duplicated list entries observed in development.
- Lexical candidates constrain available predicates; Gemma selects applicability
  and category. This is a measured hybrid, not unrestricted semantic extraction.
- Python attaches the original source. Source quotes are not generated by Gemma.
- A comparison is permitted only where the model and explicit rules agree.
  Unsupported criteria, exceptions, durations, exclusions beyond supported cases,
  and mixed meanings remain UNKNOWN. Missing/malformed model output fails visibly.
- Sponsor stipends differ from applicant request ceilings. USD, GBP and EUR request
  comparisons require the same currency; no exchange rates are invented.
- Explicit dated milestones are shown with their apparent purpose. Missing years,
  timezone boundaries and ambiguous cutoffs require review. A future conference
  does not imply open applications.
- Paragraph coverage does not establish semantic completeness. Linked policies,
  complicated dependencies and real-world eligibility need sponsor confirmation.

Only pasted public source text goes to local Ollama. Profile facts remain in Python.
Endpoints are loopback-only, redirects/proxies are blocked, Gradio sharing and
analytics are disabled. Local reports are not encrypted. Do not paste private grant
or institutional documents.

## Evidence and limitations

The [product audit](docs/PRODUCT_AUDIT.md) records the baseline gaps.
Five official development sources and three held-out sources were assigned before
tuning in [the committed split](evaluation/source_split.json). Annotations are
assistant-reviewed against the sources, **not independently human-verified**.
Full source copies stay in ignored local storage; public annotations contain hashes,
line references and labels. Tests distinguish mocks from actual local inference.

The original **20/21 synthetic clause matches** are historical results only;
[the baseline evaluation](docs/EVALUATION.md) cannot establish real-world accuracy.
Failed real-source strategies remain in `evidence/realworld-development/`.
**Real-source limits:** final development F1 is 42.11% versus rules 62.50%;
one held-out pass gives 34.48% versus rules 33.90% (10 exact matches each).
All three held-out reports need review, with no supported applicant matches or
mismatches for the evaluation profile. This is an inspectable prototype, not an
automated eligibility service. The proposed [AI annotation audit](docs/ANNOTATION_REVIEW.md)
remains separate from the original benchmark. No meaningful model superiority,
real customer, revenue or validated price is claimed. A $9 report or $39/month workspace remains a business hypothesis.

## Demo and submission

**[Watch/download the new v0.3.1 demo](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.3.1/fundpilot-onboarding-demo.webm)** · [Release notes](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/tag/v0.3.1) · [Release checks](docs/FIRST_RUN_RELEASE.md)

The 59.72-second public WebM contains three actual Gemma calls on one CNS passage,
three real report downloads, prioritized verification questions and stale-report
invalidation. Its fictional facts and excerpt scope are explicit. The [original
47-second v0.2.0 demonstration](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.2.0/fundpilot-public-call-demo.webm)
and all original evidence remain unchanged.

The DEV article remains unpublished. The [new demo evidence](evidence/onboarding/)
identifies actual model runs; curated fixtures are never passed off as live inference.
115 automated tests pass, including the unchanged original 93. No inference changes
ship in this release. The separate [v0.4 experiment](https://github.com/siamakenna/fundpilot-ai-week2-2026/pull/4)
failed its frozen release evaluation and remains unmerged; [results and limitations](docs/FIRST_RUN_RELEASE.md) are disclosed.
The [v0.3.0 video](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.3.0/fundpilot-verification-queue-demo.webm) also remains unchanged.

## License and provenance

Application code and original synthetic fixtures: [MIT](LICENSE), copyright 2026
Makenna Rodriguez. Dependencies retain their own licenses. Gemma weights are
separately downloaded under [Google's Gemma terms](https://ai.google.dev/gemma/terms),
not included or relicensed. Public source passages remain their owners' content;
only short attributed excerpts are redistributed.

The owner attests independent work during the Week 2 contest window. Original
fixtures and baseline failure evidence remain unchanged. See
[provenance](docs/PROVENANCE_AND_LICENSES.md) and the
[official challenge](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).

## Dossier release and model decision

The dossier highlights structural cues, including possible exclusions hidden in paragraphs,
AND/OR/UNLESS dependencies, periods, materials, and award benefits versus request limits.
These are review prompts, never verified interpretations or new MATCH/NOT MATCH findings.
Pasted text cannot establish complete coverage; review the full source and linked policies.

Gemma 1B remains the default. An exploratory [same-strategy 4B comparison](docs/MODEL_SIZE_COMPARISON.md)
found one additional provisional condition but more supported MATCH disagreements and longer
latency. No human-validated model improvement is claimed. The failed atomic v0.4 PR remains unmerged.
The original 42.11%/34.48% Gemma development/held-out F1 values and 62.50%/33.90% rule values are unchanged.
