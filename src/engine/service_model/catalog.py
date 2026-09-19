"""Phase 2 — unified V1 Service Model facade.

The facade exposes one deterministic, read-only Service Model API over the
existing V1 rule index. It does not create a second source of truth.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

from src.engine.ingest.v1_index import ServiceEntry, load_v1_index

SERVICE_MODEL_SCHEMA = "v1_service_model_v1"

@dataclass(frozen=True)
class ServiceModel:
    """Stable service identity and structural metadata."""
    id: str
    name: str
    service_type: str
    path: str
    categories: tuple[str, ...] = ()
    parent: str | None = None
    children: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
    clients: tuple[str, ...] = ()
    digest: str = ""

    @classmethod
    def from_entry(cls, entry: ServiceEntry) -> "ServiceModel":
        payload = {
            "id": entry.id,
            "name": entry.name,
            "service_type": entry.service_type,
            "path": entry.path,
            "categories": sorted(entry.categories, key=str.casefold),
            "parent": entry.parent,
            "children": sorted(entry.children, key=str.casefold),
            "sources": sorted(entry.sources, key=str.casefold),
            "clients": sorted(entry.clients, key=str.casefold),
        }
        digest = hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return cls(
            id=payload["id"],
            name=payload["name"],
            service_type=payload["service_type"],
            path=payload["path"],
            categories=tuple(payload["categories"]),
            parent=payload["parent"],
            children=tuple(payload["children"]),
            sources=tuple(payload["sources"]),
            clients=tuple(payload["clients"]),
            digest=digest,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "service_type": self.service_type,
            "path": self.path,
            "categories": list(self.categories),
            "parent": self.parent,
            "children": list(self.children),
            "sources": list(self.sources),
            "clients": list(self.clients),
            "digest": self.digest,
        }

@dataclass
class ServiceCatalog:
    """Deterministic collection of the V1 Service Model."""
    models: tuple[ServiceModel, ...] = ()
    errors: list[str] = field(default_factory=list)

    @classmethod
    def from_rule_root(cls, rule_root: Path) -> "ServiceCatalog":
        index = load_v1_index(Path(rule_root))
        errors = [
            str(item.get("error", item))
            for item in index.errors
            if isinstance(item, dict)
        ]
        models = tuple(ServiceModel.from_entry(entry) for entry in index.entries)
        by_id = {model.id.casefold(): model for model in models}
        if len(by_id) != len(models):
            errors.append("duplicate service identity detected")
        valid_types = {"service", "aggregate"}
        for model in models:
            if model.service_type not in valid_types:
                errors.append(f"invalid service_type for {model.id}: {model.service_type!r}")
            if model.parent and model.parent.casefold() not in by_id:
                errors.append(f"dangling parent for {model.id}: {model.parent!r}")
            for child in model.children:
                if child.casefold() not in by_id:
                    errors.append(f"dangling child for {model.id}: {child!r}")
        models = tuple(sorted(models, key=lambda item: item.id.casefold()))
        return cls(models=models, errors=sorted(set(errors)))

    def get(self, service_id: str) -> ServiceModel:
        wanted = str(service_id).strip().casefold()
        for model in self.models:
            if model.id.casefold() == wanted:
                return model
        raise KeyError(service_id)

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(model.id for model in self.models)

    @property
    def services(self) -> tuple[ServiceModel, ...]:
        return tuple(model for model in self.models if model.service_type == "service")

    @property
    def aggregates(self) -> tuple[ServiceModel, ...]:
        return tuple(model for model in self.models if model.service_type == "aggregate")

    @property
    def fingerprint(self) -> str:
        payload = [model.to_dict() for model in self.models]
        return hashlib.sha256(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    def manifest(self) -> dict[str, object]:
        return {
            "schema": SERVICE_MODEL_SCHEMA,
            "service_count": len(self.services),
            "aggregate_count": len(self.aggregates),
            "entry_count": len(self.models),
            "fingerprint": self.fingerprint,
            "errors": list(self.errors),
            "source": "rule/_index.yaml",
        }
