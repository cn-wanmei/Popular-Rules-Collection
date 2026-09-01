"""Deprecated compatibility shim; V3 owns V2Fly format parsing.

Production code must import from ``src.engine.ingest.formats.v2fly``.
This module remains only for non-production legacy callers during migration.
"""
from src.engine.ingest.formats.v2fly import expand_file as expand_v2fly_file
from src.engine.ingest.formats.v2fly import looks_like as looks_like_v2fly
from src.engine.ingest.formats.v2fly import parse_line as parse_v2fly_line

__all__ = ["parse_v2fly_line", "expand_v2fly_file", "looks_like_v2fly"]
