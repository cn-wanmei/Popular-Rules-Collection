#!/usr/bin/env python3
"""icon_validate.py — Icon Dataset quality gate (soft for main Collect pipeline)."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "icons" / "manifest.yaml"
ICON_ROOT = ROOT / "assets" / "icons"
DOMAINS = ROOT / "database" / "domains"
REPORTS = ROOT / "reports"
VALID_STATUS = frozenset(
    {"verified", "sourced", "placeholder", "missing", "review", "deprecated"}
)
VALID_TYPES = frozenset({"service", "dataset", "network", "policy"})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--require-all-services", action="store_true")
    args = ap.parse_args()
    hard: list[str] = []
    warn: list[str] = []
    info: list[str] = []

    if not MANIFEST.exists():
        print("[icon_validate] HARD missing manifest")
        return 1

    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    icons = doc.get("icons") or {}
    smap = doc.get("service_icon_map") or {}
    if not isinstance(icons, dict) or not icons:
        hard.append("manifest.icons empty")

    seen_keys: set[str] = set()
    for key, meta in icons.items():
        if key in seen_keys:
            hard.append(f"duplicate icon key: {key}")
        seen_keys.add(key)
        if not isinstance(meta, dict):
            hard.append(f"{key}: not a mapping")
            continue
        st = str(meta.get("status") or "")
        if st and st not in VALID_STATUS:
            hard.append(f"{key}: invalid status {st}")
        typ = str(meta.get("type") or "")
        if typ and typ not in VALID_TYPES:
            warn.append(f"{key}: unknown type {typ}")
        if not meta.get("license"):
            warn.append(f"{key}: missing license block")
        if not meta.get("source"):
            warn.append(f"{key}: missing source block")
        files = meta.get("files") or {}
        svg_rel = files.get("svg")
        has_svg = False
        if svg_rel:
            p = ICON_ROOT / svg_rel
            if not p.exists():
                hard.append(f"{key}: missing svg {svg_rel}")
            elif p.stat().st_size < 20:
                hard.append(f"{key}: svg too small")
            else:
                has_svg = True
        elif st not in ("missing", "deprecated"):
            warn.append(f"{key}: no svg in files")
        png = files.get("png") or {}
        for size in (64, 128, 256):
            rel = png.get(str(size)) or png.get(size)
            if not rel:
                if st in ("verified", "sourced") and has_svg:
                    warn.append(f"{key}: missing png/{size} path in manifest")
                continue
            pp = ICON_ROOT / rel
            if not pp.exists():
                if has_svg:
                    warn.append(f"{key}: missing png {rel} (run build_icons.py)")
                else:
                    hard.append(f"{key}: missing file {rel}")
            elif pp.stat().st_size < 10:
                hard.append(f"{key}: empty png {rel}")
        if st == "sourced":
            info.append(f"{key}: sourced (trademark review pending)")

    for sid, ik in smap.items():
        if ik not in icons:
            hard.append(f"service_icon_map {sid} → missing icon {ik}")

    if args.require_all_services and DOMAINS.is_dir():
        for p in sorted(DOMAINS.glob("*.txt")):
            sid = p.stem
            if sid not in smap and sid not in icons:
                warn.append(f"service without icon map: {sid}")

    status = "fail" if hard else ("warn" if warn else "pass")
    if args.strict and warn:
        status = "fail"

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    rep_dir = REPORTS / day
    rep_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "date": day,
        "status": status,
        "hard": hard,
        "warnings": warn[:80],
        "info": info[:40],
        "counts": {"icons": len(icons), "hard": len(hard), "warn": len(warn)},
    }
    (rep_dir / "icon_validate.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"[icon_validate] status={status} icons={len(icons)} "
        f"hard={len(hard)} warn={len(warn)}"
    )
    for e in hard[:25]:
        print(f"  HARD  {e}")
    for w in warn[:25]:
        print(f"  WARN  {w}")
    return 1 if status == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
