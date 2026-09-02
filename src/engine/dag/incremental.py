"""Deterministic incremental planning for the V3 Engine DAG.

The planner is deliberately pure: it only compares immutable input/output
identities and returns the minimum safe set of stages that must be rebuilt.
It never guesses that a missing or unverifiable artifact is reusable.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class StageFingerprint:
    """Immutable identity of a completed V3 Engine stage."""

    input_digest: str
    output_digest: str
    contract: str


# Keep this graph synchronized with the V3 Engine pipeline. A changed stage
# invalidates every transitive dependent; this is explicit and auditable.
DEPENDENCIES: Mapping[str, tuple[str, ...]] = {
    "snapshot": (),
    "ingest": ("snapshot",),
    "quarantine": ("ingest",),
    "canonical": ("quarantine",),
    "hierarchy": ("canonical",),
    "ir": ("hierarchy",),
    "adapters": ("ir",),
    "diff": ("canonical",),
    "golden": ("adapters",),
    "observability": ("diff", "golden"),
    "cas": ("observability",),
    "release": ("cas",),
}


def _dependents(stage: str) -> set[str]:
    if stage not in DEPENDENCIES:
        raise KeyError(f"unknown pipeline stage: {stage}")
    result: set[str] = set()
    frontier = [stage]
    while frontier:
        current = frontier.pop()
        for candidate, deps in DEPENDENCIES.items():
            if current in deps and candidate not in result:
                result.add(candidate)
                frontier.append(candidate)
    return result


def plan_incremental(
    previous: Mapping[str, StageFingerprint],
    current_inputs: Mapping[str, str],
    *,
    contracts: Mapping[str, str] | None = None,
) -> tuple[str, ...]:
    """Return the minimum safe rebuild set in deterministic topological order.

    Reuse is allowed only when prior fingerprint, both digests, the current
    input identity and the current contract are all present and equal. Missing
    evidence therefore fails closed instead of silently reusing stale output.
    """
    current_contracts = contracts or {}
    invalid: set[str] = set()

    for stage in DEPENDENCIES:
        fingerprint = previous.get(stage)
        expected_input = current_inputs.get(stage)
        expected_contract = current_contracts.get(stage)

        if fingerprint is None:
            invalid.add(stage)
            continue
        if not fingerprint.input_digest or not fingerprint.output_digest:
            invalid.add(stage)
            continue
        if expected_input is None or fingerprint.input_digest != expected_input:
            invalid.add(stage)
            continue
        if expected_contract is None or fingerprint.contract != expected_contract:
            invalid.add(stage)
            continue

    for stage in tuple(invalid):
        invalid.update(_dependents(stage))

    ordered: list[str] = []
    remaining = set(invalid)
    while remaining:
        ready = sorted(
            name for name in remaining
            if not (set(DEPENDENCIES[name]) & remaining)
        )
        if not ready:
            raise ValueError("incremental dependency graph contains a cycle")
        ordered.extend(ready)
        remaining.difference_update(ready)
    return tuple(ordered)
