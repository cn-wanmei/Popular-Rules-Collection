# V1 模型开发规划方案

> **V1 Model = V2.1.1 模型的正式生产命名**
>
> V1 是 `rule/` Service Rule 数据模型的稳定契约层；V3 Engine 负责采集、标准化、解析、决策、IR、适配器与发布。V1 不替代 V3，也不创建新的生产链。

## 1. 目标

建立一个与 V3 Production Chain 可直接对接、可持续扩展、可审计的 Service Rule Canonical Model：

```text
Category
   │ tags / references
   ▼
Service
   ├── own assets
   ├── children
   ├── requires
   └── network_references
          │
          ▼
   Dependency Closure
          │
          ▼
   Aggregate Resolution
          │
          ▼
   Canonical Set Deduplication
          │
          ▼
         V3 IR
          │
          ▼
       Adapters
          │
          ▼
      generated/
```

核心原则：

1. **Service 是 Canonical Entity**，不是 Category 的附属文件。
2. **Category 是组织与聚合关系**，不是 Service 的父级实体。
3. 每个重要 Service 都可以独立编译、独立订阅。
4. Parent Service 是真实 Service Entity，可拥有自己的 assets，同时聚合 Child Services。
5. Child Service 必须可以独立输出，也可以被 Parent Aggregate 引用。
6. Shared Component 只作为可复用依赖，不成为普通用户默认订阅入口。
7. Network Dataset 与 Service Rule 保持边界；Service 可以显式引用 Network Dataset。
8. Aggregate 不复制 Canonical Rule 数据，而是在编译阶段解析引用并集合去重。
9. 策略（DIRECT / PROXY / REJECT 等）不写入 Canonical Service Rule。
10. V1 必须能够被 V3 Engine 读取，并最终生成现有七种客户端产物。

---

## 2. V1 的范围

### 2.1 V1 包含

- Category Model
- Service Model
- Parent / Child Service Model
- Shared Component Model
- Service Dependency Model
- Aggregate Model
- Network Dataset Reference Model
- Canonical Asset Model
- Dependency Closure
- Aggregate Closure
- Canonical Deduplication
- Cycle Detection
- Service Catalog
- Service Coverage Matrix
- 迁移与兼容策略
- V3 Adapter Contract

### 2.2 V1 不包含

- 客户端策略组
- 节点选择
- 自动判断用户应当 DIRECT 还是 PROXY
- 将 ASN / 云厂商 IP 自动归入产品服务
- 无限递归 Service 层级
- 依赖客户端自身完成 Aggregate 去重
- 重新建立一套独立于 V3 的生产链
- 一次性删除现有 `rule/` 历史资产

---

## 3. 目标目录结构

V1 的物理入口统一为：

```text
rule/
├── category/
│   ├── ai/
│   ├── ai-coding/
│   ├── ai-image/
│   ├── ai-video/
│   ├── ai-audio/
│   ├── social/
│   ├── communication/
│   ├── streaming/
│   ├── music/
│   ├── video/
│   ├── gaming/
│   ├── game-platform/
│   ├── developer/
│   ├── cloud/
│   ├── infrastructure/
│   ├── ecommerce/
│   ├── payment/
│   ├── finance/
│   ├── crypto/
│   ├── productivity/
│   ├── collaboration/
│   ├── education/
│   ├── travel/
│   ├── transport/
│   ├── news/
│   ├── media/
│   ├── forum/
│   ├── security/
│   ├── privacy/
│   ├── vpn/
│   ├── domestic/
│   ├── international/
│   ├── advertising/
│   ├── tracking/
│   └── special/
│
├── service/
│   ├── google/
│   ├── microsoft/
│   ├── apple/
│   ├── meta/
│   ├── amazon/
│   ├── tencent/
│   ├── alibaba/
│   ├── bytedance/
│   ├── baidu/
│   ├── huawei/
│   ├── xiaomi/
│   ├── openai/
│   ├── anthropic/
│   ├── deepseek/
│   └── ...
│
└── shared/
    └── ...
```

