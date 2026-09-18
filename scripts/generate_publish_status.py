#!/usr/bin/env python3
"""Generate the machine-owned portion of PUBLISH_STATUS.md."""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "PUBLISH_STATUS.md"
FORMATS = ROOT / "config" / "formats.yaml"
HEALTH = ROOT / "reports" / "source_health_status.yaml"
RETENTION = ROOT / "config" / "retention.yaml"

BEGIN = "<!-- AUTO-GENERATED:BEGIN -->"
END = "<!-- AUTO-GENERATED:END -->"


def latest_collection() -> dict[str, Any] | None:
    candidates: list[tuple[dt.date, Path]] = []
    backup = ROOT / "backup"
    if backup.exists():
        for p in backup.iterdir():
            if p.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name):
                try:
                    candidates.append((dt.date.fromisoformat(p.name), p))
                except ValueError:
                    pass
    if not candidates:
        return None
    _, directory = max(candidates)
    for manifest in (
        directory / "manifests" / "_collection.json",
        directory / "collection_manifest.yaml",
        directory / "manifest.yaml",
        directory / "collection_manifest.json",
    ):
        if not manifest.exists():
            continue
        try:
            if manifest.suffix == ".json":
                import json
                return json.loads(manifest.read_text(encoding="utf-8"))
            return yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
    return {"date": directory.name, "root": str(directory.relative_to(ROOT))}


def render() -> str:
    now = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    health = yaml.safe_load(HEALTH.read_text(encoding="utf-8")) if HEALTH.exists() else {}
    retention = yaml.safe_load(RETENTION.read_text(encoding="utf-8")) if RETENTION.exists() else {}
    formats = yaml.safe_load(FORMATS.read_text(encoding="utf-8")) if FORMATS.exists() else {}
    collection = latest_collection() or {}

    health_sources = health.get("sources", {}) if isinstance(health, dict) else {}
    counts: dict[str, int] = {}
    for item in health_sources.values():
        status = str(item.get("status", "unknown"))
        counts[status] = counts.get(status, 0) + 1

    clients = formats.get("clients", {}) if isinstance(formats, dict) else {}
    outputs: list[str] = []
    if isinstance(clients, dict):
        for key, value in clients.items():
            if isinstance(value, dict):
                output = value.get("output") or value.get("dir")
                if output:
                    outputs.append(f"{key}: `{output}`")

    lines = [
        BEGIN,
        "## Automated status",
        "",
        f"Generated at: `{now}`",
        "",
        "### Collection",
        f"- Latest snapshot date: `{collection.get('date', 'unknown')}`",
        f"- Collection ID: `{collection.get('collection_id', collection.get('id', 'unknown'))}`",
        f"- Status: `{collection.get('status', 'unknown')}`",
        f"- Root: `{collection.get('root', 'unknown')}`",
        "",
        "### Source health",
    ]
    for key in sorted(counts):
        lines.append(f"- `{key}`: {counts[key]}")
    lines += [
        "",
        "### Generated clients",
        *(f"- {line}" for line in sorted(outputs)),
        "" if outputs else "- Format registry entries are available from `config/formats.yaml`.",
        "",
        "### Retention",
        f"- Policy: `{RETENTION.relative_to(ROOT)}`",
        f"- Backup keep_days: `{retention.get('backup', {}).get('keep_days', 'unknown') if isinstance(retention, dict) else 'unknown'}`",
        f"- Release evidence keep_days: `{retention.get('release_evidence', {}).get('keep_days', 'unknown') if isinstance(retention, dict) else 'unknown'}`",
        "",
        END,
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when the generated block is stale")
    args = parser.parse_args()
    text = STATUS.read_text(encoding="utf-8")
    generated = render()
    if BEGIN in text and END in text:
        before, rest = text.split(BEGIN, 1)
        _, after = rest.split(END, 1)
        output = before.rstrip() + "\n" + generated + "\n" + after.lstrip()
    else:
        output = generated + "\n\n" + text.lstrip()
    if args.check:
        if output != text:
            print("PUBLISH_STATUS.md generated block is stale")
            return 1
        return 0
    STATUS.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
