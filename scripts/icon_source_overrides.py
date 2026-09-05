#!/usr/bin/env python3
"""Apply protected semantic sources for payment brands after generic refresh."""
from __future__ import annotations
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/"assets/icons/source"; UA={"User-Agent":"PRC-Icons/2.0"}
URLS={"applepay":"https://raw.githubusercontent.com/datatrans/payment-logos/master/assets/wallets/apple-pay.svg","googlepay":"https://raw.githubusercontent.com/datatrans/payment-logos/master/assets/wallets/google-pay.svg","unionpay":"https://raw.githubusercontent.com/datatrans/payment-logos/master/assets/cards/unionpay.svg"}
def fetch(url):
 req=urllib.request.Request(url,headers=UA);return urllib.request.urlopen(req,timeout=20).read().decode("utf-8")
def wrap(key,inner):
 inner=inner.replace('<svg','<g transform="translate(4 24)"',1).replace('</svg>','</g>',1);title={"applepay":"Apple Pay","googlepay":"Google Pay","unionpay":"UnionPay"}[key];return f'<svg role="img" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg"><title>{title}</title><rect width="128" height="128" rx="28" fill="#F7F7F7"/>{inner}</svg>'
def main():
 for key,url in URLS.items():(SRC/f"{key}.svg").write_text(wrap(key,fetch(url)),encoding="utf-8")
 print("[icon_payment_overrides] updated=3")
if __name__=="__main__":main()
