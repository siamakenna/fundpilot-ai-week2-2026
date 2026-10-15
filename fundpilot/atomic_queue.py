"""Experimental grouped verification tasks; no sponsor answers or eligibility verdicts."""
import re

from .logic import safe_text
from .verification import verification_queue


def tasks(report):
    prepared = {**report,'findings':[
        dict(f,quote=f['passage_quote'],start=f['passage_start'],end=f['passage_end'])
        for f in report['findings']]}
    grouped = {}
    for item in verification_queue(prepared):
        blocker = 'exclusion' in item['kinds'] or re.search(r'not eligible|cannot apply|may not reapply|ineligible',item['quote'],re.I)
        if blocker and 'NOT MATCH' not in item['statuses']:
            item.update(priority=1,label='Potential blocker — verify')
            item['question']='Does this exclusion apply to my specific role or award history? Which dates, exceptions and evidence determine whether I can apply?'
        elif any(f['id']==item['id'] and f['relation'] in ('OR','EXCEPT','CONDITIONAL','UNRESOLVED') for f in report['findings']):
            item['question']='Which alternative or conditional pathway applies to me? What membership duration, career-stage timing or other facts and evidence does that pathway require?'
        key=(item['priority'],item['label'],item['action'],item['question'])
        grouped.setdefault(key,[]).append(item)
    return sorted(grouped.items(),key=lambda entry:entry[0][0])


def markdown(report):
    lines=['## Prioritized verification tasks','',
           'Fixed-rule suggestions, not sponsor answers. Related questions are grouped; every underlying passage and criterion remains below.','']
    for (priority,label,action,question),items in tasks(report):
        lines += [f'### Priority {priority} · {label}',action,'**Ask:** '+question]
        for item in items:
            lines += [f"- Passage {item['id']+1}, criteria: {safe_text(', '.join(item['criteria']))}. Exact evidence [{item['start']}:{item['end']}]: {safe_text(item['quote'])}"]
    lines += ['', 'Always verify the complete source, current cycle, dates, exceptions and linked policies. No matched checks certify eligibility.','']
    return '\n'.join(lines)
