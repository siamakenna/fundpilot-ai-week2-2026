# Functional upgrade audit

Baseline: `5b5d568c0dceb234bbe5e34db8d6a1c558d110e4`, preserved on main.
Work branch: `codex/real-world-readiness`. Audit date: October 14, 2026.

| Priority | Concrete baseline limitation | User impact / upgrade criterion |
| --- | --- | --- |
| P0 | `logic.assess(needs_clause_review=True)` overwrites every custom finding with UNKNOWN | Evaluate explicitly supported conditions against ordinary applicant facts; retain uncertainty for interpretation, coverage and sponsor decisions |
| P0 | `app.py` starts with fictional profile/call and reference mode; facts require JSON | Make paste + normal form + live local model the primary three-step flow |
| P0 | Currency marker forces `request_at_most` or `unmapped` | A $500 stipend is not a $500 applicant-request restriction; label money roles separately |
| P0 | 13 fixed keys and no exclusion/exception model | Real policies have funding-source overrides, membership durations and prior-award restrictions; expose unresolved dependencies, never approve by omission |
| P1 | Per-sentence model calls discard list headings and context | Preserve numbered source spans and nearby context; require a response for every span and reject duplicate/missing IDs |
| P1 | No deadlines or dated call status | Show date evidence, distinguish application/registration/notification dates, and flag historical sources |
| P1 | Single catch-all error and raw transport details | Useful recovery instructions and no stale download after any input change or failure |
| P1 | 95.24% measured on tuned fictional data only | Freeze official-source development/holdout split before tuning; compare simple rule baseline on same inputs |
| P2 | Developer installation and raw CLI assumptions | Document one-time local setup; a non-developer can use the form once runtime is running; do not claim turnkey distribution |

A previously unseen announcement can be pasted in the baseline but does not yield
usable matching findings. No existing experiment establishes superiority over a
rule baseline. Official eligibility remains the sponsor's decision; the product
should report application readiness and rule comparisons, not approval.

The three requested official pages were inspected. CNS is a current 2027 call
with a November 3, 2026 application deadline. ISMB 2026 and the 2026 SfN TPDA
application cycle are historical tests. ISMB's current-funding exclusion overrides
its broad mention of postdocs; SfN's virtual option does not carry a travel stipend.
Those relationships are not represented by the baseline enum.

## Evaluation discipline

`evaluation/source_split.json` fixes five development and three held-out pages
before extraction changes. Holdout content will be opened only after a candidate
freeze. Organizers overlap across splits; no organizer generalization claim.
Annotations will be assistant-authored and source-reviewed, never described as
independent human labels. Full retrieved text stays in ignored local storage;
public records contain attribution, hashes, short excerpts and paraphrased rules.
A failed holdout case remains a failure; tuning afterward requires retiring that
holdout status, not silently rescoring the same examples as unseen.
