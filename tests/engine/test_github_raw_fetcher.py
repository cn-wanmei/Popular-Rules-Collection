from __future__ import annotations

from unittest.mock import Mock, patch

from scripts.fetchers.github_raw import GitHubRawFetcher


def _response(status: int, content: bytes = b"", headers: dict[str, str] | None = None) -> Mock:
    response = Mock()
    response.status_code = status
    response.content = content
    response.headers = headers or {}
    return response


def test_github_raw_falls_back_to_cdn_on_transient_failure() -> None:
    fetcher = GitHubRawFetcher({
        "owner": "owner",
        "repo": "repo",
        "branch": "main",
    })
    with patch("scripts.fetchers.github_raw.SESSION.get", side_effect=[
        _response(503),
        _response(200, b"payload\n", {"etag": '"cdn"'}),
    ]) as get:
        result = fetcher.fetch_one({"path": "rules/a.yaml", "name": "a.yaml"})

    assert result.ok is True
    assert result.status_code == 200
    assert result.content == b"payload\n"
    assert "cdn.jsdelivr.net/gh/owner/repo@main" in result.url
    assert get.call_count == 2


def test_github_raw_does_not_mask_permanent_404() -> None:
    fetcher = GitHubRawFetcher({"owner": "owner", "repo": "repo", "branch": "main"})
    with patch("scripts.fetchers.github_raw.SESSION.get", return_value=_response(404)) as get:
        result = fetcher.fetch_one({"path": "missing.yaml", "name": "missing.yaml"})

    assert result.ok is False
    assert result.status_code == 404
    assert get.call_count == 1


def test_github_raw_preserves_conditional_headers_on_fallback() -> None:
    fetcher = GitHubRawFetcher({"owner": "owner", "repo": "repo", "branch": "main"})
    with patch("scripts.fetchers.github_raw.SESSION.get", side_effect=[
        _response(503),
        _response(304, headers={"etag": '"same"'}),
    ]) as get:
        result = fetcher.fetch_one({
            "path": "rules/a.yaml",
            "name": "a.yaml",
            "headers": {"If-None-Match": '"same"'},
        })

    assert result.ok is True
    assert result.not_modified is True
    assert result.status_code == 304
    assert get.call_args_list[1].kwargs["headers"]["If-None-Match"] == '"same"'


def test_immutable_binding_fetches_release_from_source_repository(
    monkeypatch, tmp_path
) -> None:
    import hashlib

    import yaml

    import scripts.fetchers.github_raw as github_raw

    payload = b"apple-cloudkit.com\\ndeveloper.apple.com\\n"
    expected_sha256 = hashlib.sha256(payload).hexdigest()
    source_ref = "a" * 40
    release_path = "releases/appledev/snap-appledev-test/release.json"
    artifact_path = "generated/source/appledev/domains.txt"
    release = {
        "service_id": "appledev",
        "snapshot_id": "snap-appledev-test",
        "content_digest": "content-digest",
        "evidence_digest": "evidence-digest",
        "policy_digest": "policy-digest",
        "generator_digest": "generator-digest",
        "release_digest": "release-digest",
        "release_identity_version": "2",
        "checksums": {"domains.txt": expected_sha256},
    }
    registry = {
        "source_repository": "cn-wanmei/Popular-Rules-Source",
        "bindings": {
            "appledev": {
                "status": "active",
                "source_id": "popular-rules-source",
                "source_ref": source_ref,
                "artifact_path": artifact_path,
                "release_path": release_path,
                "snapshot_id": "snap-appledev-test",
                "content_digest": "content-digest",
                "evidence_digest": "evidence-digest",
                "policy_digest": "policy-digest",
                "generator_digest": "generator-digest",
                "release_digest": "release-digest",
                "release_identity_version": "2",
                "expected_sha256": expected_sha256,
            }
        },
    }
    registry_path = tmp_path / "immutable_registry.yaml"
    registry_path.write_text(yaml.safe_dump(registry), encoding="utf-8")
    monkeypatch.setattr(github_raw, "IMMUTABLE_REGISTRY", registry_path)

    release_response = _response(200)
    release_response.json.return_value = release
    artifact_response = _response(200, payload)
    fetcher = GitHubRawFetcher({
        "owner": "LM-Firefly",
        "repo": "Rules",
        "branch": "master",
    })

    with patch(
        "scripts.fetchers.github_raw.SESSION.get",
        side_effect=[release_response, artifact_response],
    ) as get:
        result = fetcher.fetch_one({
            "path": "Apple/AppleDev.list",
            "name": "LM_Firefly_AppleDev.list",
            "service": "appledev",
        })

    assert result.ok is True
    assert result.content == payload
    assert get.call_count == 2
    assert get.call_args_list[0].args[0] == (
        f"https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Source/"
        f"{source_ref}/{release_path}"
    )
    assert get.call_args_list[1].args[0] == (
        f"https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Source/"
        f"{source_ref}/{artifact_path}"
    )
