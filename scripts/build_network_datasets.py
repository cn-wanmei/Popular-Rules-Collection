#!/usr/bin/env python3
"""build_network_datasets.py — export geosite/geoip/policy under generated/.

Does not touch Service client trees (generated/mihomo, …).
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def copy_txt(src: Path, dest: Path) -> int:
    if not src.exists():
        return 0
    lines = [
        ln.strip()
        for ln in src.read_text(encoding="utf-8", errors="replace").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return len(lines)


def domain_to_clash(src: Path, dest: Path) -> int:
    if not src.exists():
        return 0
    out = []
    for ln in src.read_text(encoding="utf-8", errors="replace").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        out.append(f"DOMAIN-SUFFIX,{s.lstrip('.')}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(out) + ("\n" if out else ""), encoding="utf-8")
    return len(out)


def cidr_to_clash(src: Path, dest: Path) -> int:
    if not src.exists():
        return 0
    out = []
    for ln in src.read_text(encoding="utf-8", errors="replace").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        host = s.split("/")[0]
        out.append(f"IP-CIDR6,{s}" if ":" in host else f"IP-CIDR,{s}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(out) + ("\n" if out else ""), encoding="utf-8")
    return len(out)


def main() -> int:
    gdir = ROOT / "generated" / "geosite"
    for name in ("direct", "proxy"):
        n = copy_txt(ROOT / "database" / "geosite" / f"{name}.txt", gdir / f"{name}.txt")
        domain_to_clash(
            ROOT / "database" / "geosite" / f"{name}.txt", gdir / f"{name}_mihomo.list"
        )
        print(f"  geosite/{name}: {n}")

    ipdir = ROOT / "generated" / "geoip"
    for name in ("cn", "jp", "hk", "sg", "kr", "tw"):
        n = copy_txt(ROOT / "database" / "geoip" / f"{name}.txt", ipdir / f"{name}.txt")
        cidr_to_clash(
            ROOT / "database" / "geoip" / f"{name}.txt", ipdir / f"{name}_mihomo.list"
        )
        print(f"  geoip/{name}: {n}")

    pdir = ROOT / "generated" / "policies"
    for sub in ("direct", "proxy", "dns"):
        src_root = ROOT / "database" / "policies" / sub
        if not src_root.is_dir():
            continue
        for f in src_root.glob("*"):
            if f.is_file():
                dest = pdir / sub / f.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(f.read_bytes())
    print("[build_network_datasets] done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
