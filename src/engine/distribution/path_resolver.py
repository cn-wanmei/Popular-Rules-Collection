"""Deterministic output path resolver shared by distribution builders."""
from __future__ import annotations

from pathlib import Path


class EntityPathResolver:
    """Resolve entity paths from semantic identity.

    Directory layout is intentionally independent from rule rendering logic.
    """

    @staticmethod
    def _safe(value: str) -> str:
        value = str(value).strip().casefold()
        if not value or value in {".", ".."}:
            raise ValueError(f"invalid path component: {value!r}")
        return value

    @classmethod
    def human_service(cls, provider: str, service: str) -> Path:
        provider = cls._safe(provider)
        service = cls._safe(service)
        return Path("rule") / provider / service / f"{service}.yaml"

    @classmethod
    def human_provider(cls, provider: str) -> Path:
        provider = cls._safe(provider)
        return Path("rule") / provider / provider / f"{provider}.yaml"

    @classmethod
    def generated_service(cls, client: str, provider: str, service: str) -> Path:
        client = cls._safe(client)
        provider = cls._safe(provider)
        service = cls._safe(service)
        return Path("generated") / client / provider / service / service


__all__ = ["EntityPathResolver"]
