import json
import tempfile
import unittest
from pathlib import Path

from scripts.icon_system_v5 import (
    ROOT,
    VARIANTS,
    RENDERERS,
    RENDERER_VERSION,
    discover_services_from_ir,
    discover_services_from_rule_index,
    render_pngs,
    sha256,
    validate_source,
    quality_from_px,
    QUALITY_HIGH,
    QUALITY_MEDIUM,
    QUALITY_ACCEPTABLE,
    QUALITY_LOW,
    inspect_source_bytes,
)
from scripts.icon_v5_renderers.common import svg_data_url


class IconSystemV5Tests(unittest.TestCase):
    def test_variant_contract_is_exactly_eight_layers(self):
        self.assertEqual(len(VARIANTS), 8)
        self.assertEqual(set(VARIANTS[1:]), set(RENDERERS))

    def test_rule_index_bootstrap_discovers_current_services(self):
        rows = discover_services_from_rule_index(ROOT / "rule" / "_index.yaml")
        self.assertGreaterEqual(len(rows), 146)
        self.assertIn("zhihu", {row["service_id"] for row in rows})

    def test_semantic_ir_v2_shape_is_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ir.json"
            path.write_text(
                json.dumps(
                    {
                        "schema": "semantic_ir_v2",
                        "entities": {"services": ["demo"]},
                        "views": {
                            "services": {
                                "demo": {"display_name": "Demo", "provider": "demo"}
                            }
                        },
                        "memberships": {"demo": ["r1"]},
                        "rules": [
                            {
                                "id": "r1",
                                "type": "DOMAIN_SUFFIX",
                                "value": "demo.example.com",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            rows = discover_services_from_ir(path)
            self.assertEqual(rows[0]["service_id"], "demo")
            self.assertEqual(rows[0]["display_name"], "Demo")
            # domains are optional for icon identity; discovery only requires service_id

    def test_renderer_version_is_v5(self):
        self.assertEqual(RENDERER_VERSION, "prc-icon-renderer-v5.1.0")

    def test_quality_tiers(self):
        self.assertEqual(quality_from_px(16), QUALITY_LOW)
        self.assertEqual(quality_from_px(95), QUALITY_LOW)
        self.assertEqual(quality_from_px(96), QUALITY_ACCEPTABLE)
        self.assertEqual(quality_from_px(128), QUALITY_MEDIUM)
        self.assertEqual(quality_from_px(256), QUALITY_HIGH)

    def test_svg_inspect_is_vector_high(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z"/></svg>'
        info = inspect_source_bytes(svg, "image/svg+xml", "svg")
        self.assertTrue(info["is_vector"])
        self.assertGreaterEqual(info["source_px"], 24)

    def test_source_svg_security_gate(self):
        safe = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z"/></svg>'
        self.assertEqual(validate_source(safe, "image/svg+xml", "https://example.com/icon.svg"), "svg")
        unsafe = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><script>alert(1)</script></svg>'
        with self.assertRaises(ValueError):
            validate_source(unsafe, "image/svg+xml", "https://example.com/icon.svg")

    def test_seven_renderer_modules_are_distinct(self):
        href = svg_data_url(
            b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/></svg>',
            "svg",
        )
        rendered = {name: fn(href, "Demo") for name, fn in RENDERERS.items()}
        self.assertEqual(len(rendered), 7)
        self.assertEqual(len({sha256(v) for v in rendered.values()}), 7)
        for svg in rendered.values():
            self.assertIn("<image", svg)

    def test_png_raster_contract(self):
        href = svg_data_url(
            b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/></svg>',
            "svg",
        )
        svg = RENDERERS["minimalist"](href, "Demo")
        with tempfile.TemporaryDirectory() as tmp:
            paths = render_pngs(svg, Path(tmp), "demo", "minimalist", [24, 64])
            for size in (24, 64):
                self.assertGreater((Path(tmp) / paths[str(size)]).stat().st_size, 100)


if __name__ == "__main__":
    unittest.main()
