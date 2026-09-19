from pathlib import Path
import pytest
import yaml
from src.engine.runtime.v1_cutover import run_v1_cutover_gate
from src.engine.sot.resolver import SoTResolver
def _fixture(root: Path) -> Path:
    service_root = root / "rule" / "Example" / "Child"
    service_root.mkdir(parents=True)
    (root / "rule" / "_index.yaml").write_text(yaml.safe_dump({"categories": {"example": {"rules": [{
        "id": "Example/Child", "name": "Child", "path": "rule/Example/Child",
        "service_type": "service", "domains": 1, "ips": 0
    }]}}}, sort_keys=False), encoding="utf-8")
    (service_root / "metadata.yaml").write_text("name: Child\n", encoding="utf-8")
    (service_root / "Child.list").write_text("DOMAIN-SUFFIX,example.com\n", encoding="utf-8")
    return root
def test_relative_resolver_accepts_nested_v1_path(tmp_path: Path) -> None:
    result = SoTResolver(_fixture(tmp_path)).resolve_relative("rule/Example/Child")
    assert result.source == "v1_rule"
    assert result.found
def test_relative_resolver_rejects_escape(tmp_path: Path) -> None:
    resolver = SoTResolver(tmp_path)
    with pytest.raises(ValueError): resolver.resolve_relative("rule/../outside")
    with pytest.raises(ValueError): resolver.resolve_relative("../rule/Example")
def test_runtime_cutover_gate_passes_for_indexed_v1_service(tmp_path: Path) -> None:
    report = run_v1_cutover_gate(_fixture(tmp_path))
    assert report["all_pass"] is True
    assert report["resolved"] == ["Example/Child"]
