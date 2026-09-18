#!/usr/bin/env python3
"""Reproducible V1 Phase 2.3-2.7 repository audit."""
from __future__ import annotations
import argparse, hashlib, ipaddress, json, re, subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import yaml
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_OUT=ROOT/'reports/v1/phase2'
KINDS=('domains','domain_suffixes','domain_keywords','ip_cidrs','urls','unknown')

def git(cmd):
    try:return subprocess.check_output(cmd,cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return 'unknown'

def load_yaml(p,default):
    if not p.exists():return default
    try:
        v=yaml.safe_load(p.read_text(encoding='utf-8')); return default if v is None else v
    except Exception:return default

def norm_domain(v):return v.strip().lower().rstrip('.')
def norm_cidr(v):
    try:return str(ipaddress.ip_network(v.strip(),strict=False))
    except ValueError:return None

def norm_url(v):
    try:
        p=urlsplit(v.strip()); s=p.scheme.lower()
        if s not in ('http','https') or not p.hostname:return None
        h=p.hostname.lower().rstrip('.'); port=p.port
        netloc=h if port is None or (s=='http' and port==80) or (s=='https' and port==443) else f'{h}:{port}'
        return urlunsplit((s,netloc,p.path or '',p.query or '',''))
    except Exception:return None

def looks_domain(v):
    d=norm_domain(v); return '/' not in d and ' ' not in d and '.' in d and re.fullmatch(r'[a-z0-9*_-]+(?:\.[a-z0-9*_-]+)+',d) is not None

def parse_assets(text):
    out={k:set() for k in KINDS}
    for raw in text.splitlines():
        v=raw.strip()
        if not v or v.startswith('#'):continue
        if ',' in v and not v.startswith(('http://','https://')):
            typ,val,*_=v.split(','); typ=typ.strip().upper(); val=val.strip()
            if typ in ('DOMAIN','DOMAIN-WILDCARD') and looks_domain(val):out['domains'].add(norm_domain(val));continue
            if typ in ('DOMAIN-SUFFIX','DOMAIN-SET') and val:out['domain_suffixes'].add(norm_domain(val).lstrip('*.'));continue
            if typ in ('DOMAIN-KEYWORD','HOST-KEYWORD') and val:out['domain_keywords'].add(val.lower());continue
            if typ.startswith('IP-CIDR'):
                c=norm_cidr(val)
                if c:out['ip_cidrs'].add(c);continue
            if typ in ('URL','URL-REGEX'):
                u=norm_url(val)
                if u:out['urls'].add(u);continue
        u=norm_url(v)
        if u:out['urls'].add(u);continue
        c=norm_cidr(v)
        if c:out['ip_cidrs'].add(c);continue
        d=norm_domain(v)
        if d.startswith('*.'):out['domain_suffixes'].add(d[2:]);continue
        if looks_domain(v):out['domains'].add(d);continue
        out['unknown'].add(v)
    return out

def merge(dst,src):
    for k in KINDS:dst[k].update(src[k])

def flatten_index(idx):
    rows=[]
    for cat in sorted((idx.get('categories') or {}), key=lambda x: str(x).casefold()):
        block=(idx.get('categories') or {}).get(cat)
        if not isinstance(block,dict):continue
        rules=block.get('rules') or []
        for e in sorted((x for x in rules if isinstance(x,dict)), key=lambda x: (str(x.get('id','')).casefold(), str(x.get('path','')))):
            x=dict(e);x['category']=str(cat);rows.append(x)
    return rows

def metadata(p):return load_yaml(p,{}) if p.exists() else {}

def assets(entry_dir):
    total={k:set() for k in KINDS}
    if not entry_dir.exists():return total
    for p in sorted(entry_dir.iterdir(), key=lambda x: x.name.casefold()):
        if not p.is_file() or p.name=='metadata.yaml' or p.suffix.lower() not in ('.list','.txt'):continue
        try:merge(total,parse_assets(p.read_text(encoding='utf-8',errors='replace')))
        except OSError:pass
    return total

def build_child_resolution(root, inventory, aggregate_rows):
    """Resolve Aggregate children using repository-local evidence only."""
    ids={x['legacy_id']:x for x in inventory}
    folded=defaultdict(list)
    for ident in ids: folded[ident.casefold()].append(ident)
    results=[]
    for agg in aggregate_rows:
        for child in agg['metadata_children']:
            if child in ids:
                status='exists'; matched_id=child; evidence='index:id'
            elif len(folded.get(child.casefold(),[]))==1:
                status='case_mismatch'; matched_id=folded[child.casefold()][0]; evidence='index:id-casefold'
            else:
                status='missing'; matched_id=None; evidence='no-index-id'
                # Aggregate and its children are siblings under the same category.
                candidate_path=Path(agg['legacy']).parent / child
                if (root/candidate_path).exists():
                    status='path_without_index'; evidence='filesystem:path'
            results.append({'aggregate_id':agg['aggregate_id'],'aggregate_path':agg['legacy'],'child_id':child,'status':status,'matched_id':matched_id,'evidence':evidence})
    counts=defaultdict(int)
    for r in results:counts[r['status']]+=1
    return results,dict(sorted(counts.items()))

def scan(root,out):
    out.mkdir(parents=True,exist_ok=True); index_path=root/'rule/_index.yaml'; entries=flatten_index(load_yaml(index_path,{}) or {})
    inventory=[]; aggregate_rows=[]; asset_index=defaultdict(list); indexed_paths={str(e.get('path')) for e in entries if e.get('path')}; filesystem_paths=set()
    for m in (root/'rule').glob('**/metadata.yaml'):
        rel=m.parent.relative_to(root).as_posix(); parts=m.relative_to(root/'rule').parts
        if parts and parts[0] not in {'category','service','shared'}:filesystem_paths.add(rel)
    for e in entries:
        legacy=str(e.get('path')); d=root/legacy; meta=metadata(d/'metadata.yaml'); a=assets(d)
        for k,vals in a.items():
            for v in vals:asset_index[f'{k}:{v}'].append(legacy)
        idx_type=str(e.get('service_type') or ''); meta_type=str(meta.get('service_type') or '')
        if idx_type in {'service','aggregate'} and meta_type==idx_type:istatus='confirmed';itype=idx_type;v1_id=str(e.get('id')) if idx_type=='service' else None
        elif idx_type in {'service','aggregate'}:istatus='candidate';itype=idx_type;v1_id=str(e.get('id')) if idx_type=='service' else None
        else:istatus='quarantine';itype='unknown';v1_id=None
        def lst(k):return [str(x) for x in meta.get(k,[])] if isinstance(meta.get(k),list) else []
        inventory.append({'legacy':legacy,'legacy_id':str(e.get('id')),'name':str(e.get('name') or e.get('id')),'category':str(e.get('category')),'index_service_type':idx_type,'metadata_service_type':meta_type,'index_domains':int(e.get('domains') or 0),'index_ips':int(e.get('ips') or 0),'path_exists':d.exists(),'metadata_present':bool(meta),'metadata_parent':meta.get('parent'),'metadata_primary_category':meta.get('primary_category'),'metadata_categories':sorted(lst('categories'),key=str.casefold),'metadata_children':sorted(lst('children'),key=str.casefold),'metadata_sources':sorted(lst('sources'),key=str.casefold),'metadata_clients':sorted(lst('clients'),key=str.casefold),'asset_counts':{k:len(a[k]) for k in KINDS},'identity_status':istatus,'identity_type':itype,'v1_service_id':v1_id})
    ids={x['legacy_id'] for x in inventory}
    for x in inventory:
        if x['index_service_type']!='aggregate':continue
        children=set(x['metadata_children']);missing=sorted(children-ids)
        aggregate_rows.append({'legacy':x['legacy'],'aggregate_id':x['legacy_id'],'metadata_children':sorted(children),'missing_child_ids':missing,'child_count':len(children),'relation_status':'clean' if not missing else 'drift'})
    child_resolution,child_counts=build_child_resolution(root,inventory,aggregate_rows)
    duplicate_keys=[{'key':k,'legacy_paths':sorted(set(v))} for k,v in sorted(asset_index.items()) if len(set(v))>1]
    orphan=sorted(filesystem_paths-indexed_paths);missing_paths=sorted(x['legacy'] for x in inventory if not x['path_exists']);missing_meta=sorted(x['legacy'] for x in inventory if not x['metadata_present']);unknown=sum(x['asset_counts']['unknown'] for x in inventory);agg_drift=sorted(x['legacy'] for x in aggregate_rows if x['relation_status']=='drift')
    conflicts=[]
    if orphan:conflicts.append({'id':'ORPH-INDEX-001','type':'filesystem-rule-directory-not-indexed','severity':'high','count':len(orphan),'entries':orphan[:100],'resolution':'Quarantine until mapped or explicitly deprecated.'})
    if missing_paths:conflicts.append({'id':'ORPH-INDEX-002','type':'indexed-entry-path-missing','severity':'blocking','count':len(missing_paths),'entries':missing_paths[:100],'resolution':'Repair index or restore source before promotion.'})
    if missing_meta:conflicts.append({'id':'META-001','type':'missing-metadata','severity':'high','count':len(missing_meta),'entries':missing_meta[:100],'resolution':'Complete metadata evidence before V1 promotion.'})
    if unknown:conflicts.append({'id':'ASSET-UNKNOWN-001','type':'unclassified-legacy-assets','severity':'medium','count':unknown,'resolution':'Review unsupported rule syntax; never silently discard.'})
    if agg_drift:
        detail={x['aggregate_id']:x['missing_child_ids'] for x in aggregate_rows if x['relation_status']=='drift'}
        conflicts.append({'id':'AGG-DRIFT-FINAL-001','type':'aggregate-child-missing','severity':'high','count':len(agg_drift),'entries':agg_drift,'missing_child_ids':detail,'resolution':'Do not synthesize missing services. Resolve metadata/index discrepancy explicitly.'})
    s={'inventory_sha256':hashlib.sha256(index_path.read_bytes()).hexdigest(),'legacy_entries':len(entries),'service_candidates':sum(x['index_service_type']=='service' for x in inventory),'aggregate_candidates':sum(x['index_service_type']=='aggregate' for x in inventory),'metadata_present':sum(x['metadata_present'] for x in inventory),'metadata_missing':len(missing_meta),'confirmed_identity':sum(x['identity_status']=='confirmed' for x in inventory),'candidate_identity':sum(x['identity_status']=='candidate' for x in inventory),'quarantined_identity':sum(x['identity_status']=='quarantine' for x in inventory),'aggregate_relation_drift':len(agg_drift),'aggregate_child_resolution':child_counts,'duplicate_asset_keys':len(duplicate_keys),'orphan_paths':len(orphan),'indexed_missing_paths':len(missing_paths),'unclassified_asset_lines':unknown}
    (out/'LEGACY_SEMANTIC_INVENTORY.json').write_text(json.dumps({'version':1,'phase':'2.3','summary':s,'entries':inventory},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (out/'IDENTITY_RESOLUTION.yaml').write_text(yaml.safe_dump({'version':1,'phase':'2.4','status':'audit','entries':inventory},sort_keys=False,allow_unicode=True),encoding='utf-8')
    (out/'AGGREGATE_RESOLUTION.yaml').write_text(yaml.safe_dump({'version':1,'phase':'2.5','status':'audit','aggregates':aggregate_rows},sort_keys=False,allow_unicode=True),encoding='utf-8')
    (out/'AGGREGATE_CHILD_RESOLUTION.yaml').write_text(yaml.safe_dump({'version':1,'phase':'2.5.1','policy':'repository-local evidence only; no name-based synthesis','summary':child_counts,'results':child_resolution},sort_keys=False,allow_unicode=True),encoding='utf-8')
    (out/'CANONICAL_ASSET_AUDIT.json').write_text(json.dumps({'version':1,'phase':'2.6','normalization':{'rule_syntax':'DOMAIN/DOMAIN-SUFFIX/DOMAIN-KEYWORD/IP-CIDR/URL','semantic_pruning':False},'summary':s,'duplicate_keys':duplicate_keys[:5000]},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (out/'DUPLICATES.yaml').write_text(yaml.safe_dump({'version':1,'phase':'2.7','duplicate_asset_keys':len(duplicate_keys),'duplicates':duplicate_keys[:5000],'policy':'exact canonical equality only'},sort_keys=False,allow_unicode=True),encoding='utf-8')
    (out/'ORPHANS.yaml').write_text(yaml.safe_dump({'version':1,'phase':'2.7','filesystem_rule_dirs_not_in_index':orphan,'indexed_entries_missing_path':missing_paths,'indexed_entries_missing_metadata':missing_meta},sort_keys=False,allow_unicode=True),encoding='utf-8')
    (out/'CONFLICTS_FINAL.yaml').write_text(yaml.safe_dump({'version':1,'phase':'2.7','conflicts':conflicts},sort_keys=False,allow_unicode=True),encoding='utf-8')
    blocking=any(x.get('severity')=='blocking' for x in conflicts);high=any(x.get('severity')=='high' for x in conflicts)
    gate={'version':1,'phase':'2.2-2.7','status':'blocked' if blocking or high else 'audit-complete','promotion_ready':False,'summary':s,'gates':{'2.2_baseline':index_path.exists(),'2.3_184_entries_indexed':len(entries)==184,'2.4_identity_type_resolved':s['quarantined_identity']==0 and s['candidate_identity']==0,'2.5_aggregate_relations_clean':s['aggregate_relation_drift']==0,'2.5.1_aggregate_children_resolved':all(r['status']=='exists' for r in child_resolution),'2.6_no_unclassified_assets':s['unclassified_asset_lines']==0,'2.7_no_blocking_or_high':not blocking and not high}}
    (out/'PHASE2_GATE.yaml').write_text(yaml.safe_dump(gate,sort_keys=False,allow_unicode=True),encoding='utf-8')
    (out/'PHASE2_SUMMARY.md').write_text('# V1 Phase 2.2–2.7 Audit Summary\n\n'+'\n'.join(f'- {k}: {v}' for k,v in s.items())+'\n',encoding='utf-8')
    return gate

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT);ap.add_argument('--out',type=Path,default=DEFAULT_OUT);a=ap.parse_args();r=scan(a.root,a.out);print(yaml.safe_dump(r,sort_keys=False,allow_unicode=True));return 1 if r['status']=='blocked' else 0

if __name__=='__main__':raise SystemExit(main())
