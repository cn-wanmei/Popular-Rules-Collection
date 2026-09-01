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
    """Immutable identity of a completed stage."""

    input_digest: str
    output_digest: str
    contract: str


# A changed stage invalidates every transitive dependent.  Keep this explicit
# so the impact model is auditable rather than inferred from filenames.
DEPENDENCIES: Mapping[str, tuple[str, ...]] = {
    "snapshot": (),
    "ingest": ("snapshot",),
    "canonical": ("ingest",),
    "hierarchy": ("canonical",),
    "ir": ("hierarchy",),
    "diff": ("canonical",),
    "golden": ("ir",),
    "release": ("golden", "diff"),
    "promote": ("release",),
}


def _dependents(stage: str) -> set[str]:
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
    """Return the minimal *safe* rebuild set in deterministic topological order.

    A stage is reusable only when its previous fingerprint exists, its input
    digest matches, and its contract matches the current contract. Missing
    output identity or an unknown contract is treated as non-reusable.
    """
    contracts = contracts or {}
    invalid: set[str] = set()
    for stage in DEPENDENCIES:
        fingerprint = previous.get(stage)
        expected_input = current_inputs.get(stage)
        expected_contract = contracts.get(stage)
        if fingerprint is None or not fingerprint.output_digest:
            invalid.add(stage)
            continue
        if expected_input is None or fingerprint.input_digest != expected_input:
            invalid.add(stage)
            continue
        if expected_contract is not None and fingerprint.contract != expected_contract:
            invalid.add(stage)

    for stage in tuple(invalid):
        invalid.update(_dependents(stage))

    # Stable order follows the declared DAG layers.
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
