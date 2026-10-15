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

**The report should not end at UNKNOWN.** The new verification queue puts contradictions first, groups repeated findings from the same passage, and pairs each item with a next action, a suggested sponsor question, its reason and the exact evidence. Unknown presenter status? Check your records and update the form first. A first-author contradiction? Confirm your declared fact, then ask whether the published condition prevents applying and whether any published exception applies. The tool supplies questions, never invented sponsor answers.

An optional CNS quick-start loads one verified public excerpt and clearly fictional, editable facts. It selects live Gemma, but produces no report until you click Analyze. You can replace the excerpt with another public call. This is early triage and preparation; the complete announcement and linked policies still need review.

The optional first-run guide explains the three steps and result labels without blocking the form. **Check local model** reports whether Ollama can find Gemma; it does not install anything or claim that inference succeeded. The collapsed tutorial explains the full-source review requirement and local plaintext-report privacy.

## Demo

![An actual first-author contradiction, exact source evidence and a prioritized verification question](https://raw.githubusercontent.com/siamakenna/fundpilot-ai-week2-2026/main/evidence/onboarding/contradiction.png)

**[Watch/download the new 60-second demo (WebM)](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.3.1/fundpilot-onboarding-demo.webm)** · [v0.3.1 release](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/tag/v0.3.1)

This silent, unedited recording shows the working local app, **not a publicly hosted interactive service**. The public download needs no sign-in; open it in a WebM-capable browser/player.

**Watch for:** the manual local-model check and tutorial at the start; the editable CNS sample around 0:07; two supported comparisons around 0:25; a first-author contradiction and priority-one question around 0:35; an unknown presenter fact around 0:45; and the final downloaded report around 0:53. Editing an input clears the old report before the recording ends. [Inspect the contradiction report](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/onboarding/contradiction-report.md), [the UNKNOWN report](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/onboarding/unknown-report.md), or [the event log](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/onboarding/events.json).

Each of the three analyses invokes real local Gemma on one short, attributed CNS 2027 Travel Awards passage with fictional applicant facts. Each report is actually downloaded and checked. This demonstrates the workflow on a simple condition, **not complete CNS eligibility analysis or improved extraction accuracy**. The authentic [v0.2.0 recording](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.2.0/fundpilot-public-call-demo.webm) remains unchanged.

The broader [official-source evaluation](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/REAL_WORLD_EVALUATION.md) exercises selected passages from eight announcements, including current and historical opportunities. The [source ledger](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/OFFICIAL_SOURCES.md) distinguishes them and records retrieval limitations.

## Code

[FundPilot AI on GitHub](https://github.com/siamakenna/fundpilot-ai-week2-2026) includes the Python/Gradio app, tests, original fixtures, evaluation protocol and raw model failures. Application code is MIT licensed; Gemma weights retain Google's separate terms and are downloaded through Ollama. No private grant documents, institutional research code or model weights are included.

## How I Built It

**My first real model runs failed.** Passing tests against authored examples did not mean Gemma could interpret funding announcements. Real-source runs omitted passages or repeated criteria. Strict validation rejected those reports. I kept the failures because they explain the engineering decisions better than a successful screenshot alone.

The final path uses **Gemma 3 1B, Q4_K_M, through Ollama 0.40.4** on a CPU laptop. Python gives every pasted paragraph or list item an identity and character span. Gemma proposes a category and applicable criteria using one request per passage and fixed Boolean fields. Python attaches the original text; **the model never writes the evidence quote**.

Lexical rules constrain candidate criteria and provide a measured baseline. A supported comparison is allowed only when the model and rules agree. Python then compares the condition with declared applicant facts. Applicant facts stay in Python; only public announcement text goes to Ollama. Exceptions, uncertain scope and unsupported conditions remain review items. Amount handling separates explicit request ceilings from sponsor benefits; dates retain their apparent purpose without inventing missing years or opening status.

The verification queue is a small deterministic layer over those frozen findings. It does not change model prompts, predictions, statuses, counts or source hashes. The top three questions appear beside the outcome; the full numbered list and all underlying criteria remain in the downloadable Markdown report. Award information is excluded from risk items, and even an all-MATCH excerpt retains a source-review warning. Inputs lock during analysis; changing them clears the previous report. Missing models and invalid responses produce an error instead of a fabricated answer.

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
The separate 95.24% synthetic prototype score is not real-world accuracy. This interface upgrade leaves those evaluations frozen; it improves what a researcher can do with uncertainty, not the measured extraction performance.

The original development labels are provisional. A separately supplied AI reconciliation package proposed changes to 14 of 40 development records; all 40 passage hashes and five source snapshots matched the local cache. I preserved that proposal separately, without retuning or replacing historical scores. **AI reviewers are not independent human adjudicators.** Conflicting ISMB postdoc wording remains unresolved pending sponsor clarification.

The stable suite now has **115 passing tests**: all original 93 plus 22 onboarding checks. These include adapter mocks, not live accuracy measurements. The new checks cover missing facts, exclusions, repeated criteria, compound passages, award-versus-cap handling, escaping and live-path failure. Chromium verified the queue, downloads, keyboard quick-start and narrow-screen form. The earlier five live safety probes kept injection, a membership exception and a negative cap unresolved, treated a stipend as information, and rejected a missing model. These checks demonstrate specific safeguards, not universal prompt-injection resistance or flawless interpretation.

A later atomic-clause experiment also failed its release gate. On a new, expanded common scoring unit, its F1 was 5.41% in development and 0% on two reserved sources, with only 1/3 and 0/2 reports completed. The unchanged engine scored 18.18% and 6.90% on those same provisional labels; this is a separate diagnostic, not a replacement for the historical table. Even the unchanged engine produced two MATCH statuses that disagreed with the new provisional reference expectations. I kept [the experiment and failures](https://github.com/siamakenna/fundpilot-ai-week2-2026/pull/4) unmerged and shipped onboarding alone. Exact quotations are useful evidence, but they do not make uncertain interpretation reliable.

## Why Does Open Innovation Matter?

Running an open-weight model locally let me inspect failed responses, narrow the task and change the schema without a hosted inference account. The ordinary workflow has no metered model API dependency. Installation and model download require internet; local inference still costs hardware time and electricity.

Gemma is integral to the live path: its interpretation participates in every supported comparison, and its disagreements stay visible. The explicit NO AI baseline is a separate user choice. **The measurements do not show Gemma outperforming the rules**, and no closed-model comparison was run. Local control and inspectability are the benefits demonstrated here, not superior accuracy.

The next milestone is an independently human-reviewed reference set and a consenting researcher using the product with fictional facts. The question is practical: does this evidence-backed checklist help someone decide where to spend their application time?

## Prize Categories

- **Best Use of Gemma** — real local Gemma interpretation is implemented, measured and integral to the live workflow. Its failures and limitations remain visible.

#devchallenge #hf26challenge
