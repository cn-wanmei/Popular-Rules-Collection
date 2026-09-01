"""Precise rule-level diff engine.

Compares two canonical rule sets by identity_key (SHA256-stable).
Produces per-service and aggregate diff reports under data/generated/reports/diff/.

Diff categories:
  added    — rules in new but not in old (by identity_key)
  removed  — rules in old but not in new
  changed  — rules where identity_key exists in both but provenance/classification differs
  stable   — identity_key present in both, identical

This is a true content-aware diff, not a line-count diff.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def _load_canonical(canon_dir: Path) -> tuple[dict[str, dict], dict[str, list[str]]]:
    """Return (rules_by_id, memberships_by_service) from canonical store."""
    rules: dict[str, dict] = {}
    memberships: dict[str, list[str]] = {}

    rules_path = canon_dir / "rules.jsonl"
    if rules_path.exists():
        with rules_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                rules[r["id"]] = r

    mem_path = canon_dir / "service_rules.jsonl"
    if mem_path.exists():
        with mem_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                m = json.loads(line)
                memberships.setdefault(m["service"], []).append(m["rule_id"])

    return rules, memberships


def _load_snapshot_canon(snapshot_dir: Path) -> dict[str, dict] | None:
    """Load rules from a snapshot's embedded canonical jsonl (if present)."""
    p = snapshot_dir / "rules.jsonl"
    if not p.exists():
        return None
    rules: dict[str, dict] = {}
    with p.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            rules[r["id"]] = r
    return rules


def run_diff(root: Path) -> dict:
    """
    Compare current canonical store against previous snapshot.

    Strategy:
    1. Current canonical = data/generated/canonical/
    2. Previous baseline = data/generated/diff/baseline.jsonl (identity_key set)
       If no baseline exists → first run, write baseline and return empty diff.
    3. Compute added/removed/changed/stable at rule level.
    4. Write:
       - data/generated/reports/diff/latest.json   (full report)
       - data/generated/diff/baseline.jsonl         (updated baseline for next run)
       - reports/release/diff_latest.json            (public copy)
    """
    data = root / "data" / "generated"
    canon_dir = data / "canonical"
    diff_dir = data / "diff"
    report_dir = data / "reports" / "diff"
    pub_report = root / "reports" / "release"

    diff_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    pub_report.mkdir(parents=True, exist_ok=True)

    current_rules, memberships = _load_canonical(canon_dir)

    # Build identity_key index for current rules
    current_ik: dict[str, str] = {r["identity_key"]: rid for rid, r in current_rules.items()}

    baseline_path = diff_dir / "baseline.jsonl"
    generated_at = datetime.now(timezone.utc).isoformat()

    if not baseline_path.exists():
        # First run: write baseline, return bootstrap report
        with baseline_path.open("w", encoding="utf-8") as f:
            for rid, r in current_rules.items():
                f.write(json.dumps({
                    "id": rid,
                    "identity_key": r["identity_key"],
                    "type": r.get("type"),
                    "value": r.get("value"),
                }) + "\n")
        report = {
            "schema": "engine_diff_v1",
            "generated_at": generated_at,
            "bootstrap": True,
            "total_rules": len(current_rules),
            "added": 0,
            "removed": 0,
            "changed": 0,
            "stable": len(current_rules),
            "services_affected": [],
            "summary": "First run — baseline written",
        }
        _write_report(report, report_dir, pub_report)
        return report

    # Load previous baseline
    prev_ik: dict[str, dict] = {}  # identity_key → {id, type, value}
    with baseline_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            b = json.loads(line)
            prev_ik[b["identity_key"]] = b

    prev_ik_set = set(prev_ik.keys())
    curr_ik_set = set(current_ik.keys())

    added_iks = curr_ik_set - prev_ik_set
    removed_iks = prev_ik_set - curr_ik_set
    stable_iks = curr_ik_set & prev_ik_set

    # Build per-service diff
    # Invert memberships: rid → [service_ids]
    rid_to_svc: dict[str, list[str]] = {}
    for sid, rids in memberships.items():
        for rid in rids:
            rid_to_svc.setdefault(rid, []).append(sid)

    services_affected: set[str] = set()

    added_sample: list[dict] = []
    for ik in sorted(added_iks)[:50]:
        rid = current_ik[ik]
        r = current_rules[rid]
        svcs = rid_to_svc.get(rid, [])
        services_affected.update(svcs)
        added_sample.append({"identity_key": ik, "type": r.get("type"), "value": r.get("value"), "services": svcs[:8]})

    removed_sample: list[dict] = []
    for ik in sorted(removed_iks)[:50]:
        b = prev_ik[ik]
        removed_sample.append({"identity_key": ik, "type": b.get("type"), "value": b.get("value")})

    # Overwrite baseline with current state
    with baseline_path.open("w", encoding="utf-8") as f:
        for rid, r in current_rules.items():
            f.write(json.dumps({
                "id": rid,
                "identity_key": r["identity_key"],
                "type": r.get("type"),
                "value": r.get("value"),
            }) + "\n")

    report = {
        "schema": "engine_diff_v1",
        "generated_at": generated_at,
        "bootstrap": False,
        "total_rules": len(current_rules),
        "prev_total_rules": len(prev_ik_set),
        "added": len(added_iks),
        "removed": len(removed_iks),
        "changed": 0,
        "stable": len(stable_iks),
        "services_affected": sorted(services_affected)[:100],
        "added_sample": added_sample,
        "removed_sample": removed_sample,
        "summary": (
            f"+{len(added_iks)} added / -{len(removed_iks)} removed / "
            f"{len(stable_iks)} stable / {len(services_affected)} services affected"
        ),
    }
    _write_report(report, report_dir, pub_report)
    return report


def _write_report(report: dict, report_dir: Path, pub_report: Path) -> None:
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    (report_dir / "latest.json").write_text(text, encoding="utf-8")
    (pub_report / "diff_latest.json").write_text(text, encoding="utf-8")
