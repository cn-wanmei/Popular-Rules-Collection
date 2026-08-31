#!/usr/bin/env python3
"""Shared loader: database/services + domains/ips → typed rule buckets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.adapters._common.paths import repo_root
ROOT = repo_root()
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"

TYPED_KEYS = (
    "domain",
    "domain_suffix",
    "domain_keyword",
    "domain_regex",
    "ip_cidr",
    "ip_cidr6",
)


def _norm_key(rule_type: str, value: str) -> str:
    if rule_type.startswith("domain"):
        return value.lower().strip()
    return value.strip()


def load_service_rules(service_id: str | None = None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    paths = sorted(SERVICES.glob("*.yaml"))
    if service_id:
        paths = [SERVICES / f"{service_id}.yaml"]

    for path in paths:
        if not path.exists() or path.name.startswith("example"):
            continue
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        sid = doc.get("id") or path.stem

        lists: dict[str, list[str]] = {k: [] for k in TYPED_KEYS}
        seen: dict[str, set[str]] = {k: set() for k in TYPED_KEYS}

        def add(rule_type: str, value: str) -> None:
            if rule_type not in lists or not value:
                return
            key = _norm_key(rule_type, value)
            if not key or key in seen[rule_type]:
                return
            seen[rule_type].add(key)
            lists[rule_type].append(value.strip())

        for r in doc.get("rules") or []:
            t, v = r.get("type"), r.get("value")
            if not t or not v:
                continue
            add(str(t), str(v))

        dfile = DOMAINS / f"{sid}.txt"
        if dfile.exists():
            with dfile.open(encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        add("domain_suffix", line)

        efile = DOMAINS / f"{sid}.exact.txt"
        if efile.exists():
            with efile.open(encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        add("domain", line)

        ifile = IPS / f"{sid}.txt"
        if ifile.exists():
            with ifile.open(encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if ":" in line:
                        add("ip_cidr6", line)
                    else:
                        add("ip_cidr", line)

        total = sum(len(lists[k]) for k in TYPED_KEYS)
        if total == 0:
            continue

        bucket: dict[str, Any] = {
            "id": sid,
            "name": doc.get("name", sid),
            "category": doc.get("category", "other"),
            **lists,
        }
        out.append(bucket)
    return out


if __name__ == "__main__":
    import sys

    sid = sys.argv[1] if len(sys.argv) > 1 else None
    buckets = load_service_rules(sid)
    for b in buckets:
        n = sum(len(b[k]) for k in TYPED_KEYS)
        print(f"{b['id']}: {n} rules")
    print(f"total services: {len(buckets)}")
