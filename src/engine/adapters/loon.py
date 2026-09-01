"""Native loon adapter — real format, not unified .list."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import json

from src.engine.adapters.base import domain_line
from src.engine.adapters.registry import CLIENTS

CLIENT = "loon"
EXT = CLIENTS[CLIENT]["ext"]
FMT = CLIENTS[CLIENT]["format"]


def render(rules: list[dict[str, Any]], out_path: Path) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if FMT == "json":
        # sing-box style minimal ruleset
        payload = {
            "version": 2,
            "rules": [{"domain": [r["value"] for r in rules if r.get("type", "").upper() in ("DOMAIN", "DOMAIN-SUFFIX")]}]
        }
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif FMT == "yaml":
        lines = ["payload:"]
        for r in rules:
            lines.append(f"  - {domain_line(r['type'], r['value'])}")
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    else:  # list
        lines = [domain_line(r["type"], r["value"]) for r in rules]
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path
