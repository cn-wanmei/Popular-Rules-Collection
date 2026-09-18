"""Phase 3.3 — Closure Engine.

Full transitive closures over the graphs from Phase 3.2.

    dependency_closure(A)  — A + everything A depends on (transitively)
    aggregate_closure(A)   — A + everything A includes (transitively)

Example:
    A → B → C → D
    closure(A) == {A, B, C, D}   # NOT merely {A, B}
"""
from __future__ import annotations

from typing import Iterable

from src.engine.v1.graph import DirectedGraph, ServiceGraphBundle


def _transitive_successors(g: DirectedGraph, roots: Iterable[str]) -> frozenset[str]:
    """BFS / DFS reachable set including the roots themselves."""
    result: set[str] = set()
    stack = list(roots)
    while stack:
        node = stack.pop()
        if node in result:
            continue
        result.add(node)
        for succ in g.successors(node):
            if succ not in result:
                stack.append(succ)
    return frozenset(result)


def dependency_closure(
    bundle: ServiceGraphBundle,
    service_ids: Iterable[str] | str,
) -> frozenset[str]:
    """Transitive dependency closure.

    Follows DependencyGraph edges (child → parent), so for a service S
    the closure includes S and all ancestors (parents, grandparents, …).

    Accepts a single id or an iterable of ids.
    """
    if isinstance(service_ids, str):
        roots = [service_ids]
    else:
        roots = list(service_ids)
    return _transitive_successors(bundle.dependency.graph, roots)


def aggregate_closure(
    bundle: ServiceGraphBundle,
    service_ids: Iterable[str] | str,
) -> frozenset[str]:
    """Transitive aggregate / hierarchy closure.

    Follows AggregateGraph edges (parent → child), so for an aggregate A
    the closure includes A and all descendants (children, grandchildren, …).

    Accepts a single id or an iterable of ids.
    """
    if isinstance(service_ids, str):
        roots = [service_ids]
    else:
        roots = list(service_ids)
    return _transitive_successors(bundle.aggregate.graph, roots)
