"""Versioned, no-retry comparison on hash-checked local source snapshots.

Raw responses and copyrighted text remain ignored locally. Public evidence contains
hashes, offsets, classifications and metrics, never the full announcements.
"""
import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

from fundpilot.atomic import analyze_atomic, evidence_spans
from fundpilot.realworld import Applicant, Label, analyze, candidates, model_labels, segment

KIND = {'requirement':'eligibility', 'document':'required_material', 'funding_limit':'funding_condition',
        'award':'sponsor_benefit', 'optional':'informational', 'context':'informational'}
MANDATORY = {'eligibility','exclusion','required_material','funding_condition','deadline'}


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def source_for(case):
    text = Path(f'.source-cache/v04/{case["id"]}.paragraphs.txt').read_text()
    if digest(text) != case['source_sha256']:
        raise ValueError('Snapshot hash changed: '+case['id'])
    passages = [text.splitlines()[p['source_line']-1] for p in case['passages']]
    if any(digest(t) != p['passage_sha256'] for t,p in zip(passages,case['passages'],strict=True)):
        raise ValueError('Passage hash changed')
    return '\n'.join(passages)


def metrics(rows):
    refs, preds, matched = Counter(), Counter(), Counter()
    statuses = Counter()
    false = Counter()
    kind_correct = 0
    for row in rows:
        r = Counter((row['id'], a['passage'], a['kind'], a['criterion']) for a in row['reference'])
        p = Counter((row['id'], a['passage'], a['kind'], a['criterion']) for a in row['predictions'])
        refs.update(r); preds.update(p); matched.update(r & p)
        kind_correct += sum((r & p).values())
        for f in row['findings']:
            statuses[f['status']] += 1
            if f['status'] in ('MATCH','NOT MATCH'):
                aligned = [a for a in row['reference'] if (a['passage'],a['kind'],a['criterion']) == (f['passage'],f['kind'],f['criterion'])]
                if not aligned or not any(a['expected_status'] == f['status'] for a in aligned):
                    false[f['status']] += 1
    tp, pn, rn = sum(matched.values()),sum(preds.values()),sum(refs.values())
    def recall(kinds):
        return {'matched':sum(v for k,v in matched.items() if k[2] in kinds), 'reference':sum(v for k,v in refs.items() if k[2] in kinds)}
    noninfo = sum(v for k,v in statuses.items() if k != 'INFO')
    return {'true_positive':tp,'predicted':pn,'reference':rn,'precision':tp/pn if pn else 0,
        'recall':tp/rn if rn else 0,'f1':2*tp/(pn+rn) if pn+rn else 0,
        'reference_kind_accuracy':{'correct':kind_correct,'reference':rn},
        'mandatory_recall':recall(MANDATORY),'exclusion_recall':recall({'exclusion'}),
        'missing_reference_atoms':rn-tp,'false_supported_positive':false['MATCH'],
        'false_supported_negative':false['NOT MATCH'],'status_counts':dict(statuses),
        'unknown':{'count':statuses['UNKNOWN'],'non_informational':noninfo},
        'completion':{'complete':sum(r['complete'] for r in rows),'cases':len(rows)},
        'passages':{'completed':sum(r['completed_passages'] for r in rows),'total':sum(r['passages'] for r in rows)},
        'source_spans':{'exact':sum(r['exact_spans'] for r in rows),'proposed':sum(r['proposed_spans'] for r in rows)},
        'latency_seconds':{'total':round(sum(r['seconds'] for r in rows),3),'mean':round(sum(r['seconds'] for r in rows)/len(rows),3),'cases':len(rows)},
        'tokens':{'prompt':sum(r['prompt_tokens'] for r in rows),'generated':sum(r['generated_tokens'] for r in rows)},
        'metered_api_fees_usd':0,'electricity_cost':'not measured'}


