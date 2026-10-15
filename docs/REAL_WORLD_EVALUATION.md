# Real-source evaluation: public-call upgrade

This evaluation is separate from the historical 20/21 synthetic development result.
It uses selected original passages from official organizers, fictional applicant
facts, actual local Gemma inference and an explicit rule baseline. It does not
establish general eligibility accuracy or complete coverage of whole announcements.

## Protocol and annotation limits

The five-development/three-held-out split was committed before implementation in
`3795fea`. The original three requested sources are development cases. The reserved
sources' bodies were not opened until candidate freeze. Organizers overlap across
splits; this is source-disjoint, not organizer-disjoint or guaranteed clause-disjoint.

Eight paragraphs per source are selected and labeled according to
[the rubric](../evaluation/RUBRIC.md). The coding assistant checks these against
original text separately from the evaluated Gemma. **No independent human has
adjudicated the labels.** They are provisional reviewable annotations. Mixed
paragraph categories and reviewer choices introduce uncertainty; the numerical
scores should not be read as a validated real-world accuracy estimate.

The exact matching unit is (paragraph ID, category, criterion key). Thus compound
paragraphs can contribute multiple criterion labels. Precision, recall and F1
measure extraction/classification of those labels, not whether an applicant wins
an award. Mandatory recall is limited to selected required/exclusion/materials/
funding-restriction paragraphs. Hashes and original line numbers support review
without redistributing full source documents.

## Development strategies

| Strategy | Reports completed | Exact label matches | Precision | Recall | F1 | Mandatory-label recall |
| --- | --- | --- | --- | --- | --- | --- |
| Six-passage batches, array keys (v1) | 3/5 | 4/48 reference, 4/32 predicted | 12.50% | 8.33% | 10.00% | 4/34 |
| One-passage arrays (v2) | 0/5 | 0/48 reference; no complete returned label sets | undefined | 0% | 0% | 0/34 |
| One-passage Boolean fields (v3) | 5/5 | 19/48 reference and predicted | 39.58% | 39.58% | 39.58% | 17/34 |
| Final focused Boolean prompt (v4, selected candidate) | 5/5 | 20/48 reference, 20/47 predicted | 42.55% | 41.67% | 42.11% | 15/34 |
| Rule baseline on the same development passages | 5/5 deterministic runs | 30/48 reference and predicted | 62.50% | 62.50% | 62.50% | 23/34 |

The array variants repeated criteria; the application rejected those reports instead
of deduplicating them into apparent success. The Boolean schema replaces list entries
with named fields. Lexical rules constrain possible criterion keys; Gemma selects
applicability and category. This is a hybrid, not unconstrained extraction.

The selected final prompt (v4) targets exclusions, mixed conditions and money roles.
It improves overall F1 over v3 and exclusion category recall from 3/12 to 6/12,
but mandatory-label recall falls from 17/34 to 15/34. The rule baseline remains
stronger (9/12 exclusion categories). This tradeoff is disclosed, not a model victory.
Final development time: mean 50.212 s, range 45.292–55.199 s, n=5.
There were 13 unsupported-key predictions among 47 predicted labels; all five
reports completed. No larger model was downloaded.

## Frozen held-out pass

Candidate `35dbeb8` was frozen by `evaluation/candidate-freeze.json` in `15d1ff8`.
Reference labels and the access-driven SEB-to-RSC substitution were committed in
`881c83f` before any held-out model request. SEB returned HTTP 401; no body or result
was obtained. The RSC official page was available through public web retrieval
although direct curl returned 403. There was **one held-out pass, no retries**, and
no subsequent model, prompt or rule tuning. The frozen engine hash is checked by
the evaluator. Two held-out organizers overlap development; shared wording limits
independence. Replacement source selection occurred after freeze but before inference.

| Measure | Live Gemma hybrid labels | Explicit rules |
| --- | --- | --- |
| Exact matches / predictions / references | 10 / 26 / 32 | 10 / 27 / 32 |
| Precision | 38.46% (10/26) | 37.04% (10/27) |
| Recall | 31.25% (10/32) | 31.25% (10/32) |
| F1 | 34.48% | 33.90% |
| Selected mandatory-category label recall | 5/15 (33.33%) | 5/15 (33.33%) |
| Paragraph category matches | 13/24 | 12/24 |
| Exclusion category matches | 4/4 | 3/4 |
| Unsupported-key predictions | 10/26 labels | 10/27 labels |
| Completed / failed cases | 3 / 0 | 3 / 0 |

