#!/usr/bin/env python3
"""P1.2 Write generated/_meta/provenance.json."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated" / "_meta"
DEC = ROOT / "generated" / "routing" / "decisions.meta.json"
IR = ROOT / "generated" / "ir" / "manifest.json"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "routing_contract": 2,
        "decision": None,
        "universal_ir": None,
        "note": "Builders still use rule_loader; policy lists use decision SSOT",
    }
    if DEC.exists():
        meta["decision"] = json.loads(DEC.read_text())
    if IR.exists():
        meta["universal_ir"] = json.loads(IR.read_text())
    (OUT / "provenance.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"[provenance] wrote {OUT / 'provenance.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
