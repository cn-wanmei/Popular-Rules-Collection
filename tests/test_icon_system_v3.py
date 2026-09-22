import unittest
from pathlib import Path
import yaml
from scripts.icon_system_v3 import CLIENTS,STYLES,color,semantic,render,slug,entries,yload,CFG,MAN
class IconSystemV3Tests(unittest.TestCase):
    def test_fixed_contracts(self):
        self.assertEqual(len(STYLES),7); self.assertEqual(len(CLIENTS),7)
    def test_color_priority(self):
        self.assertEqual(color({"brand":{"display_color":"#112233"},"source":{"color":"#AABBCC"}}),"#112233")
    def test_semantic_icon(self):
        self.assertIn(">DR</text>",semantic("Direct","DR"))
    def test_production_source_overrides(self):
        cfg = yaml.safe_load((Path(__file__).resolve().parents[1] / "config" / "icon_v3.yaml").read_text(encoding="utf-8"))
        overrides = cfg.get("source_overrides") or {}
        for sid in ("1688", "cainiao", "dingding", "qqmail", "qqmusic", "taobao"):
            row = overrides.get(sid) or {}
            self.assertEqual(row.get("status"), "verified")
            self.assertTrue((row.get("license") or {}).get("reviewed") is True)
            svg_rel = (row.get("files") or {}).get("svg")
            self.assertTrue(svg_rel)
            self.assertTrue((Path(__file__).resolve().parents[1] / "assets" / "icons" / svg_rel).is_file())

    def test_v3_entries_include_all_audited_production_overrides(self):
        man = yload(MAN)
        cfg = yload(CFG)
        by_id = {row["service_id"]: row for row in entries(man, cfg)}
        for sid in ("1688", "cainiao", "dingding", "qqmail", "qqmusic", "taobao"):
            self.assertIn(sid, by_id)
            self.assertEqual(by_id[sid]["role"], "service")

    def test_alias_slug_stability(self):
        self.assertEqual(slug("taobao"),"taobao")
        self.assertEqual(slug("client-policy.mihomo"),"client-policy.mihomo")

    def test_all_styles_render(self):
        base='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M2 2h20v20H2z"/></svg>'
        for style in STYLES:
            self.assertIn('viewBox="0 0 128 128"',render(base,"Demo",style,"#FF0000"))
