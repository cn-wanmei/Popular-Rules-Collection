from src.engine.v1.dedup import normalize_record
from src.engine.v1.legacy_regression import load_assets_from_records


def test_ipv6_cidr_alias_uses_canonical_asset_type() -> None:
    normalized = normalize_record({
        "service": "stun",
        "type": "ip_cidr6",
        "value": "2001:4060:1:1005::10:32/128",
    })
    assert normalized["type"] == "ip_cidr"


def test_legacy_regression_does_not_report_ipv6_alias_as_removed() -> None:
    legacy = load_assets_from_records(
        [{
            "service": "stun",
            "type": "ip_cidr6",
            "value": "2001:4060:1:1005::10:32/128",
        }],
        "legacy",
    )
    v1 = load_assets_from_records(
        [{
            "service": "stun",
            "type": "ip_cidr",
            "value": "2001:4060:1:1005::10:32/128",
        }],
        "v1",
    )
    from src.engine.v1.legacy_regression import compare_legacy_to_v1
    report = compare_legacy_to_v1(legacy, v1)
    assert report.unexplained_removed == []
    assert report.counts.get("Removed", 0) == 0
