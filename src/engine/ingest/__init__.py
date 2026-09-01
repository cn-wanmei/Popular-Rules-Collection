"""Engine Ingest — pure Source Snapshot → normalized records.
No database/services, no V2 service model, no legacy_import.
"""
from .source_ingest import ingest_snapshot

__all__ = ["ingest_snapshot"]
