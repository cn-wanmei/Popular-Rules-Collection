"""Shared registry helpers: local filename → service id, source priority."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "sources" / "registry.yaml"

SERVICE_POLICY: dict[str, str] = {
    "adblock": "reject",
    "china": "direct",
    "private": "direct",
    "applications": "direct",
    "proxy": "proxy",
    "gfw": "proxy",
    "apple": "proxy",
    "google": "proxy",
    "microsoft": "proxy",
    "github": "proxy",
    "telegram": "proxy",
    "discord": "proxy",
    "openai": "proxy",
    "youtube": "proxy",
    "netflix": "proxy",
    "disney": "proxy",
    "bilibili": "direct",
    "steam": "proxy",
    "tiktok": "proxy",
    "twitter": "proxy",
}


def load_registry() -> dict[str, Any]:
    return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}


def local_to_service() -> dict[str, str]:
    reg = load_registry()
    m: dict[str, str] = {}
    for src in reg.get("sources") or []:
        for r in src.get("rules") or src.get("files") or []:
            if not isinstance(r, dict):
                continue
            local = r.get("local")
            if not local and r.get("name") and str(r["name"]).endswith((".yaml", ".list", ".txt", ".conf")):
                local = r["name"]
            if not local:
                local = Path(str(r.get("path", ""))).name
            service = str(r.get("service") or r.get("name") or Path(str(local)).stem).lower()
            for prefix in ("clash_", "surge_"):
                if service.startswith(prefix):
                    service = service[len(prefix):]
            if local:
                m[str(local)] = service
    return m


def source_priority() -> dict[str, int]:
    reg = load_registry()
    return {s["id"]: int(s.get("priority") or 50) for s in reg.get("sources") or [] if s.get("id")}


def policy_for(service_id: str) -> str:
    return SERVICE_POLICY.get(service_id, "proxy")