Live wall time: mean **38.460 s**, range **36.476–42.356 s**, n=3 eight-passage
cases. Timings are actual workflow observations including validation, not isolated
hardware benchmarks. The baseline's runtime was not instrumented; no latency
speedup is claimed. [Raw cases and responses](../evidence/realworld-heldout/)
retain every prediction.

The tiny F1 difference comes from one fewer predicted tuple, with identical 10
matches and mandatory recall. It is **not evidence of meaningful model superiority**.
The development baseline was substantially stronger. No closed model was tested.

## End-to-end report usefulness and limits

| Source sample | MATCH | NOT MATCH | UNKNOWN | INFO | Readiness |
| --- | ---: | ---: | ---: | ---: | --- |
| CNS (development) | 1 | 1 | 7 | 2 | Contradictions to resolve |
| ISMB fellowships (development) | 0 | 0 | 11 | 1 | Review required |
| SfN TPDA (development) | 3 | 0 | 6 | 0 | Review required |
| Biologists travel (development) | 0 | 0 | 8 | 0 | Review required |
| Biochemical travel (development) | 0 | 0 | 6 | 2 | Review required |
| Biochemical online (held-out) | 0 | 0 | 8 | 0 | Review required |
| ISMB dependent care (held-out) | 0 | 0 | 9 | 1 | Review required |
| RSC researcher travel (held-out) | 0 | 0 | 7 | 2 | Review required |

For the single fictional evaluation profile: development has 4 MATCH, 1 NOT MATCH,
38 UNKNOWN and 5 INFO findings (48 total); held-out has **0 supported matches or
mismatches**, 24 UNKNOWN and 3 INFO (27 total). Each report separately includes eight
passage-scope review reminders; those are not inflated into criterion counts.
These are report outputs, not human-validated verdict accuracy. No complete official
eligibility claim is generated by design; this is not an empirical false-positive
rate estimate. All three held-out reports needing manual review is a substantive
product limitation. Supported comparisons work on simpler public conditions, as
shown in the separate browser demo; they do not generalize to every real announcement.

## Later AI annotation reconciliation

The owner supplied a separate AI-on-AI review of all 40 development passages.
[The verification report](ANNOTATION_REVIEW.md) confirms 40/40 passage and 5/5
snapshot hashes. Its proposed v2 changes 14 records and contains 50 labels rather
than 48. It remains separate, was not used for tuning or held-out scoring, and has
not been rescored. Historic scores above retain their original reference version.
ISMB postdoc interpretation remains unresolved pending sponsor clarification.
The original mandatory metric is restricted to four categories; binding deadlines
and some conditional obligations are excluded. It must not be described as recall
of every mandatory source condition.

## Model and workflow boundaries

Gemma 3 1B Q4_K_M runs through local Ollama 0.40.4 on the development Intel Mac,
using CPU inference, temperature 0, seed 42 and an 8192-token context setting.
The final request budget is 256 generated tokens per paragraph. Source size and
paragraph length are bounded. Requests time out after at most 90 seconds; a
five-minute overall budget stops incomplete analyses. No fixture fallback or
inference retry occurs inside a case.

Python attaches exact original character spans. Candidate rules and model labels
must agree before a supported applicant-fact comparison is made. Exceptions,
negations and uncertain scope prevent confident comparisons where unsupported.
Additional passage-review reminders are separate from criterion counts. A full
source-coverage count is not proof of semantic completeness. No real-call report
returns official eligibility approval.

Observed workflow times include parsing, model requests and validation on one
ordinary laptop. They are not isolated throughput, production latency or a
statistical estimate. Early development probes overlapped briefly. Failed cases
remain in denominators and raw failure records are retained.

## Interpretation

The measured development evidence does not establish that Gemma is better than
simple rules. The practical improvements are a usable form, actual public text,
explicit disagreement/unknown findings, separate money/date roles and traceable
reports. Reliability on complex exclusions and dependencies remains a limitation.
Commercial pricing, customer benefit and willingness to pay remain unvalidated.
