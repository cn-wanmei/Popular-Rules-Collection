"""Phase 5 — Seven-client regression harness.

Validates that each native adapter can emit non-empty artifacts for the
rule kinds used by the V1 golden / full catalogue:

    domain / suffix / keyword / CIDR / URL / Aggregate

Compares structural presence across:

    Legacy  vs  V1  vs  IR  vs  Generated

This module is intentionally lightweight: it does not re-run the full
pipeline.  It inspects already-built run directories (or synthetic fixtures)
and reports per-client / per-kind coverage.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Must stay in sync with src.engine.adapters.registry.CLIENTS
CLIENTS: tuple[str, ...] = (
    "mihomo",
    "singbox",
    "surge",
    "shadowrocket",
    "quantumultx",
    "egern",
    "loon",
)

CLIENT_EXT: dict[str, str] = {
    "mihomo": ".yaml",
    "singbox": ".json",
    "surge": ".list",
    "shadowrocket": ".list",
    "quantumultx": ".list",
    "egern": ".yaml",
    "loon": ".list",
}

RULE_KINDS: tuple[str, ...] = (
    "domain",
    "suffix",
    "keyword",
    "CIDR",
    "URL",
    "Aggregate",
)


@dataclass
class ClientKindResult:
    client: str
    kind: str
    present: bool
    sample_count: int = 0
    detail: str = ""


@dataclass
class ClientRegressionReport:
    schema: str = "v1_client_regression_v1"
    clients: list[str] = field(default_factory=lambda: list(CLIENTS))
    kinds: list[str] = field(default_factory=lambda: list(RULE_KINDS))
    results: list[ClientKindResult] = field(default_factory=list)
    client_artifacts_ok: dict[str, bool] = field(default_factory=dict)
    layers_compared: dict[str, bool] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "clients": self.clients,
            "kinds": self.kinds,
            "results": [
                {
                    "client": r.client,
                    "kind": r.kind,
                    "present": r.present,
                    "sample_count": r.sample_count,
                    "detail": r.detail,
                }
                for r in self.results
            ],
            "client_artifacts_ok": self.client_artifacts_ok,
            "layers_compared": self.layers_compared,
            "errors": self.errors,
            "all_pass": (
                all(self.client_artifacts_ok.values())
                and not self.errors
                and bool(self.client_artifacts_ok)
            ),
        }


def _scan_kind_in_text(text: str, kind: str) -> int:
    """Heuristic count of rule-kind markers in adapter output text."""
    upper = text.upper()
    markers: dict[str, tuple[str, ...]] = {
        "domain": ("DOMAIN,", "DOMAIN-SUFFIX,", "HOST,", '"DOMAIN"', "DOMAIN_SUFFIX"),
        "suffix": ("DOMAIN-SUFFIX,", "HOST-SUFFIX,", "SUFFIX,"),
        "keyword": ("DOMAIN-KEYWORD,", "KEYWORD,", "DOMAIN_KEYWORD"),
        "CIDR": ("IP-CIDR", "IP-CIDR6", "IP_CIDR", '"IP_CIDR"', "GEOIP,"),
        "URL": ("URL-REGEX,", "URL,", "USER-AGENT,"),
        "Aggregate": ("# aggregate", "AGGREGATE", "provider:", "RULE-SET,"),
    }
    count = 0
    for m in markers.get(kind, ()):
        count += upper.count(m.upper())
    return count


def _client_dir_ok(art_dir: Path, client: str) -> bool:
    ext = CLIENT_EXT[client]
    cdir = art_dir / client
    if not cdir.is_dir():
        return False
    files = [p for p in cdir.rglob(f"*{ext}") if p.is_file() and p.stat().st_size > 0]
    return len(files) > 0


def run_client_regression(run_dir: Path) -> ClientRegressionReport:
    """Inspect a completed V3 run directory for 7-client coverage.

    Expected layout (from existing golden/runner):
        run_dir/artifacts/{mihomo,singbox,...}/...
        run_dir/canonical/
        run_dir/ir/
    """
    run_dir = Path(run_dir)
    report = ClientRegressionReport()
    art = run_dir / "artifacts"

    # Layer presence
    report.layers_compared = {
        "Legacy": (run_dir / "legacy").exists() or (run_dir.parent / "legacy").exists(),
        "V1": (run_dir / "v1").exists() or (run_dir / "canonical").exists(),
        "IR": (run_dir / "ir" / "ir.json").exists(),
        "Generated": art.exists(),
    }

    if not art.exists():
        report.errors.append(f"artifacts dir missing: {art}")
        for client in CLIENTS:
            report.client_artifacts_ok[client] = False
        return report

    for client in CLIENTS:
        ok = _client_dir_ok(art, client)
        report.client_artifacts_ok[client] = ok
        if not ok:
            report.errors.append(f"client artifacts missing/empty: {client}")
            for kind in RULE_KINDS:
                report.results.append(
                    ClientKindResult(client=client, kind=kind, present=False, detail="no artifacts")
                )
            continue

        # Aggregate text from a sample of files (cap for speed)
        samples: list[str] = []
        ext = CLIENT_EXT[client]
        for p in sorted(art.joinpath(client).rglob(f"*{ext}"))[:40]:
            try:
                samples.append(p.read_text(encoding="utf-8", errors="replace")[:8000])
            except OSError:
                continue
        blob = "\n".join(samples)

        for kind in RULE_KINDS:
            n = _scan_kind_in_text(blob, kind)
            report.results.append(
                ClientKindResult(
                    client=client,
                    kind=kind,
                    present=n > 0,
                    sample_count=n,
                    detail=f"marker_hits={n}",
                )
            )

    return report


def write_client_regression_report(report: ClientRegressionReport, out_path: Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
