"""Phase 3 V1 runtime cutover gate."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from src.engine.ingest.v1_index import ServiceEntry, load_v1_index
from src.engine.sot.resolver import Resolution, SoTResolver
RUNTIME_CUTOVER_SCHEMA = "v1_runtime_cutover_v1"
@dataclass
class CutoverReport:
    schema: str = RUNTIME_CUTOVER_SCHEMA
    checked: list[str] = field(default_factory=list)
    resolved: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    violations: list[str] = field(default_factory=list)
    @property
    def all_pass(self) -> bool:
        return not self.unresolved and not self.violations
    def to_dict(self) -> dict[str, object]:
        return {
            "schema": self.schema,
            "checked": sorted(self.checked, key=str.casefold),
            "resolved": sorted(self.resolved, key=str.casefold),
            "unresolved": sorted(self.unresolved, key=str.casefold),
            "violations": sorted(self.violations),
            "all_pass": self.all_pass,
        }
class V1RuntimeCutover:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.resolver = SoTResolver(self.repository_root)
    def resolve_entry(self, entry: ServiceEntry) -> Resolution | None:
        if not entry.path:
            return None
        return self.resolver.resolve_relative(entry.path)
    def run(self) -> CutoverReport:
        report = CutoverReport()
        rule_root = self.repository_root / "rule"
        index = load_v1_index(rule_root)
        for error in index.errors:
            report.violations.append(str(error.get("error", error)) if isinstance(error, dict) else str(error))
        for entry in sorted(index.entries, key=lambda item: item.id.casefold()):
            if not entry.path:
                continue
            report.checked.append(entry.id)
            try:
                resolution = self.resolve_entry(entry)
            except ValueError as exc:
                report.violations.append(f"{entry.id}: {exc}")
                continue
            if resolution is None or resolution.source != "v1_rule" or not resolution.found:
                report.unresolved.append(entry.id)
                continue
            resolved_root = resolution.root.resolve()
            canonical_root = rule_root.resolve()
            if resolved_root != canonical_root and canonical_root not in resolved_root.parents:
                report.violations.append(f"{entry.id}: resolved path escaped rule/ boundary")
                continue
            report.resolved.append(entry.id)
        return report
def run_v1_cutover_gate(repository_root: Path) -> dict[str, object]:
    return V1RuntimeCutover(repository_root).run().to_dict()
