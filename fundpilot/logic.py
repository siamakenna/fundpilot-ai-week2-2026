"""Deterministic eligibility evaluation. Model text never directly sets verdict."""

from __future__ import annotations
import re
import math
import html
from .models import ExtractedRequirement, Extraction, Finding, Report

KEYS = {
    "us_based",
    "research_professional_or_grad_student",
    "degree_within_five_years",
    "accepted_presentation",
    "currently_enrolled_graduate",
    "dc_md_va",
    "training_workshop",
    "repo_mit_or_apache",
    "current_postdoc",
    "international_host_invitation",
    "outreach_project",
    "request_at_most",
    "unmapped",
}


# Only trusted, deterministic criteria may be evaluated. Everything else is UNKNOWN.
def check(key: str, profile: dict, limit: int | None = None) -> tuple[str, str]:
    def boolean(value, positive, negative):
        if type(value) is not bool:
            return ("UNKNOWN", "Profile does not contain enough information.")
        return ("MATCH", positive) if value is True else ("NOT MATCH", negative)

    if key == "us_based":
        return boolean(
            profile.get("us_based"), "Profile confirms US base.", "Profile indicates not US-based."
        )
    if key == "research_professional_or_grad_student":
        stage = profile.get("career_stage")
        enrolled = profile.get("currently_enrolled_graduate")
        if stage == "research_professional" or enrolled is True:
            return ("MATCH", "Research professional or enrolled graduate student.")
        if stage is None or enrolled is None:
            return ("UNKNOWN", "Career stage or enrollment unknown.")
        return ("NOT MATCH", "Neither eligible research profession nor graduate enrollment confirmed.")
    if key == "degree_within_five_years":
        year = profile.get("latest_degree_year")
        applied = profile.get("application_year")
        if type(year) is not int or type(applied) is not int:
            return ("UNKNOWN", "Degree or application date missing.")
        age = applied - year
        if age < 0:
            return ("UNKNOWN", "Degree year occurs after application year; verify dates.")
        return (
            ("MATCH", f"Degree age {age} years.")
            if age <= 5
            else ("NOT MATCH", f"Degree age {age} years exceeds five-year limit.")
        )
    if key == "accepted_presentation":
        return boolean(
            profile.get("accepted_presentation"),
            "Accepted presentation declared.",
            "No accepted presentation declared.",
        )
    if key == "currently_enrolled_graduate":
        return boolean(
            profile.get("currently_enrolled_graduate"),
            "Graduate enrollment declared.",
            "Not currently enrolled in graduate program.",
        )
    if key == "dc_md_va":
        region = profile.get("region")
        if region is None:
            return ("UNKNOWN", "US state or region missing.")
        eligible = {"maryland", "md", "virginia", "va", "washington, dc", "district of columbia", "dc"}
        return (
            ("MATCH", "Profile region is within DC/MD/VA.")
            if str(region).strip().lower() in eligible
            else ("NOT MATCH", "Profile region lies outside DC/MD/VA.")
        )
    if key == "training_workshop":
        kind = profile.get("event_type")
        if kind is None:
            return ("UNKNOWN", "Event type missing.")
        return (
            ("MATCH", "Trip is a training workshop.")
            if kind == "training_workshop"
            else ("NOT MATCH", "Trip is not a training workshop.")
        )
    if key == "repo_mit_or_apache":
        lic = profile.get("software_license")
        if not lic:
            return ("UNKNOWN", "Software license is not verified.")
        return (
            ("MATCH", f"Software license declared: {lic}.")
            if str(lic).lower() in {"mit", "apache-2.0"}
            else ("NOT MATCH", f"Declared license {lic} is outside accepted list.")
        )
    if key == "current_postdoc":
        return boolean(
            profile.get("current_postdoc"),
            "Current postdoc appointment declared.",
            "No current postdoc appointment.",
        )
    if key == "international_host_invitation":
        return boolean(
            profile.get("international_host_invitation"),
            "International host invitation declared.",
            "International host invitation not supplied.",
        )
    if key == "outreach_project":
        kind = profile.get("project_type")
        if kind is None:
            return ("UNKNOWN", "Project type missing.")
        return (
            ("MATCH", "Public-facing outreach project.")
            if kind == "community_outreach"
            else ("NOT MATCH", "Project does not meet outreach type.")
        )
    if key == "request_at_most":
        request = profile.get("award_request_usd")
        if (
            type(request) not in (int, float)
            or not math.isfinite(request)
            or type(limit) is not int
            or limit < 0
        ):
            return ("UNKNOWN", "Request amount or evidence-based limit unavailable.")
        if request < 0:
            return ("UNKNOWN", "Invalid negative request.")
        return (
            ("MATCH", f"Requested ${request:,.0f} <= ${limit:,.0f} cap.")
            if request <= limit
            else ("NOT MATCH", f"Requested ${request:,.0f} exceeds ${limit:,.0f} cap.")
        )
    return ("UNKNOWN", "Criterion requires manual interpretation; no supported deterministic rule.")


