"""Deterministic output path resolver shared by distribution builders.

The resolver is the single path contract for the human rule tree and client
artifacts. Provider aggregates intentionally use an identity directory; child
services remain under provider/service/service.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping

LAYOUT_SCHEMA = "directory_layout_v2"

HUMAN_LAYOUT = {
    "human_root": "rule",
    "human_aggregate": "rule/{provider}/{aggregate}/{aggregate}.yaml",
    "human_service": "rule/{provider}/{service}/{service}.yaml",
    "human_china": "rule/china/china.yaml",
    "human_category": "rule/category/{category}/{category}.yaml",
    "human_group": "rule/group/{group}/{group}.yaml",
    "human_aggregate_entity": "rule/aggregate/{aggregate}/{aggregate}.yaml",
    "human_unmapped_service": "rule/unmapped/{service}/{service}.yaml",
}

GENERATED_LAYOUT = {
    "generated_client_root": "generated/{client}",
    "generated_aggregate": "generated/{client}/{provider}/{aggregate}/{aggregate}",
    "generated_service": "generated/{client}/{provider}/{service}/{service}",
    "generated_china": "generated/{client}/china/china",
    "generated_category": "generated/{client}/categories/{category}/{category}",
}


class EntityPathResolver:
    """Resolve stable paths from semantic entity identity."""

    LAYOUT_SCHEMA = LAYOUT_SCHEMA
    HUMAN_LAYOUT = HUMAN_LAYOUT
    GENERATED_LAYOUT = GENERATED_LAYOUT

    @staticmethod
    def _safe(value: str) -> str:
        text = str(value).strip().casefold()
        text = re.sub(r"[^a-z0-9._-]+", "-", text)
        text = re.sub(r"-{2,}", "-", text).strip(".-")
        if not text or text in {".", ".."}:
            raise ValueError(f"invalid path component: {value!r}")
        return text

    @classmethod
    def human_provider(cls, provider: str, aggregate: str | None = None) -> Path:
        provider = cls._safe(provider)
        aggregate = cls._safe(aggregate or provider)
        return Path("rule") / provider / aggregate / f"{aggregate}.yaml"

    @classmethod
    def human_service(cls, provider: str, service: str) -> Path:
        provider = cls._safe(provider)
        service = cls._safe(service)
        return Path("rule") / provider / service / f"{service}.yaml"

    @classmethod
    def human_china(cls) -> Path:
        return Path("rule") / "china" / "china.yaml"

    @classmethod
    def human_category(cls, category: str) -> Path:
        category = cls._safe(category)
        return Path("rule") / "category" / category / f"{category}.yaml"

    @classmethod
    def human_group(cls, group: str) -> Path:
        group = cls._safe(group)
        return Path("rule") / "group" / group / f"{group}.yaml"

    @classmethod
    def human_aggregate(cls, aggregate: str) -> Path:
        aggregate = cls._safe(aggregate)
        return Path("rule") / "aggregate" / aggregate / f"{aggregate}.yaml"

    @classmethod
    def human_unmapped_service(cls, service: str) -> Path:
        service = cls._safe(service)
        return Path("rule") / "unmapped" / service / f"{service}.yaml"

    @classmethod
    def generated_provider(cls, client: str, provider: str, aggregate: str | None = None) -> Path:
        client = cls._safe(client)
        provider = cls._safe(provider)
        aggregate = cls._safe(aggregate or provider)
        return Path("generated") / client / provider / aggregate / aggregate

    @classmethod
    def generated_service(cls, client: str, provider: str, service: str) -> Path:
        client = cls._safe(client)
        provider = cls._safe(provider)
        service = cls._safe(service)
        return Path("generated") / client / provider / service / service

    @classmethod
    def generated_china(cls, client: str) -> Path:
        client = cls._safe(client)
        return Path("generated") / client / "china" / "china"

    @classmethod
    def generated_category(cls, client: str, category: str) -> Path:
        client = cls._safe(client)
        category = cls._safe(category)
        return Path("generated") / client / "categories" / category / category

    @staticmethod
    def _paths(records_or_paths: Iterable[Any]) -> list[str]:
        paths: list[str] = []
        for item in records_or_paths:
            value = item.get("path") if isinstance(item, Mapping) else item
            value = str(value or "").strip()
            if value:
                paths.append(Path(value).as_posix())
        return paths

    @classmethod
    def find_duplicate_paths(cls, records_or_paths: Iterable[Any]) -> list[str]:
        counts = Counter(cls._paths(records_or_paths))
        return sorted(path for path, count in counts.items() if count > 1)

    @classmethod
    def find_legacy_paths(cls, records_or_paths: Iterable[Any]) -> list[str]:
        legacy: list[str] = []
        for path in cls._paths(records_or_paths):
            parts = Path(path).parts
            if len(parts) == 3 and parts[0] == "rule" and parts[1] not in {"china", "category", "group", "aggregate", "unmapped"}:
                if parts[2] == f"{parts[1]}.yaml":
                    legacy.append(path)
            elif len(parts) == 4 and parts[0] == "generated" and parts[2] not in {"china", "categories", "_promotion"}:
                if Path(parts[3]).stem == parts[2]:
                    legacy.append(path)
        return sorted(set(legacy))

    @classmethod
    def validate_paths(cls, records_or_paths: Iterable[Any]) -> dict[str, Any]:
        paths = cls._paths(records_or_paths)
        duplicates = cls.find_duplicate_paths(paths)
        legacy = cls.find_legacy_paths(paths)
        if duplicates:
            raise RuntimeError("duplicate distribution paths: " + ", ".join(duplicates))
        if legacy:
            raise RuntimeError("legacy distribution paths: " + ", ".join(legacy))
        return {
            "duplicate_paths": 0,
            "legacy_layout": 0,
            "checked_paths": len(paths),
            "layout_schema": cls.LAYOUT_SCHEMA,
        }


__all__ = ["LAYOUT_SCHEMA", "HUMAN_LAYOUT", "GENERATED_LAYOUT", "EntityPathResolver"]
