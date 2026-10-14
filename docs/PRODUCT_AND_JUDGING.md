# FundPilot AI — judge-focused product curation (October 13, 2026)

## Product statement

A private, researcher-focused second opinion for confusing conference travel-award eligibility. Paste the announcement and your profile; receive source-linked MATCH / NOT MATCH / UNKNOWN findings and a downloadable application-readiness report.

## Who has the problem

- Independent and first-generation researchers without grant-development office support
- Mentors reviewing conference funding and early-career professional development awards
- Research administrators doing high-volume early triage (higher future willingness-to-pay hypothesis)

## Commercial hypothesis (NOT measured)

- Personal report: $9 one-time
- Department/team advisor workspace: $39/month
- Potential actual first customer: mentoring program or independent researcher, not NIH on institutional resources
- Do not claim revenue, paying users or proven pricing unless demonstrated

## Judge narrative

1. **One narrow, expensive mistake:** spending hours on awards you're not eligible for.
2. **Why general LLM chat isn't enough:** unsupported reassurance and missed clauses are costly; funding decisions need quotes, no guessing.
3. **Open model is integral:** Gemma locally extracts precise eligibility clauses from pasted documents; an inspectable rule layer checks supplied facts; no hosted closed-API call is needed.
4. **Proof instead of hype:** show three contrasting fictional scenarios, real Gemma request/response, hard-fail behavior when source evidence mismatches, and measured latency/accuracy vs a keyword baseline.
5. **Business:** test a small paid readiness report and demonstrate customer interest ethically; this is a hypothesis, not revenue.

## Scope LOCK (no detours)

| Build | Why | Exclude |
| --- | --- | --- |
| 3-step workflow | short video & fast usability | live grant search |
| local Gemma parser | partner qualification | paid inference hosting |
| deterministic rule grader | honest uncertainty | opaque LLM verdict |
| exact evidence snippets | clear trust story | unsupported citations |
| Markdown report | product artifact | accounts, payment processing |
| fictional cases | free and IP-safe demo | real lab data / real CVs |

## Distinctive product improvements after MVP

1. Show a **Needs Verification** card in the UI summarizing questions for the grant administrator.
2. Show a **why it failed** highlight tied to one exact sentence in a fictional funding call.
3. Include a 30-second comparison showing the regex baseline missing an ambiguous clause while Gemma successfully extracts it, only if actually measured.

## Rules and external references

- https://dev.to/challenges/hacktoberfest-week2-2026-10-12
- https://ollama.com/library/gemma3
- https://github.com/ollama/ollama/blob/main/docs/api.md

## Real first-user feedback protocol

Find a **consenting non-NIH independent researcher**. Give only fictional opportunities. Ask them to narrate the eligibility process, and request permission before quoting.

Suggested questions:
- What part of a funding call takes you longest to interpret?
- Did this report make an application decision easier, or did it create new questions?
- Would you pay $9 for a one-time verified-readiness report? Why or why not?

Log real feedback, interview date and consent. Don't fabricate a customer or encourage a fake transaction.

## Must-do before DEV publication

- [ ] Run and verify real Gemma extraction and model version; include only measured numbers
- [ ] Benchmark at least 6 cases against authored ground truth, document errors/limits
- [ ] Run full tests and check known unknown paths
- [ ] Confirm source validation is stringent and missing extraction cannot produce false certainty
- [ ] Produce actual video or working deployed demo (video acceptable)
- [ ] Verify GitHub repo created during October 12–18 window and public code license rights
- [ ] Publish concise, evidence-backed DEV article with template headings and tags
- [ ] Share any real user quote only with explicit permission

## Save Work credits

Use ChatGPT for drafting, demo copy, and fixture authoring; Codex for local Ollama installation, model benchmarks, issues and committing; Work only when real browser interaction or automated hosted deployment is actually needed.

## Verified continuation status — October 14, 2026

The owner attests this is independent Week 2 work. Original fixture JSON is
unchanged. The release adapter uses actual Gemma sentence classification and
Python's exact-source attachment; it does not generate evidence quotes. See
`EVALUATION.md` for the measured 20/21 clause matches, 5/6 valid reports, one rejected
case, live adversarial mistakes, and the separate wall-time outlier. The initial
19 tests and final 50 tests are distinct from live inference measurements.

The three-step local UI and Markdown reports were exercised. MIT licensing and
scoped source review are documented in `PROVENANCE_AND_LICENSES.md`. The DEV draft
preserves the official headings and tags and claims only Gemma. No baseline
superiority, customer, revenue, hosting integration or testimonial is claimed.

Still manual: record and review the authentic walkthrough using
`LOCAL_CAPTURE_STEPS.md`, upload it to obtain a real demo URL, and review/publish
one DEV entry. Publication is deliberately not performed by this continuation.
