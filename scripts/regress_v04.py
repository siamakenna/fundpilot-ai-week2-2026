"""Run the supplied development regressions through real local Gemma once per distinct text."""
import hashlib
import json
from pathlib import Path

from fundpilot.atomic import analyze_atomic, extract
from fundpilot.atomic_queue import tasks
from fundpilot.realworld import Applicant


def accepted(case, report):
    c=report['counts'];findings=report['findings'];name=case['id']
    if name=='first_author_presenter_yes':return c['MATCH']==2
    if name=='first_author_no':return c['NOT MATCH']==1 and c['MATCH']==1
    if name=='presenter_unknown':return any(f['key']=='presenting_author' and f['status']=='UNKNOWN' and 'records' in f['reason'] for f in findings)
    if name=='conditional_membership_or':return c['MATCH']==c['NOT MATCH']==0 and any(f['relation']=='OR' for f in findings)
    if name=='duration_and_membership_exception':return c['MATCH']==c['NOT MATCH']==0 and any(f['relation']=='EXCEPT' for f in findings)
    if name=='explicit_research_scientist_exclusion':return c['NOT MATCH']==0 and any(key[0]==1 for key,_ in tasks(report))
    if name=='past_recipient_wait':return c['MATCH']==c['NOT MATCH']==0 and any(f['kind']=='exclusion' for f in findings)
    if name.startswith('sponsor_'):return c['NOT MATCH']==0 and any(f['kind']=='sponsor_benefit' for f in findings)
    if name=='explicit_request_cap_exceeded':return c['NOT MATCH']==1
    if name=='explicit_request_cap_currency_mismatch':return c['NOT MATCH']==c['MATCH']==0
    if name=='mixed_eligibility_and_exclusion':return {'eligibility','exclusion'} <= {f['kind'] for f in findings}
    if name=='deadline_and_required_material':return {'deadline','required_material'} <= {f['kind'] for f in findings}
    if name=='untrusted_source_instruction':return c['MATCH']==c['NOT MATCH']==0
    raise ValueError(name)


def main():
    dest=Path('.local-reports/v04/synthetic-live');dest.mkdir(exist_ok=False)
    cache={};rows=[]
    for case in json.loads(Path('evaluation/v04/regression-cases.json').read_text())['cases']:
        source=case['source_text'];sha=hashlib.sha256(source.encode()).hexdigest()
        row={'id':case['id'],'source_sha256':sha,'complete':False,'accepted_behavior':False}
        if sha not in cache:
            try:cache[sha]=extract(source,audit_path=dest/(sha+'-raw.json'))
            except Exception as exc:cache[sha]=str(exc)
        atoms=cache[sha]
        if isinstance(atoms,str):row['error']=atoms
        else:
            report=analyze_atomic(source,Applicant(**case['applicant_facts']),atoms=atoms)
            (dest/(case['id']+'-report.json')).write_text(json.dumps(report,indent=2)+'\n')
            row.update(complete=True,accepted_behavior=accepted(case,report),counts=report['counts'],
                       proposed_kinds=[f['kind'] for f in report['findings']],relations=[f['relation'] for f in report['findings']])
        rows.append(row)
        print(case['id'],row['complete'],row['accepted_behavior'],flush=True)
        (dest/'results.json').write_text(json.dumps({'mode':'LIVE local Gemma 3 1B; no adapter mocks','inference_calls':len(cache),'scenarios':rows},indent=2)+'\n')

if __name__=='__main__':main()
