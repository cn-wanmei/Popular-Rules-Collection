"""V1 Canonical Service Model — Phases 3–8."""
from .errors import CycleDetectedError, V1GraphError
from .graph import ServiceGraphBundle, build_graphs
from .closure import aggregate_closure, dependency_closure
from .dedup import DomainAssetKey, CIDRAssetKey, URLAssetKey, dedup_records, normalize_record
from .golden import GOLDEN_SERVICE_IDS, run_v1_golden
from .client_regression import CLIENTS, run_client_regression
from .deterministic import compare_builds, run_deterministic_builds
from .legacy_regression import compare_legacy_to_v1, run_legacy_regression
from .phase8 import (
    INTENTIONAL_CODES,
    compute_coverage,
    evaluate_phase8_gates,
    load_intentional_registry,
    request_legacy_delete,
    switch_sot_to_v1,
)

__all__ = [
    "CycleDetectedError", "V1GraphError", "ServiceGraphBundle", "build_graphs",
    "aggregate_closure", "dependency_closure",
    "DomainAssetKey", "CIDRAssetKey", "URLAssetKey", "dedup_records", "normalize_record",
    "GOLDEN_SERVICE_IDS", "run_v1_golden",
    "CLIENTS", "run_client_regression",
    "compare_builds", "run_deterministic_builds",
    "compare_legacy_to_v1", "run_legacy_regression",
    "INTENTIONAL_CODES", "compute_coverage", "evaluate_phase8_gates",
    "load_intentional_registry", "request_legacy_delete", "switch_sot_to_v1",
]
