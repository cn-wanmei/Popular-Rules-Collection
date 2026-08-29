#!/usr/bin/env python3
"""validate_dataset_registry.py — contract for sources/datasets/*.yaml

Ensures network datasets stay isolated from Service Rules paths and
dangerous provider→product mappings are not declared here.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DS = ROOT / "sources" / "datasets"
VALID_KINDS = frozenset({"network", "geosite", "geoip", "asn", "policy", "provider", "binary"})
FORBIDDEN_SERVICE_COLLISION = frozenset(
    {"amazon", "google", "microsoft", "openai", "netflix", "discord"}
)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    if not DS.is_dir():
        print("[validate_dataset_registry] no sources/datasets — skip")
        return 0

    files = sorted(DS.glob("*.yaml"))
    for path in files:
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception as e:
            errors.append(f"{path.name}: invalid YAML ({e})")
            continue
        kind = str(doc.get("kind") or "").strip()
        if kind and kind not in VALID_KINDS:
            errors.append(f"{path.name}: invalid kind '{kind}'")
        for i, ds in enumerate(doc.get("datasets") or []):
            if not isinstance(ds, dict):
                errors.append(f"{path.name} datasets[{i}]: must be object")
                continue
            did = str(ds.get("id") or "")
            if not did:
                errors.append(f"{path.name} datasets[{i}]: missing id")
            scope = str(ds.get("scope") or "")
            if scope == "provider" and did in FORBIDDEN_SERVICE_COLLISION:
                errors.append(f"{did}: provider dataset must not use product service id")
            p = ds.get("path")
            if p and str(p).startswith("database/services"):
                errors.append(f"{did}: dataset path must not use database/services/")
            if p and str(p).startswith("database/ips/") and kind in ("geoip", "asn", "provider"):
                warnings.append(
                    f"{did}: prefer database/geoip|provider|asn over database/ips "
                    "(service sidecar is for verified service-owned ranges)"
                )
            if ds.get("enabled") and p:
                if not (ROOT / str(p)).exists() and not ds.get("artifact"):
                    warnings.append(f"{did}: enabled but path missing: {p}")

    print(
        f"[validate_dataset_registry] files={len(files)} "
        f"errors={len(errors)} warnings={len(warnings)}"
    )
    for e in errors[:30]:
        print(f"  ERROR {e}")
    for w in warnings[:20]:
        print(f"  WARN  {w}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
