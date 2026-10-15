# v0.4 preregistered comparison and independent-review protocol

This experiment is separate from the v0.3.0 submission. Previous development and
held-out data are historical diagnostic material. Their files and scores stay intact.
The fresh split contains three development organizers and two reserved organizers,
all different from the historical benchmark. Up to four coherent original passages per source are
selected for meaningful obligations; this convenience sample is not full-page recall.

## Annotation and blinding

Before running a split, read its official snapshot and create provisional atomic
labels without looking at predictions. Record source URL, retrieval time, snapshot
hash, line number and passage hash. Do not publish full source copies. A private
review packet contains the selected passages, surrounding context and blank label
fields, but no predictions, proposed answers or model identity. Independently have
a domain-competent human annotate each atom and its dependencies; reconcile disagreements
with rationale and reviewer identity/consent. Never silently replace provisional labels.

No human reviewer has been secured yet. The coding assistant's provisional labels
are neither independent of the implementation nor human ground truth. Gemma does
not grade itself. Automated scores against those labels are diagnostic only. No
release based solely on unreviewed annotations. The owner has been asked to arrange
review; no unsolicited sponsor/reviewer messages will be sent.

## Atomic labels and fair comparison

Each atomic reference is (source, passage, obligation kind, canonical criterion),
with evidence offsets, operator/value where meaningful, source-stated applicability,
relationship and expected supported-comparison status for the declared fictional
profile. Kind: eligibility, exclusion, required_material, funding_condition,
deadline, sponsor_benefit, informational. A paragraph may have multiple kinds.
Dependencies (AND/OR/EXCEPT/CONDITIONAL/UNRESOLVED) never imply a supported outcome.

Retain existing criterion names: membership, career_stage, first_author,
presenting_author, abstract_submitted, abstract_accepted, in_person, registration,
prior_award, us_federal_employee, upfront_costs, financial_need, request_limit,
documents, unknown. Additional concepts use stable names: residency, institution,
career_duration, other_funding, research_topic, event_attendance, expense_scope,
award_amount, application_timing, visit_duration, selection. Novel model strings
remain separate candidates, never discarded by the old lexical vocabulary. No
post-result synonym remapping or reference edits to improve a score.

Map old kinds without changing old predictions: requirement→eligibility,
document→required_material, funding_limit→funding_condition, award→sponsor_benefit,
optional/context→informational, exclusion/deadline unchanged, unclear→unclear.
All candidates and unchanged regex baseline are scored on the same labels. A
second legacy-vocabulary view may be diagnostic, but cannot replace the primary
comparison. New vocabulary creates a known expressivity disadvantage for the old
baseline; a score difference alone is not a demonstrated practical advantage.

## Measurements

- Exact criterion precision/recall/F1: multiset intersection of (passage, kind,
  criterion). Report TP, predicted and reference denominators. Duplicate predicted
  atoms count as false positives. Do not score operator correctness as if included.
- Clause-kind accuracy: align by passage + criterion; count correct kinds over all
  reference atoms (missing atoms wrong). This is reference-atom kind accuracy, not
  best-case accuracy over only matched predictions.
- Mandatory recall includes eligibility, exclusion, required_material,
  funding_condition and binding deadline atoms. Exclusion recall is separately exact.
- Missing conditions = unmatched reference atoms. False supported MATCH/NOT MATCH =
  a supported finding with no exact reference match or incompatible reference
  comparison label, for the single declared profile. Not real-world eligibility error.
- UNKNOWN rate = UNKNOWN / all non-informational proposed findings; separate source
  coverage reminders. Failures also reported, never excluded from case denominators.
- Source-span accuracy = validated exact attached spans / proposed atoms; invalid
  evidence rejects the report and is retained as a failure, not silently repaired.
- Completion/failure per case and passage; raw response/error logs retained locally,
  published predictions redact quote text while retaining spans and hashes. Keep all
  failed attempts and metrics. Report wall latency, token counts, hardware/model,
  and zero metered API fees; energy/electricity cost is unmeasured, not free inference.

## Freeze and release gate

Commit source split before tuning. Freeze B code/prompt/schema, model configuration,
scorer, development labels and selection method before opening reserved eligibility
bodies. Select and annotate final passages before predictions; run A, B and any
feasible C once on the same inputs. No final-test tuning, retries or cherry-picking.
All failed reports yield no delivered prediction tuples; partial model proposals are
retained in audits and count toward span diagnostics, not usable report completion.

A = unchanged v0.3.0 hybrid; B = atomic Gemma 3 1B; C = same frozen atomic strategy
with stronger local Gemma only after hardware assessment. Rules = unchanged regex
classifier. Historical A predictions are reused for old diagnostics, not rerun.

To recommend replacing v0.3.0: independent review completed; exact F1 at least 5
percentage points above A on development and final, with no worse mandatory or
exclusion recall, completion or false-supported count; no safety regression; bounded
runtime and full product checks pass. Compare rules transparently; do not claim a
baseline victory from changed representation. Otherwise keep v0.3.0 for the contest,
open an experimental PR with limitations, and do not change the DEV article/demo.
