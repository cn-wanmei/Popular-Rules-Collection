# 规则目录与使用场景

> 与仓库双轨架构对齐：**Service Rules**（按服务）+ **Network Datasets**（国家/策略/基础设施）。

生成路径：`generated/{mihomo,sing-box,surge,shadowrocket,quantumult-x,egern,loon}/<id>.*`  
订阅基址：`https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/`

## 策略建议（默认）

| 策略 | 适用 |
|------|------|
| **DIRECT** | 国内应用、银行、支付、运营商、LAN |
| **PROXY** | Google/AI/流媒体/国际社交/开发者平台 |
| **REJECT** | AdBlock 系列 |
| **视情况** | 微软/苹果/Steam 等：分域名或分节点 |

## 使用原则

1. **按服务引用**，不要把 Provider IP（如 AWS）当成 Amazon 购物规则。
2. **China 域名**用 `china`（China Max 级）；**中国 IP**用 `geoip/cn` 或 `database/ips/china.txt`。
3. 规则集只负责匹配；**策略（直连/代理）在客户端配置**。
4. 大列表（adblock / china）请按需订阅，避免全部塞进单一配置。

## 国内直连 / 生活

| ID | 名称 | 使用场景 | 建议策略 |
|----|------|----------|----------|
| `china` | 中国域名大全 (China Max) | 约 11 万+ 国内域名，国内走直连；对标 BM7 ChinaMax Domain | **DIRECT** |
| `alipay` | 支付宝 | 支付、生活服务；强烈建议直连 | **DIRECT** |
| `wechat` | 微信 | 即时通信与小程序；务必直连 | **DIRECT** |
| `tencent` | 腾讯生态 | 微信/QQ/腾讯系聚合 | **DIRECT** |
| `alibaba` | 阿里巴巴生态 | 淘宝/天猫/阿里云相关聚合 | **DIRECT** |
| `jingdong` | 京东 | 电商购物 | **DIRECT** |
| `pinduoduo` | 拼多多 | 电商 | **DIRECT** |
| `meituan` | 美团 | 外卖、到店、出行 | **DIRECT** |
| `didi` | 滴滴 | 网约车 | **DIRECT** |
| `eleme` | 饿了么 | 外卖点餐 | **DIRECT** |
| `xianyu` | 闲鱼 | 二手交易 | **DIRECT** |
| `amap` / `gaode` | 高德地图 | 导航、定位 | **DIRECT** |
| `baidu` | 百度 | 搜索、网盘、地图等 | **DIRECT** |
| `bilibili` | 哔哩哔哩 | 视频弹幕站 | **DIRECT** |
| `douyin` | 抖音 | 短视频国内版 | **DIRECT** |
| `kuaishou` | 快手 | 短视频 | **DIRECT** |
| `zhihu` | 知乎 | 问答社区 | **DIRECT** |
| `weibo` | 微博 | 社交媒体 | **DIRECT** |
| `xiaohongshu` | 小红书 | 社区种草 | **DIRECT** |
| `iqiyi` / `youku` / `tencentvideo` | 长视频 | 爱奇艺 / 优酷 / 腾讯视频 | **DIRECT** |
| `netease` / `kugoukuwo` | 国内音乐 | 网易云 / 酷狗酷我 | **DIRECT** |
| `ctrip` / `tongcheng` | 旅行 | 携程 / 同程 | **DIRECT** |
| `dewu` | 得物 | 潮玩电商 | **DIRECT** |
| `12306` | 12306 | 购票、行程；建议直连 | **DIRECT** |
| `huawei` / `xiaomi` / `oppo` / `vivo` | 国产手机生态 | 账号与云服务 | **DIRECT** |
| `chinamobile` / `chinaunicom` / `chinatelecom` | 运营商 | 业务域名；勿与国家 IP 列表混淆 | **DIRECT** |

## 银行 / 支付

| ID | 名称 | 使用场景 | 建议策略 |
|----|------|----------|----------|
| `unionpay` | 银联 | 银联支付 | **DIRECT** |
| `icbc` / `ccb` / `abc` / `boc` / `cmb` | 工农中建招 | 网银/App | **DIRECT** |
| `pingan` / `bocom` / `ceb` / `psbc` | 平安/交行/光大/邮储 | 银行业务 | **DIRECT** |
| `paypal` / `stripe` | 国际支付 | 出海收款/付款 | **PROXY** |

