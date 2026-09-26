import tempfile
import unittest
from pathlib import Path

from scripts.icon_system_v5 import ROOT, VARIANTS, RENDERERS, RENDERER_VERSION, discover_services_from_rule_index, render_pngs, sha256, validate_source
from scripts.icon_v5_renderers.common import svg_data_url

class IconSystemV5Tests(unittest.TestCase):
    def test_variant_contract_is_exactly_eight_layers(self):
        self.assertEqual(len(VARIANTS), 8)
        self.assertEqual(set(VARIANTS[1:]), set(RENDERERS))

    def test_rule_index_bootstrap_discovers_current_services(self):
        rows=discover_services_from_rule_index(ROOT/'rule'/'_index.yaml')
        self.assertGreaterEqual(len(rows), 146)
        self.assertIn('zhihu',{row['service_id'] for row in rows})

    def test_renderer_version_is_v5(self):
        self.assertEqual(RENDERER_VERSION,'prc-icon-renderer-v5.0.0')

    def test_source_svg_security_gate(self):
        safe=b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z"/></svg>'
        self.assertEqual(validate_source(safe,'image/svg+xml','https://example.com/icon.svg'),'svg')
        unsafe=b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><script>alert(1)</script></svg>'
        with self.assertRaises(ValueError): validate_source(unsafe,'image/svg+xml','https://example.com/icon.svg')

    def test_seven_renderer_modules_are_distinct(self):
        href=svg_data_url(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/></svg>','svg')
        rendered={name:fn(href,'Demo') for name,fn in RENDERERS.items()}
        self.assertEqual(len(rendered),7)
        self.assertEqual(len({sha256(v) for v in rendered.values()}),7)
        for svg in rendered.values():
            self.assertIn('viewBox="0 0 512 512"',svg)
            self.assertIn('<image',svg)

    def test_png_raster_contract(self):
        href=svg_data_url(b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/></svg>','svg')
        svg=RENDERERS['minimalist'](href,'Demo')
        with tempfile.TemporaryDirectory() as tmp:
            paths=render_pngs(svg,Path(tmp),'demo','minimalist',[24,64])
            for size in (24,64):
                path=Path(tmp)/paths[str(size)]
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size,100)

if __name__=='__main__': unittest.main()