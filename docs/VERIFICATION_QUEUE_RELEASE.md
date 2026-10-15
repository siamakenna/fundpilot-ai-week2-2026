# Verification queue release — v0.3.0

Baseline: `22f54af04feef4ae75d28cf8a822871a9788af5e` (public main).
Feature branch: `codex/verification-queue`. Scope: presentation and deterministic
human-verification suggestions, not model improvement or an accuracy claim.

## What changed

- UNKNOWN/NOT MATCH now produce one actionable item per source passage; contradictions
  come first. Each has exact evidence and offsets, original reasons, a first action
  and a suggested sponsor question. INFO and generic scope reminders do not inflate
  risk counts. All underlying findings remain in the report.
- UI shows the first three items; expandable and downloadable Markdown includes the
  complete numbered queue. CLI downloads use the same presentation layer.
- Optional CNS snapshot quick-start loads fictional editable facts and selects live
  Gemma. It never supplies a prediction; Analyze invokes the existing local engine.
- All-match still requires full-source/linked-policy review. No answers, exceptions,
  sponsor decisions, completeness or official eligibility are invented.
- Supplied upgrade prompt read in full; supplied `apply_judge_polish.py` applied from
  the repository root. Its screenshot/timestamp/report-link polish was then updated
  to the new authentic recording while preserving the old v0.2.0 demo.

## Completed checks

| Gate | Result |
| --- | --- |
| Pre-change tests | PASS: 79/79 |
| Post-change complete suite | PASS: 93/93; original tests unchanged |
| Focused queue/quick-start suite | PASS: 14/14; rules/adapter mocks explicitly labeled |
| Ruff release gate | PASS: `ruff check --select F .`, same gate as v0.2.0 |
| Broad optional Ruff review | 28 baseline diagnostics, 28 current; zero new diagnostics. Frozen code was not reformatted |
| Frozen data and engine | PASS: 196 protected baseline files byte-identical; candidate engine SHA matches freeze |
| Source attachment | PASS: CNS text matches original local cache and committed demo hash; 11 presentation/span checks, report unchanged |
| Browser | PASS: three actual Gemma runs, expected counts, three downloads, queue, input lock and stale-report invalidation |
| Accessibility smoke | PASS: keyboard sample load; 390px viewport without page overflow; expandable report. Not a full WCAG audit |
| Security scope | PASS: no credential-pattern matches, unexpected private document/model-weight formats or large files; no new network or paid dependency |
| Recording | PASS: continuous 45.64-second WebM, 1440×1000 VP8; playback and actual report bytes verified |
| Article | English template headings/tags retained; only Best Use of Gemma; no invented users, revenue, accuracy or hosted app |

Evidence lives in [`evidence/verification-upgrade/`](../evidence/verification-upgrade/).
The original 139/139 quote-span check and all failure evidence remain unchanged.
The new span check is deterministic presentation replay, not another benchmark.

Development F1 remains Gemma **42.11%** versus rules **62.50%**; held-out F1 remains
**34.48%** versus **33.90%**, on provisional annotations. All three held-out reports
required manual review. Proposed AI adjudication is separate, not human ground truth;
the ISMB postdoc interpretation remains unresolved. No inference/prompt/rule changes,
held-out tuning, rescore or expensive benchmark rerun occurred.

## Commands and reproducibility

From the repository root:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q tests/test_verification.py
.venv/bin/ruff check --select F .
.venv/bin/ruff check --output-format json .
git diff --check
GRADIO_ANALYTICS_ENABLED=False .venv/bin/python -c 'from app import demo; demo.launch(server_name="127.0.0.1", server_port=7862, share=False)'
```

The broad Ruff command intentionally reports pre-existing optional diagnostics;
its nonzero status is disclosed, not called a clean lint result. New modules/tests
introduce none. Gradio 6.30.0, Ollama 0.40.4 and existing `gemma3:1b` Q4_K_M were
used. Model digest remains `97558784bdc9175075a72655bf360b15da17df6b3b9e5182af9f8c0c8e58ba7c`.
See [capture commands](LOCAL_CAPTURE_STEPS.md) for the actual Playwright script.

Scoped security review covered escaping, deterministic question generation, sample
inputs, local-only transport, stale output, report privacy and new file contents.
It is not a penetration test or full dependency audit. Reports remain unencrypted
local temporary files. Only public source text and fictional profiles were captured.

## Competition and remaining human action

The [official challenge](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)
and its submission template were rechecked on October 15. The page confirms the
October 18, 2026, 11:59 PM PDT deadline and required `devchallenge` / `hf26challenge`
tags. Writing quality has the greatest weight. Optional first-user and agent-session
sections are omitted; no unsupported partner categories are claimed.

Review the [completed article](DEV_SUBMISSION_DRAFT.md) and public video. Sign in to
DEV, paste into the official template, preview the links/media and publish one entry
only when you approve. No DEV article or challenge entry has been published by Codex.

## Public asset verification before merge

[PR #3](https://github.com/siamakenna/fundpilot-ai-week2-2026/pull/3) contains the
upgrade. [v0.3.0](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/tag/v0.3.0)
points to the tested application commit `2380ccf1b9409a406563dbc972b20f59193ab85f`.
The anonymous video URL returns HTTP 200; GitHub's SHA-256 and byte size match the
locally verified video. All 15 remote links checked at the pushed code commit and
19 local documentation paths resolve. New `main` links are checked again after
merge. The v0.2.0 asset digest is unchanged. See [link evidence](../evidence/verification-upgrade/links.json).

All local release gates passed before marking the PR ready. No repository CI
workflow is configured; these are recorded local checks, not a claimed hosted CI run.
Public DEV publication remains the owner's final action.
