"""Ordinary form workflow for public announcements; no JSON editing required."""

import os
import tempfile
import time
from pathlib import Path

import gradio as gr

from .logic import safe_text
from .realworld import Applicant, analyze, markdown

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


def run_public(source, title, url, stage, amount, currency, method, *answers, progress=gr.Progress()):
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
        return overview, rows, md, target
    except Exception as exc:
        return (
            "## Analysis unavailable\n\n"
            + safe_text(str(exc))
            + "\n\nNo result or download was fabricated. Keep the complete eligibility section, including exceptions and deadlines; retry after checking local Ollama.",
            [],
            "",
            None,
        )


def clear_public(*_):
    return "Inputs changed. Analyze again before using or downloading a report.", [], "", None


def build_public_ui():
    gr.Markdown(
        "### Check the fine print before writing the application\nPaste a **public** announcement. Only its text goes to local Gemma; your applicant facts are compared in Python. Do not paste private grant documents. Fields start unknown rather than assuming eligibility."
    )
    gr.Markdown("## 1. Add the official announcement")
    with gr.Row():
        title = gr.Textbox(label="Opportunity title")
        url = gr.Textbox(label="Official source URL (attribution only; not fetched)")
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
    facts = []
    questions = list(QUESTIONS.items())
    for offset in range(0, len(questions), 3):
        with gr.Row():
            for key, label in questions[offset : offset + 3]:
                facts.append(gr.Radio(["Unknown", "Yes", "No"], value="Unknown", label=label))
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
    table = gr.Dataframe(
        headers=["Passage", "Criterion", "Finding", "Exact evidence", "Reason"],
        datatype=["number", "str", "str", "str", "str"],
        interactive=False,
        wrap=True,
        label="Supported comparisons and unresolved interpretations",
    )
    with gr.Accordion("Full evidence report and passage review checklist", open=False):
        report = gr.Markdown()
    download = gr.File(label="Download readiness report (Markdown)", interactive=False)
    inputs = [source, title, url, stage, amount, currency, method, *facts]
    outputs = [summary, table, report, download]

    def lock():
        return [gr.update(interactive=False) for _ in inputs] + [gr.update(interactive=False)]

    def unlock():
        return [gr.update(interactive=True) for _ in inputs] + [gr.update(interactive=True)]

    # Prevent an older in-flight result from overwriting edits. Inputs become
    # editable again after success or the handled error result.
    event = go.click(lock, outputs=inputs + [go], queue=False)
    event.then(run_public, inputs=inputs, outputs=outputs, concurrency_limit=1).then(
        unlock, outputs=inputs + [go]
    )
    for field in inputs:
        field.change(clear_public, outputs=outputs)
