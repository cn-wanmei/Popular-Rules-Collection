#!/usr/bin/env python3
"""Deterministic repository-wide Icon QA.

Validates every manifest icon for source SVG integrity, 64/128/256 PNG completeness,
semantic title/name consistency, payment-brand separation, and placeholder states.
"""
from __future__ import annotations
import argparse, json, re, xml.etree.ElementTree as ET
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]; ICON_ROOT=ROOT/"assets/icons"; MANIFEST=ICON_ROOT/"manifest.yaml"; SIZES=(64,128,256)
PAYMENT_KEYS={"applepay":{"apple pay","applepay","apple-pay","apple_pay","apay"},"googlepay":{"google pay","googlepay","google-pay","google_pay","gpay"},"unionpay":{"unionpay","union pay","union-pay","union_pay","银联"}}
FORBIDDEN={"applepay":{"apple"},"googlepay":{"google"},"unionpay":{"visa","mastercard","alipay","wechatpay","wechat"}}
def norm(s): return re.sub(r"[^a-z0-9]+","",str(s).lower())
def image_size(path):
    from PIL import Image
    with Image.open(path) as im: return im.size
def svg_meta(path):
    text=path.read_text(encoding="utf-8"); root=ET.fromstring(text); vb=root.attrib.get("viewBox",""); nums=[float(x) for x in re.split(r"[\\s,]+",vb.strip()) if x] if vb else []
    aspect=nums[2]/nums[3] if len(nums)==4 and nums[2]>0 and nums[3]>0 else None; title=""
    for c in root.iter():
        if c.tag.rsplit("}",1)[-1]=="title" and c.text: title=c.text.strip(); break
    return {"bytes":path.stat().st_size,"viewBox":vb,"aspect":aspect,"title":title,"has_text":bool(re.search(r"<text(?:\\s|>)",text,re.I))}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--json",default="reports/icon_qa.json"); args=ap.parse_args()
    doc=yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}; icons=doc.get("icons") or {}; report={"schema":"icon_qa_v1","icon_count":len(icons),"checks":{"source_svg":0,"png_64":0,"png_128":0,"png_256":0,"semantic":0,"payment_separation":0},"errors":[],"warnings":[]}
    for key,meta in sorted(icons.items()):
        if not isinstance(meta,dict): report["errors"].append(f"{key}: manifest entry is not a mapping"); continue
        files=meta.get("files") or {}; svg_rel=files.get("svg") or f"source/{key}.svg"; svg=ICON_ROOT/svg_rel
        if not svg.is_file(): report["errors"].append(f"{key}: missing SVG {svg_rel}"); continue
        try:
            sm=svg_meta(svg); report["checks"]["source_svg"]+=1
            if sm["aspect"] is not None and not .25 <= sm["aspect"] <= 4.0: report["warnings"].append(f"{key}: extreme source aspect ratio {sm['aspect']:.3f}")
        except Exception as exc: report["errors"].append(f"{key}: invalid SVG: {exc}"); continue
        for size in SIZES:
            rel=(files.get("png") or {}).get(str(size)) or f"png/{size}/{key}.png"; p=ICON_ROOT/rel
            if not p.is_file(): report["errors"].append(f"{key}: missing PNG {size} {rel}"); continue
            try:
                wh=image_size(p); report["checks"][f"png_{size}"]+=1
                if wh!=(size,size): report["errors"].append(f"{key}: PNG {size} is {wh[0]}x{wh[1]}, expected {size}x{size}")
            except Exception as exc: report["errors"].append(f"{key}: unreadable PNG {rel}: {exc}")
        name=str(meta.get("name") or key); title=sm.get("title",""); nk,nn,nt=norm(key),norm(name),norm(title); aliases={norm(x) for x in (meta.get("aliases") or []) if x}; ok=not title or nt in {nk,nn} or nt in aliases or nk in nt or nn in nt
        if key in PAYMENT_KEYS: ok=nt==norm(name) or nt in {norm(x) for x in PAYMENT_KEYS[key]}
        if ok: report["checks"]["semantic"]+=1
        else: report["errors"].append(f"{key}: semantic mismatch name={name!r} svg_title={title!r}")
        if key in PAYMENT_KEYS:
            report["checks"]["payment_separation"]+=1; slug=norm((meta.get("source") or {}).get("slug") or "")
            if slug in {norm(x) for x in FORBIDDEN[key]}: report["errors"].append(f"{key}: forbidden generic brand fallback {slug}")
        status=str(meta.get("status") or "")
        if status in {"missing","placeholder","review"}: report["warnings"].append(f"{key}: manifest status={status}")
    out=ROOT/args.json; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"icons":report["icon_count"],"errors":len(report["errors"]),"warnings":len(report["warnings"]),"checks":report["checks"],"report":str(out)},ensure_ascii=False)); return 1 if report["errors"] else 0
if __name__=="__main__": raise SystemExit(main())
