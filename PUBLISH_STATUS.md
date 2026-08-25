# Publish & CI status

Repository: https://github.com/cn-wanmei/Popular-Rules-Collection

## How to generate database/ + generated/ on GitHub

1. Open **Actions** → **Collect Upstream**
2. Click **Run workflow**
3. Optionally enable **Skip mega lists** for a faster test run
4. Wait for the job (can take 10–40 minutes for full lists)
5. On success the bot commits:
   - `database/` (services + domains + ips)
   - `generated/` (mihomo / sing-box / surge / shadowrocket / quantumult-x / egern)
   - `sources/health.yaml`, `reports/`, backup manifests

Daily schedule: **22:00 UTC**.

## Local equivalent

```bash
pip install -r requirements.txt
python scripts/collect.py
python scripts/normalize.py
python scripts/build_mihomo.py
python scripts/build_singbox.py
python scripts/build_surge.py
python scripts/build_shadowrocket.py
python scripts/build_quantumultx.py
python scripts/build_egern.py
```
