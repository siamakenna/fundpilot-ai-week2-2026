# Authentic automated capture

A completed Playwright recording is preserved locally at:
`.local-reports/browser-demo-verified/fundpilot-public-call-demo.webm`.
Its public release link is recorded in the README and submission article once the
asset is published. Recording is already complete; no manual recapture is required.

The existing Mac has Playwright, Chromium 151.0.7922.34 and its bundled FFmpeg.
These are developer tools, not new application dependencies. The script captures
actual browser interactions and local Gemma results. It never mocks requests.

To reproduce on this Mac, from the repository:

```bash
GRADIO_ANALYTICS_ENABLED=False .venv/bin/python -c "import app; app.demo.launch(server_name='127.0.0.1', server_port=7861, show_error=False)"
```

Then in another terminal, while local Ollama is running:

```bash
NODE_PATH=/Users/makennarodriguez/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules \
/Users/makennarodriguez/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node \
scripts/record_demo.cjs .local-reports/new-recording http://127.0.0.1:7861
```

On another computer, use an existing Node/Playwright installation with Chromium;
set NODE_PATH only if needed to locate it. Use a new output folder. The script
saves a WebM, screenshots, actual report bytes and an event log. Keep source and
profile scope visible. Review the result before sharing it. Never present the
fictional reference mode as model inference.

The first attempt remains in `.local-reports/browser-demo-final/`. Its three live
runs succeeded; the download test's locator incorrectly expected the filename
inside Gradio's link. The corrected locator targets the observed download control.
A display-only column-width correction improved the table. The frozen extraction
engine and all held-out results remained unchanged.

## Publication remaining

Review the finished DEV article and demo. Sign in to DEV, paste the article using
the official Week 2 template, preserve its headings and `devchallenge` and
`hf26challenge` tags, preview links, and publish one entry only when ready.
Deadline: October 18, 2026, 11:59 PM PDT (October 19, 2:59 AM EDT).
