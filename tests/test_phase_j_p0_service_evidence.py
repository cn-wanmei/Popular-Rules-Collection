from scripts.phase_j_p0_service_evidence import runtime_overlap, service_overlap_audit


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
