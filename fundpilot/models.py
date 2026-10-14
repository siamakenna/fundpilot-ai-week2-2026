"""Evidence-backed extraction and assessment data contracts."""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

RequirementKey = Literal[
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
]


class ExtractedRequirement(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    key: RequirementKey
    mandatory: bool = True
    source_quote: str = Field(min_length=8)
    summary: str = Field(min_length=8)
    threshold_usd: int | None = Field(default=None, ge=0)


class Extraction(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    requirements: list[ExtractedRequirement]


class Finding(BaseModel):
    key: str
    requirement: str
    source_quote: str
    status: Literal["MATCH", "NOT MATCH", "UNKNOWN"]
    reason: str
    mandatory: bool


class Report(BaseModel):
    verdict: Literal["NOT ELIGIBLE", "NEEDS VERIFICATION", "ELIGIBLE BASED ON SUPPLIED EVIDENCE"]
    findings: list[Finding]
    model_name: str | None = None
    extraction_mode: str
    reviewer_warning: str
