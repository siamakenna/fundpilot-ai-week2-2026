"""Tester-requested presentation behavior, not model accuracy measurements."""

from copy import deepcopy

import pytest

from fundpilot.dossier import markdown
from fundpilot.presentation import overview, suggested_questions
from fundpilot.real_ui import QUESTIONS, question_visibility, run_public_with_dossier
from fundpilot.realworld import Applicant, analyze


@pytest.mark.parametrize(
    "profile,expected",
    [
        (Applicant(first_author=True), (1, 0, 0)),
        (Applicant(first_author=False), (0, 1, 0)),
        (Applicant(), (0, 0, 1)),
    ],
)
def test_overview_counts_are_original_findings(profile, expected):
    r = analyze("Applicants must be first author.", profile, mode="rules")
    original = deepcopy(r)
    text = overview(r, profile)
    assert f"**{expected[0]} MATCH**" in text
    assert f"**{expected[1]} NOT MATCH**" in text
    assert f"**{expected[2]} UNKNOWN**" in text
    assert r == original


def test_possible_exclusion_is_not_promoted_to_problem():
    r = analyze("Applicants must be members unless invited.", Applicant(membership=True), mode="rules")
    text = overview(r, Applicant(membership=True))
    assert "**0 NOT MATCH**" in text
    assert "Source-review flags — provisional" in text
    assert "Possible exclusion or exception" in text


def test_missing_fact_action_and_complete_dossier_preserved():
    p = Applicant()
    r = analyze("Applicants must be the presenter.", p, mode="rules")
    assert "check and update Presenting author" in overview(r, p)
    assert all(f"## {s}." in markdown(r, p) for s in "ABCDE")


def test_suggested_questions_follow_text_not_url_or_model():
    assert suggested_questions("Applicants must be first author and presenter.", QUESTIONS) == {
        "first_author",
        "presenting_author",
    }
    assert suggested_questions("Unrecognized conditions.", QUESTIONS) == set()
    assert set(suggested_questions("", QUESTIONS)) == {"membership", "first_author", "presenting_author"}


def test_show_all_never_changes_hidden_answer_values():
    all_updates = question_visibility("Applicants must be first author.", True)
    assert len(all_updates) == 9 and all(u["visible"] for u in all_updates)
    suggested = question_visibility("Applicants must be first author.", False)
    assert sum(u["visible"] for u in suggested) == 1
    assert all("value" not in u and "interactive" not in u for u in all_updates + suggested)


def test_url_only_does_not_fetch_or_infer(monkeypatch):
    from fundpilot import realworld

    def forbidden(*args, **kwargs):
        pytest.fail("URL-only input attempted model/network retrieval")

    monkeypatch.setattr(realworld, "model_labels", forbidden)
    r = run_public_with_dossier(
        "", "", "https://example.org", "Unknown", "", "USD", "Live local Gemma", *(["Unknown"] * 9)
    )
    assert "Analysis unavailable" in r[0]
    assert r[2:] == ("", None, "", None)


@pytest.mark.parametrize(
    "error", [ConnectionError("Ollama connection refused"), ValueError("Malformed model JSON")]
)
def test_transport_and_schema_failures_clear_every_output(monkeypatch, error):
    from fundpilot import real_ui

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(real_ui, "analyze", fail)
    r = real_ui.run_public_with_dossier(
        "Applicants must be first author.",
        "",
        "",
        "Unknown",
        "",
        "USD",
        "Live local Gemma",
        *(["Unknown"] * 9),
    )
    assert "Analysis unavailable" in r[0]
    assert r[1:] == ([], "", None, "", None)
