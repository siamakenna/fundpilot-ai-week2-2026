---
title: "FundPilot AI: Read the Funding Rules Before Writing the Application"
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).*

## What I Built

“First author” is a small phrase with an expensive consequence. A researcher can have an accepted poster, a compelling project and a travel budget—and still spend an evening applying for an award whose conditions they do not meet.

**FundPilot AI helps researchers turn funding rules into an application-preparation plan.** Paste public announcement text, answer ordinary Yes/No/Unknown questions, and run local Gemma. Python attaches the original passages and compares supported conditions with the facts you supplied. A compact overview separates **requirements matching your facts**, **potential problems**, and **missing information or unclear conditions**. Open the **Application Readiness Dossier** for an actionable plan, with the full evidence report available separately.

I built it for independent researchers and small mentoring programs without a grants office. The commercial hypothesis is **$9 per readiness report or $39/month for a workspace**. Neither price is validated. There are no customers, revenue or testimonials to claim. The product needs to earn trust—and demonstrate that it saves time—before charging makes sense.

An UNKNOWN label alone leaves the researcher with another task. The dossier helps decide what that task should be:

- **Potential blockers:** distinguish a supported contradiction from a possible exclusion or exception that needs review.
- **Missing facts:** point back to the relevant form question and a record to check. An unknown presenter is different from unclear sponsor wording.
- **Materials and dates:** surface source-stated document cues and explicit dates, with uncertain roles labeled for review.
- **Sponsor questions:** group repeated questions while preserving every passage reference.
- **A final checklist:** separate work you can do yourself from questions the organizer must answer.

The source-review layer can notice “have not received” in a prior-funding restriction even when the interpreter does not give it a useful category. It keeps the whole passage and flags a **potential issue**, without turning that cue into an eligibility decision or changing the model's scores.

The form suggests questions using simple text cues and always offers **Show all questions**. Hiding a question preserves its answer; it never fills in No. The link field explicitly says the website is not read automatically: users paste the actual requirements. Detailed evidence is expandable, so the first result is a short overview rather than a wall of repeated passages.

The main workflow accepts previously unseen public text; it is not limited to authored scenarios. An optional CNS quick-start loads a verified excerpt with clearly fictional, editable facts. It produces no analysis until you click Analyze. The complete announcement and linked policies still need review.

## Demo

