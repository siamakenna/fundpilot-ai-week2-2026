# v0.4 error analysis and boundaries

The unchanged v0.3 engine and saved predictions were replayed without new inference.
Counts below come from `evidence/v04/historical-diagnostics.json` and original,
provisional annotations. Old held-out results are now observed diagnostic material,
not an untouched final test. Claude's ten scenarios used **rules, NO AI**; they are
neither live Gemma results nor human-user validation.

| Failure class | Observed evidence | Engineering response |
|---|---|---|
| Segmentation | 0 missing/misnumbered paragraph IDs in 40 development and 24 old held-out paragraphs; this does not establish semantic completeness | Retain paragraph provenance; permit multiple atoms per paragraph |
| Kind compression | 20 development and 11 old held-out paragraph-kind errors | Kind belongs to each atom, not the whole paragraph |
| Compound clauses | 7 multi-reference-key paragraphs in each split; compound cues overlap tuple errors in 14 development / 13 old held-out paragraphs | Multiple criteria and explicit AND/OR/EXCEPT dependency evidence |
| Missed exclusions | 6 of 12 development exclusion paragraphs had a kind miss; 0 of 4 old held-out | Surface potential blockers without guessing broad job-title equivalence |
| Vocabulary restriction | 0 development but 6 old held-out named reference keys outside lexical candidates | Allow novel reviewable criterion names; no candidate-list suppression |
| Temporal/applicability scope | Temporal cues overlap tuple errors in 12 development / 6 old held-out paragraphs | Preserve source-stated applicability; abstain on unsupported timing |
| Model/rule disagreement | Kind disagreements in 22 development / 15 old held-out paragraphs | Keep semantics provisional; exact evidence alone never authorizes a comparison |
| Practical usefulness | 38 UNKNOWN / 1 NOT MATCH / 4 MATCH / 5 INFO historical development findings; 24 UNKNOWN / 3 INFO old held-out | Group verification actions and distinguish records to check from sponsor interpretation |

Cue categories overlap and are descriptive, not causal attribution. Historical
labels do not independently establish true applicant eligibility errors. The
separate AI adjudication proposal is not substituted for the original references.
The ISMB postdoc interpretation remains unresolved: the available wording and
provisional annotations do not justify silently asserting a single interpretation.

New retrieval also exposed HTML source wrapping inside a paragraph. The original
HTML and text remain untouched. A separately hashed derived paragraph view collapses
whitespace inside text nodes while retaining structural breaks; it is not model output.

## Human review

Run `python -m scripts.prepare_v04_review` to create the private blind packet at
`.local-reports/v04/blind-human-review-development.md`. It contains ten development
passages, adjacent context, URLs, dates, hashes, offsets, definitions and blank
annotation fields, with no predictions or reference answers. Reserved final content
is not included. No human review has occurred; engineering proceeds without it.
A consenting domain-competent reviewer may annotate it and preserve their original
answers separately before reconciliation. Do not overwrite the provisional benchmark.
