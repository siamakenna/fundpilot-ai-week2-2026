# Current judge walkthrough — v0.3.2

## v0.3.2 readiness overview and dossier (latest)

Use the [authentic recording](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.3.2/fundpilot-dossier-demo.webm). At 0:11, inspect supported comparisons; at 0:27, the first-author contradiction and next action; at 0:44, the missing presenter fact; at 1:22, possible prior-funding exclusions in historical GNS excerpts. At 1:34, both final Markdown downloads have been checked and an edit clears the displayed findings and files. Four genuine Gemma 1B analyses, eight actual downloads. All applicant facts are fictional; the GNS deadline has passed.

The compact overview uses existing counts. Show all questions exposes every applicant field and preserves hidden values. The URL is attribution-only; paste the actual text. Expand the dossier for the five-part preparation plan and exact source links; the complete original evidence report is separately available.

This is a preparation aid, not official eligibility or measured model improvement. See [release QA](DOSSIER_RELEASE_QA.md) and [exploratory 4B results](MODEL_SIZE_COMPARISON.md). The default remains 1B; atomic v0.4 is unmerged. The 69.12-second pre-refinement checkpoint remains in local storage and `evidence/dossier`; current release evidence is in `evidence/usability`. Earlier scripts and recordings above are historical evidence.

---

# Preserved onboarding walkthrough (v0.3.1)

[Public 60-second video](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.3.1/fundpilot-onboarding-demo.webm) · [Release checks](FIRST_RUN_RELEASE.md)

59.72 seconds, silent, continuous and unedited. Real local Gemma, one short public
CNS excerpt, three fictional applicant configurations. Not a hosted application or
whole-call accuracy demonstration. Approximate timestamps:

- 0:02–0:07: manual local model check, optional glossary and sample load.
- 0:11–0:25: first real inference; two supported MATCH findings, source review required.
- 0:32–0:35: second inference; first-author contradiction and verification question.
- 0:42–0:45: third inference; missing presenter fact and records to check.
- 0:32, 0:42, 0:53: actual reports downloaded and their bytes validated.
- 0:54–0:59: expanded report, changed title, stale-output clearing and sample reload.

[Events](../evidence/onboarding/events.json), [recording manifest](../evidence/onboarding/recording-manifest.json),
[reports and screenshots](../evidence/onboarding/). Use `scripts/record_onboarding_demo.cjs`;
see [reproduction instructions](FIRST_RUN_RELEASE.md). v0.4 inference is not shipped.

# Preserved verification queue walkthrough (v0.3.0)

[New public video](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.3.0/fundpilot-verification-queue-demo.webm) · [Release](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/tag/v0.3.0)

45.64 seconds, silent and unedited. Three genuine Gemma calls on one short CNS
passage; fictional editable applicant facts. This is a local product recording,
not a hosted app, a full-call assessment or a new accuracy benchmark.

| Approximate point | Actual action |
| --- | --- |
| 0:01 | Load attributed CNS sample; first author Yes, presenter Unknown; no report fabricated |
| 0:06–0:10 | Set both facts Yes and analyze; two MATCH, source review still required |
| 0:17–0:21 | Set first author No; new inference, priority-one contradiction question |
| 0:28–0:32 | Set presenter Unknown; new inference, check own records before asking sponsor |
| 0:17, 0:28, 0:39 | Download and validate each actual Markdown report |
| 0:39–0:44 | Expand complete evidence report |
| 0:45 | Edit title; old report disappears. Reload sample; no cached prediction returned |

[Events](../evidence/verification-upgrade/events.json), [screenshots and reports](../evidence/verification-upgrade/),
[recording manifest](../evidence/verification-upgrade/recording-manifest.json).
The full numbered queue is in each report; the UI shows at most three items.
The all-match example still requires full-source and linked-policy review.

Use `scripts/record_queue_demo.cjs` as described in [capture steps](LOCAL_CAPTURE_STEPS.md).
Earlier capture attempts remain locally, including selector failures; the final
recording is a single continuous successful session. No held-out inference was rerun.

## Preserved v0.2.0 walkthrough

[Public video](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.2.0/fundpilot-public-call-demo.webm) · [Release](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/tag/v0.2.0)

The automated recording is 47.32 seconds, silent, and unedited. It uses one short
CNS 2027 eligibility passage, with explicit attribution and fictional applicant
facts. It is a focused product demonstration, not a full-call eligibility decision.

| Approximate point | What actually happens |
| --- | --- |
| 0–6 s | Public source text and ordinary form fields; live Gemma selected |
| 6–16 s | New inference with first-author Yes / presenter Yes: two MATCH findings, review still required |
| 17–27 s | New inference with first-author No / presenter Yes: one NOT MATCH and one MATCH |
| 28–38 s | New inference with first-author Yes / presenter Unknown: one MATCH and one UNKNOWN |
| 38–45 s | Actual Markdown download verified, then full report opened |
| 45–47 s | Title edited; old result and download cleared |

[Event timestamps](../evidence/public-ui/events.json),
[screenshots](../evidence/public-ui/), and the
[actual downloaded report](../evidence/public-ui/downloaded-report.md) support the
walkthrough. The video digest and recording details are in
[the manifest](../evidence/public-ui/recording-manifest.json).

The broader eight-source evaluation is separate. All three held-out samples
needed review and gave no supported applicant comparisons for that fictional
profile. The video illustrates functionality on a simple condition, not general
accuracy. No fixture, model-response mock, time compression or fabricated result
appears in the recording.

## Reproduction

Start Ollama and the app, then run `scripts/record_demo.cjs` as documented in
[local capture steps](LOCAL_CAPTURE_STEPS.md). Each click makes a new live request.
Do not rerun the held-out evaluation to record a demo.
