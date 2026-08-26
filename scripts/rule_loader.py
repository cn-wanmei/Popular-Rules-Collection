#!/usr/bin/env python3
"""rule_loader — sole Canonical Rule input layer for all client builders.

Contract
--------
Sources (merged, not overwritten):
  1. database/services/{id}.yaml  → typed rules (domain / domain_suffix /
     domain_keyword / domain_regex / ip_cidr / ip_cidr6)
  2. database/domains/{id}.txt    → each non-empty line → domain_suffix
  3. database/ips/{id}.txt        → each line → ip_cidr or ip_cidr6 (by ':')

Dedup key: (rule_type, normalized_value)
  - domain* types: value.lower()
  - ip*: value as-is
  - domain and domain_suffix with the same string are DISTINCT rules

Builders must only consume this module (or its buckets). Skip when total == 0.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"

DOMAIN_TYPES = ("domain", "domain_suffix", "domain_keyword", "domain_regex")
IP_TYPES = ("ip_cidr", "ip_cidr6")
ALL_TYPES = DOMAIN_TYPES + IP_TYPES


def _empty_bucket(sid: str, name: str, category: str) -> dict[str, Any]:
    return {
        "id": sid,
        "name": name,
        "category": category,
        "domain": [],
        "domain_suffix": [],
        "domain_keyword": [],
        "domain_regex": [],
        "ip_cidr": [],
        "ip_cidr6": [],
    }


def _dedup_key(rule_type: str, value: str) -> str:
    if rule_type.startswith("domain"):
        return f"{rule_type}\0{value.lower()}"
    return f"{rule_type}\0{value}"


def _add(bucket: dict[str, Any], seen: set[str], rule_type: str, value: str) -> None:
    value = (value or "").strip()
    if not value or rule_type not in bucket:
        return
    key = _dedup_key(rule_type, value)
    if key in seen:
        return
    seen.add(key)
    bucket[rule_type].append(value)


def _load_one(path: Path) -> dict[str, Any] | None:
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    sid = str(doc.get("id") or path.stem)
    name = str(doc.get("name") or sid)
    category = str(doc.get("category") or "other")
    bucket = _empty_bucket(sid, name, category)
    seen: set[str] = set()

    for r in doc.get("rules") or []:
        if not isinstance(r, dict):
            continue
        t = (r.get("type") or "").lower().replace("-", "_")
        v = r.get("value")
        if t == "ipcidr":
            t = "ip_cidr"
        elif t == "ipcidr6":
            t = "ip_cidr6"
        if t in ALL_TYPES and v:
            _add(bucket, seen, t, str(v))

    dfile = DOMAINS / f"{sid}.txt"
    if dfile.exists():
        for line in dfile.read_text(encoding="utf-8", errors="replace").splitlines():
            d = line.strip()
            if not d or d.startswith("#"):
                continue
            if d.startswith("+."):
                d = d[2:]
            elif d.startswith("."):
                d = d[1:]
            _add(bucket, seen, "domain_suffix", d)

    ifile = IPS / f"{sid}.txt"
    if ifile.exists():
        for line in ifile.read_text(encoding="utf-8", errors="replace").splitlines():
            ip = line.strip()
            if not ip or ip.startswith("#"):
                continue
            t = "ip_cidr6" if ":" in ip.split("/")[0] else "ip_cidr"
            _add(bucket, seen, t, ip)

    total = sum(len(bucket[k]) for k in ALL_TYPES)
    if total == 0:
        return None
    bucket["total"] = total
    return bucket


def load_service_rules(service_id: str | None = None) -> list[dict[str, Any]]:
    """Load one or all services as Canonical Rule buckets (skip empty)."""
    out: list[dict[str, Any]] = []
    if service_id:
        path = SERVICES / f"{service_id}.yaml"
        if path.exists():
            b = _load_one(path)
            if b:
                out.append(b)
        return out

    if not SERVICES.is_dir():
        return out
    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        b = _load_one(path)
        if b:
            out.append(b)
    return out


def bucket_total(bucket: dict[str, Any]) -> int:
    return int(bucket.get("total") or sum(len(bucket.get(k) or []) for k in ALL_TYPES))
