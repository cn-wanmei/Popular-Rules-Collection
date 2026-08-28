#!/usr/bin/env python3
"""build_network_lan.py — emit LAN/private network dataset for clients.

Does not touch generated/{mihomo,sing-box,...} service trees.
Writes generated/network/ only.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NET = ROOT / "database" / "network"
OUT = ROOT / "generated" / "network"


def load_cidrs(name: str) -> list[str]:
    p = NET / name
    if not p.exists():
        return []
    out: list[str] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out


def write(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def main() -> int:
    lan = load_cidrs("lan.txt")
    private = load_cidrs("private.txt")
    OUT.mkdir(parents=True, exist_ok=True)

    write(OUT / "lan.txt", lan)
    write(OUT / "private.txt", private)

    def clash_style(cidrs: list[str]) -> list[str]:
        lines = []
        for c in cidrs:
            host = c.split("/")[0]
            lines.append(f"IP-CIDR6,{c}" if ":" in host else f"IP-CIDR,{c}")
        return lines

    write(OUT / "lan_mihomo.list", clash_style(lan))
    write(OUT / "private_mihomo.list", clash_style(private))
    write(OUT / "lan_surge.list", clash_style(lan))
    write(OUT / "lan_singbox_cidrs.txt", lan)

    print(f"[build_network_lan] lan={len(lan)} private={len(private)} out={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
