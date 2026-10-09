#!/usr/bin/env python3
"""build_provider_datasets.py — export provider CIDRs under generated/provider/."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "database" / "provider"
OUT = ROOT / "generated" / "provider"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    if not SRC.is_dir():
        print("[build_provider_datasets] no database/provider")
        return 0
    n = 0
    for p in sorted(SRC.glob("*.txt")):
        lines = [
            ln.strip()
            for ln in p.read_text(encoding="utf-8", errors="replace").splitlines()
            if ln.strip() and not ln.startswith("#")
        ]
        (OUT / p.name).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        clash = []
        for c in lines:
            host = c.split("/")[0]
            clash.append(f"IP-CIDR6,{c}" if ":" in host else f"IP-CIDR,{c}")
        (OUT / f"{p.stem}_mihomo.list").write_text(
            "\n".join(clash) + ("\n" if clash else ""), encoding="utf-8"
        )
        n += 1
        print(f"  {p.name}: {len(lines)}")
    print(f"[build_provider_datasets] files={n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
