"""Common raw-rule parser for the V3 Engine.

Format-specific parsing lives under ``src.engine.ingest.formats``. This module
keeps the stable public ``parse_line`` / ``iter_rules`` API while delegating
V2Fly syntax to the dedicated input-format adapter.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import yaml

from src.engine.ingest.formats.v2fly import (
    looks_like as looks_like_v2fly,
    parse_line as parse_v2fly_line,
    expand_file as expand_v2fly_file,
)

PLAIN_DOMAIN = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\.?$")
DOMAIN_RE = re.compile(r"^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|DOMAIN-REGEX)[,\s]+(.+)$", re.I)
IP_RE = re.compile(r"^(?:IP-CIDR|IP-CIDR6|IP6-CIDR)[,\s]+([0-9a-fA-F:.\/]+)(?:,.*)?$", re.I)
HOSTS_RE = re.compile(r"^(?:0\.0\.0\.0|127\.0\.0\.1)\s+(\S+)")
CIDR_RE = re.compile(r"^(\d{1,3}(?:\.\d{1,3}){3}/\d{1,2}|[0-9a-fA-F:]+/\d{1,3})$")


def parse_line(line: str) -> list[tuple[str, str]]:
    line = line.strip()
    if not line or line[0] in "#/;!":
        return []
    if line.startswith("-"):
        line = line[1:].strip()
    line = line.strip("'\"")
    if " #" in line:
        line = line.split(" #", 1)[0].strip()

    v2 = parse_v2fly_line(line)
    if v2 and line.lower().split(":", 1)[0] in {"full", "domain", "keyword", "regexp", "regex"}:
        return v2

    m = DOMAIN_RE.match(line)
    if m:
        kind = m.group(1).upper()
        value = m.group(2).split(",", 1)[0].strip().strip("'\"").rstrip(".")
        if not value:
            return []
        return [({
            "DOMAIN": "domain",
            "DOMAIN-SUFFIX": "domain_suffix",
            "DOMAIN-KEYWORD": "domain_keyword",
            "DOMAIN-REGEX": "domain_regex",
        }[kind], value)]

    m = IP_RE.match(line)
    if m:
        value = m.group(1).strip()
        return [("ip_cidr6", value)] if ":" in value else [("ip_cidr", value)]

    m = HOSTS_RE.match(line)
    if m:
        return [("domain_suffix", m.group(1).rstrip("."))]
    if line.startswith("+."):
        return [("domain_suffix", line[2:].rstrip("."))]
    if line.startswith("."):
        return [("domain_suffix", line[1:].rstrip("."))]
    if CIDR_RE.match(line):
        return [("ip_cidr6", line)] if ":" in line else [("ip_cidr", line)]

    value = line.split(",", 1)[0].strip().rstrip(".")
    if value.startswith("||"):
        value = value[2:]
    if value.endswith("^"):
        value = value[:-1]
    if value.startswith("@@"):
        return []
    if PLAIN_DOMAIN.match(value) or (
        value and "." in value and " " not in value and "/" not in value and not value.startswith("-")
    ):
        return [("domain_suffix", value)]
    return []


def iter_rules(path: Path) -> Iterable[tuple[str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    stripped = text.lstrip()
    if looks_like_v2fly(text, path):
        yield from expand_v2fly_file(path)
        return

    if path.suffix.lower() in {".yaml", ".yml"} or stripped.startswith("payload:"):
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict) and "payload" in data:
            for item in data.get("payload") or []:
                if isinstance(item, str):
                    yield from parse_line(item)
            return
        if isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    yield from parse_line(item)
            return

    for line in text.splitlines():
        yield from parse_line(line)


__all__ = ["parse_line", "iter_rules", "parse_v2fly_line", "looks_like_v2fly", "expand_v2fly_file"]
