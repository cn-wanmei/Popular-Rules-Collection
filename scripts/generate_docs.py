#!/usr/bin/env python3
"""generate_docs.py — auto README per service under docs/rules/{id}.md"""

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

CLIENT_PATHS = [
    ("Mihomo", "generated/mihomo/{id}.yaml"),
    ("sing-box", "generated/sing-box/{id}.json"),
    ("Surge", "generated/surge/{id}.list"),
    ("Shadowrocket", "generated/shadowrocket/{id}.list"),
    ("Quantumult X", "generated/quantumult-x/{id}.list"),
    ("Egern", "generated/egern/{id}.yaml"),
    ("Loon", "generated/loon/{id}.list"),
]


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


def render(doc: dict) -> str:
    sid = doc["id"]
    name = doc.get("name", sid)
    cat = doc.get("category", "other")
    meta = doc.get("metadata") or {}
    stats = meta.get("stats") or {}
    dcount = stats.get("domain_count") or count_lines(DOMAINS / f"{sid}.txt")
    icount = stats.get("ip_count") or count_lines(IPS / f"{sid}.txt")
    sources = [s.get("id") for s in (doc.get("source") or []) if isinstance(s, dict)] or ["unknown"]
    sources_display = " / ".join(sources)
    last = (meta.get("last_updated") or "")[:10] or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    confidence = (meta.get("confidence") or "high").upper()
    rtype = doc.get("type", "domain")
    official = OFFICIAL.get(sid, "")
    primary = f"generated/mihomo/{sid}.yaml"
    purpose = f"用于匹配 **{name}** 相关域名/IP 的分流规则（上游标准化合并）。"

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
        f"| 分类 | {cat} |",
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
        "",
        "---",
        "_由 `scripts/generate_docs.py` 自动生成，勿长期手工维护。_",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    index = ["# Rules Index", "", "自动生成的规则说明文档。", ""]
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = doc.get("id") or path.stem
        (OUT / f"{sid}.md").write_text(render(doc), encoding="utf-8")
        index.append(f"- [{doc.get('name', sid)}]({sid}.md) (`{sid}`)")
        n += 1
    (OUT / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"[generate_docs] wrote {n} docs → {OUT}")
    return 0 if n else 1


if __name__ == "__main__":
    raise SystemExit(main())
