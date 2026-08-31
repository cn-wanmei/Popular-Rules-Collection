#!/usr/bin/env python3
"""Shim — use src.adapters._common.rule_loader"""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.adapters._common.rule_loader import *  # noqa: F401,F403
from src.adapters._common.rule_loader import load_service_rules  # noqa: F401
