from __future__ import annotations

import hashlib
import json
from typing import Any


SCHEMA = "collection_manifest_v2"


def canonical_payload(manifest: dict[str, Any]) -> bytes:
    payload = {k: v for k, v in manifest.items() if k not in {"manifest_sha256", "created_at"}}
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(manifest: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_payload(manifest)).hexdigest()


def seal(manifest: dict[str, Any]) -> dict[str, Any]:
    out = dict(manifest)
    out["schema"] = SCHEMA
    out["manifest_sha256"] = digest(out)
    return out


def verify(manifest: dict[str, Any]) -> bool:
    expected = manifest.get("manifest_sha256")
    return isinstance(expected, str) and expected == digest(manifest)
