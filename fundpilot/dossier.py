"""Deterministic preparation plan. Cues are review prompts, never eligibility findings."""

import re
from urllib.parse import quote, urlsplit

from .logic import safe_text
from .verification import verification_queue

FACTS = {
    "career_stage": ("career_stage", "Current career stage", "Check your current appointment or enrollment."),
    "membership": (
        "membership",
        "Current paid membership",
        "Check your membership record and the named organization.",
    ),
    "first_author": ("first_author", "First author", "Check the submitted author order."),
    "presenting_author": (
        "presenting_author",
        "Presenting author",
        "Check the designated presenter in your submission.",
    ),
    "abstract_submitted": ("abstract_submitted", "Abstract submitted", "Check your submission receipt."),
    "abstract_accepted": ("abstract_accepted", "Abstract accepted", "Check the acceptance notice."),
    "in_person": ("in_person", "In-person attendance", "Check your travel and presentation plans."),
    "registration": ("registration", "Registered for this event", "Check your registration receipt."),
    "us_federal_employee": ("us_federal_employee", "US federal employment", "Check your employer status."),
    "upfront_costs": ("upfront_costs", "Upfront costs", "Check whether you can pay before reimbursement."),
    "request_limit": (
        "request_amount",
        "Requested funding and currency",
        "Check your proposed budget and its currency.",
    ),
}
# Whole parent passages are retained. These cues deliberately do not parse eligibility logic.
CUES = (
    (
        "exclusion",
        r"\b(?:not eligible|ineligible|not received|not awarded|not (?:be )?considered|cannot apply|may not|must not|excluded|excluding|unless|except)\b",
        "Possible exclusion or exception",
        "Which exclusion or exception in this passage applies to my situation, and what evidence establishes that?",
    ),
    (
        "pathway",
        r"\b(?:and|or|unless|except|provided that|subject to|only if)\b",
        "Combined conditions or alternative pathway",
        "Must all these conditions be met, or is there an alternative pathway? Which dependencies apply?",
    ),
    (
        "duration",
        r"\b(?:previous|prior|consecutive|within|last)\b|\b(?:\d+|one|two|three|four|five)\s+(?:years?|months?)\b",
        "Prior awards or duration needs context",
        "How is the relevant period measured, and do prior awards or career dates affect this condition?",
    ),
    (
        "money",
        r"[$£€]|\b(?:USD|EUR|GBP|stipend|reimburse\w*|funding limit|request ceiling)\b",
        "Award benefit versus applicant limit",
        "Is this an award benefit, reimbursement term or applicant request limit? Which currency and expenses apply?",
    ),
    (
        "materials",
        r"\b(?:CV|curriculum vitae|resume|résumé|letter|statement|proof|certificate|application form|budget|supporting documents?)\b",
        "Possible application materials",
        "Which named materials are mandatory, in what format, and by which stated deadline?",
    ),
    (
        "linked",
        r"\b(?:see|refer to|handbook|linked|full (?:rules|terms|guidelines)|website)\b",
        "Additional source or policy may be needed",
        "Which linked policies and full instructions govern this passage?",
    ),
)


def build_dossier(report, profile):
    """Return a structured, non-mutating view of the delivered report and declared facts."""
    passages = {f["id"]: {k: f[k] for k in ("id", "quote", "start", "end")} for f in report["findings"]}
    warnings = []
    for p in passages.values():
        for code, pattern, label, question in CUES:
            if re.search(pattern, p["quote"], re.IGNORECASE):
                warnings.append({"code": code, "label": label, "question": question, "passage": p["id"]})
        if re.search(r"\b(?:must|required|eligible)\b", p["quote"], re.IGNORECASE) and re.search(
            r"\b(?:awards?|receive|reimburse\w*|optional)\b", p["quote"], re.IGNORECASE
        ):
            warnings.append(
                {
                    "code": "mixed",
                    "label": "Mixed requirements and descriptive information",
                    "question": "Which statements are mandatory conditions and which describe benefits or optional steps?",
                    "passage": p["id"],
                }
            )
    missing = {}
    contradictions = []
    for f in report["findings"]:
        if f["status"] == "NOT MATCH":
            contradictions.append(f)
        if f["status"] == "UNKNOWN" and f["key"] in FACTS:
            field, label, action = FACTS[f["key"]]
            if getattr(profile, field) in (None, "Unknown"):
                item = missing.setdefault(
                    field, {"field": field, "label": label, "action": action, "passages": []}
                )
                if f["id"] not in item["passages"]:
                    item["passages"].append(f["id"])
    questions = {}
    for item in verification_queue(report):
        questions.setdefault(item["question"], set()).add(item["id"])
    for warning in warnings:
        questions.setdefault(warning["question"], set()).add(warning["passage"])
    return {
        "passages": passages,
        "contradictions": contradictions,
        "missing": list(missing.values()),
        "warnings": warnings,
        "questions": [{"question": q, "passages": sorted(ids)} for q, ids in questions.items()],
        "milestones": report.get("milestones", []),
    }


