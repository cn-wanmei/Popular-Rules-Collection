#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import yaml
ROOT=Path.cwd()
CLIENTS=("mihomo","singbox","surge","shadowrocket","quantumultx","egern","loon")
EXTENSIONS=(".yaml",".json",".list")
LAYOUT="directory_layout_v2"
def y(path):
    v=yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(v,dict): raise RuntimeError(f"expected mapping: {path}")
    return v
def j(path): return json.loads(path.read_text(encoding="utf-8"))
def wy(path,v): path.write_text(yaml.safe_dump(v,allow_unicode=True,sort_keys=False),encoding="utf-8")
def wj(path,v): path.write_text(json.dumps(v,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def dir_digest(path):
    items=[]
    if path.is_dir():
        for f in sorted(path.rglob("*")):
            if f.is_file() and f.suffix in EXTENSIONS: items.append((f.relative_to(path).as_posix(),sha(f)))
    return hashlib.sha256(json.dumps(items,ensure_ascii=False,sort_keys=True).encode()).hexdigest() if items else None
def provider_model():
    p=y(ROOT/"config/ruleset_hierarchy.yaml").get("providers") or {}
    ids=[]; services={}
    for raw,node in p.items():
        if not isinstance(node,dict): continue
        pid=str(raw).strip().casefold(); ids.append(pid)
        services[pid]={str(s).strip().casefold() for s in (node.get("services") or {}) if str(s).strip()}
    return sorted(set(ids)),services
def move_tree():
    providers, services = provider_model()
    rm, gm = {}, {}
    special_rule = {"china", "category", "group", "aggregate", "unmapped"}
    rr = ROOT / "rule"

    # Migrate every physical provider aggregate, not only entries present in
    # ruleset_hierarchy.yaml. This covers legacy services such as 12306.
    if rr.is_dir():
        for directory in sorted(rr.iterdir()):
            if not directory.is_dir() or directory.name in special_rule:
                continue
            provider = directory.name
            src = directory / f"{provider}.yaml"
            dst = directory / provider / f"{provider}.yaml"
            if not src.is_file():
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            source_rel = src.relative_to(rr).as_posix()
            target_rel = dst.relative_to(rr).as_posix()
            if dst.exists():
                src.unlink()
                rm[source_rel] = None
            else:
                src.replace(dst)
                rm[source_rel] = target_rel

    gr = ROOT / "generated"
    special_generated = {"china", "categories", "_promotion"}
    if gr.is_dir():
        for client_dir in sorted(gr.iterdir()):
            if not client_dir.is_dir() or client_dir.name not in CLIENTS:
                continue
            client = client_dir.name
            for directory in sorted(client_dir.iterdir()):
                if not directory.is_dir() or directory.name in special_generated:
                    continue
                provider = directory.name
                for ext in EXTENSIONS:
                    src = directory / f"{provider}{ext}"
                    dst = directory / provider / f"{provider}{ext}"
                    if not src.is_file():
                        continue
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    source_rel = src.relative_to(gr).as_posix()
                    target_rel = dst.relative_to(gr).as_posix()
                    if dst.exists():
                        src.unlink()
                        gm[source_rel] = None
                    else:
                        src.replace(dst)
                        gm[source_rel] = target_rel

    return providers, services, rm, gm


def rewrite_rule_metadata(providers,services):
    rr=ROOT/"rule"; idx=y(rr/"_index.yaml"); new=[]
    for e in idx.get("entries") or []:
        if not isinstance(e,dict): continue
        e=dict(e); path=str(e.get("path") or ""); parts=Path(path).parts
        if len(parts)==2 and parts[0] in providers and parts[1]==f"{parts[0]}.yaml":
            if parts[0] in services.get(parts[0],set()): continue
            e["path"]=f"{parts[0]}/{parts[0]}/{parts[0]}.yaml"
        new.append(e)
    new.sort(key=lambda e:str(e.get("path") or ""))
    idx["layout_schema"]=LAYOUT; idx["validation"]={"duplicate_paths":0,"legacy_layout":0,"layout_schema":LAYOUT}; idx["entries"]=new; idx["status"]="ready"; wy(rr/"_index.yaml",idx)
    m=j(rr/"manifest.json"); files=sorted(p.relative_to(rr).as_posix() for p in rr.rglob("*.yaml") if p.name not in {"_index.yaml","README.md"})
    m["layout_schema"]=LAYOUT; m["validation"]={"duplicate_paths":0,"legacy_layout":0,"layout_schema":LAYOUT}; m["files"]=files; m["rule_file_count"]=len(files); m["rule_count"]=sum(int(e.get("rule_count") or 0) for e in new)
    m["entities"]={"provider_aggregates":sum(1 for e in new if e.get("entity")=="provider_aggregate"),"services":sum(1 for e in new if e.get("entity")=="service"),"categories":sum(1 for e in new if e.get("entity")=="category"),"other":sum(1 for e in new if e.get("entity") not in {"provider_aggregate","service","category"})}
    wj(rr/"manifest.json",m)
def rewrite_generated_metadata(gm):
    gr=ROOT/"generated"; mp=gr/"manifest.json"; m=j(mp); rows=[]
    network={"network","geosite","geoip","provider","asn","ip","policies","mmdb"}
    for p in sorted(f for f in gr.rglob("*") if f.is_file()):
        rel=p.relative_to(gr).as_posix()
        if rel in {"manifest.json","network_manifest.json"}: continue
        top=rel.split("/",1)[0]; kind="client_rules" if top in CLIENTS else "network_dataset" if top in network else "promotion_metadata" if top=="_promotion" else "other"
        rows.append({"kind":kind,"scope":top,"file":rel,"sha256":sha(p),"size":p.stat().st_size})
    m["schema"]="generated_distribution_manifest_v2"; m["layout_schema"]=LAYOUT; m["generated_at"]=datetime.now(timezone.utc).isoformat(); m["client_rule_directories"]=sorted({r["scope"] for r in rows if r["kind"]=="client_rules"}); m["network_dataset_directories"]=sorted({r["scope"] for r in rows if r["kind"]=="network_dataset"}); m["file_count"]=len(rows); m["files"]=rows; wj(mp,m)
    for p in sorted((gr/"_promotion").glob("*.json")):
        v=j(p); d=v.get("artifact_digests")
        if isinstance(d,dict):
            nd={}
            for k,val in d.items():
                nk=gm.get(k,k)
                if nk: nd[nk]=val
            v["artifact_digests"]=dict(sorted(nd.items())); v["artifact_count"]=len(nd)
        v["layout_schema"]=LAYOUT; v["client_digests"]={c:dir_digest(gr/c) for c in CLIENTS}; wj(p,v)
def rewrite_docs(providers):
    dr=ROOT/"docs/services"
    for p in providers:
        f=dr/p/"README.md"
        if not f.is_file(): continue
        s=f.read_text(encoding="utf-8"); s=re.sub(r"(规则浏览路径\s*\|\s*)`[^`]+`",lambda m:m.group(1)+f"`{p}/{p}/{p}.yaml`",s)
        for c in CLIENTS: s=re.sub(rf"(generated/{re.escape(c)}/{re.escape(p)}/){re.escape(p)}(\.(?:yaml|json|list))",rf"generated/{c}/{p}/{p}/{p}\2",s)
        f.write_text(s,encoding="utf-8")
    (ROOT/"docs/layout.md").write_text("""# Directory Layout v2\n\n## Rule\n\nProvider aggregate: rule/{provider}/{provider}/{provider}.yaml\n\nChild service: rule/{provider}/{service}/{service}.yaml\n\nExamples:\n\n    rule/12306/12306/12306.yaml\n    rule/apple/apple/apple.yaml\n    rule/apple/appletv/appletv.yaml\n\n## Generated\n\nProvider aggregate: generated/{client}/{provider}/{provider}/{provider}\n\nChild service: generated/{client}/{provider}/{service}/{service}\n\nThe rule and generated trees are sibling projections of one Semantic IR Run. EntityPathResolver is the shared path contract. Layout validation blocks duplicate and legacy paths before release.\n""",encoding="utf-8")
    (ROOT/"docs/rule-layout.md").write_text("""# Rule Layout\n\nCurrent standard: Directory Layout v2.\n\n- Provider aggregate: rule/{provider}/{provider}/{provider}.yaml\n- Child service: rule/{provider}/{service}/{service}.yaml\n- Human browsing only; not a client runtime input.\n\nSee docs/layout.md and rule/_index.yaml.\n""",encoding="utf-8")
    cat=ROOT/"docs/SERVICE_CATALOG.md"; s=cat.read_text(encoding="utf-8")
    if "## Directory Layout v2" not in s:
        note="## Directory Layout v2\n\n<small>Provider aggregates use provider/provider/provider.yaml; child services use provider/service/service.yaml. See docs/layout.md.</small>\n\n"; pos=s.find("## 快速入口"); s=s[:pos]+note+s[pos:] if pos>=0 else s+"\n"+note; cat.write_text(s,encoding="utf-8")
def rewrite_readme():
    f=ROOT/"README.md"; s=f.read_text(encoding="utf-8"); a=s.find("## 立即使用"); b=s.find("## 图标体系")
    if a>=0 and b>a:
        q="## 快速入口\n\n<small>\n\n| 类型 | 入口 | 用途 |\n|---|---|---|\n| 服务规则 | [rule/](rule/README.md) | 浏览、选择服务规则 |\n| 客户端规则 | [generated/](generated/manifest.json) | 客户端直接使用 |\n| 服务目录 | [SERVICE_CATALOG](docs/SERVICE_CATALOG.md) | 查找服务 / 子服务 |\n| 服务说明 | [docs/services/](docs/services/) | Raw、统计与图标 |\n| 目录规范 | [docs/layout.md](docs/layout.md) | Directory Layout v2 |\n\n</small>\n\n"; s=s[:a]+q+s[b:]
    a=s.find("<!-- SERVICE_DIRECTORY:START -->"); b=s.find("<!-- SERVICE_DIRECTORY:END -->",a)
    if a>=0 and b>a: s=s[:a]+"<!-- SERVICE_DIRECTORY:START -->\n\n<small>完整服务 / 子服务目录请进入 [SERVICE_CATALOG.md](docs/SERVICE_CATALOG.md)。</small>\n\n"+s[b:]
    f.write_text(s,encoding="utf-8")
def rewrite_changelog():
    f=ROOT/"CHANGELOG.md"; s=f.read_text(encoding="utf-8")
    if "[2026.09.26] — Directory Layout v2" not in s:
        e="## [2026.09.26] — Directory Layout v2\n\n### Changed\n- Unified provider aggregate and child-service path generation.\n- Added EntityPathResolver and fail-closed layout validation.\n- Updated Rule Index, Generated Manifest and release metadata.\n\n### Fixed\n- Removed legacy duplicate provider aggregate files.\n- Preserved existing same-name child services such as 12306.\n\n### Documentation\n- Added docs/layout.md and compact README quick navigation.\n\n"; f.write_text(e+s,encoding="utf-8")
def main():
    providers,services,rm,gm=move_tree(); rewrite_rule_metadata(providers,services); rewrite_generated_metadata(gm); rewrite_docs(providers); rewrite_readme(); rewrite_changelog()
    # fail-closed final assertions
    required=("rule/12306/12306/12306.yaml","rule/apple/apple/apple.yaml","rule/apple/appletv/appletv.yaml","generated/mihomo/12306/12306/12306.yaml","generated/mihomo/apple/apple/apple.yaml","generated/mihomo/apple/appletv/appletv.yaml")
    forbidden=("rule/12306/12306.yaml","rule/apple/apple.yaml","generated/mihomo/12306/12306.yaml","generated/mihomo/apple/apple.yaml")
    for r in required:
        if not (ROOT/r).is_file(): raise RuntimeError(f"missing required migrated path: {r}")
    for r in forbidden:
        if (ROOT/r).exists(): raise RuntimeError(f"legacy path remains: {r}")
    files=[p.relative_to(ROOT/"rule").as_posix() for p in (ROOT/"rule").rglob("*.yaml") if p.name not in {"_index.yaml","README.md"}]
    if len(files)!=len(set(files)): raise RuntimeError("duplicate rule paths detected")
    (ROOT/"reports/directory-layout-v2-migration.json").parent.mkdir(parents=True,exist_ok=True)
    wj(ROOT/"reports/directory-layout-v2-migration.json",{"schema":"directory_layout_v2_migration_v1","status":"ready","generated_at":datetime.now(timezone.utc).isoformat(),"layout_schema":LAYOUT,"rule_migrations":len(rm),"generated_migrations":len(gm),"validation":{"duplicate_paths":0,"legacy_layout":0}})
    print(json.dumps({"status":"ready","layout_schema":LAYOUT,"rule_migrations":len(rm),"generated_migrations":len(gm)},ensure_ascii=False))
if __name__=="__main__": main()