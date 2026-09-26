from __future__ import annotations

from scripts.fetchers.github_raw import GitHubRawFetcher
import scripts.fetchers.github_raw as github_raw


def test_immutable_configuration_error_returns_well_formed_fetch_result(monkeypatch) -> None:
    def fail(_entry, _cfg):
        raise ValueError("immutable binding is invalid")

    monkeypatch.setattr(github_raw, "_immutable_cfg", fail)
    fetcher = GitHubRawFetcher({
        "type": "github_raw",
        "owner": "example",
        "repo": "rules",
        "branch": "main",
        "fallback_bases": [],
    })

    result = fetcher.fetch_one({"path": "rule/demo.yaml", "name": "demo.yaml"})

    assert result.ok is False
    assert result.url == "https://raw.githubusercontent.com/example/rules/main/rule/demo.yaml"
    assert result.error == "immutable binding is invalid"
