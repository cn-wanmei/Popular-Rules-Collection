#!/usr/bin/env python3
"""V2.4 Golden L1 Structural / L2 Semantic / L3 Behavioral."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IR_OUT = ROOT / "generated" / "mihomo_ir"
CLASSIC = ROOT / "generated" / "mihomo"
REPORT = ROOT / "reports" / "mihomo_ir_golden.json"
PILOT = ("openai", "github", "telegram", "apple", "google")
BEHAVIOR = [
    ("chat.openai.com", "openai", "PROXY"),
    ("api.github.com", "github", "PROXY"),
    ("web.telegram.org", "telegram", "PROXY"),
    ("apple.com", "apple", "PROXY"),
    ("google.com", "google", "PROXY"),
]


def semantic_set_from_list(path: Path):
    out = set()
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("DOMAIN-SUFFIX,"):
            out.add(("domain_suffix", line.split(",", 1)[1].lower()))
        elif line.startswith("DOMAIN-KEYWORD,"):
            out.add(("domain_keyword", line.split(",", 1)[1].lower()))
        elif line.startswith("DOMAIN-REGEX,"):
            out.add(("domain_regex", line.split(",", 1)[1].lower()))
        elif line.startswith("DOMAIN,"):
            out.add(("domain", line.split(",", 1)[1].lower()))
        elif line.startswith("IP-CIDR6,"):
            out.add(("ip_cidr6", line.split(",", 1)[1].split(",")[0]))
        elif line.startswith("IP-CIDR,"):
            out.add(("ip_cidr", line.split(",", 1)[1].split(",")[0]))
    return out


def list_contains_host(path: Path, host: str) -> bool:
    host = host.lower()
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    if host in text:
        return True
    for line in text.splitlines():
        if "domain-suffix," in line:
            suf = line.split("domain-suffix,", 1)[-1].strip()
            if host == suf or host.endswith("." + suf):
                return True
        if line.startswith("domain,") and line.split(",", 1)[-1].strip() == host:
            return True
    return False


def main() -> int:
    structural, semantic, behavioral = [], [], []
    hard = 0
    for sid in PILOT:
        ir_yaml, ir_list = IR_OUT / f"{sid}.yaml", IR_OUT / f"{sid}.list"
        ok_s = ir_yaml.exists() and ir_list.exists() and ir_yaml.stat().st_size > 10
        structural.append({"service": sid, "pass": ok_s})
        if not ok_s:
            hard += 1
        classic, ir_set = semantic_set_from_list(CLASSIC / f"{sid}.list"), semantic_set_from_list(ir_list)
        if not ir_set:
            semantic.append({"service": sid, "pass": False, "reason": "empty_ir"})
            hard += 1
        elif not classic:
            semantic.append({"service": sid, "pass": True, "ir": len(ir_set)})
        else:
            inter = len(classic & ir_set)
            jaccard = inter / (len(classic | ir_set) or 1)
            cover = inter / (len(classic) or 1)
            ok = jaccard >= 0.5 or cover >= 0.7
            semantic.append({"service": sid, "pass": ok, "jaccard": round(jaccard, 4), "cover_classic": round(cover, 4)})
            if not ok:
                hard += 1
    for host, sid, expect in BEHAVIOR:
        hit = list_contains_host(IR_OUT / f"{sid}.list", host)
        behavioral.append({"host": host, "service": sid, "expect_action": expect, "matched_in_ir": hit, "pass": hit})
        if not hit:
            hard += 1
    report = {"structural": structural, "semantic": semantic, "behavioral": behavioral, "hard_failures": hard, "pass": hard == 0}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[mihomo_ir_golden] hard={hard} pass={report['pass']}")
    return 0 if hard == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
