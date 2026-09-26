# Icon System V5 — 最终规划方案

> 状态：Architecture Final / Bootstrap Implementation  
> 版本：V5 / Icon Matrix 8  
> 日期：2026-09-26  
> 目标仓库：cn-wanmei/Popular-Rules-Collection

## 1. 设计目标

本次不是 V3/V4 的增量修补，而是一次 **Clean-Slate Icon System 重建**。

最终每一个当前有效的服务图标身份都必须具备：

1. 官方原始图标（Source Original）
2. Glassmorphism
3. Soft 3D / Claymorphism
4. Neo-Skeuomorphism
5. Minimalist Glyph & Multi-color Flat
6. Two-tone / Broken Line
7. MBE Illustration
8. Y2K / Synthwave

因此：

~~~text
1 service_id = 1 icon identity = 1 source snapshot + 7 derived variants
~~~

其中 7 个风格属于同一官方源资产的派生表示，不产生新的品牌身份。

## 2. 本轮审计结论与规划修正

### 2.1 当前数据口径

当前 rule/_index.yaml 的真实统计为：

| Entity | 当前数量 | V5 处理 |
|---|---:|---|
| service | 146 | **Icon Identity 主覆盖集合** |
| provider_aggregate | 112 | 默认复用其 Provider/Service Icon Identity，不复制品牌资产 |
| aggregate | 1 | 语义聚合视图，不自动创建品牌 Logo |
| category | 1 | 语义聚合视图，不自动创建品牌 Logo |
| domestic_aggregate | 1 | 语义聚合视图，不自动创建品牌 Logo |
| **合计** | **261** | 以同一 Run 的 IR 为最终覆盖真相 |

V4 文档中的“262”不再作为任何 V5 统计依据。

当前 config/service_model/services.yaml 为 116 个服务条目；它不是当前已物化 Rule Index 的完整镜像，因此 V5 禁止把它单独作为图标覆盖 SSOT。

### 2.2 SSOT 与投影关系

V5 不把 rule/ 重新定义为新的 canonical source。

正式生产链使用：

~~~text
immutable source → snapshot → canonical → hierarchy → IR → icon acquisition/render → rule/generated projections
~~~

图标系统读取同一 Run 的：

- run_id
- snapshot_id
- ir_digest
- service identity
- display name
- provider
- 已确认的 rule-domain candidates

rule/_index.yaml 只用于人类分发/审计和 bootstrap；生产 Run 应优先读取 data/runs/<run-id>/ir/。

## 3. Icon Identity 模型

### 3.1 唯一键

唯一品牌身份键：

service_id

禁止：

- 通过文件名推断身份
- 通过 provider 名称猜 Logo
- 一个品牌多个随机 icon_id
- aggregate 自己复制 service Logo
- style 生成新的 icon identity

### 3.2 Provider Aggregate

Provider Aggregate 默认是服务视图：

provider aggregate → reuse provider/service icon identity

只有当 aggregate 本身是一个独立品牌身份，并且在 Service Model / Rule IR 中有明确独立 service identity 时，才允许拥有独立 icon。

### 3.3 规则与图标关系

规则文件本身不下载图标。

正确链路：

~~~text
Run → Icon Acquisition → Source Snapshot → 7 Renderers → Icon Registry → client/rule reference
~~~

禁止：

~~~text
rule file → 每个客户端各自请求图标
~~~

这样才能保证可复现、可缓存、可审计，并且真正实现“一次获取、多处复用”。

## 4. Source Acquisition

### 4.1 来源优先级

固定优先级：

1. 已注册、已审核的官方 Icon URL
2. 官方站点 HTML 中明确声明的 icon / apple-touch-icon
3. 官方 Web Manifest 中声明的 icon
4. 官方站点 favicon（仅作为 **official-origin asset**，不得自动声称为官方品牌 Logo）
5. 已审核的第三方品牌资产（V5 runtime 首轮不自动启用，进入 review/hold）
6. semantic fallback（V5 runtime 首轮不自动启用，只作为显式审查方案）

第三方资产永远不能标记为 official。

### 4.2 “不确定官方地址”的处理

不再凭 service_id 猜 URL。

当没有显式官方站点配置时：