> `category/` 与 `service/` 是两个平行的顶级实体空间。`shared/` 是第三种 Canonical Entity，用于解决跨服务复用资产；它不改变 Service 的主模型。

### 3.1 Parent Service

大型生态必须作为顶级 Service：

```text
rule/service/google/
├── service.yaml
├── aggregate.yaml
├── gmail/
│   └── service.yaml
├── gemini/
│   └── service.yaml
├── google-drive/
│   └── service.yaml
├── google-docs/
│   └── service.yaml
├── google-sheets/
│   └── service.yaml
├── google-meet/
│   └── service.yaml
├── google-maps/
│   └── service.yaml
├── google-play/
│   └── service.yaml
├── google-photos/
│   └── service.yaml
├── google-calendar/
│   └── service.yaml
├── youtube/
│   └── service.yaml
├── youtube-music/
│   └── service.yaml
├── google-cloud/
│   └── service.yaml
└── firebase/
    └── service.yaml
```

Parent Service 的聚合语义：

```text
Google Aggregate
= Google own assets
+ Child Service aggregate
+ Required dependency closure
- Canonical duplicates
```

具体资产是否属于 Parent、Child 或 Shared Component，必须通过资产审计确定，不能仅凭域名名称推断。

---

## 4. Entity 类型

### 4.1 Category

Category 用于描述服务的业务/功能集合，例如 `ai`、`developer`、`streaming`。

Category 不拥有 Service 的 Canonical Rule Assets，只保存分类定义与聚合声明。

推荐：

```yaml
id: ai
name: Artificial Intelligence
kind: category
status: active
```

Service 的 `categories` 字段是 Category → Service 的事实来源；Category 的成员清单由编译器从 Service Catalog 反向计算，避免双向维护。

### 4.2 Service

最小 Service：

```yaml
id: openai
name: OpenAI
type: service
status: active
categories:
  - ai
  - developer
assets:
  domains: []
  ip_cidrs: []
requires: []
network_references: []
```

### 4.3 Parent Service

```yaml
id: google
name: Google
type: parent-service
status: active
categories:
  - productivity
  - cloud
  - video
children:
  - google/gemini
  - google/gmail
  - google/google-drive
assets:
  domains: []
requires: []
network_references: []
```

Parent Service 不是 Pure Aggregate。它本身可以有自己的 Canonical Assets。

### 4.4 Child Service

```yaml
id: google/gemini
name: Gemini
type: child-service
parent: google
status: active
categories:
  - ai
assets:
  domains: []
requires: []
network_references: []
```

Child Service 必须可以独立生成 Artifact。

### 4.5 Shared Component

Shared Component 用于表示跨 Service 共用且不宜归属于某一个 Service 的基础资产集合。

```yaml
id: google/core
type: shared-component
status: active
assets:
  domains: []
  ip_cidrs: []
```

Service 通过 `requires` 引用 Shared Component：

```yaml
requires:
  - google/core
```

V1 默认只保留 `requires`，不引入 `optional_dependencies`。

### 4.6 Aggregate

Aggregate 是编译语义，不是重复存储规则。

存在两类：

- Service Aggregate：Parent Service → Children
- Category Aggregate：Category → Services

Aggregate 的最终资产由 Compiler 解析得到。

---

## 5. Canonical Asset 模型

V1 第一阶段只定义稳定语义，不强制所有历史规则立即重写。

推荐资产分类：

```yaml
assets:
  domains: []
  domain_suffixes: []
  domain_keywords: []
  ip_cidrs: []
  urls: []
```

原则：

- `domain` 表示明确域名。
- `domain_suffix` 表示后缀匹配范围。
- `domain_keyword` 只在确有必要时使用，避免过度匹配。
- `ip_cidr` 只接受有明确服务归属证据的资产。
- URL 规则必须明确其适配器能力。

禁止把 Provider IP 自动视为产品 Service Asset。例如云厂商基础设施 IP 不因为属于某云厂商就自动成为其某个 SaaS 产品的规则。

