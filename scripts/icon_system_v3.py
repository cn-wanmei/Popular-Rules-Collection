#!/usr/bin/env python3
from __future__ import annotations
import argparse,base64,hashlib,html,json,math,os,re
import xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
MAN=ROOT/"assets/icons/manifest.yaml"
CFG=ROOT/"config/icon_v3.yaml"
SRC=ROOT/"assets/icons/source"
STYLES=("official","gradient","liquid_glass","soft_3d","minimal","dark_neon","monochrome")
CLIENTS=("mihomo","singbox","surge","shadowrocket","quantumultx","egern","loon")
STRATEGY={"direct":"Direct","proxy":"Proxy","reject":"Reject","auto":"Auto","fallback":"Fallback","urltest":"URL Test","loadbalance":"Load Balance","final":"Final","match":"Match","dns":"DNS","global":"Global","select":"Select","private":"Private","lan":"LAN","china":"China","network":"Network"}

def yload(p):
    v=yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return v if isinstance(v,dict) else {}

def slug(s):
    return re.sub(r"[^a-zA-Z0-9._-]+","-",str(s).strip().lower()).strip("-._") or "unknown"

def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def color(meta):
    brand=meta.get("brand") or {}; source=meta.get("source") or {}
    for v in (brand.get("display_color"),brand.get("color"),brand.get("source_color"),source.get("color")):
        if isinstance(v,str):
            v="#"+v.lstrip("#")
            if re.fullmatch(r"#[0-9a-fA-F]{6}",v): return v
    return "#64748B"

def tier(meta):
    s=meta.get("source") or {}
    p=str(s.get("provider") or ""); q=str(s.get("provenance") or "")
    if q=="official-colors" or p=="project-brand": return "official"
    if p in {"simple-icons","datatrans/payment-logos"} or q=="third_party": return "trusted_third_party"
    if p=="project" or q.startswith("project"): return "project_semantic"
    return "unknown"

def base_svg(meta,key):
    rel=((meta.get("files") or {}).get("svg") or f"source/{key}.svg")
    p=ROOT/"assets/icons"/rel
    if not p.is_file():
        p=SRC/f"{key}.svg"
        if p.is_file(): rel=p.relative_to(ROOT).as_posix()
    if not p.is_file(): raise FileNotFoundError(f"{key}: missing SVG {rel}")
    txt=p.read_text(encoding="utf-8"); root=ET.fromstring(txt)
    if root.tag.rsplit("}",1)[-1]!="svg" or not root.attrib.get("viewBox"): raise ValueError(f"{key}: invalid source SVG")
    return txt,rel,sha(txt)

