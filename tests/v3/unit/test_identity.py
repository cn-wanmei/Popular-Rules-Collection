from src.v3.core.models.rule import identity_key, normalize_value

def test_domain_suffix_norm():
    assert normalize_value("domain_suffix", "Gmail.COM.") == "gmail.com"
    assert identity_key("domain_suffix", "Gmail.COM.") == "domain_suffix|gmail.com"

def test_ip_cidr():
    assert identity_key("ip_cidr", "1.2.3.0/24") == "ip_cidr|1.2.3.0/24"
