# Evidence index

Everything here is from synthetic inputs. Model responses are actual local
responses unless a test explicitly says mock. No model/runtime binaries are
included. The source fixture JSON is unchanged; see `fixture-integrity.json`.

- `evaluation-release/`: the reported six-case, 21-clause release evaluation;
  actual request/response records, cases, reports and summary.
- `cli-release/`: the three required real CLI scenarios; Markdown, audit JSON and
  `/usr/bin/time -p` output. Includes an unexplained shell wall-time outlier.
- `adversarial-live/`: four live model probes plus one actual missing-model HTTP
  failure. Application-safe outcomes do not imply correct model classifications.
- `model-tags.json`, `ollama-version.txt`, `ollama-running-model.json`: runtime and
  model identity. Full digest appears in the evaluation document.
- `starter-tests.txt`: 19 passing tests on the original starter.
- `starter-import*.txt`: the failed early import during installation and the
  successful import after installation.
- `final-tests.txt`, `lint.txt`: final 50-test result and lint check.
- `UI_CHECKS.md`, UI PNGs and text snapshots: authentic browser evidence, clearly
  distinguishing reference fixtures from live inference. No video is claimed.
- `starter-live/`: connection failures before the service restarted.
- `starter-live-retry/`: actual initial-prompt CLI results; all required verification.
- `prompt-v2`, `prompt-v3`, `prompt-v4`, `prompt-v6`, `prompt-v7`: saved development
  probes, including rejected quotes and invalid amount mappings.
- `evaluation-v5`, `evaluation-final`, `evaluation-v9`, `evaluation-v10`: earlier
  development candidates. The misleadingly named `evaluation-final` is NOT the
  release result. Keeping it preserves the measured failure history.
- `classifier-probe.json`, `category-probe.json`: real exploratory model outputs,
  not release benchmark cases.

Refer to `../docs/EVALUATION.md` for definitions, denominators, limitations and
latency caveats. These fixtures informed prompt development and are not a held-out
accuracy study. Exact quote attachment is deterministic code, not a model score.

- `release-qa/`: October 14 submission-readiness audit, lightweight smoke checks
  and link verification. No new model benchmark; original evidence is unchanged.

## Public-call upgrade (separate from the synthetic benchmark)

- `realworld-development/evaluation-v1` through `evaluation-v4`: actual strategy history, including rejected reports.
- `realworld-heldout`: the frozen candidate's single three-source pass; no retries.
- `public-safety-live`: five actual adversarial/missing-model probes.
- `annotation-review`: local-cache verification of the separately proposed AI labels.
- `public-ui`: real browser screenshots, actual downloaded report, events and video digest.
- `upgrade-tests.txt` and `upgrade-security-check.json`: final scoped release checks.

See [real-source evaluation](../docs/REAL_WORLD_EVALUATION.md) for denominators,
failures and limits. Source quotes are attached by Python; generated labels remain
model output. Full organizer pages are not redistributed. The original evidence
files above remain byte-for-byte unchanged.
