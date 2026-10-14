---
title: "FundPilot AI: Check the Fine Print Before You Write the Application"
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).*

## What I Built

An accepted conference poster can be good news followed by an expensive question: how will I get there? A travel award might help—until an enrollment requirement, regional restriction or funding cap makes the application a dead end.

**FundPilot AI checks the fine print before the writing starts.** Its three-step Gradio workflow compares supplied facts with a funding call and produces a downloadable report: MATCH, NOT MATCH or UNKNOWN, with the exact source sentence beside each finding. The intended benefit is less time spent applying where the rules do not fit, and a clearer list of questions for the sponsor.

I built this prototype for independent researchers and small mentoring programs without a grants office. A **$9 readiness report or $39/month workspace** is a commercial hypothesis. Neither price is validated; I have no customers, sales or first-user feedback to claim. All built-in calls and profiles are fictional.

## Demo

**Video URL: [INSERT VERIFIED PUBLIC VIDEO URL WHEN AVAILABLE]**

*Publication blocker: record and review the real local walkthrough, upload it, then replace this placeholder. There is no deployed app or public video yet.*

Existing evidence includes an [authentic live Gemma screenshot](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/live-ui-graduate.png) and its [downloaded report](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/live-ui-downloaded-report.md). The [capture procedure](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/LOCAL_CAPTURE_STEPS.md) shows three scenarios: Alex meets a travel call's supplied conditions, Alex fails a graduate-only call, and Casey needs presentation acceptance verified.

Select **Live local Gemma** for inference. The separate **Curated reference demo (NO AI)** mode uses authored fixtures; it is never evidence of model behavior.

## Code

[FundPilot AI on GitHub](https://github.com/siamakenna/fundpilot-ai-week2-2026) contains the MIT-licensed application, unchanged starter fixtures, tests and raw model responses—including failures. The [provenance review](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/PROVENANCE_AND_LICENSES.md) records the owner's Week 2 authorship attestation and separate dependency terms. Gemma weights are downloaded separately under Google's terms.

## How I Built It

**The first real model runs failed the useful part of the task.** The starter's 19 tests passed, but three live runs mapped every clause to “unsupported.” Later prompts produced invented quote text and inconsistent dollar caps. Those responses are [retained](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/evidence/README.md). Passing tests with reference data had not established that Gemma could interpret the calls.

The lesson was to narrow the model's job. The release runs **Gemma 3 1B, Q4_K_M, through Ollama 0.40.4**. Python splits the source into sentences. Gemma classifies each sentence's criterion, mandatory flag and amount under a strict schema. Python attaches the original sentence verbatim and compares the result with profile facts deterministically. **Exact quotes come from Python, not model generation.** Only call text goes to Gemma; the profile stays in Python.

Built-in calls have an authored checklist that detects omitted or mismatched clauses without replacing the model's answer. Custom calls always remain NEEDS VERIFICATION, with UNKNOWN findings: exact text is no guarantee of correct interpretation.

The [six-call development evaluation](https://github.com/siamakenna/fundpilot-ai-week2-2026/blob/main/docs/EVALUATION.md) returned 21 classifications against 21 reference clauses:

| Measure | Actual result |
| --- | --- |
| Exact reference clause matches | 20/21 returned and 20/21 expected: **95.24% precision and recall** |
| Validated reports | **5/6**; one rejected an inconsistent amount mapping |
| NEEDS VERIFICATION | **1/6 attempts**, or 1/5 valid reports |
| Observed workflow time | **13.715–48.203 seconds; mean 24.878 seconds, n=6**, including the rejection |

These are **tuned synthetic development cases, not held-out accuracy**. Some timing overlapped another run. A separate CLI run had an unexplained 1,878.9-second shell-time outlier versus about 80.5 seconds inside the adapter; reliable responsiveness remains unresolved.

The suite now passes **50 tests**, including explicit adapter mocks for malformed JSON and forced omissions. Separate live safety probes produced **5/5 conservative application outcomes**, but Gemma misread an astronaut requirement and “exceptional promise.” The application guard prevented eligibility claims; the model did not understand everything correctly. Sentence boundaries, exceptions and cross-sentence conditions remain limitations.

## Why Does Open Innovation Matter?

Local open-weight inference lets me inspect failures, change the prompt and schema, and reproduce the workflow without a hosted model API. Installation and model download require internet; subsequent inference uses local Ollama. Hardware and electricity still have costs.

Gemma is integral to the live path: it interprets each sentence before Python checks the facts. The fixtures cannot stand in for that work. I have not measured a keyword baseline or closed model, so I claim no superiority over either.

The next useful test is a held-out set of permitted public calls and a consenting tester using fictional profiles. Before charging for a report, I need evidence that it helps someone decide where to spend their application time.

## Prize Categories

- **Best Use of Gemma** — local Gemma classification is implemented, measured and integral to the live workflow. Its errors and the limits of this evaluation are part of the evidence.

#devchallenge #hf26challenge
