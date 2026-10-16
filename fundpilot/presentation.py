"""Plain-language presentation of unchanged findings; no additional inference."""

from .dossier import build_dossier
from .realworld import candidates


def suggested_questions(source, question_keys):
    """Keyword suggestions are incomplete; callers must always offer all fields."""
    if not source.strip():
        return set(question_keys) & {"membership", "first_author", "presenting_author"}
    return set(question_keys) & set(candidates(source[:18000])["keys"])


def overview(report, profile):
    counts = report["counts"]
    data = build_dossier(report, profile)
    lines = [
        f"## {report['readiness']}",
        "",
        "| Matching your facts | Potential problems | Missing / unclear |",
        "| --- | --- | --- |",
        f"| **{counts['MATCH']} MATCH** | **{counts['NOT MATCH']} NOT MATCH** | **{counts['UNKNOWN']} UNKNOWN** |",
        "",
        ("Supported comparisons with your declared facts—not verified credentials or official eligibility. "
        "UNKNOWN includes missing facts **and** unclear or unsupported conditions."),
        "",
        "**What to do next**",
        "",
    ]
    if counts["NOT MATCH"]:
        lines += [
            ("- **Potential problems to resolve:** check your declared facts against your records first. "
            "If the contradiction remains, ask the organizer before investing time in an application (dossier A and D).")
        ]
    if counts["UNKNOWN"]:
        labels = ", ".join(item["label"] for item in data["missing"])
        lines += [
            "- **Missing information / needs clarification:** "
            + (
                f"check and update {labels}. "
                if labels
                else "The current form facts may not resolve the wording. "
            )
            + "Review the unresolved source and ask the organizer if needed (dossier B and D)."
        ]
    if counts["MATCH"]:
        lines += [
            "- **Requirements matching your facts:** check the evidence and complete source. A MATCH does not mean the whole application qualifies."
        ]
    flags = {}
    for warning in sorted(data["warnings"], key=lambda w: w["code"] != "exclusion"):
        flags.setdefault(warning["label"], set()).add(warning["passage"] + 1)
    if flags:
        lines += ["", "**Source-review flags — provisional, not counted as NOT MATCH**", ""]
        for label, ids in flags.items():
            lines += [
                f"- {label} — passage(s) {', '.join(map(str, sorted(ids)))}. Review the full context in dossier A–D."
            ]
    lines += [
        "",
        (f"Additional informational findings: {counts.get('INFO', 0)}. "
        "Open **Application Readiness Dossier — plan and source evidence** for the five-part plan, "
        "or download it below. Always review the full official announcement and linked policies."),
    ]
    return "\n".join(lines)
