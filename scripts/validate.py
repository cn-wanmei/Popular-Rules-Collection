#!/usr/bin/env python3
"""validate.py — data health + expected-output generated validation.

Empty files are errors only when that output was *expected*.
Derived domain-set files must not exist when empty (stale).
"""

from __future__ import annotations

import argparse
import ipaddress
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "database" / "services"
DOMAINS = ROOT / "database" / "domains"
IPS = ROOT / "database" / "ips"
GENERATED = ROOT / "generated"

DOMAIN_SET_CLIENTS = {"surge", "shadowrocket"}


def check_cidr(s: str) -> bool:
    try:
        ipaddress.ip_network(s, strict=False)
        return True
    except ValueError:
        return False


def service_caps(doc: dict) -> dict:
    has_domain = False
    has_keyword = False
    has_ip = False
    has_any = False
    for r in doc.get("rules") or []:
        if not isinstance(r, dict):
            continue
        t = (r.get("type") or "").lower()
        if not r.get("value"):
            continue
        has_any = True
        if t in ("domain", "domain_suffix"):
            has_domain = True
        elif t == "domain_keyword":
            has_keyword = True
        elif t in ("ip_cidr", "ip_cidr6", "ipcidr", "ipcidr6"):
            has_ip = True
    sid = doc.get("id")
    if sid and (DOMAINS / f"{sid}.txt").exists():
        if (DOMAINS / f"{sid}.txt").stat().st_size > 0:
            has_domain = True
            has_any = True
    if sid and (IPS / f"{sid}.txt").exists():
        if (IPS / f"{sid}.txt").stat().st_size > 0:
            has_ip = True
            has_any = True
    return {
        "has_any": has_any,
        "expects_domain_set": has_domain,
        "expects_main": has_any,
        "has_keyword_only": has_keyword and not has_domain and not has_ip,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    stats = {
        "services": 0,
        "domains": 0,
        "ips": 0,
        "invalid_domains": 0,
        "invalid_cidrs": 0,
        "empty_generated": 0,
        "generated_files": 0,
        "stale_domain_set": 0,
    }

    caps_by_id: dict[str, dict] = {}

    for path in sorted(SERVICES.glob("*.yaml")):
        if path.name.startswith("example"):
            continue
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"YAML parse fail {path.name}: {e}")
            continue
        if not doc or not doc.get("id"):
            errors.append(f"missing id: {path.name}")
            continue
        stats["services"] += 1
        sid = doc["id"]
        caps_by_id[sid] = service_caps(doc)
        dfile = DOMAINS / f"{sid}.txt"
        if (doc.get("metadata") or {}).get("stats", {}).get("total", 0) == 0:
            if not dfile.exists() or dfile.stat().st_size == 0:
                warnings.append(f"empty service: {sid}")

    for path in DOMAINS.glob("*.txt"):
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            stats["domains"] += 1
            if " " in line or line.startswith("-"):
                stats["invalid_domains"] += 1
                if stats["invalid_domains"] <= 20:
                    warnings.append(f"suspicious domain {path.name}:{i}: {line[:80]}")

    for path in IPS.glob("*.txt"):
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            stats["ips"] += 1
            if not check_cidr(line):
                stats["invalid_cidrs"] += 1
                errors.append(f"invalid CIDR {path.name}:{i}: {line}")

    if GENERATED.is_dir():
        for client_dir in sorted(GENERATED.iterdir()):
            if not client_dir.is_dir():
                continue
            client = client_dir.name
            for f in sorted(client_dir.iterdir()):
                if not f.is_file():
                    continue
                stats["generated_files"] += 1
                size = f.stat().st_size
                name = f.name

                if name.endswith("_domain.list"):
                    sid = name[: -len("_domain.list")]
                    is_domain_set = True
                elif name.endswith(".list"):
                    sid = name[: -len(".list")]
                    is_domain_set = False
                elif name.endswith(".yaml"):
                    sid = name[: -len(".yaml")]
                    is_domain_set = False
                elif name.endswith(".json"):
                    sid = name[: -len(".json")]
                    is_domain_set = False
                else:
                    sid = name.rsplit(".", 1)[0]
                    is_domain_set = False

                caps = caps_by_id.get(sid)

                if is_domain_set and client in DOMAIN_SET_CLIENTS:
                    if size == 0:
                        stats["empty_generated"] += 1
                        stats["stale_domain_set"] += 1
                        errors.append(
                            f"stale empty domain-set (should not exist): {f.relative_to(ROOT)}"
                        )
                    elif caps and not caps["expects_domain_set"]:
                        warnings.append(
                            f"unexpected domain-set for keyword/ip-only service: {f.relative_to(ROOT)}"
                        )
                    continue

                if size == 0:
                    stats["empty_generated"] += 1
                    if caps and caps["expects_main"]:
                        errors.append(f"empty generated (expected output): {f.relative_to(ROOT)}")
                    else:
                        warnings.append(f"empty generated (no expected rules): {f.relative_to(ROOT)}")

    report = f"""# Data Health — {args.date}

| Metric | Value |
|--------|------:|
| Services | {stats['services']} |
| Domain lines | {stats['domains']} |
| IP/CIDR lines | {stats['ips']} |
| Invalid CIDR | {stats['invalid_cidrs']} |
| Suspicious domains | {stats['invalid_domains']} |
| Generated files | {stats['generated_files']} |
| Empty generated | {stats['empty_generated']} |
| Stale domain-set | {stats['stale_domain_set']} |
| Errors | {len(errors)} |
| Warnings | {len(warnings)} |

## Errors
"""
    report += "\n".join(f"- {e}" for e in errors[:50]) or "- none"
    report += "\n\n## Warnings\n"
    report += "\n".join(f"- {w}" for w in warnings[:50]) or "- none"
    report += "\n"
    out = ROOT / "reports" / args.date / "source-health.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    hp = ROOT / "sources" / "health.yaml"
    if hp.exists():
        report += "\n## Source Health\n\n```yaml\n" + hp.read_text(encoding="utf-8") + "```\n"
    out.write_text(report, encoding="utf-8")
    print(report)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
