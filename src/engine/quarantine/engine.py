"""Quarantine Engine — first hard gate after Snapshot.

Any record that fails basic sanity is moved to quarantine and never
reaches Canonical. This reverses the previous (wrong) order where
quarantine ran after adapters.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_RULE_FIELDS = {"type", "value"}


def run_quarantine(
    ingest_result: dict[str, Any],
    out_dir: Path,
) -> dict[str, Any]:
    """
    Split ingest records into clean vs quarantined.
    Returns updated payload with only clean records + quarantine report.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    clean: list[dict[str, Any]] = []
    quarantined: list[dict[str, Any]] = []

    for rec in ingest_result.get("records") or []:
        reasons: list[str] = []
        if not isinstance(rec, dict):
            reasons.append("not_a_dict")
        else:
            typ = rec.get("type")
            val = rec.get("value")
            if not typ:
                reasons.append("missing_type")
            if not val:
                reasons.append("missing_value")
            if typ is not None and not isinstance(typ, str):
                reasons.append("type_not_str")
            if val is not None and not isinstance(val, str):
                reasons.append("value_not_str")
            # basic empty / whitespace
            if isinstance(val, str) and not val.strip():
                reasons.append("empty_value")

        if reasons:
            quarantined.append({
                "record": rec,
                "reasons": reasons,
                "quarantined_at": datetime.now(timezone.utc).isoformat(),
            })
        else:
            clean.append(rec)

    # also carry forward previous ingest errors
    for e in ingest_result.get("errors") or []:
        quarantined.append({
            "record": e,
            "reasons": ["ingest_error"],
            "quarantined_at": datetime.now(timezone.utc).isoformat(),
        })

    report = {
        "schema": "quarantine_report_v1",
        "snapshot_id": ingest_result.get("snapshot_id"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_records": len(ingest_result.get("records") or []),
        "clean_records": len(clean),
        "quarantined_count": len(quarantined),
        "v2_runtime_dependency": 0,
    }

    (out_dir / "quarantine_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    with (out_dir / "quarantined.jsonl").open("w", encoding="utf-8") as f:
        for q in quarantined:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")

    # return a new ingest-like payload that only contains clean data
    clean_payload = {
        "snapshot_id": ingest_result.get("snapshot_id"),
        "ingested_at": ingest_result.get("ingested_at"),
        "manifest": ingest_result.get("manifest"),
        "records": clean,
        "errors": [],  # already moved to quarantine
        "stats": {
            "records": len(clean),
            "errors": 0,
            "quarantined": len(quarantined),
        },
        "quarantine_report": report,
    }
    return clean_payload
