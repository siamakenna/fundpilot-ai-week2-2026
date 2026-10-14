# Public-call upgrade release checks

Baseline preserved: `5b5d568c0dceb234bbe5e34db8d6a1c558d110e4`.
Branch: `codex/real-world-readiness`. Source split was committed as `3795fea`;
first working public-flow checkpoint and actual failures as `c8f6585`.

## Required release gates

- Existing fixtures and original failure evidence unchanged byte-for-byte.
- Automated tests and the existing `ruff --select F` check pass.
- Ordinary form fields, live default, exact evidence, uncertainty, source review,
  failure clearing, input invalidation and real download work in Chromium.
- Missing/invalid model output cannot produce a complete report or fixture fallback.
- No real-call output asserts official eligibility; no unresolved criterion is
  silently converted into an approved application.
- Current source attribution and historical calls are clearly distinguished.
- Source bodies remain outside Git; no secrets, model weights or private documents
  are included. Short quotations preserve attribution and separate ownership.
- Development results, original failures and one held-out pass are reported with
  denominators and annotation limits. No synthetic-score generalization claim.
- Demo uses actual Gemma output and identifies its excerpt scope and fictional facts.

Model superiority is not assumed or a marketing claim. Passing these gates permits
a transparent prototype release, not a production eligibility service or a claim
that complex funding rules are reliably automated. An independently human-reviewed
reference set and real consenting users remain future validation work.

## Checks recorded during implementation

- All original source fixtures and baseline evidence compared against the baseline
  Git blobs: unchanged (the evidence index may gain links).
- Current tracked and new code/evaluation files scanned for common credential
  patterns: no matches. `.source-cache/` and `.local-reports/` are ignored.
- Headless Chromium 151.0.7922.34 launches and records WebM through Playwright's
  bundled recorder. This does not require macOS screen-capture permission.
- No new model weights, paid service, cloud host or external applicant-data API.
- Developer source retrieval uses verified TLS through system curl. A compressed
  response initially decoded incorrectly; retrieval was corrected with `--compressed`
  before annotations were created. It was never evaluated as announcement text.

Final test, UI, evaluation, video and repository results will be filled after the
candidate freeze and release verification. DEV publication remains the owner's
explicit decision and is not performed by this release.
