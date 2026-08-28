#!/usr/bin/env python3
"""client_capability_matrix.py — expected artifact checks (v2)."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
CAP = ROOT / "config" / "client_capabilities.yaml"

CLIENT_DIR_ALIASES = {
    "quantumult-x": ["quantumult-x", "quantumultx"],
    "sing-box": ["sing-box", "singbox"],
}


def non_empty_file(p: Path) -> bool:
    return p.is_file() and p.stat().st_size > 0


def any_non_empty(paths: list[str]) -> bool:
    return any(non_empty_file(ROOT / Path(x)) for x in paths)


def dir_has_any(p: Path) -> bool:
    if not p.is_dir():
        return False
    for f in p.rglob("*"):
        if f.is_file() and f.stat().st_size > 0:
            return True
    return False


def service_artifact_exists(client: str, sid: str) -> bool:
    names = CLIENT_DIR_ALIASES.get(client, [client])
    suffixes = [".list", ".yaml", ".yml", ".json", ".conf", ".txt", ".srs"]
    for dname in names:
        d = ROOT / "generated" / dname
        if not d.is_dir():
            continue
        for suf in suffixes:
            if non_empty_file(d / f"{sid}{suf}"):
                return True
        for f in d.iterdir():
            if f.is_file() and f.stat().st_size > 0 and sid in f.stem:
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
        data_paths = ds.get("data_paths") or []
        data_ok = any(
            dir_has_any(ROOT / Path(p)) or non_empty_file(ROOT / Path(p))
            for p in data_paths
        )
        cap_key = ds.get("capability_key") or ""
        network_key = ds.get("network_key")
        samples = ds.get("sample_services") or []

        row = {
            "dataset": ds_id,
            "data_available": data_ok,
            "note": ds.get("note"),
            "clients": {},
        }

        for cid, cmeta in clients.items():
            capable = bool(cmeta.get(cap_key)) if cap_key else False
            export_ok = False

            if not capable:
                gap = "no_capability"
            elif not data_ok:
                gap = "no_data"
            elif network_key:
                expected = (cmeta.get("network_exports") or {}).get(network_key) or []
                if not expected:
                    gap = "no_export"
                else:
                    export_ok = any_non_empty(expected)
                    gap = "none" if export_ok else "no_export"
            elif samples:
                found = sum(1 for sid in samples if service_artifact_exists(cid, sid))
                export_ok = found > 0
                if found == 0:
                    gap = "no_export"
                elif found < max(1, len(samples) // 2):
                    gap = "invalid"
                else:
                    gap = "none"
            else:
                export_ok = data_ok
                gap = "none" if data_ok else "no_data"

            row["clients"][cid] = {
                "capability": capable,
                "export": export_ok,
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
        "version": cfg.get("version"),
        "matrix": matrix,
        "builders": builders,
        "gap_count": len(gaps),
        "gaps_sample": gaps[:50],
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
        f"- version: **{cfg.get('version')}** (expected-artifact checks)",
        f"- clients: **{len(clients)}** · datasets: **{len(datasets)}** · gaps: **{len(gaps)}**",
        f"- builders present: **{report['summary']['builders_ok']}/{len(clients)}**",
        "",
        "Legend: `Y`=ok · `c`=cap only · `d`=no export · `i`=invalid · `-`=no capability",
        "",
        "| dataset | data | " + " | ".join(client_ids) + " |",
        "|---------|------|" + "|".join(["------"] * len(client_ids)) + "|",
    ]
    mark = {
        "none": "Y",
        "no_capability": "-",
        "no_data": "c",
        "no_export": "d",
        "invalid": "i",
    }
    for row in matrix:
        cells = [mark.get(row["clients"][cid]["gap"], "?") for cid in client_ids]
        lines.append(
            f"| {row['dataset']} | {'Y' if row['data_available'] else 'n'} | "
            + " | ".join(cells)
            + " |"
        )
    if gaps:
        lines += ["", "## Gaps", ""]
        for g in gaps[:40]:
            lines.append(f"- `{g['dataset']}` × `{g['client']}`: **{g['gap']}**")
    (day / "client_capability.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"[client_capability] v{cfg.get('version')} clients={len(clients)} "
        f"datasets={len(datasets)} gaps={len(gaps)} builders={report['summary']['builders_ok']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
