"""Phase 3.4 — Canonical Dedup.

Pipeline:
    Service
      → Dependency Closure
      → Aggregate Closure
      → Normalize
      → Dedup (by AssetKey)
      → IR-ready records

AssetKey hierarchy:
    DomainAssetKey  — domain / domain-suffix / domain-keyword
    CIDRAssetKey    — IPv4 / IPv6 CIDR
    URLAssetKey     — full URL rules
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any, Iterable


# ---------------------------------------------------------------------------
# AssetKey types
# ---------------------------------------------------------------------------

@dataclass(frozen=True, order=True)
class AssetKey:
    """Base canonical identity for a rule asset."""

    kind: str
    value: str

    def identity(self) -> str:
        """Stable string identity used for dedup."""
        return f"{self.kind}:{self.value}"

    def digest(self) -> str:
        return hashlib.sha256(self.identity().encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True, order=True)
class DomainAssetKey(AssetKey):
    """Domain-family asset (domain, domain_suffix, domain_keyword, …)."""

    def __init__(self, value: str, *, subtype: str = "domain") -> None:
        normalized = _normalize_domain(value)
        object.__setattr__(self, "kind", f"domain/{subtype}")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, order=True)
class CIDRAssetKey(AssetKey):
    """IP-CIDR asset (v4 or v6)."""

    def __init__(self, value: str) -> None:
        normalized = _normalize_cidr(value)
        object.__setattr__(self, "kind", "cidr")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, order=True)
class URLAssetKey(AssetKey):
    """URL-family asset."""

    def __init__(self, value: str) -> None:
        normalized = _normalize_url(value)
        object.__setattr__(self, "kind", "url")
        object.__setattr__(self, "value", normalized)


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

_DOMAIN_RE = re.compile(r"^[a-z0-9*._-]+$", re.IGNORECASE)


def _normalize_domain(value: str) -> str:
    v = value.strip().lower().rstrip(".")
    # Strip leading wildcard dots for stable identity; keep '*' marker if present
    if v.startswith("*."):
        v = "*." + v[2:].lstrip(".")
    return v


def _normalize_cidr(value: str) -> str:
    v = value.strip().lower()
    # Collapse whitespace; keep as-is otherwise (full IP normalization is heavier)
    return re.sub(r"\s+", "", v)


def _normalize_url(value: str) -> str:
    return value.strip()


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a shallow copy with normalized type/value fields."""
    out = dict(record)
    typ = str(out.get("type", "")).strip().lower().replace("-", "_")
    val = str(out.get("value", "")).strip()

    if typ in ("domain", "domain_suffix", "domain_keyword", "domain_regex",
               "host", "host_suffix", "keyword"):
        val = _normalize_domain(val)
    elif typ in ("ip_cidr", "ip_cidr6", "ip", "cidr"):
        val = _normalize_cidr(val)
    elif typ in ("url", "url_regex"):
        val = _normalize_url(val)

    out["type"] = typ
    out["value"] = val
    return out


def asset_key_for(record: dict[str, Any]) -> AssetKey:
    """Map a normalized record to its AssetKey."""
    typ = str(record.get("type", "")).lower()
    val = str(record.get("value", ""))

    if typ in ("domain", "domain_suffix", "domain_keyword", "domain_regex",
               "host", "host_suffix", "keyword"):
        subtype = typ if typ.startswith("domain") else "domain"
        if typ in ("host", "host_suffix"):
            subtype = "domain_suffix" if "suffix" in typ else "domain"
        if typ == "keyword":
            subtype = "domain_keyword"
        return DomainAssetKey(val, subtype=subtype)

    if typ in ("ip_cidr", "ip_cidr6", "ip", "cidr"):
        return CIDRAssetKey(val)

    if typ in ("url", "url_regex"):
        return URLAssetKey(val)

    # Fallback: treat as opaque domain-like key
    return DomainAssetKey(val, subtype=typ or "unknown")


# ---------------------------------------------------------------------------
# Dedup
# ---------------------------------------------------------------------------

def dedup_records(
    records: Iterable[dict[str, Any]],
    *,
    prefer_service: str | None = None,
) -> list[dict[str, Any]]:
    """Normalize + deduplicate records by AssetKey.

    Keeps first occurrence in deterministic order (caller should pre-sort
    if a specific priority is required). When prefer_service is set and a
    duplicate arrives from that service, it replaces the existing entry.

    Each output record gains:
        asset_key   — string identity
        asset_digest — short SHA-256 prefix
    """
    seen: dict[str, dict[str, Any]] = {}
    order: list[str] = []

    for raw in records:
        rec = normalize_record(raw)
        key = asset_key_for(rec)
        ident = key.identity()
        rec["asset_key"] = ident
        rec["asset_digest"] = key.digest()

        if ident not in seen:
            seen[ident] = rec
            order.append(ident)
        else:
            # Optional preference: keep the prefer_service version
            if prefer_service and rec.get("service") == prefer_service:
                seen[ident] = rec

    return [seen[i] for i in order]
