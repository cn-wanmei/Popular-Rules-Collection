# Icons

当前规划：Icon System V5 / Icon Matrix 8

SSOT 文档：

- docs/ICON_SYSTEM_V5_PLAN.md
- docs/ICON_USAGE.md

## Active

V5：

assets/icons/v5/

包含：

- Source Original
- Glassmorphism
- Soft 3D / Claymorphism
- Neo-Skeuomorphism
- Minimalist Glyph & Multi-color Flat
- Two-tone / Broken Line
- MBE Illustration
- Y2K / Synthwave

## Historical

以下仅保留历史兼容、回滚与审计：

- v4/
- v3/
- legacy

V3/V4 不再定义 V5 的身份、来源或覆盖口径。

## 生产原则

~~~text
same Run / Snapshot / IR
        ↓
Icon Acquisition
        ↓
Source Snapshot
        ↓
Source Original
        ↓
7 independent renderers
        ↓
QA + Coverage + Lineage
        ↓
Immutable Release
~~~

规则文件、客户端生成物和图标系统均为同一 Run 的兄弟投影。

规则文件不得自身联网抓取图标；客户端也不得绕过 Icon Registry 各自抓取。

## 命令

~~~bash
python scripts/icon_system_v5.py contract
python scripts/icon_system_v5.py discover --rule-index rule/_index.yaml --out build/icon-v5/service-discovery.json
python scripts/icon_system_v5.py build --rule-index rule/_index.yaml --out build/icon-v5 --strict
python scripts/icon_system_v5.py gate --registry build/icon-v5/registry.json --strict
~~~