def run(refs, variant, target, model='gemma3:1b'):
    target.mkdir(parents=True,exist_ok=False)
    rows = []
    profile = Applicant(**refs['profile'])
    for case in refs['cases']:
        source = source_for(case); units = segment(source)
        if len(units) != len(case['passages']):
            raise ValueError('Selected paragraphs do not match engine segmentation')
        row = {'id':case['id'],'input_sha256':digest(source),'passages':len(units),
               'reference':[dict(a,passage=i) for i,p in enumerate(case['passages']) for a in p['atoms']],
               'predictions':[],'findings':[],'complete':False,'completed_passages':0,
               'exact_spans':0,'proposed_spans':0,'prompt_tokens':0,'generated_tokens':0}
        tick = time.perf_counter(); audit_path = target/(case['id']+'-raw.json')
        print(f'{variant}: start {case["id"]}',flush=True)
        try:
            if variant == 'B':
                report = analyze_atomic(source,profile,model=model,audit_path=audit_path)
                row['predictions'] = [{'passage':f['id'],'kind':f['kind'],'criterion':f['key']} for f in report['findings']]
            else:
                labels = model_labels(units,audit_path=audit_path) if variant == 'A' else [Label(id=u['id'],kind=candidates(u['quote'])['kind'],keys=candidates(u['quote'])['keys']) for u in units]
                report = analyze(source,profile,mode='gemma' if variant=='A' else 'rules',labels=labels)
                row['predictions'] = [{'passage':l.id,'kind':KIND.get(l.kind,l.kind),'criterion':k} for l in labels for k in l.keys]
            row['findings'] = [{'passage':f['id'],'kind':KIND.get(f['model_kind'],f['model_kind']),
                                'criterion':f['key'],'status':f['status'],'start':f['start'],'end':f['end'],
                                'evidence_sha256':digest(f['quote'])} for f in report['findings'] if f['key']!='scope_review']
            row['complete'] = True; row['completed_passages'] = len(units)
            (target/(case['id']+'-report.json')).write_text(json.dumps(report,indent=2)+'\n')
            if variant != 'B':
                row['proposed_spans'] = len(row['predictions'])
                row['exact_spans'] = len(row['predictions'])
        except Exception as exc:
            # Full original error remains private. Public text could otherwise quote source or raw JSON.
            row['error_type'] = type(exc).__name__
            (target/(case['id']+'-error.txt')).write_text(str(exc))
        row['seconds'] = round(time.perf_counter()-tick,3)
        if audit_path.exists():
            audit = json.loads(audit_path.read_text())
            row['completed_passages'] = sum('error' not in c for c in audit['calls'])
            for call in audit['calls']:
                response = call.get('response',{})
                row['prompt_tokens'] += response.get('prompt_eval_count',0)
                row['generated_tokens'] += response.get('eval_count',0)
                if variant == 'B':
                    try:
                        proposed = json.loads(response.get('response',''))['atoms']
                        for atom in proposed:
                            row['proposed_spans'] += 1
                            span_id = atom.get('span_id')
                            spans = evidence_spans(units[call['passage_id']]['quote'])
                            quote = spans[span_id] if type(span_id) is int and 0 <= span_id < len(spans) else atom.get('evidence')
                            row['exact_spans'] += int(isinstance(quote,str) and bool(quote) and units[call['passage_id']]['quote'].count(quote)==1)
                    except (ValueError,KeyError,TypeError):
                        row['unparseable_calls'] = row.get('unparseable_calls',0)+1
        rows.append(row)
        print(f'{variant}: {case["id"]} complete={row["complete"]} {row["seconds"]}s',flush=True)
        result = {'variant':variant,'model':model if variant=='B' else ('gemma3:1b' if variant=='A' else None),
                  'annotation_status':refs['reviewer'],'metrics':metrics(rows),'cases':rows}
        (target/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--split',choices=['development','final'],required=True)
    p.add_argument('--variant',choices=['A','B','rules'],required=True)
    p.add_argument('--out',required=True);args=p.parse_args()
    if args.split=='final' and not Path('evaluation/v04/candidate-freeze.json').exists():
        p.error('Candidate must be frozen before final evaluation')
    refs=json.loads(Path(f'evaluation/v04/annotations-{args.split}.json').read_text())
    run(refs,args.variant,Path(args.out))

if __name__=='__main__':
    main()
