from __future__ import annotations

from pathlib import Path

from scripts.phase_j_p0_service_evidence import (
    canonicalize,
    find_source,
    parse_rules,
    positive_and_negative,
    runtime_overlap,
    service_overlap_audit,
    service_token_match,
)


def test_service_token_match_accepts_exact_service_filename() -> None:
    assert service_token_match("geosite_deepseek.list", "deepseek")
    assert service_token_match("Clash_TestFlight.yaml", "testflight")
    assert not service_token_match("Clash_Apple.yaml", "appledev")


def test_parse_rules_and_canonical_identity_are_deterministic() -> None:
    rules = parse_rules("+.example.com\napi.example.com\nIP-CIDR,192.0.2.0/24\n")
    canonical = canonicalize(rules)
    assert [r["type"] for r in canonical] == ["DOMAIN-SUFFIX", "DOMAIN-SUFFIX", "IP-CIDR"]
    assert canonical[0]["identity_key"] == "domain-suffix|example.com"
    assert len(canonical[0]["rule_id"]) == 64


def test_keyword_rule_requires_explicit_review() -> None:
    semantic = __import__("scripts.phase_j_p0_service_evidence", fromlist=["semantic_audit"]).semantic_audit(
        canonicalize([{ "type": "HOST-KEYWORD", "value": "testflight" }])
    )
    assert semantic["status"] == "blocked"
    assert "keyword_rule_requires_explicit_acceptance" in semantic["reasons"]


def test_cidr_probe_has_inside_and_outside_examples() -> None:
    positive, negative = positive_and_negative({"type": "IP-CIDR", "value": "192.0.2.0/24"})
    assert positive == "192.0.2.1"
    assert negative == "192.0.3.0"

def test_unrelated_services_remain_pass_when_overlap_exists_elsewhere() -> None:
    def rule_matches(rule, host):
        return rule["value"] == host

    rows = {
        "service-a": {
            "semantic": {"probes": [{"positive_match": True, "positive": "shared.example"}]},
            "canonical_rules": [],
        },
        "service-b": {
            "semantic": {"probes": []},
            "canonical_rules": [{"type": "HOST", "value": "shared.example", "rule_id": "b"}],
        },
        "service-c": {
            "semantic": {"probes": [{"positive_match": True, "positive": "isolated.example"}]},
            "canonical_rules": [{"type": "HOST", "value": "isolated.example", "rule_id": "c"}],
        },
    }

    overlap = runtime_overlap(rows, rule_matches)
    assert overlap["status"] == "blocked"
    assert service_overlap_audit("service-a", overlap)["status"] == "blocked"
    assert service_overlap_audit("service-b", overlap)["status"] == "blocked"
    assert service_overlap_audit("service-c", overlap)["status"] == "pass"


def test_find_source_prefers_rule_list_within_same_hint(tmp_path: Path) -> None:
    backup = tmp_path / "backup" / "2026-09-20" / "sources" / "blackmatrix7"
    backup.mkdir(parents=True)
    (backup / "Clash_AppStore.yaml").write_text(
        "payload:\n  - DOMAIN,apps.apple.com\n", encoding="utf-8"
    )
    (backup / "QuantumultX_AppStore.list").write_text(
        "HOST,apps.apple.com\n", encoding="utf-8"
    )
    found = find_source(tmp_path, "appstore", ["blackmatrix7"])
    assert found is not None
    assert found.name == "QuantumultX_AppStore.list"


def test_find_source_honors_verified_provider_hint_order(tmp_path: Path) -> None:
    blackmatrix = tmp_path / "backup" / "2026-09-20" / "sources" / "blackmatrix7"
    firefly = tmp_path / "backup" / "2026-09-20" / "sources" / "lm-firefly"
    blackmatrix.mkdir(parents=True)
    firefly.mkdir(parents=True)
    (blackmatrix / "Clash_AppleDev.yaml").write_text(
        "payload:\n  - DOMAIN,developer.apple.com\n", encoding="utf-8"
    )
    (firefly / "LM_Firefly_AppleDev.list").write_text(
        "DOMAIN-SUFFIX,developer.apple.com\n", encoding="utf-8"
    )
    found = find_source(tmp_path, "appledev", ["lm-firefly", "blackmatrix7"])
    assert found is not None
    assert found.name == "LM_Firefly_AppleDev.list"


def test_publish_provenance_contract_separates_workflow_and_engine_ids() -> None:
    root = Path(__file__).resolve().parents[2]
    build = (root / ".github" / "workflows" / "build.yml").read_text(encoding="utf-8")
    publish = (root / ".github" / "workflows" / "publish.yml").read_text(encoding="utf-8")

    assert 'github.run_id' in build
    assert 'github.sha' in build
    assert "release-candidate/build-run-id.txt" in build
    assert "release-candidate/build-head-sha.txt" in build

    assert "release-candidate/build-run-id.txt" in publish
    assert "release-candidate/build-head-sha.txt" in publish
    assert 'ENGINE_RUN_ID="$(cat release-candidate/run-id.txt)"' in publish
    assert 'build-run-id.txt)" = "${EXPECTED_BUILD_RUN_ID}"' in publish
    assert 'build-head-sha.txt)" = "${EXPECTED_BUILD_SHA}"' in publish
    assert 'release-candidate/run-id.txt)" = "${EXPECTED_BUILD_RUN_ID}"' not in publish
