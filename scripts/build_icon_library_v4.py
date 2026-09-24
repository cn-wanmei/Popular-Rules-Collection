#!/usr/bin/env python3
"""Rebuild Icon Library V4 service index deterministically."""
from __future__ import annotations
import json,re
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
RULE=ROOT/"rule/_index.yaml"
V3=ROOT/"assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/index/clients/mihomo.json"
OUT=ROOT/"assets/icons/v4/service-index.json"
V3RAW="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v3/releases/2026.09.22-5e0e48ad55c6/"
V4RAW="https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/"
STYLES=["lucide","tabler","phosphor","material-symbols","fluent","heroicons","remix","bootstrap","solar"]
def style_for(sid):
    h=0
    for ch in sid: h=(h*31+ord(ch))%len(STYLES)
    return STYLES[h]
idx=yaml.safe_load(RULE.read_text(encoding="utf-8")) or {}
v3=json.loads(V3.read_text(encoding="utf-8")).get("entries") or {}
out={"schema":"icon_service_index_v4","version":4,"release":"2026.09.25-prc-icon-matrix-1","styles":["official"]+STYLES,"entries":[],"by_id":{}}
for e in idx.get("entries") or []:
    sid=e["id"]
    icon=v3.get(sid) or v3.get(re.sub(r"_aggregate$","",sid))
    if icon:
        item={"path":e.get("path"),"id":sid,"display_name":e.get("display_name"),"primary":"official","icon":{"type":"existing-v3","raw":V3RAW+icon["path"],"identity":icon.get("identity"),"role":icon.get("role"),"digest":icon.get("digest")}}\n        out["entries"].append(item)\n        out["by_id"].setdefault(sid,[]).append(item)
    else:
        st=style_for(sid)
        item={"path":e.get("path"),"id":sid,"display_name":e.get("display_name"),"primary":st,"icon":{"type":"style-fallback","style":st,"raw":V4RAW+st+"/service.svg","identity":"semantic.fallback."+st}}\n        out["entries"].append(item)\n        out["by_id"].setdefault(sid,[]).append(item)
out["coverage"]={"rule_entries":len(idx.get("entries") or []),"unique_service_ids":len(out["by_id"]),"coverage_pct":100}
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("entries",len(out["entries"]),"unique_ids",len(out["by_id"]))
