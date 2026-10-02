#!/usr/bin/env python3
"""Documentation Layer v1 — generate docs from _index + manifest + Icon V6."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as e:
    raise SystemExit("PyYAML required") from e

ROOT = Path(__file__).resolve().parents[1]
RAW_BASE = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/"
ICON_URL = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/dist/v/{hash}.png"
CLIENTS = ["egern", "loon", "mihomo", "quantumultx", "shadowrocket", "singbox", "surge"]
STYLES = [
    "source_original",
    "minimalist",
    "duotone_line",
    "soft_3d",
    "glassmorphism",
    "neo_skeuomorphism",
    "mbe",
    "y2k",
]
ICON_REP = {
    "apple": "appleid",
    "microsoft": "microsoftedge",
    "google": "google-calendar",
    "meta": "facebook",
    "amazon": "amazon",
    "alibaba": "taobao",
    "tencent": "qq",
    "bytedance": "douyin",
}

GEN_START = "<!-- DOC_LAYER_GENERATED_START -->"
GEN_END = "<!-- DOC_LAYER_GENERATED_END -->"
OVR_START = "<!-- DOC_LAYER_OVERRIDES_START -->"
OVR_END = "<!-- DOC_LAYER_OVERRIDES_END -->"


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_manifest_index(
    files: list[dict],
) -> tuple[dict[str, dict[str, dict]], dict[str, dict[str, dict]]]:
    """Index client_rules by path-without-ext and by service_id."""
    by_relstem: dict[str, dict[str, dict]] = {}
    by_sid: dict[str, dict[str, dict]] = {}
    for f in files:
        if f.get("kind") != "client_rules":
            continue
        rel = f.get("file") or ""
        parts = rel.split("/")
        if len(parts) < 4 or parts[0] not in CLIENTS:
            continue
        client = parts[0]
        stem_path = "/".join(parts[1:-1] + [Path(parts[-1]).stem])
        meta = {"file": rel, "rule_count": f.get("rule_count")}
        by_relstem.setdefault(stem_path, {})[client] = meta
        sid = Path(parts[-1]).stem
        by_sid.setdefault(sid, {})[client] = meta
        by_sid.setdefault(parts[2], {})[client] = meta
    return by_relstem, by_sid


def raw_for_entry(
    rule_path: str,
    service_id: str,
    by_relstem: dict[str, dict[str, dict]],
    by_sid: dict[str, dict[str, dict]],
) -> dict[str, dict]:
    stem_path = str(Path(rule_path).with_suffix(""))
    for key in (stem_path, service_id):
        if key in by_relstem and by_relstem[key]:
            return dict(by_relstem[key])
        if key in by_sid and by_sid[key]:
            return dict(by_sid[key])
    parts = Path(rule_path).parts
    if len(parts) >= 2:
        alt = "/".join(list(parts[:-1]) + [Path(parts[-1]).stem])
        if alt in by_relstem:
            return dict(by_relstem[alt])
    return dict(by_sid.get(service_id) or {})


def resolve_icon_id(service_id: str, icon_ids: set[str]) -> str | None:
    if service_id in icon_ids:
        return service_id
    if service_id.endswith("_aggregate"):
        base = service_id[: -len("_aggregate")]
        if base in icon_ids:
            return base
    if service_id in ICON_REP and ICON_REP[service_id] in icon_ids:
        return ICON_REP[service_id]
    return None


def icon_payload(
    service_id: str,
    icon_by_id: dict,
    icon_ids: set[str],
    release_id: str,
    default_style: str,
    default_size: int,
) -> dict:
    rid = resolve_icon_id(service_id, icon_ids)
    if not rid:
        return {
            "release_id": release_id,
            "available": False,
            "service_id_used": None,
            "style": default_style,
            "size": default_size,
            "url": None,
            "variants_256": {},
        }
    entry = icon_by_id[rid]
    key = f"{default_style}:{default_size}:png"
    variants = entry.get("variants") or {}
    primary = variants.get(key) or {}
    h = primary.get("variant_hash")
    v256 = {}
    for s in STYLES:
        vk = f"{s}:256:png"
        vv = variants.get(vk)
        if vv and vv.get("variant_hash"):
            v256[s] = ICON_URL.format(hash=vv["variant_hash"])
    return {
        "release_id": release_id,
        "available": bool(h),
        "service_id_used": rid,
        "style": default_style,
        "size": default_size,
        "variant_key": key,
        "variant_hash": h,
        "url": ICON_URL.format(hash=h) if h else None,
        "variants_256": v256,
    }


def render_generated_block(rec: dict) -> str:
    lines: list[str] = []
    icon = rec["icon"]
    if icon.get("url"):
        lines.append(
            f'<img src="{icon["url"]}" alt="{rec["service_id"]} icon" width="72" height="72">'
        )
        lines.append("")
    lines.append(f"# {rec['display_name']} — 分流规则说明")
    lines.append("")
    lines.append(
        f"> 由 Documentation Layer v1 生成。真源：`rule/_index.yaml` + `generated/manifest.json` + Icon V6 `{icon.get('release_id')}`。"
    )
    lines.append("> `rule/` 仅供浏览；客户端请使用 `generated/` Raw。")
    lines.append("")
    lines.append("## 1. 服务基本信息")
    lines.append("")
    lines.append("| 项目 | 当前值 |")
    lines.append("|---|---|")
    lines.append(f"| Service ID | `{rec['service_id']}` |")
    lines.append(f"| Rule ID | `{rec['service_id']}` |")
    lines.append(f"| 类型 | {rec['entity']} |")
    lines.append(f"| Provider | `{rec['provider']}` |")
    lines.append(f"| 规则浏览路径 | `rule/{rec['path']}` |")
    lines.append(f"| 规则数量（_index） | **{rec['rule_count']}** |")
    lines.append(f"| SHA-256 | `{rec['sha256']}` |")
    lines.append("")
    lines.append("## 2. 构建指纹")
    lines.append("")
    lines.append("| 项目 | 当前值 |")
    lines.append("|---|---|")
    lines.append(f"| Run ID | `{rec['run_id']}` |")
    lines.append(f"| IR digest | `{rec['ir_digest']}` |")
    lines.append(f"| IR schema | `{rec.get('ir_schema', '')}` |")
    lines.append("")
    lines.append("## 3. 图标（Icon System 6.0）")
    lines.append("")
    if icon.get("available"):
        lines.append("- Provider：`cn-wanmei/Popular-Rules-Icon`（branch `dist`）")
        lines.append(f"- Release：`{icon['release_id']}`")
        lines.append(f"- 默认：`{icon['style']}` @ {icon['size']}px")
        if icon.get("service_id_used") != rec["service_id"]:
            lines.append(f"- Icon 映射自：`{icon['service_id_used']}`")
        lines.append(f"- Object：`v/{icon.get('variant_hash')}.png`")
        lines.append(f"- Raw：`{icon['url']}`")
        if icon.get("variants_256"):
            lines.append("")
            lines.append("| 风格 | 256 |")
            lines.append("|---|---|")
            for s, u in icon["variants_256"].items():
                lines.append(f"| `{s}` | [link]({u}) |")
    else:
        lines.append("- Icon：unavailable for this service_id in production manifest")
    lines.append("")
    lines.append("## 4. 仓库路径绑定（rule ↔ generated）")
    lines.append("")
    lines.append("| 层 | 路径 |")
    lines.append("|---|---|")
    lines.append(f"| Human browse（非运行时） | [`rule/{rec['path']}`](../../../../rule/{rec['path']}) |")
    lines.append(f"| Index 条目 | `rule/_index.yaml` → id `{rec['service_id']}` |")
    raw = rec.get("raw") or {}
    for c in CLIENTS:
        meta = raw.get(c)
        if meta and meta.get("file"):
            lines.append(f"| Client `{c}` | `generated/{meta['file']}` |")
        else:
            lines.append(f"| Client `{c}` | _not in manifest_ |")
    lines.append("")
    lines.append("## 5. 七客户端 Raw 与 rule_count")
    lines.append("")
    lines.append("| 客户端 | Manifest rule_count | Raw URL |")
    lines.append("|---|---:|---|")
    for c in CLIENTS:
        meta = raw.get(c) or {}
        rel = meta.get("file")
        rc = meta.get("rule_count")
        rc_s = "—" if rc is None else str(rc)
        if rel:
            lines.append(f"| {c} | {rc_s} | `{RAW_BASE}{rel}` |")
        else:
            lines.append(f"| {c} | — | _not in manifest_ |")
    lines.append("")
    lines.append(
        "> **说明：** `singbox` 的 Manifest `rule_count=0` **不代表无规则**；"
        "sing-box 使用 JSON rule-set，统计口径与 classical list/yaml 不同。"
        "以文件存在与 `_index` 的 rule_count 为准。"
    )
    lines.append("")
    lines.append("## 6. Source")
    lines.append("")
    lines.append(
        "证据与 lifecycle 见 [Popular-Rules-Source](https://github.com/cn-wanmei/Popular-Rules-Source)；"
        "Collection 不复制 evidence 正文。"
    )
    lines.append("")
    lines.append("## 7. 使用注意")
    lines.append("")
    lines.append("- 选择客户端后复制对应 Raw，加入 Rule Provider / rule-set，再绑定策略。")
    lines.append("- 不要跨客户端混用格式；不要把 `rule/` 当作运行时输入。")
    lines.append(
        "- 目录总表：[SERVICE_CATALOG.generated.md](https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/SERVICE_CATALOG.generated.md)"
    )
    lines.append("")
    return "\n".join(lines)


def merge_page(existing: str | None, generated: str, override: str | None) -> str:
    body = f"{GEN_START}\n{generated.rstrip()}\n{GEN_END}\n"
    ovr = override.strip() if override else ""
    body += f"\n{OVR_START}\n"
    if ovr:
        body += ovr.rstrip() + "\n"
    body += f"{OVR_END}\n"
    return body


def services_readme_path(rule_path: str) -> Path:
    parts = Path(rule_path).parts
    if len(parts) >= 2:
        return ROOT / "docs" / "services" / parts[0] / parts[1] / "README.md"
    return ROOT / "docs" / "services" / parts[0] / "README.md"


def main() -> int:
    idx = load_yaml(ROOT / "rule" / "_index.yaml")
    man = load_json(ROOT / "generated" / "manifest.json")
    icon_docs = load_yaml(ROOT / "config" / "icon_docs.yaml")
    icon_v6 = load_yaml(ROOT / "config" / "icon_v6.yaml")
    release_id = (icon_v6.get("v6") or {}).get("release_id") or icon_docs.get(
        "production_release_id"
    )
    default_style = icon_docs.get("default_style") or "source_original"
    default_size = int(icon_docs.get("default_size") or 256)

    icon_path = ROOT / "docs" / "generated" / "icon_manifest_cache.json"
    candidates: list[Path] = []
    env_raw = (os.environ.get("ICON_MANIFEST_PATH") or "").strip()
    if env_raw:
        candidates.append(Path(env_raw))
    candidates.extend(
        [
            icon_path,
            Path("/tmp/doclayer/clean1.json"),
            Path("/tmp/docv2/clean1.json"),
        ]
    )
    icon_data = None
    for candidate in candidates:
        if candidate.is_file():
            icon_data = load_json(candidate)
            break
    if icon_data is None and release_id:
        import urllib.request

        url = (
            "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Icon/"
            f"dist/manifests/{release_id}.json"
        )
        try:
            with urllib.request.urlopen(url, timeout=120) as resp:
                icon_data = json.loads(resp.read().decode("utf-8"))
            icon_path.parent.mkdir(parents=True, exist_ok=True)
            icon_path.write_text(json.dumps(icon_data), encoding="utf-8")
        except Exception as exc:
            print(f"generate_rule_docs: warning icon manifest fetch failed: {exc}")
            icon_data = {"entries": [], "release_id": release_id}
    if icon_data is None:
        icon_data = {"entries": [], "release_id": release_id}

    icon_by_id = {e["service_id"]: e for e in icon_data.get("entries") or []}
    icon_ids = set(icon_by_id)
    by_relstem, by_sid = build_manifest_index(man.get("files") or [])
    run_id = idx.get("run_id")
    ir_digest = idx.get("ir_digest")
    ir_schema = idx.get("ir_schema")

    records = []
    for ent in idx.get("entries") or []:
        sid = str(ent["id"])
        path = ent["path"]
        raw_map = raw_for_entry(path, sid, by_relstem, by_sid)
        rec = {
            "service_id": sid,
            "display_name": ent.get("display_name") or sid,
            "provider": ent.get("provider") or "",
            "entity": ent.get("entity") or "",
            "path": path,
            "rule_count": ent.get("rule_count"),
            "sha256": ent.get("sha256"),
            "run_id": run_id,
            "ir_digest": ir_digest,
            "ir_schema": ir_schema,
            "clients": [c for c in CLIENTS if c in raw_map],
            "raw": raw_map,
            "icon": icon_payload(
                sid, icon_by_id, icon_ids, release_id, default_style, default_size
            ),
        }
        records.append(rec)

    index_out = {
        "documentation_contract_version": "1.0",
        "run_id": run_id,
        "ir_digest": ir_digest,
        "icon_release_id": release_id,
        "service_count": len(records),
        "services": [
            {
                "id": r["service_id"],
                "display_name": r["display_name"],
                "provider": r["provider"],
                "entity": r["entity"],
                "path": r["path"],
                "rule_count": r["rule_count"],
                "clients": r["clients"],
                "icon_available": r["icon"].get("available"),
            }
            for r in records
        ],
    }
    out_index = ROOT / "docs" / "generated" / "docs-index.json"
    out_index.parent.mkdir(parents=True, exist_ok=True)
    out_index.write_text(
        json.dumps(index_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    overrides_dir = ROOT / "docs" / "overrides"
    rules_dir = ROOT / "docs" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)

    for rec in records:
        sid = rec["service_id"]
        gen = render_generated_block(rec)
        ovr_path = overrides_dir / f"{sid}.md"
        ovr = ovr_path.read_text(encoding="utf-8") if ovr_path.is_file() else None
        rp = rules_dir / f"{sid}.md"
        rp.write_text(merge_page(None, gen, ovr), encoding="utf-8")
        sp = services_readme_path(rec["path"])
        sp.parent.mkdir(parents=True, exist_ok=True)
        sp.write_text(merge_page(None, gen, ovr), encoding="utf-8")

    cat_lines = [
        "# Service Catalog (generated)",
        "",
        f"Run: `{run_id}`  ",
        f"IR: `{ir_digest}`  ",
        f"Services: **{len(records)}**  ",
        f"Icon release: `{release_id}`",
        "",
        "Do not hand-edit. Source: `rule/_index.yaml` + `generated/manifest.json`.",
        "",
        "| Service ID | Display | Provider | Entity | Rules | Clients | Docs |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for r in sorted(records, key=lambda x: x["service_id"]):
        doc = f"rules/{r['service_id']}.md"
        cat_lines.append(
            f"| `{r['service_id']}` | {r['display_name']} | `{r['provider']}` | {r['entity']} | {r['rule_count']} | {len(r['clients'])} | [{r['service_id']}]({doc}) |"
        )
    cat_lines.append("")
    (ROOT / "docs" / "SERVICE_CATALOG.generated.md").write_text(
        "\n".join(cat_lines), encoding="utf-8"
    )

    readme_lines = [
        "# Rule documentation index",
        "",
        f"Run: `{run_id}`  ",
        f"Services: **{len(records)}**",
        "",
        "Generated by Documentation Layer v1. Links use `(service_id.md)` for SSOT gate.",
        "",
    ]
    for r in sorted(records, key=lambda x: x["service_id"]):
        sid = r["service_id"]
        readme_lines.append(f"- [{r['display_name']}]({sid}.md)")
    readme_lines.append("")
    (rules_dir / "README.md").write_text("\n".join(readme_lines), encoding="utf-8")

    # Root generated README (single file, not per-service) — points to catalog
    gen_readme = ROOT / "generated" / "README.md"
    if gen_readme.parent.exists():
        gen_readme.write_text(
            "\n".join(
                [
                    "# Generated client rules",
                    "",
                    "This tree is **machine-produced** from Semantic IR. Do not hand-edit.",
                    "",
                    "Per-service documentation (identity, Icon V6, seven-client Raw, rule ↔ generated binding):",
                    "",
                    "- [SERVICE_CATALOG.generated.md](../docs/SERVICE_CATALOG.generated.md)",
                    "- [docs/rules/](../docs/rules/)",
                    "- [docs/services/](../docs/services/)",
                    "",
                    "Clients: " + ", ".join(CLIENTS),
                    "",
                ]
            ),
            encoding="utf-8",
        )

    print(
        f"generate_rule_docs: wrote {len(records)} services; run_id={run_id}; index={out_index}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
