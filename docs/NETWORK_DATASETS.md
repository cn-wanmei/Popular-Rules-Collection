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

## Capability Matrix (initial)

| Dataset | mihomo | sing-box | surge | others | notes |
|---------|--------|----------|-------|--------|-------|
| Service rules | list | json | list | list | existing |
| Service IP sidecar | IP-CIDR | ip_cidr | IP-CIDR | … | existing |
| LAN / private | IP-CIDR | ip_cidr | IP-CIDR | … | P0 `generated/network/` |
| Geosite | rule-set / geosite | geosite | DOMAIN sets | optional | P1 |
| GeoIP country list | IP-CIDR | ip_cidr | IP-CIDR | optional | P1 |
| GeoIP MMDB | binary | binary | — | — | artifact only |
| ASN metadata | meta | meta | — | — | P1 |
| Proxy/Direct policy | P2 | P2 | P2 | P2 | policy domain |
| DNS policy | P2 | P2 | P2 | P2 | not full config gen |

## Directory contract

```
database/
  services/ domains/ ips/     # Service Rules (frozen path contract)
  network/                    # LAN, private, multicast
  geosite/                    # category domain lists (future)
  geoip/                      # country CIDR lists (future)
  asn/                        # metadata (future)
  policies/                   # proxy/direct/dns (P2)
generated/
  mihomo/ … loon/             # Service client rules (unchanged)
  network/                    # Network dataset client exports
  mmdb/                       # MMDB artifacts only (never expanded to ips/)
sources/
  registry.yaml
  ip_registry.yaml
  datasets/
    network.yaml
    geosite.yaml
    geoip.yaml
    asn.yaml
```

## Priority

- **P0**: LAN/private + dataset registry + docs + validate (this commit)
- **P1**: Geosite/GeoIP materialization, MMDB as artifact, ASN metadata
- **P2**: Proxy/Direct/DNS policy datasets
- **Out of scope here**: full proxy config generator (separate project if ever)

## Non-goals

- Do not route AWS ASN into Amazon service lists
- Do not explode MMDB into `database/ips/`
- Do not treat geosite `category-social` as a single Service
- Do not replace Primary Ecosystem / Service Canonical with Geosite ids
