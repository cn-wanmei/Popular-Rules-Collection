"""Native client adapters — one module per client (P0-6)."""
from .registry import CLIENTS, get_adapter

__all__ = ["CLIENTS", "get_adapter"]
