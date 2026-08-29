#!/usr/bin/env python3
"""icon_coverage.py — Icon Coverage stats."""
from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "assets" / "icons"
MAN = ICON / "manifest.yaml"
REG = ICON / "registry.yaml"
OUT_J = ROOT / "reports" / "latest_icon_coverage.json"
OUT_M = ROOT / "reports" / "latest_icon_coverage.md"


def load(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}


def main() -> int:
    man = load(MAN) or {}
    reg = load(REG) or {}
    icons = man.get("icons") or {}
    smap = man.get("service_icon_map") or {}
    services = reg.get("services") or {}

    status_c = Counter()
    prov_c = Counter()
    type_c = Counter()
    for k, meta in icons.items():
        if not isinstance(meta, dict):
            continue
        status_c[str(meta.get("status") or "unknown")] += 1
        prov_c[str(((meta.get("source") or {}).get("provenance") or "unknown"))] += 1
        type_c[str(meta.get("type") or "unknown")] += 1

    mapped = len(smap)
    placeholder = sum(1 for v in smap.values() if str(v) == "placeholder")
    real = mapped - placeholder
    verified = status_c.get("verified", 0)
    sourced = status_c.get("sourced", 0)
    png_ok = sum(
        1 for k in icons
        if (ICON / f"png/256/{k}.png").exists() and (ICON / f"png/256/{k}.png").stat().st_size > 200
    )

    doc = {
        "date": str(date.today()),
        "service_map_entries": mapped,
        "icon_entities": len(icons),
        "registry_services": len(services),
        "with_real_icon": real,
        "placeholder_decisions": placeholder,
        "verified_entities": verified,
        "sourced_entities": sourced,
        "png_256_ok": png_ok,
        "by_status": dict(status_c),
        "by_provenance": dict(prov_c),
        "by_type": dict(type_c),
        "non_placeholder_pct": round(100.0 * real / max(mapped, 1), 2),
    }
    OUT_J.parent.mkdir(parents=True, exist_ok=True)
    OUT_J.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        f"# Icon Coverage {doc['date']}",
        "",
        f"- service_map_entries: **{mapped}**",
        f"- with_real_icon: **{real}** ({doc['non_placeholder_pct']}%)",
        f"- placeholder_decisions: **{placeholder}**",
        f"- verified / sourced: **{verified}** / **{sourced}**",
        f"- png_256_ok: **{png_ok}**",
        "",
        "## Provenance",
        "",
    ]
    for k, v in sorted(prov_c.items(), key=lambda x: -x[1]):
        lines.append(f"- {k}: {v}")
    OUT_M.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[icon_coverage] map={mapped} real={real} placeholder={placeholder} png256={png_ok}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
