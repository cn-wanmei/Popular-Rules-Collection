#!/usr/bin/env python3
"""validate_ip_registry.py — hard contract for sources/ip_registry.yaml.

Blocks dangerous mappings:
  country/carrier → product service
  provider → Amazon/Google/Microsoft product ids
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "sources" / "ip_registry.yaml"
PRIM = ROOT / "config" / "service_primary.yaml"
EXTRA = ROOT / "config" / "service_primary_extra.yaml"

VALID_SCOPES = frozenset(
    {"service", "provider", "country", "carrier", "infrastructure"}
)

COUNTRY_IDS = frozenset({"china"})
CARRIER_IDS = frozenset({"chinamobile", "chinaunicom", "chinatelecom"})
INFRA_IDS = frozenset({"private", "stun"})

PROVIDER_FORBIDDEN_TARGETS = frozenset(
    {
        "amazon",
        "google",
        "microsoft",
        "apple",
        "netflix",
        "openai",
        "discord",
        "facebook",
        "meta",
        "alibaba",
        "tencent",
        "bytedance",
    }
)


def load_primary_ids() -> set[str]:
    services: dict = {}
    for p in (PRIM, EXTRA):
        if not p.exists():
            continue
        doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        services.update(doc.get("services") or {})
        for sid, ov in (doc.get("aggregate_overrides") or {}).items():
            base = dict(services.get(sid) or {})
            base.update(ov or {})
            services[sid] = base
    return set(services.keys())


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    if not REG.exists():
        print("[validate_ip_registry] no ip_registry.yaml — skip")
        return 0

    cfg = yaml.safe_load(REG.read_text(encoding="utf-8")) or {}
    sources = cfg.get("sources") or []
    if not isinstance(sources, list):
        print("[validate_ip_registry] sources must be a list")
        return 1

    primary = load_primary_ids()
    seen_ids: set[str] = set()

    for i, src in enumerate(sources):
        if not isinstance(src, dict):
            errors.append(f"sources[{i}]: must be object")
            continue
        sid = str(src.get("id") or "").strip()
        if not sid:
            errors.append(f"sources[{i}]: missing id")
            continue
        if sid in seen_ids:
            errors.append(f"{sid}: duplicate id")
        seen_ids.add(sid)

        scope = str(src.get("scope") or "").strip().lower()
        if scope not in VALID_SCOPES:
            errors.append(f"{sid}: invalid scope '{scope}'")
        maps_to = str(src.get("maps_to") or "").strip()
        enabled = bool(src.get("enabled"))

        if enabled and not maps_to:
            errors.append(f"{sid}: enabled source requires maps_to")

        if not maps_to:
            continue

        if maps_to not in primary:
            errors.append(f"{sid}: maps_to '{maps_to}' not in service_primary")

        if scope == "country":
            if maps_to not in COUNTRY_IDS and maps_to not in CARRIER_IDS:
                errors.append(
                    f"{sid}: scope=country maps_to '{maps_to}' "
                    f"not in country/carrier allowlist"
                )
        elif scope == "carrier":
            if maps_to not in CARRIER_IDS:
                if maps_to not in COUNTRY_IDS:
                    errors.append(
                        f"{sid}: scope=carrier maps_to '{maps_to}' "
                        f"not in carrier/country allowlist"
                    )
                else:
                    warnings.append(
                        f"{sid}: carrier source folded into country id '{maps_to}'"
                    )
        elif scope == "provider":
            if maps_to in PROVIDER_FORBIDDEN_TARGETS:
                errors.append(
                    f"{sid}: scope=provider must not map to product service '{maps_to}'"
                )
            warnings.append(
                f"{sid}: provider scope — ensure maps_to is infra-only, not product"
            )
        elif scope == "infrastructure":
            if maps_to not in INFRA_IDS and maps_to not in primary:
                errors.append(f"{sid}: infrastructure maps_to '{maps_to}' unknown")
        elif scope == "service":
            if maps_to != sid and not src.get("notes"):
                warnings.append(
                    f"{sid}: service scope should document ownership evidence in notes"
                )

        fetch = src.get("fetch") or {}
        if enabled and (not fetch.get("type") or not src.get("path")):
            errors.append(f"{sid}: enabled source needs fetch.type and path")

    print(
        f"[validate_ip_registry] sources={len(sources)} "
        f"errors={len(errors)} warnings={len(warnings)}"
    )
    for e in errors[:40]:
        print(f"  ERROR {e}")
    for w in warnings[:20]:
        print(f"  WARN  {w}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
