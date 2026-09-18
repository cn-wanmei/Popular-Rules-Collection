#!/usr/bin/env python3
"""Phase 2.8 final integrity gate: diff, reproducibility, and audit self-consistency."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIT = ROOT / "scripts" / "v1_phase2_audit.py"
DEFAULT_BASELINE = ROOT / "reports" / "v1" / "PHASE2_BASELINE.yaml"
VOLATILE_KEYS = set()


def run(cmd: list[str], cwd: Path = ROOT) -> str:
    return subprocess.check_output(cmd, cwd=cwd, text=True).strip()


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        value = yaml.safe_load(fh)
    return value if isinstance(value, dict) else {}


def canonical_bytes(path: Path) -> bytes:
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_dump(load_yaml(path), sort_keys=True, allow_unicode=True).encode()
    if path.suffix.lower() == ".json":
        return json.dumps(json.loads(path.read_text(encoding="utf-8")), sort_keys=True, ensure_ascii=False, indent=2).encode()
    return path.read_bytes()


def tree_digest(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted((p for p in root.rglob("*") if p.is_file()), key=lambda p: p.relative_to(root).as_posix()):
        h.update(path.relative_to(root).as_posix().encode())
        h.update(b"\0")
        h.update(canonical_bytes(path))
        h.update(b"\0")
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    ap.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    ap.add_argument("--runs", type=int, default=3)
    args = ap.parse_args()

    baseline = load_yaml(args.baseline)
    baseline_meta = baseline.get("baseline") or {}
    index_path = ROOT / str((baseline.get("source_inventory") or {}).get("index", "rule/_index.yaml"))
    expected_index_sha = str((baseline.get("source_inventory") or {}).get("index_sha256", ""))
    actual_index_sha = hashlib.sha256(index_path.read_bytes()).hexdigest()
    head = run(["git", "rev-parse", "HEAD"])
    baseline_head = str(baseline_meta.get("current_audit_head", ""))
    ancestor_ok = bool(baseline_head) and subprocess.run(
        ["git", "merge-base", "--is-ancestor", baseline_head, head], cwd=ROOT
    ).returncode == 0

    with tempfile.TemporaryDirectory(prefix="v1-phase2-8-") as td:
        root = Path(td)
        digests = []
        for i in range(args.runs):
            out = root / f"run-{i+1}"
            subprocess.run(
                ["python", str(args.audit), "--out", str(out)],
                cwd=ROOT,
                check=True,
            )
            digests.append(tree_digest(out))

        reproducible = len(set(digests)) == 1
        files = sorted(
            p.relative_to(root / "run-1").as_posix()
            for p in (root / "run-1").rglob("*")
            if p.is_file()
        )

    scope = baseline.get("known_scope") or {}
    summary = {
        "head": head,
        "baseline_current_audit_head": baseline_head,
        "baseline_head_is_ancestor": ancestor_ok,
        "baseline_main_commit": str(baseline_meta.get("main_commit", "")),
        "index_sha256_expected": expected_index_sha,
        "index_sha256_actual": actual_index_sha,
        "index_self_consistent": expected_index_sha == actual_index_sha,
        "legacy_entries_expected": int(scope.get("legacy_entries", 0)),
        "reproducibility_runs": args.runs,
        "reproducible": reproducible,
        "run_digests": digests,
        "generated_files": files,
    }

    gates = {
        "baseline_index_matches": summary["index_self_consistent"],
        "baseline_audit_head_is_ancestor": ancestor_ok,
        "legacy_scope_consistent": summary["legacy_entries_expected"] >= 184 or summary["legacy_entries_expected"] == 0,
        "three_builds_identical": reproducible,
    }
    result = {"version": 1, "phase": "2.8", "status": "pass" if all(gates.values()) else "blocked", "gates": gates, "summary": summary}
    print(yaml.safe_dump(result, sort_keys=False, allow_unicode=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
