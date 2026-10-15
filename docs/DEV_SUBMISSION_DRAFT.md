---
title: "FundPilot AI: Read the Funding Rules Before Writing the Application"
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).*

## What I Built

“First author” is a small phrase with an expensive consequence. A researcher can have an accepted poster, a compelling project and a travel budget—and still miss a funding requirement before spending an evening on the application.

**FundPilot AI helps researchers check those requirements before they start writing.** Paste a public announcement, answer ordinary Yes/No/Unknown questions, and download a report connecting each supported comparison to its exact source passage. A missing fact becomes a question. A contradiction becomes something to resolve. Neither becomes an official eligibility decision.

I built it for independent researchers and small mentoring programs without a grants office. The business hypothesis is **$9 per readiness report or $39/month for a workspace**. Neither price is validated. There are no customers, revenue or first-user testimonials to claim. Before charging, I need to establish whether the report saves people time without creating misplaced confidence.

The original prototype depended heavily on fictional examples. The main workflow now accepts previously unseen public text and ordinary applicant facts. Fictional fixtures remain in a clearly labeled secondary tab. They never substitute for live model output.

## Demo

**Video URL: [INSERT VERIFIED PUBLIC VIDEO URL WHEN AVAILABLE]**

The walkthrough uses a short, attributed passage from the real CNS 2027 Travel Awards announcement and three fictional applicant configurations. Each analysis invokes local Gemma. It shows supported matches, a first-authorship contradiction, an unknown presenter fact, and an actual report download. This is a focused workflow demonstration, **not complete CNS eligibility analysis**.

The broader [official-source evaluation](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/REAL_WORLD_EVALUATION.md) exercises selected passages from eight announcements, including current and historical opportunities. The [source ledger](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/OFFICIAL_SOURCES.md) distinguishes them and records retrieval limitations.

## Code

[FundPilot AI on GitHub](https://github.com/siamakenna/fundpilot-ai-week2-2026) includes the Python/Gradio app, tests, original fixtures, evaluation protocol and raw model failures. Application code is MIT licensed; Gemma weights retain Google's separate terms and are downloaded through Ollama. No private grant documents, institutional research code or model weights are included.

## How I Built It

**My first real model runs failed.** Passing tests against authored examples did not mean Gemma could interpret funding announcements. Real-source runs omitted passages or repeated criteria. Strict validation rejected those reports. I kept the failures because they explain the engineering decisions better than a successful screenshot alone.

The final path uses **Gemma 3 1B, Q4_K_M, through Ollama 0.40.4** on a CPU laptop. Python gives every pasted paragraph or list item an identity and character span. Gemma proposes a category and applicable criteria using one request per passage and fixed Boolean fields. Python attaches the original text; **the model never writes the evidence quote**.

Lexical rules constrain candidate criteria and provide a measured baseline. A supported comparison is allowed only when the model and rules agree. Python then compares the condition with declared applicant facts. Applicant facts stay in Python; only public announcement text goes to Ollama. Exceptions, uncertain scope and unsupported conditions remain review items. Amount handling separates explicit request ceilings from sponsor benefits; dates retain their apparent purpose without inventing missing years or opening status.

The useful product changes are concrete: no mandatory JSON editing, a live-model default, visible contradictions, source evidence beside findings, and a downloadable review checklist. Inputs lock during analysis; changing them clears the previous report. Missing models and invalid responses produce an error instead of a fabricated answer.

I tested alternative schemas on five development sources, froze the candidate, and reserved three additional sources for one held-out pass. An inaccessible reserved page was replaced before inference, with the substitution recorded. Eight paragraphs per source were selected; these are not whole-document completeness tests.

The measured results were humbling:

| Original provisional reference | Live Gemma precision / recall / F1 | Rule-baseline F1 | Reports completed |
| --- | --- | --- | --- |
| Development: 40 paragraphs, 48 labels | 42.55% / 41.67% / 42.11% (20 matches, 47 predictions) | 62.50% | 5/5 |
| Held-out: 24 paragraphs, 32 labels | 38.46% / 31.25% / 34.48% (10 matches, 26 predictions) | 33.90% | 3/3 |

Selected mandatory-category recall was 15/34 in development and 5/15 held-out.
Mean workflow time was 50.212 seconds for development and 38.460 seconds held-out.
The held-out reports contained 24 UNKNOWN and three informational findings, with
**no supported applicant matches or mismatches** for the evaluation profile. They
all needed manual review. That is a real limitation, not a successful eligibility
verdict. A tiny held-out F1 difference from rules does not establish superiority.
The separate 95.24% synthetic prototype score is not real-world accuracy.

The original development labels are provisional. A separately supplied AI reconciliation package proposed changes to 14 of 40 development records; all 40 passage hashes and five source snapshots matched the local cache. I preserved that proposal separately, without retuning or replacing historical scores. **AI reviewers are not independent human adjudicators.** Conflicting ISMB postdoc wording remains unresolved pending sponsor clarification.

The suite has **79 passing tests**, including adapter mocks for malformed JSON, omitted IDs, timeout budgets and unsupported conditions. Five additional live safety probes kept injection, a membership exception and a negative cap unresolved, treated a stipend as information, and rejected a missing model. These checks demonstrate specific safeguards, not universal prompt-injection resistance or flawless interpretation.

## Why Does Open Innovation Matter?

Running an open-weight model locally let me inspect failed responses, narrow the task and change the schema without a hosted inference account. The ordinary workflow has no metered model API dependency. Installation and model download require internet; local inference still costs hardware time and electricity.

Gemma is integral to the live path: its interpretation participates in every supported comparison, and its disagreements stay visible. The explicit NO AI baseline is a separate user choice. **The measurements do not show Gemma outperforming the rules**, and no closed-model comparison was run. Local control and inspectability are the benefits demonstrated here, not superior accuracy.

The next milestone is an independently human-reviewed reference set and a consenting researcher using the product with fictional facts. The question is practical: does this evidence-backed checklist help someone decide where to spend their application time?

## Prize Categories

- **Best Use of Gemma** — real local Gemma interpretation is implemented, measured and integral to the live workflow. Its failures and limitations remain visible.

#devchallenge #hf26challenge
