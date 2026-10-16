"""Build an unfilled reviewer packet from hash-checked cached public paragraphs.

The packet contains no predictions or reference answers. Source text stays in ignored local storage.
"""

import hashlib
import json
from pathlib import Path


def main():
    refs = json.loads(Path("evaluation/model-size/references.json").read_text())
    retrieved = {
        c["id"]: c["retrieved_at_utc"]
        for c in json.loads(Path("evaluation/model-size/retrieval.json").read_text())
    }
    lines = [
        "# Blind source annotation packet",
        "",
        (
            "No human review has occurred. Do not consult reference answers or model predictions. "
            "Identify all conditions, exclusions, materials, financial restrictions and dependencies. "
            "Record exact spans, AND/OR/EXCEPT relationships, expected status and uncertainty. "
            "Historical selected excerpts do not establish whole-call completeness."
        ),
        "",
        "Fictional profile: " + json.dumps(refs["profile"]),
        "",
    ]
    for case in refs["cases"]:
        text = Path(f".source-cache/v04/{case['id']}.paragraphs.txt").read_text()
        assert hashlib.sha256(text.encode()).hexdigest() == case["source_sha256"]
        for i, passage in enumerate(case["passages"]):
            quote = text.splitlines()[passage["source_line"] - 1]
            assert hashlib.sha256(quote.encode()).hexdigest() == passage["passage_sha256"]
            lines += [
                f"## {case['id']} / passage {i + 1}",
                case["source_url"],
                "Snapshot retrieved UTC: " + retrieved[case["id"]],
                case["source_status"],
                passage["passage_sha256"],
                "",
                quote,
                "",
                "Reviewer: ______; category / criterion / span / relationship / expected status / uncertainty: ______",
                "",
            ]
    target = Path(".local-reports/model-size/blind-annotation-packet.md")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines))
    print(target)


if __name__ == "__main__":
    main()
