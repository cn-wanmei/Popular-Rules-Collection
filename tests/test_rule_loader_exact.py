from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from rule_loader import load_service_rules  # noqa: E402


def test_loader_openai():
    buckets = load_service_rules("openai")
    assert buckets
    b = buckets[0]
    assert b["id"] == "openai"
    total = sum(len(b[k]) for k in ("domain", "domain_suffix", "domain_keyword", "domain_regex", "ip_cidr", "ip_cidr6"))
    assert total > 0
