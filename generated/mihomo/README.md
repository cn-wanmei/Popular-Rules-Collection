# Mihomo / Clash Meta 规则使用说明

> 目录：`generated/mihomo/`

## 热门规则

| 规则 | 说明 | 策略 | 直链 |
|------|------|------|------|
| `china` | 国内域名直连 | DIRECT | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/china.yaml) |
| `google` | Google | PROXY | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google.yaml) |
| `youtube` | YouTube | PROXY | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/youtube.yaml) |
| `ai` | AI 聚合 | PROXY | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/ai.yaml) |
| `apple` | Apple | 按需 | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/apple.yaml) |
| `telegram` | Telegram | PROXY | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/telegram.yaml) |
| `github` | GitHub | PROXY | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/github.yaml) |
| `netflix` | Netflix | PROXY | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/netflix.yaml) |
| `adblock-light` | 广告轻量 | REJECT | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/adblock-light.yaml) |
| `restricted` | 受限媒体 | PROXY | [Raw](https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/restricted.yaml) |

## URL 模板

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/<id>.yaml
https://cdn.jsdelivr.net/gh/cn-wanmei/Popular-Rules-Collection@main/generated/mihomo/<id>.yaml
```

## 配置示例

```yaml
rule-providers:
  china:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/china.yaml"
    interval: 86400
  google:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/google.yaml"
    interval: 86400
  restricted:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/restricted.yaml"
    interval: 86400
rules:
  - RULE-SET,china,DIRECT
  - RULE-SET,google,PROXY
  - RULE-SET,restricted,PROXY
  - GEOIP,CN,DIRECT
  - MATCH,PROXY
```

[总览](../README.md) · [单服务说明](../../docs/rules/README.md)
