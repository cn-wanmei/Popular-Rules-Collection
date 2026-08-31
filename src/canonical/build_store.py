#!/usr/bin/env python3
"""Build Canonical Rule Store (streaming dual-write)."""
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
    seen: set[str] = set()
    n_rules = n_mem = 0
    with (OUT / "rules.jsonl").open("w", encoding="utf-8") as fr, (OUT / "service_rules.jsonl").open(
        "w", encoding="utf-8"
    ) as fm:
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
                if rid not in seen:
                    seen.add(rid)
                    fr.write(
                        json.dumps(
                            {"id": rid, "type": typ, "value": val, "identity_key": identity_key(typ, val)},
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
                    n_rules += 1
                fm.write(json.dumps({"service": sid, "rule_id": rid}, ensure_ascii=False) + "\n")
                n_mem += 1
    (OUT / "manifest.json").write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "schema": "canonical_store_v1",
                "unique_rules": n_rules,
                "memberships": n_mem,
                "source": "database/services",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[canonical_store] unique_rules={n_rules} memberships={n_mem}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
