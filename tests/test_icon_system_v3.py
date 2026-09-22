import unittest
from scripts.icon_system_v3 import CLIENTS,STYLES,color,semantic,render,slug
class IconSystemV3Tests(unittest.TestCase):
    def test_fixed_contracts(self):
        self.assertEqual(len(STYLES),7); self.assertEqual(len(CLIENTS),7)
    def test_color_priority(self):
        self.assertEqual(color({"brand":{"display_color":"#112233"},"source":{"color":"#AABBCC"}}),"#112233")
    def test_semantic_icon(self):
        self.assertIn(">DR</text>",semantic("Direct","DR"))
    def test_alias_slug_stability(self):
        self.assertEqual(slug("taobao"),"taobao")
        self.assertEqual(slug("client-policy.mihomo"),"client-policy.mihomo")

    def test_all_styles_render(self):
        base='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M2 2h20v20H2z"/></svg>'
        for style in STYLES:
            self.assertIn('viewBox="0 0 128 128"',render(base,"Demo",style,"#FF0000"))
