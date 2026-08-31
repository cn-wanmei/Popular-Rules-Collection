#!/usr/bin/env python3
"""Shim → src.canonical.build_store"""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.canonical.build_store import main
if __name__ == "__main__":
    raise SystemExit(main())
