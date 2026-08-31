"""Shared adapter formatters for 7 clients."""
from __future__ import annotations


def format_line(client: str, typ: str, value: str) -> str | None:
    t = (typ or "").lower()
    v = value or ""
    if client in ("mihomo", "clash"):
        m = {
            "domain_suffix": f"DOMAIN-SUFFIX,{v}",
            "domain": f"DOMAIN,{v}",
            "domain_keyword": f"DOMAIN-KEYWORD,{v}",
            "domain_regex": f"DOMAIN-REGEX,{v}",
            "ip_cidr": f"IP-CIDR,{v},no-resolve",
            "ip_cidr6": f"IP-CIDR6,{v},no-resolve",
        }
        return m.get(t)
    if client == "surge":
        m = {
            "domain_suffix": f"DOMAIN-SUFFIX,{v}",
            "domain": f"DOMAIN,{v}",
            "domain_keyword": f"DOMAIN-KEYWORD,{v}",
            "ip_cidr": f"IP-CIDR,{v},no-resolve",
            "ip_cidr6": f"IP-CIDR6,{v},no-resolve",
        }
        return m.get(t)
    if client in ("loon", "shadowrocket"):
        m = {
            "domain_suffix": f"DOMAIN-SUFFIX,{v}",
            "domain": f"DOMAIN,{v}",
            "domain_keyword": f"DOMAIN-KEYWORD,{v}",
            "ip_cidr": f"IP-CIDR,{v}",
            "ip_cidr6": f"IP-CIDR6,{v}",
        }
        return m.get(t)
    if client == "singbox":
        if t in ("domain", "domain_suffix"):
            return v.lower().rstrip(".")
        if t in ("ip_cidr", "ip_cidr6"):
            return f"ip:{v}"
        return None
    if client == "quantumultx":
        m = {
            "domain_suffix": f"host-suffix, {v}",
            "domain": f"host, {v}",
            "domain_keyword": f"host-keyword, {v}",
            "ip_cidr": f"ip-cidr, {v}",
            "ip_cidr6": f"ip6-cidr, {v}",
        }
        return m.get(t)
    if client == "egern":
        m = {
            "domain_suffix": f"DOMAIN-SUFFIX,{v}",
            "domain": f"DOMAIN,{v}",
            "ip_cidr": f"IP-CIDR,{v}",
            "ip_cidr6": f"IP-CIDR6,{v}",
        }
        return m.get(t)
    return None