1. 从当前 Run 的 service rule 中提取 domain candidates；
2. 用确定性评分选择最可能的一方官方站点；
3. 仅访问该候选站点进行一次 discovery；
4. 从该响应中定位 icon URL；
5. 再对最终 icon asset 做一次实际 asset acquisition；
6. 将最终 source_url + homepage_url + digest + headers + resolution_reason 写入 provenance。

“发现官方站点”和“获取最终图标”是不同步骤，但 **同一个 source_url 在同一个 Run 中只允许一次实际图标获取**。

### 4.3 单次获取不变量

对同一 Run：

~~~text
(service_id, resolved_source_url) → at most one asset fetch
~~~

命中本地/ CAS snapshot 时：

~~~text
network fetch = 0
~~~

重新渲染风格时：network fetch = 0。

renderer 升级时：network fetch = 0。

只有 source digest 变化才重新 acquisition。

### 4.4 网络安全

Acquisition 必须：

- 仅 HTTPS
- 限制重定向次数
- 限制响应体大小
- 白名单允许 MIME
- 拒绝脚本注入 SVG
- 拒绝 foreignObject
- 拒绝外部远程 SVG/image 引用
- 记录最终 URL
- 记录 HTTP 状态 / Content-Type / 长度 / SHA-256
- source cache 采用持久化 digest 校验和 source URL 映射；正式发布时可进一步接入 Engine CAS，不得把缓存文件名本身当作身份
- 严禁无限爬站

## 5. Rights / Provenance

“官方来源”与“可自由再分发”不是同一个事实。

因此 Registry 必须分离：

- source_origin
- source_url
- provenance
- rights_basis
- redistribution_status
- attribution_required

默认不把“来自官方网站”自动写成任何 CC / MIT / Apache 等许可证。

没有明确授权信息的品牌资源可以记录为 redistribution_status: review；不得伪造许可证。

已有第三方资源必须保留来源、许可证证据和审核状态。

## 6. 八层资产模型

### Layer 0 — Source Original

目标：尽可能保留真实官方源资产。

要求：

- 原始字节可校验
- SHA-256
- source URL
- homepage URL
- content type
- fetched timestamp
- source snapshot / run lineage
- rights metadata

### Layer 1 — Glassmorphism

视觉算法：

- 半透明材质
- backdrop-like glow
- 柔和高光
- frosted surface
- 品牌色作为玻璃内部光源
- 保留 Logo 主体辨识度

### Layer 2 — Soft 3D / Claymorphism

视觉算法：

- 明确的厚度方向
- soft extrusion
- clay-like bevel
- 环境阴影
- 边缘高光
- 不允许只改变背景颜色

### Layer 3 — Neo-Skeuomorphism

视觉算法：

- bevel / inset
- material surface
- controlled gradient
- directional highlight
- tactile control surface

### Layer 4 — Minimalist Glyph & Multi-color Flat

视觉算法：

- 大面积留白
- reduced geometry
- flat multi-color planes
- optical centering
- 不依赖厚重容器

### Layer 5 — Two-tone / Broken Line

视觉算法：

- two-tone palette
- line/filled hybrid
- broken contour
- negative-space emphasis
- 小尺寸优先

### Layer 6 — MBE Illustration

视觉算法：

- playful rounded geometry
- bold outline
- simplified illustration
- accent objects
- sticker-like visual rhythm

### Layer 7 — Y2K / Synthwave

视觉算法：

- cyber gradient
- chromatic edge
- glow
- scanline / grid texture
- sparkle / chrome cues

### 强制要求

7 个 renderer 必须是 **7 个独立算法模块**，对应 `scripts/icon_v5_renderers/` 下的独立实现文件。

允许共享：

- mask
- bbox
- palette extraction
- shadow primitives
- SVG safety sanitizer
- composition helpers

禁止：

render(base, style) + 7 个不同 CSS wrapper。

这正是 V3 “模板套 Logo”问题的主要来源。

## 7. 统一尺寸与输出

主画布：

512 × 512 SVG

输出至少覆盖：

- SVG master
- 256 PNG
- 128 PNG
- 64 PNG

V5 build 已将 SVG 通过 CairoSVG 栅格化为 64/128/256；QA 仍需检查 24/32/48/64/128/256。

QA 还必须检查：

- 24
- 32
- 48
- 64
- 128
- 256

所有小尺寸都使用同一 identity，不允许手工重绘成另一个 Logo。

## 8. Active Library Layout

