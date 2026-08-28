#!/usr/bin/env python3
"""
normalize.py — V1.1 memory-efficient upstream → Universal Rule Schema
- Streaming parse for large adblock lists
- File→service mapping loaded from registry.yaml (no hardcoded list)
- Full provenance only for non-adblock services
- AdBlock written as domain aggregates + light metadata
- v2fly domain-list-community via v2fly_parser
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

from v2fly_parser import (  # noqa: E402
    V2FLY_PREFIX,
    expand_v2fly_file,
    looks_like_v2fly,
    parse_v2fly_line,
)

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "backup"
DATABASE = ROOT / "database"
SERVICES = DATABASE / "services"
DOMAINS = DATABASE / "domains"
IPS = DATABASE / "ips"


def load_file_to_service() -> dict[str, str]:
    """Build local-filename → service id strictly from registry.yaml."""
    reg_path = ROOT / "sources" / "registry.yaml"
    reg = yaml.safe_load(reg_path.read_text(encoding="utf-8")) or {}
    mapping: dict[str, str] = {}
    for src in reg.get("sources") or []:
        for r in src.get("rules") or []:
            name = r.get("name")
            if not name:
                continue
            local = r.get("local")
            path = r.get("path") or ""
            if local:
                mapping[local] = name
            base = path.rsplit("/", 1)[-1] if path else ""
            if base:
                mapping[base] = name
    return mapping


FILE_TO_SERVICE: dict[str, str] = {}


SERVICE_META: dict[str, dict[str, str]] = {
    "apple": {"name": "Apple", "category": "service"},
    "google": {"name": "Google", "category": "service"},
    "telegram": {"name": "Telegram", "category": "social"},
    "netflix": {"name": "Netflix", "category": "streaming"},
    "github": {"name": "GitHub", "category": "service"},
    "microsoft": {"name": "Microsoft", "category": "service"},
    "discord": {"name": "Discord", "category": "social"},
    "openai": {"name": "OpenAI", "category": "ai"},
    "youtube": {"name": "YouTube", "category": "streaming"},
    "bilibili": {"name": "Bilibili", "category": "streaming"},
    "steam": {"name": "Steam", "category": "game"},
    "tiktok": {"name": "TikTok", "category": "social"},
    "twitter": {"name": "Twitter", "category": "social"},
    "disney": {"name": "Disney", "category": "streaming"},
    "china": {"name": "China", "category": "network"},
    "private": {"name": "Private / LAN", "category": "network"},
    "adblock": {"name": "AdBlock", "category": "adblock"},
    "gfw": {"name": "GFW", "category": "network"},
    "proxy": {"name": "Proxy", "category": "network"},
    "applications": {"name": "Applications", "category": "other"},
    "ai": {"name": "AI (aggregate)", "category": "ai"},
    "claude": {"name": "Claude", "category": "ai"},
    "gemini": {"name": "Gemini", "category": "ai"},
    "copilot": {"name": "Copilot", "category": "ai"},
    "spotify": {"name": "Spotify", "category": "streaming"},
    "twitch": {"name": "Twitch", "category": "streaming"},
    "hbo": {"name": "HBO / Max", "category": "streaming"},
    "hulu": {"name": "Hulu", "category": "streaming"},
    "primevideo": {"name": "Prime Video", "category": "streaming"},
    "appletv": {"name": "Apple TV+", "category": "streaming"},
    "reddit": {"name": "Reddit", "category": "social"},
    "facebook": {"name": "Facebook", "category": "social"},
    "instagram": {"name": "Instagram", "category": "social"},
    "whatsapp": {"name": "WhatsApp", "category": "social"},
    "onedrive": {"name": "OneDrive", "category": "service"},
    "googlefcm": {"name": "Google FCM", "category": "service"},
    "paypal": {"name": "PayPal", "category": "finance"},
    "epic": {"name": "Epic Games", "category": "game"},
    "nintendo": {"name": "Nintendo", "category": "game"},
    "xbox": {"name": "Xbox", "category": "game"},
    "playstation": {"name": "PlayStation", "category": "game"},
    "ea": {"name": "EA", "category": "game"},
    "ubisoft": {"name": "Ubisoft", "category": "game"},
    "rockstar": {"name": "Rockstar", "category": "game"},
    "hoyoverse": {"name": "HoYoverse", "category": "game"},
    "cloudflare": {"name": "Cloudflare", "category": "developer"},
    "gitlab": {"name": "GitLab", "category": "developer"},
    "developer": {"name": "Developer", "category": "developer"},
    "speedtest": {"name": "Speedtest", "category": "network"},
    "icloud": {"name": "iCloud", "category": "service"},
    "applemusic": {"name": "Apple Music", "category": "streaming"},
    "adblock-pro": {"name": "AdBlock Pro", "category": "adblock"},
    "adblock-light": {"name": "AdBlock Light", "category": "adblock"},
}

LARGE_SERVICES = {"adblock", "proxy", "china", "gfw"}

DOMAIN_RE = re.compile(
    r"^(?:DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|DOMAIN-REGEX)[,\s]+(.+?)(?:,.*)?$",
    re.I,
)
IP_RE = re.compile(r"^(?:IP-CIDR|IP-CIDR6|IP6-CIDR)[,\s]+([0-9a-fA-F:.\/]+)(?:,.*)?$", re.I)
HOSTS_RE = re.compile(r"^(?:0\.0\.0\.0|127\.0\.0\.1)\s+(\S+)")
CIDR_RE = re.compile(r"^(\d{1,3}(?:\.\d{1,3}){3}/\d{1,2}|[0-9a-fA-F:]+/\d{1,3})$")
PLAIN_DOMAIN = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\.?$"
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_line(line: str) -> list[tuple[str, str]]:
    line = line.strip()
    if not line or line[0] in "#/;!":
        return []
    if " #" in line:
        line = line.split(" #", 1)[0].strip()

    m = DOMAIN_RE.match(line)
    if m:
        raw = m.group(0).upper()
        val = m.group(1).strip().strip("'\"").rstrip(".")
        if "DOMAIN-SUFFIX" in raw:
            return [("domain_suffix", val)]
        if "DOMAIN-KEYWORD" in raw:
            return [("domain_keyword", val)]
        if "DOMAIN-REGEX" in raw:
            return [("domain_regex", val)]
        return [("domain", val)]

    m = IP_RE.match(line)
    if m:
        val = m.group(1).strip()
        return [("ip_cidr6", val)] if ":" in val else [("ip_cidr", val)]

    m = HOSTS_RE.match(line)
    if m:
        return [("domain_suffix", m.group(1).rstrip("."))]

    if line.startswith("+."):
        return [("domain_suffix", line[2:].rstrip("."))]
    if line.startswith("."):
        return [("domain_suffix", line[1:].rstrip("."))]

    if CIDR_RE.match(line):
        return [("ip_cidr6", line)] if ":" in line else [("ip_cidr", line)]

    d = line.split(",")[0].strip().rstrip(".")
    if d.startswith("||"):
        d = d[2:]
    if d.endswith("^"):
        d = d[:-1]
    if d.startswith("@@"):
        return []
    if PLAIN_DOMAIN.match(d) or (
        d and "." in d and " " not in d and "/" not in d and not d.startswith("-")
    ):
        return [("domain_suffix", d)]
    return []


def iter_rules_from_file(path: Path) -> Iterable[tuple[str, str]]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    if looks_like_v2fly(text, path) and path.suffix not in {".yaml", ".yml"}:
        yield from expand_v2fly_file(path)
        return
    is_yamlish = path.suffix in {".yaml", ".yml"} or text.lstrip().startswith("payload:")
    if is_yamlish:
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict) and "payload" in data:
                for item in data["payload"] or []:
                    if isinstance(item, str):
                        yield from parse_line(item)
                return
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        yield from parse_line(item)
                return
        except yaml.YAMLError:
            pass
    for line in text.splitlines():
        stripped = line.strip().split(" #", 1)[0].strip() if " #" in line else line.strip()
        if V2FLY_PREFIX.match(stripped):
            yield from parse_v2fly_line(line)
        else:
            yield from parse_line(line)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    parser.add_argument("--skip-large", action="store_true", help="Skip adblock/proxy mega lists")
    args = parser.parse_args()

    day = BACKUP / args.date / "sources"
    if not day.exists():
        print(f"[normalize] missing {day}")
        return 1

    global FILE_TO_SERVICE
    FILE_TO_SERVICE = load_file_to_service()
    print(f"[normalize] registry file→service mappings: {len(FILE_TO_SERVICE)}")
    reg = yaml.safe_load((ROOT / "sources" / "registry.yaml").read_text(encoding="utf-8"))
    prio = {s["id"]: s.get("priority", 50) for s in reg.get("sources", [])}

    values: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    sources_seen: dict[str, set[str]] = defaultdict(set)

    file_count = 0
    for src_dir in sorted(day.iterdir()):
        if not src_dir.is_dir():
            continue
        source_id = src_dir.name
        for f in sorted(src_dir.iterdir()):
            if not f.is_file():
                continue
            service_id = FILE_TO_SERVICE.get(f.name)
            if not service_id:
                continue
            if args.skip_large and service_id in LARGE_SERVICES:
                print(f"  skip large {source_id}/{f.name}")
                continue
            n = 0
            for typ, val in iter_rules_from_file(f):
                values[service_id][typ].add(val)
                n += 1
            sources_seen[service_id].add(source_id)
            file_count += 1
            print(f"  parsed {source_id}/{f.name} → {service_id} (~{n} lines)")

    SERVICES.mkdir(parents=True, exist_ok=True)
    DOMAINS.mkdir(parents=True, exist_ok=True)
    IPS.mkdir(parents=True, exist_ok=True)

    written = 0
    for service_id, by_type in sorted(values.items()):
        meta = SERVICE_META.get(service_id, {"name": service_id.title(), "category": "other"})
        rules: list[dict[str, Any]] = []
        attach_src = service_id not in LARGE_SERVICES
        src_list = [{"id": s, "priority": prio.get(s, 50)} for s in sorted(sources_seen[service_id])]
        src_list.sort(key=lambda x: -x["priority"])

        for typ in sorted(by_type.keys()):
            for val in sorted(by_type[typ]):
                item: dict[str, Any] = {"type": typ, "value": val}
                if attach_src:
                    item["sources"] = src_list
                rules.append(item)

        domain_count = sum(len(by_type[t]) for t in by_type if t.startswith("domain"))
        ip_count = sum(len(by_type[t]) for t in by_type if t.startswith("ip_"))
        doc = {
            "id": service_id,
            "name": meta["name"],
            "category": meta["category"],
            "type": "mixed" if domain_count and ip_count else ("ip" if ip_count else "domain"),
            "version": 1,
            "source": [{"id": s} for s in sorted(sources_seen[service_id])],
            "rules": rules if service_id not in LARGE_SERVICES else [],
            "metadata": {
                "priority": "high",
                "confidence": "high",
                "last_updated": utc_now_iso(),
                "notes": "Generated by normalize.py V1.1",
                "stats": {
                    "domain_count": domain_count,
                    "ip_count": ip_count,
                    "total": domain_count + ip_count,
                },
            },
        }
        stub = dict(doc)
        if service_id in LARGE_SERVICES:
            stub["rules"] = []
            stub["metadata"]["notes"] += " | large list: see database/domains and database/ips"
        out = SERVICES / f"{service_id}.yaml"
        out.write_text(
            yaml.dump(stub, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )

        domain_vals: set[str] = set()
        for t in ("domain", "domain_suffix"):
            domain_vals |= by_type.get(t, set())
        (DOMAINS / f"{service_id}.txt").write_text(
            "\n".join(sorted(domain_vals)) + ("\n" if domain_vals else ""),
            encoding="utf-8",
        )
        ip_vals = set(by_type.get("ip_cidr", set())) | set(by_type.get("ip_cidr6", set()))
        if ip_vals:
            (IPS / f"{service_id}.txt").write_text(
                "\n".join(sorted(ip_vals)) + "\n", encoding="utf-8"
            )
        written += 1
        print(f"  write {service_id}: domains={domain_count} ips={ip_count}")

    print(f"[normalize] files={file_count} services={written}")
    return 0 if written else 1


if __name__ == "__main__":
    sys.exit(main())
