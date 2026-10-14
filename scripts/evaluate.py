"""Six fresh LIVE requests, one per unchanged fictional opportunity; no adapter mocks."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics
import time
from urllib.request import urlopen

from fundpilot.fixtures import opportunities, profiles, reference_extraction
from fundpilot.gemma import extract, DEFAULT_MODEL
from fundpilot.logic import assess, to_markdown


def signature(r):
    return (r.get("key"), r.get("source_quote"), r.get("mandatory"), r.get("threshold_usd"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="evidence/evaluation")
    args = parser.parse_args()
    root = Path(args.output)
    root.mkdir(parents=True, exist_ok=False)
    rows = []
    for oid, op in opportunities().items():
        reference = reference_extraction(op)
        expected = Counter(signature(r.model_dump()) for r in reference.requirements)
        baseline = assess(reference, profiles()["alex_postgrad"], op["eligibility_text"], mode="reference")
        row = {
            "opportunity": oid,
            "profile": "alex_postgrad",
            "expected_verdict": baseline.verdict,
            "expected_clauses": len(reference.requirements),
            "source_sha256": hashlib.sha256(op["eligibility_text"].encode()).hexdigest(),
        }
        audit = root / f"{oid}.json"
        started = time.perf_counter()
        try:
            actual = extract(op["eligibility_text"], audit_path=audit)
            report = assess(
                actual,
                profiles()["alex_postgrad"],
                op["eligibility_text"],
                mode="live Gemma",
                model_name=DEFAULT_MODEL,
                expected_requirements=reference,
            )
            (root / f"{oid}.md").write_text(to_markdown(report, op["title"]))
            row.update(
                outcome="validated",
                verdict=report.verdict,
                unknown_findings=sum(f.status == "UNKNOWN" for f in report.findings),
            )
        except Exception as exc:
            row.update(
                outcome="failed", verdict=None, error=f"{type(exc).__name__}: {exc}", unknown_findings=None
            )
        row["seconds"] = round(time.perf_counter() - started, 3)
        raw = []
        if audit.exists():
            try:
                saved = json.loads(audit.read_text())
                for call in saved["calls"]:
                    if "response" not in call:
                        continue
                    parsed = json.loads(call["response"]["response"])
                    raw.append({**parsed, "source_quote": call["sentence"]})
            except (KeyError, ValueError, TypeError):
                pass
        predicted = Counter(signature(r) for r in raw if isinstance(r, dict))
        row.update(
            returned_clauses=len(raw),
            true_positive=sum((predicted & expected).values()),
            exact_quotes=sum(
                isinstance(r, dict)
                and isinstance(r.get("source_quote"), str)
                and bool(r["source_quote"])
                and r["source_quote"] in op["eligibility_text"]
                for r in raw
            ),
        )
        row["false_positive"] = len(raw) - row["true_positive"]
        row["false_negative"] = sum(expected.values()) - row["true_positive"]
        rows.append(row)
        print(json.dumps(row), flush=True)
        (root / "cases.json").write_text(json.dumps(rows, indent=2))
    tp = sum(r["true_positive"] for r in rows)
    returned = sum(r["returned_clauses"] for r in rows)
    expected = sum(r["expected_clauses"] for r in rows)
    summary = {
        "kind": "live local inference, development fixtures, no mocks, no retries",
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "model": DEFAULT_MODEL,
        "model_inventory": json.load(urlopen("http://127.0.0.1:11434/api/tags")),
        "ollama": json.load(urlopen("http://127.0.0.1:11434/api/version")),
        "attempts": len(rows),
        "validated": sum(r["outcome"] == "validated" for r in rows),
        "failed": sum(r["outcome"] == "failed" for r in rows),
        "unknown_verdicts": sum(r["verdict"] == "NEEDS VERIFICATION" for r in rows),
        "verdict_agreement": sum(r["verdict"] == r["expected_verdict"] for r in rows),
        "true_positive": tp,
        "returned": returned,
        "reference": expected,
        "precision": tp / returned if returned else None,
        "recall": tp / expected,
        "exact_quotes": sum(r["exact_quotes"] for r in rows),
        "latency_mean_seconds": statistics.mean(r["seconds"] for r in rows),
        "latency_median_seconds": statistics.median(r["seconds"] for r in rows),
        "latency_min_seconds": min(r["seconds"] for r in rows),
        "latency_max_seconds": max(r["seconds"] for r in rows),
        "cases": rows,
    }
    (root / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("cases", "model_inventory")}, indent=2))


if __name__ == "__main__":
    main()
