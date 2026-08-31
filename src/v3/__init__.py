"""Popular-Rules V3 — greenfield runtime.

Hard rule: V3 must NOT import from scripts/ or V2 runtime modules.
V2 is baseline/oracle only; data enters V3 via legacy_import from frozen snapshots.
"""
__version__ = "3.0.0-dev"
