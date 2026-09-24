# 客户端 Icon Profile — Current V3

当前图标 SSOT：`assets/icons/v3/release-pointer.json`。它指向不可变 Icon System 3 Release，并为 7 个客户端提供独立 client index。

| 客户端 | 当前 Index |
|---|---|
| Mihomo | `index/clients/mihomo.json` |
| sing-box | `index/clients/singbox.json` |
| Surge | `index/clients/surge.json` |
| Shadowrocket | `index/clients/shadowrocket.json` |
| Quantumult X | `index/clients/quantumultx.json` |
| Egern | `index/clients/egern.json` |
| Loon | `index/clients/loon.json` |

准确图标 URL 与 digest 必须从对应 client index 读取，不应继续根据旧 `assets/icons/png/{size}/` 模板猜路径。

详见 [ICON_USAGE.md](ICON_USAGE.md)。