# Architecture — Rule Product Units

## Layers

| Layer | Path | Editable | Role |
|-------|------|----------|------|
| Data | `database/` | No (pipeline) | Canonical services, domains, provenance |
| Product pages | `rule/` | No (generated) | Human browse + classical base lists |
| Clients | `generated/` | No (generated) | Mihomo / Surge / sing-box / … |
| Config | `config/` | Yes | categories, primary mapping, CDN |

## Primary Ecosystem

- **One physical path per service**, decided only by `primary_category`.
- `categories` tags are for search only — never create duplicate folders.
- Category ids are lowercase enums in `config/categories.yaml`.

```text
primary_category → categories.yaml display_name → rule/{Display}/{ServiceName}/
```

## Files per service

```text
rule/Tencent/WeChat/
├── README.md
├── metadata.yaml
├── wechat.list          # DOMAIN-SUFFIX / DOMAIN / IP-CIDR classical
├── wechat_domain.list   # domains only (if any)
└── wechat_ip.list       # CIDR only (if any)
```

- Filenames use **lowercase service id**.
- Folder names use **display_name**.
- No empty `_ip.list` when there are zero IP rules.

## Aggregate

`service_type: aggregate` only when upstream or merged data exists (e.g. `alibaba`, `tencent`). No empty shell pages.

## UnionPay

Physical home for 银联 + banks. README states banks are not owned by UnionPay; `sources` remain real upstream ids.

## Generator

```bash
python scripts/generate_rule_pages.py --clean
```

CI runs this after builders. Do not hand-edit `rule/`.

## Phase 8 cutover boundary

The previous description of `database/` as the canonical service store is historical. During the Phase 8 migration:

- `database/services/` = explicit Legacy Source.
- `rule/` = V1 Canonical Service Model.
- `generated/` = generated distribution only.
- V3 remains the sole production build chain.
- Legacy deletion requires the final asset-level migration gate; no workflow deletes the source automatically.
