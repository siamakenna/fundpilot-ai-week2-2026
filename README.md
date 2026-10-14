# FundPilot AI

**A local Gemma prototype for checking fictional funding requirements against supplied facts.**
Before spending hours on a travel-award application, see which conditions match,
which do not, and which still need verification. The result includes exact source
sentences and a downloadable Markdown report.

This independent Week 2 project continues the supplied starter. It is a tested
prototype, not a funder's decision service. **All built-in calls and profiles are
fictional.** No NIH, institutional or private grant material is included.

## Run locally

Requires Python 3.11+ and [Ollama](https://ollama.com/).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m pytest -q
ollama pull gemma3:1b
OLLAMA_NO_CLOUD=1 ollama serve  # separate terminal; skip if already running
GRADIO_ANALYTICS_ENABLED=False python app.py
```

Open the localhost URL printed by Gradio. The three steps are: choose a fictional
researcher, read the fictional call, review evidence and download. Select **Live
local Gemma** to actually run the model. **Curated reference demo (NO AI)** uses
hand-authored fixture clauses and is never presented as model output.

On the development Mac, Ollama 0.40.4 is installed locally in `.tools/ollama`; use
`export PATH="$PWD/.tools/ollama:$PATH"`. That directory is excluded from Git.
`requirements-tested.txt` records the tested Python dependency versions.

## Real model, explicit boundaries

1. Python splits the call into sentences. Every sentence is sent to Gemma.
2. Gemma chooses the supported criterion, mandatory flag and dollar ceiling.
   Sentences with a literal `$` or `USD` marker are restricted to a money-cap or
   unsupported key; other sentences cannot emit a dollar amount. This is a
   documented schema constraint, not a model-generated finding.
3. Python copies the exact input sentence as the quote. **Gemma does not generate
   the quote in the release adapter.** No quote is invented or repaired.
4. Validation checks schema, amount evidence and source identity. Built-in calls
   also compare every classified clause against the authored reference, including
   key, full sentence, amount and mandatory flag. Missing or mismatched clauses
   produce UNKNOWN findings; the reference never replaces model output.
5. Deterministic Python checks the supplied profile. A verified mandatory mismatch
   can yield NOT ELIGIBLE. Unknowns block approval. Edited/custom calls always
   remain NEEDS VERIFICATION, including when the model produces confident labels.

Only funding-call text goes to local Ollama. The profile is evaluated in Python.
Ollama endpoints are limited to loopback; redirects and environment proxies are
blocked. Gradio binds to 127.0.0.1 with sharing and analytics disabled. Setup and
model download require internet. No hosted model API, account or payment flow is
integrated. Reports and browser history are local files; local is not encrypted.

## Reproduce the evidence

```bash
python -m fundpilot.cli --mode gemma --profile alex_postgrad --opportunity early_career_travel --output alex.md --audit alex-live.json
python -m fundpilot.cli --mode gemma --profile alex_postgrad --opportunity graduate_student_only --output graduate.md
python -m fundpilot.cli --mode gemma --profile casey_uncertain --opportunity early_career_travel --output casey.md
python scripts/evaluate.py --output evidence/my-new-run
```

The benchmark refuses to overwrite existing results. Audit files contain the
actual prompts and responses: use only fictional data when sharing them.

- [Measured evaluation and limitations](docs/EVALUATION.md)
- [Command history](docs/COMMANDS_RUN.md)
- [Authentic UI evidence](evidence/UI_CHECKS.md)
- [Exact local video-capture instructions](docs/LOCAL_CAPTURE_STEPS.md)
- [Unpublished DEV submission draft](docs/DEV_SUBMISSION_DRAFT.md)
- [Provenance and dependency licenses](docs/PROVENANCE_AND_LICENSES.md)

## What this prototype cannot establish

The measured release run matched 20/21 clauses (95.24% precision/recall), accepted
5/6 reports and rejected 1/6. All 50 tests pass. A separate CLI run had an
unexplained wall-time outlier; reliable responsiveness is not established.

Six synthetic calls are a development set, not a general accuracy estimate. The
prompt was tuned against these calls. No held-out evaluation, real grants,
customer validation, willingness-to-pay evidence or paid users are claimed.
Earlier failed prompts and their raw responses are retained in `evidence/`.

Sentence splitting loses cross-sentence conditions and context. Currency-marker
routing does not cover all written-out amounts, currencies or mixed conditions.
Dates use supplied years rather than exact anniversaries; self-reported licenses
and presentation acceptances are not independently verified. Confirm full calls,
deadlines, sponsor interpretations and all UNKNOWN findings before acting.

This project does not claim to beat a keyword baseline or a closed model; those
comparisons were not measured. The $9 report / $39 monthly workspace ideas are
unvalidated pricing hypotheses. The current scope has no new hosting integrations.

## License and challenge

Application code and synthetic fixtures: [MIT](LICENSE). Dependencies keep their
own licenses. Gemma 3 weights are downloaded separately under [Google's Gemma
terms](https://ai.google.dev/gemma/terms); they are not included or relicensed.

Created during the October 12–18, 2026 challenge window according to the owner's
attestation; Git records the supplied starter and subsequent real changes. Original
fixture JSON files are unchanged. See the [official Week 2 challenge](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)
for the template, categories and deadline. No DEV post has been published by this
continuation. Any changes made after the deadline must be noted here.
