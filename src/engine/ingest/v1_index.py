"""V1 Index Parser — rule/_index.yaml → Canonical Service Model entries.

Reads the authoritative _index.yaml and each service's metadata.yaml to
produce a fully-typed service catalogue.  No rule assets are parsed here;
only structural / identity information is resolved.

Seven entity types per the Phase 3 spec:
    Service       — leaf service (service_type: service)
    Parent        — a declared provider aggregate (service_type: aggregate)
    Child         — a service whose metadata declares a parent
    Shared        — appears in multiple categories
    Category      — the _index.yaml category block itself
    Aggregate     — same as Parent (alias used in hierarchy config)
    NetworkRef    — a service with IP/CIDR rules (has_ip: true)

These types are *not* mutually exclusive: a single entry can be a Child,
a NetworkRef, and appear in a Shared category simultaneously.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

INDEX_FILENAME = "_index.yaml"
METADATA_FILENAME = "metadata.yaml"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ServiceEntry:
    """Canonical identity record for one V1 rule service."""

    id: str
    name: str
    path: str                          # relative path, e.g. "rule/Google/YouTube"
    service_type: str                  # "service" | "aggregate"
    categories: frozenset[str]         # all index categories this entry belongs to
    domains: int
    ips: int

    # Resolved from metadata.yaml (may be absent for generated-only entries)
    parent: str | None                 # parent aggregate id, or None
    children: frozenset[str]           # declared children (aggregates only)
    sources: frozenset[str]            # upstream data sources
    clients: frozenset[str]            # supported client platforms
    has_ip: bool                       # has IP/CIDR rules → NetworkRef
    auto_generated: bool

    # Derived type flags (all may be True simultaneously)
    is_aggregate: bool
    is_child: bool                     # has a non-null parent
    is_network_ref: bool               # has_ip is True
    is_shared: bool                    # appears in ≥2 categories

    # Stable digest (excludes volatile fields)
    digest: str

    def type_flags(self) -> list[str]:
        """Human-readable list of applicable type labels."""
        flags = ["Service"]
        if self.is_aggregate:
            flags += ["Parent", "Aggregate"]
        if self.is_child:
            flags.append("Child")
        if self.is_network_ref:
            flags.append("NetworkRef")
        if self.is_shared:
            flags.append("Shared")
        return flags


@dataclass
class V1IndexResult:
    """Complete parsed output of the V1 index."""

    schema: str = "v1_index_v1"
    index_path: str = ""
    entry_count: int = 0
    service_count: int = 0
    aggregate_count: int = 0
    category_count: int = 0
    entries: list[ServiceEntry] = field(default_factory=list)
    categories: dict[str, dict[str, Any]] = field(default_factory=dict)  # raw cat blocks
    errors: list[dict[str, Any]] = field(default_factory=list)

    # convenience maps built after load
    by_id: dict[str, ServiceEntry] = field(default_factory=dict)
    by_category: dict[str, list[str]] = field(default_factory=dict)  # cat → [service_id]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_yaml(path: Path, errors: list[dict[str, Any]], label: str) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        return doc if isinstance(doc, dict) else None
    except Exception as exc:
        errors.append({"label": label, "path": str(path), "error": str(exc)})
        return None


def _entry_digest(entry_id: str, path: str, service_type: str, domains: int, ips: int) -> str:
    """Stable 12-char prefix of SHA-256 over structural fields."""
    blob = json.dumps(
        {"id": entry_id, "path": path, "service_type": service_type, "domains": domains, "ips": ips},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Main loader
# ---------------------------------------------------------------------------

def load_v1_index(rule_root: Path) -> V1IndexResult:
    """Parse rule/_index.yaml and all reachable metadata.yaml files.

    Args:
        rule_root: the ``rule/`` directory (contains _index.yaml and service dirs).

    Returns:
        V1IndexResult with fully resolved ServiceEntry objects.
    """
    rule_root = Path(rule_root)
    index_path = rule_root / INDEX_FILENAME
    result = V1IndexResult(index_path=str(index_path))
    errors = result.errors

    if not index_path.exists():
        errors.append({"label": "index", "path": str(index_path), "error": "index file not found"})
        return result

    raw = _load_yaml(index_path, errors, "index")
    if raw is None:
        return result

    categories_block: dict[str, Any] = raw.get("categories") or {}
    result.categories = categories_block
    result.category_count = len(categories_block)

    # Build: entry_id → set of category names (for Shared detection)
    entry_categories: dict[str, list[str]] = {}
    # Build: entry_id → raw index row
    entry_rows: dict[str, dict[str, Any]] = {}

    for cat_name in sorted(categories_block, key=str.casefold):
        cat_block = categories_block[cat_name]
        if not isinstance(cat_block, dict):
            continue
        rules = cat_block.get("rules") or []
        for row in sorted(
            (r for r in rules if isinstance(r, dict)),
            key=lambda r: (str(r.get("id", "")).casefold(), str(r.get("path", ""))),
        ):
            eid = str(row.get("id", "")).strip()
            if not eid:
                errors.append({"label": "index_row", "category": cat_name, "error": "missing id", "row": row})
                continue
            entry_categories.setdefault(eid, []).append(cat_name)
            if eid not in entry_rows:
                entry_rows[eid] = dict(row)
            result.by_category.setdefault(cat_name, []).append(eid)

    # Resolve each entry
    entries: list[ServiceEntry] = []
    for eid in sorted(entry_rows, key=str.casefold):
        row = entry_rows[eid]
        path_rel = str(row.get("path", "")).strip()
        service_type = str(row.get("service_type", "service")).strip()
        domains = int(row.get("domains", 0))
        ips = int(row.get("ips", 0))
        cats_for_entry = frozenset(entry_categories.get(eid, []))

        # Load metadata.yaml for this entry
        meta: dict[str, Any] = {}
        if path_rel:
            meta_path = rule_root.parent / path_rel / METADATA_FILENAME
            loaded = _load_yaml(meta_path, errors, f"metadata:{eid}")
            if loaded:
                meta = loaded

        parent = meta.get("parent") or None
        if parent is not None:
            parent = str(parent).strip() or None

        children = frozenset(
            str(c).strip().casefold()
            for c in (meta.get("children") or [])
            if str(c).strip()
        )
        sources_set = frozenset(
            str(s).strip()
            for s in (meta.get("sources") or [])
            if str(s).strip()
        )
        clients_set = frozenset(
            str(c).strip()
            for c in (meta.get("clients") or [])
            if str(c).strip()
        )
        rule_meta = meta.get("rule") or {}
        has_ip = bool(rule_meta.get("has_ip", False)) or ips > 0
        auto_generated = bool(meta.get("auto_generated", False))

        entry = ServiceEntry(
            id=eid,
            name=str(row.get("name", meta.get("name", eid))),
            path=path_rel,
            service_type=service_type,
            categories=cats_for_entry,
            domains=domains,
            ips=ips,
            parent=parent,
            children=children,
            sources=sources_set,
            clients=clients_set,
            has_ip=has_ip,
            auto_generated=auto_generated,
            is_aggregate=(service_type == "aggregate"),
            is_child=(parent is not None),
            is_network_ref=has_ip,
            is_shared=(len(cats_for_entry) >= 2),
            digest=_entry_digest(eid, path_rel, service_type, domains, ips),
        )
        entries.append(entry)
        result.by_id[eid] = entry

    result.entries = entries
    result.entry_count = len(entries)
    result.service_count = sum(1 for e in entries if not e.is_aggregate)
    result.aggregate_count = sum(1 for e in entries if e.is_aggregate)

    return result
