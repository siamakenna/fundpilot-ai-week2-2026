"""Ordinary form workflow for public announcements; no JSON editing required."""

import os
import tempfile
import time
from pathlib import Path

import gradio as gr

from .dossier import markdown as dossier_markdown
from .logic import safe_text
from .onboarding import INITIAL_STATUS, INTRO, SAMPLE_STATUS, TUTORIAL, check_local_model
from .presentation import overview as readiness_overview
from .presentation import suggested_questions
from .quickstart import CNS_EXCERPT, CNS_RETRIEVED, CNS_URL, sample_inputs
from .realworld import Applicant, analyze
from .verification import markdown, queue_markdown

QUESTIONS = {
    "membership": "Current paid member of every organization required by this call?",
    "first_author": "First author of the submitted work?",
    "presenting_author": "Presenting author / presenter of the work?",
    "abstract_submitted": "Abstract submitted to this event?",
    "abstract_accepted": "Abstract or presentation accepted / approved?",
    "in_person": "Will attend and present in person?",
    "registration": "Registered for this event?",
    "us_federal_employee": "Employed by a US federal agency?",
    "upfront_costs": "Able to pay all attendance expenses before reimbursement?",
}


def run_public(
    source,
    title,
    url,
    stage,
    amount,
    currency,
    method,
    *answers,
    progress=gr.Progress(),  # noqa: B008 — Gradio injects its progress dependency.
    include_dossier=False,
):
    tick = time.perf_counter()
    try:
        values = {"Yes": True, "No": False, "Unknown": None}
        profile = Applicant(
            career_stage=stage,
            request_amount=None if amount is None or str(amount).strip() == "" else float(amount),
            request_currency=currency,
            **{key: values[value] for key, value in zip(QUESTIONS, answers, strict=True)},
        )
        mode = "gemma" if method == "Live local Gemma" else "rules"
        report = analyze(source, profile, mode=mode, progress=progress)
        md = markdown(report, title=title or "Public funding announcement", source_url=url)
        fd, target = tempfile.mkstemp(prefix="fundpilot_public_", suffix=".md")
        os.close(fd)
        Path(target).write_text(md)
        rows = [
            [f["id"] + 1, f["key"].replace("_", " "), f["status"], f["quote"], f["reason"]]
            for f in report["findings"]
            if f["key"] != "scope_review"
        ]
        overview = f"## {report['readiness']}\n\n" + " · ".join(
            f"**{n} {s}**" for s, n in report["counts"].items()
        )
        overview += f"\n\n{report['covered_units']}/{report['source_units']} source passages accounted for. Completed in {time.perf_counter() - tick:.1f}s. "
        overview += "**Live Gemma interpretation**" if mode == "gemma" else "**Rule baseline — NO AI**"
        overview += "\n\nSupported comparisons use your declared facts; they are not verified credentials. Every passage also requires a scope review for additional conditions, exceptions and linked rules. See the report for all review items. This is not a sponsor’s eligibility decision."
        if not include_dossier:
            overview += "\n\n" + queue_markdown(report, limit=3)
        result = (overview, rows, md, target)
        if include_dossier:
            overview = readiness_overview(report, profile)
            overview += f"\n\n{'Live local Gemma 1B' if mode == 'gemma' else 'Rule baseline — NO AI'} · {time.perf_counter() - tick:.1f}s · {report['covered_units']}/{report['source_units']} pasted passages accounted for (not proof of complete interpretation)."
            result = (overview, rows, md, target)
            dossier = dossier_markdown(
                report, profile, title=title or "Public funding announcement", source_url=url
            )
            fd, dossier_target = tempfile.mkstemp(prefix="fundpilot_dossier_", suffix=".md")
            os.close(fd)
            Path(dossier_target).write_text(dossier, encoding="utf-8")
            # Gradio prefixes generated header IDs; portable Markdown downloads do not.
            display_dossier = dossier.replace("(#source-passage-", "(#h-source-passage-")
            return result + (display_dossier, dossier_target)
        return result
    except Exception as exc:  # noqa: BLE001 — UI boundary must clear every output on failure.
        result = (
            "## Analysis unavailable\n\n"
            + safe_text(str(exc))
            + "\n\nNo result or download was fabricated. Keep the complete eligibility section, including exceptions and deadlines; retry after checking local Ollama.",
            [],
            "",
            None,
        )
        return result + ("", None) if include_dossier else result


def run_public_with_dossier(*args, progress=gr.Progress()):  # noqa: B008 — Gradio dependency injection
    return run_public(*args, progress=progress, include_dossier=True)


def clear_dossier(*_):
    return clear_public() + ("", None)


def clear_public(*_):
    return "Inputs changed. Analyze again before using or downloading a report.", [], "", None


def question_visibility(source, show_all):
    suggested = suggested_questions(source, QUESTIONS)
    return [gr.update(visible=bool(show_all or key in suggested)) for key in QUESTIONS]


