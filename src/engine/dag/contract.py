"""Stable stage identity used by future resume/cache planning."""
from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stage_fingerprint(
    name: str,
    contract_version: str,
    input_digest: str,
    config: dict[str, Any] | None = None,
) -> str:
    payload = {
        "stage": name,
        "contract_version": contract_version,
        "input_digest": input_digest,
        "config": config or {},
    }
    return hashlib.sha256(canonical_json(payload)).hexdigest()
