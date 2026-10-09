#!/usr/bin/env python3
"""Build policy-level client artifacts from routing Decision SSOT.

Does NOT replace per-service builders (openai/github/…).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEC = ROOT / "generated" / "routing"
OUT = ROOT / "generated" / "policies"


def load_list(name: str) -> list[str]:
    p = DEC / name
    if not p.exists():
        return []
    return [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]


def write_domain_suffix_list(path: Path, domains: list[str]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"DOMAIN-SUFFIX,{d}" for d in domains]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return len(lines)


def write_plain(path: Path, domains: list[str]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(domains) + ("\n" if domains else ""), encoding="utf-8")
    return len(domains)


def main() -> int:
    meta_path = DEC / "decisions.meta.json"
    if not meta_path.exists():
        print("[build_routing_policies] SKIP: no decisions.meta.json — run routing_emit first")
        return 0
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    direct = load_list("direct.list")
    proxy = load_list("proxy.list")
    reject = load_list("reject.list")

    stats = {
        "direct_plain": write_plain(OUT / "direct" / "domains.txt", direct),
        "proxy_plain": write_plain(OUT / "proxy" / "domains.txt", proxy),
        "reject_plain": write_plain(OUT / "reject" / "domains.txt", reject),
        "direct_mihomo": write_domain_suffix_list(OUT / "direct" / "mihomo.list", direct),
        "proxy_mihomo": write_domain_suffix_list(OUT / "proxy" / "mihomo.list", proxy),
        "reject_mihomo": write_domain_suffix_list(OUT / "reject" / "mihomo.list", reject),
    }

    manifest = {
        "decision_digest": meta.get("decision_digest"),
        "contract_version": meta.get("contract_version"),
        "engine": meta.get("engine"),
        "counts": meta.get("counts"),
        "artifacts": {
            "direct": ["generated/policies/direct/domains.txt", "generated/policies/direct/mihomo.list"],
            "proxy": ["generated/policies/proxy/domains.txt", "generated/policies/proxy/mihomo.list"],
            "reject": ["generated/policies/reject/domains.txt", "generated/policies/reject/mihomo.list"],
        },
        "note": "Policy-level only. Per-service subscriptions still from build_* + rule_loader.",
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[build_routing_policies] {stats} digest={(meta.get('decision_digest') or '')[:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
