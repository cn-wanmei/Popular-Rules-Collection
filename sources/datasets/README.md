# Dataset Registries

| File | Kind | Status |
|------|------|--------|
| network.yaml | LAN / private / DNS / NTP / STUN | **active** |
| geosite.yaml | domain categories (text) | **active** |
| geoip.yaml | country CIDR + Country.mmdb | **active** |
| **binary.yaml** | MMDB / DAT mirrors | **active** |
| asn.yaml | ASN **metadata** only | **active** |
| provider.yaml | cloud provider CIDRs | **active** |
| policy.yaml | direct/proxy/dns policy refs | **active** |

**Hard rules**

- Geosite category ≠ Service id
- GeoIP country ≠ product service IP
- Provider ASN ≠ Amazon/Google service list
- MMDB/DAT under `generated/mmdb/` only
- Never write Network Dataset into `database/ips/<service>.txt`

**Stable client URLs:** [docs/CLIENT_NETWORK_URLS.md](../../docs/CLIENT_NETWORK_URLS.md)

```bash
python scripts/collect_datasets.py
python scripts/dataset_quality.py
```
