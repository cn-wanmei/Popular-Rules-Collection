from pathlib import Path

import yaml

from src.engine.service_model.catalog import SERVICE_MODEL_SCHEMA, ServiceCatalog

def _write_fixture(root: Path) -> Path:
    rule_root = root / "rule"
    service_root = rule_root / "Example"
    child_root = service_root / "Child"
    child_root.mkdir(parents=True)
    (rule_root / "_index.yaml").write_text(
        yaml.safe_dump(
            {
                "categories": {
                    "example": {
                        "display_name": "Example",
                        "rules": [
                            {"id": "Example", "name": "Example", "path": "rule/Example", "service_type": "aggregate", "domains": 1, "ips": 0},
                            {"id": "Example/Child", "name": "Child", "path": "rule/Example/Child", "service_type": "service", "domains": 1, "ips": 0},
                        ],
                    }
                }
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    (service_root / "metadata.yaml").write_text(
        yaml.safe_dump({"name": "Example", "children": ["Example/Child"], "clients": ["mihomo"]}, sort_keys=False),
        encoding="utf-8",
    )
    (child_root / "metadata.yaml").write_text(
        yaml.safe_dump({"name": "Child", "parent": "Example", "categories": ["example"]}, sort_keys=False),
        encoding="utf-8",
    )
    (child_root / "Child.list").write_text("DOMAIN-SUFFIX,example.com\n", encoding="utf-8")
    return rule_root

def test_service_catalog_is_single_deterministic_model(tmp_path: Path) -> None:
    catalog = ServiceCatalog.from_rule_root(_write_fixture(tmp_path))
    assert catalog.errors == []
    assert catalog.ids == ("Example", "Example/Child")
    assert catalog.get("example/child").parent == "Example"
    assert catalog.manifest()["schema"] == SERVICE_MODEL_SCHEMA
    assert len(catalog.services) == 1
    assert len(catalog.aggregates) == 1

def test_service_catalog_fingerprint_is_stable(tmp_path: Path) -> None:
    rule_root = _write_fixture(tmp_path)
    first = ServiceCatalog.from_rule_root(rule_root)
    second = ServiceCatalog.from_rule_root(rule_root)
    assert first.fingerprint == second.fingerprint
    assert first.get("Example").digest == second.get("Example").digest
