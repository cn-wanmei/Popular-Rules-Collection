#!/usr/bin/env python3
"""Path Links G3 — short README pointers under rule/ and generated/."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as e:
    raise SystemExit("PyYAML required") from e

ROOT = Path(__file__).resolve().parents[1]
CLIENTS = ["egern", "loon", "mihomo", "quantumultx", "shadowrocket", "singbox", "surge"]
RAW_BASE = "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/"
DOC_RULES = "https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/rules/{id}.md"
DOC_SVC = "https://github.com/cn-wanmei/Popular-Rules-Collection/blob/main/docs/services/{provider}/{service_dir}/README.md"
START = "<!-- PATH_LINKS_GENERATED_START -->"
END = "<!-- PATH_LINKS_GENERATED_END -->"


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_indexes(files: list[dict]):
    by_relstem: dict[str, dict[str, dict]] = {}
    by_sid: dict[str, dict[str, dict]] = {}
    for f in files:
        if f.get("kind") != "client_rules":
            continue
        rel = f.get("file") or ""
        parts = rel.split("/")
        if len(parts) < 3 or parts[0] not in CLIENTS:
            continue
        client = parts[0]
        stem_path = "/".join(parts[1:-1] + [Path(parts[-1]).stem])
        meta = {"file": rel, "rule_count": f.get("rule_count")}
        by_relstem.setdefault(stem_path, {})[client] = meta
        sid = Path(parts[-1]).stem
        by_sid.setdefault(sid, {})[client] = meta
        if len(parts) >= 4:
            by_sid.setdefault(parts[2], {})[client] = meta
        else:
            by_sid.setdefault(parts[1], {})[client] = meta
    return by_relstem, by_sid


def raw_for(rule_path: str, service_id: str, by_relstem, by_sid) -> dict[str, dict]:
    stem_path = str(Path(rule_path).with_suffix(""))
    for key in (stem_path, service_id):
        if key in by_relstem and by_relstem[key]:
            return dict(by_relstem[key])
        if key in by_sid and by_sid[key]:
            return dict(by_sid[key])
    return dict(by_sid.get(service_id) or {})


def wrap(body: str) -> str:
    return f"{START}\n{body.rstrip()}\n{END}\n"


def rule_readme(rec: dict, raw: dict[str, dict]) -> str:
    sid = rec["service_id"]
    parts = Path(rec["path"]).parts
    service_dir = parts[1] if len(parts) >= 2 else parts[0]
    provider = rec.get("provider") or (parts[0] if parts else sid)
    lines = [
        f"# {rec['display_name']}",
        "",
        f"- **Service ID:** `{sid}`",
        f"- **说明文档:** [docs/rules/{sid}.md]({DOC_RULES.format(id=sid)})",
        f"- **树状说明:** [docs/services/...]({DOC_SVC.format(provider=provider, service_dir=service_dir)})",
        f"- **本目录规则文件:** `{rec['path']}`（浏览用，**非**客户端运行时输入）",
        f"- **Run:** `{rec.get('run_id', '')}`",
        "",
        "## 七客户端 Raw",
        "",
        "| 客户端 | Raw |",
        "|---|---|",
    ]
    for c in CLIENTS:
        meta = raw.get(c) or {}
        rel = meta.get("file")
        if rel:
            lines.append(f"| {c} | `{RAW_BASE}{rel}` |")
        else:
            lines.append(f"| {c} | _not in manifest_ |")
    lines.append("")
    lines.append(
        "完整说明（图标 / 指纹 / rule↔generated 绑定）见 Documentation Layer 页面。"
    )
    lines.append("")
    return wrap("\n".join(lines))


def generated_readme(
    client: str, rel_file: str, sid: str, display: str, rule_path: str, doc_ok: bool
) -> str:
    lines = [
        f"# {display} · `{client}`",
        "",
        f"- **Service ID:** `{sid}`",
        f"- **本文件 Raw:** `{RAW_BASE}{rel_file}`",
        f"- **说明文档:** [docs/rules/{sid}.md]({DOC_RULES.format(id=sid)})",
        f"- **浏览用规则:** `rule/{rule_path}`（非运行时输入）",
        "",
        "本目录其它文件为客户端规则正文；本 README 为自动生成的快速链接（Path Links G3）。",
        "",
    ]
    return wrap("\n".join(lines))


def main() -> int:
    idx = load_yaml(ROOT / "rule" / "_index.yaml")
    man = load_json(ROOT / "generated" / "manifest.json")
    by_relstem, by_sid = build_indexes(man.get("files") or [])
    run_id = idx.get("run_id")
    entries = idx.get("entries") or []

    rule_n = 0
    gen_n = 0
    # Map sid -> display/path for generated side
    meta_by_sid = {}
    for ent in entries:
        sid = str(ent["id"])
        path = ent["path"]
        display = ent.get("display_name") or sid
        provider = ent.get("provider") or ""
        raw = raw_for(path, sid, by_relstem, by_sid)
        rec = {
            "service_id": sid,
            "display_name": display,
            "provider": provider,
            "path": path,
            "run_id": run_id,
        }
        meta_by_sid[sid] = rec
        # rule tree README
        rule_file = ROOT / "rule" / path
        target = rule_file.parent / "README.md"
        if rule_file.parent.exists() or True:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rule_readme(rec, raw), encoding="utf-8")
            rule_n += 1
        # generated G3: one README per client file directory
        for c, meta in raw.items():
            rel = meta.get("file")
            if not rel:
                continue
            gpath = ROOT / "generated" / rel
            gdir = gpath.parent
            gdir.mkdir(parents=True, exist_ok=True)
            (gdir / "README.md").write_text(
                generated_readme(c, rel, sid, display, path, True),
                encoding="utf-8",
            )
            gen_n += 1

    # Also walk manifest for client files not keyed via _index (should be rare)
    for f in man.get("files") or []:
        if f.get("kind") != "client_rules":
            continue
        rel = f.get("file") or ""
        parts = rel.split("/")
        if len(parts) < 3:
            continue
        sid = Path(parts[-1]).stem
        if sid in meta_by_sid:
            continue
        # orphan client file — still write minimal pointer
        gdir = (ROOT / "generated" / rel).parent
        gdir.mkdir(parents=True, exist_ok=True)
        readme = gdir / "README.md"
        if not readme.exists():
            readme.write_text(
                generated_readme(
                    parts[0],
                    rel,
                    sid,
                    sid,
                    "/".join(parts[1:]),
                    False,
                ),
                encoding="utf-8",
            )
            gen_n += 1

    # Guarantee G3 README for every client_rules leaf
    for f in man.get("files") or []:
        if f.get("kind") != "client_rules":
            continue
        rel = f.get("file") or ""
        parts = rel.split("/")
        if len(parts) < 3 or parts[0] not in CLIENTS:
            continue
        sid = Path(parts[-1]).stem
        rec = meta_by_sid.get(sid) or {
            "service_id": sid,
            "display_name": sid,
            "path": "/".join(parts[1:]),
            "run_id": run_id,
        }
        gdir = (ROOT / "generated" / rel).parent
        gdir.mkdir(parents=True, exist_ok=True)
        target = gdir / "README.md"
        if not target.exists():
            target.write_text(
                generated_readme(
                    parts[0],
                    rel,
                    sid,
                    rec.get("display_name") or sid,
                    rec.get("path") or "/".join(parts[1:]),
                    sid in meta_by_sid,
                ),
                encoding="utf-8",
            )
            gen_n += 1

    # Root pointers
    (ROOT / "rule" / "README.md").write_text(
        wrap(
            "\n".join(
                [
                    "# Rule browse tree",
                    "",
                    "Human-readable rule distribution (`directory_layout_v2`). **Not** client runtime input.",
                    "",
                    f"- Run: `{run_id}`",
                    "- Service docs: [docs/SERVICE_CATALOG.generated.md](../docs/SERVICE_CATALOG.generated.md)",
                    "- Flat docs: [docs/rules/](../docs/rules/)",
                    "- Client artifacts: [generated/](../generated/)",
                    "",
                    "Each service directory contains a short `README.md` (Path Links G3) with documentation and Raw links.",
                    "",
                ]
            )
        ),
        encoding="utf-8",
    )
    (ROOT / "generated" / "README.md").write_text(
        wrap(
            "\n".join(
                [
                    "# Generated client rules",
                    "",
                    "Machine-produced client rule files. Do not hand-edit rule payloads.",
                    "",
                    f"- Run (from index): `{run_id}`",
                    "- Catalog: [docs/SERVICE_CATALOG.generated.md](../docs/SERVICE_CATALOG.generated.md)",
                    "- Docs index: [docs/rules/](../docs/rules/)",
                    "",
                    "Clients: " + ", ".join(CLIENTS),
                    "",
                    "Each leaf directory has a short `README.md` (Path Links G3): this file's Raw URL + link to service documentation.",
                    "",
                ]
            )
        ),
        encoding="utf-8",
    )

    print(f"generate_path_links: rule_readmes={rule_n} generated_readmes={gen_n} run_id={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