def semantic(title,glyph):
    key=str(glyph).lower().strip()
    shapes={
        "direct":'<path d="M30 64h49" stroke="#16A34A" stroke-width="7" stroke-linecap="round"/><path d="M66 40l24 24-24 24" fill="none" stroke="#16A34A" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
        "proxy":'<circle cx="40" cy="46" r="10" fill="#2563EB"/><circle cx="88" cy="82" r="10" fill="#2563EB"/><path d="M47 52l34 24" stroke="#2563EB" stroke-width="6" stroke-linecap="round"/>',
        "reject":'<path d="M39 39l50 50M89 39L39 89" stroke="#DC2626" stroke-width="8" stroke-linecap="round"/>',
        "auto":'<path d="M64 29l8 25 25 10-25 9-8 26-8-26-25-9 25-10z" fill="#7C3AED"/>',
        "fallback":'<path d="M88 44H48c-12 0-20 8-20 20s8 20 20 20h25" fill="none" stroke="#D97706" stroke-width="7" stroke-linecap="round"/><path d="M64 67l24 17-24 17" transform="translate(0 -17)" fill="none" stroke="#D97706" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
        "urltest":'<path d="M30 78l12-18 12 11 14-25 17 18" fill="none" stroke="#0891B2" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><circle cx="88" cy="84" r="9" fill="#10B981"/>',
        "loadbalance":'<path d="M64 31v22M64 53L39 79M64 53l25 26" stroke="#4F46E5" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><circle cx="64" cy="27" r="8" fill="#4F46E5"/><circle cx="38" cy="83" r="8" fill="#4F46E5"/><circle cx="90" cy="83" r="8" fill="#4F46E5"/>',
        "final":'<circle cx="64" cy="64" r="34" fill="none" stroke="#0F766E" stroke-width="7"/><path d="M46 64l12 12 25-28" fill="none" stroke="#0F766E" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
        "match":'<circle cx="64" cy="64" r="31" fill="none" stroke="#7C3AED" stroke-width="7"/><circle cx="64" cy="64" r="9" fill="#7C3AED"/><path d="M64 22v14M64 92v14M22 64h14M92 64h14" stroke="#7C3AED" stroke-width="6" stroke-linecap="round"/>',
        "dns":'<circle cx="64" cy="64" r="35" fill="none" stroke="#0891B2" stroke-width="6"/><path d="M29 64h70M64 29c10 10 15 21 15 35S74 89 64 99M64 29C54 39 49 50 49 64s5 25 15 35" fill="none" stroke="#0891B2" stroke-width="5"/>',
        "global":'<circle cx="64" cy="64" r="35" fill="none" stroke="#475569" stroke-width="6"/><path d="M29 64h70M64 29c10 10 15 21 15 35S74 89 64 99M64 29C54 39 49 50 49 64s5 25 15 35" fill="none" stroke="#475569" stroke-width="5"/>',
        "select":'<rect x="30" y="33" width="68" height="10" rx="5" fill="#2563EB"/><rect x="30" y="59" width="48" height="10" rx="5" fill="#2563EB"/><rect x="30" y="85" width="58" height="10" rx="5" fill="#2563EB"/>',
        "private":'<rect x="38" y="54" width="52" height="38" rx="8" fill="#334155"/><path d="M48 54V45c0-9 7-16 16-16s16 7 16 16v9" fill="none" stroke="#334155" stroke-width="7"/><circle cx="64" cy="73" r="6" fill="#FFFFFF"/>',
        "lan":'<path d="M64 36v17M64 53L42 76M64 53l22 23" stroke="#059669" stroke-width="7" stroke-linecap="round"/><circle cx="64" cy="31" r="9" fill="#059669"/><circle cx="40" cy="82" r="9" fill="#059669"/><circle cx="88" cy="82" r="9" fill="#059669"/>',
        "china":'<path d="M42 39h30l16 16-11 34-31 2-13-24z" fill="#DC2626" opacity=".9"/><circle cx="72" cy="48" r="7" fill="#FFFFFF"/>',
        "network":'<circle cx="42" cy="43" r="9" fill="#2563EB"/><circle cx="86" cy="43" r="9" fill="#2563EB"/><circle cx="64" cy="86" r="9" fill="#2563EB"/><path d="M49 48l9 28M79 48l-9 28M51 43h28" stroke="#2563EB" stroke-width="6" stroke-linecap="round"/>'
    }
    body=shapes.get(key,f'<text x="64" y="64" text-anchor="middle" dominant-baseline="middle" font-family="system-ui,sans-serif" font-size="28" font-weight="800" fill="#0F172A">{html.escape(str(glyph)[:3].upper())}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><title>{html.escape(title)}</title><rect x="12" y="12" width="104" height="104" rx="30" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>{body}</svg>'

def render(base,title,style,c):
    root=ET.fromstring(base); vb=root.attrib.get("viewBox","0 0 24 24")
    inner="".join(ET.tostring(x,encoding="unicode") for x in list(root))
    defs=bg=filt=""
    if style=="gradient":
        defs=f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}"/><stop offset=".55" stop-color="#FFFFFF" stop-opacity=".84"/><stop offset="1" stop-color="{c}" stop-opacity=".62"/></linearGradient></defs>'
        bg='<rect x="8" y="8" width="112" height="112" rx="34" fill="url(#g)"/><circle cx="93" cy="34" r="23" fill="#FFFFFF" opacity=".18"/>'
    elif style=="liquid_glass":
        defs='<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".9"/><stop offset="1" stop-color="#CBD5E1" stop-opacity=".2"/></linearGradient><filter id="b"><feGaussianBlur stdDeviation="8"/></filter></defs>'
        bg=f'<rect x="8" y="8" width="112" height="112" rx="34" fill="#F8FAFC" opacity=".4"/><circle cx="42" cy="40" r="34" fill="{c}" opacity=".28" filter="url(#b)"/><rect x="14" y="14" width="100" height="100" rx="30" fill="url(#g)" stroke="#FFFFFF" stroke-opacity=".7"/>'
    elif style=="soft_3d":
        defs='<defs><filter id="s" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#0F172A" flood-opacity=".18"/></filter></defs>'
        bg=f'<rect x="11" y="11" width="106" height="106" rx="31" fill="#FFFFFF" filter="url(#s)"/><rect x="15" y="15" width="98" height="98" rx="29" fill="{c}" opacity=".09"/>'
    elif style=="minimal":
        bg=f'<rect x="12" y="12" width="104" height="104" rx="29" fill="#FFFFFF" stroke="{c}" stroke-opacity=".18" stroke-width="1.5"/>'
    elif style=="dark_neon":
        defs='<defs><filter id="n" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
        bg=f'<rect x="7" y="7" width="114" height="114" rx="34" fill="#08111F"/><rect x="16" y="16" width="96" height="96" rx="28" fill="#0D1726" stroke="{c}" stroke-opacity=".35"/><circle cx="64" cy="64" r="45" fill="{c}" opacity=".14" filter="url(#n)"/>'
        filt=' filter="url(#n)"'
    elif style=="monochrome":
        defs='<defs><filter id="m"><feColorMatrix type="saturate" values="0"/></filter></defs>'
        bg='<rect x="12" y="12" width="104" height="104" rx="29" fill="#FFFFFF" stroke="#0F172A" stroke-opacity=".14"/>'
        filt=' filter="url(#m)"'
    nested=f'<svg x="25" y="25" width="78" height="78" viewBox="{vb}" preserveAspectRatio="xMidYMid meet"{filt}>{inner}</svg>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" role="img"><title>{html.escape(title)} — {style}</title>{defs}{bg}{nested}</svg>'

