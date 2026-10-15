"""Short public CNS excerpt verified in v0.2.0; no predictions or fixture output."""

CNS_EXCERPT = (
    "Applicants must be the first author and presenter of a poster submitted for "
    "presentation at the CNS 2027 Annual Meeting."
)
CNS_URL = "https://www.cogneurosociety.org/travel-award/"
CNS_RETRIEVED = "2026-10-14"
CNS_SHA256 = "e27d9633aefe0d4538b36c6aab602f9e7a0d13ddbb53ddbfc782b3ddc951ad74"


def sample_inputs(question_keys):
    """Editable fictional facts, deliberately leaving presenter status unknown."""
    facts = {"first_author": "Yes"}
    return [
        CNS_EXCERPT,
        "CNS 2027 — short public excerpt; fictional applicant",
        CNS_URL,
        "Unknown",
        "",
        "USD",
        "Live local Gemma",
        *(facts.get(key, "Unknown") for key in question_keys),
    ]
