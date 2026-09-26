#!/usr/bin/env python3
"""Icon System V5: deterministic source acquisition, eight-layer registry and gates."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener
import xml.etree.ElementTree as ET
import sys

import yaml

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from scripts.icon_v5_renderers import RENDERERS
from scripts.icon_v5_renderers.common import svg_data_url

POLICY=ROOT/"config/icon_v5.yaml"
OFFICIAL_SITES=ROOT/"config/official_sites.yaml"
DEFAULT_CACHE=ROOT/"assets/icons/v5/source"
VARIANTS=("source_original","glassmorphism","soft_3d","neo_skeuomorphism","minimalist","duotone_line","mbe","y2k")
RENDERER_VERSION="prc-icon-renderer-v5.0.0"

def sha256(data: bytes|str)->str:
    raw=data.encode('utf-8') if isinstance(data,str) else data
    return hashlib.sha256(raw).hexdigest()

def load_yaml(path: Path)->dict:
    value=yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    return value if isinstance(value,dict) else {}

def load_json(path: Path)->dict:
    return json.loads(path.read_text(encoding='utf-8'))

def slug(value: str)->str:
    text=re.sub(r'[^a-zA-Z0-9._-]+','-',str(value).strip().lower())
    return text.strip('-._') or 'unknown'

def discover_services_from_rule_index(rule_index: Path)->list[dict]:
    doc=load_yaml(rule_index); rows=[]; seen=set()
    for item in doc.get('entries') or []:
        if not isinstance(item,dict) or item.get('entity')!='service': continue
        sid=str(item.get('id') or '').strip()
        if not sid: continue
        if sid in seen: raise ValueError(f'duplicate service_id in rule index: {sid}')
        seen.add(sid)
        rows.append({'service_id':sid,'display_name':str(item.get('display_name') or sid),'provider':item.get('provider'),'rule_path':str(item.get('path') or ''),'rule_count':int(item.get('rule_count') or 0)})
    if not rows: raise ValueError('no service entities discovered')
    return sorted(rows,key=lambda x:x['service_id'])

def discover_services_from_ir(ir_path: Path)->list[dict]:
    doc=load_json(ir_path)
    entities=doc.get('entities') or doc.get('entity') or {}
    service_ids=entities.get('services') if isinstance(entities,dict) else []
    views=doc.get('views') or doc.get('view') or {}
    service_views=views.get('services') if isinstance(views,dict) else {}
    memberships=doc.get('memberships') or {}
    rule_map={str(r.get('id')):r for r in (doc.get('rules') or []) if isinstance(r,dict) and r.get('id')}
    if isinstance(service_ids,dict): service_ids=list(service_ids.keys())
    rows=[]; seen=set()
    for sid_raw in service_ids or []:
        sid=str(sid_raw).strip()
        if not sid: continue
        if sid in seen: raise ValueError(f'duplicate service_id in IR: {sid}')
        seen.add(sid)
        view=service_views.get(sid,{}) if isinstance(service_views,dict) else {}
        if not isinstance(view,dict): view={}
        domain_values=[]; rule_ids=memberships.get(sid,[]) if isinstance(memberships,dict) else []
        for rid in rule_ids if isinstance(rule_ids,list) else []:
            rule=rule_map.get(str(rid),{})
            kind=str(rule.get('type') or '').upper(); value=str(rule.get('value') or '').strip()
            if value and kind in {'DOMAIN','DOMAIN_SUFFIX','DOMAIN_KEYWORD'}: domain_values.append(value.lstrip('.'))
        rows.append({'service_id':sid,'display_name':str(view.get('display_name') or view.get('name') or sid),'provider':view.get('provider'),'rule_path':'','domains':domain_values,'rule_count':len(rule_ids) if isinstance(rule_ids,list) else 0})
    if not rows: raise ValueError('IR contains no entities.services')
    return sorted(rows,key=lambda x:x['service_id'])

def discover_services(*,rule_index:Path|None=None,ir_path:Path|None=None)->list[dict]:
    if ir_path is not None: return discover_services_from_ir(ir_path)
    if rule_index is None: raise ValueError('one of --ir or --rule-index is required')
    return discover_services_from_rule_index(rule_index)

def candidate_domains(root: Path,row:dict)->list[tuple[str,int]]:
    path=root/row['rule_path']
    if row.get('domains'):
        return sorted({(str(x).lower().strip('.'),2) for x in row.get('domains') if re.fullmatch(r'[a-z0-9.-]+\.[a-z]{2,}',str(x).lower().strip('.'))},key=lambda x:x[0])[:8]
    if not path.is_file(): return []
    try: doc=load_yaml(path)
    except Exception: doc={}
    if row.get('domains'):
        return sorted({(str(x).lower().strip('.'),2) for x in row.get('domains') if re.fullmatch(r'[a-z0-9.-]+\\.[a-z]{2,}',str(x).lower().strip('.'))},key=lambda x:x[0])[:8]
    tokens=re.findall(r'[a-z0-9]+',str(row['service_id']).lower())+re.findall(r'[a-z0-9]+',str(row['display_name']).lower())
    hosts=set()
    for rule in doc.get('rules') or []:
        if not isinstance(rule,dict): continue
        kind=str(rule.get('type') or '').upper(); value=str(rule.get('value') or '').strip()
        if not value or kind not in {'DOMAIN','DOMAIN_SUFFIX','DOMAIN_KEYWORD'}: continue
        host=value
        if '://' in host: host=urlparse(host).hostname or ''
        host=host.split('/')[0].strip().lower().rstrip('.')
        if not re.fullmatch(r'[a-z0-9.-]+\.[a-z]{2,}',host): continue
        if any(x in host for x in ('cdn.','static.','img.','image.','images.','assets.','download.','update.','api.','gateway.','cloudfront.net','akamaized.net','fastly.net','githubusercontent.com')): continue
        score=2*sum(1 for token in tokens if token and token in host)
        if host.split('.')[0] in {'www','m','mobile','home'}: score+=1
        hosts.add((host,score))
    return sorted(hosts,key=lambda x:(-x[1],x[0]))[:8]

class IconLinkParser(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.links=[]; self.manifest=None
    def handle_starttag(self,tag,attrs):
        if tag.lower()!='link': return
        data={str(k).lower():str(v or '') for k,v in attrs}; rel={x.strip().lower() for x in data.get('rel','').split()}; href=data.get('href','').strip()
        if not href: return
        if 'manifest' in rel: self.manifest=href
        if rel & {'icon','shortcut','apple-touch-icon','apple-touch-icon-precomposed'}:
            self.links.append({'href':href,'priority':0 if 'apple-touch-icon' in rel else (1 if 'icon' in rel else 2),'sizes':data.get('sizes','')})

class LimitedRedirectHandler(HTTPRedirectHandler):
    def __init__(self,max_redirects:int): super().__init__(); self.remaining=max_redirects
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if self.remaining<=0: raise RuntimeError('redirect limit exceeded')
        self.remaining-=1; return super().redirect_request(req,fp,code,msg,headers,newurl)

def fetch_bytes(url:str,*,timeout:int,max_bytes:int,user_agent:str,max_redirects:int)->tuple[bytes,dict]:
    if urlparse(url).scheme.lower()!='https': raise ValueError(f'only https is allowed: {url}')
    opener=build_opener(LimitedRedirectHandler(max_redirects)); req=Request(url,headers={'User-Agent':user_agent,'Accept':'*/*'})
    with opener.open(req,timeout=timeout) as response:
        final_url=response.geturl()
        if urlparse(final_url).scheme.lower()!='https': raise ValueError(f'redirected to non-https: {final_url}')
        clen=response.headers.get('Content-Length')
        if clen and int(clen)>max_bytes: raise ValueError(f'response exceeds {max_bytes} bytes')
        content=response.read(max_bytes+1)
        if len(content)>max_bytes: raise ValueError(f'response exceeds {max_bytes} bytes')
        return content,{'status_code':getattr(response,'status',None),'content_type':response.headers.get('Content-Type'),'content_length':clen,'final_url':final_url,'fetched_at':datetime.now(timezone.utc).isoformat()}

def validate_source(content:bytes,content_type:str|None,source_url:str)->str:
    ctype=(content_type or '').split(';',1)[0].strip().lower()
    if content.lstrip().lower().startswith(b'<svg'): kind='svg'
    elif content.startswith(b'\x89PNG\r\n\x1a\n'): kind='png'
    elif len(content)>=12 and content[:4]==b'RIFF' and content[8:12]==b'WEBP': kind='webp'
    elif content.startswith(b'\x00\x00\x01\x00'): kind='ico'
    else:
        allowed={'image/svg+xml':'svg','image/png':'png','image/webp':'webp','image/x-icon':'ico','image/vnd.microsoft.icon':'ico','image/jpeg':'jpg'}
        if ctype not in allowed: raise ValueError(f'unsupported icon content: {source_url} ({ctype or "unknown"})')
        kind=allowed[ctype]
    if kind=='svg':
        root=ET.fromstring(content.decode('utf-8')); forbidden={'script','foreignObject','iframe','object','embed'}
        for node in root.iter():
            local=node.tag.rsplit('}',1)[-1]
            if local in forbidden: raise ValueError(f'unsafe svg element {local}: {source_url}')
            for attr,value in node.attrib.items():
                if attr.rsplit('}',1)[-1] in {'href','src'}:
                    val=str(value).strip()
                    if val and not val.startswith('data:') and not val.startswith('#'): raise ValueError(f'external svg reference: {source_url}')
    return kind

def select_manifest_icon(base_url:str,data:bytes)->str|None:
    try: doc=json.loads(data.decode('utf-8'))
    except Exception: return None
    candidates=[]
    for item in (doc.get('icons') if isinstance(doc,dict) else None) or []:
        if not isinstance(item,dict) or not item.get('src'): continue
        area=0
        for token in str(item.get('sizes') or '').split():
            if 'x' not in token: continue
            try: a,b=token.lower().split('x',1); area=max(area,int(a)*int(b))
            except Exception: pass
        candidates.append((area,str(item['src'])))
    return urljoin(base_url,sorted(candidates,key=lambda x:(-x[0],x[1]))[0][1]) if candidates else None

def load_cache(cache_dir:Path)->dict:
    path=cache_dir/'cache.json'
    if not path.is_file(): return {}
    try: doc=load_json(path)
    except Exception: return {}
    return doc.get('services') if isinstance(doc.get('services'),dict) else {}

def save_cache(cache_dir:Path,services:dict)->None:
    cache_dir.mkdir(parents=True,exist_ok=True)
    (cache_dir/'cache.json').write_text(json.dumps({'schema':'icon_source_cache_v5','updated_at':datetime.now(timezone.utc).isoformat(),'services':services},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def resolve_source(root:Path,row:dict,official:dict,policy:dict,cache:dict,asset_cache:dict,*,refresh:bool)->dict:
    sid=row['service_id']; cached=None if refresh else cache.get(sid)
    if cached:
        path=ROOT/str(cached.get('path') or '')
        if path.is_file() and sha256(path.read_bytes())==str(cached.get('digest') or '') and cached.get('source_url'):
            content=path.read_bytes(); return {**cached,'status':'ok','content':content,'cached':True}
    homepage=str(official.get(sid) or '').strip(); reason='registered_official' if homepage else None
    if not homepage:
        candidates=candidate_domains(root,row)
        if not candidates or candidates[0][1]<2: return {'status':'hold','reason':'no_high_confidence_official_homepage_candidate'}
        homepage='https://'+candidates[0][0]+'/'; reason='rule_domain_candidate'
    acq=policy['acquisition']
    page,page_headers=fetch_bytes(homepage,timeout=int(acq['timeout_seconds']),max_bytes=int(acq['max_bytes']),user_agent=str(acq['user_agent']),max_redirects=int(acq['max_redirects']))
    parser=IconLinkParser(); parser.feed(page.decode('utf-8',errors='ignore'))
    icon_url=None
    for link in sorted(parser.links,key=lambda x:(x['priority'],x['sizes'] or '',x['href'])):
        icon_url=urljoin(page_headers['final_url'],link['href'])
        if icon_url: break
    if not icon_url and parser.manifest:
        manifest_url=urljoin(page_headers['final_url'],parser.manifest)
        manifest,_=fetch_bytes(manifest_url,timeout=int(acq['timeout_seconds']),max_bytes=int(acq['max_bytes']),user_agent=str(acq['user_agent']),max_redirects=int(acq['max_redirects']))
        icon_url=select_manifest_icon(page_headers['final_url'],manifest)
    if not icon_url: icon_url=urljoin(page_headers['final_url'],'/favicon.ico')
    shared=asset_cache.get(icon_url)
    if shared:
        icon,icon_headers=shared
    else:
        icon,icon_headers=fetch_bytes(icon_url,timeout=int(acq['timeout_seconds']),max_bytes=int(acq['max_bytes']),user_agent=str(acq['user_agent']),max_redirects=int(acq['max_redirects']))
        asset_cache[icon_url]=(icon,icon_headers)
    kind=validate_source(icon,icon_headers.get('content_type'),icon_headers['final_url'])
    return {'status':'ok','content':icon,'cached':False,'service_id':sid,'homepage_url':page_headers['final_url'],'source_url':icon_headers['final_url'],'source_kind':kind,'content_type':icon_headers.get('content_type'),'source_digest':sha256(icon),'resolution_reason':reason,'http_status':icon_headers.get('status_code'),'content_length':icon_headers.get('content_length'),'fetched_at':icon_headers.get('fetched_at')}

def persist_cache(cache_dir:Path,row:dict,result:dict)->dict:
    ext={'svg':'svg','png':'png','webp':'webp','ico':'ico','jpg':'jpg'}[result['source_kind']]; path=cache_dir/(slug(row['service_id'])+'.'+ext); path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(result['content'])
    return {'path':str(path.relative_to(ROOT)),'source_url':result['source_url'],'homepage_url':result['homepage_url'],'source_kind':result['source_kind'],'digest':result['source_digest'],'content_type':result.get('content_type'),'http_status':result.get('http_status'),'content_length':result.get('content_length'),'fetched_at':result.get('fetched_at'),'resolution_reason':result.get('resolution_reason')}

def render_pngs(svg:str,out_root:Path,service_id:str,variant:str,sizes:list[int])->dict[str,str]:
    import cairosvg
    paths={}
    for size in sizes:
        path=out_root/'png'/str(size)/variant/(slug(service_id)+'.png'); path.parent.mkdir(parents=True,exist_ok=True)
        cairosvg.svg2png(bytestring=svg.encode('utf-8'),write_to=str(path),output_width=size,output_height=size); paths[str(size)]=str(path.relative_to(out_root))
    return paths

def build(args:argparse.Namespace)->int:
    policy,official=load_yaml(POLICY),load_yaml(OFFICIAL_SITES)
    run_dir=Path(args.run_dir) if args.run_dir else None
    rule_index=Path(args.rule_index) if args.rule_index else None
    ir_path=Path(args.ir) if args.ir else None
    if run_dir:
        if rule_index or ir_path: raise ValueError('--run-dir cannot be combined with --rule-index or --ir')
        ir_path=run_dir/'ir'/'ir.json'
    entries=discover_services(rule_index=rule_index,ir_path=ir_path)
    lineage={'run_id':str(args.run_id or ''),'snapshot_id':str(args.snapshot_id or ''),'ir_digest':str(args.ir_digest or '')}
    if run_dir:
        run_manifest=load_json(run_dir/'run_manifest.json') if (run_dir/'run_manifest.json').is_file() else {}
        ir_manifest=load_json(run_dir/'ir'/'manifest.json') if (run_dir/'ir'/'manifest.json').is_file() else {}
        lineage['run_id']=lineage['run_id'] or str(run_manifest.get('run_id') or '')
        lineage['snapshot_id']=lineage['snapshot_id'] or str(run_manifest.get('snapshot_id') or '')
        lineage['ir_digest']=lineage['ir_digest'] or str(ir_manifest.get('ir_digest') or '')
    if rule_index:
        doc=load_yaml(rule_index); lineage['run_id']=lineage['run_id'] or str(doc.get('run_id') or ''); lineage['ir_digest']=lineage['ir_digest'] or str(doc.get('ir_digest') or '')
    if ir_path:
        doc=load_json(ir_path); meta=doc.get('metadata') if isinstance(doc.get('metadata'),dict) else {}; lineage['run_id']=lineage['run_id'] or str(doc.get('run_id') or meta.get('run_id') or ''); lineage['snapshot_id']=lineage['snapshot_id'] or str(doc.get('snapshot_id') or meta.get('snapshot_id') or ''); lineage['ir_digest']=lineage['ir_digest'] or str(doc.get('ir_digest') or meta.get('ir_digest') or '')
    if args.strict and not all(lineage.values()): print(json.dumps({'status':'blocked','reason':'strict build requires run_id, snapshot_id and ir_digest'},ensure_ascii=False)); return 1
    cache_dir=Path(args.cache_dir) if args.cache_dir else DEFAULT_CACHE; cache=load_cache(cache_dir); asset_cache={}; out=Path(args.out); out.mkdir(parents=True,exist_ok=True); results=[]
    for row in entries:
        try:
            result=resolve_source(ROOT,row,official,policy,cache,asset_cache,refresh=args.refresh)
            if result.get('status')!='ok':
                results.append({**row,'icon_identity':f"service:{row['service_id']}",'source':{'origin':'hold','digest':None,'reason':result.get('reason')},'variants':{},'lineage':{**lineage,'source_digest':None,'renderer_version':RENDERER_VERSION},'release_eligible':False}); continue
            source=result if result.get('cached') else persist_cache(cache_dir,row,result); cache[row['service_id']]=source
            source_path=ROOT/source['path']; content=source_path.read_bytes(); href=svg_data_url(content,source['source_kind']); sid=slug(row['service_id'])
            normalized=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><image href="{href}" x="96" y="96" width="320" height="320" preserveAspectRatio="xMidYMid meet"/></svg>'
            np=out/'normalized'/(sid+'.svg'); np.parent.mkdir(parents=True,exist_ok=True); np.write_text(normalized,encoding='utf-8')
            variants={'source_original':{'path':str(source_path.relative_to(ROOT)),'digest':source['digest'],'source_kind':source['source_kind']}}
            for style,renderer in RENDERERS.items():
                svg=renderer(href,row['display_name']); sp=out/'styles'/style/(sid+'.svg'); sp.parent.mkdir(parents=True,exist_ok=True); sp.write_text(svg,encoding='utf-8')
                variants[style]={'path':str(sp.relative_to(out)),'digest':sha256(svg),'png':render_pngs(svg,out,row['service_id'],style,list(policy['render']['png_sizes']))}
            results.append({**row,'icon_identity':f"service:{row['service_id']}",'source':{'origin':'official_registered' if source['resolution_reason']=='registered_official' else 'official_discovered','homepage_url':source['homepage_url'],'source_url':source['source_url'],'content_type':source.get('content_type'),'digest':source['digest'],'rights_basis':'official_site_asset','redistribution_status':'review','resolution_reason':source.get('resolution_reason'),'http_status':source.get('http_status'),'content_length':source.get('content_length'),'fetched_at':source.get('fetched_at')},'normalized':{'path':str(np.relative_to(out)),'digest':sha256(normalized)},'variants':variants,'lineage':{**lineage,'source_digest':source['digest'],'renderer_version':RENDERER_VERSION},'release_eligible':True})
        except Exception as exc:
            results.append({**row,'icon_identity':f"service:{row['service_id']}",'source':{'origin':'hold','digest':None,'reason':f'{type(exc).__name__}: {exc}'},'variants':{},'lineage':{**lineage,'source_digest':None,'renderer_version':RENDERER_VERSION},'release_eligible':False})
    save_cache(cache_dir,cache); results.sort(key=lambda x:x['service_id']); complete=sum(1 for r in results if r.get('release_eligible') and len(r.get('variants',{}))==8); missing=[r['service_id'] for r in results if not (r.get('release_eligible') and len(r.get('variants',{}))==8)]
    registry={'schema':'icon_registry_v5','version':5,'renderer_version':RENDERER_VERSION,'generated_at':datetime.now(timezone.utc).isoformat(),**lineage,'service_universe':{'source':str(ir_path or rule_index),'count':len(entries)},'variants':list(VARIANTS),'entries':results,'coverage':{'service_count':len(entries),'icon_identity_count':sum(1 for r in results if r.get('source',{}).get('digest')),'complete_8_of_8':complete,'missing':missing,'orphans':[]},'acquisition':{'network_policy':'one_asset_fetch_per_run','persistent_cache':str(cache_dir)}}
    (out/'registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); (out/'release-pointer.json').write_text(json.dumps({'schema':'icon_release_pointer_v5','status':'candidate' if missing else 'rc_ready','registry':'registry.json',**lineage,'renderer_version':RENDERER_VERSION},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'blocked' if args.strict and missing else 'ok','service_count':len(entries),'complete_8_of_8':complete,'missing':missing,'out':str(out)},ensure_ascii=False)); return 1 if args.strict and missing else 0

def gate(args:argparse.Namespace)->int:
    registry_path=Path(args.registry); registry=load_json(registry_path); errors=[]
    if registry.get('schema')!='icon_registry_v5' or registry.get('variants')!=list(VARIANTS): errors.append('V5 registry contract mismatch')
    expected=None
    registry_ids_list=[str(r.get('service_id') or '') for r in registry.get('entries') or []]
    if len(registry_ids_list)!=len(set(registry_ids_list)): errors.append('duplicate service_id in registry')
    identity_ids=[str(r.get('icon_identity') or '') for r in registry.get('entries') or [] if r.get('icon_identity')]
    if len(identity_ids)!=len(set(identity_ids)): errors.append('duplicate icon_identity in registry')
    if args.rule_index or args.ir:
        expected={r['service_id'] for r in discover_services(rule_index=Path(args.rule_index) if args.rule_index else None,ir_path=Path(args.ir) if args.ir else None)}; actual={str(r.get('service_id') or '') for r in registry.get('entries') or []}
        if actual!=expected: errors.append(f'service coverage mismatch: missing={sorted(expected-actual)} extra={sorted(actual-expected)}')
    for row in registry.get('entries') or []:
        sid=row.get('service_id')
        if row.get('release_eligible') is not True:
            if args.strict: errors.append(f'{sid}: not release eligible')
            continue
        source=row.get('source') or {}
        if not re.fullmatch(r'[0-9a-f]{64}',str(source.get('digest') or '')): errors.append(f'{sid}: invalid source digest')
        for key in VARIANTS:
            item=(row.get('variants') or {}).get(key)
            if not item: errors.append(f'{sid}:{key}: missing variant'); continue
            path=ROOT/str(item.get('path') or '') if key=='source_original' else registry_path.parent/str(item.get('path') or '')
            if not path.is_file(): errors.append(f'{sid}:{key}: missing file'); continue
            if sha256(path.read_bytes())!=str(item.get('digest') or ''): errors.append(f'{sid}:{key}: digest mismatch')
            if key!='source_original':
                try:
                    root=ET.fromstring(path.read_text(encoding='utf-8'))
                    if root.tag.rsplit('}',1)[-1]!='svg': raise ValueError('not svg')
                except Exception as exc: errors.append(f'{sid}:{key}: invalid svg: {exc}')
                for size in (64,128,256):
                    png=registry_path.parent/str((item.get('png') or {}).get(str(size)) or '')
                    if args.strict and (not png.is_file() or png.stat().st_size<=100): errors.append(f'{sid}:{key}: missing PNG {size}')
        lin=row.get('lineage') or {}
        if args.strict:
            for field in ('run_id','snapshot_id','ir_digest','source_digest','renderer_version'):
                if not str(lin.get(field) or '').strip(): errors.append(f'{sid}: missing lineage {field}')
            if not str(source.get('rights_basis') or '').strip(): errors.append(f'{sid}: missing rights_basis')
    coverage=registry.get('coverage') or {}
    if args.strict and int(coverage.get('complete_8_of_8') or 0)!=int(coverage.get('service_count') or 0): errors.append('8/8 coverage incomplete')
    report={'schema':'icon_v5_gate_v1','status':'PASS' if not errors else 'FAIL','errors':errors}; (registry_path.parent/'gate.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(report,ensure_ascii=False)); return 0 if not errors else 1

def discover(args:argparse.Namespace)->int:
    rows=discover_services(rule_index=Path(args.rule_index) if args.rule_index else None,ir_path=Path(args.ir) if args.ir else None); out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps({'schema':'icon_service_discovery_v5','run_id':args.run_id,'snapshot_id':args.snapshot_id,'ir_digest':args.ir_digest,'service_count':len(rows),'services':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'status':'ok','service_count':len(rows),'out':str(out)},ensure_ascii=False)); return 0

def contract()->int:
    policy=load_yaml(POLICY)
    if policy.get('version')!=5 or tuple(policy.get('variants') or [])!=VARIANTS or set(RENDERERS)!=set(VARIANTS[1:]): raise SystemExit('icon_v5 contract mismatch')
    print(json.dumps({'status':'PASS','schema':'icon_v5_contract_v1','variants':list(VARIANTS),'renderer_version':RENDERER_VERSION,'renderer_modules':sorted(RENDERERS)},ensure_ascii=False)); return 0

def main()->int:
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command',required=True); sub.add_parser('contract')
    for command in ('discover','build'):
        p=sub.add_parser(command); p.add_argument('--rule-index'); p.add_argument('--ir'); p.add_argument('--run-dir'); p.add_argument('--out',required=True)
        if command=='discover': p.add_argument('--run-id'); p.add_argument('--snapshot-id'); p.add_argument('--ir-digest')
        else: p.add_argument('--cache-dir'); p.add_argument('--run-id'); p.add_argument('--snapshot-id'); p.add_argument('--ir-digest'); p.add_argument('--refresh',action='store_true'); p.add_argument('--strict',action='store_true')
    p=sub.add_parser('gate'); p.add_argument('--registry',required=True); p.add_argument('--rule-index'); p.add_argument('--ir'); p.add_argument('--strict',action='store_true')
    args=ap.parse_args()
    if args.command=='contract': return contract()
    if args.command=='discover':
        if sum(bool(x) for x in (args.rule_index,args.ir,args.run_dir))!=1: ap.error('discover requires exactly one of --rule-index, --ir or --run-dir')
        return discover(args)
    if args.command=='build':
        if sum(bool(x) for x in (args.rule_index,args.ir,args.run_dir))!=1: ap.error('build requires exactly one of --rule-index, --ir or --run-dir')
        return build(args)
    return gate(args)

if __name__=='__main__': raise SystemExit(main())