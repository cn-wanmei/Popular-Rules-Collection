#!/usr/bin/env python3
"""Emit DNS recommendation fragment from resolution_policy + server registry."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
POL = ROOT / "config" / "resolution_policy.yaml"
SRV = ROOT / "database" / "policies" / "dns" / "servers.yaml"
OUT = ROOT / "generated" / "resolution"


def main() -> int:
    pol = yaml.safe_load(POL.read_text(encoding="utf-8")) if POL.exists() else {}
    srv = yaml.safe_load(SRV.read_text(encoding="utf-8")) if SRV.exists() else {}
    servers = {s["id"]: s for s in (srv.get("servers") or []) if isinstance(s, dict) and s.get("id")}
    intents = pol.get("intents") or {}
    frag = {"version": 1, "routing_orthogonal": True, "intents": {}}
    for intent, conf in intents.items():
        if not isinstance(conf, dict):
            continue
        ids = conf.get("example_servers") or []
        frag["intents"][intent] = {
            "preferred_tags": conf.get("preferred_tags") or [],
            "servers": [servers[i] for i in ids if i in servers],
            "note": conf.get("note"),
        }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "recommendations.json").write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# DNS Resolution Recommendations (not routing actions)", ""]
    for intent, body in frag["intents"].items():
        lines.append(f"## {intent}")
        for s in body.get("servers") or []:
            lines.append(f"- {s.get('id')}: {s.get('address')} ({s.get('protocol')})")
        lines.append("")
    (OUT / "recommendations.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[resolution_fragment] intents={len(frag['intents'])} → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
