#!/usr/bin/env python3
"""generate_rule_pages — Primary Ecosystem product pages under rule/"""
from __future__ import annotations
import argparse, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES, DOMAINS, IPS = ROOT/"database"/"services", ROOT/"database"/"domains", ROOT/"database"/"ips"
RULE, CAT, PRIM = ROOT/"rule", ROOT/"config"/"categories.yaml", ROOT/"config"/"service_primary.yaml"
CDN_P, OFF_P = ROOT/"config"/"cdn.yaml", ROOT/"config"/"official_sites.yaml"
CLIENTS = [("Mihomo","generated/mihomo/{id}.yaml"),("sing-box","generated/sing-box/{id}.json"),("Surge","generated/surge/{id}.list"),("Shadowrocket","generated/shadowrocket/{id}.list"),("Quantumult X","generated/quantumult-x/{id}.list"),("Egern","generated/egern/{id}.yaml"),("Loon","generated/loon/{id}.list")]
TYPE_MAP = {"domain":"DOMAIN","domain_suffix":"DOMAIN-SUFFIX","domain_keyword":"DOMAIN-KEYWORD","ip_cidr":"IP-CIDR","ipcidr":"IP-CIDR","cidr":"IP-CIDR","ip_cidr6":"IP-CIDR6","ipcidr6":"IP-CIDR6"}

def load(p):
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else None

def load_header(path: Path) -> dict:
    lines, n = [], 0
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            n += 1
            if n > 80 and line.startswith("rules:"): break
            if n > 200: break
            lines.append(line)
    d = yaml.safe_load("".join(lines)) or {}
    d.setdefault("id", path.stem)
    d["rules"] = []
    return d

def cats():
    out = {}
    for c in (load(CAT) or {}).get("categories") or []:
        out[str(c["id"])] = {"id": str(c["id"]), "display_name": c.get("display_name") or str(c["id"]).title(), "order": int(c.get("order") or 999), "notes": c.get("notes") or ""}
    if not out: raise SystemExit("no categories")
    return out

def primary_map():
    raw = load(PRIM) or {}
    defaults, services, out = raw.get("defaults") or {}, raw.get("services") or {}, {}
    for sid, meta in services.items():
        m = dict(defaults)
        if isinstance(meta, dict): m.update(meta)
        out[str(sid)] = m
    return out

def mirror(cdn, path, kind):
    t = (cdn.get("mirrors") or {}).get(kind)
    return t.format(owner=cdn.get("owner","cn-wanmei"), repo=cdn.get("repo","Popular-Rules-Collection"), branch=cdn.get("branch","main"), path=path) if t else path

def classical(doc):
    mixed, domains, ips, seen = [], [], [], set()
    def add(line, bucket):
        if line in seen: return
        seen.add(line); mixed.append(line); bucket.append(line)
    sid = doc.get("id")
    if sid:
        dp = DOMAINS / f"{sid}.txt"
        if dp.exists():
            for line in dp.read_text(encoding="utf-8", errors="replace").splitlines():
                v = line.strip()
                if not v or v.startswith("#"): continue
                if v.startswith("+."): v = v[2:]
                add(f"DOMAIN-SUFFIX,{v}", domains)
        ip = IPS / f"{sid}.txt"
        if ip.exists():
            for line in ip.read_text(encoding="utf-8", errors="replace").splitlines():
                v = line.strip()
                if not v or v.startswith("#"): continue
                prefix = "IP-CIDR6" if ":" in v.split("/")[0] else "IP-CIDR"
                add(f"{prefix},{v}", ips)
    if domains or ips: return mixed, domains, ips
    for r in doc.get("rules") or []:
        if not isinstance(r, dict): continue
        t = (r.get("type") or "").lower().replace("-", "_"); val = (r.get("value") or "").strip()
        if not val: continue
        prefix = TYPE_MAP.get(t) or ("IP-CIDR" if t in ("ip","ipv4") else ("IP-CIDR6" if t=="ipv6" else None))
        if not prefix: continue
        line = f"{prefix},{val}"
        add(line, ips if prefix.startswith("IP") else domains)
    return mixed, domains, ips

def write_list(path, lines, header):
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(lines)
    path.write_text(f"# {header}\n# AUTO-GENERATED — do not edit\n{body}\n" if body else f"# {header}\n# AUTO-GENERATED — empty\n", encoding="utf-8")