---

## 6. Dependency 模型

依赖关系是有向图：

```text
Service A
   ↓ requires
Shared B
   ↓ requires
Shared C
```

编译前必须计算完整 Dependency Closure：

```text
closure(A) = A ∪ requires(B) ∪ requires(C) ...
```

必须检测：

- A → A
- A → B → A
- A → B → C → A

任何 Dependency Cycle 都必须在 Release Gate 前失败。

### 6.1 去重

去重必须发生在 Compiler，而不是依赖客户端。

```text
Service Assets
+ Dependency Closure
+ Aggregate Closure
→ Canonical Set Deduplication
→ IR
```

去重依据是 Canonical Asset Identity，而不是简单字符串比较。后续可扩展标准化：

- domain lowercase
- trailing dot normalization
- CIDR canonicalization
- URL normalization

---

## 7. Aggregate 模型

### 7.1 Parent Aggregate

```text
Parent own assets
        +
Child A aggregate
        +
Child B aggregate
        +
Dependency closure
        ↓
Canonical Set Deduplication
        ↓
Parent Artifact
```

### 7.2 Category Aggregate

```text
Category
  ├── Service A
  ├── Service B
  └── Service C
       ↓
Aggregate Resolution
       ↓
Dedup
       ↓
Category Artifact
```

Category 不直接复制服务规则。

### 7.3 Aggregate Cycle

禁止：

```text
Category A → Service B → Category A
```

以及：

```text
Parent A → Child B → Parent A
```

Compiler 必须在解析阶段报告完整 cycle path。

---

## 8. Network Dataset Reference

Service 可以引用 Network Dataset，但必须显式声明其是否纳入构建产物。

推荐结构：

```yaml
network_references:
  - id: asn/example
    include: false
  - id: geoip/example
    include: true
```

语义：

- `include: true`：该 Dataset 参与最终 Service Artifact 编译。
- `include: false`：仅作为元数据/关联信息，不进入 Service Artifact。

V1 阶段必须保持 `database/` 与 Service Rule 的边界，不把 Network Dataset 目录搬入 `rule/service/`。

---

## 9. V3 Engine 对接契约

V1 不直接调用客户端 Adapter。V3 Engine 负责：

```text
V1 Canonical Model
      ↓
V3 ingest / validation
      ↓
hierarchy / decision
      ↓
Dependency Resolution
      ↓
Aggregate Resolution
      ↓
Canonical Dedup
      ↓
IR
      ↓
7 Adapters
      ↓
generated/
```

### 9.1 V3 必须能够读取

- `rule/category/**`
- `rule/service/**`
- `rule/shared/**`
- V1 Model metadata

### 9.2 V3 不应依赖

- `generated/` 作为 Canonical Source
- 客户端产物反向解析 Service
- Category 的手工成员清单作为权威来源
- 用户策略配置

### 9.3 向后兼容

迁移期允许旧 `rule/<LegacyService>/` 继续存在，但必须标记为 legacy/source-of-record transitional asset。

在 V1 Catalog 完成前：

```text
Legacy Rule
    ↓ mapping
V1 Service ID
    ↓
Canonical Model
```

迁移完成后才允许删除旧入口。

---

## 10. Service ID 规范

Service ID 使用稳定、小写、ASCII、URL-safe 标识：

```text
openai
anthropic
google

google/gemini
google/gmail
google/youtube
```

规则：

1. Parent Service：`vendor`
2. Child Service：`vendor/service`
3. 不使用大小写区分实体。
4. 不使用客户端名称进入 Service ID。
5. 不使用策略名称作为 Service ID。
6. ID 一旦进入正式 Release，不随显示名称变化。

---

## 11. Category 规范

推荐第一阶段建立稳定的一级分类：

```text
ai
ai-coding
ai-image
ai-video
ai-audio
social
communication
streaming
music
video
gaming
game-platform
developer
cloud
infrastructure
ecommerce
payment
finance
crypto
productivity
collaboration
education
travel
transport
news
media
forum
security
privacy
vpn
domestic
international
advertising
tracking
special
```

