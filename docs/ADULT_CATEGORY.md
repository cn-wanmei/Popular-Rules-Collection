# Adult（18+）类目说明

## 定位

独立 **成人 / NSFW 聚合服务** `adult`，与社交、流媒体等类目分离。

## 上游（仅可信源）

| 源 | 路径 | 规模 |
|----|------|------|
| MetaCubeX | `geo/geosite/category-porn.list` | ~6500+ |
| v2fly | `data/category-porn` | ~6000+ |
| 侧车 | pornhub / xvideos / ehentai geosite | 补充 |

**不收录**无上游验证的站点域名（不猜测草榴镜像、性吧备用域等）。

## 已覆盖（抽样）

Pornhub、XVideos、Chaturbate、XHamster、XNXX、E-Hentai、ExHentai、nhentai、91porn、t66y、海角(haijiao)、Jable、MissAV、JavBus、JavDB、色花堂(sehuatang) 等。

OnlyFans 主域等若上游未列，则不强制补全。

## 客户端策略建议

```text
RULE-SET,adult,PROXY   # 或独立节点策略
```

订阅示例（Mihomo）：

```yaml
rule-providers:
  adult:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/adult.yaml"
    interval: 86400
```

## 与广告拦截的区别

- `adblock*` → **REJECT**
- `adult` → 内容站点匹配，一般 **PROXY**（非拦截）
