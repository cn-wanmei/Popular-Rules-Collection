import json
import subprocess
import sys
from pathlib import Path

import scripts.build_network_bundle as bundle


def test_network_variants(tmp_path):
    bundle._write_network_variants(
        "network",
        "mixed",
        ["10.0.0.0/8", "dns.example.com"],
        tmp_path,
    )
    assert (tmp_path / "network/mixed.txt").read_text() == "10.0.0.0/8\ndns.example.com\n"
    mihomo = (tmp_path / "network/mixed_mihomo.list").read_text().splitlines()
    assert mihomo == ["IP-CIDR,10.0.0.0/8", "DOMAIN-SUFFIX,dns.example.com"]
    assert (tmp_path / "network/mixed_singbox_cidrs.txt").read_text().strip() == "10.0.0.0/8"


def test_generated_manifest_includes_client_and_network(tmp_path):
    generated = tmp_path / "generated"
    (generated / "mihomo/tencent/taobao").mkdir(parents=True)
    (generated / "network").mkdir()
    (generated / "mihomo/tencent/taobao/rules.list").write_text(
        "DOMAIN-SUFFIX,taobao.com\n",
        encoding="utf-8",
    )
    (generated / "network/lan.txt").write_text("10.0.0.0/8\n", encoding="utf-8")

    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            "scripts/generated_manifest.py",
            "--root",
            str(generated),
            "--output",
            str(generated / "manifest.json"),
            "--date",
            "2026-09-22",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "network" in result.stdout
    data = json.loads((generated / "manifest.json").read_text(encoding="utf-8"))
    assert "mihomo" in data["client_rule_directories"]
    assert "network" in data["network_dataset_directories"]
    assert data["file_count"] == 2


def test_geoip_has_one_stable_publication_scope_and_cleans_legacy_country(tmp_path):
    legacy = tmp_path / "country"
    legacy.mkdir()
    (legacy / "cn.txt").write_text("1.0.0.0/8\n", encoding="utf-8")
    bundle._clean_network_outputs(tmp_path)
    assert not legacy.exists()
    bundle._write_network_variants("geoip", "cn", ["1.0.0.0/8"], tmp_path)
    assert (tmp_path / "geoip/cn.txt").is_file()
    assert (tmp_path / "geoip/cn_mihomo.list").is_file()
    assert not (tmp_path / "country/cn.txt").exists()
