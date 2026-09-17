from __future__ import annotations

import argparse
from pathlib import Path

from src.engine.ingest.legacy_asset_reconciliation import reconcile_legacy_assets


def main() -> None:
    parser = argparse.ArgumentParser(description="Reconcile Legacy Asset IR against rule/_index.yaml")
    parser.add_argument("--rule-root", type=Path, default=Path("rule"))
    parser.add_argument("--jsonl", type=Path, default=Path("data/legacy_asset_ir.jsonl"))
    parser.add_argument("--report", type=Path, default=Path("reports/v1/LEGACY_ASSET_RECONCILIATION.yaml"))
    args = parser.parse_args()
    report = reconcile_legacy_assets(args.rule_root, jsonl_output=args.jsonl, report_path=args.report)
    print(f"reconciled services={report['summary']['services']}")
    print(f"exact domains={report['summary']['exact_domain_services']} exact ips={report['summary']['exact_ip_services']}")
    print(f"promotion candidates={sum(1 for x in report['promotion_candidates'] if x['candidate'])} blocked={report['promotion']['blocked']}")


if __name__ == "__main__":
    main()
