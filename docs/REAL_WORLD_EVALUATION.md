# Real-source evaluation: public-call upgrade

This evaluation is separate from the historical 20/21 synthetic development result.
It uses selected original passages from official organizers, fictional applicant
facts, actual local Gemma inference and an explicit rule baseline. It does not
establish general eligibility accuracy or complete coverage of whole announcements.

## Protocol and annotation limits

The five-development/three-held-out split was committed before implementation in
`3795fea`. The original three requested sources are development cases. The reserved
sources' bodies are not opened until candidate freeze. Organizers overlap across
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