## AI

| ID | 名称 | 使用场景 | 建议策略 |
|----|------|----------|----------|
| `ai` / `aisuite` | AI 聚合 | 一键代理常用 AI | **PROXY** |
| `openai` | OpenAI | ChatGPT / API | **PROXY** |
| `claude` / `anthropic` | Claude | Anthropic 对话 | **PROXY** |
| `gemini` | Gemini | Google AI | **PROXY** |
| `copilot` | Copilot | AI 编程助手 | **PROXY** |
| `perplexity` / `groq` / `xai` / `huggingface` / `cursor` / `elevenlabs` | 其他 AI | 搜索/推理/IDE/语音 | **PROXY** |
| `doubao` | 豆包 | 字节 AI；国内多直连 | **DIRECT** |
| `deepseek` | DeepSeek | 按线路选择 | **视情况** |

## 国际社交

| ID | 名称 | 建议策略 |
|----|------|----------|
| `telegram` / `discord` / `twitter` / `facebook` / `instagram` / `whatsapp` / `messenger` / `threads` / `reddit` / `signal` / `bluesky` / `snapchat` | 国际社交 IM/社区 | **PROXY** |
| `linkedin` / `slack` | 职业/办公协作 | **视情况** |
| `line` / `kakaotalk` | 东亚 IM | **PROXY** |

## Google / Microsoft / Apple

| ID | 名称 | 使用场景 | 建议策略 |
|----|------|----------|----------|
| `google` / `youtube` / `youtubemusic` / `googlefcm` / `firebase` | Google 系 | 搜索/视频/推送 | **PROXY** |
| `microsoft` / `onedrive` / `teams` / `azure` | 微软系 | 账号与办公；可按域名细分 | **视情况** |
| `xbox` | Xbox | Game Pass 等 | **PROXY** |
| `apple` / `icloud` / `applemusic` | 苹果系 | 账号/云/音乐；国内节点或可直连 | **视情况** |
| `appletv` | Apple TV+ | 流媒体 | **PROXY** |

## 流媒体 / 游戏 / 开发

| 类别 | 示例 ID | 建议 |
|------|---------|------|
| 流媒体 | `netflix` `disney` `hbo` `spotify` `twitch` … | **PROXY**（解锁节点） |
| 游戏 | `steam` `epic` `nintendo` `playstation` `battlenet` `roblox` … | 商店多 **PROXY**；Steam 下载可分流 |
| 开发/云 | `github` `docker` `vercel` `aws`(域名) `cloudflare`(域名) … | 多 **PROXY**；Provider IP ≠ 产品服务 |

## 广告拦截 / 列表型

| ID | 使用场景 | 建议策略 |
|----|----------|----------|
| `adblock-light` | 轻量拦截，低配设备 | **REJECT** |
| `adblock` / `adblock-pro` | 全量/激进拦截，体积大 | **REJECT** |
| `proxy` / `gfw` | 常见需代理域名参考 | **PROXY** |
| `private` / `stun` | 内网与 NAT；直连 | **DIRECT** |

## Network Datasets（非 Service）

| 路径 | 说明 | 策略 |
|------|------|------|
| `geosite/direct` | 国内直连域名策略，与 china 互补 | **DIRECT** |
| `geosite/proxy` | 需代理域名策略 | **PROXY** |
| `geoip/cn` | 中国大陆 IP | **DIRECT** |
| `network/lan` | 局域网 CIDR | **DIRECT** |
| `provider/cloudflare` / `provider/aws` | 云厂商 IP；**不是**购物/SaaS 产品规则 | **视情况** |
| `mmdb/Country.mmdb` | GeoIP 数据库（Mihomo/sing-box） | — |

## 客户端示例

### Mihomo

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
rules:
  - RULE-SET,china,DIRECT
  - RULE-SET,google,PROXY
  - GEOIP,CN,DIRECT
  - MATCH,PROXY
```

### Surge

```text
RULE-SET,https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/china.list,DIRECT
RULE-SET,https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/openai.list,PROXY
```

单服务 Raw 页：`docs/rules/<id>.md`

---

*规则数据以 `database/` 与 `generated/` 为准；本目录描述用途与场景。*
