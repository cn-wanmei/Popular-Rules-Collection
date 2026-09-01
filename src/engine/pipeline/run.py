"""Engine pipeline — data/generated/ workspace; publish → generated/."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

STAGES_ALL = (
    "naming_gate", "canonical", "hierarchy", "ir", "ir_full", "adapters", "diff",
    "snapshot", "quarantine", "golden", "release", "publish",
)


def _run_stage(name: str) -> int:
    if name == "naming_gate":
        from src.engine.validation.naming_gate import main as naming_main
        return naming_main()

    from src.engine.canonical.store import build_from_v2_services, load_memberships, load_rules
    from src.engine.legacy_import.v2_service_model import load_entity_graph
    from src.engine.hierarchy.resolver import resolve_aggregate
    from src.engine.ir.builder import build_ir, build_ir_streaming_full
    from src.engine.adapters.build_all import build_service_lists
    from src.engine.snapshot.engine import snapshot_v2_oracle
    from src.engine.quarantine.engine import evaluate_health_yaml
    from src.engine.golden.runner import run_golden
    from src.engine.release.cutover import write_cutover_manifest, publish_artifacts_to_production
    from src.engine import __version__

    services_dir = ROOT / "database" / "services"
    sm_dir = ROOT / "config" / "service_model"
    data = ROOT / "data" / "generated"
    canon, ir_dir, art, reports = data / "canonical", data / "ir", data / "artifacts", data / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    if name == "canonical":
        m = build_from_v2_services(services_dir, canon)
        print(f"[engine] canonical unique_rules={m['unique_rules']} memberships={m['memberships']}")
        return 0
    if name == "snapshot":
        m = snapshot_v2_oracle(ROOT)
        print(f"[engine] snapshot id={m['snapshot_id']} files={m['file_count']}")
        return 0
    if name == "quarantine":
        r = evaluate_health_yaml(ROOT, data / "quarantine" / "state.json")
        print(f"[engine] quarantine evaluated={r['evaluated']} accepted={r['accepted']} quarantined={r['quarantined']}")
        return 0
    if name == "golden":
        g = run_golden(ROOT)
        print(f"[engine] golden pass={g['pass']} hard={g['hard_failures']}")
        return 0 if g["pass"] else 1
    if name == "release":
        doc = write_cutover_manifest(ROOT, version=__version__)
        print(f"[engine] release status={doc['status']} version={doc.get('product_version') or doc.get('version')} cutover={doc['production_cutover']}")
        return 0 if doc["status"] == "RC_READY" else 1
    if name == "publish":
        r = publish_artifacts_to_production(ROOT, dry_run=False)
        print(f"[engine] publish ok={r.get('ok')} copied={r.get('copied')}")
        return 0 if r.get("ok") else 1

    graph = load_entity_graph(sm_dir)
    rules = load_rules(canon)
    memberships = load_memberships(canon)

    if name == "hierarchy":
        hier = {}
        for vid in sorted(graph.aggregates.keys()):
            resolved = resolve_aggregate(graph, vid, memberships, rules)
            hier[vid] = {"rules": resolved["rule_count"], "sha256": resolved["sha256"], "members": resolved["members"]}
            print(f"[engine] hierarchy {vid} rules={resolved['rule_count']}")
        (reports / "hierarchy_summary.json").write_text(json.dumps(hier, indent=2) + "\n")
        return 0
    if name == "ir":
        meta = build_ir(rules, memberships, graph, ir_dir, full=False)
        print(f"[engine] ir rules={meta['rules']} scope={meta['scope']}")
        return 0
    if name == "ir_full":
        meta = build_ir_streaming_full(canon, graph, ir_dir)
        print(f"[engine] ir_full rules={meta['rules']}")
        return 0
    if name == "adapters":
        stats = build_service_lists(rules, memberships, graph, art)
        print(f"[engine] adapters {list(stats.keys())}")
        return 0
    if name == "diff":
        v2_summary = ROOT / "reports" / "hierarchy" / "summary.json"
        v3_summary = reports / "hierarchy_summary.json"
        diff: dict = {"compared": False}
        if v2_summary.exists() and v3_summary.exists():
            v2 = {x["view"]: x for x in json.loads(v2_summary.read_text())}
            v3 = json.loads(v3_summary.read_text())
            rows = [{
                "view": vid,
                "v2_rules": (v2.get(vid) or {}).get("rules"),
                "v3_rules": v3r.get("rules"),
                "rules_match": (v2.get(vid) or {}).get("rules") == v3r.get("rules"),
                "sha_match": (v2.get(vid) or {}).get("sha256") == v3r.get("sha256"),
            } for vid, v3r in v3.items()]
            diff = {"compared": True, "rows": rows, "all_rules_match": all(r["rules_match"] for r in rows), "all_sha_match": all(r["sha_match"] for r in rows)}
            print(f"[engine] diff rules_match={diff['all_rules_match']}")
        (reports / "differential.json").write_text(json.dumps(diff, indent=2) + "\n")
        return 0

    print(f"unknown stage: {name}", file=sys.stderr)
    return 2


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    stage = argv[0] if argv else "all"
    if stage == "all":
        for s in STAGES_ALL:
            r = subprocess.run([sys.executable, "-m", "src.engine.cli", s], cwd=str(ROOT))
            if r.returncode != 0:
                print(f"[engine] stage failed: {s}", file=sys.stderr)
                return r.returncode
        print("[engine] pipeline all done → data/generated/ + generated/")
        return 0
    return _run_stage(stage)


if __name__ == "__main__":
    raise SystemExit(main())
