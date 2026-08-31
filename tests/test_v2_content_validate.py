from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from source_content_validate import validate_file, validate_bytes  # noqa: E402


def test_html_rejected():
    p = ROOT / "tests" / "fixtures" / "negative" / "access_denied.html"
    assert "html_document" in validate_file(p)


def test_empty_rejected():
    assert "empty" in validate_bytes(b"")


def test_ok_text():
    assert validate_bytes(b"DOMAIN-SUFFIX,example.com\n") == []
