"""Reproduce the public-call workflow without the UI; no fixture defaults."""

import argparse
import json
from pathlib import Path

from .realworld import Applicant, analyze
from .verification import markdown


def main():
    p = argparse.ArgumentParser(description="Analyze a public funding announcement with local Gemma")
    p.add_argument("--source-file", required=True)
    p.add_argument("--source-url", default="")
    p.add_argument("--title", default="Public funding announcement")
    p.add_argument(
        "--profile-json", help="Optional developer profile file; the Gradio UI provides ordinary form fields"
    )
    p.add_argument("--mode", choices=["gemma", "rules"], default="gemma")
    p.add_argument("--output", required=True)
    p.add_argument("--audit", help="Raw model labels and timing; excludes source text and prompt")
    a = p.parse_args()
    profile = (
        Applicant.model_validate_json(Path(a.profile_json).read_text()) if a.profile_json else Applicant()
    )
    report = analyze(Path(a.source_file).read_text(), profile, mode=a.mode, audit_path=a.audit)
    Path(a.output).write_text(markdown(report, title=a.title, source_url=a.source_url))
    print(
        json.dumps(
            {"readiness": report["readiness"], "counts": report["counts"], "mode": a.mode, "output": a.output}
        )
    )


if __name__ == "__main__":
    main()
