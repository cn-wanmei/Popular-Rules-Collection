# Icons — Icon System V5 / Matrix 8

**Active system: V5 only**

| | |
|--|--|
| Coverage | **146 / 146** services × **8/8** (含独立子服务) |
| Release | [`icon-v5-1.0.0`](https://github.com/cn-wanmei/Popular-Rules-Collection/releases/tag/icon-v5-1.0.0) |
| Registry | `assets/icons/v5/registry.json` |
| Pointer | `assets/icons/v5/release-pointer.json` |
| Client policy | `config/icon_v5_clients.yaml` |
| Client URL profiles | `assets/icons/client_profiles.yaml` |

## Eight layers

1. Source Original  
2. Glassmorphism  
3. Soft 3D / Claymorphism  
4. Neo-Skeuomorphism  
5. Minimalist Glyph & Multi-color Flat  
6. Two-tone / Broken Line  
7. MBE Illustration  
8. Y2K / Synthwave  

```text
1 service_id = 1 icon_identity = 1 source + 7 derived styles
```

## Client preferred style

| Client | Style |
|--------|-------|
| mihomo / singbox / shadowrocket | minimalist |
| surge / egern | glassmorphism |
| quantumultx | duotone_line |
| loon | soft_3d |

```bash
python scripts/icon_resolver_v5.py \
  --registry assets/icons/v5/registry.json \
  --service-id github \
  --client mihomo
```

## Layout

```text
assets/icons/v5/
├── registry.json
├── release-pointer.json
├── normalized/
├── styles/{glassmorphism,soft-3d,...}/
├── png/{64,128,256}/
└── seed/          # reviewed seeds only
```

Full SVG/PNG pack: Release asset `icon-v5-rc1-full-pack.zip` (tag `icon-v5-1.0.0`).

## Historical systems

V1 / V2 / V3 / V4 icon systems are **removed** from the active tree. Do not reference legacy `assets/icons/v3`, `v4`, root `normalized/`, `png/`, `rendered/`, or `icon_system_v3.py`.

## Commands

```bash
python scripts/icon_system_v5.py contract
python scripts/icon_system_v5.py discover --rule-index rule/_index.yaml --out build/icon-v5/service-discovery.json
python scripts/icon_system_v5.py build --rule-index rule/_index.yaml --out build/icon-v5 --strict
python scripts/icon_system_v5.py gate --registry build/icon-v5/registry.json --rule-index rule/_index.yaml --strict
```
