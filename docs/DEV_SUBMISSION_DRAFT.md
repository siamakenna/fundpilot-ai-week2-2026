---
title: "FundPilot AI: A Local Gemma Assistant for Funding Eligibility That Doesn't Guess"
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).*

## What I Built

**FundPilot AI** addresses a narrow but frustrating problem for early-career researchers: spending hours on grant or conference travel applications only to discover a hidden eligibility requirement. It takes a researcher's profile and a funding call, then produces source-linked MATCH / NOT MATCH / UNKNOWN findings. Its most important feature is knowing when it can't make a reliable determination.

The customer is an independent researcher or small mentoring program without dedicated grant-development support. My proposed business model is a $9 one-off readiness report or a $39/month advising workspace; these are **pricing hypotheses**, not sales.

## Demo

[ADD REAL VERIFIED VIDEO OR WORKING DEMO URL; REMOVE THIS PLACEHOLDER BEFORE PUBLICATION]

Show one fictional eligible profile, one disqualifying condition, one case lacking evidence. Distinguish a genuinely live Gemma run from any reference fixture demonstration.

## Code

[ADD VERIFIED PUBLIC GITHUB URL BEFORE PUBLICATION]

## How I Built It

The design is source text → local Gemma structured eligibility extraction → exact-source evidence validation → deterministic requirement evaluation → markdown report. A generated sentence that doesn't appear in the provided source is rejected. Unrecognized requirements are marked UNKNOWN. The model does not get to declare an applicant eligible itself.

[ADD REAL MODEL VERSION, REAL TIMING, PASSING TEST COUNTS, AND ACTUAL ERROR CASES]

## Why Does Open Innovation Matter?

Open-weight local inference makes it possible to evaluate a profile without submitting private applicant details to an external model API. The model and its prompt can be inspected, swapped, and tested on a known fixture set. Local operation removes external per-call API charges, though compute still has hardware and electricity costs.

[ADD EVIDENCE THAT THE OPEN MODEL ACTUALLY WORKS, INCLUDING ITS WEAKNESSES]

## My Agent Session

[OPTIONAL: ONLY ADD REAL RECORDED SESSION. OTHERWISE DELETE SECTION.]

## My First User

[OPTIONAL: ONLY ADD PERMITTED REAL TESTER COMMENTS. OTHERWISE DELETE SECTION.]

## Prize Categories

- Best Use of Gemma (only after Gemma is genuinely implemented and demonstrated)
