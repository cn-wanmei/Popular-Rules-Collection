#!/usr/bin/env python3
"""Resolve a Service ID against the current PRC Icon Library V4."""
from __future__ import annotations
import argparse,json
from pathlib import Path
INDEX=Path(__file__).resolve().parents[1]/"assets/icons/v4/service-index.json"
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("service_id")
    ap.add_argument("--json",action="store_true")
    args=ap.parse_args()
    data=json.loads(INDEX.read_text(encoding="utf-8"))
    item=data.get("entries",{}).get(args.service_id)
    if not item:
        print("service_id not found:",args.service_id)
        return 1
    result={"service_id":args.service_id,"release":data.get("release"),**item}
    print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else result["icon"]["raw"])
    return 0
if __name__=="__main__":
    raise SystemExit(main())
