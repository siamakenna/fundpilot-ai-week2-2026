# v0.3.2 Application Readiness Dossier — release QA

## Scope and decision

Ship the product-only dossier, retain Gemma 1B and keep v0.3.1 as fallback. Production interpretation, exact source attachment, old verification queue, original fixtures, all historical annotations/scores and the rejected atomic PR #4 are unchanged. The new 4B comparison is exploratory documentation; no inference rewrite is included.

The dossier adds five visible sections, a separate Markdown download and exact-passage navigation. It distinguishes supported contradictions from structural warning cues, missing applicant facts from unclear source wording, and self-verification from sponsor questions. The full existing evidence report remains separately downloadable. UI outputs clear together on edits or failure, and inputs lock during analysis.

## Local gates

- Full suite: **137 passed** (115 original + 22 dossier regressions). Focused dossier suite: 22 passed. Tests do not measure live model accuracy.
- `python -m ruff check --select F .`: passed.
- Configured focused lint on `fundpilot/dossier.py`, `real_ui.py`, `public_cli.py`, `tests/test_dossier.py`, and both model-comparison/review-packet scripts: passed. Gradio progress injection and the UI/trial exception boundaries have narrow explained suppressions.
- `git diff --check`: passed. Baseline comparison verified **224 protected source/evidence/evaluation files unchanged**. All original tests retained. Production `realworld.py` SHA-256 remains `7fb7ce091e1d16a7950bd131a9950c543777b6bfabe1f18f2c75d1e52f8674fc`.
- Scoped privacy/security review: no credential-pattern hits in publishable files; no new model weights, private document formats, source-cache dumps, personal profiles, environment files or local temporary reports in Git. Public demo inputs are attributed official excerpts plus fictional facts. Raw model-size audits contain Boolean classifications/timing, not source prompts or applicant data. MIT attribution and separate Gemma terms preserved. This is a scoped review, not a penetration-test guarantee.
- Unchanged production model, prompt/schema and evidence/decision engine; new warnings never change findings or counts. Source-derived items retain exact parent passage references, with offsets. Full-source completeness is a general recommendation, never inferred from excerpt length.

## Actual browser and live inference

Chromium 151.0.7922.34, Gradio 6.30.0, local Ollama 0.40.4, Gemma 3 1B Q4_K_M.

[Browser checks](../evidence/dossier/checks.json): keyboard sample loading and source-anchor navigation; 390×844 viewport with no horizontal overflow; negative, NaN and nonnumeric amounts; empty source; real Ollama HTTP 404 for deliberately absent `fundpilot-deliberately-missing:qa`; no fallback and no stale downloads. The missing-model diagnostic uses a separate local server configured with that name, not a mocked network response. Desktop live inputs and sample button lock while inference is pending. Editing title and reloading the sample clear both report and dossier. No browser page errors.

[Continuous recording events](../evidence/dossier/events.json) and [playback check](../evidence/dossier/playback.json): **69.12 seconds**, 1440×1000, three real analyses, six actual downloaded Markdown files. Download byte counts and SHA-256 values are in the event log. All decoded source quotations match their source character slices; Markdown escapes are presentation syntax, not altered quotes. Screenshots were inspected.

| Actual demonstration | Outcome | Dossier contribution |
| --- | --- | --- |
| CNS, fictional first author No / presenter Yes | 1 MATCH, 1 NOT MATCH | First-author contradiction; own-record check before sponsor question |
| CNS, fictional first author Yes / presenter Unknown | 1 MATCH, 1 UNKNOWN | Missing presenter fact and the record/form field to check |
| GNS historical excerpts, unknown career stage | 3 UNKNOWN, 1 INFO | Possible prior-funding exclusions and a past explicit date, without inventing eligibility |

GNS passages 2 and 3 remain unclassified in the original report. The dossier prominently identifies their “not received” cue as a possible exclusion and groups the sponsor question across both passages. This is the demonstrated warning benefit, **not an improved extraction score**. The GNS source was retrieved 2026-10-15; its February 13, 2026 deadline is historical. CNS was retrieved 2026-10-14. Neither excerpt establishes a complete call or current application status.

Three earlier capture attempts were retained locally and excluded from the release video: an app-startup connection refusal, a download assertion that did not decode Markdown escapes, and an assertion that did not handle blank lines between evidence paragraphs. Browser testing also caught and fixed Gradio's prefixed heading-anchor behavior. None was replaced by simulated inference. The final capture completes all assertions, and its video is unedited at normal speed.

Video file: `fundpilot-dossier-demo.webm`, **5,884,135 bytes**, SHA-256 **`321d13a4156f1381ba9cd6da5aecfa689698419cf1402ccb11c6cf6ca4c1f643`**. The v0.3.1 and earlier release assets remain unchanged. See the [v0.3.2 release](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/tag/v0.3.2) for the video and the post-upload `release-verification.json` manifest. CI must pass on the product PR before merging; the public release is tied to the merged commit.

## Reproduction

```bash
python -m pytest -q
python -m ruff check --select F .
python -m ruff check fundpilot/dossier.py fundpilot/real_ui.py fundpilot/public_cli.py tests/test_dossier.py scripts/compare_model_size.py scripts/prepare_blind_model_review.py
GRADIO_ANALYTICS_ENABLED=False python -c 'from app import demo; demo.launch(server_name="127.0.0.1", server_port=7864, share=False)'
# With installed Playwright Chromium and NODE_PATH set as needed:
node scripts/record_dossier_demo.cjs .local-reports/dossier-release-new
```

The recording script requires the hash-checked historical GNS cache; it does not fetch or fabricate it. For browser failure checks, start a second local process:

```bash
GRADIO_ANALYTICS_ENABLED=False python -c 'from functools import partial; from fundpilot import real_ui; real_ui.analyze = partial(real_ui.analyze, model="fundpilot-deliberately-missing:qa"); from app import demo; demo.launch(server_name="127.0.0.1", server_port=7865, share=False)'
node scripts/check_dossier_browser.cjs
```

## Limitations and submission

Structural cues can overflag ordinary AND/OR wording and miss unrecognized language. Materials are candidate mentions, not a complete mandatory-document list. Milestone roles are heuristic, especially in multi-date paragraphs. Missing fields are detected only for existing supported form facts. Applicant facts are self-reported. The dossier improves preparation, not model accuracy or official eligibility determination. Reports are local plaintext; initial installation still needs technical setup.

[1B versus 4B comparison](MODEL_SIZE_COMPARISON.md): same ten previously observed development passages and twenty provisional units. 4B was slower and produced more supported MATCH disagreements. No independent human review exists, so no promotion or further speculative strategy was shipped. Original real-source F1 values remain 42.11%/34.48% for Gemma and 62.50%/33.90% for rules. PR #4 stays unmerged.

The [official Week 2 page and template](https://dev.to/challenges/hacktoberfest-week2-2026-10-12) were checked again on October 15, 2026 (local time): one new project, English article for prize judging, demo/code links, required tags `devchallenge` and `hf26challenge`, deadline **October 18, 2026, 11:59 PM PDT**. The draft preserves the required headings; optional first-user and agent-session sections are omitted. Best Use of Gemma is the only claimed partner category. No customer, revenue, independent-review or superiority claim has been added.

Only the owner should approve and publish the English DEV draft through the Week 2 template, previewing its working video/screenshots and retaining the required tags before the deadline. No DEV article or competition entry has been published by this work.
