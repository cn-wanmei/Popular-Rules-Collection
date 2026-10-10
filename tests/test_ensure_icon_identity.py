from __future__ import annotations

import hashlib
import sys

import pytest

from scripts import ensure_icon_identity as identity


def snapshot_with_sha(value: str, ref: str = "deadbeef") -> dict:
    return {"source": {"file_sha256": value, "ref": ref}}


def invoke_main(monkeypatch, index_path, snapshot, *, token="", extra_args=None):
    monkeypatch.setattr(identity, "fetch_snapshot", lambda: snapshot)
    monkeypatch.setattr(identity, "current_git_sha", lambda: "a" * 40)
    monkeypatch.setenv("ICON_DISPATCH_TOKEN", token)
    args = [
        "ensure_icon_identity.py",
        "--index-path",
        str(index_path),
        "--timeout-seconds",
        "5",
        "--poll-interval-seconds",
        "1",
    ]
    args.extend(extra_args or [])
    monkeypatch.setattr(sys, "argv", args)
    return identity.main()


def test_matching_snapshot_does_not_require_dispatch_token(tmp_path, monkeypatch):
    index_path = tmp_path / "_index.yaml"
    raw = b"entries:\n  - id: example\n    entity: service\n"
    index_path.write_bytes(raw)
    expected = hashlib.sha256(raw).hexdigest()

    result = invoke_main(
        monkeypatch,
        index_path,
        snapshot_with_sha(expected),
    )

    assert result == 0


def test_stale_snapshot_without_token_fails_closed(tmp_path, monkeypatch):
    index_path = tmp_path / "_index.yaml"
    index_path.write_bytes(b"entries: []\n")

    with pytest.raises(SystemExit, match="ICON_DISPATCH_TOKEN is not configured"):
        invoke_main(
            monkeypatch,
            index_path,
            snapshot_with_sha("0" * 64),
        )


def test_dispatches_once_and_waits_for_exact_snapshot(tmp_path, monkeypatch):
    index_path = tmp_path / "_index.yaml"
    raw = b"entries:\n  - id: example\n    entity: service\n"
    index_path.write_bytes(raw)
    expected = hashlib.sha256(raw).hexdigest()
    responses = iter([
        snapshot_with_sha("0" * 64, "old-collection-sha"),
        snapshot_with_sha(expected, "new-collection-sha"),
    ])
    calls = []

    monkeypatch.setattr(identity, "fetch_snapshot", lambda: next(responses))
    monkeypatch.setattr(identity, "current_git_sha", lambda: "a" * 40)
    monkeypatch.setattr(identity, "dispatch_identity_refresh", lambda *args: calls.append(args))
    monkeypatch.setattr(identity.time, "sleep", lambda _: None)
    monkeypatch.setenv("ICON_DISPATCH_TOKEN", "test-token")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "ensure_icon_identity.py",
            "--index-path",
            str(index_path),
            "--source",
            "test",
            "--timeout-seconds",
            "5",
            "--poll-interval-seconds",
            "1",
        ],
    )

    assert identity.main() == 0
    assert len(calls) == 1
    assert calls[0][0] == "test-token"
    assert calls[0][1] == "test"
    assert calls[0][2] == "a" * 40
    assert calls[0][3] == expected


def test_pinned_sha_supports_transition_alias():
    assert identity.pinned_sha({"source": {"file_sha": "abc"}}) == "abc"
    assert identity.pinned_sha({"source": {"file_sha256": "def", "file_sha": "abc"}}) == "def"
    assert identity.pinned_sha({}) == ""
