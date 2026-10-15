# Official-source evaluation rubric

The split was committed before implementation. Labels below are reviewed against
original organizer text by the coding assistant, separately from the evaluated
Gemma. **No independent human adjudicator has checked them.** They are provisional,
human-reviewable reference annotations, not established ground truth. Reviewer
bias, category ambiguity and shared organizers limit inference.

Each case contains eight selected original paragraphs/list items. Public annotations
record source line numbers, hashes and labels; full source copies remain ignored.
This tests paragraph interpretation on real text, not complete extraction of every
condition in a whole website. Linked policies and page navigation are excluded.
All selected passages must be returned exactly once. Original fixture files and
synthetic evaluation metrics are unrelated and unchanged.

## Labels and scoring

- `requirement`: positive applicant condition; `exclusion`: barred applicant,
  submission or activity; `document`: required materials; `funding_limit`:
  restriction on applicant funding/expenses (not necessarily a request ceiling).
- `award`: sponsor benefit amount; `deadline`: any dated milestone; `optional`:
  nonmandatory guidance; `context`: headings/background; `unclear`: mixed or
  conditional meanings that cannot safely be reduced to one category.
- Keys identify supported applicant facts; `unknown` denotes a criterion outside
  the supported keys. Compound conditions may have multiple keys. An amount
  awarded is never automatically an applicant request ceiling. A future-stage
  exception is not equivalent to a current-stage requirement.
- A prediction is the tuple (source case, paragraph ID, primary kind, key). Micro
  precision = exact matches / predicted tuples; recall = exact matches / reference
  tuples; F1 is their harmonic mean. Counts and denominators are always published.
  These are **criterion-label** metrics, not applicant eligibility accuracy.
- Mandatory recall uses the same exact tuple match restricted to paragraphs labeled
  requirement, exclusion, document or funding_limit. This intentionally penalizes
  a model that treats an exclusion as harmless context. It is recall only within
  selected passages, not all conditions on the complete source website.
- Paragraph category accuracy and exclusion category recall are reported separately.
  Unsupported predictions count when the key is unknown. End-to-end unknowns,
  contradictions, report failures and observed wall time are reported separately
  from extraction. Passage-scope review reminders are counted separately from
  unsupported model interpretations.

The explicit regex classifier in `realworld.candidates` is the NO AI baseline.
Gemma uses the identical text, and the hybrid report permits a comparison only
where the model and explicit rules agree. No baseline response replaces a failed
model response. A lower model score is reported as such; no superiority is assumed.

All held-out requests run once after a committed candidate freeze. A failed call
stays in the denominator with zero predicted tuples; raw generated responses,
errors and latency remain in evidence. No retries of held-out inference and no
prompt tuning after results. Public audits exclude prompt/source copies and Ollama
context token IDs; exact generated label JSON is retained.

## Development strategy history

The initial six-passage batches confused passage identities and duplicated criteria.
The single-passage array strategy also repeated keys despite a JSON-schema uniqueness
hint; all five development reports were rejected. Neither failure was repaired into
a result. The next candidate uses fixed Boolean criterion properties per passage,
which makes duplicate list entries structurally impossible. Lexical candidate keys
constrain the schema; Gemma chooses their applicability and the paragraph category.
This hybrid is not an unrestricted semantic extractor. No larger model was downloaded.
Early zero-prediction summaries display precision 0 by convention (0 predictions
means mathematical precision is undefined); reference and prediction denominators
remain available. Some early development probes overlapped; final comparison timings
are observed workflow times, not isolated hardware benchmarks.
