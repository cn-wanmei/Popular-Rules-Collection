#!/usr/bin/env python3
"""validate.py — V1.1 data health + build validation"""

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


def check_cidr(s: str) -> bool:
    try:
        ipaddress.ip_network(s, strict=False)
        return True
    except ValueError:
        return False


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
    }

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
        dfile = DOMAINS / f"{doc['id']}.txt"
        if (doc.get("metadata") or {}).get("stats", {}).get("total", 0) == 0:
            if not dfile.exists() or dfile.stat().st_size == 0:
                warnings.append(f"empty service: {doc['id']}")

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

    for client_dir in GENERATED.iterdir():
        if not client_dir.is_dir():
            continue
        for f in client_dir.iterdir():
            if not f.is_file():
                continue
            stats["generated_files"] += 1
            if f.stat().st_size == 0:
                stats["empty_generated"] += 1
                errors.append(f"empty generated: {f.relative_to(ROOT)}")

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
