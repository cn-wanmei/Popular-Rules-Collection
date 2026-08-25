# Publish status

Repository: https://github.com/cn-wanmei/Popular-Rules-Collection

## Uploaded via API
- Core scripts (partial), workflows, config, sources
- Sample generated rules and domain lists

## Large artifacts (local / CI regenerate)
Files over ~1MB (adblock, china, proxy full lists and multi-client builds) should be produced by:

```bash
pip install -r requirements.txt
python scripts/collect.py
python scripts/normalize.py
python scripts/build_mihomo.py
python scripts/build_surge.py
python scripts/build_singbox.py
python scripts/build_shadowrocket.py
python scripts/build_quantumultx.py
python scripts/build_egern.py
```

Or enable GitHub Actions workflows (collect → normalize → build).

> Note: Uploading 100MB+ of rule text via Contents API is rate/size constrained; CI is the intended path for mega lists.
