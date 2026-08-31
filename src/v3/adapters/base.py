"""Shared adapter helpers."""
from __future__ import annotations


def format_line(client: str, typ: str, value: str) -> str | None:
    t = (typ or "").lower()
    if client in ("mihomo", "clash", "surge", "loon", "shadowrocket"):
        if t == "domain_suffix":
            return f"DOMAIN-SUFFIX,{value}"
        if t == "domain":
            return f"DOMAIN,{value}"
        if t == "domain_keyword":
            return f"DOMAIN-KEYWORD,{value}"
        if t == "ip_cidr":
            return f"IP-CIDR,{value}"
        if t == "ip_cidr6":
            return f"IP-CIDR6,{value}"
        if t == "domain_regex":
            return f"DOMAIN-REGEX,{value}" if client == "mihomo" else None
    if client == "singbox":
        if t in ("domain", "domain_suffix"):
            return value
        return None
    if client in ("quantumultx", "egern"):
        if t == "domain_suffix":
            return f"host-suffix, {value}"
        if t == "domain":
            return f"host, {value}"
        if t == "ip_cidr":
            return f"ip-cidr, {value}"
        return None
    return None