def markdown(report, profile, *, title="Public funding announcement", source_url=""):
    data = build_dossier(report, profile)
    try:
        parsed = urlsplit(source_url)
        source_link = (
            "[Official source](" + quote(source_url, safe="/:?&=%#@+~.-_") + ")"
            if parsed.scheme in ("https", "http") and parsed.hostname
            else "No valid HTTP(S) source URL supplied"
        )
    except ValueError:
        source_link = "No valid HTTP(S) source URL supplied"

    def refs(ids):
        return ", ".join(f"[Passage {i + 1}](#source-passage-{i + 1})" for i in sorted(set(ids)))

    lines = [
        "# Application Readiness Dossier",
        "",
        safe_text(title),
        "",
        f"**Source:** {source_link}",
        "",
        f"**Analysis:** {safe_text(report['mode'])} · {safe_text(str(report.get('model') or 'No model'))}",
        f"**Source SHA-256:** {report['source_sha256']}",
        "",
        (
            "**Preparation aid, not an official eligibility decision.** Findings compare text with self-reported facts. "
            "The additional source cues below are potential issues requiring review, not verified interpretations; "
            "they never change MATCH / NOT MATCH / UNKNOWN counts. Keep this local report private."
        ),
        "",
        "## A. Potential application blockers",
        "",
        "**Supported text-to-declared-fact contradictions**",
        "",
    ]
    for f in data["contradictions"]:
        lines += [
            f"- **NOT MATCH · {safe_text(f['key'].replace('_', ' '))}** — {safe_text(f['reason'])} ({refs([f['id']])}). Check your records first; ask the sponsor if the contradiction remains."
        ]
    if not data["contradictions"]:
        lines += ["No supported contradiction was identified. This does not establish eligibility."]
    lines += ["", "**Unresolved source cues — potential issues requiring review**", ""]
    for w in data["warnings"]:
        if w["code"] in ("exclusion", "duration", "pathway", "mixed"):
            lines += [
                f"- {w['label']} ({refs([w['passage']])}). Review the full passage and its dependencies before acting."
            ]
    if not any(w["code"] in ("exclusion", "duration", "pathway", "mixed") for w in data["warnings"]):
        lines += ["No targeted structural cue was found; unrecognized restrictions may still exist."]
    lines += [
        "",
        "## B. Missing applicant information",
        "",
        (
            "Fill facts you know, then analyze again. A missing fact and unclear sponsor wording are different problems; "
            "filling a field does not prove the condition applies."
        ),
        "",
    ]
    for item in data["missing"]:
        lines += [
            f"- **{item['label']}** — {item['action']} Update the corresponding form field ({refs(item['passages'])})."
        ]
    if not data["missing"]:
        lines += [
            "No missing existing form field was identified among UNKNOWN findings. Other facts may be needed for unsupported conditions."
        ]
    lines += [
        "",
        "## C. Application materials and deadlines",
        "",
        "**Materials / financial terms to review** — cue matches retain the whole passage; mandatory status is not established.",
        "",
    ]
    for w in data["warnings"]:
        if w["code"] in ("materials", "money"):
            lines += [f"- {w['label']}: {w['question']} ({refs([w['passage']])})."]
    if not any(w["code"] in ("materials", "money") for w in data["warnings"]):
        lines += [
            "No targeted document or monetary cue identified. Check the complete application instructions."
        ]
    lines += [
        "",
        (
            "**Explicit dated milestones** — roles are heuristic review labels, especially when a paragraph contains several dates. "
            "Dates alone do not establish that applications are open; confirm the cycle, role and timezone."
        ),
        "",
    ]
    for m in data["milestones"]:
        lines += [
            f"- **{safe_text(m['text'])}** — proposed role: {safe_text(m['role'])}; date comparison: {safe_text(m['status'])} ({refs([m['id']])})."
        ]
    if not data["milestones"]:
        lines += [
            "No supported explicit date with year identified. No deadline or timezone has been inferred."
        ]
    lines += [
        "",
        "## D. Sponsor clarification questions",
        "",
        (
            "Grouped suggestions, not sponsor answers. Resolve missing facts yourself first. "
            "Ask only questions still relevant after reviewing the complete source; share minimal necessary facts, not private records."
        ),
        "",
    ]
    for item in data["questions"]:
        lines += [f"- {item['question']} ({refs(item['passages'])})."]
    if not data["questions"]:
        lines += [
            "No targeted question identified. General recommendation: confirm unresolved scope with the sponsor."
        ]
    lines += [
        "",
        "## E. Final pre-application checklist",
        "",
        "- [ ] **1 · Your records:** resolve the supported contradictions in A and supply the missing facts in B; rerun after edits.",
        "- [ ] **2 · Your source review:** inspect every cited passage, especially exclusions, alternatives, waiting periods and mixed sections in A. Warnings are not conclusions.",
        "- [ ] **3 · Your preparation:** check the materials and dates in C, distinguish award benefits from request limits, and verify the current cycle and timezone.",
        "- [ ] **4 · Sponsor confirmation:** use the still-unresolved questions in D. Record the actual response yourself; FundPilot has not contacted anyone.",
        "- [ ] **5 · General recommendation:** review the full official announcement and linked policies. Pasted excerpts cannot establish completeness. Even all-MATCH findings need this review.",
        "",
        "## Exact source evidence",
        "",
        "Original parent passages are preserved, including exceptions. Offsets are zero-based character slices in the submitted text.",
        "",
    ]
    for p in data["passages"].values():
        lines += [
            f"### Source passage {p['id'] + 1}",
            "",
            f"Characters {p['start']}:{p['end']}",
            "",
            safe_text(p["quote"]),
            "",
        ]
    return "\n".join(lines)
