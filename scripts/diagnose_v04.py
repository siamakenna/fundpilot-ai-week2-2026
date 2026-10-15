"""Historical error accounting from saved predictions; no new model inference."""
import collections
import hashlib
import json
import re
from pathlib import Path
from fundpilot.realworld import Applicant, Label, analyze, candidates, segment


def main():
    all_results = []
    for split, folder in [('development','evidence/realworld-development/evaluation-v4'),('historical_holdout','evidence/realworld-heldout')]:
        rows=json.loads(Path(folder,'cases.json').read_text())
        c=collections.Counter();reason_counts=collections.Counter();details=[]
        for row in rows:
            lines=Path('.source-cache',row['id']+'.txt').read_text().splitlines()
            selected=[lines[g['source_line']-1] for g in row['reference']]
            assert all(hashlib.sha256(s.encode()).hexdigest()==g['passage_sha256'] for s,g in zip(selected,row['reference']))
            units=segment('\n'.join(selected)); c['passages']+=len(selected)
            c['segmentation_id_or_count_failures']+=int(len(units)!=len(selected))
            c['paragraphs_with_multiple_reference_keys']+=sum(len(g['keys'])>1 for g in row['reference'])
            for i,(text,g) in enumerate(zip(selected,row['reference'])):
                pred=next((p for p in row['predicted'] if p['id']==i),None)
                base=candidates(text);ref={(g['kind'],k) for k in g['keys']};predset={(pred['kind'],k) for k in pred['keys']} if pred else set()
                c['reference_tuples']+=len(ref);c['predicted_tuples']+=len(predset);c['true_positive']+=len(ref&predset)
                c['false_negative_tuples']+=len(ref-predset);c['false_positive_tuples']+=len(predset-ref)
                c['category_errors']+=int(not pred or pred['kind']!=g['kind'])
                c['named_reference_keys_outside_candidates']+=len(set(g['keys'])-{'unknown'}-set(base['keys']))
                c['unknown_reference_tuples']+=g['keys'].count('unknown')
                exclusion=g['kind']=='exclusion';c['exclusion_passages']+=exclusion
                c['exclusion_kind_misses']+=int(exclusion and (not pred or pred['kind']!='exclusion'))
                compound=bool(re.search(r'\b(and|or|except|unless|if)\b',text,re.I))
                c['compound_cue_passages']+=compound;c['compound_passages_with_tuple_errors']+=int(compound and ref!=predset)
                temporal=bool(re.search(r'\b(before|after|previous|prior|deadline|following|years?|months?|202[0-9])\b',text,re.I))
                c['temporal_scope_cue_passages']+=temporal;c['temporal_passages_with_tuple_errors']+=int(temporal and ref!=predset)
                c['model_rule_category_disagreements']+=int(pred is not None and pred['kind']!=base['kind'])
                c['model_rule_key_disagreements']+=int(pred is not None and set(pred['keys'])!=set(base['keys']))
                if ref!=predset:details.append({'case':row['id'],'passage':i,'source_line':g['source_line'],'missing':sorted(ref-predset),'extra':sorted(predset-ref)})
            r=analyze('\n'.join(selected),Applicant(career_stage='Graduate student',membership=True,first_author=False,presenting_author=True,abstract_submitted=True,in_person=True,registration=False,upfront_costs=True),labels=[Label(**p) for p in row['predicted']])
            for f in r['findings']:
                if f['key']!='scope_review':c['outcome_'+f['status']]+=1;reason_counts[f['reason']]+=1
        all_results.append({'split':split,'counts':dict(c),'unknown_reason_counts':dict(reason_counts),'tuple_errors':details})
    original=json.loads(Path('evaluation/annotations-development.json').read_text())
    revised=json.loads(Path('evaluation/annotations-development.adjudicated-v2.json').read_text())
    changed=sum(x!=y for a,b in zip(original['cases'],revised['cases']) for x,y in zip(a['clauses'],b['clauses']))
    out={'method':'Deterministic accounting/replay of saved v4/old-heldout labels; no inference or historical rescore against revised labels. Cue groups overlap and are not causal diagnoses.','annotation_records_changed_in_proposed_v2':changed,'results':all_results}
    Path('evidence/v04/historical-diagnostics.json').write_text(json.dumps(out,indent=2)+'\n')
    for r in all_results:print(r['split'],json.dumps(r['counts']))

if __name__=='__main__': main()