分类不是不可变事实。新增 Category 必须通过 Catalog Review，避免为了单个服务不断创建新分类。

一个 Service 可以拥有多个 Category。

---

## 12. 开发阶段

### Phase 0 — Contract Freeze

交付：

- V1 Model 文档
- Entity 类型定义
- ID 规范
- Asset 规范
- Dependency 语义
- Aggregate 语义
- Network Reference 语义
- V3 Contract

状态：本阶段随本次开发启动。

### Phase 1 — 目录骨架

创建：

```text
rule/category/
rule/service/
rule/shared/
```

建立 README、Schema、示例实体。

**不迁移旧规则、不删除旧目录。**

### Phase 2 — 全量资产扫描

扫描：

- `rule/`
- `docs/rules/`
- `database/`
- `sources/`
- V3 ingest / canonical / hierarchy 相关代码
- generated 与旧规则映射

生成：

- Legacy Asset Inventory
- Service Candidate Inventory
- Category Candidate Inventory
- Duplicate Inventory
- Orphan Inventory
- Conflict Inventory

### Phase 3 — SERVICE_CATALOG

建立唯一 Service Catalog：

```text
Service ID
Name
Type
Parent
Categories
Legacy Paths
Asset Source
Dependencies
Network References
Status
```

### Phase 4 — Coverage Matrix

建立：

```text
Service × Category × Client × Source × Coverage
```

状态至少包括：

- canonical
- legacy
- partial
- missing
- conflict
- deprecated

### Phase 5 — Canonical Migration

迁移顺序：

```text
无争议服务
→ Parent/Child 生态
→ Shared Components
→ 有重叠服务
→ 有 IP/ASN 风险服务
```

### Phase 6 — Compiler Integration

加入：

1. schema validation
2. ID validation
3. graph validation
4. dependency closure
5. aggregate closure
6. canonical dedup
7. IR emission
8. adapter regression

### Phase 7 — Hot Service Completion

根据 Coverage Matrix 与真实使用频率补全热门服务。

来源优先级：

1. 官方文档 / 官方网络资产
2. 成熟、长期维护的上游规则项目
3. 仓库历史资产
4. 人工验证补充

不得凭空生成域名。

### Phase 8 — Release Migration

验证：

```text
V1 Canonical
   ≈
V3 IR
   ≈
Generated
```

在 golden test、diff test、schema test 全部通过后，逐步将 V1 标记为生产 Source of Truth。

---

## 13. 质量门禁

### Schema Gate

- YAML/JSON 可解析
- Required fields 完整
- ID 合法
- Type 合法
- Parent 存在
- Child 引用合法
- Category 存在

### Graph Gate

- Dependency 无环
- Parent/Child 无环
- Aggregate 无环
- 不允许不存在的 Entity Reference

### Asset Gate

- Canonical normalization
- Duplicate detection
- Invalid CIDR detection
- Domain syntax validation
- 明显错误归属检测

### Build Gate

- 每个 active Service 可编译
- 每个 Parent Aggregate 可编译
- 每个 active Category Aggregate 可编译
- 七客户端 Adapter 均能处理支持的 IR

### Regression Gate

- Legacy → V1 mapping 不丢规则
- V1 → IR 不丢规则
- IR → generated 不丢规则
- Diff 变化必须可解释

---

## 14. 迁移原则

### 禁止直接重命名覆盖

旧目录不能直接删除后重新建同名 V1 目录。

### Canonical First

先建立实体身份，再迁移资产：

```text
Legacy Path
   ↓
Service Identity
   ↓
Canonical Assets
```

### 一条规则一个 Canonical Source

相同资产如果属于多个 Service，只能拥有一个 Canonical Source；其他 Service 通过 `requires` 或 Aggregate 引用。

### 不做语义自动剪枝

例如：不能因为 `google.com` 已存在，就自动认为 `gemini.google.com` 不需要保留。

Dedup 只解决 Canonical Asset 重复，不解决业务语义归属。

