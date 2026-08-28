#!/usr/bin/env python3
"""coverage_matrix.py — Phase 3B Coverage Matrix (machine-readable first)."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
CLIENTS = ("mihomo", "sing-box", "surge", "shadowrocket", "quantumult-x", "egern", "loon")


def load_yaml(p: Path) -> dict:
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def count_lines(p: Path) -> int:
    if not p.exists():
        return 0
    n = 0
    with p.open(encoding="utf-8", errors="replace") as f:
        for ln in f:
            s = ln.strip()
            if s and not s.startswith("#"):
                n += 1
    return n


def load_primary() -> dict[str, dict]:
    services: dict = {}
    for name in ("service_primary.yaml", "service_primary_extra.yaml"):
        doc = load_yaml(ROOT / "config" / name)
        services.update(doc.get("services") or {})
        for sid, ov in (doc.get("aggregate_overrides") or {}).items():
            base = dict(services.get(sid) or {})
            base.update(ov or {})
            services[sid] = base
    return services


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = ap.parse_args()
    day = REPORTS / args.date
    day.mkdir(parents=True, exist_ok=True)

    primary = load_primary()
    intentional = load_yaml(ROOT / "config" / "intentional_unmaterialized.yaml")
    intent_map = intentional.get("services") or {}

    geosite_direct = count_lines(ROOT / "database/geosite/direct.txt")
    geosite_proxy = count_lines(ROOT / "database/geosite/proxy.txt")
    geoip_cn = count_lines(ROOT / "database/geoip/cn.txt")
    lan = count_lines(ROOT / "database/network/lan.txt")
    asn_doc = load_yaml(ROOT / "database/asn/metadata.yaml")
    asn_n = len(asn_doc.get("asns") or [])

    rows = []
    mat_n = dom_n = ip_n = client_ok = 0
    for sid in sorted(primary.keys()):
        meta = primary[sid] or {}
        svc_path = ROOT / "database/services" / f"{sid}.yaml"
        dom_path = ROOT / "database/domains" / f"{sid}.txt"
        ip_path = ROOT / "database/ips" / f"{sid}.txt"
        materialized = svc_path.exists()
        d_count = count_lines(dom_path)
        rules_n = 0
        if materialized:
            try:
                doc = yaml.safe_load(svc_path.read_text(encoding="utf-8")) or {}
                rules_n = len(doc.get("rules") or [])
            except Exception:
                pass
        domain_avail = d_count > 0 or rules_n > 0
        i_count = count_lines(ip_path)
        ip_avail = i_count > 0
        if materialized:
            mat_n += 1
        if domain_avail:
            dom_n += 1
        if ip_avail:
            ip_n += 1

        clients = {}
        any_client = False
        for c in CLIENTS:
            candidates = [
                ROOT / "generated" / c / f"{sid}.yaml",
                ROOT / "generated" / c / f"{sid}.list",
                ROOT / "generated" / c / f"{sid}.json",
                ROOT / "generated" / c / f"{sid}.conf",
            ]
            ok = any(p.exists() and p.stat().st_size > 0 for p in candidates)
            if not ok:
                d = ROOT / "generated" / c
                if d.is_dir():
                    ok = any(
                        p.is_file() and p.stat().st_size > 0 and sid in p.stem
                        for p in d.iterdir()
                    )
            clients[c] = ok
            if ok:
                any_client = True
        if any_client:
            client_ok += 1

        intent = intent_map.get(sid)
        reason = None
        if isinstance(intent, dict):
            reason = intent.get("code") or intent.get("reason")
        elif intent:
            reason = str(intent)

        rows.append(
            {
                "service": sid,
                "primary_category": meta.get("primary_category"),
                "service_type": meta.get("service_type", "service"),
                "materialized": materialized,
                "domain": {"available": domain_avail, "count": d_count + rules_n},
                "ip": {"available": ip_avail, "count": i_count},
                "geosite": {"available": geosite_direct > 0 or geosite_proxy > 0},
                "geoip": {"available": geoip_cn > 0},
                "asn": {"available": asn_n > 0},
                "lan": {"available": lan > 0},
                "clients": clients,
                "client_any": any_client,
                "intentional_code": reason,
            }
        )

    summary = {
        "date": args.date,
        "registered": len(primary),
        "materialized": mat_n,
        "with_domain": dom_n,
        "with_ip": ip_n,
        "with_any_client": client_ok,
        "dataset_globals": {
            "geosite_direct": geosite_direct,
            "geosite_proxy": geosite_proxy,
            "geoip_cn": geoip_cn,
            "lan": lan,
            "asn_entries": asn_n,
        },
        "services": rows,
    }
    (day / "coverage.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (REPORTS / "latest_coverage.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    lines = [
        f"# Coverage Matrix ({args.date})",
        "",
        f"- registered: **{len(primary)}**",
        f"- materialized: **{mat_n}**",
        f"- with domain rules: **{dom_n}**",
        f"- with IP sidecar: **{ip_n}**",
        f"- with ≥1 client artifact: **{client_ok}**",
        "",
        "| service | domain | ip | clients | intentional |",
        "|---------|--------|----|---------|-------------|",
    ]
    for r in rows:
        ncli = sum(1 for v in r["clients"].values() if v)
        lines.append(
            f"| {r['service']} | {'Y' if r['domain']['available'] else 'n'} "
            f"({r['domain']['count']}) | {'Y' if r['ip']['available'] else 'n'} "
            f"({r['ip']['count']}) | {ncli}/{len(CLIENTS)} | {r['intentional_code'] or ''} |"
        )
    (day / "coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"[coverage_matrix] registered={len(primary)} materialized={mat_n} "
        f"domain={dom_n} ip={ip_n} clients={client_ok}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
