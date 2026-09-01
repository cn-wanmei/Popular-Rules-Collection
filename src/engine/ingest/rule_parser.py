"""Input-format rule parser for the V3 Engine.

This module is a format adapter only. It parses common raw upstream formats,
including Clash-style YAML payloads and V2Fly/domain-list-community syntax,
without importing the legacy V2 runtime or data model.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import yaml

PLAIN_DOMAIN = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\.?$")
V2FLY_PREFIX = re.compile(r"^(?:full|domain|keyword|regexp|regex|include):\s*(.+)$", re.I)
DOMAIN_RE = re.compile(r"^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|DOMAIN-REGEX)[,\s]+(.+)$", re.I)
IP_RE = re.compile(r"^(?:IP-CIDR|IP-CIDR6|IP6-CIDR)[,\s]+([0-9a-fA-F:.\/]+)(?:,.*)?$", re.I)
HOSTS_RE = re.compile(r"^(?:0\.0\.0\.0|127\.0\.0\.1)\s+(\S+)")
CIDR_RE = re.compile(r"^(\d{1,3}(?:\.\d{1,3}){3}/\d{1,2}|[0-9a-fA-F:]+/\d{1,3})$")


def parse_v2fly_line(line: str) -> list[tuple[str, str]]:
    line = line.strip()
    if not line or line.startswith("#"):
        return []
    if " #" in line:
        line = line.split(" #", 1)[0].strip()
    if " @" in line:
        line = line.split(" @", 1)[0].strip()
    m = V2FLY_PREFIX.match(line)
    if m:
        kind = line.split(":", 1)[0].lower()
        value = m.group(1).strip()
        if not value:
            return []
        if kind == "include":
            return [("include", value.split()[0])]
        if kind == "full":
            return [("domain", value.rstrip("."))]
        if kind == "keyword":
            return [("domain_keyword", value)]
        if kind in {"regexp", "regex"}:
            return [("domain_regex", value)]
        return [("domain_suffix", value.rstrip("."))]
    if PLAIN_DOMAIN.match(line.rstrip(".")) or (
        line and "." in line and " " not in line and "/" not in line and not line.startswith("-")
    ):
        return [("domain_suffix", line.rstrip("."))]
    return []


def parse_line(line: str) -> list[tuple[str, str]]:
    line = line.strip()
    if not line or line[0] in "#/;!":
        return []
    if line.startswith("-"):
        line = line[1:].strip()
    line = line.strip("'\"")
    if " #" in line:
        line = line.split(" #", 1)[0].strip()

    m = DOMAIN_RE.match(line)
    if m:
        kind = m.group(1).upper()
        value = m.group(2).split(",", 1)[0].strip().strip("'\"").rstrip(".")
        if not value:
            return []
        if kind == "DOMAIN-SUFFIX":
            return [("domain_suffix", value)]
        if kind == "DOMAIN-KEYWORD":
            return [("domain_keyword", value)]
        if kind == "DOMAIN-REGEX":
            return [("domain_regex", value)]
        return [("domain", value)]

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


def _expand_v2fly_file(path: Path, *, depth: int = 0, stack: set[str] | None = None) -> list[tuple[str, str]]:
    if stack is None:
        stack = set()
    key = str(path.resolve())
    if key in stack or depth > 8:
        return []
    stack.add(key)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        stack.discard(key)
        return []
    out: list[tuple[str, str]] = []
    for raw in text.splitlines():
        for typ, value in parse_v2fly_line(raw):
            if typ != "include":
                out.append((typ, value))
                continue
            candidates = (
                path.parent / value,
                path.parent / f"v2fly_{value}",
                path.parent / f"{value}.list",
            )
            inc = next((candidate for candidate in candidates if candidate.exists()), None)
            if inc is not None:
                out.extend(_expand_v2fly_file(inc, depth=depth + 1, stack=stack))
    stack.discard(key)
    return out


def looks_like_v2fly(text: str, path: Path | None = None) -> bool:
    head = "\n".join(text.splitlines()[:40])
    if re.search(r"(?i)^(full|domain|keyword|regexp|regex|include):", head, re.M):
        return True
    if "DOMAIN-SUFFIX" in head.upper() or "payload:" in head:
        return False
    if path is not None:
        parent = path.parent.name.lower()
        name = path.name.lower()
        if parent in {"v2fly", "domain-list-community"} or name.startswith("v2fly_"):
            return True
        if path.suffix == "" and not name.endswith((".yaml", ".yml", ".list", ".txt", ".conf")):
            lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
            if lines and sum(
                1 for ln in lines
                if PLAIN_DOMAIN.match(ln.rstrip(".")) or ln.startswith(("full:", "domain:", "include:"))
            ) >= max(1, len(lines) // 2):
                return True
    return False


def iter_rules(path: Path) -> Iterable[tuple[str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    stripped = text.lstrip()
    if looks_like_v2fly(text, path):
        yield from _expand_v2fly_file(path)
        return

    # YAML list / payload formats are parsed structurally first so list markers,
    # quoting and indentation cannot change the semantic rule type.
    if path.suffix.lower() in {".yaml", ".yml"} or stripped.startswith("payload:"):
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict) and "payload" in data:
            payload = data.get("payload") or []
            for item in payload:
                if isinstance(item, str):
                    yield from parse_line(item)
            return
        if isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    yield from parse_line(item)
            return

    for line in text.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith(("full:", "domain:", "keyword:", "regexp:", "regex:", "include:")):
            yield from parse_v2fly_line(stripped_line)
        else:
            yield from parse_line(stripped_line)
