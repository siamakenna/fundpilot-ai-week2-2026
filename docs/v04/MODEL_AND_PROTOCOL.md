# Candidate and protocol notes

Hardware: Intel Core i5-1038NG7 2.00 GHz, 8 logical CPUs, 16 GiB RAM.
Installed Ollama 0.40.4; Gemma 3 1B Q4_K_M, 806 MB on disk.
Model digest: `97558784bdc9175075a72655bf360b15da17df6b3b9e5182af9f8c0c8e58ba7c`.
A sampled 1B inference process used approximately 1.15 GiB RSS; this is not peak
memory. CPU-only local inference; no metered API fees. Electricity unmeasured.

A larger model was not downloaded. Although 16 GiB does not automatically rule out
a quantized larger model, capacity alone would not establish acceptable CPU latency
or fix the observed schema/semantics failures. The scoped comparison uses the
already installed 1B model and preserves the stronger-model option for a separate,
newly preregistered experiment. There is no claim that 1B is optimal or superior.

Development iterations are retained separately:

- B1: model copied evidence/applicability/dependency strings. Exact validation
  rejected all three development reports; copied wording was not silently repaired.
- B2: model selected numbered spans, but nullable dependency selections contradicted
  its non-NONE relationships. All three reports rejected; no dependency invented.
- B3: model selects numbered evidence and semantic fields. Python explicitly attaches
  full paragraph context for every relationship. This is source context for review,
  **not independently validated evidence that the proposed relationship is correct**.
  No free-form model quotation becomes source evidence. Scope remains conservative.

No source labels were edited in response to these outputs. B3 is the final candidate
for the reserved comparison regardless of its outcome; no post-final tuning.
The original engine, fixtures, references, historical metrics and released videos
remain intact. New scores are a different common-unit experiment with expanded
vocabulary; they must never replace the original paragraph/criterion scores.

The initial A development attempt found Ollama stopped (3 connection failures).
It remains in evidence. Starting the existing local service was an infrastructure
repair; the separate A service-restored run uses unchanged code/configuration.
Final evaluation has no such retries: service health is checked before the run,
then all failures count in the fixed denominator.

Source span accuracy means literal attachment, not semantic relevance, minimality,
coverage or correctness. Numbered evidence deliberately makes literal attachment
more reliable while leaving interpretation errors visible in other metrics.
Unparseable responses have no countable atoms; their failures remain in case and
passage denominators and are reported separately. Partial accepted passages in a
failed case do not yield a delivered report.
