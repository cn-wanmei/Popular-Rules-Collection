"""V1 Service Source-of-Truth resolver.

The resolver makes the post-cutover ownership boundary explicit:
- rule/ is the only V1 canonical service source.
- generated/ is never a source.
- Legacy data is outside the V1 runtime boundary.

Resolution is deterministic and explainable; it does not copy or mutate data.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Resolution:
    service: str
    root: Path
    source: str
    files: tuple[Path, ...]

    @property
    def found(self) -> bool:
        return bool(self.files)


class SoTResolver:
    """Resolve a service to the V1 canonical rule/ tree."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = Path(repository_root)

    def resolve(self, service: str) -> Resolution:
        name = str(service).strip()
        if not name or name in {".", ".."} or "/" in name or "\\" in name:
            raise ValueError("service must be a single path-safe name")

        service_root = self.repository_root / "rule" / name
        files = self._rule_files(service_root)
        if files:
            return Resolution(name, service_root, "v1_rule", files)

        return Resolution(name, service_root, "unresolved", ())

    @staticmethod
    def _rule_files(root: Path) -> tuple[Path, ...]:
        if not root.is_dir():
            return ()
        return tuple(sorted(p for p in root.rglob("*") if p.is_file()))
