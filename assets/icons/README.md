# Icons

当前 active：**Icon System V5 / Icon Matrix 8**

SSOT：

- `docs/ICON_SYSTEM_V5_PLAN.md`
- `assets/icons/v5/registry.json`
- `assets/icons/v5/release-pointer.json`

## Active

V5：`assets/icons/v5/`

Coverage：**146 / 146 services × 8/8**（含各 provider 下独立子服务）

- Source Original
- Glassmorphism
- Soft 3D / Claymorphism
- Neo-Skeuomorphism
- Minimalist Glyph & Multi-color Flat
- Two-tone / Broken Line
- MBE Illustration
- Y2K / Synthwave

完整 SVG/PNG 包：Release [`icon-v5-rc1`](https://github.com/cn-wanmei/Popular-Rules-Collection/releases/tag/icon-v5-rc1)

## Historical

- `v4/` / `v3/` / `legacy` — 仅历史兼容与审计，不参与 V5 SSOT

## 生产原则

```text
same Run / Snapshot / IR
        ↓
Icon Acquisition
        ↓
Source Snapshot
        ↓
7 independent renderers
        ↓
QA + Coverage + Lineage
        ↓
Immutable Release
```

## 命令

```bash
python scripts/icon_system_v5.py contract
python scripts/icon_system_v5.py discover --rule-index rule/_index.yaml --out build/icon-v5/service-discovery.json
python scripts/icon_system_v5.py build --rule-index rule/_index.yaml --out build/icon-v5 --strict
python scripts/icon_system_v5.py gate --registry build/icon-v5/registry.json --rule-index rule/_index.yaml --strict
```
