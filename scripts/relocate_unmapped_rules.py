#!/usr/bin/env python3
"""Move hierarchy-declared services out of rule/unmapped into rule/{provider}/{service}/."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping: {path}")
    return data


def hierarchy_services(path: Path) -> dict[str, str]:
    doc = load_yaml(path)
    out: dict[str, str] = {}
    for provider, meta in (doc.get("providers") or {}).items():
        if not isinstance(meta, dict):
            continue
        for service in meta.get("services") or {}:
            sid = str(service).strip()
            if sid in out and out[sid] != str(provider):
                raise ValueError(f"service {sid!r} multi-provider: {out[sid]!r} vs {provider!r}")
            out[sid] = str(provider)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root = args.root.resolve()
    rule_root = root / "rule"
    unmapped = rule_root / "unmapped"
    mapping = hierarchy_services(root / "config" / "ruleset_hierarchy.yaml")
    moved: list[dict[str, str]] = []
    unknown: list[str] = []
    if not unmapped.is_dir():
        print(json.dumps({"schema": "relocate_unmapped_v1", "moved": [], "unknown": [], "note": "no unmapped dir"}, ensure_ascii=False))
        return 0
    for entry in sorted(unmapped.iterdir(), key=lambda p: p.name.casefold()):
        if entry.name in {"README.md", "_index.yaml", "manifest.json"}:
            continue
        sid = entry.stem if entry.is_file() else entry.name
        provider = mapping.get(sid)
        if not provider:
            if entry.is_dir() and any(entry.rglob("*")):
                unknown.append(sid)
            elif entry.is_file() and entry.suffix in {".yaml", ".yml", ".json"}:
                unknown.append(sid)
            continue
        dest_dir = rule_root / provider / sid
        if args.dry_run:
            moved.append({"service_id": sid, "from": str(entry.relative_to(root)), "to": str(dest_dir.relative_to(root)), "dry_run": "true"})
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        if entry.is_dir():
            for child in entry.iterdir():
                target = dest_dir / child.name
                if target.exists():
                    if target.is_dir():
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                shutil.move(str(child), str(target))
            # remove empty unmapped dir
            try:
                entry.rmdir()
            except OSError:
                shutil.rmtree(entry, ignore_errors=True)
        else:
            target = dest_dir / entry.name
            if target.exists():
                target.unlink()
            shutil.move(str(entry), str(target))
        moved.append({"service_id": sid, "provider": provider, "to": str(dest_dir.relative_to(root))})
    # drop empty unmapped if possible
    if unmapped.is_dir() and not any(unmapped.iterdir()) and not args.dry_run:
        unmapped.rmdir()
    report = {"schema": "relocate_unmapped_v1", "moved": moved, "unknown": unknown}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if unknown else 0


if __name__ == "__main__":
    raise SystemExit(main())
