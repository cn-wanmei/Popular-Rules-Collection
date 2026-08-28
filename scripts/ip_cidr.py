#!/usr/bin/env python3
"""ip_cidr.py — IPv4/IPv6 CIDR normalize, validate, containment dedup.

Scope policy (see docs/IP_ARCHITECTURE.md):
  service / provider / country / carrier / infrastructure
Only *service*-scoped CIDRs may enter per-service client rulesets.
Country/carrier/provider lists stay in their own ids (china, chinamobile, ...).
"""
from __future__ import annotations

import ipaddress
from typing import Iterable


def parse_cidr(line: str) -> ipaddress._BaseNetwork | None:
    s = (line or "").strip()
    if not s or s.startswith("#") or s.startswith(";"):
        return None
    if " #" in s:
        s = s.split(" #", 1)[0].strip()
    try:
        if "/" not in s:
            ip = ipaddress.ip_address(s)
            return ipaddress.ip_network(f"{ip}/{ip.max_prefixlen}", strict=False)
        return ipaddress.ip_network(s, strict=False)
    except ValueError:
        return None


def normalize_lines(lines: Iterable[str]) -> list[str]:
    """Validate + normalize; drop invalid; collapse exact duplicates."""
    seen: set[str] = set()
    out: list[str] = []
    for line in lines:
        net = parse_cidr(line)
        if net is None:
            continue
        key = net.with_prefixlen
        if key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


def containment_dedup(cidrs: Iterable[str]) -> list[str]:
    """Remove networks fully contained in a broader kept network (same family).

    Keeps broader prefixes; drops more-specific that are subsets.
    Does not merge adjacent networks (safe, reversible).
    """
    v4: list[ipaddress.IPv4Network] = []
    v6: list[ipaddress.IPv6Network] = []
    for c in normalize_lines(cidrs):
        net = parse_cidr(c)
        if net is None:
            continue
        if isinstance(net, ipaddress.IPv4Network):
            v4.append(net)
        else:
            v6.append(net)

    def _dedup(nets: list) -> list[str]:
        if not nets:
            return []
        nets = sorted(nets, key=lambda n: (n.prefixlen, int(n.network_address)))
        kept: list = []
        for n in nets:
            if any(n.subnet_of(k) for k in kept):  # type: ignore[attr-defined]
                continue
            kept = [k for k in kept if not k.subnet_of(n)]  # type: ignore[attr-defined]
            kept.append(n)
        return [
            k.with_prefixlen
            for k in sorted(kept, key=lambda n: (n.prefixlen, int(n.network_address)))
        ]

    return _dedup(v4) + _dedup(v6)


def merge_files(
    existing: Iterable[str], incoming: Iterable[str], *, contain: bool = True
) -> list[str]:
    combined = list(existing) + list(incoming)
    return containment_dedup(combined) if contain else normalize_lines(combined)
