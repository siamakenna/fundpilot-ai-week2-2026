"""Retrieve versioned official snapshots without changing historical caches."""
import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from scripts.fetch_official_sources import Text


class ParagraphText(Text):
    """Derived view: collapse HTML source wrapping, retain structural boundaries."""
    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(re.sub(r"\s+", " ", data))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--split', choices=['development', 'final'], required=True)
    args = p.parse_args()
    if args.split == 'final' and not Path('evaluation/v04/candidate-freeze.json').exists():
        p.error('Freeze the candidate before accessing final eligibility bodies')
    cache = Path('.source-cache/v04')
    cache.mkdir(exist_ok=True, parents=True)
    records = []
    for row in json.loads(Path('evaluation/v04/source-split.json').read_text())['sources']:
        if row['split'] != args.split:
            continue
        dest = cache / (row['id'] + '.txt')
        if dest.exists():
            p.error('Refusing to overwrite original snapshot: ' + str(dest))
        raw = subprocess.check_output(['curl', '-fsSL', '--compressed', '--max-time', '45', row['url']])
        parser = Text()
        parser.feed(raw.decode('utf-8'))
        body = parser.text()
        if len(body) < 500:
            raise ValueError('Suspiciously short source response')
        normalized = ParagraphText()
        normalized.feed(raw.decode('utf-8'))
        paragraphs = normalized.text()
        (cache / (row['id'] + '.paragraphs.txt')).write_text(paragraphs)
        dest.write_text(body)
        (cache / (row['id'] + '.html')).write_bytes(raw)
        records.append({**row, 'retrieved_at_utc': datetime.now(timezone.utc).isoformat(), 'text_sha256': hashlib.sha256(body.encode()).hexdigest(), 'html_sha256': hashlib.sha256(raw).hexdigest(), 'characters': len(body), 'paragraphs_sha256': hashlib.sha256(paragraphs.encode()).hexdigest(), 'normalization': 'Derived view collapses whitespace inside HTML text nodes; structural paragraph breaks retained. Original HTML and text unchanged.'})
    Path(f'evaluation/v04/retrieval-{args.split}.json').write_text(json.dumps(records, indent=2)+'\n')
    print(json.dumps(records, indent=2))

if __name__ == '__main__':
    main()
