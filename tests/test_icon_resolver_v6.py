from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import scripts.icon_resolver_v6 as resolver


class IconResolverV6Tests(unittest.TestCase):
    def test_resolve_uses_manifest_path(self) -> None:
        manifest = {
            "release_id": "icon-2026.09.30.r14.1",
            "entries": [
                {
                    "service_id": "demo",
                    "variants": {
                        "source_original:256:png": {
                            "variant_hash": "abc123",
                            "path": "/v/abc123.png",
                        }
                    },
                }
            ],
        }
        self.assertEqual(
            resolver.resolve(manifest, "demo"),
            "https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Icon@dist/v/abc123.png",
        )

    def test_invalid_manifest_path_is_rejected(self) -> None:
        manifest = {
            "release_id": "icon-2026.09.30.r14.1",
            "entries": [
                {
                    "service_id": "demo",
                    "variants": {
                        "source_original:256:png": {
                            "variant_hash": "abc123",
                            "path": "/v/abc123.bin",
                        }
                    },
                }
            ],
        }
        with self.assertRaises(ValueError):
            resolver.resolve(manifest, "demo")

    def test_offline_config_release_mismatch_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = root / "config.yaml"
            manifest = root / "manifest.json"
            config.write_text(
                "provider: v6\n"
                "v6:\n"
                "  release_id: expected\n"
                "  fallback_to_v5: false\n",
                encoding="utf-8",
            )
            manifest.write_text(
                json.dumps({"release_id": "actual", "entries": []}),
                encoding="utf-8",
            )
            import subprocess
            import sys
            proc = subprocess.run(
                [
                    sys.executable,
                    "scripts/icon_resolver_v6.py",
                    "--config",
                    str(config),
                    "--manifest-file",
                    str(manifest),
                    "--service",
                    "demo",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 4)


if __name__ == "__main__":
    unittest.main()
