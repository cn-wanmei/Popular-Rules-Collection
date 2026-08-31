#!/usr/bin/env python3
"""P1.3 Cross-client sample differential."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from rule_loader import load_service_rules  # noqa: E402

GEN = ROOT / "generated"
CORPUS = ["openai", "github", "telegram", "apple", "google"]
CLIENTS = {
    "mihomo": "mihomo",
    "surge": "surge",
    "shadowrocket": "shadowrocket",
    "quantumultx": "quantumultx",
    "loon": "loon",
    "egern": "egern",
    "singbox": "singbox",
}


def main() -> int:
    results = []
    hard = 0
    for sid in CORPUS:
        buckets = load_service_rules(sid)
        if not buckets:
            results.append({"service": sid, "status": "SKIP", "reason": "no rules"})
            continue
        client_status = {}
        for name, folder in CLIENTS.items():
            paths = list((GEN / folder).glob(f"{sid}.*")) if (GEN / folder).exists() else []
            present = len(paths) > 0
            client_status[name] = {"artifact": present, "files": [str(p.relative_to(ROOT)) for p in paths[:3]]}
            if not present:
                hard += 1
        results.append({
            "service": sid,
            "clients": client_status,
            "status": "PASS" if all(c["artifact"] for c in client_status.values()) else "GAP",
        })
    out = ROOT / "reports" / "cross_client_semantic.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"corpus": CORPUS, "results": results, "gaps": hard}, indent=2) + "\n", encoding="utf-8")
    print(f"[cross_client] services={len(CORPUS)} gaps={hard}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
