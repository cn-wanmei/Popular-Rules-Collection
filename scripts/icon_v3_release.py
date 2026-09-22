#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--build-root",type=Path,required=True)
    ap.add_argument("--version",required=True)
    a=ap.parse_args()
    b=a.build_root
    m=json.loads((b/"manifest.json").read_text(encoding="utf-8"))
    q=json.loads((b/"reports"/"qa.json").read_text(encoding="utf-8"))
    g=json.loads((b/"reports"/"gate.json").read_text(encoding="utf-8"))
    if m.get("renderer_version")!="3.0.0" or q.get("status")!="PASS" or g.get("status")!="PASS":
        raise SystemExit("Icon System 3 release blocked")
    releases=ROOT/"assets/icons/v3/releases"
    target=releases/a.version
    latest=releases/"latest"
    for p in (target,latest):
        if p.exists(): shutil.rmtree(p)
    target.mkdir(parents=True,exist_ok=True)
    for name in ("variants","clients","previews","index","reports"):
        shutil.copytree(b/name,target/name)
    if (b/"quarantine").exists():
        shutil.copytree(b/"quarantine", target/"quarantine")
    for name in ("registry.yaml","manifest.json","icon-review-manifest.json"):
        shutil.copy2(b/name,target/name)
    shutil.copytree(target,latest)
    pointer={"schema":"icon_v3_latest_pointer_v1","version":a.version,"manifest_digest":hashlib.sha256((latest/"manifest.json").read_bytes()).hexdigest(),"path":f"assets/icons/v3/releases/{a.version}"}
    (ROOT/"assets/icons/v3/release-pointer.json").write_text(json.dumps(pointer,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return 0
if __name__=="__main__": raise SystemExit(main())
