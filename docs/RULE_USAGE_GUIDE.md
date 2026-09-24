# Popular-Rules-Collection 规则使用说明

> 面向规则使用者、客户端配置维护者与二次集成开发者。
>
> 本文档以仓库当前 `main` 分支的 2026-09-24 Release 产物为基准。

## 1. 项目定位

Popular-Rules-Collection 是一条面向 Mihomo、sing-box、Surge、Shadowrocket、Quantumult X、Egern、Loon 的规则数据生产与发行管线。

用户真正需要关注的不是上游采集过程，而是两个发行入口：

- `rule/`：人类浏览、搜索、选择规则。
- `generated/<client>/`：针对具体客户端编译后的最终规则。

规则真源不是 `rule/`，也不是 `generated/`。V3 运行时的 Canonical 真源位于 `data/runs/<run>/canonical/`；`rule/` 与 `generated/` 都属于由同一 Immutable Run 派生出的发行物。

---

## 2. 当前发行状态

当前 `generated/manifest.json` 标记的发行批次：

- Collection Date：`2026-09-24`
- Client Rule Directories：`egern`、`loon`、`mihomo`、`quantumultx`、`shadowrocket`、`singbox`、`surge`
- Generated 文件数：`1984`
- `rule/` 浏览发行树：262 个规则文件
- 当前 Run ID：`20260924T043120249584Z-run`

这些数字属于当前 Release 的事实状态；后续重新生成后应以新的 `generated/manifest.json` 和 `rule/README.md` 为准，不应手工维护数字。

---

## 3. 规则目录 `rule/`

### 3.1 目录定位

`rule/` 是给人看的规则浏览目录，不是客户端直接加载的运行时目录。

典型结构：

```text
rule/
├── _index.yaml
├── README.md
├── 12306/
├── abc/
├── acfun/
├── adobe/
├── airbnb/
├── alibaba/
├── amazon/
├── anthropic/
├── apple/
├── atlassian/
├── ...
```

每一个一级目录通常代表一个服务、品牌、产品或规则集合；一级服务下面还可以继续存在子服务。

例如：

```text
rule/
└── alibaba/
    ├── alipay/
    ├── amap/
    ├── cainiao/
    ├── dingding/
    ├── eleme/
    ├── gaode/
    ├── taobao/
    ├── tmall/
    ├── xianyu/
    └── youku/
```

### 3.2 `rule/` 的正确用途

适合：

1. 浏览服务分类。
2. 查找某个品牌或产品是否存在规则。
3. 查看规则的语义内容。
4. 在不同客户端之间确认同一个服务的规则是否属于同一 Semantic IR。
5. 为后续配置选择目标服务。

不适合：

- 直接把 `rule/` 当作 Mihomo、sing-box、Surge 等客户端的最终配置。
- 手工修改 `rule/` 后期待下一次发布自动保留。
- 把 `rule/` 当作 V3 Runtime Input。

`rule/README.md` 明确规定该树由同一 Semantic IR Run 生成，并且不应手工编辑；如果上游或 Canonical 输入发生变化，应重新构建对应 Immutable Run。

---

## 4. 客户端发行目录 `generated/`

### 4.1 一级目录

当前正式客户端规则目录共 7 个：

| 目录 | 客户端 | 典型文件格式 | 主要用途 |
|---|---|---|---|
| `generated/mihomo/` | Mihomo / Clash Meta 生态 | YAML | Mihomo Rule Provider / ruleset |
| `generated/singbox/` | sing-box | JSON | sing-box rule-set / 规则配置 |
| `generated/surge/` | Surge | LIST | Surge Rule Set |
| `generated/shadowrocket/` | Shadowrocket | LIST | Shadowrocket 规则 |
| `generated/quantumultx/` | Quantumult X | LIST | Quantumult X 规则 |
| `generated/egern/` | Egern | YAML | Egern 规则 |
| `generated/loon/` | Loon | LIST | Loon 规则 |

客户端目录来自当前 `generated/manifest.json` 的 `client_rule_directories` 字段，不应根据历史版本自行增加或删除客户端目录。

### 4.2 客户端目录结构

标准形式为：

