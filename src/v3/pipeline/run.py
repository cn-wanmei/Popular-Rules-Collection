"""V3 pipeline — writes only under data/v3/."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

STAGES_ALL = (
    "canonical", "hierarchy", "ir", "ir_full", "adapters", "diff",
    "snapshot", "quarantine", "golden", "release",
)


def _run_stage(name: str) -> int:
    from src.v3.canonical.store import build_from_v2_services, load_memberships, load_rules
    from src.v3.legacy_import.v2_service_model import load_entity_graph
    from src.v3.hierarchy.resolver import resolve_aggregate
    from src.v3.ir.builder import build_ir, build_ir_streaming_full
    from src.v3.adapters.build_all import build_service_lists
    from src.v3.snapshot.engine import snapshot_v2_oracle
    from src.v3.quarantine.engine import evaluate_health_yaml
    from src.v3.golden.runner import run_golden
    from src.v3.release.cutover import write_cutover_manifest
    from src.v3 import __version__

    services_dir = ROOT / "database" / "services"
    sm_dir = ROOT / "config" / "service_model"
    data = ROOT / "data" / "v3"
    canon, ir_dir, art, reports = data / "canonical", data / "ir", data / "artifacts", data / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    if name == "canonical":
        m = build_from_v2_services(services_dir, canon)
        print(f"[v3] canonical unique_rules={m['unique_rules']} memberships={m['memberships']}")
        return 0
    if name == "snapshot":
        m = snapshot_v2_oracle(ROOT)
        print(f"[v3] snapshot id={m['snapshot_id']} files={m['file_count']}")
        return 0
    if name == "quarantine":
        state = data / "quarantine" / "state.json"
        r = evaluate_health_yaml(ROOT, state)
        print(f"[v3] quarantine evaluated={r['evaluated']} accepted={r['accepted']} quarantined={r['quarantined']}")
        return 0
    if name == "golden":
        g = run_golden(ROOT)
        print(f"[v3] golden pass={g['pass']} hard={g['hard_failures']}")
        return 0 if g["pass"] else 1
    if name == "release":
        doc = write_cutover_manifest(ROOT, version=__version__)
        print(f"[v3] release status={doc['status']} version={doc['version']}")
        return 0 if doc["status"] == "RC_READY" else 1

    graph = load_entity_graph(sm_dir)
    rules = load_rules(canon)
    memberships = load_memberships(canon)

    if name == "hierarchy":
        hier = {}
        for vid in sorted(graph.aggregates.keys()):
            resolved = resolve_aggregate(graph, vid, memberships, rules)
            hier[vid] = {"rules": resolved["rule_count"], "sha256": resolved["sha256"], "members": resolved["members"]}
            print(f"[v3] hierarchy {vid} rules={resolved['rule_count']}")
        (reports / "hierarchy_summary.json").write_text(json.dumps(hier, indent=2) + "\n")
        return 0
    if name == "ir":
        meta = build_ir(rules, memberships, graph, ir_dir, full=False)
        print(f"[v3] ir scope={meta['scope']} rules={meta['rules']} digest={meta['ir_digest'][:12]}")
        return 0
    if name == "ir_full":
        meta = build_ir_streaming_full(canon, graph, ir_dir)
        print(f"[v3] ir_full rules={meta['rules']} digest={meta['ir_digest'][:12]}")
        return 0
    if name == "adapters":
        stats = build_service_lists(rules, memberships, graph, art)
        print(f"[v3] adapters clients={list(stats.keys())}")
        return 0
    if name == "diff":
        v2_summary = ROOT / "reports" / "hierarchy" / "summary.json"
        v3_summary = reports / "hierarchy_summary.json"
        diff: dict = {"compared": False}
        if v2_summary.exists() and v3_summary.exists():
            v2 = {x["view"]: x for x in json.loads(v2_summary.read_text())}
            v3 = json.loads(v3_summary.read_text())
            rows = []
            for vid, v3r in v3.items():
                v2r = v2.get(vid) or {}
                rows.append({
                    "view": vid,
                    "v2_rules": v2r.get("rules"),
                    "v3_rules": v3r.get("rules"),
                    "rules_match": v2r.get("rules") == v3r.get("rules"),
                    "sha_match": v2r.get("sha256") == v3r.get("sha256"),
                })
            diff = {
                "compared": True,
                "rows": rows,
                "all_rules_match": all(r["rules_match"] for r in rows),
                "all_sha_match": all(r["sha_match"] for r in rows),
            }
            print(f"[v3] diff rules_match={diff['all_rules_match']} sha_match={diff['all_sha_match']}")
        else:
            print("[v3] diff skipped (missing summary)")
        (reports / "differential.json").write_text(json.dumps(diff, indent=2) + "\n")
        return 0

    print(f"unknown stage: {name}", file=sys.stderr)
    return 2


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    stage = argv[0] if argv else "all"
    if stage == "all":
        for s in STAGES_ALL:
            r = subprocess.run([sys.executable, "-m", "src.v3.cli", s], cwd=str(ROOT))
            if r.returncode != 0:
                print(f"[v3] stage failed: {s} code={r.returncode}", file=sys.stderr)
                return r.returncode
        print("[v3] pipeline all done → data/v3/")
        return 0
    return _run_stage(stage)


if __name__ == "__main__":
    raise SystemExit(main())
