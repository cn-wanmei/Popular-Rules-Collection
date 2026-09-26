#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
POLICY=ROOT/'config/icon_v5_clients.yaml'

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--registry',required=True); ap.add_argument('--service-id',required=True); ap.add_argument('--client',default='minimalist'); ap.add_argument('--style')
    args=ap.parse_args(); registry=json.loads(Path(args.registry).read_text(encoding='utf-8'))
    if registry.get('schema')!='icon_registry_v5': raise SystemExit('not an icon_registry_v5 registry')
    if registry.get('release_status') in {'candidate','bootstrap'}: pass
    entry=next((x for x in registry.get('entries',[]) if x.get('service_id')==args.service_id),None)
    if not entry: raise SystemExit(f'unknown service: {args.service_id}')
    if entry.get('release_eligible') is not True: raise SystemExit(f'service not release eligible: {args.service_id}')
    policy=__import__('yaml').safe_load(POLICY.read_text(encoding='utf-8')) or {}
    style=args.style or (policy.get('preferred_style') or {}).get(args.client)
    if not style: raise SystemExit(f'no preferred style for client: {args.client}')
    if style not in registry.get('variants',[]): raise SystemExit(f'unsupported style: {style}')
    item=entry.get('variants',{}).get(style)
    if not item: raise SystemExit(f'missing variant: {args.service_id}:{style}')
    print(json.dumps({'service_id':args.service_id,'icon_identity':entry['icon_identity'],'style':style,'path':item['path'],'png':item.get('png',{}),'source_digest':entry.get('source',{}).get('digest')},ensure_ascii=False))
    return 0

if __name__=='__main__': raise SystemExit(main())