```text
generated/<client>/
└── <service>/
    ├── <service>.<ext>
    └── <subservice>/
        └── <subservice>.<ext>
```

例如当前 12306：

```text
generated/mihomo/12306/
├── 12306.yaml
└── 12306/
    └── 12306.yaml
```

顶层文件和子目录文件都属于生成产物；实际选择哪个文件，应以目标集成场景和该服务目录中的实际结构为准。

---

## 5. Raw 链接规则

所有最终客户端规则都可以通过 GitHub Raw 直接访问：

```text
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/<client>/<service>/<file>
```

### 5.1 一级服务 Raw

当服务只有标准一级文件时：

```text
generated/<client>/<service>/<service>.<ext>
```

例如 12306：

```text
Mihomo:
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/mihomo/12306/12306.yaml

sing-box:
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/singbox/12306/12306.json

Surge:
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/surge/12306/12306.list

Shadowrocket:
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/shadowrocket/12306/12306.list

Quantumult X:
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/quantumultx/12306/12306.list

Egern:
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/egern/12306/12306.yaml

Loon:
https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/generated/loon/12306/12306.list
```

### 5.2 子服务独立 Raw

如果一个服务存在子服务，则子服务拥有独立发行路径：

```text
generated/<client>/<parent>/<child>/<child>.<ext>
```

例如 Alibaba 下的 Taobao：

```text
generated/<client>/alibaba/taobao/taobao.<ext>
```

因此子服务不是通过 URL 参数筛选出来的，而是作为独立文件直接发布。这样可以让客户端只加载自己需要的服务规则，避免无关规则进入配置。

如果继续存在更深层级，则继续沿用目录层级：

```text
generated/<client>/<parent>/<child>/<grandchild>/<grandchild>.<ext>
```

### 5.3 Raw 链接选择原则

优先顺序：

1. 目标客户端对应的 `generated/<client>/`。
2. 精确到服务的文件。
3. 如果存在子服务，优先使用子服务自己的文件。
4. 不要跨客户端复用其他格式的规则文件。
5. 不要手工猜测不存在的路径；应先检查对应 `generated/<client>/` 目录或 `generated/manifest.json`。

---

## 6. 规则服务总览

### 6.1 浏览入口

服务总览建议从以下三个入口进入：

- `rule/_index.yaml`：规则浏览索引。
- `rule/README.md`：规则浏览发行说明。
- `generated/manifest.json`：最终生成文件级清单。

其中：

```text
rule/_index.yaml
    ↓
服务/规则浏览
    ↓
选择服务
    ↓
选择目标客户端
    ↓
generated/<client>/<service>/...
    ↓
Raw URL
```

### 6.2 典型服务组织

仓库采用服务树，而不是把所有规则平铺在一个目录：

```text
服务
├── 主服务规则
├── 子服务 A
├── 子服务 B
├── 子服务 C
└── ...
```

例如 Alibaba 家族可以继续拆分为：

```text
Alibaba
├── Alibaba
├── Alipay
├── Amap / Gaode
├── Cainiao
├── DingTalk
├── Eleme
├── Taobao
├── Tmall
├── Xianyu
└── Youku
```

这样做的核心价值是：

- 可以按服务独立更新。
- 可以按服务独立引用。
- 可以按客户端独立编译。
- 可以避免一个大型服务规则集把所有子产品强制绑定在一起。

---

## 7. 七客户端使用方法

### 7.1 Mihomo

目录：

```text
generated/mihomo/
```

规则文件主要使用 YAML。

典型引用方式：

```yaml
rule-providers:
  example:
    type: http
    behavior: classical
    format: yaml
    url: "<对应 generated/mihomo 的 Raw URL>"
    path: ./ruleset/example.yaml
    interval: 86400
```

然后在 `rules:` 中引用：

```yaml
- RULE-SET,example,PROXY
```

具体 `behavior`、格式和文件内容应以目标规则文件实际生成结果为准，不要仅凭服务名称推断。

### 7.2 sing-box

目录：

```text
generated/singbox/
```

典型文件为 JSON。应根据当前 sing-box 版本支持的 rule-set / remote rule-set 机制进行接入，并以仓库生成文件的实际 schema 为准。

