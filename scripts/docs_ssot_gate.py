#!/usr/bin/env python3
"""Documentation SSOT gate — aligned with Documentation Layer v1 + directory_layout_v2."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "rule" / "_index.yaml"
MANIFEST = ROOT / "generated" / "manifest.json"
DOC_DIR = ROOT / "docs" / "rules"
PRIMARY = ROOT / "config" / "service_primary.yaml"

try:
    import yaml
except Exception as exc:
    print(f"ERROR: PyYAML unavailable: {exc}", file=sys.stderr)
    sys.exit(2)

idx = yaml.safe_load(INDEX.read_text(encoding="utf-8")) or {}
entries = idx.get("entries") or []
# Prefer full distribution index; if empty fall back to service_primary keys
service_ids = [str(e.get("id")) for e in entries if e.get("id") is not None]
if not service_ids and PRIMARY.exists():
    reg = yaml.safe_load(PRIMARY.read_text(encoding="utf-8")) or {}
    service_ids = sorted((reg.get("services") or {}).keys())

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
generated = manifest.get("files") or []
generated_paths = {item.get("file") for item in generated if item.get("file")}
clients = set(manifest.get("client_rule_directories") or [])
EXPECTED_CLIENTS = {"egern", "loon", "mihomo", "quantumultx", "shadowrocket", "singbox", "surge"}

legacy_markers = (
    "generated/sing-box",
    "generated/quantumult-x",
    "database/" + "domains/",
    "scripts/generate_docs.py",
    "scripts/generate_rule_pages.py",
)
legacy_service_prefix = "database/" + "services/"

errors: list[str] = []
if clients != EXPECTED_CLIENTS:
    errors.append(f"unexpected client directory contract: {sorted(clients)}")

# Map service_id -> client relative paths under directory_layout_v2
# e.g. mihomo/alibaba/taobao/taobao.yaml when parts[2]==service_id or stem==service_id
paths_by_service: dict[str, set[str]] = {}
for item in generated:
    if item.get("kind") != "client_rules":
        continue
    path = item.get("file") or ""
    parts = path.split("/")
    if len(parts) < 4 or parts[0] not in EXPECTED_CLIENTS:
        continue
    # provider/service/filename
    service_dir = parts[2]
    stem = Path(parts[-1]).stem
    for key in {service_dir, stem}:
        paths_by_service.setdefault(key, set()).add(path)

id_patterns = (
    lambda sid: re.compile(r"Service ID\s*\|\s*`" + re.escape(sid) + r"`\s*\|"),
    lambda sid: re.compile(r"Rule ID\s*\|\s*`" + re.escape(sid) + r"`\s*\|"),
)

for service_id in sorted(set(service_ids)):
    doc = DOC_DIR / f"{service_id}.md"
    if not doc.is_file():
        errors.append(f"missing current service doc: {doc.relative_to(ROOT)}")
        continue
    text = doc.read_text(encoding="utf-8", errors="strict")
    for marker in legacy_markers:
        if marker in text:
            errors.append(
                f"{doc.relative_to(ROOT)} contains forbidden legacy marker: {marker}"
            )
    for line in text.splitlines():
        if legacy_service_prefix in line and not (
            "Legacy" in line or "legacy" in line or "不是" in line or "not" in line
        ):
            errors.append(
                f"{doc.relative_to(ROOT)} uses the retired service-source path as a current reference: {line.strip()}"
            )

    if not any(p(service_id).search(text) for p in id_patterns):
        errors.append(
            f"{doc.relative_to(ROOT)} does not declare Service ID or Rule ID {service_id}"
        )

    expected = paths_by_service.get(service_id) or set()
    # Only require mention when manifest has client rules for this id
    if expected:
        # At least one client path must appear (full relative path as used in Raw table)
        if not any(path in text for path in expected):
            # also accept raw.githubusercontent URLs containing the path
            if not any(path in text for path in expected):
                errors.append(
                    f"{doc.relative_to(ROOT)} does not mention any materialized client path for {service_id}"
                )

    for candidate in re.findall(
        r"generated/((?:egern|loon|mihomo|quantumultx|shadowrocket|singbox|surge)/[A-Za-z0-9_.\-/]+\.(?:yaml|json|list))",
        text,
    ):
        rel = candidate
        parts = rel.split("/")
        if len(parts) >= 4 and parts[0] in EXPECTED_CLIENTS and rel not in generated_paths:
            errors.append(
                f"{doc.relative_to(ROOT)} references non-manifest generated path: {rel}"
            )

index = DOC_DIR / "README.md"
if not index.is_file():
    errors.append("missing docs/rules/README.md")
else:
    index_text = index.read_text(encoding="utf-8", errors="strict")
    missing_links = 0
    for service_id in sorted(set(service_ids)):
        if f"({service_id}.md)" not in index_text:
            missing_links += 1
            if missing_links <= 30:
                errors.append(f"rules index missing current service link: {service_id}")
    if missing_links > 30:
        errors.append(f"rules index missing current service link: ... {missing_links - 30} more")

if errors:
    print("DOC SSOT GATE: FAIL")
    for err in errors[:200]:
        print(f"- {err}")
    if len(errors) > 200:
        print(f"- ... {len(errors) - 200} more")
    sys.exit(1)

print(f"DOC SSOT GATE: PASS ({len(set(service_ids))} indexed services)")
