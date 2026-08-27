#!/usr/bin/env python3
"""identity_validate.py — P1-1 Source → Service identity (warn-first).

Checks BlackMatrix7 Clash YAML headers (# NAME:) against expected service id.
HTTP 200 alone is not identity. Does not mutate registry or guess paths.

Exit 0 always (soft gate) unless --strict.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "sources" / "registry.yaml"
HINTS = ROOT / "config" / "identity_hints.yaml"
BM_DIR = ROOT / "sources" / "blackmatrix7"
BACKUP = ROOT / "backup"

NAME_RE = re.compile(r"^#\s*NAME:\s*(.+?)\s*$", re.I | re.M)


def load_hints() -> dict:
    if HINTS.exists():
        data = yaml.safe_load(HINTS.read_text(encoding="utf-8")) or {}
        return dict(data.get("services") or {})
    return {}


def default_expected(sid: str) -> list[str]:
    parts = re.split(r"[-_]", sid)
    camel = "".join(p[:1].upper() + p[1:] for p in parts if p)
    return list({sid, sid.lower(), camel, camel.lower()})


def find_bm_file(local_name: str, day: str | None) -> Path | None:
    p = BM_DIR / local_name
    if p.exists():
        return p
    if day:
        alt = BACKUP / day / "sources" / "blackmatrix7" / local_name
        if alt.exists():
            return alt
    if BACKUP.is_dir():
        days = sorted([d for d in BACKUP.iterdir() if d.is_dir()], reverse=True)
        for d in days[:5]:
            alt = d / "sources" / "blackmatrix7" / local_name
            if alt.exists():
                return alt
    return None


def extract_name(text: str) -> str | None:
    m = NAME_RE.search(text[:2000])
    return m.group(1).strip() if m else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    hints = load_hints()
    warnings: list[str] = []
    checked = 0

    for src in reg.get("sources") or []:
        if src.get("id") != "blackmatrix7" or not src.get("enabled", True):
            continue
        for rule in src.get("rules") or []:
            sid = rule.get("name")
            path = rule.get("path") or ""
            if not sid or not path.endswith((".yaml", ".yml")):
                continue
            local = rule.get("local") or Path(path).name
            f = find_bm_file(local, args.date)
            if not f:
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            checked += 1
            uname = extract_name(text)
            if not uname:
                warnings.append(f"{sid}: no # NAME header in {local}")
                continue
            expected = hints.get(sid) or {}
            tokens = expected.get("name_tokens") if isinstance(expected, dict) else None
            if not tokens:
                tokens = default_expected(sid)
            tokens_l = [str(t).lower() for t in tokens]
            if uname.lower() not in tokens_l and not any(
                t in uname.lower() or uname.lower() in t for t in tokens_l
            ):
                warnings.append(
                    f"{sid}: upstream NAME '{uname}' not in expected {tokens} ({local})"
                )

    print(f"[identity_validate] checked={checked} warnings={len(warnings)}")
    for w in warnings[:40]:
        print(f"  WARN  {w}")
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
