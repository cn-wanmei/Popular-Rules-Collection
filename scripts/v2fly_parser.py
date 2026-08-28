"""v2fly domain-list-community parser + include expansion."""
from __future__ import annotations

import re
from pathlib import Path

PLAIN_DOMAIN = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\.?$"
)
V2FLY_PREFIX = re.compile(
    r"^(?:full|domain|keyword|regexp|regex|include):\s*(.+)$", re.I
)


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
        val = m.group(1).strip()
        if not val:
            return []
        if kind == "include":
            return [("include", val.split()[0])]
        if kind == "full":
            return [("domain", val.rstrip("."))]
        if kind == "keyword":
            return [("domain_keyword", val)]
        if kind in ("regexp", "regex"):
            return [("domain_regex", val)]
        return [("domain_suffix", val.rstrip("."))]
    if PLAIN_DOMAIN.match(line.rstrip(".")) or (
        line and "." in line and " " not in line and "/" not in line and not line.startswith("-")
    ):
        return [("domain_suffix", line.rstrip("."))]
    return []


def expand_v2fly_file(
    path: Path, *, depth: int = 0, stack: set[str] | None = None
) -> list[tuple[str, str]]:
    if stack is None:
        stack = set()
    key = str(path.resolve())
    if key in stack or depth > 6:
        return []
    stack.add(key)
    out: list[tuple[str, str]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    for raw in text.splitlines():
        for typ, val in parse_v2fly_line(raw):
            if typ == "include":
                candidates = [
                    path.parent / val,
                    path.parent / f"v2fly_{val}",
                    path.parent / f"{val}.list",
                ]
                inc = next((c for c in candidates if c.exists()), None)
                if inc is None:
                    continue
                out.extend(expand_v2fly_file(inc, depth=depth + 1, stack=stack))
            else:
                out.append((typ, val))
    stack.discard(key)
    return out


def looks_like_v2fly(text: str, path: Path | None = None) -> bool:
    head = "\n".join(text.splitlines()[:40])
    if re.search(r"(?i)^(full|domain|keyword|regexp|regex|include):", head, re.M):
        return True
    if "DOMAIN-SUFFIX" in head.upper() or "payload:" in head:
        return False
    if re.search(r"(?m)^include:", head):
        return True
    if path is not None:
        name = path.name.lower()
        parent = path.parent.name.lower()
        if parent in {"v2fly", "domain-list-community"} or name.startswith("v2fly_"):
            return True
        if path.suffix == "" and not name.endswith((".yaml", ".yml", ".list", ".txt", ".conf")):
            lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
            if lines and sum(
                1
                for ln in lines
                if PLAIN_DOMAIN.match(ln.rstrip(".")) or ln.startswith(("full:", "domain:", "include:"))
            ) >= max(1, len(lines) // 2):
                return True
    return False
