#!/usr/bin/env python3
"""
generate_docs.py — auto README per service under docs/rules/{id}.md

Primary metadata from service_primary (+ extra), same source as generate_rule_pages.
Never hand-edit docs/rules/*.md for long-term maintenance.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"
OUT = ROOT / "docs" / "rules"
CDN = yaml.safe_load((ROOT / "config" / "cdn.yaml").read_text(encoding="utf-8"))
OFFICIAL = yaml.safe_load((ROOT / "config" / "official_sites.yaml").read_text(encoding="utf-8")) or {}
CAT = ROOT / "config" / "categories.yaml"
PRIM = ROOT / "config" / "service_primary.yaml"
EXTRA = ROOT / "config" / "service_primary_extra.yaml"

CLIENT_PATHS = [
    ("Mihomo", "generated/mihomo/{id}.yaml"),
    ("sing-box", "generated/sing-box/{id}.json"),
    ("Surge", "generated/surge/{id}.list"),
    ("Shadowrocket", "generated/shadowrocket/{id}.list"),
    ("Quantumult X", "generated/quantumult-x/{id}.list"),
    ("Egern", "generated/egern/{id}.yaml"),
    ("Loon", "generated/loon/{id}.list"),
]


def load_yaml(p: Path) -> dict:
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def primary_map() -> dict[str, dict]:
    prim = load_yaml(PRIM)
    services = dict(prim.get("services") or {})
    defaults = prim.get("defaults") or {}
    extra = load_yaml(EXTRA)
    services.update(extra.get("services") or {})
    for sid, ov in (extra.get("aggregate_overrides") or {}).items():
        base = dict(services.get(sid) or {})
        base.update(ov)
        services[sid] = base
    out: dict[str, dict] = {}
    for sid, meta in services.items():
        m = dict(defaults)
        if isinstance(meta, dict):
            m.update(meta)
        out[str(sid)] = m
    return out


def categories() -> dict[str, str]:
    cats = load_yaml(CAT)
    return {
        str(c["id"]): str(c.get("display_name") or c["id"])
        for c in (cats.get("categories") or [])
    }


def mirror(path: str, kind: str) -> str:
    return CDN["mirrors"][kind].format(
        owner=CDN["owner"], repo=CDN["repo"], branch=CDN["branch"], path=path
    )


def count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    n = 0
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def render(doc: dict, pm: dict, cat_names: dict[str, str]) -> str:
    sid = doc["id"]
    meta_p = pm.get(sid) or {}
    name = meta_p.get("display_name") or doc.get("name", sid)
    pc = str(meta_p.get("primary_category") or doc.get("category") or "other")
    pc_display = cat_names.get(pc, pc)
    st = str(meta_p.get("service_type") or "service")
    tags = meta_p.get("categories") or []
    meta = doc.get("metadata") or {}
    stats = meta.get("stats") or {}
    dcount = stats.get("domain_count") or count_lines(DOMAINS / f"{sid}.txt")
    icount = stats.get("ip_count") or count_lines(IPS / f"{sid}.txt")
    sources = [s.get("id") for s in (doc.get("source") or []) if isinstance(s, dict)]
    if not sources:
        sources = ["unknown"]
    sources_display = " / ".join(sources)
    last = (meta.get("last_updated") or "")[:10] or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    confidence = (meta.get("confidence") or "high").upper()
    rtype = doc.get("type", "domain")
    official = OFFICIAL.get(sid, "")
    primary = f"generated/mihomo/{sid}.yaml"
    purpose = f"用于匹配 **{name}** 相关域名/IP 的分流规则（来自上游标准化合并）。"

    rows = []
    for label, pat in CLIENT_PATHS:
        path = pat.format(id=sid)
        rows.append(f"| {label} | `{path}` | [Raw]({mirror(path, 'raw')}) |")

    lines = [
        f"# {name}",
        "",
        f"> {purpose}",
        "",
        "| 项目 | 内容 |",
        "|------|------|",
        f"| Rule ID | `{sid}` |",
        f"| Primary Ecosystem | **{pc_display}** (`{pc}`) |",
        f"| Service Type | {st} |",
        f"| Tags | {', '.join(str(t) for t in tags) or '—'} |",
        f"| 类型 | {rtype} |",
        f"| Domains | {dcount} |",
        f"| CIDR | {icount} |",
        f"| 最后更新 | {last} |",
        f"| Sources | {sources_display} |",
        f"| Confidence | {confidence} |",
        "",
        "## 用途",
        "",
        purpose,
        "",
        "支持：Mihomo · sing-box · Surge · Shadowrocket · Quantumult X · Egern · Loon",
        "",
        "## 一键订阅",
        "",
        "| 客户端 | 路径 | 链接 |",
        "|--------|------|------|",
        *rows,
        "",
        "## CDN 镜像（Mihomo）",
        "",
        "| 镜像 | 链接 |",
        "|------|------|",
        f"| GitHub Raw | {mirror(primary, 'raw')} |",
        f"| jsDelivr | {mirror(primary, 'jsdelivr')} |",
        f"| Fastly | {mirror(primary, 'fastly')} |",
        f"| Cloudflare 加速 | {mirror(primary, 'cloudflare')} |",
        "",
        "## 官方网站",
        "",
        f"[官方站点]({official})" if official else "_未在 config/official_sites.yaml 配置_",
        "",
        "## 规则来源（Provenance）",
        "",
    ]
    for s in sources:
        lines.append(f"- `{s}`")
    lines += [
        "",
        "由 Popular-Rules-Collection 自动采集、标准化、去重并构建。**请勿把本页当作域名清单。**",
        "",
        "## 数据位置",
        "",
        f"- Schema: `database/services/{sid}.yaml`",
        f"- Domains: `database/domains/{sid}.txt`",
        f"- IPs: `database/ips/{sid}.txt`（若有）",
        f"- Product page: `rule/{pc_display.replace('/', '-')}/…`（见 generate_rule_pages）",
        "",
        "---",
        "_由 `scripts/generate_docs.py` 自动生成，勿长期手工维护。_",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pm = primary_map()
    cat_names = categories()
    n = 0
    index = ["# Rules Index", "", "自动生成的规则说明文档（Primary Ecosystem 对齐）。", ""]
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = doc.get("id") or path.stem
        body = render(doc, pm, cat_names)
        (OUT / f"{sid}.md").write_text(body, encoding="utf-8")
        meta_p = pm.get(sid) or {}
        name = meta_p.get("display_name") or doc.get("name", sid)
        pc = str(meta_p.get("primary_category") or "other")
        index.append(f"- [{name}]({sid}.md) (`{sid}` · {pc})")
        n += 1
    (OUT / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"[generate_docs] wrote {n} docs → {OUT} (primary-aligned)")
    return 0 if n else 1


if __name__ == "__main__":
    raise SystemExit(main())
