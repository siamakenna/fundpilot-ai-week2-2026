# Judge walkthrough: check the fine print

Record the real Gradio UI with **Live local Gemma** selected throughout. Target
2–3 minutes of explanation, plus actual inference waits. A longer honest recording
is preferable to an implied speed claim. If a run fails, show the error; do not
replace it with a fixture result. The outcomes below are previously observed,
not promises about the next model run.

| Action | Suggested narration / point to show |
| --- | --- |
| Open the three-step UI | “Before writing a funding application, check whether its conditions fit. This prototype is for independent researchers and small mentoring programs. Everything on screen is fictional.” |
| Alex Morgan → Early Career Science Conference Travel Award → Live local Gemma → Analyze requirements | “Gemma classifies the call sentences locally. Python attaches their exact text and checks the profile. Alex previously matched these supplied conditions.” Show the actual verdict and source evidence. |
| Alex → Enrolled Graduate Student Mobility Grant → Analyze requirements | “The new inputs clear the old result. Alex is not enrolled, and the request exceeds this call's cap.” Show NOT MATCH findings if returned. |
| Casey Rivera → Early Career Science Conference Travel Award → Analyze requirements | “Casey's presentation acceptance is unknown. The next step is to verify it, rather than infer an answer.” Show the actual result. |
| Download Markdown report; open it | Show model/mode, quotes, findings and verification questions in the real downloaded file. |
| Open the evaluation document | “The tuned development set matched 20 of 21 clauses, and only five of six reports validated. This is not accuracy on unseen grants. Custom calls always require review.” |
| Finish on the repository | “The $9 report and $39 monthly workspace are unvalidated hypotheses. My next test is whether this saves application time for a consenting tester.” |

Keep live waits visible or explicitly label trimmed waits. Do not use an old report
as if just generated, show reference fixtures as AI, invent a customer, or claim
that source attachment proves semantic correctness. Review the recording before
uploading. See [capture steps](LOCAL_CAPTURE_STEPS.md).
