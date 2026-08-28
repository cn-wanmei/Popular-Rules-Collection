# Network Datasets Architecture

The repository is a **Network Dataset / Rule Distribution** platform.

Two domains share CI and collectors but **must not** collapse into one model:

```
Service Rules                    Network Datasets
registry.yaml                    sources/datasets/*
database/services|domains|ips    database/geosite|geoip|asn|network|policies
rule_loader                      dedicated dataset loaders (no load_everything)
×7 client builders               Capability Matrix (not all datasets × 7)
```

## Capability Matrix

| Dataset | mihomo | sing-box | surge | notes |
|---------|--------|----------|-------|-------|
| Service rules | list | json | list | existing ×7 |
| LAN / private | list | cidr | list | `generated/network/` |
| Geosite direct/proxy | DOMAIN-SUFFIX | domains | list | `generated/geosite/` |
| GeoIP country | IP-CIDR | cidr | list | `generated/geoip/` |
| GeoIP MMDB | binary | binary | — | `generated/mmdb/` artifact only |
| ASN metadata | yaml | yaml | — | provider scope only |
| Proxy/Direct policy | manifest | manifest | — | references datasets |
| DNS servers | yaml | yaml | — | registry only, not full config |

## Directory contract

```
database/
  services/ domains/ ips/     # Service Rules (frozen)
  network/                    # LAN, private
  geosite/                    # category domain lists
  geoip/                      # country CIDR lists
  asn/                        # metadata
  policies/                   # proxy/direct/dns
  datasets_provenance/
generated/
  mihomo/ … loon/             # Service client rules
  network/ geosite/ geoip/    # Network exports
  mmdb/                       # MMDB artifacts (never expanded to ips/)
  policies/
sources/datasets/
  network.yaml geosite.yaml geoip.yaml asn.yaml policy.yaml
```

## Pipeline

```
validate_dataset_registry
  → build_network_lan
  → collect_datasets
  → build_network_datasets
```

Isolated from Service `collect → normalize → ×7 builders`.

## Status (2026-08-28)

| Track | Status |
|-------|--------|
| P0 LAN/private | **done** |
| P1 Geosite direct/proxy | **done** |
| P1 GeoIP cn/jp/hk/sg/kr | **done** |
| P1 Country.mmdb artifact | **done** (CI fetch) |
| P1 ASN metadata | **done** |
| P2 Proxy/Direct/DNS policy | **done** (manifests + DNS server registry) |

## Non-goals

- AWS ASN → Amazon service lists
- Explode MMDB into `database/ips/`
- Geosite category = Service id
- Full proxy config generator (separate project if ever)
