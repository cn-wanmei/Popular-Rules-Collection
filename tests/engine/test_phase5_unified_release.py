from src.engine.release import engine as release_engine

def test_unified_release_blocks_when_pipeline_fails(tmp_path, monkeypatch):
    def fake_pipeline(*args, **kwargs): return {"status": "blocked", "run_id": "r1", "failure_stages": ["golden"]}
    called = []
    monkeypatch.setattr(release_engine, "run_pipeline", fake_pipeline)
    monkeypatch.setattr(release_engine, "promote_run", lambda *a, **k: called.append(1))
    result = release_engine.run_unified_release(tmp_path / "sources", tmp_path / "data", tmp_path / "generated")
    assert result["status"] == "blocked"
    assert called == []

def test_unified_release_blocks_before_promotion_when_not_rc_ready(tmp_path, monkeypatch):
    def fake_pipeline(*args, **kwargs): return {"status": "ok", "run_id": "r1", "stages": {"release": {"state": "BLOCKED"}}}
    called = []
    monkeypatch.setattr(release_engine, "run_pipeline", fake_pipeline)
    monkeypatch.setattr(release_engine, "promote_run", lambda *a, **k: called.append(1))
    result = release_engine.run_unified_release(tmp_path / "sources", tmp_path / "data", tmp_path / "generated")
    assert result["status"] == "blocked"
    assert called == []

def test_unified_release_promotes_only_rc_ready(tmp_path, monkeypatch):
    monkeypatch.setattr(release_engine, "run_pipeline", lambda *a, **k: {"status": "ok", "run_id": "r1", "stages": {"release": {"state": "RC_READY"}}})
    monkeypatch.setattr(release_engine, "promote_run", lambda *a, **k: {"run_id": "r1", "release_state": "RC_READY"})
    result = release_engine.run_unified_release(tmp_path / "sources", tmp_path / "data", tmp_path / "generated")
    assert result["status"] == "published"
    assert result["release_state"] == "RC_READY"
