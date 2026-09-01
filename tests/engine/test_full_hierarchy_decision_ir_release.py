"""Full Hierarchy + Decision + IR + Golden L1-L7 + Release State Machine."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from src.engine.pipeline.run import run_pipeline, STAGES


def _sources(tmp: Path) -> Path:
    src = tmp / "sources" / "services"
    src.mkdir(parents=True)
    (src / "google-gmail.yaml").write_text(
        "id: google-gmail\ncategory: mail\nrules:\n"
        "  - type: DOMAIN-SUFFIX\n    value: gmail.com\n"
        "  - type: DOMAIN\n    value: mail.google.com\n", encoding="utf-8")
    (src / "google-drive.yaml").write_text(
        "id: google-drive\ncategory: storage\nrules:\n"
        "  - type: DOMAIN-SUFFIX\n    value: drive.google.com\n", encoding="utf-8")
    (src / "china.yaml").write_text(
        "id: china\ncategory: china\nrules:\n"
        "  - type: DOMAIN-SUFFIX\n    value: baidu.com\n", encoding="utf-8")
    return tmp / "sources"


def test_full_pipeline_hierarchy_ir_golden_release():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        sources = _sources(tmp)
        data = tmp / "data"
        result = run_pipeline(sources, data)

        assert result["v2_runtime_dependency"] == 0
        assert result["status"] == "ok"
        for s in STAGES:
            assert s in result["stages"], f"missing stage {s}"

        run_id = result["run_id"]
        run_dir = data / "runs" / run_id

        # Hierarchy
        hier = json.loads((run_dir / "hierarchy" / "graph.json").read_text(encoding="utf-8"))
        assert "google-gmail" in hier["services"]
        assert "google" in hier["groups"]
        assert "google" in hier["aggregates"]

        # IR contains full hierarchy + decisions
        ir = json.loads((run_dir / "ir" / "ir.json").read_text(encoding="utf-8"))
        assert len(ir["entity"]["services"]) >= 3
        assert len(ir["entity"]["groups"]) >= 1
        assert len(ir["decisions"]) >= 3
        assert ir["v2_runtime_dependency"] == 0
        # china rule must be DIRECT
        china_dec = [d for d in ir["decisions"] if "baidu.com" in d.get("value", "")]
        assert china_dec and china_dec[0]["action"] == "DIRECT"

        # Golden
        golden = json.loads((run_dir / "golden" / "report.json").read_text(encoding="utf-8"))
        assert golden["all_pass"] is True
        for level in ("L1_snapshot", "L2_canonical", "L3_hierarchy", "L4_ir",
                      "L5_native_adapters", "L6_service_views", "L7_reproducibility_base"):
            assert golden["results"][level]["pass"] is True, level

        # Release State Machine
        release = json.loads((run_dir / "release" / "state.json").read_text(encoding="utf-8"))
        assert release["state"] == "RC_READY"
        assert release["can_publish"] is True
        assert release["gates"]["v2_runtime_dependency_zero"] is True
        assert release["gates"]["golden_all_pass"] is True


def test_stage_order_complete():
    assert STAGES.index("quarantine") < STAGES.index("canonical")
    assert STAGES.index("canonical") < STAGES.index("hierarchy")
    assert STAGES.index("hierarchy") < STAGES.index("ir")
    assert STAGES.index("ir") < STAGES.index("adapters")
    assert STAGES.index("adapters") < STAGES.index("golden")
    assert STAGES.index("golden") < STAGES.index("release")
