# DEPRECATED: production normalization has moved to src/engine.ingest.
# This file intentionally fails closed so legacy callers cannot reintroduce the 2.X database pipeline.
raise SystemExit("scripts/normalize.py is retired; use python -m src.engine.cli all")
