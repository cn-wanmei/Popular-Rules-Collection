"""Phase 6 — Deterministic Build gate.

Same V1 Snapshot built three times (A / B / C) must produce:

    IR_A == IR_B == IR_C
    generated_A == generated_B == generated_C

Eliminates non-determinism from:
    - filesystem order
    - dict iteration order
    - category order
    - dependency traversal order

This module reuses the existing reproducibility hash_compare helpers and
adds a multi-build orchestrator that only needs stable digests.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


VOLATILE_KEYS = {
    "generated_at",
    "started_at",
    "finished_at",
    "promoted_at",
    "run_dir",
    "ingested_at",
}


def _stable_json_bytes(data: Any) -> bytes:
    def strip(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: strip(v) for k, v in sorted(value.items()) if k not in VOLATILE_KEYS}
        if isinstance(value, list):
            return [strip(v) for v in value]
        return value

    return json.dumps(strip(data), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def digest_path(path: Path) -> str:
    path = Path(path)
    if path.suffix == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return hashlib.sha256(_stable_json_bytes(data)).hexdigest()
        except (OSError, json.JSONDecodeError):
            pass
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def digest_jsonl(path: Path) -> str:
    """Order-independent digest of a JSONL file (sort lines first)."""
    path = Path(path)
    if not path.exists():
        return hashlib.sha256(b"").hexdigest()
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    # Parse + re-serialize each line with sorted keys for stability
    normalized: list[str] = []
    for ln in lines:
        try:
            obj = json.loads(ln)
            normalized.append(
                json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            )
        except json.JSONDecodeError:
            normalized.append(ln)
    normalized.sort()
    return hashlib.sha256("\n".join(normalized).encode("utf-8")).hexdigest()


@dataclass
class BuildDigest:
    label: str
    ir_digest: str = ""
    rules_digest: str = ""
    memberships_digest: str = ""
    hierarchy_digest: str = ""
    artifacts_digest: str = ""
    overall: str = ""

    def compute_overall(self) -> str:
        payload = {
            "ir": self.ir_digest,
            "rules": self.rules_digest,
            "memberships": self.memberships_digest,
            "hierarchy": self.hierarchy_digest,
            "artifacts": self.artifacts_digest,
        }
        self.overall = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        return self.overall


def digest_run(run_dir: Path, label: str = "run") -> BuildDigest:
    """Compute stable digests for the semantic outputs of one build."""
    run_dir = Path(run_dir)
    d = BuildDigest(label=label)

    ir = run_dir / "ir" / "ir.json"
    if ir.exists():
        d.ir_digest = digest_path(ir)

    rules = run_dir / "canonical" / "rules.jsonl"
    if rules.exists():
        d.rules_digest = digest_jsonl(rules)

    mem = run_dir / "canonical" / "memberships.jsonl"
    if mem.exists():
        d.memberships_digest = digest_jsonl(mem)

    hier = run_dir / "hierarchy" / "graph.json"
    if hier.exists():
        d.hierarchy_digest = digest_path(hier)

    art = run_dir / "artifacts"
    art_parts: dict[str, str] = {}
    if art.exists():
        for f in sorted(art.rglob("*")):
            if f.is_file() and f.suffix in {".yaml", ".list", ".json"} and f.name != "build_report.json":
                art_parts[str(f.relative_to(run_dir))] = digest_path(f)
    d.artifacts_digest = hashlib.sha256(
        json.dumps(art_parts, sort_keys=True).encode("utf-8")
    ).hexdigest()
    d.compute_overall()
    return d


@dataclass
class DeterministicReport:
    schema: str = "v1_deterministic_v1"
    builds: list[dict[str, str]] = field(default_factory=list)
    match: bool = False
    mismatches: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "builds": self.builds,
            "match": self.match,
            "mismatches": self.mismatches,
            "errors": self.errors,
            "all_pass": self.match and not self.errors,
        }


def compare_builds(run_dirs: list[Path], labels: list[str] | None = None) -> DeterministicReport:
    """Compare digests of N builds; N≥2 required, N=3 recommended (A/B/C)."""
    report = DeterministicReport()
    if len(run_dirs) < 2:
        report.errors.append("need at least 2 build directories to compare")
        return report

    labels = labels or [f"build_{i}" for i in range(len(run_dirs))]
    digests = [digest_run(Path(d), label=labels[i]) for i, d in enumerate(run_dirs)]

    for d in digests:
        report.builds.append(
            {
                "label": d.label,
                "ir": d.ir_digest,
                "rules": d.rules_digest,
                "memberships": d.memberships_digest,
                "hierarchy": d.hierarchy_digest,
                "artifacts": d.artifacts_digest,
                "overall": d.overall,
            }
        )

    base = digests[0]
    for other in digests[1:]:
        for field_name in ("ir_digest", "rules_digest", "memberships_digest", "hierarchy_digest", "artifacts_digest"):
            if getattr(base, field_name) != getattr(other, field_name):
                report.mismatches.append(
                    f"{field_name}: {base.label}={getattr(base, field_name)[:12]}… "
                    f"!= {other.label}={getattr(other, field_name)[:12]}…"
                )

    report.match = len(report.mismatches) == 0
    return report


def run_deterministic_builds(
    build_fn: Callable[[Path], None],
    work_root: Path,
    *,
    n: int = 3,
) -> DeterministicReport:
    """Invoke build_fn(out_dir) N times into work_root/build_{i} and compare.

    build_fn is responsible for writing the full run layout under out_dir.
    """
    work_root = Path(work_root)
    work_root.mkdir(parents=True, exist_ok=True)
    run_dirs: list[Path] = []
    labels: list[str] = []
    errors: list[str] = []

    for i in range(n):
        label = f"build_{chr(ord('A') + i)}"
        out = work_root / label
        out.mkdir(parents=True, exist_ok=True)
        try:
            build_fn(out)
        except Exception as exc:
            errors.append(f"{label} failed: {exc}")
        run_dirs.append(out)
        labels.append(label)

    report = compare_builds(run_dirs, labels=labels)
    report.errors.extend(errors)
    if errors:
        report.match = False
    return report


def write_deterministic_report(report: DeterministicReport, out_path: Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
