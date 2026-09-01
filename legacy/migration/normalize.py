"""Migration-only compatibility entry point for retired normalize semantics.

No production workflow imports this module. V3 production normalization is
performed by ``src.engine.ingest.normalizer`` and the canonical store.
"""
from src.engine.ingest.normalizer import normalize_record

__all__ = ["normalize_record"]
