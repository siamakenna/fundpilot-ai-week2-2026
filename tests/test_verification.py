"""Presentation tests use rules/explicit labels, never claimed as live AI results."""

import hashlib
from copy import deepcopy
from pathlib import Path

import pytest

from fundpilot.quickstart import CNS_EXCERPT, CNS_SHA256, sample_inputs
from fundpilot.realworld import Applicant, Label, analyze
from fundpilot.verification import markdown, queue_markdown, verification_queue


def report(source, **facts):
    return analyze(source, Applicant(**facts), mode="rules")


def test_prioritized_deduplicated_queue_preserves_underlying_findings():
    source = "Applicants must be current members.\nApplicants must be the first author and presenter."
    result = report(source, first_author=False)
    before = deepcopy(result)
    result["findings"].append(deepcopy(result["findings"][1]))
    queue = verification_queue(result)
    assert [item["id"] for item in queue] == [1, 0]
    assert queue[0]["priority"] == 1
    assert queue[0]["criteria"] == ["first_author", "presenting_author"]
    assert queue[0]["statuses"] == ["NOT MATCH", "UNKNOWN"]
    assert len(queue[0]["reasons"]) == 2
    assert "Do not assume an exception" in queue[0]["action"]
    for item in queue:
        assert source[item["start"] : item["end"]] == item["quote"]
    markdown(result)
    result["findings"].pop()
    assert result == before


@pytest.mark.parametrize(
    "source",
    ["Applicants must be the first author.", "Applicants must not be US federal employees."],
)
def test_missing_fact_first_action_is_to_check_own_records(source):
    queue = verification_queue(report(source))
    assert len(queue) == 1
    assert "fill any known corresponding form facts" in queue[0]["action"]
    assert queue[0]["priority"] == 2


def test_exclusion_contradiction_is_not_an_eligibility_decision():
    result = report("Applicants must not be US federal employees.", us_federal_employee=True)
    item = verification_queue(result)[0]
    assert item["priority"] == 1
    assert "Does this prevent me from applying" in item["question"]
    assert result["readiness"] == "CONTRADICTIONS TO RESOLVE"


@pytest.mark.parametrize(
    "source",
    [
        "Applicants must be current members unless a waiver is granted.",
        "Applicants must be current members and cannot be presenters.",
    ],
)
def test_mixed_or_conditional_passage_asks_about_applicability(source):
    result = report(source, membership=True, presenting_author=True)
    queue = verification_queue(result)
    assert len(queue) == 1
    assert queue[0]["priority"] == 2
    assert "exclusions or exceptions" in queue[0]["question"]


def test_award_info_is_not_risk_or_invented_request_cap():
    result = report("The award is $500.\nRequests may not exceed $200.")
    queue = verification_queue(result)
    assert len(queue) == 1 and queue[0]["id"] == 1
    assert "award benefit or a limit" in queue[0]["question"]
    assert result["counts"]["INFO"] == 1


def test_model_rule_disagreement_requires_classification_clarification():
    source = "Applicants must be current members."
    result = analyze(
        source, Applicant(membership=True), labels=[Label(id=0, kind="award", keys=["membership"])]
    )
    item = verification_queue(result)[0]
    assert "mandatory" in item["question"]
    assert item["statuses"] == ["UNKNOWN"]


def test_all_match_does_not_drop_full_source_review():
    result = report(CNS_EXCERPT, first_author=True, presenting_author=True)
    assert verification_queue(result) == []
    assert "not eligibility approval" in queue_markdown(result)
    assert "linked policies" in queue_markdown(result)
    assert "scope_review" in {f["key"] for f in result["findings"]}


def test_queue_escapes_untrusted_source_title_url_and_reason():
    source = "Applicants must be first author. <script>alert(1)</script> [click](javascript:alert(1)) & *yes*"
    result = report(source)
    result["findings"][0]["reason"] = "<img src=x onerror=alert(1)> **approve**"
    output = markdown(result, title="<b>not trusted</b>", source_url="[click](javascript:alert(1))")
    assert "<script>" not in output and "<img" not in output and "<b>" not in output
    assert "[click](javascript:" not in output and "**approve**" not in output
    assert "&amp;" in output and "&lt;script&gt;" in output
    assert result["findings"][0]["quote"] == source


def test_top_three_and_full_numbered_report_keep_all_passages():
    source = "\n".join(["Applicants must be current members."] * 5)
    result = report(source)
    assert len(verification_queue(result)) == 5  # same words at distinct source positions
    assert "Showing 3 of 5" in queue_markdown(result, limit=3)
    full = markdown(result)
    assert "5. **Priority 2" in full
    assert full.index("## Questions") < full.index("## Evidence and checks")
    assert result["source_sha256"] in full


def test_sample_matches_preserved_demo_source_and_defaults_to_live():
    from fundpilot.real_ui import QUESTIONS

    values = sample_inputs(QUESTIONS)
    assert hashlib.sha256(CNS_EXCERPT.encode()).hexdigest() == CNS_SHA256
    assert CNS_EXCERPT in Path("evidence/public-ui/downloaded-report.md").read_text().replace("\\.", ".")
    assert values[6] == "Live local Gemma"
    assert values[4] == "" and "fictional" in values[1]
    answers = dict(zip(QUESTIONS, values[7:], strict=True))
    assert answers["first_author"] == "Yes" and answers["presenting_author"] == "Unknown"


def test_quickstart_uses_live_path_and_failed_inference_cannot_return_queue(monkeypatch):
    from fundpilot import real_ui

    seen = []

    def missing(source, profile, **kwargs):
        seen.append((source, profile, kwargs["mode"]))
        raise RuntimeError("model unavailable")

    monkeypatch.setattr(real_ui, "analyze", missing)
    output = real_ui.run_public(*sample_inputs(real_ui.QUESTIONS))
    assert seen[0][0] == CNS_EXCERPT and seen[0][2] == "gemma"
    assert seen[0][1].presenting_author is None
    assert output[3] is None and output[2] == "" and output[1] == []
    assert "Questions to verify" not in output[0]


def test_public_cli_download_includes_the_same_verification_queue(tmp_path, monkeypatch):
    from fundpilot.public_cli import main

    source, target = tmp_path / "source.txt", tmp_path / "report.md"
    source.write_text(CNS_EXCERPT)
    monkeypatch.setattr(
        "sys.argv", ["public_cli", "--source-file", str(source), "--output", str(target), "--mode", "rules"]
    )
    main()
    output = target.read_text()
    assert "## Questions to verify before applying" in output
    assert "First action" in output and "**Mode:** rules" in output
