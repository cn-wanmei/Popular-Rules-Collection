#!/usr/bin/env python3
"""Regression tests for payment-brand icon semantic resolution."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from icon_resolver import resolve  # noqa: E402

EXPECTED = {
    "googlepay": "googlepay",
    "google-pay": "googlepay",
    "google_pay": "googlepay",
    "gpay": "googlepay",
    "applepay": "applepay",
    "apple-pay": "applepay",
    "apple_pay": "applepay",
    "apay": "applepay",
    "unionpay": "unionpay",
    "union-pay": "unionpay",
    "union_pay": "unionpay",
    "unionpayinternational": "unionpay",
}

for service_id, key in EXPECTED.items():
    result = resolve(service_id)
    assert result["ok"], f"{service_id}: resolver failed"
    assert result["semantic_override"], f"{service_id}: semantic override missing"
    assert result["variant_id"] == f"{key}-semantic", result
    assert result["path_svg"] == f"source/{key}.svg", result
    assert result["path_png_256"] == f"png/128/{key}.png", result
    assert (ROOT / "assets/icons" / result["path_svg"]).exists(), result
    assert (ROOT / "assets/icons" / result["path_png_256"]).exists(), result

# Generic Google/Apple IDs remain distinct; they must not be silently remapped.
assert resolve("google")["variant_id"] != "googlepay-semantic"
assert resolve("apple")["variant_id"] != "applepay-semantic"

print(f"[icon_payment_semantic_test] PASS ({len(EXPECTED)} payment aliases)")