---

## 15. Google 等大型生态的标准模板

```text
rule/service/google/
├── service.yaml
├── aggregate.yaml
├── gmail/
├── gemini/
├── google-drive/
├── google-docs/
├── google-sheets/
├── google-slides/
├── google-meet/
├── google-maps/
├── google-play/
├── google-photos/
├── google-calendar/
├── google-cloud/
├── firebase/
├── youtube/
└── youtube-music/
```

Google 顶级 Service 必须能够独立输出整个 Google 生态 Aggregate；子服务也必须能够独立订阅。

同理适用于：

- Microsoft
- Apple
- Meta
- Amazon
- Tencent
- Alibaba
- ByteDance
- Baidu
- Huawei
- Xiaomi

是否建立 Child Service，以真实业务边界和规则资产证据为准，而不是机械拆分所有产品。

---

## 16. 与现有仓库的关系

当前仓库已经以 V3 Engine 作为 Service Rules 的生产构建链，并将 `generated/` 定义为客户端订阅产物；V1 的职责是为这一生产链提供稳定的 Canonical Service Model，而不是替换 V3。fileciteturn19file0

现有规则目录已经存在 AI、Alibaba、Amazon、Apple、Baidu、ByteDance、China、Developer、Finance、Gaming、Google 等生态目录，因此第一阶段必须先做资产盘点，再建立最终 Catalog，不应直接按设计清单批量迁移。fileciteturn22file0

现有客户端输出仍由 `config/formats.yaml` 定义的七类 Adapter 目录承接，V1 不改变这些客户端目录契约。fileciteturn21file0

---

## 17. 第一批实施清单

本次提交只做模型基础设施，不宣称已经完成全部服务迁移：

- [x] V1 模型开发规划
- [x] `rule/category/` 骨架
- [x] `rule/service/` 骨架
- [x] `rule/shared/` 骨架
- [x] Category Schema
- [x] Service Schema
- [x] Shared Component Schema
- [x] V3 Contract 文档
- [x] Google Parent/Child 示例模型
- [ ] 全量 Legacy Asset Inventory
- [ ] SERVICE_CATALOG
- [ ] Service Coverage Matrix
- [ ] 全量 Duplicate / Orphan / Conflict Audit
- [ ] V3 Compiler 实际接入
- [ ] 七客户端 Golden Regression
- [ ] 热门服务规则补全

---

## 18. 完成定义（Definition of Done）

V1 Model 进入生产 Source of Truth 前必须满足：

1. 所有 Active Service 都有唯一 Service ID。
2. 所有 Service 都有明确 Category 归属或明确说明为何不归类。
3. Parent/Child 关系全部可解析。
4. Dependency Graph 无环。
5. Aggregate Graph 无环。
6. 所有引用均指向存在的实体。
7. Canonical Asset 可规范化、可去重。
8. Legacy Asset 迁移覆盖率可量化。
9. V3 Engine 可以直接消费 V1 Model。
10. 七客户端产物可以由 V3 IR 稳定生成。
11. 生成结果具有 deterministic build 特性。
12. Golden / Diff / Schema / Graph Tests 全部通过。
13. 历史规则资产没有未经审计的静默丢失。
14. `generated/` 永远不是 V1 Canonical Source。
15. Service Rule 不携带客户端策略。

---

## 19. 当前执行顺序

```text
现在
 ↓
V1 Contract Freeze
 ↓
目录骨架 + Schema + Example
 ↓
全量 Legacy Asset Scan
 ↓
SERVICE_CATALOG
 ↓
Coverage Matrix
 ↓
Duplicate / Orphan / Conflict Audit
 ↓
Parent / Child / Shared / Aggregate 建模
 ↓
V3 Compiler Integration
 ↓
Hot Service Completion
 ↓
Golden Regression
 ↓
V1 Source of Truth
```

**本阶段的原则是先建模、再盘点、再迁移、最后补全规则。绝不因为目录设计已经确定，就跳过现有资产审计。**
