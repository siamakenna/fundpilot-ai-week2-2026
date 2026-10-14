# Finish the authentic video demo

## What automation verified

On October 14, release QA found macOS `/usr/sbin/screencapture` with video support,
but `CGPreflightScreenCaptureAccess()` returned **false** for the command process.
No screen-recording permission was changed. `ffmpeg` and `obs` were not on PATH.
The available browser automation exposes screenshots, not video recording; native
app control is disabled. A metered remote browser recorder cannot reach this
loopback-only app and was not used. No video was made or uploaded.

The existing PNGs are authentic browser screenshots, not a video. The earlier
`evidence/UI_CHECKS.md` describes the capabilities exposed during that session;
this permission check is the more specific current recording result.

## Record, review and upload (the remaining demo task)

The app and Ollama answered health checks at QA time. Open
http://127.0.0.1:7860. If it is still running, skip the startup commands below.

1. Press **Shift–Command–5 → Record Selected Portion**. Frame only FundPilot;
   hide unrelated windows and notifications. Choose a microphone under Options
   if narrating. Click **Record**.
2. Select **Live local Gemma** and analyze these three pairs, waiting for each real
   result: **Alex Morgan / Early Career Science Conference Travel Award**;
   **Alex Morgan / Enrolled Graduate Student Mobility Grant**;
   **Casey Rivera / Early Career Science Conference Travel Award**.
   Show the actual outcomes, even if a run fails. Keep waits visible or label cuts.
3. Download and open the Markdown report. Explain that Python attaches source
   sentences and checks profile facts; Gemma classifies requirements. End with
   “20/21 clause matches on six tuned fictional calls; five reports validated;
   real-world accuracy and pricing are unvalidated.” The
   [short narration script](JUDGE_DEMO_SCRIPT.md) is optional.
4. Stop with **Command–Control–Escape**, review the whole clip, and upload it to
   your chosen video host with viewing available to anyone with the link. Open
   that URL in a signed-out/private window to verify playback.
5. Replace the video placeholder in `README.md` and
   `docs/DEV_SUBMISSION_DRAFT.md` with the verified URL; remove the article's
   publication-blocker note. Update the status in `docs/RELEASE_READINESS.md`,
   commit and push those documentation changes. No benchmark rerun is needed.

No editing, paid service or new infrastructure is required. Recording can be longer
than 2–3 minutes if inference is slow. Do not substitute fixture mode for a live run.

## Only if the local services have stopped

In one Terminal:

```bash
cd /Users/makennarodriguez/Downloads/fundpilot_side_hustle_starter
OLLAMA_NO_CLOUD=1 .tools/ollama/ollama serve
```

An address-in-use message means a service already owns port 11434; check
`.tools/ollama/ollama list` from the project directory. `gemma3:1b` was already
installed during development; do not download it again unless it is absent.

In another Terminal:

```bash
cd /Users/makennarodriguez/Downloads/fundpilot_side_hustle_starter
GRADIO_ANALYTICS_ENABLED=False .venv/bin/python app.py
```

## Publication remains the owner's decision

DEV opened at sign-in during QA, so no authenticated draft could be saved. After
adding the video, sign in to DEV, open the official challenge's Submission Template,
and paste the completed article. Set the title and tags `devchallenge` and
`hf26challenge` (front matter belongs in the Markdown editor, not the rendered
article). Preview links and the video, then publish **one** entry only when ready.
The deadline is October 18, 2026, 11:59 PM PDT (October 19, 2:59 AM EDT).
Review the [official rules](https://dev.to/page/hacktoberfest-week2-2026-10-12-contest-rules)
for personal eligibility and publication terms. This continuation did not publish
or submit the entry.
