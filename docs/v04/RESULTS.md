# Atomic v0.4 evaluation — NO SHIP

The experimental inference upgrade does not meet the release gates. Keep it on its feature branch. Ship the independently tested onboarding with the unchanged v0.3 engine.

All results below are against coding-assistant provisional annotations, **not independently human-validated ground truth**. Ten development passages / 20 atoms / 3 organizers; eight reserved passages / 20 atoms / 2 different organizers. All three systems use the same preregistered (passage, kind, criterion) unit. Expanded vocabulary disadvantages the legacy schema. These scores do not replace historical scores or establish general accuracy.

| Split / system | TP / predicted / reference | Precision | Recall | F1 | Mandatory | Exclusion | Reports | Mean seconds/case |
|---|---|---|---|---|---|---|---|---|
| Development / v0.3 Gemma | 3 / 13 / 20 | 23.08% | 15.00% | 18.18% | 3/17 | 1/4 | 3/3 | 15.442 |
| Development / Atomic B3 | 1 / 17 / 20 | 5.88% | 5.00% | 5.41% | 1/17 | 0/4 | 1/3 | 50.764 |
| Development / Rules | 8 / 13 / 20 | 61.54% | 40.00% | 48.48% | 8/17 | 1/4 | 3/3 | 0.005 |
| Reserved final / v0.3 Gemma | 1 / 9 / 20 | 11.11% | 5.00% | 6.90% | 1/18 | 0/2 | 2/2 | 16.841 |
| Reserved final / Atomic B3 | 0 / 0 / 20 | 0.00% | 0.00% | 0.00% | 0/18 | 0/2 | 0/2 | 79.504 |
| Reserved final / Rules | 0 / 9 / 20 | 0.00% | 0.00% | 0.00% | 0/18 | 0/2 | 2/2 | 0.007 |

| Split / system | UNKNOWN / non-INFO | False supported MATCH / all MATCH | False supported NOT MATCH / all NOT MATCH | Exact source spans / proposed | Completed passages / total |
|---|---|---|---|---|---|
| dev-A-service-restored | 8/10 | 2/2 | 0/0 | 13/13 | 10/10 |
| dev-B3 | 17/17 | 0/0 | 0/0 | 60/60 | 5/10 |
| dev-rules | 3/10 | 4/7 | 0/0 | 13/13 | 10/10 |
| final-A | 9/9 | 0/0 | 0/0 | 9/9 | 8/8 |
| final-B | 0/0 | 0/0 | 0/0 | 58/58 | 5/8 |
| final-rules | 8/8 | 0/0 | 0/0 | 9/9 | 8/8 |

Zero-denominator rates are undefined, not perfect safety. False-supported counts are disagreements with provisional reference comparison labels for ONE fictional profile, not confirmed real applicant eligibility errors. Kind accuracy uses the same matched/reference numerator and denominator; missing atoms count wrong. JSON files retain missing-atom counts and token totals.

## Failures and limitations
- Initial development A: 0/3 reports because Ollama was stopped. All three failures are preserved separately. Service-restored A uses unchanged inference; there were no reserved-test retries.
- B1: 0/3 reports, rejected invented applicability/dependency text. B2: 0/3, rejected absent dependency spans. B3 keeps full original context beside numbered span proposals; duplicate or inconsistent conditions still reject reports.
- A failed report contributes zero delivered predictions and all its references remain in recall. Validated partial passages and exact spans are diagnostic only, never delivered as a complete report.
- Literal span accuracy is not semantic accuracy. Numbered-span selection structurally prevents model-written quotations; incorrect categories, omissions and duplicated conditions remain real failures.
- Final model code and protocol froze at `083ab38` / manifest commit `e9972c2`, before reserved retrieval. Provisional final labels froze at `e8574ab` before predictions. No final-source tuning or retries.
- Tiny convenience sample, related scientific funding domains, selected paragraphs rather than whole announcements, expanded criterion vocabulary, and non-independent annotations preclude general performance claims. No statistical superiority claim or closed-model comparison.
- No larger model was downloaded; see [hardware and protocol](MODEL_AND_PROTOCOL.md). CPU wall time is measured; CPU utilization/energy and electricity cost are not. Metered inference fees: $0.

## Supplied development regressions
Real local Gemma completed 13/14 profile scenarios and met 4/14 defined behavior checks. Eleven distinct source texts were inferred once each; three repeated-text profile scenarios reused the same real extraction. No fixture or adapter response substituted for inference.
These are development scenarios from an AI usability audit of the v0.3 rule baseline, not human-user evidence. See `evidence/v04/synthetic-live.json` for every result. Deterministic tests separately demonstrate what happens GIVEN supplied semantic proposals; they are not model accuracy tests.

## Preserved evidence and human review
All original benchmarks, references, fixtures, raw failures and v0.2/v0.3 demos remain unchanged. Historical development F1 stays Gemma 42.11% vs rules 62.50%; historical held-out F1 stays 34.48% vs 33.90%, using provisional annotations.
New public JSON has classifications, offsets, hashes and denominators. Full official snapshots and raw source-bearing responses remain in `.source-cache/v04` and `.local-reports/v04`; `evidence/v04/private-evidence-manifest.json` fingerprints them. No failed attempt was discarded.
The blind development review packet is prepared locally with URLs, retrieval dates, source hashes, context, schema and blank fields. No reviewer has completed it. The ISMB postdoc interpretation remains unresolved. Do not replace references with AI reconciliation proposals.

## Decision
**NO SHIP for v0.4 inference.** Completion, recall and practical regressions fail the gates; independent human review is also outstanding. **Ship onboarding only** after its separate browser, security, test and authentic-demo checks. This does not claim improved model accuracy.
