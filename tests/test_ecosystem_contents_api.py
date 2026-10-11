from __future__ import annotations

import json

from scripts import ensure_icon_identity as identity
from scripts import verify_ecosystem_release_lock as verifier
from scripts import write_ecosystem_release_lock as writer


class FakeResponse:
    def __init__(self, payload: bytes):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


def install_api_response(monkeypatch, module, payload: bytes) -> dict:
    observed = {}

    def fake_urlopen(request, timeout=60):
        observed["url"] = request.full_url
        observed["accept"] = request.get_header("Accept")
        observed["authorization"] = request.get_header("Authorization")
        observed["cache_control"] = request.get_header("Cache-control")
        return FakeResponse(payload)

    monkeypatch.setattr(module.urllib.request, "urlopen", fake_urlopen)
    return observed


def test_identity_poll_reads_live_icon_snapshot_via_authenticated_contents_api(monkeypatch):
    expected = {
        "schema": "collection_icon_identity_snapshot_v1",
        "source": {"file_sha256": "a" * 64, "ref": "c" * 40},
    }
    monkeypatch.setenv("ICON_DISPATCH_TOKEN", "unit-test-token")
    observed = install_api_response(
        monkeypatch, identity, json.dumps(expected).encode("utf-8")
    )

    assert identity.fetch_snapshot() == expected
    assert observed["url"].startswith(
        "https://api.github.com/repos/cn-wanmei/Popular-Rules-Icon/contents/"
    )
    assert "ref=main" in observed["url"]
    assert "raw.githubusercontent.com" not in observed["url"]
    assert observed["accept"] == "application/vnd.github.raw+json"
    assert observed["authorization"] == "Bearer unit-test-token"
    assert observed["cache_control"] == "no-cache"


def test_lock_writer_preserves_raw_json_file_returned_by_contents_api(monkeypatch):
    expected = {
        "schema": "collection_icon_identity_snapshot_v1",
        "source": {"file_sha256": "b" * 64},
    }
    raw = json.dumps(expected).encode("utf-8")
    observed = install_api_response(monkeypatch, writer, raw)

    result = writer.fetch_repo_file_bytes(
        "cn-wanmei/Popular-Rules-Icon", "config/collection_identity_snapshot.json"
    )

    assert json.loads(result.decode("utf-8")) == expected
    assert observed["url"].startswith(
        "https://api.github.com/repos/cn-wanmei/Popular-Rules-Icon/contents/"
    )
    assert "ref=main" in observed["url"]
    assert "raw.githubusercontent.com" not in observed["url"]


def test_strict_verifier_reads_live_icon_snapshot_via_contents_api(monkeypatch):
    expected = {
        "schema": "collection_icon_identity_snapshot_v1",
        "source": {"file_sha256": "d" * 64, "ref": "e" * 40},
    }
    observed = install_api_response(
        monkeypatch, verifier, json.dumps(expected).encode("utf-8")
    )

    assert verifier.read_live_icon_snapshot() == expected
    assert observed["url"].startswith(
        "https://api.github.com/repos/cn-wanmei/Popular-Rules-Icon/contents/"
    )
    assert "ref=main" in observed["url"]
    assert observed["accept"] == "application/vnd.github.raw+json"
    assert "raw.githubusercontent.com" not in observed["url"]
