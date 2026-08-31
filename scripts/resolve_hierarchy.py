#!/usr/bin/env python3
"""Shim → src.hierarchy.resolve_hierarchy"""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.hierarchy.resolve_hierarchy import main
if __name__ == "__main__":
    raise SystemExit(main())
