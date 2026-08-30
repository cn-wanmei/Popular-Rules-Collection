# 图标使用说明（SSOT）

面向客户端与贡献者的**唯一入口**。其它 `docs/ICON_*.md` 为历史设计笔记，以本文为准。

## 1. 方案概览

| 层级 | 路径 | 说明 |
|------|------|------|
| SSOT 元数据 | `assets/icons/manifest.yaml` | 每个 icon 的 id、色、来源、映射 |
| 源矢量 | `assets/icons/source/{id}.svg` | 品牌 / 策略几何原图 |
| 主交付 PNG | `assets/icons/png/{64,128,256}/{id}.png` | **客户端默认使用** |
| 规范化 SVG | `assets/icons/normalized/{id}.svg` | Engine 居中裁切后 |
| 主题渲染 | `assets/icons/rendered/{transparent,light,dark}/{size}/{id}.png` | 可选主题底 |
| 配置 | `profiles.yaml` / `themes.yaml` / `client_profiles.yaml` | 客户端配置档 |
| 元数据 | `metadata/*.yaml` | schema / QA / 色板 / 源优先级 |

**已移除（重复或违背「无纯黑」策略）：**

- `strategies/`、`datasets/`（与 `png/` + `source/` 重复）
- `monochrome/`（纯黑剪影，仓库禁止纯黑品牌图）
- `official/`（空壳目录）

## 2. 客户端使用路径

Base（GitHub raw）：

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons
```

| 用途 | URL 模板 |
|------|----------|
| 推荐 128 | `{base}/png/128/{id}.png` |
| 大图 256 | `{base}/png/256/{id}.png` |
| 小图 64 | `{base}/png/64/{id}.png` |
| SVG | `{base}/source/{id}.svg` |
| 透明底主题 | `{base}/rendered/transparent/128/{id}.png` |
| 浅底 | `{base}/rendered/light/128/{id}.png` |
| 深底 | `{base}/rendered/dark/128/{id}.png` |

`{id}` 与规则服务 id 对齐（见 `manifest.service_icon_map`），例如：

```text
google → .../png/128/google.png
direct → .../png/128/direct.png
alipay → .../png/128/alipay.png
```

策略组 id：`direct` `proxy` `reject` `select` `auto` `urltest` `fallback` `loadbalance` `match` `final` `dns` `adblock` `global` …

## 3. 生成流水线

```text
source/*.svg
    │
    ├─ icon_policy_set.py          # 策略几何全彩
    ├─ icon_identity_si_refresh.py # Simple Icons 路径
    ├─ icon_color_identity_fix.py
    ├─ icon_no_black.py            # 禁止纯黑品牌色
    │
    ▼
build_icons.py --force             # → png/{64,128,256}/
icon_engine.py --force             # → normalized/ + rendered/
icon_contact_sheet.py              # → reports/icons/contact-sheet*.png
icon_validate.py
```

本地一键：

```bash
python scripts/icon_policy_set.py
python scripts/icon_identity_si_refresh.py
python scripts/icon_no_black.py
python scripts/build_icons.py --force
python scripts/icon_engine.py --force
python scripts/icon_validate.py
python scripts/icon_cleanup_dirs.py
```

Collect CI 在 `Icon build` 步骤中自动执行上述链路。

## 4. 设计规则（硬约束）

1. **无纯黑品牌图标**：Apple/GitHub/X 等使用流行灰/紫/蓝等非黑填充（`icon_no_black.py`）。
2. **多色 Logo 原样保留**（Google、Microsoft 等）。
3. **策略 / 网络 / 数据集** 使用项目几何色，不套品牌 Logo。
4. **service → icon 身份绑定**：`service_icon_map`；禁止错绑。
5. **决策覆盖优先于 Logo 覆盖**：无可信源可不造假官方标。

## 5. 目录允许清单

```text
assets/icons/
  manifest.yaml          # 必选
  decisions.yaml
  registry.yaml          # 可由 registry_build 生成
  profiles.yaml
  themes.yaml
  client_profiles.yaml
  visual_baseline.json   # 视觉回归基线
  README.md
  source/*.svg
  png/{64,128,256}/*.png
  normalized/*.svg
  rendered/{transparent,light,dark}/{64,128,256}/*.png
  metadata/*.yaml
```

其它路径视为无效冗余，用 `scripts/icon_cleanup_dirs.py` 清理。

## 6. 相关文档索引

| 文档 | 内容 |
|------|------|
| **本文 ICON_USAGE.md** | 使用与路径 SSOT |
| ICON_POLICY_SET.md | 策略组图标色板 |
| ICON_NO_BLACK.md | 无纯黑色板 |
| ICON_SCHEMA_V2.md | manifest 字段 |
| ICON_ENGINE.md | Normalize / 主题渲染 |
| CLIENT_ICON_URLS.md | 客户端 URL 摘要 |
