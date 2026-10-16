"""Synthetic presentation regressions; these are not live model accuracy tests."""

from copy import deepcopy
from pathlib import Path

import pytest

from fundpilot import real_ui
from fundpilot.dossier import build_dossier, markdown
from fundpilot.realworld import Applicant, Label, analyze


def report(text, profile=None):
    return analyze(text, profile or Applicant(), mode="rules")


def test_no_mutation_or_promoted_warnings():
    r = report("Applicants must be members unless an exception applies. Awards provide $500.")
    before = deepcopy(r)
    d = build_dossier(r, Applicant())
    assert {"exclusion", "pathway", "money", "mixed"} <= {w["code"] for w in d["warnings"]}
    assert r == before
    assert not d["contradictions"]


def test_hidden_exclusion_visible_when_interpreter_calls_it_information():
    text = "Award recipients receive support. Previous winners may not apply unless invited."
    r = analyze(text, Applicant(), labels=[Label(id=0, kind="context", keys=["unknown"])])
    d = build_dossier(r, Applicant())
    assert any(w["code"] == "exclusion" for w in d["warnings"])
    assert d["passages"][0]["quote"] == text
    assert not d["contradictions"]
    assert "not verified interpretations" in markdown(r, Applicant())


def test_contradiction_separate_from_missing_fact():
    p = Applicant(first_author=False)
    r = report("Applicants must be first author.\nApplicants must be the presenter.", p)
    d = build_dossier(r, p)
    assert len(d["contradictions"]) == 1
    assert [f["field"] for f in d["missing"]] == ["presenting_author"]
    assert "Check the designated presenter" in markdown(r, p)


def test_ambiguity_does_not_fabricate_missing_fact():
    p = Applicant(membership=True)
    d = build_dossier(report("Members may apply unless they received a prior award.", p), p)
    assert not d["missing"]
    assert d["warnings"]


def test_unknown_amount_not_zero():
    r = report("Applicants may request up to $500.")
    d = build_dossier(r, Applicant())
    assert any(f["field"] == "request_amount" for f in d["missing"])


def test_stipend_not_applicant_cap():
    r = report("The award provides a $500 stipend.")
    d = build_dossier(r, Applicant())
    assert not d["missing"] and not d["contradictions"]
    assert "award benefit" in markdown(r, Applicant())


def test_materials_dates_and_roles_are_review_labels():
    text = "Submit a CV and letter by October 18, 2026. Notification: November 2, 2026."
    md = markdown(report(text), Applicant())
    assert "Possible application materials" in md
    assert "October 18, 2026" in md and "November 2, 2026" in md
    assert "roles are heuristic review labels" in md
    assert "confirm the cycle, role and timezone" in md


def test_no_dates_or_documents_invented():
    md = markdown(report("Applicants must be members."), Applicant())
    assert "No supported explicit date with year identified" in md
    assert "No targeted document or monetary cue identified" in md
    assert "CV" not in md


def test_duplicate_questions_group_all_references():
    r = report("Applicants may request $200.\nThe award provides $500.")
    questions = build_dossier(r, Applicant())["questions"]
    money = [q for q in questions if q["question"].startswith("Is this an award benefit")]
    assert len(money) == 1 and money[0]["passages"] == [0, 1]


def test_complete_source_recommendation_always_present():
    md = markdown(
        report("Applicants must be first author.", Applicant(first_author=True)), Applicant(first_author=True)
    )
    assert "Pasted excerpts cannot establish completeness" in md
    assert "No supported contradiction" in md


def test_evidence_offsets_and_html_escaping():
    text = "<script>alert(1)</script>\nApplicants must be members unless invited."
    r = report(text)
    md = markdown(r, Applicant(), title="<img src=x>", source_url="javascript:alert(1)")
    assert "<script>" not in md and "<img" not in md
    assert "](" not in md.split("**Source:**")[1].split("\n")[0]
    for p in build_dossier(r, Applicant())["passages"].values():
        assert text[p["start"] : p["end"]] == p["quote"]
        assert f"Characters {p['start']}:{p['end']}" in md


@pytest.mark.parametrize(
    "text,code",
    [
        ("Applicants are ineligible unless invited.", "exclusion"),
        ("who have not received any other sources of funding", "exclusion"),
        ("Only one award within three years.", "duration"),
        ("A member or trainee can apply.", "pathway"),
        ("See the full rules in the handbook.", "linked"),
    ],
)
def test_structural_cues(text, code):
    assert any(w["code"] == code for w in build_dossier(report(text), Applicant())["warnings"])


def test_ui_downloads_same_analysis_once(monkeypatch):
    calls = []

    def actual_rules(source, profile, **kwargs):
        calls.append(source)
        return analyze(source, profile, mode="rules")

    monkeypatch.setattr(real_ui, "analyze", actual_rules)
    result = real_ui.run_public_with_dossier(
        "Applicants must be members.",
        "Test",
        "",
        "Unknown",
        "",
        "USD",
        "Rule baseline (NO AI)",
        *(["Unknown"] * 9),
    )
    assert len(calls) == 1 and len(result) == 6
    assert Path(result[3]).read_text() == result[2]
    assert Path(result[5]).read_text() == result[4].replace("(#h-source-passage-", "(#source-passage-")
    assert "## Evidence and checks" in result[2]
    assert all(f"## {letter}." in result[4] for letter in "ABCDE")


@pytest.mark.parametrize("amount", ["-1", "NaN", "abc"])
def test_invalid_input_clears_both_outputs(amount):
    r = real_ui.run_public_with_dossier(
        "Applicants must be members.",
        "Test",
        "",
        "Unknown",
        amount,
        "USD",
        "Live local Gemma",
        *(["Unknown"] * 9),
    )
    assert r[0].startswith("## Analysis unavailable")
    assert r[2:] == ("", None, "", None)


def test_failed_model_clears_dossier_without_fallback(monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("Model unavailable")

    monkeypatch.setattr(real_ui, "analyze", fail)
    r = real_ui.run_public_with_dossier(
        "Applicants must be members.", "", "", "Unknown", "", "USD", "Live local Gemma", *(["Unknown"] * 9)
    )
    assert r[2:] == ("", None, "", None)
    assert real_ui.clear_dossier()[2:] == ("", None, "", None)


def test_attribution_link_is_safe_and_resolves_without_markdown_escapes():
    r = report("Applicants must be members.")
    md = markdown(r, Applicant(), source_url="https://www.example.org/travel-award/?x=(1)")
    assert "[Official source](https://www.example.org/travel-award/?x=%281%29)" in md
    assert "No valid HTTP(S)" in markdown(r, Applicant(), source_url="javascript:alert(1)")
    assert "No valid HTTP(S)" in markdown(r, Applicant(), source_url="https://[")
