"""Synthetic fixtures for deterministic demonstrations; these are not model outputs."""
import json
from pathlib import Path
from .models import Extraction, ExtractedRequirement

ROOT = Path(__file__).resolve().parents[1]

def load_json(name: str):
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))

def opportunities():
    return {x["id"]: x for x in load_json("fictional_opportunities.json")}

def profiles():
    return {x["id"]: x for x in load_json("fictional_profiles.json")}

def reference_extraction(opportunity: dict) -> Extraction:
    """Curated, human-readable ground truth — NEVER portray as an AI output."""
    import re
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", opportunity["eligibility_text"]) if s.strip()]
    keys = opportunity["mandatory"]
    if len(sentences) != len(keys):
        raise ValueError(f"Fixture has {len(sentences)} sentences and {len(keys)} keys")
    items = []
    for key, sentence in zip(keys, sentences):
        limit = None
        if key.startswith("request_le_"):
            limit = int(key.rsplit("_",1)[1]); key = "request_at_most"
        items.append(ExtractedRequirement(key=key, mandatory=True, source_quote=sentence,
                                          summary=sentence, threshold_usd=limit))
    return Extraction(requirements=items)
