#!/usr/bin/env python3
"""dataset_quality.py — Phase 3A + Network Dataset Quality Gate."""
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

EXPECTED_EXPORTS = [
    ("database/network/lan.txt", "generated/network/lan.txt"),
    ("database/geosite/direct.txt", "generated/geosite/direct.txt"),
    ("database/geosite/proxy.txt", "generated/geosite/proxy.txt"),
    ("database/geoip/cn.txt", "generated/geoip/cn.txt"),
    ("database/provider/cloudflare.txt", "generated/provider/cloudflare.txt"),
]

DOMAIN_RE = re.compile(
    r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$", re.I
)


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


def check_domain_syntax(lines: list[str], limit: int = 300) -> int:
    bad = 0
    for ln in lines[:limit]:
        s = ln.lstrip(".")
        if not DOMAIN_RE.match(s) and "*" not in s:
            if "." not in s:
                continue
            bad += 1
    return bad


def check_clash_list(path: Path) -> list[str]:
    issues = []
    if not path.exists():
        return [f"missing {path}"]
    lines = load_lines(path)
    if not lines:
        return [f"empty {path}"]
    ok_prefix = ("DOMAIN-SUFFIX,", "DOMAIN,", "DOMAIN-KEYWORD,", "IP-CIDR,", "IP-CIDR6,")
    bad = 0
    for ln in lines[:200]:
        if not ln.startswith(ok_prefix):
            bad += 1
    if bad > 5:
        issues.append(f"format issues in {path.relative_to(ROOT)}: bad_prefix={bad}")
    return issues


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
        "database/provider/*.txt",
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

    for p in ROOT.glob("database/geosite/*.txt"):
        lines = load_lines(p)
        if len(lines) < 10:
            continue
        bad = check_domain_syntax(lines)
        if bad > 20:
            warn.append(f"domain syntax sample: {p.relative_to(ROOT)} bad={bad}")

    for src_rel, dest_rel in EXPECTED_EXPORTS:
        src, dest = ROOT / src_rel, ROOT / dest_rel
        if src.exists() and load_lines(src):
            if not dest.exists() or not load_lines(dest):
                hard.append(f"generated missing/empty: {dest_rel} (source {src_rel})")
            else:
                info.append(f"export ok {dest_rel}")

    for rel in (
        "generated/geosite/direct_mihomo.list",
        "generated/geosite/proxy_mihomo.list",
        "generated/geoip/cn_mihomo.list",
    ):
        p = ROOT / rel
        if p.exists():
            for issue in check_clash_list(p):
                warn.append(issue)
        src_map = {
            "generated/geosite/direct_mihomo.list": "database/geosite/direct.txt",
            "generated/geosite/proxy_mihomo.list": "database/geosite/proxy.txt",
            "generated/geoip/cn_mihomo.list": "database/geoip/cn.txt",
        }
        if (ROOT / src_map[rel]).exists() and not p.exists():
            warn.append(f"mihomo list missing: {rel}")

    if (ROOT / "database/provider").exists():
        for p in (ROOT / "database/provider").glob("*.txt"):
            info.append(f"provider dataset present: {p.name} count={len(load_lines(p))}")

    asn = ROOT / "database/asn/metadata.yaml"
    if asn.exists():
        try:
            doc = yaml.safe_load(asn.read_text(encoding="utf-8")) or {}
            n = len(doc.get("asns") or [])
            if n == 0:
                warn.append("asn metadata empty")
            else:
                info.append(f"asn_metadata entries={n}")
        except Exception as e:
            hard.append(f"asn metadata invalid YAML: {e}")

    for sub in ("direct", "proxy", "dns"):
        d = ROOT / "database/policies" / sub
        if d.is_dir():
            files = list(d.glob("*"))
            if not files:
                warn.append(f"policy dir empty: {sub}")
            else:
                info.append(f"policy {sub} files={len(files)}")

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
        "informational": info[:60],
        "counts": {"hard": len(hard), "warn": len(warn), "info": len(info)},
        "thresholds": {
            "shrink_hard": SHRINK_HARD,
            "shrink_warn": SHRINK_WARN,
            "growth_warn": GROWTH_WARN,
        },
        "scope": "service_adjacent+network_datasets",
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
