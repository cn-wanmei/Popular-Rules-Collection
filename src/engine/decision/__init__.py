"""Decision SSOT — deterministic routing decision per rule + view + profile."""
from .engine import decide, decide_batch

__all__ = ["decide", "decide_batch"]
