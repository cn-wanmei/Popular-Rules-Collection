#!/usr/bin/env python3
"""package_client_releases.py — Build 7 client rule zip artifacts + release notes.

Filesystem-safe naming (required by shell / gh / Actions / architecture_gate):
  {client}-{YYYY}-{M}-{D}-{HH}-{MM}-{SS}.zip
  e.g. egern-2026-10-2-13-25-31.zip

Human-readable stamp (for notes/title only):
  {YYYY}-{M}-{D}-{H}[{MM}:{SS}]  e.g. 2026-10-2-13[25:31]

Outputs under --out-dir:
  - 7 client zips
  - RELEASE_NOTES.md
  - SHA256SUMS.txt
  - release-meta.json

Trigger: manual workflow_dispatch only (never on build/publish).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CLIENTS = (
    "egern",
    "loon",
    "mihomo",
    "quantumultx",
    "shadowrocket",
    "singbox",
    "surge",
)

# Characters that break shell glob, Actions artifacts, or gh path matching
_UNSAFE = re.compile(r"[\[\]:*?\"<>|\\/]")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _format_stamp_human(dt: datetime) -> str:
    """Display-only stamp matching product language."""
    return f"{dt.year}-{dt.month}-{dt.day}-{dt.hour}[{dt.minute:02d}:{dt.second:02d}]"


def _format_stamp_safe(dt: datetime) -> str:
    """Filename/tag-safe stamp: no colon, brackets, or spaces."""
    return f"{dt.year}-{dt.month}-{dt.day}-{dt.hour:02d}-{dt.minute:02d}-{dt.second:02d}"


def _sanitize_stamp(stamp: str) -> str:
    """Convert any user-provided stamp into a safe filename fragment."""
    s = stamp.strip()
    s = s.replace("[", "-").replace("]", "").replace(":", "-")
    s = _UNSAFE.sub("-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def _count_rules_in_tree(root: Path) -> int:
    total = 0
    if not root.is_dir():
        return 0
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".list", ".txt", ".yaml", ".yml", ".json", ".conf"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in text.splitlines():
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("//"):
                continue
            total += 1
    return total


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _zip_dir(src: Path, dest_zip: Path) -> int:
    count = 0
    with zipfile.ZipFile(dest_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in sorted(src.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(src).as_posix())
                count += 1
    return count


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def build_notes(
    *,
    stamp_human: str,
    stamp_safe: str,
    run_id: str,
    collection_id: str,
    client_stats: dict[str, dict[str, Any]],
    total_rules: int,
    latest: dict[str, Any] | None,
    index_services: int | None,
) -> str:
    lines: list[str] = []
    lines.append(f"# Popular-Rules-Collection Release Notes — {stamp_human}")
    lines.append("")
    lines.append("## 总览")
    lines.append("")
    lines.append(f"- **发布时间戳（展示）**: `{stamp_human}`")
    lines.append(f"- **文件名时间戳（安全）**: `{stamp_safe}`")
    lines.append(f"- **Run ID**: `{run_id or 'n/a'}`")
    lines.append(f"- **Collection / Snapshot**: `{collection_id or 'n/a'}`")
    if latest:
        lines.append(f"- **IR digest**: `{latest.get('ir_digest', 'n/a')}`")
        lines.append(f"- **Canonical digest**: `{latest.get('canonical_digest', 'n/a')}`")
        lines.append(f"- **Quality score**: `{latest.get('quality_score', 'n/a')}`")
    if index_services is not None:
        lines.append(f"- **Canonical services (rule/_index)**: **{index_services}**")
    lines.append(f"- **全客户端规则条目合计（估算）**: **{total_rules}**")
    lines.append("")
    lines.append("## 七客户端发行包")
    lines.append("")
    lines.append("| 客户端 | 文件名 | 规则条目估算 | 文件数 |")
    lines.append("|---|---|---:|---:|")
    for c in CLIENTS:
        st = client_stats.get(c, {})
        lines.append(
            f"| {c} | `{st.get('zip_name', '')}` | {st.get('rule_count', 0)} | {st.get('file_count', 0)} |"
        )
    lines.append("")
    lines.append("## 本次变更说明")
    lines.append("")
    lines.append("> 权威数字以 `reports/latest_release.json` 与 `data/runs/<run_id>/release/manifest.json` 为准。")
    lines.append("")
    lines.append("### 新增服务 / 规则")
    lines.append("")
    lines.append("- 新增服务数：见本次 Collection 相对上一 snapshot 的 `reports/v1/` 与 dataset_diff 输出。")
    lines.append("- 新增规则条目：由各客户端 builder 增量体现；完整 diff 在 immutable evidence 中。")
    lines.append("")
    lines.append("### 失效 / 过期 / 删除")
    lines.append("")
    lines.append("- 失效或删除的服务与规则：由 Source health + intentional_unmaterialized + 上一 baseline 对比产生。")
    lines.append("- 详细列表位于 `reports/` 与对应 run 的 release evidence。")
    lines.append("")
    lines.append("### 使用方式")
    lines.append("")
    lines.append("1. 下载对应客户端 zip。")
    lines.append("2. 解压后按客户端文档导入规则文件。")
    lines.append("3. 图标请使用 [Popular-Rules-Icon](https://github.com/cn-wanmei/Popular-Rules-Icon) 对应风格包。")
    lines.append("")
    lines.append("---")
    lines.append("*本说明由 `scripts/package_client_releases.py` 自动生成。发布仅通过手动 workflow_dispatch 触发。*")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generated-root", type=Path, default=Path("generated"))
    parser.add_argument("--out-dir", type=Path, default=Path("release-packages"))
    parser.add_argument("--stamp", default="", help="Override stamp (human or safe form)")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--collection-id", default="")
    args = parser.parse_args()

    gen = args.generated_root
    if not gen.is_dir():
        raise SystemExit(f"generated root not found: {gen}")

    dt = _now()
    if args.stamp:
        stamp_human = args.stamp
        stamp_safe = _sanitize_stamp(args.stamp)
    else:
        stamp_human = _format_stamp_human(dt)
        stamp_safe = _format_stamp_safe(dt)

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    latest = _load_json(Path("reports/latest_release.json"))
    run_id = args.run_id or (latest.get("run_id") if latest else "") or ""
    collection_id = args.collection_id or ""

    index_services: int | None = None
    index_path = Path("rule/_index.yaml")
    if index_path.is_file():
        try:
            text = index_path.read_text(encoding="utf-8")
            index_services = sum(
                1
                for line in text.splitlines()
                if line.strip().startswith("- id:") or line.strip().startswith("id:")
            )
        except OSError:
            pass

    client_stats: dict[str, dict[str, Any]] = {}
    total_rules = 0
    zips: list[Path] = []

    for client in CLIENTS:
        src = gen / client
        if not src.is_dir():
            raise SystemExit(f"missing client directory: {src}")
        zip_name = f"{client}-{stamp_safe}.zip"
        dest = out / zip_name
        file_count = _zip_dir(src, dest)
        rule_count = _count_rules_in_tree(src)
        total_rules += rule_count
        client_stats[client] = {
            "zip_name": zip_name,
            "rule_count": rule_count,
            "file_count": file_count,
            "sha256": _sha256_file(dest),
            "size_bytes": dest.stat().st_size,
        }
        zips.append(dest)
        print(f"[package] {zip_name} files={file_count} rules≈{rule_count}")

    notes = build_notes(
        stamp_human=stamp_human,
        stamp_safe=stamp_safe,
        run_id=run_id,
        collection_id=collection_id,
        client_stats=client_stats,
        total_rules=total_rules,
        latest=latest,
        index_services=index_services,
    )
    notes_path = out / "RELEASE_NOTES.md"
    notes_path.write_text(notes, encoding="utf-8")

    sums_path = out / "SHA256SUMS.txt"
    with sums_path.open("w", encoding="utf-8") as f:
        for c in CLIENTS:
            st = client_stats[c]
            f.write(f"{st['sha256']}  {st['zip_name']}\n")
        f.write(f"{_sha256_file(notes_path)}  RELEASE_NOTES.md\n")

    meta = {
        "schema": "client_release_package_v1",
        "stamp_human": stamp_human,
        "stamp_safe": stamp_safe,
        "generated_at": dt.isoformat(),
        "run_id": run_id,
        "collection_id": collection_id,
        "clients": client_stats,
        "total_rules_estimate": total_rules,
        "zip_count": len(zips),
        "trigger": "manual_workflow_dispatch_only",
    }
    (out / "release-meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"[package] wrote {len(zips)} zips + notes (safe_stamp={stamp_safe})")
    print(f"[package] total rules estimate: {total_rules}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
