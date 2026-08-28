#!/usr/bin/env python3
"""dataset_quality.py — Phase 3A Dataset Quality Gate.

Hard Fail / Warning / Informational tiers.
Does not modify Builders or Primary.

Writes reports/<date>/dataset_quality.json
Exit code 1 only on Hard Fail.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

SHRINK_HARD = 0.90
SHRINK_WARN = 0.30
GROWTH_WARN = 3.0

REQUIRED_NONEMPTY = [
    "database/network/lan.txt",
    "database/network/private.txt",
]

OPTIONAL_NONEMPTY_IF_PRESENT = [
    "database/geosite/direct.txt",
    "database/geosite/proxy.txt",
    "database/geoip/cn.txt",
]


def load_lines(path: Path) -> list[str]:
    try:
        return [
            ln.strip()
            for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()
            if ln.strip() and not ln.strip().startswith("#")
        ]
    except OSError:
        return []


def check_cidr_syntax(lines: list[str], limit: int = 500) -> int:
    """Return invalid CIDR count in sample; -1 if not a CIDR-like file."""
    bad = 0
    cidr_re = re.compile(r"^([0-9a-fA-F:.]+)/\d{1,3}$")
    bare_ip = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$|^[0-9a-fA-F:]+$")
    for ln in lines[:limit]:
        if "/" in ln:
            if not cidr_re.match(ln):
                try:
                    import ipaddress

                    ipaddress.ip_network(ln, strict=False)
                except Exception:
                    bad += 1
        elif bare_ip.match(ln):
            continue
        else:
            return -1
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    day = REPORTS / args.date
    day.mkdir(parents=True, exist_ok=True)

    hard: list[str] = []
    warn: list[str] = []
    info: list[str] = []

    for rel in REQUIRED_NONEMPTY:
        p = ROOT / rel
        lines = load_lines(p) if p.exists() else []
        if not p.exists():
            hard.append(f"missing required dataset: {rel}")
        elif not lines:
            hard.append(f"empty dataset: {rel}")
        else:
            info.append(f"ok {rel} count={len(lines)}")

    for rel in OPTIONAL_NONEMPTY_IF_PRESENT:
        p = ROOT / rel
        if p.exists():
            lines = load_lines(p)
            if not lines:
                hard.append(f"empty dataset: {rel}")
            else:
                info.append(f"ok {rel} count={len(lines)}")

    for pattern in (
        "database/geoip/*.txt",
        "database/network/*.txt",
        "database/ips/*.txt",
    ):
        for p in ROOT.glob(pattern):
            if not p.is_file():
                continue
            lines = load_lines(p)
            if not lines:
                continue
            bad = check_cidr_syntax(lines)
            if bad == -1:
                continue
            if bad > 0 and bad / max(min(len(lines), 500), 1) > 0.05:
                hard.append(f"syntax invalid sample: {p.relative_to(ROOT)} bad={bad}")
            elif bad > 0:
                warn.append(f"syntax issues: {p.relative_to(ROOT)} bad={bad}")

    if (ROOT / "database/network/lan.txt").exists():
        gen = ROOT / "generated/network/lan.txt"
        if not gen.exists() or gen.stat().st_size == 0:
            hard.append("generated missing/empty: generated/network/lan.txt")
        else:
            info.append("generated network/lan present")

    prov_dir = ROOT / "database" / "ips_provenance"
    china = ROOT / "database" / "ips" / "china.txt"
    if china.exists() and len(load_lines(china)) > 100:
        if not (prov_dir / "china.json").exists():
            warn.append("provenance missing for large database/ips/china.txt")
        else:
            info.append("provenance ok: ips/china")

    ds_prov = ROOT / "database" / "datasets_provenance"
    if (ROOT / "database/geosite/direct.txt").exists() and len(
        load_lines(ROOT / "database/geosite/direct.txt")
    ) > 1000:
        if not (ds_prov / "geosite-direct.json").exists():
            warn.append("provenance missing: geosite-direct (datasets_provenance)")

    mmdb = ROOT / "generated/mmdb/Country.mmdb"
    meta = ROOT / "generated/mmdb/Country.meta.json"
    if mmdb.exists():
        if mmdb.stat().st_size < 1000:
            hard.append("checksum/size anomaly: Country.mmdb too small")
        elif meta.exists():
            try:
                m = json.loads(meta.read_text(encoding="utf-8"))
                if m.get("bytes") and abs(m["bytes"] - mmdb.stat().st_size) > 0:
                    hard.append("checksum mismatch: Country.mmdb size != meta.bytes")
                else:
                    info.append("mmdb artifact ok")
            except Exception:
                warn.append("mmdb meta unreadable")
        else:
            warn.append("mmdb present but meta.json missing")

    diff_path = day / "dataset_diff.json"
    if diff_path.exists():
        try:
            diff_doc = json.loads(diff_path.read_text(encoding="utf-8"))
        except Exception:
            diff_doc = {}
        for rel, d in (diff_doc.get("diffs") or {}).items():
            sr = float(d.get("shrink_ratio") or 0)
            gr = float(d.get("growth_ratio") or 0)
            oc = int(d.get("old_count") or 0)
            nc = int(d.get("new_count") or 0)
            if d.get("status") == "missing" and oc >= 50:
                hard.append(f"dataset disappeared: {rel} old_count={oc}")
            if oc >= 50 and sr >= SHRINK_HARD:
                hard.append(
                    f"unexpected shrink>={int(SHRINK_HARD*100)}%: {rel} "
                    f"{oc}->{nc} (-{sr:.0%})"
                )
            elif oc >= 50 and sr >= SHRINK_WARN:
                warn.append(
                    f"shrink>={int(SHRINK_WARN*100)}%: {rel} {oc}->{nc} (-{sr:.0%})"
                )
            if oc >= 100 and gr >= GROWTH_WARN:
                warn.append(
                    f"unexpected growth>={int(GROWTH_WARN*100)}%: {rel} "
                    f"{oc}->{nc} (+{gr:.0%})"
                )
            if d.get("status") == "new" and nc > 0:
                info.append(f"new dataset: {rel} count={nc}")
    else:
        info.append("no dataset_diff.json — run dataset_diff.py first")

    health_path = ROOT / "sources" / "health.yaml"
    if health_path.exists():
        try:
            health = yaml.safe_load(health_path.read_text(encoding="utf-8")) or {}
            for sid, meta_h in (health.get("sources") or {}).items():
                st = (meta_h or {}).get("status")
                if st == "blocked":
                    warn.append(f"source blocked: {sid}")
                elif st == "degraded":
                    warn.append(f"source degraded: {sid}")
        except Exception:
            pass

    status = "fail" if hard else ("warn" if warn else "pass")
    if args.strict and warn:
        status = "fail"

    report = {
        "date": args.date,
        "status": status,
        "hard_fail": hard,
        "warnings": warn,
        "informational": info[:50],
        "counts": {"hard": len(hard), "warn": len(warn), "info": len(info)},
        "thresholds": {
            "shrink_hard": SHRINK_HARD,
            "shrink_warn": SHRINK_WARN,
            "growth_warn": GROWTH_WARN,
        },
    }
    (day / "dataset_quality.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(
        f"[dataset_quality] status={status} hard={len(hard)} "
        f"warn={len(warn)} info={len(info)}"
    )
    for e in hard[:20]:
        print(f"  HARD  {e}")
    for w in warn[:20]:
        print(f"  WARN  {w}")
    return 1 if status == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