~~~text
assets/icons/
├── v5/
│   ├── README.md
│   ├── release-pointer.json
│   ├── registry.json
│   ├── source/
│   │   ├── original/
│   │   └── fallback/
│   ├── normalized/
│   ├── styles/
│   │   ├── source-original/
│   │   ├── glassmorphism/
│   │   ├── soft-3d/
│   │   ├── neo-skeuomorphism/
│   │   ├── minimalist/
│   │   ├── duotone-line/
│   │   ├── mbe/
│   │   └── y2k/
│   ├── png/
│   │   ├── 64/
│   │   ├── 128/
│   │   └── 256/
│   ├── metadata/
│   ├── previews/
│   └── releases/
├── v4/        # historical compatibility only
├── v3/        # historical compatibility only
└── legacy/    # historical compatibility only
~~~

V3/V4/Legacy 不再成为 active SSOT。

V5 bootstrap 阶段允许从 `rule/_index.yaml` 发现服务；正式 production acquisition 优先通过 `--run-dir` 读取同一 Engine Run 的 `ir/ir.json` 与 `ir/manifest.json`，并从 run manifest 绑定 `run_id/snapshot_id`。

历史版本仍保留 Git 历史与 immutable release evidence，以支持 rollback 和审计。

## 9. Registry 契约

每个 service：

~~~yaml
service_id: qqmail
icon_identity: service:qqmail
source:
  origin: official
  homepage_url: https://mail.qq.com/
  source_url: <resolved>
  content_type: image/svg+xml
  digest: <sha256>
  rights_basis: official_site_asset
  redistribution_status: review
variants:
  source_original: ...
  glassmorphism: ...
  soft_3d: ...
  neo_skeuomorphism: ...
  minimalist: ...
  duotone_line: ...
  mbe: ...
  y2k: ...
lineage:
  run_id: ...
  snapshot_id: ...
  ir_digest: ...
  source_digest: ...
  renderer_version: ...
~~~

## 10. Coverage 契约

正式 active service icon coverage：

active_service_id ∩ current_run_service_id

必须：

missing = 0

并且每一个 service 必须：

8 / 8 variants

必须执行双向校验：

service → icon

以及：

icon → active service

因此不会出现：

- 新服务没有图标
- 删除服务后遗留无主图标
- 同一服务多个图标
- 图标有文件但 registry 没身份
- registry 有身份但文件缺失

## 11. 新服务自动维护

未来新增：

Service Rule / Independent Child Service

必须触发：

service diff → icon coverage check → source resolution → acquisition → 7 renderers → QA → release

缺少任何一个 variant：

Icon Release = FAIL

服务删除：

service diff → orphan detection

历史资产不立即销毁，进入历史 release；active library 移除引用。

## 12. 与 Rule / Generated 的依赖边界

必须保持：

~~~text
Canonical / IR
   ├── Rule Tree
   ├── Generated Clients
   └── Icon System
~~~

禁止：

~~~text
Rule → Icon → Rule
Generated → Icon → Rule
Icon → Generated
Generated → Rule
~~~

客户端偏好只影响 preferred_style，不改变 identity。

不得把图标二进制嵌入 sing-box / Surge / Mihomo 等规则 JSON。

## 13. QA Gate

### Source Gate

- HTTP success
- content type valid
- size limit
- digest valid
- SVG safety
- source URL recorded
- rights metadata recorded

### Identity Gate

- service_id 唯一
- identity stable
- source digest recorded
- no duplicate identity
- no provider aggregate accidental duplication

### Style Gate

每种 style：

- file exists
- valid SVG
- digest matches
- 视觉算法版本一致
- 不得与其它 style 仅仅改变颜色

### Legibility Gate

必须检查：

24 / 32 / 48 / 64 / 128 / 256

### Coverage Gate

必须：

8/8 × all active services

### Lineage Gate

必须存在：

run_id + snapshot_id + ir_digest + source_digest + renderer_version

全部 fail-closed。

## 14. Release 状态机

~~~text
DISCOVERED
   ↓
SOURCE_RESOLVED
   ↓
SOURCE_ACQUIRED
   ↓
NORMALIZED
   ↓
RENDERED
   ↓
QA_PASSED
   ↓
COVERAGE_PASSED
   ↓
LINEAGE_BOUND
   ↓
RC_READY
   ↓
IMMUTABLE_RELEASE
~~~

任何失败不得 fail-open。

