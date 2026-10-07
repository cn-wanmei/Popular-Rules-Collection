#!/usr/bin/env python3
"""Report rule/_index.yaml entity counts vs Icon service-only coverage口径."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "rule" / "_index.yaml"


def main() -> int:
    data = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
    entries = data.get("entries") or []
    counts: Counter[str] = Counter()
    for item in entries:
        if not isinstance(item, dict):
            counts["invalid"] += 1
            continue
        counts[str(item.get("entity") or "service")] += 1
    service_n = counts.get("service", 0)
    total = sum(counts.values())
    report = {
        "schema": "entity_coverage_report_v1",
        "path": str(INDEX.relative_to(ROOT)),
        "by_entity": dict(counts),
        "total_entries": total,
        "icon_denominator_entity_service": service_n,
        "note": "Icon coverage uses entity=service only; do not compare to total_entries.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
