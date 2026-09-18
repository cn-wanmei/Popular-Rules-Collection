"""V1 Canonical Service Model — Graph, Closure, Dedup, Golden, Regression (Phase 3–7).

Pipeline:
    V1IndexResult (Phase 3.1)
      → Graph Engine        (3.2)
      → Closure Engine      (3.3)
      → Canonical Dedup     (3.4)
      → Golden Set          (4)
      → Client Regression   (5)
      → Deterministic Build (6)
      → Legacy Regression   (7)
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
from .golden import GOLDEN_SERVICE_IDS, GoldenReport, run_v1_golden
from .client_regression import CLIENTS, ClientRegressionReport, run_client_regression
from .deterministic import DeterministicReport, compare_builds, digest_run, run_deterministic_builds
from .legacy_regression import LegacyRegressionReport, compare_legacy_to_v1, run_legacy_regression

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
    "GOLDEN_SERVICE_IDS",
    "GoldenReport",
    "run_v1_golden",
    "CLIENTS",
    "ClientRegressionReport",
    "run_client_regression",
    "DeterministicReport",
    "compare_builds",
    "digest_run",
    "run_deterministic_builds",
    "LegacyRegressionReport",
    "compare_legacy_to_v1",
    "run_legacy_regression",
]
