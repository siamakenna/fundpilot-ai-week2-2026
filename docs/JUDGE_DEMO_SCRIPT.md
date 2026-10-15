# Judge walkthrough — actual public-text workflow

[Public video](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.2.0/fundpilot-public-call-demo.webm) · [Release](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/tag/v0.2.0)

The automated recording is 47.32 seconds, silent, and unedited. It uses one short
CNS 2027 eligibility passage, with explicit attribution and fictional applicant
facts. It is a focused product demonstration, not a full-call eligibility decision.

| Approximate point | What actually happens |
| --- | --- |
| 0–6 s | Public source text and ordinary form fields; live Gemma selected |
| 6–16 s | New inference with first-author Yes / presenter Yes: two MATCH findings, review still required |
| 17–27 s | New inference with first-author No / presenter Yes: one NOT MATCH and one MATCH |
| 28–38 s | New inference with first-author Yes / presenter Unknown: one MATCH and one UNKNOWN |
| 38–45 s | Actual Markdown download verified, then full report opened |
| 45–47 s | Title edited; old result and download cleared |

[Event timestamps](../evidence/public-ui/events.json),
[screenshots](../evidence/public-ui/), and the
[actual downloaded report](../evidence/public-ui/downloaded-report.md) support the
walkthrough. The video digest and recording details are in
[the manifest](../evidence/public-ui/recording-manifest.json).

The broader eight-source evaluation is separate. All three held-out samples
needed review and gave no supported applicant comparisons for that fictional
profile. The video illustrates functionality on a simple condition, not general
accuracy. No fixture, model-response mock, time compression or fabricated result
appears in the recording.

## Reproduction

Start Ollama and the app, then run `scripts/record_demo.cjs` as documented in
[local capture steps](LOCAL_CAPTURE_STEPS.md). Each click makes a new live request.
Do not rerun the held-out evaluation to record a demo.
