# Dataset Registries

| File | Kind | Status |
|------|------|--------|
| network.yaml | LAN / private | **P0 active** |
| geosite.yaml | domain categories | **P1 active** (direct/proxy) |
| geoip.yaml | country + MMDB | **P1 active** |
| asn.yaml | ASN metadata | **P1 active** |
| policy.yaml | direct/proxy/dns | **P2 active** (policy only) |

**Hard rules**

- Geosite category ≠ Service id
- GeoIP country ≠ product service IP
- Provider ASN ≠ Amazon/Google service list
- MMDB stays under `generated/mmdb/`
- DNS registry ≠ full Fake-IP/TUN config generator
