# Dataset Registries

Separate from Service domain (`sources/registry.yaml`) and IP service-sidecar (`sources/ip_registry.yaml`).

| File | Kind | Status |
|------|------|--------|
| network.yaml | LAN / private | **P0 active** |
| geosite.yaml | domain categories | P0 scaffold / P1 materialize |
| geoip.yaml | country + MMDB artifact | P0 scaffold / P1 |
| asn.yaml | ASN metadata | P1 |

**Hard rules**

- Geosite category ≠ Service id
- GeoIP country ≠ product service IP
- Provider ASN ≠ Amazon/Google service list
- MMDB stays as artifact under `generated/mmdb/`
