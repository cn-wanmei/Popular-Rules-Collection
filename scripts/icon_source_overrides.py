#!/usr/bin/env python3
"""Apply protected semantic sources for payment brands after generic brand refresh.

These three keys must never be replaced by Apple/Google/other generic service marks.
Sources are maintained as dedicated payment-logo assets and normalized into the
repository's 128x128 icon canvas.
"""
from __future__ import annotations
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/"assets/icons/source"; UA={"User-Agent":"PRC-Icons/2.0"}
URLS={
 "applepay":"https://raw.githubusercontent.com/datatrans/payment-logos/master/assets/wallets/apple-pay.svg",
 "googlepay":"https://raw.githubusercontent.com/datatrans/payment-logos/master/assets/wallets/google-pay.svg",
 "unionpay":"https://raw.githubusercontent.com/datatrans/payment-logos/master/assets/cards/unionpay.svg",
}

def fetch(url):
    req=urllib.request.Request(url,headers=UA); return urllib.request.urlopen(req,timeout=20).read().decode("utf-8")
def wrap(key, inner):
    # The upstream payment assets use a 120x80 card canvas. Preserve the artwork
    # and put it on the repository's 128x128 presentation canvas without stretching.
    inner=inner.replace('<svg','<g transform="translate(4 24)"',1)
    inner=inner.replace('</svg>','</g>',1)
    return f'<svg role="img" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg"><title>{"Apple Pay" if key=="applepay" else "Google Pay" if key=="googlepay" else "UnionPay"}</title><rect width="128" height="128" rx="28" fill="#F7F7F7"/>{inner}</svg>'
def main():
    changed=0
    for key,url in URLS.items():
        data=fetch(url); out=SRC/f"{key}.svg"; wrapped=wrap(key,data); out.write_text(wrapped,encoding="utf-8"); changed+=1
    print(f"[icon_payment_overrides] updated={changed}")
if __name__=="__main__": main()
