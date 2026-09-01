"""Source Snapshot — immutable input boundary for every run.
Must be created BEFORE any Canonical / Hierarchy / IR / Adapter work.
"""
from .engine import create_source_snapshot, load_snapshot_manifest

__all__ = ["create_source_snapshot", "load_snapshot_manifest"]
