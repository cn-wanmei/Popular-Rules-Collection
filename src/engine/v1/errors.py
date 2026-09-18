"""Structured errors for V1 Graph / Closure / Dedup."""
from __future__ import annotations

from typing import Sequence


class V1GraphError(ValueError):
    """Base error for V1 graph engine failures."""


class CycleDetectedError(V1GraphError):
    """Cycle detected in a dependency / hierarchy / aggregate graph.

    Message format (required by Phase 3.2):

        Dependency cycle detected:
        google/core
         → shared/network
         → google/core
    """

    def __init__(self, kind: str, path: Sequence[str]) -> None:
        self.kind = kind  # "Dependency" | "Hierarchy" | "Aggregate"
        self.path = list(path)
        lines = [f"{kind} cycle detected:"]
        if self.path:
            lines.append(self.path[0])
            for node in self.path[1:]:
                lines.append(f" → {node}")
        super().__init__("\n".join(lines))

    def __str__(self) -> str:
        return super().__str__()
