"""V3 human rule and generated distribution directory validation."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
import yaml
from src.engine.distribution.path_resolver import EntityPathResolver

ROOT = Path(__file__).resolve().parents[3]
_METADATA_FILES = {"_index.yaml", "manifest.json", "README.md"}
_ENTITY_TYPES = {"category":"category","group":"group","aggregate":"aggregate","unmapped":"unmapped_service"}
_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")

def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict): raise ValueError(f"expected mapping: {path}")
    return data

def _all_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*") if p.is_file()] if root.exists() else []

def _rule_files(root: Path) -> list[Path]:
    return [p for p in _all_files(root) if p.name.endswith(".yaml") and p.name not in _METADATA_FILES]

def _valid_rule_path(root: Path, path: Path) -> bool:
    parts = path.relative_to(root).parts
    if parts in {("README.md",), ("_index.yaml",), ("manifest.json",)}: return True
    if any(part in {".","..","all","rules"} for part in parts): return False
    if not parts or not parts[-1].endswith(".yaml"): return False
    if not all(_NAME_RE.fullmatch(part) for part in parts[:-1]): return False
    if len(parts) == 3: return parts[2] == f"{parts[1]}.yaml"
    if len(parts) == 4: return parts[0] in _ENTITY_TYPES and parts[3] == f"{parts[2]}.yaml"
    return False

def _provider_metadata(root: Path) -> tuple[dict[str,str], dict[str,set[str]]]:
    path=root/"config/ruleset_hierarchy.yaml"
    if not path.is_file(): return {},{}
    providers=(_load_yaml(path).get("providers") or {})
    aggregates={}; services={}
    for provider,node in providers.items():
        if not isinstance(node,dict): continue
        pid=str(provider).strip().casefold()
        aggregates[pid]=str(node.get("aggregate") or provider).strip()
        services[pid]={str(s).strip().casefold() for s in (node.get("services") or {})}
    return aggregates,services

def _entity_expectation(root: Path,path: Path,aggregates:dict[str,str],services:dict[str,set[str]]) -> tuple[str,str,str|None]:
    parts=path.relative_to(root).parts
    if len(parts)==3:
        provider,name,_=parts
        if provider=="china" and name=="china": return "domestic_aggregate","china",None
        if provider in aggregates and name==provider and name not in services.get(provider,set()):
            return "provider_aggregate",aggregates.get(provider,provider),provider
        return "service",name,provider
    if len(parts)==4 and parts[0] in _ENTITY_TYPES:
        return _ENTITY_TYPES[parts[0]],parts[1],None
    return "invalid","",None

def _validate_rule_payload(root:Path,path:Path,expected_run_id:str|None,aggregates:dict[str,str],services:dict[str,set[str]])->list[str]:
    try: payload=_load_yaml(path)
    except (OSError,UnicodeDecodeError,ValueError,yaml.YAMLError) as exc: return [f"invalid human rule payload: {path.relative_to(root)}: {exc}"]
    errors=[]
    rel=path.relative_to(root).as_posix()
    entity,entity_id,provider=_entity_expectation(root,path,aggregates,services)
    if entity=="invalid":
        return [f"invalid human rule path: {rel}"]
    if payload.get("schema")!="human_rule_distribution_v1": errors.append(f"invalid human rule schema: {rel}")
    if payload.get("entity")!=entity: errors.append(f"human rule entity mismatch: {rel}")
    if str(payload.get("id") or "").strip()!=entity_id: errors.append(f"human rule id mismatch: {rel}")
    actual_provider=str(payload.get("provider") or "").strip().casefold()
    if provider is not None and actual_provider!=provider.casefold(): errors.append(f"human rule provider mismatch: {rel}")
    if provider is None and payload.get("provider") not in {None,""}: errors.append(f"unexpected human rule provider: {rel}")
    generated_from=payload.get("generated_from") or {}
    actual_run_id=str(generated_from.get("run_id") or "").strip()
    if expected_run_id and actual_run_id!=expected_run_id: errors.append(f"human rule lineage mismatch: {rel}")
    if not str(generated_from.get("ir_digest") or "").strip(): errors.append(f"human rule missing ir_digest: {rel}")
    return errors

def validate(root:Path=ROOT,*,rule_root:Path|None=None,generated_root:Path|None=None)->dict[str,Any]:
    workspace=Path(root).resolve()
    policy_path=workspace/"config/service_model/directories.yaml"
    policy=_load_yaml(policy_path)
    errors=[]
    if policy.get("schema")!="rule_distribution_policy_v2": errors.append("unsupported rule distribution policy schema")
    for key,expected in EntityPathResolver.HUMAN_LAYOUT.items():
        if str((policy.get("layout") or {}).get(key) or "").strip()!=expected: errors.append(f"directory policy layout mismatch: {key} must be {expected}")
    alternate=workspace/"rules"
    if alternate.exists(): errors.append("obsolete third rule tree exists: rules/")
    aggregates,services=_provider_metadata(workspace)
    rr=Path(rule_root).resolve() if rule_root is not None else workspace/"rule"
    gr=Path(generated_root).resolve() if generated_root is not None else workspace/"generated"
    if not rr.is_dir(): errors.append(f"human rule distribution root does not exist: {rr}")
    else:
        for required in _METADATA_FILES:
            if not (rr/required).is_file(): errors.append(f"missing human distribution metadata: {rr/required}")
        for path in _all_files(rr):
            if not _valid_rule_path(rr,path): errors.append(f"invalid human rule path: {path.relative_to(rr)}")
        try:
            manifest=json.loads((rr/"manifest.json").read_text(encoding="utf-8"))
            index=_load_yaml(rr/"_index.yaml")
            if manifest.get("schema")!="human_rule_distribution_manifest_v1": errors.append("invalid human distribution manifest schema")
            if index.get("schema")!="human_rule_distribution_index_v1": errors.append("invalid human distribution index schema")
            if manifest.get("layout_schema")!=EntityPathResolver.LAYOUT_SCHEMA: errors.append("human distribution manifest is not directory_layout_v2")
            if index.get("layout_schema")!=EntityPathResolver.LAYOUT_SCHEMA: errors.append("human distribution index is not directory_layout_v2")
            actual=sorted(p.relative_to(rr).as_posix() for p in _rule_files(rr))
            mf=sorted(str(x) for x in (manifest.get("files") or []))
            ix=sorted(str(e.get("path")) for e in (index.get("entries") or []) if isinstance(e,dict) and e.get("path"))
            if manifest.get("status")=="ready":
                if manifest.get("run_id")!=index.get("run_id") or manifest.get("ir_digest")!=index.get("ir_digest"): errors.append("human distribution manifest/index identity mismatch")
                if mf!=actual: errors.append("human distribution manifest file list does not match tree")
                if ix!=actual: errors.append("human distribution index file list does not match tree")
            expected_run=str(manifest.get("run_id") or "").strip() if manifest.get("status")=="ready" else None
            for path in _rule_files(rr): errors.extend(_validate_rule_payload(rr,path,expected_run,aggregates,services))
        except (OSError,UnicodeDecodeError,json.JSONDecodeError,ValueError,yaml.YAMLError) as exc:
            errors.append(f"invalid human distribution metadata: {exc}")
    return {"schema":"rule_distribution_gate_v4","pass":not errors,"errors":errors,"human_rule_files":len(_rule_files(rr)),"canonical_rule_files":len(_rule_files(rr)),"generated_rule_files":len(_all_files(gr)),"alternate_rule_tree_exists":alternate.exists(),"china_excluded_independent_providers":sorted({str(x).strip().casefold() for x in (policy.get("china") or {}).get("exclude_independent_providers") or [] if str(x).strip()}),"policy":str(policy_path.relative_to(workspace)),"rule_root":str(rr),"layout_schema":EntityPathResolver.LAYOUT_SCHEMA}
