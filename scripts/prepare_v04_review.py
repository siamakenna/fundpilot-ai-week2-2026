"""Create a private blind development packet, without predictions or proposed labels."""
import hashlib
import json
from pathlib import Path

from scripts.evaluate_v04 import source_for


def main():
    manifest=json.loads(Path('evaluation/v04/annotations-development.json').read_text())
    retrieval={r['id']:r for r in json.loads(Path('evaluation/v04/retrieval-development.json').read_text())}
    lines=['# Independent human annotation packet — development sources only','',
        'Target: 20–30 minutes. Ten selected paragraphs from three organizers, not full-page coverage.',
        'No reviewer has yet completed this packet. Do not consult FundPilot predictions, prior labels or AI audits.',
        'Use only the source and its context. List EVERY atomic condition, then identify dependencies and ambiguity.',
        'Do not infer eligibility or current opening status. Source dates may refer to expired 2026 opportunities.',
        'Reviewer name/pseudonym: ____  Date: ____  Domain experience: ____',
        'Consent to attribution (yes/no): ____  Consent to publish annotation/rationale (yes/no): ____',
        'If uncertain, record disagreement and confidence; never guess. Keep private applicant information out of this packet.','',
        '## Schema',
        'Kinds: eligibility (positive applicant requirement); exclusion (bar); required_material; funding_condition (applicant request/expense limit); deadline (binding date); sponsor_benefit (award provided); informational; unclear.',
        'Relations: NONE, AND, OR, EXCEPT, CONDITIONAL, UNRESOLVED. Quote the source supporting each dependency.',
        'For each atom record: kind, descriptive criterion, exact evidence start/end character offsets, operator/value if explicit, applicability, relationship/dependency evidence, confidence and rationale.',
        'A stipend or maximum award is not automatically a cap on an applicant request. A supported literal quote does not prove semantic completeness.',
        'Compare only the following fictional declared profile when an unambiguous literal rule permits it: '+json.dumps(manifest['profile']),
        'Comparison labels: MATCH (supported declared fact), NOT MATCH (supported contradiction), UNKNOWN (missing fact/scope/unsupported), INFO (non-applicant-comparison information). None means official eligibility.','']
    for case in manifest['cases']:
        source_for(case) # verify original snapshot and passage hashes
        path=Path('.source-cache/v04')/(case['id']+'.paragraphs.txt')
        body=path.read_text();all_lines=body.splitlines()
        row=retrieval[case['id']]
        lines += ['## '+case['id'],case['source_url'],'Retrieved UTC: '+row['retrieved_at_utc'],
                  'Normalized snapshot SHA-256: '+hashlib.sha256(body.encode()).hexdigest(),'']
        for index,p in enumerate(case['passages']):
            i=p['source_line']-1;quote=all_lines[i]
            lines += [f'### Passage {index+1} · source line {i+1}',
                'Passage SHA-256: '+p['passage_sha256'],f'Local passage offsets: [0:{len(quote)}] (Python Unicode characters).',
                'Preceding context (may be a heading; determine scope yourself): '+(all_lines[i-1] if i else ''),
                '',quote,'','Following context: '+(all_lines[i+1] if i+1<len(all_lines) else ''),'',
                '| Atom | Kind / criterion | Evidence offsets | Operator/value | Applicability / relationship | Comparison / rationale |',
                '|---|---|---|---|---|---|','| 1 | | | | | |','',
                'Additional atoms: ____  Unresolved interpretation: ____  Confidence: ____','']
    dest=Path('.local-reports/v04/blind-human-review-development.md')
    if dest.exists():raise ValueError('Refuse to overwrite completed reviewer work')
    dest.write_text('\n'.join(lines))
    print(dest)

if __name__=='__main__':main()
