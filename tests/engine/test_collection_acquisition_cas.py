import json
from pathlib import Path

from src.engine.cas.store import digest_bytes, read_bytes
from src.engine.collection.acquisition_cas import load, store
from src.engine.collection.manifest import digest, seal, verify


def test_acquisition_cas_roundtrip(tmp_path: Path):
    data = b"DOMAIN-SUFFIX,example.com\n"
    d = store(data, tmp_path)
    assert d == digest_bytes(data)
    assert load(d, tmp_path) == data
    assert read_bytes(d, tmp_path / "data" / "cas" / "acquisition") == data


def test_acquisition_cas_detects_corruption(tmp_path: Path):
    data = b"example.org\n"
    d = store(data, tmp_path)
    p = tmp_path / "data" / "cas" / "acquisition" / d[:2] / d[2:]
    p.write_bytes(b"corrupt")
    try:
        load(d, tmp_path)
    except RuntimeError as exc:
        assert "digest mismatch" in str(exc)
    else:
        raise AssertionError("corrupt CAS object must fail closed")


def test_manifest_digest_ignores_runtime_timestamp(tmp_path: Path):
    base = {"date": "2026-09-02", "registry_version": 3, "sources": [{"source": "demo", "files": [{"cas_sha256": "a" * 64}]}]}
    a = seal({**base, "created_at": "2026-09-02T00:00:00Z"})
    b = seal({**base, "created_at": "2026-09-02T01:00:00Z"})
    assert verify(a) and verify(b)
    assert digest(a) == digest(b)
    assert json.dumps(a, sort_keys=True)
