"""Retrieve official public pages into ignored local storage; never vendor pages.

Network fetch is a developer evaluation tool, not part of the user application.
Uses system curl with TLS verification and Python's standard HTML parser.
"""
import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.hidden=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','noscript'):self.hidden+=1
        if tag in ('p','li','br','h1','h2','h3','h4','tr','div'):self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript'):self.hidden=max(0,self.hidden-1)
        if tag in ('p','li','h1','h2','h3','h4','tr','div'):self.parts.append('\n')
    def handle_data(self,data):
        if not self.hidden:self.parts.append(data)
    def text(self):
        return '\n'.join(re.sub(r'\s+',' ',s).strip() for s in ''.join(self.parts).splitlines() if s.strip())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--split',choices=['development','holdout'],default='development');args=parser.parse_args()
    if args.split=='holdout' and not (ROOT/'evaluation/candidate-freeze.json').exists():
        parser.error('Freeze the candidate before retrieving held-out source bodies.')
    cache=ROOT/'.source-cache';cache.mkdir(exist_ok=True)
    records=[]
    for source in json.loads((ROOT/'evaluation/source_split.json').read_text())['sources']:
        if source['split']!=args.split:continue
        raw=subprocess.check_output(['curl','--compressed','--fail','--location','--silent','--show-error','--retry','2','--max-time','45',source['url']])
        decoded=raw.decode('utf-8')
        if '<html' not in decoded.lower(): raise ValueError('Response was not an HTML page: '+source['id'])
        text=Text();text.feed(decoded);body=text.text()
        (cache/(source['id']+'.txt')).write_text(body)
        records.append({**source,'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'text_sha256':hashlib.sha256(body.encode()).hexdigest(),'characters':len(body),'storage':'ignored local cache; not redistributed'})
    (ROOT/'evaluation'/('retrieval-'+args.split+'.json')).write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))

if __name__=='__main__':main()
