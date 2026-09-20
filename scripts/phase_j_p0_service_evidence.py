#!/usr/bin/env python3
"""Derive immutable P0 service-level production evidence from one V3 run.

This is an evidence calculator, not a second SSOT. It never promotes a service
merely because an artifact path exists. Production requires all eight hard gates:
identity, source, canonical, semantic, overlap, seven-client, golden, release.
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLIENTS = {
    "mihomo": ".yaml",
    "singbox": ".json",
    "surge": ".list",
    "shadowrocket": ".list",
    "quantumultx": ".list",
    "egern": ".yaml",
    "loon": ".list",
}
RULE_TYPES = {
    "HOST",
    "DOMAIN",
    "HOST-SUFFIX",
    "DOMAIN-SUFFIX",
    "HOST-KEYWORD",
    "DOMAIN-KEYWORD",
    "IP-CIDR",
    "IP6-CIDR",
    "IP-CIDR4",
    "IP-CIDR6",
}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def p0_ids(root: Path) -> list[str]:
    doc = load_yaml(root / "config" / "p0_materialization.yaml")
    ids = []
    for item in doc.get("services") or []:
        if isinstance(item, dict) and item.get("id"):
            ids.append(str(item["id"]).strip())
    return ids


def p0_meta(root: Path) -> dict[str, dict[str, Any]]:
    doc = load_yaml(root / "config" / "p0_materialization.yaml")
    result: dict[str, dict[str, Any]] = {}
    for item in doc.get("services") or []:
        if isinstance(item, dict) and item.get("id"):
            result[str(item["id"]).strip()] = item
    return result


def latest_backup(root: Path) -> Path | None:
    candidates = []
    for path in (root / "backup").glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]"):
        if (path / "sources").is_dir():
            candidates.append(path)
    return max(candidates, key=lambda p: p.name) if candidates else None


def service_token_match(filename: str, sid: str) -> bool:
    stem = Path(filename).stem.casefold()
    wanted = sid.casefold()
    if stem in {wanted, f"geosite_{wanted}", f"v2fly_{wanted}", f"dler_{wanted}"}:
        return True
    return bool(re.search(rf"(^|[_\-.]){re.escape(wanted)}($|[_\-.])", stem))


def find_source(root: Path, sid: str, hints: list[str]) -> Path | None:
    backup = latest_backup(root)
    if backup is None:
        return None
    ranked: list[tuple[int, int, str, Path]] = []
    hint_rank = {str(name).casefold(): i for i, name in enumerate(hints)}
    for path in (backup / "sources").rglob("*"):
        if not path.is_file() or not path.stat().st_size:
            continue
        if not service_token_match(path.name, sid):
            continue
        parent = path.parts[-2].casefold() if len(path.parts) >= 2 else ""
        rank = hint_rank.get(parent, 100)
        exact = 0 if Path(path.name).stem.casefold() in {
            sid.casefold(),
            f"geosite_{sid}".casefold(),
            f"v2fly_{sid}".casefold(),
            f"dler_{sid}".casefold(),
        } else 1
        ranked.append((rank, exact, path.as_posix(), path))
    if not ranked:
        return None
    format_rank = {".list": 0, ".txt": 1, "": 1, ".yaml": 2, ".yml": 2, ".json": 3}
    ranked.sort(key=lambda item: (item[0], format_rank.get(Path(item[-1].name).suffix.casefold(), 2), item[1], item[2]))
    return ranked[0][-1]


def parse_rules(text: str) -> list[dict[str, str]]:
    rules: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for raw in text.splitlines():
        line = raw.strip().strip("\ufeff")
        if not line or line.startswith(("#", "//", ";")):
            continue
        # Standard rule-list syntax: TYPE,value[,options...]
        if "," in line:
            head, value = [part.strip() for part in line.split(",", 1)]
            typ = head.upper()
            value = value.split(",", 1)[0].strip()
            if typ in RULE_TYPES and value:
                key = (typ, value.casefold())
                if key not in seen:
                    seen.add(key)
                    rules.append({"type": typ, "value": value})
                continue
        # MetaCubeX geosite convention: +.example.com
        if line.startswith("+.") and len(line) > 2:
            typ, value = "DOMAIN-SUFFIX", line[2:]
        elif re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*\.[A-Za-z]{2,63}", line):
            typ, value = "DOMAIN-SUFFIX", line
        else:
            continue
        key = (typ, value.casefold())
        if key not in seen:
            seen.add(key)
            rules.append({"type": typ, "value": value})
    return rules


def canonicalize(rules: list[dict[str, str]]) -> list[dict[str, str]]:
    out = []
    for rule in rules:
        typ = rule["type"].strip().upper()
        value = rule["value"].strip()
        identity_key = f"{typ.casefold()}|{value.casefold()}"
        out.append({
            "type": typ,
            "value": value,
            "identity_key": identity_key,
            "rule_id": sha256_text(identity_key),
        })
    return out


def import_matcher():
    from src.engine.audit.matcher import rule_matches
    return rule_matches


def positive_and_negative(rule: dict[str, str]) -> tuple[str, str] | None:
    typ = rule["type"]
    value = rule["value"]
    if typ in {"HOST", "DOMAIN"}:
        return value, value + ".evil.example"
    if typ in {"HOST-SUFFIX", "DOMAIN-SUFFIX"}:
        return value, "x." + value + ".evil.example"
    if typ in {"HOST-KEYWORD", "DOMAIN-KEYWORD"}:
        return value, "x-not-a-service.evil.example"
    if typ in {"IP-CIDR", "IP-CIDR4", "IP6-CIDR", "IP-CIDR6"}:
        try:
            network = ipaddress.ip_network(value, strict=False)
            positive = str(network.network_address + 1)
            if network.num_addresses <= 2:
                positive = str(network.network_address)
            if network.version == 4:
                candidate = network.broadcast_address + 1
                negative = str(candidate) if candidate <= ipaddress.IPv4Address("255.255.255.255") else str(network.network_address - 1)
            else:
                candidate = network.broadcast_address + 1
                negative = str(candidate) if candidate <= ipaddress.IPv6Address("ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff") else str(network.network_address - 1)
            return positive, negative
        except ValueError:
            return None
    return None


def semantic_audit(rules: list[dict[str, str]]) -> dict[str, Any]:
    rule_matches = import_matcher()
    candidates = [r for r in rules if r["type"] in RULE_TYPES][:6]
    probes = []
    blocked_reasons = []
    for rule in candidates:
        pair = positive_and_negative(rule)
        if pair is None:
            continue
        positive, negative = pair
        positive_match = rule_matches(rule, positive)
        negative_match = rule_matches(rule, negative)
        # Keyword rules deliberately require review because a negative lexical
        # boundary cannot prove semantic exclusivity.
        review = rule["type"] in {"HOST-KEYWORD", "DOMAIN-KEYWORD"}
        probes.append({
            "rule_id": rule.get("rule_id"),
            "type": rule["type"],
            "positive": positive,
            "positive_match": positive_match,
            "negative": negative,
            "negative_match": negative_match,
            "review_required": review,
        })
        if review:
            blocked_reasons.append("keyword_rule_requires_explicit_acceptance")
        elif not positive_match or negative_match:
            blocked_reasons.append(f"matcher_probe_failed:{rule['type']}:{rule['value']}")
    if not probes:
        return {"status": "blocked", "probes": [], "reasons": ["no_supported_runtime_probes"]}
    if blocked_reasons:
        return {"status": "blocked", "probes": probes, "reasons": sorted(set(blocked_reasons))}
    return {"status": "pass", "probes": probes, "reasons": []}


def client_presence(build_report: dict[str, Any], sid: str) -> tuple[list[str], dict[str, list[str]]]:
    present = []
    details: dict[str, list[str]] = {}
    for client in CLIENTS:
        client_doc = (build_report.get("clients") or {}).get(client) or {}
        paths = list(client_doc.get("paths") or [])
        hits = [
            p for p in paths
            if f"/{sid}/" in p.casefold()
            or p.casefold().endswith(f"/{sid}.yaml")
            or p.casefold().endswith(f"/{sid}.list")
            or p.casefold().endswith(f"/{sid}.json")
        ]
        if hits:
            present.append(client)
            details[client] = hits[:4]
    return present, details


def service_overlap_audit(
    sid: str, overlap: dict[str, Any]
) -> dict[str, Any]:
    """Project global overlap findings onto one service without false blocking."""
    collisions = [
        collision
        for collision in overlap.get("runtime_collisions", [])
        if collision.get("service") == sid
        or collision.get("other_service") == sid
    ]
    return {
        "status": "blocked" if collisions else "pass",
        "runtime_probe_count": overlap.get("runtime_probe_count", 0),
        "collisions": collisions,
    }


def runtime_overlap(rows: dict[str, dict[str, Any]], rule_matches) -> dict[str, Any]:
    collisions = []
    positives: list[tuple[str, str]] = []
    for sid, row in rows.items():
        for probe in (row.get("semantic") or {}).get("probes") or []:
            if probe.get("positive_match") is True and probe.get("positive"):
                positives.append((sid, str(probe["positive"])))
    for sid, host in positives:
        for other, row in rows.items():
            if other == sid:
                continue
            for rule in row.get("canonical_rules") or []:
                if rule_matches({"type": rule["type"], "value": rule["value"]}, host):
                    collisions.append({
                        "service": sid,
                        "probe": host,
                        "other_service": other,
                        "rule_id": rule["rule_id"],
                    })
                    break
    return {
        "status": "pass" if not collisions else "blocked",
        "runtime_probe_count": len(positives),
        "runtime_collisions": collisions,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    run = args.root / "data" / "runs" / args.run_id
    if not run.is_dir():
        raise SystemExit(f"run not found: {run}")

    build_report = load_json(run / "artifacts" / "build_report.json")
    golden = load_json(run / "golden" / "report.json")
    release = load_json(run / "release" / "manifest.json")
    identities = load_yaml(args.root / "config" / "p0_service_identity.yaml")
    identity_ids = {
        str(item.get("id"))
        for item in identities.get("services") or []
        if isinstance(item, dict) and item.get("id")
    }
    meta = p0_meta(args.root)
    ids = p0_ids(args.root)
    global_golden = golden.get("all_pass") is True
    global_release = release.get("release_state") in {"RC_READY", "RELEASED", "PROMOTED"}

    rows: dict[str, dict[str, Any]] = {}
    for sid in ids:
        hints = list(meta.get(sid, {}).get("source_hints") or [])
        source = find_source(args.root, sid, hints)
        source_text = source.read_text(encoding="utf-8", errors="ignore") if source else ""
        parsed = canonicalize(parse_rules(source_text)) if source else []
        semantic = semantic_audit(parsed) if parsed else {
            "status": "blocked",
            "probes": [],
            "reasons": ["independent_source_missing"],
        }
        present, artifacts = client_presence(build_report, sid)
        identity_pass = sid in identity_ids
        source_pass = source is not None and bool(source_text.strip())
        canonical_pass = source_pass and bool(parsed)
        seven_pass = len(present) == len(CLIENTS)
        semantic_pass = semantic.get("status") == "pass"
        # Overlap is computed after all service canonical rules/probes are loaded.
        rows[sid] = {
            "service_id": sid,
            "identity": "pass" if identity_pass else "blocked",
            "source": {
                "status": "pass" if source_pass else "blocked",
                "snapshot": source.relative_to(args.root).as_posix() if source else None,
                "sha256": sha256_bytes(source.read_bytes()) if source else None,
                "rule_count": len(parsed),
                "hints": hints,
            },
            "canonical_rules": parsed,
            "canonical": "pass" if canonical_pass else "blocked",
            "semantic": semantic,
            "seven_client": {
                "status": "pass" if seven_pass else "blocked",
                "present": sorted(present),
                "count": len(present),
                "expected": len(CLIENTS),
                "artifacts": artifacts,
            },
            "golden": "pass" if global_golden else "blocked",
            "release": "pass" if global_release else "blocked",
            "blockers": [],
        }

    rule_matches = import_matcher()
    overlap = runtime_overlap(rows, rule_matches)
    for sid, row in rows.items():
        scoped = [c for c in overlap["runtime_collisions"] if c["service"] == sid or c["other_service"] == sid]
        row["overlap_audit"] = service_overlap_audit(sid, overlap)
        if row["identity"] != "pass":
            row["blockers"].append("identity")
        if row["source"]["status"] != "pass":
            row["blockers"].append("source")
        if row["canonical"] != "pass":
            row["blockers"].append("canonical")
        if row["semantic"].get("status") != "pass":
            row["blockers"].append("semantic_audit")
        if row["overlap_audit"]["status"] != "pass":
            row["blockers"].append("overlap_audit")
        if row["seven_client"]["status"] != "pass":
            row["blockers"].append("seven_client")
        if row["golden"] != "pass":
            row["blockers"].append("golden")
        if row["release"] != "pass":
            row["blockers"].append("release")
        row["status"] = "production" if not row["blockers"] else "blocked"

    production = [sid for sid, row in rows.items() if row["status"] == "production"]
    blocked = [sid for sid in ids if sid not in production]
    payload = {
        "schema": "phase_j_p0_service_evidence_v2",
        "run_id": args.run_id,
        "queue_size": len(ids),
        "production_count": len(production),
        "blocked_count": len(blocked),
        "production_complete": len(production) == 50,
        "global": {
            "golden": global_golden,
            "release": global_release,
            "client_count": len(CLIENTS),
        },
        "services": {
            sid: {
                k: v for k, v in row.items()
                if k != "canonical_rules"
            }
            for sid, row in rows.items()
        },
        "blocked": {sid: rows[sid]["blockers"] for sid in blocked},
    }
    out = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    print(out, end="")
    target = args.json_out or (run / "reports" / "phase_j_p0_service_evidence.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    # Compatibility path consumed by the existing publication/reporting chain.
    compat = run / "reports" / "service_production_evidence.json"
    compat.write_text(out, encoding="utf-8")
    return 0 if payload["production_complete"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
