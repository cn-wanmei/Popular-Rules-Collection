"""Entity graph kinds."""
from __future__ import annotations

from enum import Enum


class EntityKind(str, Enum):
    PROVIDER = "provider"
    SERVICE = "service"
    GROUP = "group"
    PRODUCT = "product"
    PLATFORM = "platform"


class ViewKind(str, Enum):
    AGGREGATE = "aggregate"
    EXCLUSIVE = "exclusive"
    EFFECTIVE = "effective"


class Scope(str, Enum):
    ECOSYSTEM = "ecosystem"
    PRODUCT_FAMILY = "product_family"
    PRODUCT = "product"
    PROVIDER_CORE = "provider_core"
    SHARED_INFRASTRUCTURE = "shared_infrastructure"
