#!/usr/bin/env python3
"""Fetch and verify the stable Universal-Rules-Collection client input."""
from __future__ import annotations
import argparse, hashlib, json, urllib.request
from pathlib import Path

REQUIRED={"id","kind","pattern","action","source","sources","provenance","category","popularity_score"}
ALLOWED={"DIRECT","PROXY","REJECT","REJECT-DROP","REJECT-TINYGIF","PASS","NO-RESOLVE"}

def fetch(url: str) -> bytes:
    req=urllib.request.Request(url,headers={"User-Agent":"Popular-Rules-Collection/universal-sync/1"})
    with urllib.request.urlopen(req,timeout=30) as r: return r.read()

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--manifest-url",required=True); ap.add_argument("--input-url",required=True); ap.add_argument("--output-dir",default="data/upstream/universal"); a=ap.parse_args()
    manifest=json.loads(fetch(a.manifest_url).decode())
    raw=fetch(a.input_url)
    checksum=hashlib.sha256(raw).hexdigest()
    if checksum != manifest.get("checksum"): raise SystemExit(f"checksum mismatch: expected {manifest.get('checksum')} got {checksum}")
    lines=[]
    for n,line in enumerate(raw.decode().splitlines(),1):
        if not line.strip(): continue
        item=json.loads(line)
        missing=REQUIRED-set(item)
        if missing: raise SystemExit(f"line {n}: missing fields {sorted(missing)}")
        if item["action"] not in ALLOWED: raise SystemExit(f"line {n}: unsupported action {item['action']}")
        if not item["provenance"]: raise SystemExit(f"line {n}: missing provenance")
        lines.append(item)
    if len(lines)!=manifest.get("rules_count"): raise SystemExit(f"rule count mismatch: manifest={manifest.get('rules_count')} actual={len(lines)}")
    out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    (out/"client-input.jsonl").write_bytes(raw)
    (out/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"synced {len(lines)} rules; checksum={checksum}"); return 0
if __name__=='__main__': raise SystemExit(main())
