"""Entity graph nodes."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Provider:
    id: str
    display_name: str = ""
    meta: dict[str, Any] = field(default_factory=dict)

@dataclass
class Service:
    id: str
    provider: str | None = None
    display_name: str = ""
    body_service_id: str | None = None
    meta: dict[str, Any] = field(default_factory=dict)

@dataclass
class Group:
    id: str
    members: list[str] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)

@dataclass
class AggregateView:
    id: str
    members: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)

@dataclass
class EntityGraph:
    providers: dict[str, Provider] = field(default_factory=dict)
    services: dict[str, Service] = field(default_factory=dict)
    groups: dict[str, Group] = field(default_factory=dict)
    aggregates: dict[str, AggregateView] = field(default_factory=dict)
    aliases: dict[str, str] = field(default_factory=dict)
