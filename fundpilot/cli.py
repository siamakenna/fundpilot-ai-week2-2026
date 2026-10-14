"""Command line demo: curated (offline) vs real Gemma (localhost)."""
import argparse
from pathlib import Path
from .fixtures import opportunities, profiles, reference_extraction
from .logic import assess, to_markdown
from .gemma import extract, DEFAULT_MODEL

def main():
    p = argparse.ArgumentParser(description="FundPilot AI source-grounded funding readiness demo")
    p.add_argument("--profile",default="alex_postgrad")
    p.add_argument("--opportunity",default="early_career_travel")
    p.add_argument("--mode",choices=["fixture","gemma"],default="fixture")
    p.add_argument("--model",default=DEFAULT_MODEL)
    p.add_argument("--output",default="fundpilot_report.md")
    a=p.parse_args()
    op=opportunities()[a.opportunity]; profile=profiles()[a.profile]
    source=op["eligibility_text"]
    extraction=reference_extraction(op) if a.mode=="fixture" else extract(source,a.model)
    report=assess(extraction,profile,source,mode="curated fictional reference (NO model)" if a.mode=="fixture" else "live Gemma",
                  model_name=a.model if a.mode=="gemma" else None,
                  expected_keys=op["mandatory"])
    Path(a.output).write_text(to_markdown(report,op["title"]),encoding="utf-8")
    print(f"{report.verdict} — {len(report.findings)} criteria — wrote {a.output}")
    if a.mode=="fixture":
        print("NOTE: No AI inference was performed; this is a reference evaluator test only.")
if __name__=="__main__": main()
