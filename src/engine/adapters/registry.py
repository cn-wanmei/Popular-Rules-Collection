"""Single SSOT for client list + expected extensions (P0-6)."""
from __future__ import annotations

from typing import Callable

# extension per client — must match real native format
CLIENTS = {
    "mihomo": {"ext": ".yaml", "format": "yaml"},
    "singbox": {"ext": ".json", "format": "json"},
    "surge": {"ext": ".list", "format": "list"},
    "shadowrocket": {"ext": ".list", "format": "list"},
    "quantumultx": {"ext": ".list", "format": "list"},
    "egern": {"ext": ".yaml", "format": "yaml"},
    "loon": {"ext": ".list", "format": "list"},
}


def get_adapter(client: str) -> Callable:
    if client not in CLIENTS:
        raise KeyError(f"Unknown client: {client}")
    # lazy import to keep modules independent
    mod = __import__(f"src.engine.adapters.{client}", fromlist=["render"])
    return mod.render
