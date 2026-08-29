# Icon Dataset / Icon Registry

> 产品展示层。与 Service Rules / Network Dataset **解耦**。  
> 缺图标 **不得** 阻断 Collect / Normalize / Builder 主链。

## 架构

```text
Service Registry          Icon Registry (manifest.yaml)
       │                            │
  database/services            assets/icons/
       │                            │
  rule builders              build_icons.py
       │                            │
       └──────── generate_rule_pages / Docs ────────┘
```

## 目录

```text
assets/icons/
├── manifest.yaml     # SSOT
├── source/*.svg      # 源（品牌或几何）
├── png/{64,128,256}/
└── ico/              # 可选
```

**不做 JPG**（Logo 需要透明）。WebP 可后期加。

## Manifest 字段

| 字段 | 说明 |
|------|------|
| `type` | `service` / `dataset` / `network` / `policy` |
| `status` | `verified` / `sourced` / `placeholder` / `missing` / `review` / `deprecated` |
| `source` | 来源 provider / slug / url |
| `license` | **逐图标**记录；禁止写死「全部 CC0」 |
| `files` | svg + png 尺寸路径 |
| `service_icon_map` | service_id → icon_key（默认可 1:1） |

### 许可注意

Simple Icons **项目**为 CC0，但 **品牌商标**仍受各公司规范约束。`status: sourced` 表示来源明确、尚未逐品牌法务确认。策略/网络类几何图标为本项目原创，可用 CC0-1.0。

## 稳定 URL

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/png/256/<icon_key>.png
```

由生成器读 `manifest.defaults.raw_url_template`，勿在上百个 Markdown 里手写。

## 命令

```bash
python scripts/build_icons.py
python scripts/icon_validate.py
python scripts/icon_validate.py --require-all-services   # 仅审计
```

CI：建议 `continue-on-error: true`，与主规则门禁分离。

## 策略图标

`direct` / `proxy` / `reject` / `dns` / `lan` / `china` / `geoip` / … 使用**自制几何标**，不用任何品牌 Logo。
