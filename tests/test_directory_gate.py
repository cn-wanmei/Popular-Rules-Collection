from pathlib import Path

from scripts.directory_gate import validate


def test_directory_policy_passes_bootstrap_tree() -> None:
    root = Path(__file__).resolve().parents[1]
    report = validate(root)
    assert report["pass"], report["errors"]
    assert "alibaba" in report["china_excluded_independent_providers"]
    assert "tencent" in report["china_excluded_independent_providers"]
    assert "baidu" in report["china_excluded_independent_providers"]


def test_directory_policy_rejects_flat_canonical_rule(tmp_path: Path) -> None:
    root = tmp_path
    policy = root / "config" / "service_model"
    policy.mkdir(parents=True)
    policy.write_text("", encoding="utf-8")
