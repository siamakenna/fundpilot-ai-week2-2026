# Gemma 1B versus 4B: exploratory development comparison

**Decision: retain Gemma 3 1B.** The installed 4B model found one additional provisional reference condition, took longer, and produced one additional supported MATCH that disagreed with the provisional labels. No independently reviewed evidence justifies promotion. Strategy C was not pursued: these results do not establish a promising safety/usability gain. No production prompt, schema or model default changed.

The protocol was saved before the new inference run. Control A reuses a completed real 1B run; control B is one new real 4B run through the identical frozen interpreter. Three historical development sources (SDB, ALBA, GNS), ten passages, twenty provisional atomic reference labels, identical fictional profile and input hashes. No fresh holdout, tuning or human validation. Previously exposed v0.4 reserved sources were excluded. This common diagnostic unit differs from the original historical benchmark; its scores do not replace those results.

| Metric | Control A: 1B | Control B: 4B |
| --- | --- | --- |
| Exact category + criterion matches | 3/20 reference; 13 predictions | 4/20 reference; 14 predictions |
| Precision / recall / F1 | 23.08% / 15.00% / 18.18% | 28.57% / 20.00% / 23.53% |
| Mandatory-condition recall | 3/17 (17.65%) | 4/17 (23.53%) |
| Exclusion recall | 1/4 (25%) | 1/4 (25%) |
| Literal source-span attachment | 13/13 | 14/14 |
| Supported MATCH disagreement with provisional reference | 2/2 MATCH findings | 3/3 MATCH findings |
| Supported NOT MATCH disagreement | 0; no NOT MATCH findings delivered | 0; no NOT MATCH findings delivered |
| UNKNOWN / delivered non-INFO findings | 8/10 (80%); 3 INFO | 9/12 (75%); 2 INFO |
| Completed reports / passages | 3/3; 10/10 | 3/3; 10/10 |
| Mean / total workflow latency | 15.442s / 46.325s | 40.943s / 122.830s |
| Prompt / generated tokens | 4,143 / 274 | 4,153 / 286 |

False supported findings here mean disagreement with **provisional, coding-assistant annotations**, not verified real-world eligibility errors. No confidence intervals or population accuracy claims are warranted. Exact quotations measure source fidelity, not interpretation completeness. The runs occurred in different sessions, so latency is descriptive rather than a controlled paired speed study. There were no failed reports in this comparison; historical failed atomic runs remain in unmerged PR #4. A smaller UNKNOWN fraction does not establish greater safety.

Runtime: Intel Core i5-1038NG7 CPU, 16 GiB RAM, Ollama 0.40.4, Q4_K_M. Full digests: 1B `97558784bdc9175075a72655bf360b15da17df6b3b9e5182af9f8c0c8e58ba7c`; 4B `68ceab7e468a31c988b44d5a4984a0e21f58c4f7158c6ce29c1804babac38df7`. Same embedded prompt/schema in `realworld.py`, temperature 0, seed 42, context 8192, output cap 256; request timeout 90 seconds, workflow limit 300 seconds. No downloaded models, cloud inference or metered API fees; electricity not measured.

Reproduction requires the hash-checked local official-source cache. `PYTHONPATH=. python scripts/compare_model_size.py` refuses to overwrite its existing output directory. The references are byte-for-byte copies from the preserved experimental branch. [Protocol](../evaluation/model-size/PROTOCOL.md), [freeze hashes](../evaluation/model-size/freeze.json), [1B saved result](../evidence/model-size/control-1b.json), [4B result and raw Boolean responses](../evidence/model-size/), [model identities](../evidence/model-size/model-tags.json).

A new blind annotation packet contains the original public passages, attribution, hashes, blank annotation fields and the fictional profile, **without predictions or reference answers**. It is local to avoid duplicating entire copyrighted paragraphs in the public repository: `.local-reports/model-size/blind-annotation-packet.md`. Regenerate it with `PYTHONPATH=. python scripts/prepare_blind_model_review.py`; a reviewer must annotate without looking at the result directory. No reviewer has completed this packet and no invitation has been sent. Engineering did not wait for review.

The earlier atomic v0.4 candidate remains rejected and unmerged. Product-only source warnings and the dossier make uncertainty actionable; they do not improve these extraction scores or repair the engine's semantic limitations.
