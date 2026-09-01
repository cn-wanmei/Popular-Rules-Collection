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
