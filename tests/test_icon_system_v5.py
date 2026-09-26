import unittest

from scripts.icon_system_v5 import (
    ROOT,
    VARIANTS,
    RENDERER_VERSION,
    discover_services,
    render_variant,
    sha256,
    validate_source,
)


class IconSystemV5Tests(unittest.TestCase):
    def test_variant_contract_is_exactly_eight_layers(self):
        self.assertEqual(len(VARIANTS), 8)

    def test_rule_index_bootstrap_discovers_146_services_on_current_mainline(self):
        rows = discover_services(ROOT / "rule" / "_index.yaml")
        self.assertEqual(len(rows), 146)
        self.assertIn("zhihu", {row["service_id"] for row in rows})

    def test_renderer_version_is_v5(self):
        self.assertEqual(RENDERER_VERSION, "prc-icon-renderer-v5.0.0")

    def test_source_svg_security_gate(self):
        safe = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z"/></svg>'
        self.assertEqual(validate_source(safe, "image/svg+xml", "https://example.com/icon.svg"), "svg")
        unsafe = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><script>alert(1)</script></svg>'
        with self.assertRaises(ValueError):
            validate_source(unsafe, "image/svg+xml", "https://example.com/icon.svg")

    def test_style_renderers_are_separate_outputs(self):
        base = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxIDIiPjwvc3ZnPg=="
        outputs = {style: render_variant(base, "Demo", style) for style in VARIANTS[1:]}
        self.assertEqual(len(outputs), 7)
        self.assertEqual(len({sha256(value) for value in outputs.values()}), 7)
        for svg in outputs.values():
            self.assertIn('viewBox="0 0 512 512"', svg)
            self.assertIn("<image", svg)


if __name__ == "__main__":
    unittest.main()
