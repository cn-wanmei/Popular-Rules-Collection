# IP Architecture (Phase 2B-IP)

## Why domain ≫ IP is not automatically a bug

Most modern services sit behind CDN / Anycast / shared cloud ranges.
**Domain → service** is usually more accurate than **IP → service**.
Inflating IP counts by attaching provider ranges to services causes mis-routing
(e.g. AWS → Amazon.list would hit Netflix, OpenAI, Discord, …).

## Hard scopes (`ip_scope`)

| Scope | Meaning | May enter service client ruleset? |
|-------|---------|-------------------------------------|
| `service` | Addresses verified as *that product only* | Yes |
| `provider` | Cloud/CDN operator (AWS, Cloudflare, …) | **No** (infra lists only) |
| `country` | National aggregates (CN, US, …) | Only via country ids (`china`, …) |
| `carrier` | ISP ranges (CMCC / CU / CT) | Only via carrier ids |
| `infrastructure` | DNS, STUN, NTP, private, … | Dedicated infra ids only |

### Examples

- `8.8.8.8` → provider/infrastructure Google DNS — **not** `service: google` product suite.
- Loyalsoldier `cn.txt` → `scope: country` → `china` id only.
- OpenAI published API ranges (if ever verified) → `scope: service` → `openai`.

## Directory contract (compatible with current builders)

Builders read **flat** `database/ips/{id}.txt` (same id as service/country/carrier).

```
database/ips/
  china.txt           # country
  chinamobile.txt     # carrier
  chinaunicom.txt
  chinatelecom.txt
  openai.txt          # service (only if verified service-owned)
  cloudflare.txt      # prefer infrastructure; do not treat as "all sites on CF"
  ...
```

Optional future layout (`service/`, `country/`, …) requires builder changes — **not** in P0.

## Source pool

See `sources/ip_registry.yaml` (independent from domain `sources/registry.yaml`).

## Pipeline

```
ip_registry → collect_ip → ip_cidr normalize/dedup → database/ips/{id}.txt
                                                      ↓
                                              rule_loader / ×7 builders
```

## P0 / P1 / P2 (IP track)

- **P0**: schema + registry + CIDR tools + country/carrier seed (CN)
- **P1**: more country lists; operator lists; never auto-map GeoIP country → service
- **P2**: verified *service*-owned ranges only (OpenAI/Google/… after manual proof)

Domain hot-service gaps remain a **separate** track.
