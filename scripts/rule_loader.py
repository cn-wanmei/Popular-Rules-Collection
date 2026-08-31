#!/usr/bin/env python3
"""Compatibility shim — implementation: src.adapters._common.rule_loader

Patch targets for tests: src.adapters._common.rule_loader.SERVICES / DOMAINS / IPS
(not this shim module — load_service_rules resolves globals in the impl module).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.adapters._common import rule_loader as _impl  # noqa: E402
from src.adapters._common.rule_loader import (  # noqa: E402,F401
    TYPED_KEYS,
    load_service_rules,
)

ROOT = _impl.ROOT
SERVICES = _impl.SERVICES
DOMAINS = _impl.DOMAINS
IPS = _impl.IPS
