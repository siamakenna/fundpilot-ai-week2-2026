# Stage 2 annotation reconciliation — separate proposed reference

The owner supplied `FundPilot_Stage2_Completed.zip`. Its README, adjudication report
and handoff were read before ingestion. The proposed
[`annotations-development.adjudicated-v2.json`](../evaluation/annotations-development.adjudicated-v2.json)
is preserved byte-for-byte, separately from the original benchmark. This is
AI-on-AI review by Claude, Codex and ChatGPT, **not human-validated ground truth**.
Recommendations in the packet are future design proposals, not changes to the
frozen candidate or scoring protocol.

Local verification confirmed **40/40 passage digests and 5/5 whole-source digests**
against the original October 14 cache. The supplied Stage 1 CSV hash also matches
`88dfbf1d359a36a1cd543ae31381ac003c6976d15e6ad43c370e84009cc3e0c8`.
See [verification records](../evidence/annotation-review/verification.json) and
[the supplied verifier's output](../evidence/annotation-review/cache-verification.txt).
The full archive, spreadsheets, source quotations and reviewer notes remain locally
preserved under ignored `.source-cache/stage2-reconciliation/`; unnecessary source
copies are not republished. The archive digest is recorded for provenance.

The packet proposes 14 changed records out of 40, with 25 KEEP_ORIGINAL,
4 ACCEPT_PRIOR_PROPOSAL, 10 NEW_REVISION and 1 UNRESOLVED dispositions. It yields
50 category/key tuples versus the original 48. These are annotation counts, not
improved model results. No inference was rerun and no post-hoc rescore was performed.
Historical scores, predictions, the original annotations and candidate `35dbeb8`
remain unchanged. Held-out labels use the original committed rubric, not v2.

## Unresolved ISMB postdoc interpretation

`ismb_2026:151` mentions eligible postdoctoral applicants and then excludes postdocs
under the stated current federal-only funding source. Treat current eligibility
as unresolved pending sponsor clarification; do not treat the broad stage list as
permission to apply. The original exclusion label is carried forward provisionally
in v2. No sponsor was contacted or answer invented.

Replaying the stored live v4 labels through the frozen checks with a fictional
Postdoc profile leaves all findings for this paragraph UNKNOWN, including stage
and federal employment. This is a deterministic replay, not a new model evaluation;
[the record](../evidence/annotation-review/ismb-postdoc-abstention.json) shows it.

The reconciliation exposes real ontology limits: positive prerequisites and their
negations overlap, binding deadlines are outside the original mandatory-category
metric, post-award duties differ from application eligibility, and conditional
alternatives cannot be fully represented by one primary category. These limitations
qualify the scores; they are not silently corrected after seeing predictions.
