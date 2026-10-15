"""Publish diagnostic metadata while keeping full source/raw replies in ignored storage."""
import hashlib
import json
from pathlib import Path

ROOT=Path('.local-reports/v04')
DEST=Path('evidence/v04')
RUNS=['dev-A','dev-A-service-restored','dev-rules','dev-B','dev-B2','dev-B3','final-A','final-B','final-rules']


def main():
    DEST.mkdir(exist_ok=True,parents=True)
    manifest=[];results={}
    for name in RUNS:
        directory=ROOT/name
        result=json.loads((directory/'results.json').read_text())
        expected=2 if name.startswith('final') else 3
        if len(result['cases']) != expected:raise ValueError('Refuse to publish a partial run: '+name)
        results[name]=result
        (DEST/(name+'.json')).write_text(json.dumps(result,indent=2)+'\n')
        for p in sorted(directory.glob('*')):
            if p.is_file():
                manifest.append({'local_file':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    synthetic=json.loads((ROOT/'synthetic-live/results.json').read_text())
    (DEST/'synthetic-live.json').write_text(json.dumps(synthetic,indent=2)+'\n')
    for p in sorted((ROOT/'synthetic-live').glob('*')):
        manifest.append({'local_file':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (DEST/'private-evidence-manifest.json').write_text(json.dumps({'note':'Raw source-bearing evidence preserved locally, not published in full. No paths to personal documents.','files':manifest},indent=2)+'\n')
    lines=['# Atomic v0.4 evaluation — NO SHIP','',
      'The experimental inference upgrade does not meet the release gates. Keep it on its feature branch. Ship the separately tested onboarding with the unchanged v0.3 engine.','',
      'All results below are against coding-assistant provisional annotations, **not independently human-validated ground truth**. Ten development passages / 20 atoms / 3 organizers; eight reserved passages / 20 atoms / 2 different organizers. All three systems use the same preregistered (passage, kind, criterion) unit. Expanded vocabulary disadvantages the legacy schema. These scores do not replace historical scores or establish general accuracy.','',
      '| Split / system | TP / predicted / reference | Precision | Recall | F1 | Mandatory | Exclusion | Reports | Mean seconds/case |',
      '|---|---|---|---|---|---|---|---|---|']
    for split,prefix in [('Development','dev'),('Reserved final','final')]:
        for label,suffix in [('v0.3 Gemma','A-service-restored' if prefix=='dev' else 'A'),('Atomic B3','B3' if prefix=='dev' else 'B'),('Rules','rules')]:
            m=results[prefix+'-'+suffix]['metrics'];mandatory=m['mandatory_recall'];ex=m['exclusion_recall'];c=m['completion']
            lines.append(f"| {split} / {label} | {m['true_positive']} / {m['predicted']} / {m['reference']} | {format(m['precision'], '.2%') if m['predicted'] else 'undefined (0 predictions)'} | {m['recall']:.2%} | {m['f1']:.2%} | {mandatory['matched']}/{mandatory['reference']} | {ex['matched']}/{ex['reference']} | {c['complete']}/{c['cases']} | {m['latency_seconds']['mean']:.3f} |")
    lines += ['', '| Split / system | UNKNOWN / non-INFO | False supported MATCH / all MATCH | False supported NOT MATCH / all NOT MATCH | Exact source spans / proposed | Completed passages / total |', '|---|---|---|---|---|---|']
    for name in ['dev-A-service-restored','dev-B3','dev-rules','final-A','final-B','final-rules']:
        m=results[name]['metrics'];u=m['unknown'];s=m['source_spans'];p=m['passages'];c=m['status_counts']
        lines.append(f"| {name} | {u['count']}/{u['non_informational']} | {m['false_supported_positive']}/{c.get('MATCH',0)} | {m['false_supported_negative']}/{c.get('NOT MATCH',0)} | {s['exact']}/{s['proposed']} | {p['completed']}/{p['total']} |")
    lines += ['', 'Zero-denominator rates are undefined, not perfect safety. Raw JSON uses 0 as a computational sentinel for undefined precision; the table marks it explicitly. False-supported counts are disagreements with provisional reference comparison labels for ONE fictional profile, not confirmed real applicant eligibility errors. Kind accuracy uses the same matched/reference numerator and denominator; missing atoms count wrong. JSON files retain missing-atom counts and token totals.',
       '', '## Failures and limitations',
       '- Initial development A: 0/3 reports because Ollama was stopped. All three failures are preserved separately. Service-restored A uses unchanged inference; there were no reserved-test retries.',
       '- B1: 0/3 reports, rejected invented applicability/dependency text. B2: 0/3, rejected absent dependency spans. B3 keeps full original context beside numbered span proposals; duplicate or inconsistent conditions still reject reports.',
       '- A failed report contributes zero delivered predictions and all its references remain in recall. Validated partial passages and exact spans are diagnostic only, never delivered as a complete report.',
       '- Literal span accuracy is not semantic accuracy. Numbered-span selection structurally prevents model-written quotations; incorrect categories, omissions and duplicated conditions remain real failures.',
       '- Final model code and protocol froze at `083ab38` / manifest commit `e9972c2`, before reserved retrieval. Provisional final labels froze at `e8574ab` before predictions. No final-source tuning or retries.',
       '- Tiny convenience sample, related scientific funding domains, selected paragraphs rather than whole announcements, expanded criterion vocabulary, and non-independent annotations preclude general performance claims. No statistical superiority claim or closed-model comparison.',
       '- No larger model was downloaded; see [hardware and protocol](MODEL_AND_PROTOCOL.md). CPU wall time is measured; CPU utilization/energy and electricity cost are not. Metered inference fees: $0.',
       '', '## Supplied development regressions',
       f"Real local Gemma completed {sum(r['complete'] for r in synthetic['scenarios'])}/14 profile scenarios and met {sum(r['accepted_behavior'] for r in synthetic['scenarios'])}/14 defined behavior checks. Eleven distinct source texts were inferred once each; three repeated-text profile scenarios reused the same real extraction. No fixture or adapter response substituted for inference.",
       'These are development scenarios from an AI usability audit of the v0.3 rule baseline, not human-user evidence. See `evidence/v04/synthetic-live.json` for every result. Deterministic tests separately demonstrate what happens GIVEN supplied semantic proposals; they are not model accuracy tests.',
       '', '## Preserved evidence and human review',
       'All original benchmarks, references, fixtures, raw failures and v0.2/v0.3 demos remain unchanged. Historical development F1 stays Gemma 42.11% vs rules 62.50%; historical held-out F1 stays 34.48% vs 33.90%, using provisional annotations.',
       'New public JSON has classifications, offsets, hashes and denominators. Full official snapshots and raw source-bearing responses remain in `.source-cache/v04` and `.local-reports/v04`; `evidence/v04/private-evidence-manifest.json` fingerprints them. No failed attempt was discarded.',
       'The blind development review packet is prepared locally with URLs, retrieval dates, source hashes, context, schema and blank fields. No reviewer has completed it. The ISMB postdoc interpretation remains unresolved. Do not replace references with AI reconciliation proposals.',
       '', '## Decision',
       '**NO SHIP for v0.4 inference.** Completion, recall and practical regressions fail the gates; independent human review is also outstanding. **Ship onboarding only** after its separate browser, security, test and authentic-demo checks. This does not claim improved model accuracy.']
    Path('docs/v04/RESULTS.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