def build_public_ui():
    gr.Markdown(INTRO)
    with gr.Row():
        sample = gr.Button("Load sample public excerpt (CNS; fictional applicant)", variant="primary")
        status_button = gr.Button("Check local model")
    model_status = gr.Markdown(INITIAL_STATUS)
    sample_status = gr.Markdown("")
    with gr.Accordion("How FundPilot works, results and privacy", open=False):
        gr.Markdown(TUTORIAL)
    status_button.click(check_local_model, outputs=model_status)
    gr.Markdown("## 1. Add the official announcement")
    gr.Markdown(
        f"Optional quick-start: one short [official CNS passage]({CNS_URL}), retrieved {CNS_RETRIEVED}. "
        "Loads **fictional, editable facts**, not an analysis. Click **Analyze public announcement** "
        "to run genuine local Gemma. This excerpt does not cover the full call or confirm that applications "
        "are open. Replace it with your own public text at any time."
    )
    with gr.Row():
        title = gr.Textbox(label="Opportunity title")
        url = gr.Textbox(
            label="Official announcement link (reference only — not fetched)",
            info="This website is not automatically read. Paste the actual requirements below.",
        )
    source = gr.Textbox(
        label="Eligibility, exclusions, amounts, deadlines and application instructions",
        lines=6,
        placeholder="Paste the complete relevant public text. Keep list headings, exceptions and dates. Use a separate line for each paragraph or list item.",
    )
    gr.Markdown("## 2. Supply your facts")
    with gr.Row():
        stage = gr.Dropdown(
            [
                "Unknown",
                "Undergraduate",
                "Graduate student",
                "Postbaccalaureate",
                "Postdoc",
                "Research professional",
                "Other",
            ],
            value="Unknown",
            label="Current career stage",
        )
        amount = gr.Textbox(
            value="",
            label="Requested funding (optional; leave blank if unknown)",
            placeholder="For example: 250.50",
        )
        currency = gr.Dropdown(["USD", "GBP", "EUR"], value="USD", label="Request currency")
    gr.Markdown(
        "Questions below are suggested from simple text cues, which can miss requirements. "
        "**Show all questions** to inspect every field. Hidden answers are preserved; unknown facts stay Unknown."
    )
    show_all = gr.Checkbox(label="Show all questions", value=False)
    facts = []
    questions = list(QUESTIONS.items())
    for offset in range(0, len(questions), 3):
        with gr.Row():
            for key, label in questions[offset : offset + 3]:
                facts.append(
                    gr.Radio(
                        ["Unknown", "Yes", "No"],
                        value="Unknown",
                        label=label,
                        visible=key in suggested_questions("", QUESTIONS),
                    )
                )
    gr.Markdown(
        "Membership duration, prior awards, required materials, conditional pathways and unsupported restrictions remain review questions. A sponsor stipend is not automatically a limit on your request."
    )
    method = gr.Radio(
        ["Live local Gemma", "Rule baseline (NO AI)"], value="Live local Gemma", label="Analysis method"
    )
    go = gr.Button("Analyze public announcement", variant="primary")
    gr.Markdown("## 3. Review evidence and next steps")
    summary = gr.Markdown(
        "No analysis yet. Local Ollama and gemma3:1b must be installed for live analysis. CPU inference can take several minutes; the report stops after five minutes instead of guessing."
    )
    with gr.Accordion("Application Readiness Dossier — plan and source evidence", open=False):
        dossier = gr.Markdown(elem_id="readiness-dossier", header_links=True)
    dossier_download = gr.File(
        label="Download Application Readiness Dossier (Markdown)",
        interactive=False,
        elem_id="dossier-download",
    )
    with gr.Accordion("Detailed findings and exact passages", open=False):
        table = gr.Dataframe(
            headers=["Passage", "Criterion", "Finding", "Exact evidence", "Reason"],
            column_widths=[80, 160, 130, 420, 420],
            datatype=["number", "str", "str", "str", "str"],
            interactive=False,
            wrap=True,
            label="Supported comparisons and unresolved interpretations",
        )
    with gr.Accordion("Full evidence report and passage review checklist", open=False):
        report = gr.Markdown()
    download = gr.File(
        label="Download readiness report (Markdown)", interactive=False, elem_id="evidence-download"
    )
    inputs = [source, title, url, stage, amount, currency, method, *facts]
    outputs = [summary, table, report, download, dossier, dossier_download]
    source.change(question_visibility, inputs=[source, show_all], outputs=facts)
    show_all.change(question_visibility, inputs=[source, show_all], outputs=facts)

    def lock():
        return [gr.update(interactive=False) for _ in inputs + [go, sample]]

    def unlock():
        return [gr.update(interactive=True) for _ in inputs + [go, sample]]

    # Prevent an older in-flight result from overwriting edits. Inputs become
    # editable again after success or the handled error result.
    sample.click(lambda: sample_inputs(QUESTIONS) + [SAMPLE_STATUS], outputs=inputs + [sample_status]).then(
        clear_dossier, outputs=outputs
    )
    source.change(
        lambda text: SAMPLE_STATUS if text == CNS_EXCERPT else "", inputs=source, outputs=sample_status
    )
    event = go.click(lock, outputs=inputs + [go, sample], queue=False)
    event.then(run_public_with_dossier, inputs=inputs, outputs=outputs, concurrency_limit=1).then(
        unlock, outputs=inputs + [go, sample]
    )
    for field in inputs:
        field.change(clear_dossier, outputs=outputs)
