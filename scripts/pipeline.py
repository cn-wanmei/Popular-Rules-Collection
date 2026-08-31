#!/usr/bin/env python3
"""Local pipeline entry (V2.6)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "config" / "builder_registry.yaml"


def run(cmd: list[str]) -> int:
    print(f"$ {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=ROOT)


def builders() -> list[str]:
    if not REG.exists():
        return [f"scripts/build_{x}.py" for x in ("mihomo", "singbox", "surge", "shadowrocket", "quantumultx", "egern", "loon")]
    doc = yaml.safe_load(REG.read_text(encoding="utf-8")) or {}
    return [v["script"] for v in (doc.get("builders") or {}).values() if v.get("script")]


def preflight() -> int:
    print("[preflight]")
    ok = True
    if sys.version_info < (3, 10):
        print("✗ Python >= 3.10 required")
        ok = False
    else:
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
    print("✓ requirements.txt" if (ROOT / "requirements.txt").exists() else "✗ requirements")
    if (ROOT / "database" / "services").is_dir():
        print("✓ database/services")
    else:
        print("✗ database/services missing")
        ok = False
    print(f"✓ builder_registry ({len(builders())} builders)" if REG.exists() else "✗ builder_registry")
    return 0 if ok else 1


def cmd_build() -> int:
    if preflight() != 0:
        print("BUILD BLOCKED")
        return 1
    for s in builders():
        rc = run([sys.executable, str(ROOT / s)])
        if rc != 0:
            return rc
    return 0


def cmd_validate() -> int:
    for s in ("scripts/schema_validate.py", "scripts/validate.py", "scripts/builder_validate.py", "scripts/size_gate.py"):
        rc = run([sys.executable, str(ROOT / s)])
        if rc != 0:
            return rc
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["preflight", "collect", "normalize", "deduplicate", "build", "validate", "all"])
    args = ap.parse_args()
    if args.command == "preflight":
        return preflight()
    if args.command == "collect":
        return run([sys.executable, str(ROOT / "scripts/collect.py")])
    if args.command == "normalize":
        return run([sys.executable, str(ROOT / "scripts/normalize.py")])
    if args.command == "deduplicate":
        return run([sys.executable, str(ROOT / "scripts/deduplicate.py")])
    if args.command == "build":
        return cmd_build()
    if args.command == "validate":
        return cmd_validate()
    if args.command == "all":
        if preflight() != 0:
            return 1
        for s in ("scripts/normalize.py", "scripts/deduplicate.py"):
            rc = run([sys.executable, str(ROOT / s)])
            if rc != 0:
                return rc
        rc = cmd_build()
        return rc if rc != 0 else cmd_validate()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
