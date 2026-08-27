#!/usr/bin/env python3
"""quality_validate.py — P1-3 abnormal domain width (warn-first).

Flags bare public suffixes, ultra-short labels, pathological wildcards.
Does not fail the pipeline unless --strict.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"

SHORT_PUBLIC = frozenset(
    {
        "com",
        "net",
        "org",
        "edu",
        "gov",
        "io",
        "co",
        "cn",
        "hk",
        "tw",
        "jp",
        "kr",
        "uk",
        "de",
        "fr",
        "ru",
        "info",
        "xyz",
        "top",
        "app",
        "dev",
        "me",
        "tv",
        "cc",
    }
)


def issues(value: str, rule_type: str) -> list[str]:
    v = (value or "").strip().lower().rstrip(".")
    if not v:
        return ["empty"]
    out: list[str] = []
    if v.startswith("."):
        out.append("leading-dot")
    if " " in v or "\\" in v:
        out.append("whitespace-or-backslash")
    if rule_type in ("domain", "domain_suffix", "domain_keyword") or rule_type == "line":
        labels = [x for x in v.split(".") if x]
        if len(labels) == 1 and labels[0] in SHORT_PUBLIC:
            out.append(f"bare-public-suffix:{labels[0]}")
        if len(labels) == 1 and len(labels[0]) <= 2 and labels[0].isalpha():
            out.append(f"ultra-short-label:{labels[0]}")
        if v in ("*", "*.*", "."):
            out.append("pathological-wildcard")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--max-warn", type=int, default=40)
    args = ap.parse_args()

    warnings: list[str] = []

    if SERVICES.is_dir():
        for path in sorted(SERVICES.glob("*.yaml")):
            if path.name.startswith("example"):
                continue
            try:
                doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            if not isinstance(doc, dict):
                continue
            for i, r in enumerate(doc.get("rules") or []):
                if not isinstance(r, dict):
                    continue
                t = (r.get("type") or "").lower()
                v = str(r.get("value") or "")
                if t not in ("domain", "domain_suffix", "domain_keyword"):
                    continue
                for iss in issues(v, t):
                    warnings.append(f"{path.stem} rules[{i}]: {iss} value={v[:60]}")

    # sample domains sidecars lightly (first 500 lines each) for extreme width
    if DOMAINS.is_dir():
        for path in sorted(DOMAINS.glob("*.txt")):
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[:500]
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                for iss in issues(line, "line"):
                    warnings.append(f"{path.name}:{i}: {iss} value={line[:60]}")

    shown = warnings[: args.max_warn]
    print(f"[quality_validate] flags={len(warnings)} shown={len(shown)}")
    for w in shown:
        print(f"  WARN  {w}")
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
