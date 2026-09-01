"""Pipeline — hard-ordered stages. Quarantine & Snapshot before Canonical."""
from .run import run_pipeline, STAGES

__all__ = ["run_pipeline", "STAGES"]
