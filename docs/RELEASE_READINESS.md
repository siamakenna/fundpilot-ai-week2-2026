> Historical baseline planning/QA record. The completed public-call upgrade is documented in [upgrade release checks](UPGRADE_RELEASE_CHECKS.md), [real-source evaluation](REAL_WORLD_EVALUATION.md), and [the current demo guide](JUDGE_DEMO_SCRIPT.md). Earlier pending steps below are superseded by those records.

# Final submission readiness — October 14, 2026

**Release QA passes. Competition publication is blocked by the missing public
video and awaits the owner's final decision.** No deployed app is claimed.

## Release audit

- Started from clean `main` at `a4343355703e90b7cd0973922158634952ac2ab9`.
  `git fetch origin` and `git rev-list --left-right --count HEAD...origin/main`
  returned `0 0`; no fast-forward or merge was needed.
- `.venv/bin/python -m pytest -q`: **50 passed in 6.85s**.
- `.venv/bin/python -c 'import app; print("app import OK")'`: passed.
  Three fixture callback/report smoke checks passed; explicitly **NO AI**.
  Existing Gradio HTTP endpoint returned 200; Ollama returned version 0.40.4.
- The existing release lint command, `ruff check app.py fundpilot scripts tests --select F`, passes. An optional broader `ruff check .` reports 16 pre-existing import-order, exception-style and datetime-style diagnostics; recorded in `evidence/release-qa/optional-lint.txt`. They do not identify a submission blocker, and no source cleanup was made.
- Reviewed the retained six-case evaluation, live CLI responses, adversarial
  failures, UI captures and downloaded report. **No live benchmark was rerun.**
- Heuristic scan of all **144 historical Git blobs** found no credential-pattern
  matches. Inventory of 137 tracked files found no model-weight/private-document
  extensions or committed runtime/environment directories. Source scope and
  synthetic fixtures agree with the existing provenance review. This is a scoped
  check, not an independent ownership determination or a guarantee against secrets.
- All three fixture files match both their recorded SHA-256 and initial import.
  Application code, fixtures, model outputs and raw failure evidence are unchanged
  by this QA release. MIT attribution and separate Gemma terms are preserved.

Machine-readable results: [audit](../evidence/release-qa/audit.json),
[smoke checks](../evidence/release-qa/smoke.json),
[link checks](../evidence/release-qa/links.json). All 13 public links returned HTTP 200
and all 19 relative links resolved. One GitHub 503 succeeded on retry; the initial
Python trust-store issue was resolved by using system curl with TLS verification.

## Rules and template verification

Checked the [official challenge](https://dev.to/challenges/hacktoberfest-week2-2026-10-12),
its linked Submission Template, and [Week 2 rules](https://dev.to/page/hacktoberfest-week2-2026-10-12-contest-rules).
The entry window is October 12 at noon through **October 18, 2026, 11:59 PM PDT**;
the deadline is October 19 at 2:59 AM EDT. One entry is allowed. The rules require
a new project, core open AI, a plausible paying audience, code, a video or deployed
demo, and a published DEV article. Writing is the highest-weighted criterion.
English is required for prize consideration. Personal eligibility and acceptance
of publication/contest terms remain the entrant's responsibility.

The draft preserves the template's What I Built, Demo, Code, How I Built It,
Why Does Open Innovation Matter?, and Prize Categories headings. Optional agent
session and first-user sections are omitted because there is no material to claim.
Both `devchallenge` and `hf26challenge` tags are present. Best Use of Gemma is the
only partner category claimed, supported by actual local inference.

## PASS / BLOCKED checklist

| Check | Status | Evidence / remaining condition |
| --- | --- | --- |
| Public MIT repository and real history | PASS | [Repository](https://github.com/siamakenna/fundpilot-ai-week2-2026); owner attests independent Week 2 authorship |
| Tests and lightweight application smoke | PASS | 50 tests; import; three fixture reports; running HTTP endpoints |
| Gemma integral and claims supported | PASS | 20/21 clause matches on six tuned synthetic calls; 5/6 validated; failures disclosed; no fresh accuracy claim |
| Original fixtures and failure records preserved | PASS | Fixture hashes and Git diff; no application changes |
| Scope, credentials and model-weight review | PASS | Scoped historical scan and provenance; separate Gemma terms |
| English narrative, template headings and tags | PASS | Customer, unvalidated prices, engineering lesson, limitations and evidence linked |
| Accessible demo video or deployed app | **BLOCKED** | Neither exists; explicit video placeholder retained |
| Authenticated DEV draft | **BLOCKED** | Browser opened at sign-in; article saved locally instead |
| Final publication and entry | **BLOCKED** | Owner review/decision; no article was published or challenge entry submitted |

## Recording capability and remaining owner actions

macOS `screencapture` supports recording, but the read-only
`CGPreflightScreenCaptureAccess()` check returned **false**. No permission was
changed. Browser automation offers screenshots but no recorder; native controls
are disabled. No available local recording path was ready to run autonomously.
There is no recording to upload. A remote metered recorder was not used for this
loopback-only application.

1. [Record, review and upload the three live scenarios and report](LOCAL_CAPTURE_STEPS.md).
   Replace the video placeholder in README and the DEV article with the verified
   viewing URL; remove the blocker note, update this checklist and push the docs.
2. Sign in to DEV, paste the article into the official template, preview the
   video/links and tags, and publish one entry only after your final review and
   rules acceptance, before the deadline.

No retesting of model accuracy, new hosting, payment setup or customer testimonial
is needed to finish these steps. This is one submission, not a new implementation.

## Commands and checks performed

`git status --short`, `git remote -v`, `git fetch origin`,
`git rev-list --left-right --count HEAD...origin/main`, `git log -1`,
`.venv/bin/python -m pytest -q`, the `app` import command, local HTTP health checks,
three `app.run` fixture callbacks with downloaded-file assertions, tracked-file
and historical-blob scans, fixture SHA-256 comparisons, Markdown link checks,
`git diff --check`, and direct official-page/template review. The screen-capture
permission check used Python ctypes with the macOS CoreGraphics framework; an
initial Swift probe was stopped before returning a result. No permission prompt
was accepted, model inference restarted, or paid dependency added.
