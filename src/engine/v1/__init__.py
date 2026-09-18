"""V1 Canonical Service Model — Graph, Closure, Dedup (Phase 3.2–3.4).

Pipeline:
    V1IndexResult (Phase 3.1)
      → Graph Engine   (3.2)  Dependency / Hierarchy / Aggregate + Cycle Detector
      → Closure Engine (3.3)  dependency_closure / aggregate_closure
      → Canonical Dedup(3.4)  AssetKey → Normalize → Dedup → IR-ready records
"""
from .errors import CycleDetectedError, V1GraphError
from .graph import (
    AggregateGraph,
    DependencyGraph,
    HierarchyGraph,
    ServiceGraphBundle,
    build_graphs,
)
from .closure import aggregate_closure, dependency_closure
from .dedup import (
    AssetKey,
    CIDRAssetKey,
    DomainAssetKey,
    URLAssetKey,
    dedup_records,
    normalize_record,
)

__all__ = [
    "CycleDetectedError",
    "V1GraphError",
    "AggregateGraph",
    "DependencyGraph",
    "HierarchyGraph",
    "ServiceGraphBundle",
    "build_graphs",
    "aggregate_closure",
    "dependency_closure",
    "AssetKey",
    "CIDRAssetKey",
    "DomainAssetKey",
    "URLAssetKey",
    "dedup_records",
    "normalize_record",
]
