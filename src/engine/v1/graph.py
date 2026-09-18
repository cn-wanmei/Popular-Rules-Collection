"""Phase 3.2 — Graph Engine.

Builds three graphs from a V1IndexResult:

    DependencyGraph  — explicit parent→child edges from metadata
    HierarchyGraph   — same edges oriented as hierarchy (parent owns children)
    AggregateGraph   — aggregate nodes and their declared children

Unified Cycle Detector produces path-formatted errors:

    Dependency cycle detected:
    google/core
     → shared/network
     → google/core
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from src.engine.ingest.v1_index import ServiceEntry, V1IndexResult
from src.engine.v1.errors import CycleDetectedError, V1GraphError


# ---------------------------------------------------------------------------
# Graph primitives
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Edge:
    """Directed edge source → target."""

    source: str
    target: str


@dataclass
class DirectedGraph:
    """Simple adjacency-list digraph with deterministic iteration order."""

    nodes: set[str] = field(default_factory=set)
    # adjacency: source → sorted list of targets
    _adj: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))
    # reverse adjacency for convenience
    _rev: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))

    def add_node(self, node: str) -> None:
        self.nodes.add(node)

    def add_edge(self, source: str, target: str) -> None:
        self.nodes.add(source)
        self.nodes.add(target)
        if target not in self._adj[source]:
            self._adj[source].append(target)
            self._adj[source].sort(key=str.casefold)
        if source not in self._rev[target]:
            self._rev[target].append(source)
            self._rev[target].sort(key=str.casefold)

    def successors(self, node: str) -> list[str]:
        return list(self._adj.get(node, []))

    def predecessors(self, node: str) -> list[str]:
        return list(self._rev.get(node, []))

    def edges(self) -> list[Edge]:
        result: list[Edge] = []
        for src in sorted(self._adj, key=str.casefold):
            for tgt in self._adj[src]:
                result.append(Edge(src, tgt))
        return result

    def has_edge(self, source: str, target: str) -> bool:
        return target in self._adj.get(source, [])


# ---------------------------------------------------------------------------
# Typed graph wrappers
# ---------------------------------------------------------------------------

@dataclass
class DependencyGraph:
    """Edges mean: source *depends on* target (child → parent)."""

    graph: DirectedGraph = field(default_factory=DirectedGraph)
    kind: str = "Dependency"

    def detect_cycles(self) -> None:
        _detect_cycles(self.graph, self.kind)


@dataclass
class HierarchyGraph:
    """Edges mean: source *is parent of* target (parent → child)."""

    graph: DirectedGraph = field(default_factory=DirectedGraph)
    kind: str = "Hierarchy"

    def detect_cycles(self) -> None:
        _detect_cycles(self.graph, self.kind)


@dataclass
class AggregateGraph:
    """Edges mean: aggregate source *includes* target child."""

    graph: DirectedGraph = field(default_factory=DirectedGraph)
    kind: str = "Aggregate"

    def detect_cycles(self) -> None:
        _detect_cycles(self.graph, self.kind)


@dataclass
class ServiceGraphBundle:
    """All three graphs derived from one V1 index."""

    dependency: DependencyGraph
    hierarchy: HierarchyGraph
    aggregate: AggregateGraph
    entry_ids: frozenset[str]
    errors: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Cycle detector (DFS with path reconstruction)
# ---------------------------------------------------------------------------

def _detect_cycles(g: DirectedGraph, kind: str) -> None:
    """Raise CycleDetectedError with full path if a cycle exists.

    Uses white/gray/black DFS coloring. On back-edge to a gray node,
    reconstruct the cycle path for the required error format.
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {n: WHITE for n in g.nodes}
    parent: dict[str, str | None] = {n: None for n in g.nodes}

    def dfs(u: str) -> None:
        color[u] = GRAY
        for v in g.successors(u):
            if color[v] == GRAY:
                # Reconstruct cycle path: v → … → u → v
                path = [v]
                cur = u
                while cur != v and cur is not None:
                    path.append(cur)
                    cur = parent.get(cur)
                path.append(v)
                path.reverse()  # now v → … → u → v
                # Prefer starting at the lexicographically smallest rotation
                # for stability, but keep the detected path as-is for clarity.
                raise CycleDetectedError(kind, path)
            if color[v] == WHITE:
                parent[v] = u
                dfs(v)
        color[u] = BLACK

    for node in sorted(g.nodes, key=str.casefold):
        if color[node] == WHITE:
            dfs(node)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_graphs(
    index: V1IndexResult,
    *,
    raise_on_cycle: bool = True,
) -> ServiceGraphBundle:
    """Build Dependency / Hierarchy / Aggregate graphs from V1 index.

    Edge semantics:
        Dependency  : child → parent   (service depends on its parent aggregate)
        Hierarchy   : parent → child   (aggregate owns its children)
        Aggregate   : aggregate → child (same as Hierarchy for declared children)

    Also adds reverse edges from parent.children declarations when present.

    Args:
        index: result of load_v1_index()
        raise_on_cycle: if True, raise CycleDetectedError on first cycle

    Returns:
        ServiceGraphBundle with all three graphs (cycles already checked if
        raise_on_cycle=True).
    """
    dep = DependencyGraph()
    hier = HierarchyGraph()
    agg = AggregateGraph()

    entry_ids: set[str] = set()
    errors: list[str] = []

    by_id = index.by_id

    for entry in index.entries:
        entry_ids.add(entry.id)
        dep.graph.add_node(entry.id)
        hier.graph.add_node(entry.id)
        agg.graph.add_node(entry.id)

    # Edges from parent field (child → parent)
    for entry in index.entries:
        if entry.parent:
            parent_id = entry.parent
            if parent_id not in by_id:
                errors.append(
                    f"dangling parent reference: {entry.id!r} → parent {parent_id!r} not in index"
                )
            # Dependency: child depends on parent
            dep.graph.add_edge(entry.id, parent_id)
            # Hierarchy / Aggregate: parent owns child
            hier.graph.add_edge(parent_id, entry.id)
            agg.graph.add_edge(parent_id, entry.id)

    # Edges from children declarations on aggregates
    for entry in index.entries:
        if not entry.is_aggregate:
            continue
        for child_id in sorted(entry.children, key=str.casefold):
            if child_id not in by_id:
                errors.append(
                    f"dangling child reference: aggregate {entry.id!r} → child {child_id!r} not in index"
                )
            # Hierarchy / Aggregate: parent owns child
            hier.graph.add_edge(entry.id, child_id)
            agg.graph.add_edge(entry.id, child_id)
            # Dependency: child depends on parent
            dep.graph.add_edge(child_id, entry.id)

    bundle = ServiceGraphBundle(
        dependency=dep,
        hierarchy=hier,
        aggregate=agg,
        entry_ids=frozenset(entry_ids),
        errors=errors,
    )

    if raise_on_cycle:
        dep.detect_cycles()
        hier.detect_cycles()
        agg.detect_cycles()

    return bundle
