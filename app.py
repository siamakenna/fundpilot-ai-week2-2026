"""FundPilot demo Gradio UI. Local Gemma inference requires running Ollama."""
import json
import os
import tempfile
from pathlib import Path
import gradio as gr
from fundpilot.fixtures import opportunities, profiles, reference_extraction
from fundpilot.logic import assess, to_markdown
from fundpilot.gemma import extract, DEFAULT_MODEL

OPS=opportunities(); PROFILES=profiles()

def initial_opportunity(op_id):
    return OPS[op_id]["eligibility_text"]

def initial_profile(profile_id):
    return json.dumps(PROFILES[profile_id],indent=2)

def run(profile_text, call_text, op_id, mode, verified_clause_review):
    try:
        profile=json.loads(profile_text)
        if not isinstance(profile,dict): raise ValueError("Profile must be a JSON object")
        if not call_text.strip(): raise ValueError("Funding call text is required")
        ref=OPS[op_id]
        same_call = call_text.strip() == ref["eligibility_text"].strip()
        if mode=="Curated reference demo (NO AI)":
            if not same_call:
                raise ValueError("Reference demo only works with an unchanged fictional opportunity. Choose Live Gemma for edited call text.")
            extraction=reference_extraction(ref)
            extraction_mode="Curated reference (not AI)"
            model_name=None
            clause_review=False
        else:
            extraction=extract(call_text)
            extraction_mode="Real local Gemma"
            model_name=DEFAULT_MODEL
            clause_review=not verified_clause_review and not same_call
        result=assess(extraction,profile,call_text,mode=extraction_mode,model_name=model_name,
                      needs_clause_review=clause_review,
                      expected_keys=ref["mandatory"] if same_call else None)
        md=to_markdown(result,ref["title"] if same_call else "User-provided funding text")
        fd, target=tempfile.mkstemp(prefix="fundpilot_",suffix=".md")
        os.close(fd)
        file=Path(target)
        file.write_text(md,encoding="utf-8")
        explanation = "**This result used live Gemma inference.**" if mode=="Live local Gemma" else "**Reference demo only: no generative model was used.** Switch to Live local Gemma to validate the real model path."
        return explanation+"\n\n"+md,str(file)
    except Exception as e:
        return f"### Could not analyze\n\n{type(e).__name__}: {e}\n\nNo result was fabricated.",None

with gr.Blocks(title="FundPilot AI — Evidence-First Funding Readiness", analytics_enabled=False) as demo:
    gr.Markdown("# FundPilot AI\nResearch funding eligibility, explained with evidence. **All built-in opportunities and profiles are fictional.**")
    with gr.Row():
        with gr.Column():
            profile_id=gr.Dropdown(choices=list(PROFILES),value="alex_postgrad",label="1. Fictional researcher")
            profile_json=gr.Code(value=initial_profile("alex_postgrad"),language="json",label="Profile JSON (editable)")
            opportunity=gr.Dropdown(choices=list(OPS),value="early_career_travel",label="2. Fictional funding call")
            call_text=gr.Textbox(value=initial_opportunity("early_career_travel"),lines=9,label="Funding requirements (editable)")
            mode=gr.Radio(["Curated reference demo (NO AI)","Live local Gemma"],value="Curated reference demo (NO AI)",label="Analysis method")
            reviewed=gr.Checkbox(value=False,label="I personally reviewed extracted clauses for completeness (custom calls only)")
            go=gr.Button("Analyze requirements",variant="primary")
        with gr.Column():
            output=gr.Markdown("**No analysis has run.** Select a scenario and click Analyze requirements.")
            downloadable=gr.File(label="Download source-grounded Markdown report")
    profile_id.change(initial_profile, inputs=profile_id,outputs=profile_json)
    opportunity.change(initial_opportunity,inputs=opportunity,outputs=call_text)
    go.click(run,inputs=[profile_json,call_text,opportunity,mode,reviewed],outputs=[output,downloadable])
    gr.Markdown("Informational tool only. Real grant deadlines, eligibility, and award amounts always need verification against the official sponsor. No data is transmitted to a hosted model API in local mode.")
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1",share=False)
