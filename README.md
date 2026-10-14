# FundPilot AI (Hacktoberfest Week 2 prototype)

**Status: independent starter code — NOT a verified Gemma demo and NOT a submitted entry.**

Privacy-oriented, evidence-backed, researcher funding readiness. The core value is *honest uncertainty*:
MATCH / NOT MATCH / UNKNOWN, with exact source quotes and a deterministic final verdict.

## Set up

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python -m pytest -q
python app.py
```

For real, **local** Gemma inference, install [Ollama](https://ollama.com/), then:

```bash
ollama pull gemma3:1b
ollama serve # if Ollama service is not already running
python -m fundpilot.cli --mode gemma --profile alex_postgrad --opportunity early_career_travel
```

Your model is not verified to be running merely because this repository implements its API. Verify and benchmark on your own system.

Without Ollama, test the curated fictional reference cases (explicitly **NOT AI**):

```bash
python -m fundpilot.cli --mode fixture --profile alex_postgrad --opportunity early_career_travel
python -m fundpilot.cli --mode fixture --profile alex_postgrad --opportunity graduate_student_only
python -m fundpilot.cli --mode fixture --profile casey_uncertain --opportunity early_career_travel
```

## Privacy, source constraints and limitations

- Fictional funding calls and profiles are synthetic test materials; never display them as real grants.
- Do not load any unpublished NIH or collaborator-owned material into the challenge application.
- Local Ollama only; no external model traffic built in. Gradio runs on 127.0.0.1 with sharing disabled.
- Evidence quotes must match source text exactly. Arbitrary claims or quotes fail.
- A live Gemma extraction is not proof the model found *every* requirement. An unreviewed custom call stays NEEDS VERIFICATION even if all extracted clauses match.
- For built-in fixtures, manually authored mandatory keys detect omissions in the model extraction.
- Unknown or unrecognized requirements are marked UNKNOWN, and negative mandatory findings override positive ones.
- Treat reports as informational, not formal grants-administration or legal advice.
- Only submit measured inference and evaluation numbers. Demo fixture scores are not Gemma performance.
- The code license is **not yet selected**: inspect rights and dependencies before publishing an open-source license.

## Competition

Official rules and categories: https://dev.to/challenges/hacktoberfest-week2-2026-10-12

Target: Best Use of Gemma ($200) and overall ($250); one win maximum per submission. Deadline October 18 2026 11:59 PM PDT. Publish on DEV with tags `devchallenge`, `hf26challenge`, code link and verified demo/video.

See `docs/PRODUCT_AND_JUDGING.md` for positioning, user research, and remaining tasks.
