"""Format-aware raw-rule parser for the V3 Engine.

Public APIs remain ``parse_line`` / ``iter_rules``. ``detect_format`` makes the
input grammar explicit so Source Semantic Gate can audit the parser decision.
The line-aware API is the single-pass provenance path used by Legacy Asset
Extractor; the legacy APIs remain backward compatible.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Iterator

import yaml

from src.engine.ingest.formats.v2fly import (
    iter_expanded_records,
    looks_like as looks_like_v2fly,
    parse_line as parse_v2fly_line,
)

PLAIN_DOMAIN = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\.?$")
URL_RE = re.compile(r"^https?://[^\s]+$", re.I)
DOMAIN_RE = re.compile(r"^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|DOMAIN-REGEX)[,\s]+(.+)$", re.I)
HOST_RE = re.compile(r"^(HOST|HOST-KEYWORD)[,\s]+(.+)$", re.I)
IP_RE = re.compile(r"^(?:IP-CIDR|IP-CIDR6|IP6-CIDR)[,\s]+([0-9a-fA-F:.\/]+)(?:,.*)?$", re.I)
PROCESS_RE = re.compile(r"^(PROCESS-NAME|PROCESS-PATH)[,\s]+(.+)$", re.I)
HOSTS_RE = re.compile(r"^(?:0\.0\.0\.0|127\.0\.0\.1)\s+(\S+)")
CIDR_RE = re.compile(r"^(\d{1,3}(?:\.\d{1,3}){3}/\d{1,2}|[0-9a-fA-F:]+/\d{1,3})$")


def detect_format(path: Path, text: str | None = None) -> str:
    path = Path(path)
    text = text if text is not None else path.read_text(encoding="utf-8", errors="replace")
    if looks_like_v2fly(text, path):
        return "v2fly"
    if path.suffix.lower() in {".yaml", ".yml"} or text.lstrip().startswith("payload:"):
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict) and "payload" in data:
            return "clash_yaml"
    head = "\n".join(text.splitlines()[:80])
    if any(line.lstrip().startswith("+.") for line in text.splitlines() if line.strip()):
        return "metacubex_geosite"
    if any(token in head.upper() for token in ("DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "HOST-KEYWORD", "PROCESS-NAME")):
        return "native_list"
    if any(line.strip().startswith(("0.0.0.0 ", "127.0.0.1 ")) for line in text.splitlines()):
        return "hosts"
    return "plain_list"


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

    m = HOST_RE.match(line)
    if m:
        kind = m.group(1).upper()
        value = m.group(2).split(",", 1)[0].strip().strip("'\"").rstrip(".")
        if not value:
            return []
        return [("host" if kind == "HOST" else "host_keyword", value)]

    m = PROCESS_RE.match(line)
    if m:
        kind = m.group(1).upper()
        value = m.group(2).split(",", 1)[0].strip().strip("'\"")
        return [("process_name" if kind == "PROCESS-NAME" else "process_path", value)] if value else []

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


def iter_rule_records_with_line(path: Path) -> Iterator[tuple[Path, int, str, str, str]]:
    """Yield ``(source_path, line, type, value, format)`` in one parse pass."""
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    fmt = detect_format(path, text)
    if fmt == "v2fly":
        yield from ((source, line, typ, value, fmt) for source, line, typ, value in iter_expanded_records(path))
        return
    if fmt == "clash_yaml":
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict) and "payload" in data:
            for item in data.get("payload") or []:
                if isinstance(item, str):
                    for typ, value in parse_line(item):
                        yield path, 0, typ, value, fmt
            return

    for line_no, raw_line in enumerate(text.splitlines(), 1):
        stripped = raw_line.strip().strip("'\"")
        if URL_RE.match(stripped):
            yield path, line_no, "url", stripped, "url"
        for typ, value in parse_line(raw_line):
            yield path, line_no, typ, value, fmt


def iter_rule_records(path: Path) -> Iterable[tuple[str, str, str]]:
    """Yield ``(type, value, detected_format)`` for Source Ingest provenance."""
    for _source, _line, typ, value, fmt in iter_rule_records_with_line(path):
        yield typ, value, fmt


def iter_rules(path: Path) -> Iterable[tuple[str, str]]:
    for typ, value, _fmt in iter_rule_records(path):
        yield typ, value


__all__ = [
    "parse_line",
    "iter_rules",
    "iter_rule_records",
    "iter_rule_records_with_line",
    "detect_format",
    "parse_v2fly_line",
    "looks_like_v2fly",
]
