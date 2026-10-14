import pytest
from fundpilot.fixtures import opportunities,profiles,reference_extraction,load_json
from fundpilot.logic import assess, validate_extraction, check
from fundpilot.models import Extraction, ExtractedRequirement

OPS=opportunities(); PEOPLE=profiles()

@pytest.mark.parametrize("case",load_json("expected_scenarios.json"))
def test_expected_scenarios(case):
    op=OPS[case["opportunity_id"]]; profile=PEOPLE[case["profile_id"]]
    extraction=reference_extraction(op)
    r=assess(extraction,profile,op["eligibility_text"],mode="reference",expected_keys=op["mandatory"])
    actual=r.verdict.replace(" ","_")
    assert actual==case["expected"]

def test_all_quotes_verifiable():
    for op in OPS.values():
        validate_extraction(reference_extraction(op),op["eligibility_text"])

def test_reject_hallucinated_quote():
    e=Extraction(requirements=[ExtractedRequirement(key="us_based",mandatory=True,
      source_quote="Applicants must have a NASA astronaut badge.",summary="Requires astronaut badge")])
    with pytest.raises(ValueError,match="Unverified"):
        validate_extraction(e,"Applicants must be based in the United States.")

def test_unknown_blocks_eligible():
    op=OPS["early_career_travel"]; profile=PEOPLE["casey_uncertain"]
    r=assess(reference_extraction(op),profile,op["eligibility_text"],mode="reference")
    assert r.verdict=="NEEDS VERIFICATION"

def test_missing_extracted_key_blocks_eligible():
    op=OPS["early_career_travel"]
    full=reference_extraction(op)
    partial=Extraction(requirements=full.requirements[:-1])
    r=assess(partial,PEOPLE["alex_postgrad"],op["eligibility_text"],mode="test",expected_keys=op["mandatory"])
    assert r.verdict=="NEEDS VERIFICATION"

def test_award_limit_requires_quote_evidence():
    e=Extraction(requirements=[ExtractedRequirement(key="request_at_most",mandatory=True,
        source_quote="The requested award must not exceed $1,000.",summary="Award cap $100",threshold_usd=100)])
    with pytest.raises(ValueError,match="not supported"):
        validate_extraction(e,"The requested award must not exceed $1,000.")

def test_unknown_profile_field():
    assert check("us_based",{})[0]=="UNKNOWN"

def test_uncertain_custom_requirements():
    op=OPS["early_career_travel"]
    r=assess(reference_extraction(op),PEOPLE["alex_postgrad"],op["eligibility_text"],mode="test",needs_clause_review=True)
    assert r.verdict=="NEEDS VERIFICATION"