![An actual live Gemma result with a source-backed contradiction and application dossier](https://raw.githubusercontent.com/siamakenna/fundpilot-ai-week2-2026/main/evidence/usability/contradiction-overview.png)

**[Watch/download the authentic 96-second v0.3.2 walkthrough (WebM)](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.3.2/fundpilot-dossier-demo.webm)** · [Release](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/tag/v0.3.2)

Watch for supported comparisons at **0:11**, the contradiction overview at **0:27**, the missing-fact result at **0:44**, historical restrictions at **1:22**, and the final downloads and cleared outputs at **1:34**.

This silent, continuous Chromium recording shows the local application and real Gemma 1B inference. It is not a hosted interactive service. The first three analyses use a short CNS passage: two supported comparisons, a first-author contradiction, then a missing presenter fact. The fourth uses historical German Neuroscience Society excerpts to show prior-funding warnings and a passed deadline. All applicant facts are fictional; these selected passages are not whole-call assessments.

Inspect the actual downloads: [contradiction dossier](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/usability/contradiction-dossier.md), [missing-fact dossier](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/usability/unknown-dossier.md), [historical-source dossier](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/usability/historical-exclusion-dossier.md), and [full evidence report](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/usability/historical-exclusion-report.md). The [event log](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/usability/events.json) records actual timings and downloaded-file hashes. Editing an input clears both downloads.

The authentic [v0.3.1 fallback demonstration](https://github.com/siamakenna/fundpilot-ai-week2-2026/releases/download/v0.3.1/fundpilot-onboarding-demo.webm) remains unchanged. The [official-source ledger](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/OFFICIAL_SOURCES.md) distinguishes current and historical evaluation sources.

## Code

[FundPilot AI on GitHub](https://github.com/siamakenna/fundpilot-ai-week2-2026) includes the Python/Gradio application, tests, original fixtures, evaluation protocols and preserved failures. Application code is MIT licensed; Gemma weights retain Google's separate terms. No private grant documents, institutional research code or model weights are included. There are no accounts, payments or cloud inference services.

## How I Built It

**My first real model runs failed.** Tests against authored examples passed, but real announcements produced omitted passages and repeated criteria. Instead of silently repairing those responses, I narrowed the task and kept the failure evidence.

The stable path uses **Gemma 3 1B, Q4_K_M, through Ollama 0.40.4** on a CPU laptop. Python assigns each pasted paragraph or list item an ID and character span. Gemma proposes a category and applicable criteria using a small fixed schema. Python attaches the original text: **the model never writes the evidence quote**.

Lexical rules constrain candidate criteria and provide a measured baseline. A supported comparison requires agreement between model and rules, followed by a deterministic check against declared facts. Only public announcement text goes to local Ollama; applicant facts stay in Python. This guardrail is useful but imperfect: agreement can still miss semantic dependencies.

The dossier reuses those findings and the existing verification queue. It adds deterministic source cues for exclusions, AND/OR pathways, periods, materials and financial terms. It does not change the interpreter or promote warnings to MATCH or NOT MATCH. Exact source links make those prompts inspectable. Downloads remain local plaintext files; they are not encrypted storage. The form locks during inference, edits clear both outputs, and missing models produce an error without a fallback answer.

Measured interpretation remains limited:

| Original provisional reference | Live Gemma precision / recall / F1 | Rule-baseline F1 | Reports completed |
| --- | --- | --- | --- |
| Development: 40 paragraphs, 48 labels | 42.55% / 41.67% / 42.11% (20 matches, 47 predictions) | 62.50% | 5/5 |
| Held-out: 24 paragraphs, 32 labels | 38.46% / 31.25% / 34.48% (10 matches, 26 predictions) | 33.90% | 3/3 |

Mandatory-category recall was 15/34 in development and 5/15 held-out. Mean workflow times were 50.212 and 38.460 seconds. The held-out reports produced 24 UNKNOWN and three INFO findings, with no supported matches or mismatches for that profile. The tiny held-out F1 difference does not establish superiority to rules. The earlier 95.24% synthetic prototype result is not real-world accuracy. [Full evaluation and limitations](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/REAL_WORLD_EVALUATION.md).

I also tested the already-installed **4B model with the unchanged interpreter**. On three previously observed development sources, ten passages and twenty provisional atomic reference units, F1 rose from 18.18% to 23.53%, but supported MATCH disagreements with the provisional reference increased from 2 to 3. Mean case time was 40.94 seconds versus the saved 1B run's 15.44 seconds. **I kept 1B.** Different sessions and unreviewed labels do not justify a bigger default model. [Comparison, exact denominators and raw responses](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/MODEL_SIZE_COMPARISON.md).

The earlier [atomic v0.4 experiment](https://github.com/siamakenna/fundpilot-ai-week2-2026/pull/4) failed its release gates and remains unmerged. Historical scores, original annotations and failures are preserved. A supplied AI reconciliation is a separate proposal, not human validation; conflicting ISMB postdoc wording remains unresolved. A new blind annotation packet is ready for an independent reviewer, but none has completed it.

The product has **147 passing automated tests**, including the 137-test dossier checkpoint. These are regression checks, not proof of model accuracy. Actual Chromium checks cover keyboard evidence navigation, a narrow-screen dossier, invalid inputs, a genuinely missing model, downloads and stale-result clearing. The walkthrough runs four real analyses. Keyword suggestions, hidden-value preservation and URL-only rejection also have regression coverage. [Release checks and evidence](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/DOSSIER_RELEASE_QA.md).

## Why Does Open Innovation Matter?

Local open-weight inference let me inspect failed responses, narrow the task and compare installed models without a hosted inference account. Gemma genuinely participates in every live interpretation; the NO AI baseline remains a separate, explicit choice. The open approach gives me control over the runtime and access to failures worth investigating.

That is the demonstrated benefit—not proven superiority to closed models. Initial installation and model downloads require internet. Local inference still costs hardware time and electricity. The current workflow has no metered model API dependency, but I have not established commercial unit economics.

The next milestone is structured, consent-based usability tasks with fictional facts and a fair timed comparison against manual review, alongside independent human review of the reference labels. Qualitative observations do not establish measured time savings. Does it help them resolve an uncertainty or avoid a wasted application? I want that answer before adding another model or claiming a business.

## Prize Categories

- **Best Use of Gemma** — real local Gemma interpretation is integral to the workflow, measured and accompanied by its limitations.

#devchallenge #hf26challenge
