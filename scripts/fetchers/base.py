from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any


@dataclass
class FetchResult:
    ok: bool
    source_id: str
    path: str
    name: str
    url: str
    content: bytes | None = None
    sha256: str | None = None
    size: int = 0
    error: str | None = None
    status_code: int | None = None
    not_modified: bool = False
    headers: dict[str, str] = field(default_factory=dict)

    def compute_hash(self) -> None:
        if self.content is not None:
            self.sha256 = hashlib.sha256(self.content).hexdigest()
            self.size = len(self.content)


class BaseFetcher:
    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg

    @staticmethod
    def request_headers(entry: dict[str, Any]) -> dict[str, str]:
        headers = entry.get("headers") or {}
        return {str(k): str(v) for k, v in headers.items()}

    def fetch_one(self, entry: dict[str, Any]) -> FetchResult:
        raise NotImplementedError

    def fetch_all(self, entries: list[dict[str, Any]], source_id: str) -> list[FetchResult]:
        results = []
        for e in entries:
            r = self.fetch_one(e)
            r.source_id = source_id
            results.append(r)
        return results
