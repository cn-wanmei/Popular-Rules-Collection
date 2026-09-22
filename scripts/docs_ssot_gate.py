#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'config' / 'service_primary.yaml'
MANIFEST = ROOT / 'generated' / 'manifest.json'
DOC_DIR = ROOT / 'docs' / 'rules'

try:
    import yaml
except Exception as exc:
    print(f'ERROR: PyYAML unavailable: {exc}', file=sys.stderr)
    sys.exit(2)

registry = yaml.safe_load(REGISTRY.read_text(encoding='utf-8')) or {}
services = registry.get('services', {})
manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
generated = manifest.get('files', [])
generated_paths = {item.get('file') for item in generated if item.get('file')}
clients = set(manifest.get('client_rule_directories', []))

legacy_markers = (
    'generated/' + 'sing-box',
    'generated/' + 'quantumult-x',
    'database/' + 'domains/',
    'scripts/' + 'generate_docs.py',
    'scripts/' + 'generate_rule_pages.py',
)

legacy_service_prefix = 'database/' + 'services/'

errors = []
if clients != {'egern', 'loon', 'mihomo', 'quantumultx', 'shadowrocket', 'singbox', 'surge'}:
    errors.append(f'unexpected client directory contract: {sorted(clients)}')

for service_id in sorted(services):
    doc = DOC_DIR / f'{service_id}.md'
    if not doc.is_file():
        errors.append(f'missing current service doc: {doc.relative_to(ROOT)}')
        continue
    text = doc.read_text(encoding='utf-8', errors='strict')
    for marker in legacy_markers:
        if marker in text:
            errors.append(f'{doc.relative_to(ROOT)} contains forbidden legacy marker: {marker}')
    for line in text.splitlines():
        if legacy_service_prefix in line and not ('Legacy' in line or 'legacy' in line or '不是' in line or 'not' in line):
            errors.append(f'{doc.relative_to(ROOT)} uses database/services as a current reference: {line.strip()}')

    expected = []
    for item in generated:
        path = item.get('file', '')
        parts = path.split('/')
        if (item.get('scope') in clients and len(parts) == 4 and
                parts[0] in clients and parts[2] == service_id and
                parts[3].startswith('rules.')):
            expected.append(path)
    for path in sorted(set(expected)):
        if path not in text:
            errors.append(f'{doc.relative_to(ROOT)} does not mention materialized path: {path}')

    for candidate in re.findall(r'generated/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/rules\.(?:yaml|json|list)', text):
        if candidate not in generated_paths:
            errors.append(f'{doc.relative_to(ROOT)} references non-manifest generated path: {candidate}')

    if not re.search(r'Rule ID\s*\|\s*`' + re.escape(service_id) + r'`\s*\|', text):
        errors.append(f'{doc.relative_to(ROOT)} does not declare Rule ID {service_id}')

index = DOC_DIR / 'README.md'
if not index.is_file():
    errors.append('missing docs/rules/README.md')
else:
    index_text = index.read_text(encoding='utf-8', errors='strict')
    for service_id in sorted(services):
        if f'({service_id}.md)' not in index_text:
            errors.append(f'rules index missing current service link: {service_id}')

if errors:
    print('DOC SSOT GATE: FAIL')
    for err in errors[:200]:
        print(f'- {err}')
    if len(errors) > 200:
        print(f'- ... {len(errors)-200} more')
    sys.exit(1)

print(f'DOC SSOT GATE: PASS ({len(services)} configured services)')