def entries(man,cfg):
    icons=man.get("icons") or {}
    mapping=man.get("service_icon_map") or {}
    out=[]
    seen=set()

    def add(sid,key,meta,role):
        sid=str(sid).strip()
        key=str(key).strip()
        if not sid or sid in seen:
            return
        seen.add(sid)
        out.append({
            "service_id":sid,
            "icon_identity":("brand." if role=="service" else "semantic.")+slug(key),
            "role":role,
            "canonical_name":str(meta.get("name") or sid),
            "meta":meta,
            "icon_key":key,
        })

    # V1 manifest uses service_ids inside each icon entry; prefer this as the identity source.
    for key,meta in sorted(icons.items()):
        if not isinstance(meta,dict):
            continue
        t=str(meta.get("type") or "").lower()
        ns=str(meta.get("namespace") or "").lower()
        role="strategy" if t in {"policy","strategy"} or ns=="policy" or key in STRATEGY else ("special" if t in {"dataset","network"} or ns in {"dataset","network"} else "service")
        service_ids=meta.get("service_ids") or []
        if isinstance(service_ids,str):
            service_ids=[service_ids]
        for sid in service_ids:
            add(sid,key,meta,role)

    # Keep an explicit service_icon_map authoritative where present.
    for sid,key in sorted(mapping.items()):
        meta=icons.get(key) or {}
        if not isinstance(meta,dict):
            meta={}
        t=str(meta.get("type") or "").lower()
        ns=str(meta.get("namespace") or "").lower()
        role="strategy" if t in {"policy","strategy"} or ns=="policy" or key in STRATEGY else ("special" if t in {"dataset","network"} or ns in {"dataset","network"} else "service")
        add(sid,key,meta,role)
    for key,label in STRATEGY.items():
        sid="strategy."+slug(key)
        if sid not in present: out.append({"service_id":sid,"icon_identity":sid,"role":"strategy","canonical_name":label,"meta":{},"icon_key":key})
    for key,glyph in ((cfg.get("semantic_sets") or {}).get("client_policy") or {}).items():
        sid="client-policy."+slug(key)
        out.append({"service_id":sid,"icon_identity":sid,"role":"client_policy","canonical_name":str(key),"meta":{},"icon_key":str(glyph)})
    return out

