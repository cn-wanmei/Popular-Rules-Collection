#!/usr/bin/env python3
"""collect_providers.py — Phase 3C provider CIDRs (Provider ≠ Service)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ip_cidr import normalize_lines  # noqa: E402

REG = ROOT / "sources" / "datasets" / "provider.yaml"
OUT = ROOT / "database" / "provider"
PROV = ROOT / "database" / "datasets_provenance"
REPORTS = ROOT / "reports"


def http_get(url: str, timeout: int = 60) -> bytes:
    req = Request(url, headers={"User-Agent": "Popular-Rules-Collection/1.0"})
    with urlopen(req, timeout=timeout) as r:
        return r.read()


def parse_google_cloud_json(data: bytes) -> list[str]:
    doc = json.loads(data.decode("utf-8", errors="replace"))
    out: list[str] = []
    for pref in doc.get("prefixes") or []:
        if not isinstance(pref, dict):
            continue
        v4 = pref.get("ipv4Prefix") or pref.get("ipv4prefix")
        v6 = pref.get("ipv6Prefix") or pref.get("ipv6prefix")
        if v4:
            out.append(str(v4).strip())
        if v6:
            out.append(str(v6).strip())
    return out


def parse_oracle_json(data: bytes) -> list[str]:
    doc = json.loads(data.decode("utf-8", errors="replace"))
    out: list[str] = []
    regions = doc.get("regions") or []
    if isinstance(regions, list):
        for reg in regions:
            if not isinstance(reg, dict):
                continue
            for cidr in reg.get("cidrs") or []:
                if isinstance(cidr, dict) and cidr.get("cidr"):
                    out.append(str(cidr["cidr"]).strip())
                elif isinstance(cidr, str):
                    out.append(cidr.strip())
    return out


def parse_aws_json(data: bytes) -> list[str]:
    doc = json.loads(data.decode("utf-8", errors="replace"))
    out: list[str] = []
    for pref in doc.get("prefixes") or []:
        if isinstance(pref, dict) and pref.get("ip_prefix"):
            out.append(str(pref["ip_prefix"]).strip())
    for pref in doc.get("ipv6_prefixes") or []:
        if isinstance(pref, dict) and pref.get("ipv6_prefix"):
            out.append(str(pref["ipv6_prefix"]).strip())
    return out


def main() -> int:
    now = datetime.now(timezone.utc)
    if not REG.exists():
        print("[collect_providers] no provider.yaml")
        return 0
    doc = yaml.safe_load(REG.read_text(encoding="utf-8")) or {}
    OUT.mkdir(parents=True, exist_ok=True)
    PROV.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    results: dict[str, dict] = {}
    for ds in doc.get("datasets") or []:
        if not isinstance(ds, dict) or not ds.get("enabled"):
            continue
        did = str(ds.get("id") or "?")
        path = ds.get("path") or ""
        fetch = ds.get("fetch") or {}
        url = fetch.get("url")
        if not url or not path:
            print(f"  SKIP {did}: missing url/path")
            fail += 1
            continue
        if path.startswith("database/ips/"):
            print(f"  HARD skip {did}: provider must not write database/ips/")
            fail += 1
            continue
        try:
            raw = http_get(url)
        except Exception as e:
            print(f"  FAIL {did}: {e}")
            fail += 1
            continue
        fmt = ds.get("format") or "text"
        if fmt == "aws_json":
            lines = parse_aws_json(raw)
        elif fmt == "google_cloud_json":
            lines = parse_google_cloud_json(raw)
        elif fmt == "oracle_json":
            lines = parse_oracle_json(raw)
        else:
            lines = [
                ln.strip()
                for ln in raw.decode("utf-8", errors="replace").splitlines()
                if ln.strip() and not ln.strip().startswith("#")
            ]
        merged = normalize_lines(lines)
        dest = ROOT / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("\n".join(merged) + ("\n" if merged else ""), encoding="utf-8")
        meta = {
            "id": did,
            "scope": "provider",
            "path": path,
            "lines": len(merged),
            "fetched_at": now.isoformat(),
            "source_url": url,
            "notes": ds.get("notes") or "Provider ≠ Service",
        }
        (PROV / f"{did}.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        results[did] = meta
        ok += 1
        print(f"  OK {did} lines={len(merged)}")
    rep = REPORTS / now.strftime("%Y-%m-%d")
    rep.mkdir(parents=True, exist_ok=True)
    (rep / "provider_collect.json").write_text(
        json.dumps({"ok": ok, "failed": fail, "results": results}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[collect_providers] ok={ok} failed={fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
