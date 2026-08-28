# Restricted 类目

独立聚合服务 **`restricted`**。

订阅路径使用含蓄 ID，避免规则集名称过于直白。

## 上游

- MetaCubeX `geo/geosite/category-porn.list`
- v2fly `data/category-porn`
- 侧车：pornhub / xvideos / ehentai geosite

仅物化可信上游；不手写域名。

## 客户端

```yaml
rule-providers:
  restricted:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/restricted.yaml"
    interval: 86400
rules:
  - RULE-SET,restricted,PROXY
```

策略一般为 **PROXY**（与 `adblock` 的 REJECT 不同）。
