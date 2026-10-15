# Authentic automated capture

A completed Playwright recording is preserved locally at:
`.local-reports/queue-demo-release/fundpilot-verification-queue-demo.webm`.
Its [public release](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/tag/v0.3.0) contains the verified video asset. Recording is already complete; no manual recapture is required.

The existing Mac has Playwright, Chromium 151.0.7922.34 and its bundled FFmpeg.
These are developer tools, not new application dependencies. The script captures
actual browser interactions and local Gemma results. It never mocks requests.

To reproduce on this Mac, from the repository:

```bash
GRADIO_ANALYTICS_ENABLED=False .venv/bin/python -c "import app; app.demo.launch(server_name='127.0.0.1', server_port=7862, show_error=False)"
```

Then in another terminal, while local Ollama is running:

```bash
NODE_PATH=/Users/makennarodriguez/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules \
/Users/makennarodriguez/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node \
scripts/record_queue_demo.cjs .local-reports/new-recording http://127.0.0.1:7862
```

On another computer, use an existing Node/Playwright installation with Chromium;
set NODE_PATH only if needed to locate it. Use a new output folder. The script
saves a WebM, screenshots, actual report bytes and an event log. Keep source and
profile scope visible. Review the result before sharing it. Never present the
fictional reference mode as model inference.

The original v0.2.0 recording and `scripts/record_demo.cjs` remain unchanged.
For v0.3.0, earlier takes are retained in `.local-reports/queue-demo/`,
`queue-demo-verified/` and `queue-demo-final/`. Recording automation needed an
explicit scroll and an accordion selector that tolerates its arrow label. The
final take in `queue-demo-release/` passed every check. These changes did not
alter the model, source, profile logic or frozen evaluations.

## Publication remaining

Review the finished DEV article and demo. Sign in to DEV, paste the article using
the official Week 2 template, preserve its headings and `devchallenge` and
`hf26challenge` tags, preview links, and publish one entry only when ready.
Deadline: October 18, 2026, 11:59 PM PDT (October 19, 2:59 AM EDT).