def sheet(root,style,rows,name="master-all"):
    cols=10; cw,ch=154,152; rowsn=max(1,math.ceil(len(rows)/cols))
    w=28+cols*cw; h=80+rowsn*ch; p=root/"previews"/style/f"{name}.svg"; p.parent.mkdir(parents=True,exist_ok=True)
    z=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="#F1F5F9"/><text x="28" y="32" font-family="system-ui,sans-serif" font-size="22" font-weight="800" fill="#0F172A">{html.escape(style)} · {html.escape(name)}</text>']
    for i,x in enumerate(rows):
        r,c=divmod(i,cols); xx=14+c*cw; yy=58+r*ch; svg=(root/x["variant"]["path"]).read_text(); b=base64.b64encode(svg.encode()).decode()
        z += [f'<rect x="{xx}" y="{yy}" width="144" height="142" rx="18" fill="#FFFFFF" stroke="#CBD5E1"/>',f'<image x="{xx+31}" y="{yy+10}" width="82" height="82" href="data:image/svg+xml;base64,{b}"/>',f'<text x="{xx+72}" y="{yy+112}" text-anchor="middle" font-family="system-ui,sans-serif" font-size="10" font-weight="700" fill="#0F172A">{html.escape(x["canonical_name"][:20])}</text>',f'<text x="{xx+72}" y="{yy+128}" text-anchor="middle" font-family="ui-monospace,monospace" font-size="7" fill="#64748B">{html.escape(x["service_id"][:20])}</text>']
    z.append("</svg>"); p.write_text("".join(z),encoding="utf-8"); return p

def legibility(root,style,rows,size):
    cols=14; cell=max(62,size+28); h=62+max(1,math.ceil(len(rows)/cols))*(cell+22); w=24+cols*cell; p=root/"previews"/style/f"legibility-{size}.svg"; p.parent.mkdir(parents=True,exist_ok=True)
    z=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="#FFFFFF"/><text x="24" y="28" font-family="system-ui,sans-serif" font-size="16" font-weight="800" fill="#0F172A">{style} · {size}px</text>']
    for i,x in enumerate(rows):
        r,c=divmod(i,cols); xx=8+c*cell; yy=40+r*(cell+22); svg=(root/x["variant"]["path"]).read_text(); b=base64.b64encode(svg.encode()).decode()
        z += [f'<image x="{xx+10}" y="{yy}" width="{size}" height="{size}" href="data:image/svg+xml;base64,{b}"/>',f'<text x="{xx+cell/2}" y="{yy+size+14}" text-anchor="middle" font-family="ui-monospace,monospace" font-size="7" fill="#64748B">{html.escape(x["service_id"][:11])}</text>']
    z.append("</svg>"); p.write_text("".join(z),encoding="utf-8"); return p

