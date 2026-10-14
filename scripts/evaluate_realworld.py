"""One-pass live official-source evaluation; no fixtures, no model fallback."""

import argparse
import hashlib
import json
import statistics
import time
from pathlib import Path

from fundpilot.realworld import Applicant, Label, analyze, candidates, model_labels, segment

ROOT = Path(__file__).resolve().parents[1]


def metrics(rows):
    gold = set()
    pred = set()
    mandatory = set()
    categories = 0
    paragraphs = 0
    exclusions = 0
    exclusion_hits = 0
    for row in rows:
        for i, c in enumerate(row["reference"]):
            tuples = {(row["id"], i, c["kind"], k) for k in c["keys"]}
            gold |= tuples
            if c["mandatory"]:
                mandatory |= tuples
            paragraphs += 1
            match = next((p for p in row["predicted"] if p["id"] == i), None)
            categories += int(match is not None and match["kind"] == c["kind"])
            if c["kind"] == "exclusion":
                exclusions += 1
                exclusion_hits += int(match is not None and match["kind"] == "exclusion")
        for p in row["predicted"]:
            pred |= {(row["id"], p["id"], p["kind"], k) for k in p["keys"]}
    tp = len(gold & pred)
    precision = tp / len(pred) if pred else 0
    recall = tp / len(gold) if gold else 0
    return {
        "true_positive": tp,
        "predicted": len(pred),
        "reference": len(gold),
        "precision": precision,
        "recall": recall,
        "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0,
        "mandatory_matched": len(mandatory & pred),
        "mandatory_reference": len(mandatory),
        "mandatory_recall": len(mandatory & pred) / len(mandatory) if mandatory else 0,
        "category_correct": categories,
        "paragraphs": paragraphs,
        "exclusion_category_correct": exclusion_hits,
        "exclusion_paragraphs": exclusions,
        "unsupported_predictions": sum("unknown" in p["keys"] for r in rows for p in r["predicted"]),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--split", choices=["development", "holdout"], required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    out = ROOT / a.output
    out.mkdir(exist_ok=False, parents=True)
    if a.split == "holdout":
        freeze = json.loads((ROOT / "evaluation/candidate-freeze.json").read_text())
        assert (
            hashlib.sha256((ROOT / "fundpilot/realworld.py").read_bytes()).hexdigest()
            == freeze["realworld_sha256"]
        ), "Candidate changed after freeze"
        marker = ROOT / "evaluation/holdout-started.json"
        with marker.open("x") as f:
            json.dump({"output": a.output, "started": time.time()}, f)
    annotation = json.loads((ROOT / f"evaluation/annotations-{a.split}.json").read_text())
    live = []
    rules = []
    for case in annotation["cases"]:
        full = (ROOT / ".source-cache" / f"{case['id']}.txt").read_text()
        lines = full.splitlines()
        assert hashlib.sha256(full.encode()).hexdigest() == case["source_sha256"]
        selected = [lines[c["source_line"] - 1] for c in case["clauses"]]
        assert all(
            hashlib.sha256(s.encode()).hexdigest() == c["passage_sha256"]
            for s, c in zip(selected, case["clauses"])
        )
        source = "\n".join(selected)
        units = segment(source)
        base = [
            Label(id=u["id"], kind=candidates(u["quote"])["kind"], keys=candidates(u["quote"])["keys"])
            for u in units
        ]
        rules.append(
            {"id": case["id"], "reference": case["clauses"], "predicted": [x.model_dump() for x in base]}
        )
        row = {"id": case["id"], "reference": case["clauses"], "predicted": []}
        tick = time.perf_counter()
        try:
            labels = model_labels(units, audit_path=out / f"{case['id']}-audit.json")
            row["predicted"] = [x.model_dump() for x in labels]
            result = analyze(
                source,
                Applicant(
                    career_stage="Graduate student",
                    membership=True,
                    first_author=False,
                    presenting_author=True,
                    abstract_submitted=True,
                    in_person=True,
                    registration=False,
                    upfront_costs=True,
                ),
                labels=labels,
            )
            row.update(
                outcome=result["readiness"],
                counts=result["counts"],
                scope_review_items=sum(f["key"] == "scope_review" for f in result["findings"]),
                unsupported_or_uncertain_findings=sum(
                    f["status"] == "UNKNOWN" and f["key"] != "scope_review" for f in result["findings"]
                ),
            )
        except Exception as exc:
            row["error"] = str(exc)
        row["seconds"] = round(time.perf_counter() - tick, 3)
        live.append(row)
        (out / "cases.json").write_text(json.dumps(live, indent=2) + "\n")
        print(case["id"], row.get("outcome", "FAILED"), row["seconds"], flush=True)
    summary = {
        "split": a.split,
        "reviewer": annotation["reviewer"],
        "live_model": metrics(live),
        "rules_baseline": metrics(rules),
        "cases": len(live),
        "completed": sum("error" not in r for r in live),
        "failed": sum("error" in r for r in live),
        "latency_seconds": {
            "mean": statistics.mean(r["seconds"] for r in live),
            "min": min(r["seconds"] for r in live),
            "max": max(r["seconds"] for r in live),
        },
        "inference": "actual local Gemma; no retries or fixture substitutions",
        "scope": "Selected original paragraphs, not whole-document completeness or independently human-adjudicated eligibility accuracy",
    }
    (out / "baseline.json").write_text(json.dumps(rules, indent=2) + "\n")
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
