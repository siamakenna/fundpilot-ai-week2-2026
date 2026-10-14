# Commands and execution record

Work directory: `/Users/makennarodriguez/Downloads/fundpilot_side_hustle_starter`.
The initially selected `Documents/ChatGPT/hackthon projs` directory was empty;
no research project was changed. User-facing continuation date: October 14, 2026.
Raw tool/OS timestamps in evidence are preserved as recorded.

## Setup and original-code checks

```bash
python -m pytest -q       # initially failed: python was not on PATH
python -c 'import app'    # initially failed for the same reason
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
source .venv/bin/activate
python -m pytest -q       # original starter: 19 passed
GRADIO_ANALYTICS_ENABLED=False python -c 'import app; print("app import OK")'
GRADIO_ANALYTICS_ENABLED=False python app.py
```

One early import overlapped dependency installation and failed with missing
Gradio; the post-install import succeeded. Both logs are retained. The three
original fixture cases were clicked in the real local Gradio browser UI and
returned eligible, not eligible and needs verification. They performed no AI
inference. The UI also exposed a downloadable Markdown report in each case.

## Ollama

`HOMEBREW_NO_AUTO_UPDATE=1 brew install ollama` attempted a source build on this
Intel Mac. CMake was installed; the slow Go/Ollama build was stopped. The official
prebuilt Ollama 0.40.4 archive was downloaded instead and extracted into the
ignored `.tools/ollama` directory. No model/runtime binaries are published.

```bash
curl -fL 'https://github.com/ollama/ollama/releases/download/v0.40.4/ollama-darwin.tgz' -o .tools/ollama-darwin.tgz
tar -xzf .tools/ollama-darwin.tgz -C .tools/ollama
export PATH="$PWD/.tools/ollama:$PATH"
OLLAMA_HOST=127.0.0.1:11434 OLLAMA_NO_CLOUD=1 ollama serve
ollama pull gemma3:1b
ollama --version
ollama list
curl http://127.0.0.1:11434/api/tags
```

Background attempts did not persist across the interrupted session. Initial CLI
connection errors are retained in `evidence/starter-live`. Foreground service
sessions worked. The three original live CLI commands were then executed:

```bash
python -m fundpilot.cli --mode gemma --profile alex_postgrad --opportunity early_career_travel
python -m fundpilot.cli --mode gemma --profile alex_postgrad --opportunity graduate_student_only
python -m fundpilot.cli --mode gemma --profile casey_uncertain --opportunity early_career_travel
```

These original-prompt live reports and `/usr/bin/time -p` results are retained in
`evidence/starter-live-retry`. All returned needs verification; they are not
successful extraction claims.

## Development and release verification

Prompt/schema probes and six-case development evaluations were run locally.
Their raw requests/responses are retained in the numbered evidence directories.
They informed prompt changes and are not independent held-out benchmarks.

```bash
python scripts/evaluate.py --output evidence/evaluation-v5
python scripts/evaluate.py --output evidence/evaluation-final
python scripts/evaluate.py --output evidence/evaluation-v9
python scripts/evaluate.py --output evidence/evaluation-v10
python scripts/evaluate.py --output evidence/evaluation-release
python scripts/adversarial.py
python -m pytest -q
ruff check app.py fundpilot scripts tests --select F
git diff --check
git diff 381205d -- fixtures
```

The directory called `evaluation-final` is an earlier failed candidate, not the
release result. Use `docs/EVALUATION.md` and `evidence/evaluation-release` for the
release benchmark. Evaluation refuses to overwrite an existing output directory.
The full passing test log is `evidence/final-tests.txt`; all adapter mocks are
explicitly named as mocks. No mock result enters live evaluation metrics.

## Public repository

After ownership attestation, MIT licensing, scoped source review and checks:

```bash
git init -b main
git commit -m 'Import independent Week 2 starter as supplied'
git commit -m 'Verify live Gemma classification and harden evidence and uncertainty handling'
git commit -m 'Document measured model results, failures, demo evidence and submission draft'
gh repo create fundpilot-ai-week2-2026 --public --source . --remote origin --push
```

Created and pushed: https://github.com/siamakenna/fundpilot-ai-week2-2026 .
The DEV draft was then updated with this genuinely created URL. No DEV publication,
customer outreach, payment or paid hosting was performed.
