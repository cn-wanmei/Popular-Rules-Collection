#!/usr/bin/env python3
"""Build Canonical Rule Store from database/services (dual-write)."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.core.models.rule import identity_key  # noqa: E402

SERVICES = ROOT / "database" / "services"
OUT = ROOT / "generated" / "canonical"


def rule_id(typ: str, value: str) -> str:
    return hashlib.sha256(identity_key(typ, value).encode()).hexdigest()[:16]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rules: dict[str, dict] = {}
    memberships: list[dict] = []
    for p in sorted(SERVICES.glob("*.yaml")):
        if p.name.startswith("example"):
            continue
        try:
            doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        sid = doc.get("id") or p.stem
        for r in doc.get("rules") or []:
            if not isinstance(r, dict):
                continue
            typ, val = r.get("type"), r.get("value")
            if not typ or not val:
                continue
            typ, val = str(typ), str(val)
            rid = rule_id(typ, val)
            if rid not in rules:
                rules[rid] = {"id": rid, "type": typ, "value": val, "identity_key": identity_key(typ, val)}
            memberships.append({"service": sid, "rule_id": rid})
    with (OUT / "rules.jsonl").open("w", encoding="utf-8") as f:
        for rid in sorted(rules.keys()):
            f.write(json.dumps(rules[rid], ensure_ascii=False) + "\n")
    with (OUT / "service_rules.jsonl").open("w", encoding="utf-8") as f:
        for m in memberships:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema": "canonical_store_v1",
        "unique_rules": len(rules),
        "memberships": len(memberships),
        "source": "database/services",
        "note": "dual-write; services yaml remains builder authority until cutover",
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"[canonical_store] unique_rules={len(rules)} memberships={len(memberships)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