## 15. 增量更新策略

### 仅规则内容变化

source digest 不变：

no icon refetch

### 官方图标变化

source digest 变化：

refetch → regenerate 7 styles

### Renderer 版本变化

cached source → rerender

不访问网络。

### 单一风格 renderer 变化

仅：

that style → rerender

其它 6 层不动。

## 16. Client Style Policy

默认通过 profile 配置，不把“某客户端一定应该使用某风格”写死在 renderer 中。

建议提供：

~~~yaml
preferred_style:
  mihomo: minimalist
  singbox: minimalist
  surge: glassmorphism
  shadowrocket: minimalist
  quantumultx: duotone_line
  egern: glassmorphism
  loon: soft_3d
~~~

此表属于可配置的呈现策略，不改变 icon identity。

## 17. CI / Writer

### Pull Request Gate

检查：

- schema
- contract
- service/icon coverage
- renderer tests
- provenance
- no legacy active reference

### Acquisition Writer

只允许：

branch → generated assets → PR

禁止：

workflow → direct main mutation

与仓库既有 icon_writer: branch_pr_only 规则保持一致。

### Release

只有经过：

CI → Gate → Review → immutable release

才能推进 active pointer。

## 18. 分阶段实施

### Phase 0 — Audit

已完成。

### Phase 1 — V5 Foundation

本变更执行：

- V5 policy
- schema
- renderer framework
- source resolver
- one-fetch cache contract
- registry contract
- gate
- tests
- CI skeleton
- 文档切换

### Phase 2 — Official Source Acquisition

执行：

- 显式 official URL
- official HTML icon discovery
- manifest/icon discovery
- rule-domain candidate resolution
- source snapshot

### Phase 3 — 8-style Rendering

执行全部七个独立 renderer。

### Phase 4 — Full Service Coverage

目标：

当前 Run 全部 active service = 8/8

当前 bootstrap 基准为 Rule Index 中 146 个 service；后续以同一 Run IR 动态计算，不锁死 146。

### Phase 5 — Active Cutover

执行：

- V5 release pointer
- V4 active pointer removal
- V3/V4/legacy → historical compatibility
- docs / resolver / client profiles 全部切换

### Phase 6 — Continuous Maintenance

任何新增 service 都自动触发 icon coverage/build gate。

### Phase 7 — Immutable Release

完成：

- release manifest
- registry digest
- source digest
- renderer digest
- lineage evidence
- rollback pointer

## 19. 禁止事项

1. 不继续修补 V3/V4 renderer 作为 V5。
2. 不把 Simple Icons 直接冒充官方 Logo。
3. 不把 favicon 自动标成官方品牌 Logo。
4. 不把“官方网站来源”自动等同于开放许可证。
5. 不把 aggregate 自动复制成新品牌身份。
6. 不允许规则文件自行联网。
7. 不允许同一 Run 重复拉取同一个 source URL。
8. 不允许生成器依赖 rule/ 作为 canonical input。
9. 不允许图标反向改变 Rule / IR。
10. 不允许 missing variant 进入 active release。
11. 不允许通过空白/占位图标伪造 coverage。
12. 不允许直接写 main。

## 20. 完成定义

V5 只有在以下条件同时成立后才算“完成”：

- 全部 active services 有 icon identity
- 每个 identity 都有 source provenance
- 每个 identity 都有 8/8 variants
- 所有 source 都可追溯
- 所有 renderer 都有独立算法
- 所有小尺寸 QA 通过
- service ↔ icon 双向 coverage 为 100%
- 与同一 Run / Snapshot / IR lineage 绑定
- CI fail-closed
- V5 immutable release 建立
- V3/V4 从 active path 完成退出

在完成第一次完整 acquisition 前，V5 处于 **Bootstrap / Candidate**，不得宣称“100% 已完成”。

## 21. 本次实现范围

本次提交先把 **V5 的架构、契约、自动化和 CI 边界一次建立正确**；随后由受控 branch writer 在 Engine Run 上执行完整官方 source acquisition 与当前 service universe 的首轮构建。V5 不把 bootstrap Rule Index 当作正式生产输入。

受限于当前执行环境无法直接访问互联网源站，不能在本次离线提交中伪造“已抓取全部官方图标”；因此所有未 acquisition 的服务必须真实进入 review/hold，不得用假图标把 coverage 填满。
