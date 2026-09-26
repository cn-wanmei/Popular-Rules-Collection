from src.engine.validation.manifest_validator import validate_distribution


def _manifest(root, files):
    root.mkdir(parents=True, exist_ok=True)
    (root / "manifest.json").write_text(
        '{"schema":"human_rule_distribution_manifest_v1","schema_version":2,"status":"ready","run_id":"run-1","ir_digest":"abc","layout_schema":"directory_layout_v2","files":' + str(files).replace("'", '"') + "}",
        encoding="utf-8",
    )


def test_accepts_matching_identity(tmp_path):
    rule_root = tmp_path / "rule"
    _manifest(rule_root, ["apple/apple/apple.yaml"])
    result = validate_distribution(
        rule_root=rule_root,
        artifacts_root=tmp_path / "artifacts",
        build_report={
            "schema":"adapter_build_v5",
            "run_id":"run-1",
            "ir_digest":"abc",
            "layout_schema":"directory_layout_v2",
            "resolver":"EntityPathResolver",
            "clients":{"mihomo":{"paths":["apple/appletv/appletv.yaml"]}},
        },
        expected_run_id="run-1",
    )
    assert result["pass"], result["errors"]


def test_rejects_legacy_layout(tmp_path):
    rule_root = tmp_path / "rule"
    _manifest(rule_root, ["apple/apple.yaml"])
    result = validate_distribution(
        rule_root=rule_root,
        artifacts_root=tmp_path / "artifacts",
        build_report={
            "run_id":"run-1",
            "ir_digest":"abc",
            "layout_schema":"directory_layout_v2",
            "resolver":"EntityPathResolver",
            "clients":{},
        },
        expected_run_id="run-1",
    )
    assert not result["pass"]
    assert result["legacy_layout"] == 1