def build(out):
    cfg=yload(CFG); man=yload(MAN); official_sites=yload(ROOT/"config/official_sites.yaml"); es=entries(man,cfg); out.mkdir(parents=True,exist_ok=True); cache={}; regs=[]; rows={s:[] for s in STYLES}
    for e in es:
        meta_status=str(e["meta"].get("status") or "").lower()
        release_eligible = e["role"] != "service" or meta_status in {"verified","sourced","approved","active"}
        official_reference=official_sites.get(e["icon_key"]) or official_sites.get(e["service_id"])
        if e["role"] in {"strategy","client_policy"}:
            base=semantic(e["canonical_name"],e["icon_key"]); src_path="generated:semantic"; src_digest=sha(base); provider="project-semantic"; stier="project_semantic"; surl=None
        else:
            base,src_path,src_digest=base_svg(e["meta"],e["icon_key"]); src=e["meta"].get("source") or {}; provider=str(src.get("provider") or "unknown"); stier=tier(e["meta"]); surl=src.get("url")
        vs={}
        variant_root=out/"variants" if release_eligible else out/"quarantine"/"variants"
        for style in STYLES:
            p=variant_root/style/f"{slug(e["service_id"])}.svg"; p.parent.mkdir(parents=True,exist_ok=True); txt=render(base,e["canonical_name"],style,color(e["meta"])); p.write_text(txt,encoding="utf-8")
            vs[style]={"asset_id":f"icon.{slug(e['service_id'])}.{style}","path":p.relative_to(out).as_posix(),"digest":sha(txt),"style":style,"source_asset_digest":src_digest,"source_tier":stier,"source_provider":provider,"source_url":surl,"source_path":src_path}
            rows[style].append({"service_id":e["service_id"],"canonical_name":e["canonical_name"],"variant":vs[style],"group":e["role"]})
        regs.append({"service_id":e["service_id"],"icon_identity":e["icon_identity"],"role":e["role"],"canonical_name":e["canonical_name"],"release_eligible":release_eligible,"base_asset":{"asset_id":vs["official"]["asset_id"],"path":src_path,"source_tier":stier,"source_provider":provider,"source_url":surl,"official_reference":official_reference,"license":e["meta"].get("license") or {},"digest":src_digest},"variants":vs,"quality":{"identity":"pass" if release_eligible or e["role"]!="service" else "hold","integrity":"pass","visual":"pending_review","legibility":"pending_review","license":"review" if e["role"]=="service" else "pass","regression":"baseline_pending"},"provenance":{"source_provider":provider,"source_path":src_path,"source_url":surl,"official_reference":official_reference,"source_tier":stier,"source_asset_digest":src_digest,"license":e["meta"].get("license") or {},"renderer_version":"3.0.0","workspace_commit":os.environ.get("GITHUB_SHA","local"),"generation_run_id":os.environ.get("GITHUB_RUN_ID","local")}})
    for style in STYLES:
        sheet(out,style,rows[style])
        for role in sorted({x["group"] for x in rows[style]}): sheet(out,style,[x for x in rows[style] if x["group"]==role],f"role-{slug(role)}")
        for size in (24,32,48): legibility(out,style,rows[style],size)
    cc=cfg.get("clients") or {}
    for client in CLIENTS:
        c=cc.get(client) or {}; preferred=str(c.get("preferred_style") or "minimal"); size=int(c.get("preferred_size") or 256); ix={}
        for r in regs:
            if not r.get("release_eligible", True):
                continue
            p=out/"clients"/client/str(size)/f'{slug(r["service_id"])}.png'; p.parent.mkdir(parents=True,exist_ok=True)
            try:
                import cairosvg
            except ImportError as exc:
                raise SystemExit("cairosvg is required for client PNG generation") from exc
            cairosvg.svg2png(bytes=(out/r["variants"][preferred]["path"]).read_bytes(),write_to=str(p),output_width=size,output_height=size)
            ix[r["service_id"]]={"identity":r["icon_identity"],"role":r["role"],"style":preferred,"size":size,"format":"png","path":p.relative_to(out).as_posix(),"digest":hashlib.sha256(p.read_bytes()).hexdigest()}
        q=out/"index"/"clients"/f"{client}.json"; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps({"schema":"icon_client_index_v3","client":client,"entries":ix},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    now=datetime.now(timezone.utc).isoformat()
    reg={"schema":"icon_registry_v3","version":3,"renderer_version":"3.0.0","generated_at":now,"workspace_commit":os.environ.get("GITHUB_SHA","local"),"styles":list(STYLES),"clients":list(CLIENTS),"entries":regs}
    (out/"registry.yaml").write_text(yaml.dump(reg,allow_unicode=True,sort_keys=False,width=160),encoding="utf-8")
    (out/"index"/"icons.json").write_text(json.dumps({"schema":"icon_index_v3","generated_at":now,"styles":list(STYLES),"entries":regs},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    review={"schema":"icon_review_manifest_v1","generated_at":now,"renderer_version":"3.0.0","style_count":7,"client_count":7,"entry_count":len(regs),"master_previews":[f"previews/{s}/master-all.svg" for s in STYLES],"legibility_previews":[f"previews/{s}/legibility-{n}.svg" for s in STYLES for n in (24,32,48)],"role_sheet_policy":"one per role/style"}
    (out/"icon-review-manifest.json").write_text(json.dumps(review,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (out/"manifest.json").write_text(json.dumps({"schema":"icon_v3_build_manifest_v1","version":3,"generated_at":now,"renderer_version":"3.0.0","workspace_commit":os.environ.get("GITHUB_SHA","local"),"styles":list(STYLES),"clients":list(CLIENTS),"entries":regs},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def qa(out):
    d=json.loads((out/"manifest.json").read_text(encoding="utf-8")); errors=[]
    if d.get("styles") != list(STYLES): errors.append("style contract mismatch")
    if d.get("clients") != list(CLIENTS): errors.append("client contract mismatch")
    for e in d.get("entries",[]):
        for style in STYLES:
            p=out/e["variants"][style]["path"]
            try: ET.fromstring(p.read_text(encoding="utf-8"))
            except Exception as exc: errors.append(f'{e["service_id"]}:{style}:{exc}')
    q={"schema":"icon_v3_qa_v1","status":"PASS" if not errors else "FAIL","entry_count":len(d.get("entries",[])),"errors":errors}
    (out/"reports").mkdir(exist_ok=True); (out/"reports"/"qa.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return q

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("command",choices=("build","qa","all")); ap.add_argument("--out",type=Path,default=Path("build/icon-v3")); a=ap.parse_args()
    if a.command in {"build","all"}: build(a.out)
    result=qa(a.out); print(json.dumps(result,ensure_ascii=False)); return 0 if result["status"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
