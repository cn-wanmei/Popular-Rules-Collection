from scripts.phase_j_p0_service_evidence import find_source, runtime_overlap, service_overlap_audit


def test_unrelated_services_remain_pass_when_overlap_exists_elsewhere():
    def rule_matches(rule, host):
        return rule['value'] == host

    rows = {
        'service-a': {
            'semantic': {'probes': [{'positive_match': True, 'positive': 'shared.example'}]},
            'canonical_rules': [],
        },
        'service-b': {
            'semantic': {'probes': []},
            'canonical_rules': [{'type': 'HOST', 'value': 'shared.example', 'rule_id': 'b'}],
        },
        'service-c': {
            'semantic': {'probes': [{'positive_match': True, 'positive': 'isolated.example'}]},
            'canonical_rules': [{'type': 'HOST', 'value': 'isolated.example', 'rule_id': 'c'}],
        },
    }

    overlap = runtime_overlap(rows, rule_matches)
    assert overlap['status'] == 'blocked'
    collisions = overlap['runtime_collisions']
    assert collisions == [
        {
            'service': 'service-a',
            'probe': 'shared.example',
            'other_service': 'service-b',
            'rule_id': 'b',
        },
    ]

    assert service_overlap_audit('service-a', overlap)['status'] == 'blocked'
    assert service_overlap_audit('service-b', overlap)['status'] == 'blocked'
    assert service_overlap_audit('service-c', overlap)['status'] == 'pass'
    assert service_overlap_audit('service-c', overlap)['collisions'] == []


def test_find_source_prefers_rule_list_within_same_hint(tmp_path: Path):
    backup = tmp_path / 'backup' / '2026-09-20' / 'sources' / 'blackmatrix7'
    backup.mkdir(parents=True)
    (backup / 'Clash_AppStore.yaml').write_text('payload:\n  - DOMAIN,apps.apple.com\n', encoding='utf-8')
    (backup / 'QuantumultX_AppStore.list').write_text('HOST,apps.apple.com\n', encoding='utf-8')
    found = find_source(tmp_path, 'appstore', ['blackmatrix7'])
    assert found is not None
    assert found.name == 'QuantumultX_AppStore.list'


def test_find_source_honors_verified_provider_hint_order(tmp_path: Path):
    blackmatrix = tmp_path / 'backup' / '2026-09-20' / 'sources' / 'blackmatrix7'
    firefly = tmp_path / 'backup' / '2026-09-20' / 'sources' / 'lm-firefly'
    blackmatrix.mkdir(parents=True)
    firefly.mkdir(parents=True)
    (blackmatrix / 'Clash_AppleDev.yaml').write_text('payload:\n  - DOMAIN,developer.apple.com\n', encoding='utf-8')
    (firefly / 'LM_Firefly_AppleDev.list').write_text('DOMAIN-SUFFIX,developer.apple.com\n', encoding='utf-8')
    found = find_source(tmp_path, 'appledev', ['lm-firefly', 'blackmatrix7'])
    assert found is not None
    assert found.name == 'LM_Firefly_AppleDev.list'