### 7.3 Surge

目录：

```text
generated/surge/
```

规则文件为 `.list`。

通常作为 Surge Rule Set 的远程规则源使用；引用时应使用对应 Raw URL，并按照 Surge 当前版本的 Rule Set 语法配置。

### 7.4 Shadowrocket

目录：

```text
generated/shadowrocket/
```

规则文件为 `.list`。在 Shadowrocket 的规则配置中使用对应 Raw URL。

### 7.5 Quantumult X

目录：

```text
generated/quantumultx/
```

规则文件为 `.list`。根据 Quantumult X 当前版本支持的远程规则格式进行引用。

### 7.6 Egern

目录：

```text
generated/egern/
```

规则文件主要为 YAML。应直接引用与 Egern 对应的生成文件，不要拿 Mihomo 文件替代。

### 7.7 Loon

目录：

```text
generated/loon/
```

规则文件为 `.list`，用于 Loon 的远程规则引用。

---

## 8. 网络数据与服务规则的区别

`generated/` 不只有服务规则，还包含 Network Dataset：

```text
generated/
├── network/
├── geosite/
├── geoip/
├── provider/
├── asn/
├── ip/
├── policies/
└── mmdb/
```

这些数据和 Service Rule 的语义层不同。

### 服务规则

回答：

> “这个域名/IP 属于哪个服务？”

例如：12306、Apple、Alibaba、Amazon 等。

### Network Dataset

回答：

> “这个地址属于哪类网络基础设施或网络范围？”

例如 LAN、Private、DNS、NTP、STUN、GeoIP、ASN、Provider 等。

不要把 Network Dataset 当成普通服务规则使用；它们虽然属于同一个 Release Candidate，但用途和数据语义不同。

---

## 9. `generated/manifest.json` 的作用

`generated/manifest.json` 是最终生成树的单一文件级目录清单。

建议所有自动化程序在消费规则前先读取 Manifest，而不是扫描 GitHub 页面。

Manifest 可以用于：

- 判断客户端是否存在。
- 判断服务文件是否存在。
- 获取规则文件路径。
- 获取规则类型。
- 获取 rule_count。
- 获取文件大小。
- 获取 SHA-256。
- 建立本地缓存。
- 检查版本变更。
- 生成自己的服务索引。

自动化消费推荐流程：

```text
读取 generated/manifest.json
        ↓
过滤 kind=client_rules
        ↓
过滤 scope=<目标客户端>
        ↓
选择目标 service/path
        ↓
拼接或读取 Raw URL
        ↓
下载并缓存
        ↓
使用 sha256 做变更检测
```

---

## 10. 更新机制

当前生产链路不是“修改一个规则文件然后直接发布”，而是：

```text
Official / External Upstream
        ↓
Collection DAG
        ↓
backup/<date>
        ↓
Immutable Source Lineage Gate
        ↓
V3 Snapshot
        ↓
Ingest
        ↓
Source Gate
        ↓
Quarantine
        ↓
Canonical
        ↓
Hierarchy
        ↓
Semantic IR
        ↓
7 Client Adapters
        ↓
Determinism / Semantic / Directory Gates
        ↓
Release Candidate
        ↓
Immutable Publish
        ↓
rule/ + generated/
```

因此使用者通常不需要关心上游采集细节，只需要使用当前发布树。

---

## 11. 不建议的使用方式

### 不要直接使用 GitHub 网页 HTML 地址

错误：

```text
https://github.com/.../blob/main/generated/...
```

用于客户端远程规则时，应使用 Raw 内容地址。

### 不要使用 `rule/` 代替 `generated/`

`rule/` 是浏览发行树；客户端规则应从对应 `generated/<client>/` 获取。

### 不要跨客户端复用

例如：

```text
Mihomo YAML → 直接给 Quantumult X
```

这是错误的思路。每个客户端都有自己的 Adapter 和最终输出格式。

### 不要手工修改 generated

`generated/` 是构建产物。需要修改规则来源或语义时，应修改上游输入 / Canonical / 生产逻辑，再重新构建。

### 不要把不存在的服务 URL 写进配置

先确认：

