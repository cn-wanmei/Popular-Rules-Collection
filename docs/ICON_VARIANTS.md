# Icon Variants / Profiles / Themes（P0）

一 Service 可有多个合法 Variant；客户端一次只选一个。**禁止** Client Builder 各自找图。

## 三层

| 层 | 文件 | 职责 |
|----|------|------|
| Manifest | `manifest.yaml` | 实体、来源、license、路径 |
| Registry | `registry.yaml` | Service → variant 角色 |
| Profile/Theme | `profiles.yaml` / `themes.yaml` | 场景默认角色 |

## 角色（≤5）

`brand` · `simple` · `mono` · `network` · `flat`（预留）· `placeholder`

Variant **可共享同一 SVG**，避免文件爆炸。

## 命令

```bash
python scripts/icon_registry_build.py
python scripts/icon_resolver.py google --profile client
python scripts/icon_resolver.py --sample --profile monochrome
```

## 主题 → Profile

| Theme | Profile |
|-------|---------|
| official | brand |
| colorful | colorful |
| minimal | minimal |
| monochrome | monochrome |
| network | network |

## 边界

- P0：模型 + registry 引导（已完成）
- P1：仅高频 30～50 独立 brand/mono 源
- 不把 icon 写入 7 Client 规则正文
