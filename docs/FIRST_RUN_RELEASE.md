# First-run onboarding release — v0.3.1

This release keeps the v0.3 inference engine and all original benchmarks unchanged.
The separate v0.4 atomic experiment **did not pass its release gates** and remains
in [experimental PR #4](https://github.com/siamakenna/fundpilot-ai-week2-2026/pull/4).
See its [full results and denominators](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/feature/interpretation-v04/docs/v04/RESULTS.md).

## Shipped scope

A compact optional introduction explains the three steps and links to the existing
CNS sample action. A collapsed tutorial defines MATCH, NOT MATCH, UNKNOWN and INFO,
source completeness, plaintext-report privacy and explicit NO AI operation.

**Check local model** queries only loopback Ollama `/api/tags`, only when clicked.
It verifies the configured tag, with a 2.5-second timeout and bounded response size.
It does not generate text, install software, download weights or prove successful
inference. Errors distinguish unavailable service, missing model, timeout and invalid
response. Redirects and proxies are disabled; no new external integration was added.

The sample notice follows source edits, and the empty queue no longer says
“Showing 0 of 0.” The unchanged engine still decides which comparisons are supported.

## Checks

- Full stable suite: **115 passed**, including all original 93 tests unchanged.
- Focused onboarding: 22 passed; focused onboarding + verification: 36 passed.
- Ruff `--select F .`: pass. Full configured lint on new onboarding module/tests: pass.
- Actual Chromium: 390px viewport without horizontal overflow; keyboard tutorial,
  model check and sample load; no fabricated sample report; notice clears on edits.
- Genuine Gemma recording: three fictional profile configurations on the same
  attributed short CNS excerpt; downloaded report bytes and exact source checked.
- Real service-off browser check: explicit NO AI still works; selected live mode
  fails visibly and clears the previous download. No model-response mocks in browser checks.
- Protected old engine, fixtures, references, metrics, tests and failure evidence
  are byte-identical. v0.2.0 and v0.3.0 release videos are retained.
- Scoped review: local transport, HTML/Markdown escaping, input invalidation,
  plaintext reports, new-file credential patterns/private formats and file sizes.
  Not a full penetration test, dependency audit or WCAG conformance claim.

Ollama 0.40.4; Gemma 3 1B Q4_K_M, digest
`97558784bdc9175075a72655bf360b15da17df6b3b9e5182af9f8c0c8e58ba7c`.
The app is MIT; Gemma weights keep their separate Google terms. Only public source
text and fictional applicant data were captured. No model weights, private research
code, unpublished grant documents or credentials were added.

Evidence: [`evidence/onboarding/`](../evidence/onboarding/). The browser recording
is silent, continuous and unedited, with actual inference and downloads. It is a
local-app demonstration, not a hosted public application or whole-call evaluation.

## Experimental decision and remaining limitations

The new common-unit diagnostic used 3 development sources/10 passages/20 provisional
atoms, then 2 reserved sources/8 passages/20 atoms. Candidate and protocol froze
before reserved retrieval; references froze before predictions. No final tuning.

| New diagnostic | v0.3 Gemma F1 | Atomic v0.4 F1 | Rules F1 | Atomic reports complete |
|---|---:|---:|---:|---:|
| Development | 18.18% | 5.41% | 48.48% | 1/3 |
| Reserved final | 6.90% | 0% | 0% | 0/2 |

This expanded atomic vocabulary is a different measurement from the historical
42.11%/34.48% Gemma F1 figures, which remain intact. All annotations are provisional,
not independently human-validated. Original v0.3 also produced two supported MATCH
statuses that disagreed with provisional reference expectations in the new development
sample. These are diagnostic disagreements for one fictional profile, not confirmed
real eligibility errors; they reinforce the requirement to verify every comparison.
No superiority claim follows from these small, difficult samples.

v0.4 met only 4/14 supplied live regression behavior checks (13/14 reports completed;
11 distinct source texts). Its deterministic tests pass **given supplied proposals**;
that is not improved model accuracy. The separate experimental suite has 137 tests.
No larger model was downloaded. Raw failures and frozen artifacts are preserved on
its branch and locally. A blind development annotation packet is prepared, with no
reviewer participation claimed. ISMB postdoc scope remains unresolved.

**Ship onboarding; do not ship v0.4 inference.** Human annotation and broader model
work remain future tasks, not blockers to preparing the conservative v0.3 entry.

## Reproduce

```bash
.venv/bin/python -m pytest -q
.venv/bin/ruff check --select F .
.venv/bin/ruff check fundpilot/onboarding.py tests/test_onboarding.py
GRADIO_ANALYTICS_ENABLED=False python app.py
# With Playwright installed and NODE_PATH set if needed:
node scripts/check_onboarding_browser.cjs
node scripts/record_onboarding_demo.cjs .local-reports/onboarding-demo http://127.0.0.1:7863
# Stop local Ollama deliberately before this failure-only check, then restart it:
node scripts/check_onboarding_failures.cjs
```

Browser scripts default to port 7863. Start the app on that port for reproduction:
`python -c 'from app import demo; demo.launch(server_name="127.0.0.1", server_port=7863, share=False)'`.
No hosted CI is configured; these are recorded local checks. Review is by the coding
agent, not independent human approval. No DEV article or challenge entry was published.

## Public release verification

[v0.3.1](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/tag/v0.3.1)
is published with the original 5,489,046-byte recording. Anonymous download returned
HTTP 200 and SHA-256 `a6215bea3ab527c6d06510d09a79de4785c6113ae8f754cff6b81536864510cf`,
matching both the local artifact and GitHub asset metadata. All 17 pre-merge repository,
release and evidence links resolved against the release commit; transient HEAD 503
responses were rechecked successfully with GET. The original two video digests match.

[Onboarding-only PR #5](https://github.com/siamakenna/fundpilot-ai-week2-2026/pull/5)
contains the release. [Verification evidence](../evidence/onboarding/public-release-verification.json)
records the final checks. Atomic PR #4 remains draft and unmerged. No DEV publication
or challenge submission was performed.