# The model must quote exact spans. No fuzzy matching or fabricated quote correction.
def validate_extraction(extraction: Extraction, source: str) -> Extraction:
    for requirement in extraction.requirements:
        if requirement.source_quote not in source:
            raise ValueError(
                f"Unverified source quotation for {requirement.key}: {requirement.source_quote!r}"
            )
        if requirement.key == "request_at_most":
            if requirement.threshold_usd is None:
                raise ValueError("Amount cap missing from extracted award request requirement")
            # Parse complete USD tokens; never accept 100 from $1,100 or 100.50.
            amounts = re.findall(
                r"(?<![\w.,-])(?:\$|USD\s*)(-?\d[\d,]*(?:\.\d+)?)(?!\d|[.,]\d)", requirement.source_quote
            )
            if not amounts or any(float(x.replace(",", "")) < 0 for x in amounts):
                raise ValueError("Invalid or missing USD amount cap in source quote")
            if float(requirement.threshold_usd) not in [float(x.replace(",", "")) for x in amounts]:
                raise ValueError("Amount cap not supported by exact source quote")
        elif requirement.threshold_usd is not None:
            raise ValueError("Amount cap supplied for a non-money requirement")
    if not extraction.requirements:
        raise ValueError("No extractable requirements; manual review required")
    return extraction


def clause_matches(actual: ExtractedRequirement, reference: ExtractedRequirement) -> bool:
    """Strict clause identity for synthetic calls; not a general semantic verifier."""
    return (
        actual.key == reference.key
        and actual.source_quote == reference.source_quote
        and actual.threshold_usd == reference.threshold_usd
        and actual.mandatory == reference.mandatory
    )


def assess(
    extraction: Extraction,
    profile: dict,
    source: str,
    *,
    mode: str,
    model_name: str | None = None,
    needs_clause_review: bool = False,
    expected_keys: list[str] | None = None,
    expected_requirements: Extraction | None = None,
) -> Report:
    validate_extraction(extraction, source)
    findings: list[Finding] = []
    expected = expected_requirements.requirements if expected_requirements is not None else None
    for req in extraction.requirements:
        status, reason = check(req.key, profile, req.threshold_usd)
        if expected is not None and not any(clause_matches(req, ref) for ref in expected):
            status, reason = (
                "UNKNOWN",
                "Extracted key, quote, cap or mandatory flag differs from the authored clause.",
            )
        if needs_clause_review:
            status = "UNKNOWN"
            reason = f"Custom call: model suggests {req.key}; verify the meaning and completeness with the sponsor."
        findings.append(
            Finding(
                key=req.key,
                requirement=req.source_quote,
                source_quote=req.source_quote,
                status=status,
                reason=reason,
                mandatory=req.mandatory or req.key == "unmapped" or expected is not None,
            )
        )
    if expected is not None:
        for ref in expected:
            if not any(clause_matches(req, ref) for req in extraction.requirements):
                findings.append(
                    Finding(
                        key=ref.key,
                        requirement="Required clause not reliably extracted",
                        source_quote=ref.source_quote,
                        status="UNKNOWN",
                        reason="Authored reference clause; not model output. Missing or mismatched extraction.",
                        mandatory=True,
                    )
                )
    if expected_keys is not None:
        present = [r.key for r in extraction.requirements if r.mandatory]
        for key in expected_keys:
            canonical = "request_at_most" if key.startswith("request_le_") else key
            if canonical not in present:
                findings.append(
                    Finding(
                        key=canonical,
                        requirement=f"Missing extracted criterion: {canonical}",
                        source_quote="[Not extracted; reference fixture indicates requirement exists]",
                        status="UNKNOWN",
                        reason="Extractor omitted a required clause.",
                        mandatory=True,
                    )
                )
    mandatory = [f for f in findings if f.mandatory]
    if needs_clause_review:
        verdict = "NEEDS VERIFICATION"
    elif any(f.status == "NOT MATCH" for f in mandatory):
        verdict = "NOT ELIGIBLE"
    elif needs_clause_review or not mandatory or any(f.status == "UNKNOWN" for f in mandatory):
        verdict = "NEEDS VERIFICATION"
    else:
        verdict = "ELIGIBLE BASED ON SUPPLIED EVIDENCE"
    return Report(
        verdict=verdict,
        findings=findings,
        model_name=model_name,
        extraction_mode=mode,
        reviewer_warning="Informational assessment, not an eligibility determination from a funder. Source text can be incomplete; confirm the official call and deadlines.",
    )


def safe_text(value: str) -> str:
    value = html.escape(value)
    return re.sub(r"([\\`*_{}\[\]()#+.!|>~-])", r"\\\1", value).replace("\n", " ")


def to_markdown(report: Report, source_name: str) -> str:
    text = [
        "# FundPilot AI — Funding Readiness Report",
        "",
        f"**Opportunity:** {safe_text(source_name)}",
        f"**Assessment:** {report.verdict}",
        f"**Extraction mode:** {report.extraction_mode}",
        f"**Model:** {safe_text(report.model_name or 'Not used')}",
        "",
        f"> {report.reviewer_warning}",
        "",
        "## Requirement evidence",
        "",
    ]
    for i, f in enumerate(report.findings, 1):
        text += [
            f"### {i}. {safe_text(f.requirement)}",
            f"- Status: **{f.status}**",
            f"- Mandatory: {f.mandatory}",
            f"- Source: {safe_text(f.source_quote)}",
            f"- Reason: {safe_text(f.reason)}",
            "",
        ]
    text += [
        "## Next steps",
        "",
        "Verify all UNKNOWN findings with the official sponsor; confirm that the pasted call is complete and current. Never treat this report as official approval.",
    ]
    return "\n".join(text) + "\n"
