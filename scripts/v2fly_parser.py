# DEPRECATED: V2Fly parsing is owned by src.engine.ingest.formats.v2fly.
# This entrypoint intentionally fails closed to prevent production reintroduction of the old parser path.
raise SystemExit("scripts/v2fly_parser.py is retired; use src.engine.ingest.formats.v2fly")
