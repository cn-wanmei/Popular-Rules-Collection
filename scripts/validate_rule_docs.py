#!/usr/bin/env python3
"""Validate Documentation Layer v1 outputs against _index + manifest + icon policy."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
CLIENTS = ["egern", "loon", "mihomo", "quantumultx", "shadowrocket", "singbox", "surge"]
FORBIDDEN = ["assets/icons/v3", "assets/icons/v4", "assets/icons/v5", "Icon Library V4"]


def main() -> int:
    errors: list[str] = []
    idx = yaml.safe_load((ROOT / "rule" / "_index.yaml").read_text(encoding="utf-8"))
    man = json.loads((ROOT / "generated" / "manifest.json").read_text(encoding="utf-8"))
    run_id = idx.get("run_id")
    entries = idx.get("entries") or []
    man_files = {f["file"] for f in man.get("files") or [] if f.get("kind") == "client_rules"}

    # coverage
    for ent in entries:
        sid = str(ent["id"])
        p = ROOT / "docs" / "rules" / f"{sid}.md"
        if not p.exists():
            errors.append(f"missing docs/rules/{sid}.md")
            continue
        text = p.read_text(encoding="utf-8")
        if run_id and f"`{run_id}`" not in text and run_id not in text:
            errors.append(f"{sid}: run_id not found in docs/rules page")
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"{sid}: forbidden token {token}")
        # raw paths mentioned should exist if present as generated/...
        for c in CLIENTS:
            # look for main/generated/{client}/
            pass
        # extract relative generated paths from markdown backticks
        for m in re.finditer(
            r"generated/((?:egern|loon|mihomo|quantumultx|shadowrocket|singbox|surge)/[^`\s]+)",
            text,
        ):
            rel = m.group(1)
            if rel not in man_files:
                errors.append(f"{sid}: raw not in manifest: {rel}")

    # docs-index
    index_path = ROOT / "docs" / "generated" / "docs-index.json"
    if not index_path.exists():
        errors.append("missing docs/generated/docs-index.json")
    else:
        di = json.loads(index_path.read_text(encoding="utf-8"))
        if di.get("run_id") != run_id:
            errors.append(
                f"docs-index run_id mismatch: {di.get('run_id')} vs {run_id}"
            )
        if di.get("service_count") != len(entries):
            errors.append(
                f"docs-index service_count {di.get('service_count')} != entries {len(entries)}"
            )

    cat = ROOT / "docs" / "SERVICE_CATALOG.generated.md"
    if not cat.exists():
        errors.append("missing docs/SERVICE_CATALOG.generated.md")

    # compose existing icon gates if present
    for script in (
        "validate_icon_docs.py",
        "check_icon_pointers.py",
    ):
        sp = ROOT / "scripts" / script
        if sp.exists():
            r = subprocess.run([sys.executable, str(sp)], cwd=ROOT, capture_output=True, text=True)
            if r.returncode != 0:
                errors.append(f"{script} failed: {r.stdout or r.stderr}")

    if errors:
        print("validate_rule_docs: FAIL")
        for e in errors[:60]:
            print(" ", e)
        if len(errors) > 60:
            print(f"  ... +{len(errors)-60} more")
        return 1
    print(f"validate_rule_docs: OK ({len(entries)} services, run_id={run_id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
