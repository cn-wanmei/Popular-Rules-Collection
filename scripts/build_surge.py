#!/usr/bin/env python3
"""Compatibility shim — implementation: src/adapters/surge/build.py"""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.adapters.surge.build import main  # noqa: E402
if __name__ == "__main__":
    raise SystemExit(main())
