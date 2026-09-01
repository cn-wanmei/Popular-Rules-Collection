"""Quarantine — must run BEFORE Canonical / Hierarchy / IR / Adapters.
Invalid or suspicious records are isolated; they never enter production build.
"""
from .engine import run_quarantine

__all__ = ["run_quarantine"]
