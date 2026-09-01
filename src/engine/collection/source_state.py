from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FetchStateStore:
    """Persistent per-source response metadata used for conditional requests."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self._data: dict[str, Any] = {}
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    self._data = loaded
            except (OSError, json.JSONDecodeError):
                self._data = {}

    def get(self, key: str) -> dict[str, Any]:
        value = self._data.get(key, {})
        return value if isinstance(value, dict) else {}

    def put(self, key: str, **values: Any) -> None:
        current = self.get(key).copy()
        current.update({k: v for k, v in values.items() if v is not None})
        self._data[key] = current

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name(f".{self.path.name}.tmp")
        tmp.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        tmp.replace(self.path)
