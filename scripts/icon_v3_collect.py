#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,urllib.error,urllib.request
from datetime import datetime,timezone
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,default=Path("build/icon-v3/upstream-sources.json"))
    ap.add_argument("--fetch",action="store_true")
    a=ap.parse_args()
    cfg=yaml.safe_load((ROOT/"config/icon_v3.yaml").read_text(encoding="utf-8")) or {}
    rows=[]
    for src in cfg.get("upstream_sources",[]):
        row=dict(src); url=src.get("homepage")
        if a.fetch and url:
            try:
                req=urllib.request.Request(str(url),headers={"User-Agent":"Popular-Rules-Collection/Icon-System-3.0"})
                with urllib.request.urlopen(req,timeout=20) as resp:data=resp.read()
                row.update(reachable=True,retrieved_bytes=len(data),content_digest=hashlib.sha256(data).hexdigest())
            except (urllib.error.URLError,OSError,TimeoutError) as exc:
                row.update(reachable=False,error=str(exc))
        else:
            row["reachable"]=None
        rows.append(row)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps({"schema":"icon_v3_upstream_source_snapshot_v1","generated_at":datetime.now(timezone.utc).isoformat(),"fetch_enabled":a.fetch,"sources":rows},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return 0
if __name__=="__main__": raise SystemExit(main())
