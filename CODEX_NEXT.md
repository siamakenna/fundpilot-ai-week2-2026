# Minimal Codex continuation — preserve your credits

Continue FundPilot AI from the supplied **new independent starter project**. Do not rebuild from scratch or rewrite the already-supplied fixtures. This code was newly authored during the October 12–18, 2026 contest window. Do not copy research or other institutional code.

## Step 1 (blocking): run the existing code and tell the truth

1. Open `README.md`, `docs/PRODUCT_AND_JUDGING.md`, and the source files.
2. Run `python -m pytest -q` and import `app.py`.
3. Verify the Gradio local UI functions for three fixture cases. Fixtures are never Gemma output.
4. Install/start Ollama if needed (with user permission as appropriate), `ollama pull gemma3:1b`, and verify **real** local inference using `python -m fundpilot.cli --mode gemma ...` on at least three fictional scenarios.
5. Validate every returned quote is exact and all required clauses are accounted for; fix Gemma JSON schema/prompt if necessary, never silently fake responses.

## Step 2: improve, test, benchmark

1. Compare actual Gemma extraction to reference fixture clauses. Report requirement extraction precision/recall, unknown/failure outcomes and latency with denominators. Distinguish adapter mocks from live inference.
2. Fix bugs and improve the UI's readability. Keep three-step workflow and downloadable report. Avoid new integrations unless MVP is working.
3. Test prompt-injection handling and dangerous overconfidence: missing model, malformed JSON, unsupported conditions, omitted mandatory clauses, negative cap, unclear funding criteria.

## Step 3: prepare submission

1. Create a **new** public GitHub repository only after verifying original code licensing and no restricted NIH/third-party information. Add real commit history and README.
2. Capture an authentic video walkthrough, or provide exact local capture steps if GUI tools are unavailable.
3. Complete `docs/DEV_SUBMISSION_DRAFT.md`, substantiating real findings and leaving no invented URL/metrics/testimonials. Draft in English and preserve the official headings and hashtags.
4. Include Best Use of Gemma only once Gemma is proven to be integral. Don't claim Render/DigitalOcean/etc. without material integration.
5. Do **not** publish the DEV post, claim first-user feedback, or spend money without explicit approval.

## Non-negotiables

Deadline: October 18 at 11:59 PM PDT. Newly built Week 2 code only. One entry; prioritize a verifiable, useful submission and a compelling writeup (writing is the most heavily weighted criterion). Keep the original research projects unchanged. No NIH proprietary code, data, unpublished figures, or grant documents.

Finish by reporting commands run, test counts, confirmed Gemma version, six-case actual evaluation, paths to demo evidence, repo URL if genuinely created, and the precise remaining manual steps.
