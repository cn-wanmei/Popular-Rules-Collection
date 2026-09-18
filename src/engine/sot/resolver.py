"""V1 Service Source-of-Truth resolver.

The resolver makes the post-cutover ownership boundary explicit:
- rule/ is the only V1 canonical service source.
- generated/ is never a source.
Resolution is deterministic and read-only.
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
    """Resolve a service or explicit V1 rule path inside rule/."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = Path(repository_root).resolve()

    def resolve(self, service: str) -> Resolution:
        name = str(service).strip()
        if not name or name in {".", ".."} or "/" in name or "\\" in name:
            raise ValueError("service must be a single path-safe name")
        service_root = self.repository_root / "rule" / name
        return self._resolution(name, service_root)

    def resolve_relative(self, relative_path: str) -> Resolution:
        relative = Path(str(relative_path).strip())
        rule_root = (self.repository_root / "rule").resolve()
        if relative.is_absolute() or not relative.parts or relative.parts[0] != "rule":
            raise ValueError("relative_path must begin with rule/")
        if ".." in relative.parts:
            raise ValueError("relative_path cannot contain parent traversal")
        target = (self.repository_root / relative).resolve()
        if target != rule_root and rule_root not in target.parents:
            raise ValueError("relative_path escapes rule/ boundary")
        return self._resolution(relative.as_posix(), target)

    def _resolution(self, name: str, service_root: Path) -> Resolution:
        files = self._rule_files(service_root)
        source = "v1_rule" if files else "unresolved"
        return Resolution(name, service_root, source, files)

    @staticmethod
    def _rule_files(root: Path) -> tuple[Path, ...]:
        if not root.is_dir():
            return ()
        return tuple(sorted(p for p in root.rglob("*") if p.is_file()))
