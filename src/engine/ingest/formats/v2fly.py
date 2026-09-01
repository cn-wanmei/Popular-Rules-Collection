"""V2Fly/domain-list-community input-format adapter for V3 ingest.

This module deliberately contains format parsing only. It has no dependency
on the legacy V2 runtime, database model, or normalization pipeline.
"""
from __future__ import annotations

import re
from pathlib import Path

PLAIN_DOMAIN = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\.?$"
)
V2FLY_PREFIX = re.compile(r"^(?:full|domain|keyword|regexp|regex|include):\s*(.+)$", re.I)


def parse_line(line: str) -> list[tuple[str, str]]:
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


def expand_file(path: Path, *, depth: int = 0, stack: set[str] | None = None) -> list[tuple[str, str]]:
    """Expand V2Fly include directives with cycle/depth protection."""
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
        for kind, value in parse_line(raw):
            if kind != "include":
                out.append((kind, value))
                continue
            candidates = (
                path.parent / value,
                path.parent / f"v2fly_{value}",
                path.parent / f"{value}.list",
            )
            included = next((candidate for candidate in candidates if candidate.exists()), None)
            if included is not None:
                out.extend(expand_file(included, depth=depth + 1, stack=stack))
    stack.discard(key)
    return out


def looks_like(text: str, path: Path | None = None) -> bool:
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
