"""FundPilot demo Gradio UI. Local Gemma inference requires running Ollama."""

import json
import time
import os
import tempfile
from pathlib import Path
import gradio as gr
from fundpilot.fixtures import opportunities, profiles, reference_extraction
from fundpilot.logic import assess, to_markdown, safe_text
from fundpilot.gemma import extract, DEFAULT_MODEL

OPS = opportunities()
PROFILES = profiles()


def initial_opportunity(op_id):
    return OPS[op_id]["eligibility_text"]


def initial_profile(profile_id):
    return json.dumps(PROFILES[profile_id], indent=2)


def run(profile_text, call_text, op_id, mode, verified_clause_review=False):
    started = time.perf_counter()
    try:
        profile = json.loads(profile_text)
        if not isinstance(profile, dict):
            raise ValueError("Profile must be a JSON object")
        if not call_text.strip():
            raise ValueError("Funding call text is required")
        ref = OPS[op_id]
        same_call = call_text.strip() == ref["eligibility_text"].strip()
        if mode == "Curated reference demo (NO AI)":
            if not same_call:
                raise ValueError(
                    "Reference demo only works with an unchanged fictional opportunity. Choose Live Gemma for edited call text."
                )
            extraction = reference_extraction(ref)
            extraction_mode = "Curated reference (not AI)"
            model_name = None
            clause_review = False
        elif mode == "Live local Gemma":
            extraction = extract(call_text)
            extraction_mode = "Real local Gemma"
            model_name = DEFAULT_MODEL
            clause_review = not same_call
        else:
            raise ValueError("Choose a supported analysis method")
        result = assess(
            extraction,
            profile,
            call_text,
            mode=extraction_mode,
            model_name=model_name,
            needs_clause_review=clause_review,
            expected_requirements=reference_extraction(ref) if same_call else None,
        )
        md = to_markdown(result, ref["title"] if same_call else "User-provided funding text")
        fd, target = tempfile.mkstemp(prefix="fundpilot_", suffix=".md")
        os.close(fd)
        file = Path(target)
        file.write_text(md, encoding="utf-8")
        explanation = (
            "**This result used live Gemma inference.**"
            if mode == "Live local Gemma"
            else "**Reference demo only: no generative model was used.** Switch to Live local Gemma to validate the real model path."
        )
        counts = {
            status: sum(f.status == status for f in result.findings)
            for status in ("MATCH", "NOT MATCH", "UNKNOWN")
        }
        summary = f"## {result.verdict}\n\n" + " · ".join(f"**{n} {k}**" for k, n in counts.items())
        summary += f"\n\nCompleted in **{time.perf_counter() - started:.1f}s**. " + explanation
        questions = [
            f"- {safe_text(f.source_quote)} — {safe_text(f.reason)}"
            for f in result.findings
            if f.status in ("UNKNOWN", "NOT MATCH")
        ]
        if clause_review:
            questions.insert(
                0,
                "- Custom text: verify the meaning and completeness of every extracted clause with the sponsor. This prototype cannot certify a custom call.",
            )
        if questions:
            summary += "\n\n### Before you apply\n\n" + "\n".join(questions)
        return summary + "\n\n---\n\n" + md, str(file)
    except Exception as e:
        return (
            f"### Could not analyze\n\n{type(e).__name__}: {safe_text(str(e))}\n\nNo result was fabricated.",
            None,
        )


def profile_overview(profile_id):
    p = PROFILES[profile_id]
    presentation = (
        "Unknown"
        if p["accepted_presentation"] is None
        else ("Accepted" if p["accepted_presentation"] else "Not accepted")
    )
    return (
        f"**{p['display_name']}** · {p['career_stage'].replace('_', ' ')}\n\n"
        f"{p['region']} · Request **${p['award_request_usd']:,}** · Presentation: **{presentation}**"
    )


def clear_result(*_):
    return "**Inputs changed.** Analyze again to create a report for these inputs.", None


with gr.Blocks(title="FundPilot AI — Public Funding Readiness", analytics_enabled=False) as demo:
    gr.Markdown("# FundPilot AI")
    with gr.Tab("Analyze a public announcement"):
        from fundpilot.real_ui import build_public_ui
        build_public_ui()
    with gr.Tab("Fictional reference examples (legacy)"):
        gr.Markdown(
            "# FundPilot AI\n### Before you spend hours applying, check the fine print.\n"
            "Compare your supplied facts with the funding call, see the exact evidence, and take away questions to verify. "
            "**Every built-in profile and opportunity is fictional.**"
        )
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 1. Choose a researcher")
                profile_id = gr.Dropdown(
                    choices=[(p["display_name"], k) for k, p in PROFILES.items()],
                    value="alex_postgrad",
                    label="Fictional researcher",
                )
                overview = gr.Markdown(profile_overview("alex_postgrad"))
                with gr.Accordion("Edit supplied facts (JSON)", open=False):
                    gr.Markdown(
                        "Use true, false, or null for unknown facts. Only the funding text is sent to local Gemma."
                    )
                    profile_json = gr.Code(
                        value=initial_profile("alex_postgrad"), language="json", label="Profile JSON (editable)"
                    )
                gr.Markdown("## 2. Read the funding call")
                opportunity = gr.Dropdown(
                    choices=[(v["title"].replace("FICTIONAL — ", ""), k) for k, v in OPS.items()],
                    value="early_career_travel",
                    label="Fictional funding call",
                )
                call_text = gr.Textbox(
                    value=initial_opportunity("early_career_travel"),
                    lines=8,
                    label="Funding requirements (editable)",
                )
                mode = gr.Radio(
                    ["Curated reference demo (NO AI)", "Live local Gemma"],
                    value="Curated reference demo (NO AI)",
                    label="Analysis method",
                )
                gr.Markdown(
                    "Custom or edited calls always need human verification. Local Gemma must be running for live analysis."
                )
                go = gr.Button("Analyze requirements", variant="primary")
            with gr.Column(scale=1):
                gr.Markdown("## 3. Review evidence & download")
                output = gr.Markdown("**No analysis has run.** Select a scenario and click Analyze requirements.")
                downloadable = gr.File(label="Download Markdown report", interactive=False)
        profile_id.change(initial_profile, inputs=profile_id, outputs=profile_json)
        profile_id.change(profile_overview, inputs=profile_id, outputs=overview)
        opportunity.change(initial_opportunity, inputs=opportunity, outputs=call_text)
        for component in (profile_id, profile_json, opportunity, call_text, mode):
            component.change(clear_result, inputs=None, outputs=[output, downloadable])
        go.click(run, inputs=[profile_json, call_text, opportunity, mode], outputs=[output, downloadable])
        gr.Markdown(
            "Informational only. Supplied facts are self-reported. Confirm official eligibility, deadlines and all UNKNOWN findings with the sponsor. "
            "Local inference, no hosted model API, no accounts or payments."
        )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", share=False)
