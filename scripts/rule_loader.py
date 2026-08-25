#!/usr/bin/env python3
"""Shared loader: database/services + domains/ips → typed rule buckets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"


def load_service_rules(service_id: str | None = None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    paths = sorted(SERVICES.glob("*.yaml"))
    if service_id:
        paths = [SERVICES / f"{service_id}.yaml"]
    for path in paths:
        if not path.exists() or path.name.startswith("example"):
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        sid = doc.get("id") or path.stem
        bucket: dict[str, Any] = {
            "id": sid,
            "name": doc.get("name", sid),
            "category": doc.get("category", "other"),
            "domain": [],
            "domain_suffix": [],
            "domain_keyword": [],
            "domain_regex": [],
            "ip_cidr": [],
            "ip_cidr6": [],
        }
        for r in doc.get("rules") or []:
            t, v = r.get("type"), r.get("value")
            if not t or not v:
                continue
            if t in bucket:
                bucket[t].append(v)
        dfile = DOMAINS / f"{sid}.txt"
        if dfile.exists():
            for line in dfile.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and line not in bucket["domain_suffix"] and line not in bucket["domain"]:
                    bucket["domain_suffix"].append(line)
        ifile = IPS / f"{sid}.txt"
        if ifile.exists():
            for line in ifile.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                if ":" in line:
                    if line not in bucket["ip_cidr6"]:
                        bucket["ip_cidr6"].append(line)
                else:
                    if line not in bucket["ip_cidr"]:
                        bucket["ip_cidr"].append(line)
        for k in ("domain", "domain_suffix", "domain_keyword", "domain_regex", "ip_cidr", "ip_cidr6"):
            seen: set[str] = set()
            uniq = []
            for v in bucket[k]:
                key = v.lower() if k.startswith("domain") else v
                if key not in seen:
                    seen.add(key)
                    uniq.append(v)
            bucket[k] = uniq
        total = sum(len(bucket[k]) for k in ("domain", "domain_suffix", "domain_keyword", "domain_regex", "ip_cidr", "ip_cidr6"))
        if total:
            out.append(bucket)
    return out
