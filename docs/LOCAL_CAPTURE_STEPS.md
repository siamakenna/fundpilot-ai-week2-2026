# Authentic local walkthrough capture

The available automation can drive the browser and save screenshots, but does not
expose native screen recording. No video has been created or uploaded. The PNGs in
`evidence/` are real browser captures, not design mockups or model-generated images.

## Start the app on this Mac

Open Terminal and run:

```bash
cd /Users/makennarodriguez/Downloads/fundpilot_side_hustle_starter
source .venv/bin/activate
export PATH="$PWD/.tools/ollama:$PATH"
OLLAMA_NO_CLOUD=1 ollama serve
```

If it reports that port 11434 is already occupied, the existing Ollama service may
already be running. Check `ollama list` in a second Terminal; it must show
`gemma3:1b`. If absent, run `ollama pull gemma3:1b` once.

In that second Terminal:

```bash
cd /Users/makennarodriguez/Downloads/fundpilot_side_hustle_starter
source .venv/bin/activate
GRADIO_ANALYTICS_ENABLED=False python app.py
```

Open the localhost URL printed by Gradio (normally http://127.0.0.1:7860).
Select **Live local Gemma**. Keep the fictional data unchanged. Do not put a private
profile or real grant document on screen.

## Record with macOS Screenshot

1. Press **Shift–Command–5**, choose **Record Selected Portion**, and frame the
   browser window. Under Options choose a save location and a microphone if you
   want narration. Close unrelated windows and notifications first.
2. Click Record. Introduce the problem in one sentence: “Before writing a travel
   award application, I want to know which conditions match and what I still need
   to verify.” Point to the three steps and the fictional-data label.
3. Use **Alex Morgan → Early Career Science Conference Travel Award → Live local
   Gemma → Analyze requirements**. Let inference finish on screen. Say that only
   call text goes to local Gemma; profile comparison happens in Python. Show the
   actual result, including any UNKNOWN or error; do not substitute a fixture run.
4. Switch to **Enrolled Graduate Student Mobility Grant**. The old result should
   disappear. Analyze again and show the enrollment quote and amount comparison.
5. Switch back to **Early Career Science Conference Travel Award**, choose
   **Casey Rivera**, and analyze. Point to missing presentation acceptance and the
   verification questions.
6. Click the Markdown download link. Open the downloaded report and show its live
   mode and model name. Mention that exact quotes do not prove complete extraction.
7. Briefly show `docs/EVALUATION.md` and the saved raw model response. State the
   actual measured development-set result and the limitation: six synthetic calls
   are not validation on real funding documents.
8. End with the business hypothesis: a small readiness report for independent
   researchers or mentors; no customers, payments or testimonials are claimed.
9. Stop with the menu-bar stop button or **Command–Control–Escape**. Review the
   entire recording. Keep actual wait times visible or clearly label any cuts;
   never imply that an edited delay is a measured latency.

Aim for 2–3 minutes, or retain a longer truthful recording if local inference is
slow. Upload only after reviewing the content. Add its real URL to the DEV draft's
Demo section. That upload and DEV publication remain manual steps; this task does
not authorize publishing the DEV post.
