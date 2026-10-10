from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path

from scripts import verify_ecosystem_release_lock as verifier


def make_lock(index_sha: str, *, matches: bool = True, icon_sha: str | None = None) -> dict:
    return {
        "schema": "popular_rules_ecosystem_release_lock_v1",
        "collection": {"index_sha256": index_sha},
        "icon": {
            "identity_matches_index": matches,
            "collection_identity_sha256": icon_sha if icon_sha is not None else index_sha,
        },
    }


def setup_lock(tmp_path: Path, monkeypatch, lock_data: dict, index_bytes: bytes) -> str:
    lock_path = tmp_path / "reports" / "ecosystem-release-lock.json"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(json.dumps(lock_data), encoding="utf-8")
    index_path = tmp_path / "rule" / "_index.yaml"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_bytes(index_bytes)
    monkeypatch.setattr(verifier, "LOCK", lock_path)
    monkeypatch.setattr(verifier, "INDEX", index_path)
    return hashlib.sha256(index_bytes).hexdigest()


def mock_icon(monkeypatch, snapshot: dict) -> None:
    body = json.dumps(snapshot).encode("utf-8")
    monkeypatch.setattr(
        verifier.urllib.request,
        "urlopen",
        lambda *args, **kwargs: io.BytesIO(body),
    )


def test_verify_passes_only_when_lock_index_and_live_icon_match(tmp_path, monkeypatch, capsys):
    raw = b"entries:\n  - id: example\n    entity: service\n"
    digest = hashlib.sha256(raw).hexdigest()
    setup_lock(tmp_path, monkeypatch, make_lock(digest), raw)
    mock_icon(monkeypatch, {"source": {"file_sha256": digest, "ref": "a" * 40}})

    assert verifier.main() == 0
    assert "OK: ecosystem-release-lock verifies" in capsys.readouterr().out


def test_verify_fails_when_live_icon_drifted_even_if_old_lock_claims_match(tmp_path, monkeypatch, capsys):
    raw = b"entries:\n  - id: example\n    entity: service\n"
    digest = hashlib.sha256(raw).hexdigest()
    setup_lock(tmp_path, monkeypatch, make_lock(digest, matches=True), raw)
    mock_icon(monkeypatch, {"source": {"file_sha256": "0" * 64, "ref": "stale"}})

    assert verifier.main() == 1
    assert "live Icon identity sha256" in capsys.readouterr().out


def test_verify_fails_when_lock_icon_hash_does_not_match_index(tmp_path, monkeypatch, capsys):
    raw = b"entries: []\n"
    digest = hashlib.sha256(raw).hexdigest()
    setup_lock(
        tmp_path,
        monkeypatch,
        make_lock(digest, matches=False, icon_sha="0" * 64),
        raw,
    )

    assert verifier.main() == 1
    assert "lock icon.identity_matches_index is not true" in capsys.readouterr().out


def test_verify_fails_closed_when_live_icon_snapshot_is_unavailable(tmp_path, monkeypatch, capsys):
    raw = b"entries: []\n"
    digest = hashlib.sha256(raw).hexdigest()
    setup_lock(tmp_path, monkeypatch, make_lock(digest), raw)

    def unavailable(*args, **kwargs):
        raise OSError("network unavailable")

    monkeypatch.setattr(verifier.urllib.request, "urlopen", unavailable)
    assert verifier.main() == 1
    assert "could not read live Icon identity snapshot" in capsys.readouterr().out