def readme(meta, cat_display, mixed, domains, ips, sources, cdn, official, notes):
    sid, name, day = meta["id"], meta["name"], datetime.now(timezone.utc).strftime("%Y-%m-%d")
    base = f"rule/{cat_display}/{name}"
    rows = [f"| {lab} | [Raw]({mirror(cdn, pat.format(id=sid), 'raw')}) | [jsDelivr]({mirror(cdn, pat.format(id=sid), 'jsdelivr')}) |" for lab, pat in CLIENTS]
    un = "\n> **说明：** 本目录集中管理银联及银行类服务规则；银行域名并不属于银联实体。\n" if meta["primary_category"]=="unionpay" else ""
    lines = [f"# {name}", "", f"**{cat_display}** · `{sid}` · {meta['service_type']}", "", un, "## 统计", "", "| 项目 | 数值 |", "|------|------|", f"| Domains | {len(domains)} |", f"| IP/CIDR | {len(ips)} |", f"| Mixed | {len(mixed)} |", f"| Sources | {', '.join(sources) or '—'} |", f"| Updated | {day} |", "", "## 基础规则（Classical）", "", f"- 混合：[`{sid}.list`](./{sid}.list)"]
    if domains: lines.append(f"- 域名：[`{sid}_domain.list`](./{sid}_domain.list)")
    if ips: lines.append(f"- IP：[`{sid}_ip.list`](./{sid}_ip.list)")
    lines += ["", "## 客户端订阅", "", "| 客户端 | Raw | jsDelivr |", "|--------|-----|----------|", *rows, "", "## CDN", "", f"- Raw: {mirror(cdn, base+'/'+sid+'.list', 'raw')}", f"- jsDelivr: {mirror(cdn, base+'/'+sid+'.list', 'jsdelivr')}", "", "## 来源", "", ", ".join(f"`{s}`" for s in sources) or "—", ""]
    if official: lines += ["## 官方", "", official, ""]
    if notes: lines += ["## 分类说明", "", notes, ""]
    lines += ["---", "", "⚠️ 自动生成，勿手工修改。真源：`database/`。", ""]
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--clean", action="store_true"); ap.add_argument("--strict", action="store_true"); args = ap.parse_args()
    categories, pmap, cdn, official_map = cats(), primary_map(), load(CDN_P) or {}, load(OFF_P) or {}
    if not SERVICES.is_dir(): print("ERROR: database/services missing", file=sys.stderr); return 1
    if args.clean and RULE.exists(): shutil.rmtree(RULE)
    errors, index, path_used, count = [], {"generated_at": datetime.now(timezone.utc).isoformat(), "categories": {}}, set(), 0
    for path in sorted(SERVICES.glob("*.yaml")):
        doc = load_header(path) if path.stat().st_size > 512_000 else (load(path) or {})
        sid = str(doc.get("id") or path.stem)
        if sid not in pmap and args.strict: errors.append(f"{sid}: missing mapping"); continue
        pm = pmap.get(sid) or {}
        pc = str(pm.get("primary_category") or doc.get("category") or "other")
        if pc not in categories: pc = "other"
        st = str(pm.get("service_type") or "service")
        if st not in ("service", "aggregate"): errors.append(f"{sid}: bad service_type"); continue
        display = str(pm.get("display_name") or doc.get("name") or sid)
        tags = list(pm.get("categories") or [])
        cat = categories[pc]; cat_display = cat["display_name"].replace("/", "-"); svc_folder = display.replace("/", "-")
        rel = f"{cat_display}/{svc_folder}"
        if rel in path_used: errors.append(f"path conflict {rel}"); continue
        path_used.add(rel)
        out = RULE / cat_display / svc_folder; out.mkdir(parents=True, exist_ok=True)
        mixed, domains, ips = classical(doc)
        sources = []
        for s in doc.get("source") or []:
            if isinstance(s, dict) and s.get("id"): sources.append(str(s["id"]))
            elif isinstance(s, str): sources.append(s)
        write_list(out / f"{sid}.list", mixed, f"{sid} mixed")
        if domains: write_list(out / f"{sid}_domain.list", domains, f"{sid} domain")
        if ips: write_list(out / f"{sid}_ip.list", ips, f"{sid} ip")
        page = {"id": sid, "name": display, "primary_category": pc, "categories": tags, "service_type": st, "rule": {"has_domain": bool(domains), "has_ip": bool(ips), "mixed": True}, "generated_files": {"mixed": f"{sid}.list", "domain": f"{sid}_domain.list" if domains else None, "ip": f"{sid}_ip.list" if ips else None}, "statistics": {"domains": len(domains), "ipv4_or_cidr": len(ips), "mixed": len(mixed)}, "sources": sources, "clients": [c[0] for c in CLIENTS], "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "auto_generated": True}
        (out / "metadata.yaml").write_text(yaml.dump(page, allow_unicode=True, sort_keys=False), encoding="utf-8")
        meta = {"id": sid, "name": display, "primary_category": pc, "service_type": st}
        (out / "README.md").write_text(readme(meta, cat_display, mixed, domains, ips, sources, cdn, str(official_map.get(sid) or ""), cat.get("notes") or ""), encoding="utf-8")
        index["categories"].setdefault(pc, {"display_name": cat_display, "order": cat["order"], "rules": []})
        index["categories"][pc]["rules"].append({"id": sid, "name": display, "path": f"rule/{rel}", "service_type": st, "domains": len(domains), "ips": len(ips)})
        count += 1
    for v in index["categories"].values(): v["rules"] = sorted(v["rules"], key=lambda x: x["id"])
    RULE.mkdir(parents=True, exist_ok=True)
    (RULE / "_index.yaml").write_text(yaml.dump(index, allow_unicode=True, sort_keys=False), encoding="utf-8")
    if errors:
        print("VALIDATION:", file=sys.stderr)
        for e in errors: print(" -", e, file=sys.stderr)
        if args.strict: return 1
    print(f"OK generate_rule_pages: {count} services → rule/")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
