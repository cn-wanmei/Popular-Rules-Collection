#!/usr/bin/env python3
"""collect_datasets.py — fetch Network Dataset sources (geosite/geoip/mmdb/dat).

Isolated from Service Rules collect. Writes database/{geosite,geoip}/ and
generated/mmdb artifacts + provenance. Never writes into database/services.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fetchers import get_fetcher  # noqa: E402
from ip_cidr import normalize_lines  # noqa: E402

DS_DIR = ROOT / "sources" / "datasets"
PROV = ROOT / "database" / "datasets_provenance"
BACKUP = ROOT / "backup"
REPORTS = ROOT / "reports"

DOMAIN_KINDS = {"geosite"}
CIDR_KINDS = {"geoip"}


def load_all_datasets() -> list[tuple[str, dict, dict]]:
    out: list[tuple[str, dict, dict]] = []
    if not DS_DIR.is_dir():
        return out
    for path in sorted(DS_DIR.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        kind = str(doc.get("kind") or path.stem)
        for ds in doc.get("datasets") or []:
            if isinstance(ds, dict):
                out.append((kind, doc, ds))
    return out


def main() -> int:
    now = datetime.now(timezone.utc)
    day = now.strftime("%Y-%m-%d")
    bak = BACKUP / day / "datasets"
    bak.mkdir(parents=True, exist_ok=True)
    PROV.mkdir(parents=True, exist_ok=True)

    ok = fail = skip = 0
    results: dict[str, dict] = {}

    for kind, _doc, ds in load_all_datasets():
        did = str(ds.get("id") or "?")
        if not ds.get("enabled"):
            skip += 1
            continue
        fetch = ds.get("fetch")
        if not fetch:
            skip += 1
            continue

        remote_path = ds.get("remote_path") or ds.get("path_remote")
        if not remote_path and not (fetch or {}).get("url"):
            print(f"  SKIP {did}: missing remote_path/url")
            fail += 1
            continue
        if not remote_path:
            remote_path = str((fetch or {}).get("url"))

        fetcher = get_fetcher(fetch)
        url = (fetch or {}).get("url") or remote_path
        fr = fetcher.fetch_one({"path": remote_path, "url": url, "name": did, "local": f"{did}.bin"})
        if not fr.ok or not fr.content:
            print(f"  FAIL {did}: {fr.error}")
            fail += 1
            continue

        content: bytes = fr.content
        sha = hashlib.sha256(content).hexdigest()
        (bak / f"{did}.bin").write_bytes(content)

        scope = str(ds.get("scope") or kind)
        dest_path = ds.get("path")
        artifact = ds.get("artifact")

        if scope == "artifact" or artifact:
            art = Path(artifact or f"generated/mmdb/{did}")
            if not art.is_absolute():
                art = ROOT / art
            art.parent.mkdir(parents=True, exist_ok=True)
            art.write_bytes(content)
            meta = {
                "id": did,
                "kind": kind,
                "scope": "artifact",
                "path": str(art.relative_to(ROOT)),
                "sha256": sha,
                "bytes": len(content),
                "fetched_at": now.isoformat(),
                "source": {
                    "owner": fetch.get("owner"),
                    "repo": fetch.get("repo"),
                    "branch": fetch.get("branch"),
                    "path": remote_path,
                    "url": (fetch or {}).get("url") or remote_path,
                },
            }
            meta_path = art.parent / f"{art.stem}.meta.json"
            meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
            results[did] = meta
            ok += 1
            print(f"  OK ARTIFACT {did} bytes={len(content)} sha256={sha[:12]}…")
            continue

        text = content.decode("utf-8", errors="replace")
        lines = [
            ln.strip()
            for ln in text.splitlines()
            if ln.strip() and not ln.strip().startswith("#")
        ]

        if not dest_path:
            print(f"  SKIP {did}: no path")
            fail += 1
            continue
        dest = ROOT / str(dest_path)
        dest.parent.mkdir(parents=True, exist_ok=True)

        if kind in CIDR_KINDS or scope == "country":
            merged = normalize_lines(lines)
            dest.write_text("\n".join(merged) + ("\n" if merged else ""), encoding="utf-8")
            n = len(merged)
        else:
            seen: set[str] = set()
            out_lines: list[str] = []
            for ln in lines:
                v = ln
                for prefix in (
                    "domain:",
                    "full:",
                    "keyword:",
                    "regexp:",
                    "DOMAIN,",
                    "DOMAIN-SUFFIX,",
                ):
                    if v.lower().startswith(prefix.lower()):
                        v = v[len(prefix) :].strip()
                key = v.lower()
                if key in seen:
                    continue
                seen.add(key)
                out_lines.append(v)
            dest.write_text(
                "\n".join(out_lines) + ("\n" if out_lines else ""), encoding="utf-8"
            )
            n = len(out_lines)

        prov = {
            "id": did,
            "kind": kind,
            "scope": scope,
            "path": str(dest_path),
            "lines": n,
            "sha256_source": sha,
            "fetched_at": now.isoformat(),
            "source": {
                "owner": fetch.get("owner"),
                "repo": fetch.get("repo"),
                "branch": fetch.get("branch"),
                "path": remote_path,
                "url": (fetch or {}).get("url") or remote_path,
            },
            "notes": ds.get("notes") or "",
        }
        (PROV / f"{did}.json").write_text(
            json.dumps(prov, indent=2) + "\n", encoding="utf-8"
        )
        results[did] = prov
        ok += 1
        print(f"  OK {did} kind={kind} lines={n}")

    rep_dir = REPORTS / day
    rep_dir.mkdir(parents=True, exist_ok=True)
    (rep_dir / "dataset_collect.json").write_text(
        json.dumps(
            {"ok": ok, "failed": fail, "skipped": skip, "results": results},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[collect_datasets] ok={ok} failed={fail} skipped={skip}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
