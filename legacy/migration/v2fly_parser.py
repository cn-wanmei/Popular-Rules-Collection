"""Migration compatibility import for the retired V2Fly parser path."""
from src.engine.ingest.formats.v2fly import expand_file, looks_like, parse_line

__all__ = ["parse_line", "expand_file", "looks_like"]
