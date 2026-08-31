#!/usr/bin/env python3
"""Resolve multi-layer match hits to a single routing action (P1 decision engine)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "config" / "routing_contract.yaml"
OVERRIDES = ROOT / "database" / "policies" / "overrides"


def load_contract():
    c = yaml.safe_load(CONTRACT.read_text(encoding="utf-8")) or {}
    layers = {x["id"]: int(x.get("precedence") or 0) for x in (c.get("layers") or []) if isinstance(x, dict)}
    terminal = (c.get("terminal") or {}).get("unmatched") or "PROXY"
    return c, layers, terminal


def load_overrides() -> list[dict]:
    out = []
    for name, action in (
        ("force_direct.yaml", "DIRECT"),
        ("force_proxy.yaml", "PROXY"),
        ("force_reject.yaml", "REJECT"),
    ):
        p = OVERRIDES / name
        if not p.exists():
            continue
        doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        for e in doc.get("entries") or []:
            if not isinstance(e, dict):
                continue
            out.append(
                {
                    "layer": "explicit",
                    "action": action,
                    "match": e.get("match") or {},
                    "reason": e.get("reason"),
                }
            )
    return out


def resolve(hits: list[dict], layers: dict[str, int], terminal: str) -> dict:
    if not hits:
        return {"action": terminal, "layer": "fallback", "reason": "unmatched"}
    for h in hits:
        if str(h.get("action") or "").upper() == "REJECT":
            return {
                "action": "REJECT",
                "layer": h.get("layer"),
                "reason": "reject_vs_other",
                "from": h,
            }
    ranked = sorted(
        hits,
        key=lambda h: (-layers.get(str(h.get("layer") or ""), -1), str(h.get("id") or "")),
    )
    top = ranked[0]
    action = str(top.get("action") or terminal).upper()
    if action not in ("DIRECT", "PROXY", "REJECT"):
        action = terminal
    return {
        "action": action,
        "layer": top.get("layer"),
        "reason": "higher_precedence",
        "from": top,
        "considered": len(hits),
    }


def demo_cases(layers, terminal):
    cases = [
        {
            "name": "openai_vs_cn_geo",
            "hits": [
                {"layer": "geosite", "action": "DIRECT", "id": "china"},
                {"layer": "service", "action": "PROXY", "id": "openai"},
            ],
            "expect": "PROXY",
        },
        {
            "name": "lan_vs_proxy_category",
            "hits": [
                {"layer": "system", "action": "DIRECT", "id": "lan"},
                {"layer": "category", "action": "PROXY", "id": "proxy"},
            ],
            "expect": "DIRECT",
        },
        {
            "name": "reject_beats_proxy",
            "hits": [
                {"layer": "security", "action": "REJECT", "id": "malware"},
                {"layer": "service", "action": "PROXY", "id": "example"},
            ],
            "expect": "REJECT",
        },
        {
            "name": "geosite_before_geoip_same_intent",
            "hits": [
                {"layer": "geoip", "action": "DIRECT", "id": "cn"},
                {"layer": "geosite", "action": "PROXY", "id": "gfw"},
            ],
            "expect": "PROXY",
        },
        {"name": "empty", "hits": [], "expect": terminal},
    ]
    ok = 0
    for c in cases:
        r = resolve(c["hits"], layers, terminal)
        passed = r["action"] == c["expect"]
        ok += int(passed)
        print(f"  {'PASS' if passed else 'FAIL'}  {c['name']}: {r['action']} (expect {c['expect']})")
    return ok, len(cases)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--hits", default="", help='JSON list of {layer,action,id}')
    args = ap.parse_args()
    _, layers, terminal = load_contract()
    if args.demo or not args.hits:
        print(f"[routing_resolve] layers={len(layers)} terminal={terminal}")
        print(f"[routing_resolve] explicit override entries={len(load_overrides())}")
        ok, n = demo_cases(layers, terminal)
        print(f"[routing_resolve] demo {ok}/{n}")
        return 0 if ok == n else 1
    hits = json.loads(args.hits)
    print(json.dumps(resolve(hits, layers, terminal), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
