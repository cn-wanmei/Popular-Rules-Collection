from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Decision:
    action: str
    layer: str = "service"
    precedence: int = 800
    reason: str = ""
