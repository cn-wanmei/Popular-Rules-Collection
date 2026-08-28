#!/usr/bin/env python3
"""client_capability_matrix.py — Phase 4 Client Capability Matrix."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
CAP = ROOT / "config" / "client_capabilities.yaml"


def non_empty_dir(p: Path) -> bool:
    if not p.exists():
        return False
    if p.is_file():
        return p.stat().st_size > 0
    for f in p.rglob("*"):
        if f.is_file() and f.stat().st_size > 0:
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = ap.parse_args()
    day = REPORTS / args.date
    day.mkdir(parents=True, exist_ok=True)

    cfg = yaml.safe_load(CAP.read_text(encoding="utf-8")) if CAP.exists() else {}
    clients = cfg.get("clients") or {}
    datasets = cfg.get("datasets") or {}

    matrix = []
    gaps = []

    for ds_id, ds in datasets.items():
        data_ok = any(non_empty_dir(ROOT / Path(p)) for p in (ds.get("data_paths") or []))
        export_roots = ds.get("export_roots") or []
        export_ok = False
        if export_roots:
            export_ok = any(non_empty_dir(ROOT / Path(p)) for p in export_roots)
        elif ds.get("capability_key") == "asn_meta":
            export_ok = data_ok

        cap_key = ds.get("capability_key") or ""
        row = {
            "dataset": ds_id,
            "data_available": data_ok,
            "export_available": export_ok,
            "clients": {},
        }
        for cid, cmeta in clients.items():
            capable = bool(cmeta.get(cap_key)) if cap_key else False
            if ds_id in ("service_rules", "service_ip"):
                exp = non_empty_dir(ROOT / "generated" / cid)
            else:
                exp = export_ok
            if not capable:
                gap = "no_capability"
            elif not data_ok:
                gap = "no_data"
            elif capable and data_ok and not exp and export_roots:
                gap = "no_export"
            else:
                gap = "none"
            row["clients"][cid] = {
                "capability": capable,
                "export": exp if capable else False,
                "gap": gap,
            }
            if gap != "none":
                gaps.append({"dataset": ds_id, "client": cid, "gap": gap})
        matrix.append(row)

    builders = {}
    for cid, cmeta in clients.items():
        script = cmeta.get("service_builder")
        builders[cid] = {
            "script": script,
            "present": bool(script and (ROOT / "scripts" / script).exists()),
        }

    report = {
        "date": args.date,
        "matrix": matrix,
        "builders": builders,
        "gap_count": len(gaps),
        "gaps_sample": gaps[:40],
        "summary": {
            "clients": len(clients),
            "datasets": len(datasets),
            "gaps": len(gaps),
            "builders_ok": sum(1 for b in builders.values() if b["present"]),
        },
    }
    (day / "client_capability.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (REPORTS / "latest_client_capability.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    client_ids = list(clients.keys())
    lines = [
        f"# Client Capability Matrix ({args.date})",
        "",
        f"- clients: **{len(clients)}** · datasets: **{len(datasets)}** · gaps: **{len(gaps)}**",
        f"- service builders present: **{report['summary']['builders_ok']}/{len(clients)}**",
        "",
        "Legend: `Y` = ok · `c` = capability only · `d` = data no export · `-` = no capability",
        "",
        "| dataset | data | " + " | ".join(client_ids) + " |",
        "|---------|------|" + "|".join(["------"] * len(client_ids)) + "|",
    ]
    for row in matrix:
        cells = []
        for cid in client_ids:
            cell = row["clients"][cid]
            g = cell["gap"]
            cells.append(
                "Y" if g == "none" else "-" if g == "no_capability" else "c" if g == "no_data" else "d" if g == "no_export" else "?"
            )
        lines.append(
            f"| {row['dataset']} | {'Y' if row['data_available'] else 'n'} | "
            + " | ".join(cells)
            + " |"
        )
    if gaps:
        lines += ["", "## Gaps", ""]
        for g in gaps[:30]:
            lines.append(f"- `{g['dataset']}` × `{g['client']}`: **{g['gap']}**")
    (day / "client_capability.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"[client_capability] clients={len(clients)} datasets={len(datasets)} "
        f"gaps={len(gaps)} builders={report['summary']['builders_ok']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