```text
generated/<client>/<service>/
```

是否真实存在，再使用 Raw URL。

---

## 12. 故障排查

### 12.1 Raw 返回 404

检查：

1. 客户端目录是否正确。
2. 服务目录是否正确。
3. 文件扩展名是否正确。
4. 是否误把父服务当成子服务。
5. 是否使用了已经不存在的历史路径。
6. 是否应从 `generated/manifest.json` 查找准确路径。

### 12.2 客户端无法解析

首先确认使用的是目标客户端的生成目录：

```text
generated/mihomo
 generated/singbox
 generated/surge
 generated/shadowrocket
 generated/quantumultx
 generated/egern
 generated/loon
```

然后检查文件格式与客户端版本是否匹配。

### 12.3 规则数量与预期不一致

不要手工判断规则是否丢失。使用 `generated/manifest.json` 中的：

- `rule_count`
- `size`
- `sha256`
- `file`

进行版本间比较。

### 12.4 服务存在但某客户端没有

这是需要区分的情况：

- 服务在 `rule/` 存在，不代表每个客户端都一定存在同名文件。
- `generated/<client>/` 才是该客户端实际发行结果。
- 应以 Manifest 中 `kind=client_rules` 的实际记录为准。

---

## 13. 给第三方集成者的推荐接口

如果你要把 Popular-Rules-Collection 集成到自己的程序、Web 面板或规则管理器，建议只依赖以下公开发行层：

### A. 服务索引

```text
rule/_index.yaml
```

### B. 文件清单

```text
generated/manifest.json
```

### C. 客户端规则

```text
generated/<client>/...
```

### D. Network Dataset

```text
generated/network/...
generated/geosite/...
generated/geoip/...
generated/provider/...
generated/asn/...
generated/ip/...
generated/policies/...
generated/mmdb/...
```

不要把 `data/runs/` 当作普通用户 API；它属于生产运行和 lineage 证据层。

---

## 14. 最简使用流程

如果只是普通用户：

```text
1. 找服务
   ↓
2. 确认客户端
   ↓
3. 打开 generated/<client>/服务目录
   ↓
4. 找到对应规则文件
   ↓
5. 复制 Raw URL
   ↓
6. 添加到客户端
   ↓
7. 按客户端规则语法绑定策略组
```

如果是开发者：

```text
1. 拉取 generated/manifest.json
   ↓
2. 构建服务索引
   ↓
3. 按 client + service 查询
   ↓
4. 使用 file 字段定位产物
   ↓
5. 使用 sha256 做缓存/更新判断
   ↓
6. 使用 Raw URL 下载
```

---

## 15. 当前版本的几个重要原则

1. `rule/` 是用户浏览与选择入口。
2. `generated/<client>/` 是客户端消费入口。
3. `data/runs/<run>/canonical/` 才是 V3 Canonical 真源。
4. 不重新建立 `rules/` 第三套规则目录。
5. 服务规则与 Network Dataset 属于不同语义层。
6. `generated/manifest.json` 是最终发行树的单一文件级清单。
7. 子服务可以拥有独立规则文件和独立 Raw URL。
8. 客户端之间必须使用各自 Adapter 生成的规则，不应跨格式复用。
9. 派生发行物不应手工编辑。
10. 发布、更新和回滚应以 Immutable Run / Release 为边界，而不是以单个手工修改文件为边界。

---

## 16. 相关入口

- Repository：`https://github.com/cn-wanmei/Popular-Rules-Collection`
- Rule Browse：`rule/`
- Rule Index：`rule/_index.yaml`
- Rule README：`rule/README.md`
- Generated Manifest：`generated/manifest.json`
- Client Outputs：`generated/<client>/`
- Production Chain：`docs/PRODUCTION_RULE_CHAIN.md`
- Generated Outputs：`docs/GENERATED_OUTPUTS.md`
- Network Datasets：`docs/NETWORK_DATASETS.md`
- Architecture：`docs/ARCHITECTURE.md`

> 本文档只描述发行层的使用方式。生产链路、Immutable Lineage、Canonical、IR、Adapter、Release Gate 等工程细节，应以仓库现有架构文档和当前 Release 证据为准。
