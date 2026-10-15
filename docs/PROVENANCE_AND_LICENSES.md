# Provenance and release review

The supplied starter was imported into a new, separate local Git repository in commit
`381205d`. The user states it was independently authored during October 12–18, 2026,
and confirmed in this session that the work is their own. This is an ownership
attestation, not an independent historical or legal audit. Commit timestamps record
actual work; no history was backdated. AI assistance was used for development,
testing and writing during this continuation.

The release scope is only `fundpilot_side_hustle_starter`. All original source,
fixtures, examples and documents were inspected. The three fixture JSON files
remain byte-for-byte unchanged from the import commit. They contain explicitly
fictional people, calls and expected assessments. No research repository, NIH code,
private grant, unpublished figure, real applicant document or institutional dataset
was incorporated. References to NIH in the documentation are exclusions, not data.

The application source and synthetic fixtures are released under the root MIT
license, copyright 2026 Makenna Rodriguez. The owner confirmed that the work is
original; MIT was explained in the conversation before continuing the release.

## Dependencies retain their own licenses

- Gradio 6.30.0: Apache-2.0.
- Pydantic 2.14.1: MIT.
- Pytest 9.1.1 and Ruff 0.17.0: MIT (development tools).
- Ollama: MIT; installed from the official `ollama/ollama` release, not vendored.
- Gemma 3 weights: Google's Gemma Terms of Use, **not** this project's MIT license.
  Download separately through Ollama; no model weights are included in Git.

Installed direct dependency metadata is recorded in
`evidence/dependency-licenses.json`; tested Python versions are in
`requirements-tested.txt`. Transitive dependencies are installed by pip and are not
copied into the repository. Their licenses continue to apply.

Official references: [Ollama license](https://github.com/ollama/ollama/blob/main/LICENSE),
[Gemma terms](https://ai.google.dev/gemma/terms),
[Gemma 3 model package](https://ollama.com/library/gemma3:1b).

The public release excludes virtual environments, installed model/runtime binaries,
credentials, temporary files and system logs. Baseline evidence contains synthetic requests and responses, tests and screenshots.
The upgrade adds generated label responses from public official announcements,
source hashes and short attributed excerpts. Full organizer pages and supplied
review archives remain local and ignored; third-party text is not relicensed as MIT. These checks
support a scoped release; they cannot independently establish all ownership facts.
