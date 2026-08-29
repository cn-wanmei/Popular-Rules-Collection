# 客户端 Icon Profile（P4）

规则 Builder **不**写入图标。客户端按 Profile 取 URL：

```bash
python scripts/icon_resolver.py google --profile client
```

配置见 `assets/icons/client_profiles.yaml`。

| 客户端 | Profile | 推荐尺寸 |
|--------|---------|----------|
| Surge | client | 256 |
| Loon | client | 256 |
| Egern | client | 256 |
| Mihomo | client | 128 |
| sing-box | client | 128 |
| Shadowrocket | client | 256 |
| Quantumult X | client | 256 |

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/png/{size}/{icon_key}.png
```

单色：`…/monochrome/{size}/{icon_key}.png`
