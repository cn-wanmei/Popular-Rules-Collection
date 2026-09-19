"""V3 rule-directory contract validation."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
ROOT=Path(__file__).resolve().parents[3]
def load_yaml(path:Path)->dict[str,Any]:
    data=yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data,dict): raise ValueError(f"expected mapping: {path}")
    return data
def _rule_files(root:Path)->list[Path]:
    if not root.exists(): return []
    allowed={".yaml",".yml",".json",".jsonl",".list",".txt",".mmdb"}
    return [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in allowed]
def validate(root:Path=ROOT,require_rules_content:bool=False)->dict[str,Any]:
    root=Path(root).resolve()
    policy_path=root/"config/service_model/directories.yaml"
    policy=load_yaml(policy_path)
    if policy.get("schema")!="rule_directory_policy_v1": raise ValueError("unsupported directory policy schema")
    errors=[]; rules_root=root/"rules"; generated_root=root/"generated"; semantics=policy.get("semantics") or {}
    if semantics.get("no_flattened_service_files") is not True: errors.append("policy must forbid flattened service files")
    files=_rule_files(rules_root)
    if require_rules_content and not rules_root.is_dir(): errors.append("canonical rules/ root does not exist")
    if require_rules_content and rules_root.is_dir() and not files: errors.append("canonical rules/ root contains no supported rule files")
    for path in files:
        rel=path.relative_to(rules_root).parts
        if len(rel)<3:
            errors.append(f"canonical rule file is too shallow: {path.relative_to(root)}"); continue
        provider,scope=rel[0],rel[1]
        if scope in {"china","all"} and scope!="all": errors.append(f"invalid canonical scope placement: {path.relative_to(root)}")
        if provider=="china" and scope!="all": errors.append(f"China may only contain the all aggregate: {path.relative_to(root)}")
    china=policy.get("china") or {}; excluded_list=china.get("exclude_independent_providers") or []; excluded={str(x).strip().lower() for x in excluded_list}
    if len(excluded)!=len(excluded_list): errors.append("China exclusion list contains duplicates or empty provider ids")
    if china.get("require_domain_and_ip_coverage") is not True: errors.append("China aggregate must require domain and IP coverage")
    return {"schema":"rule_directory_gate_v2","pass":not errors,"errors":errors,"canonical_rule_files":len(files),"generated_rule_files":len(_rule_files(generated_root)),"require_rules_content":require_rules_content,"china_excluded_independent_providers":sorted(excluded),"policy":str(policy_path.relative_to(root))}
