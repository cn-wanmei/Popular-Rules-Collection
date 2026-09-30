# Icon Identity Boundary V1

## 目标

建立 Popular-Rules-Collection 与 Popular-Rules-Icon 之间唯一、单向的身份边界：

> Collection 定义服务是谁；Icon Registry 只绑定该服务并提供图标资产。

Icon Registry 不再拥有“服务身份解释权”。

## 1. 权威关系

~~~
Popular-Rules-Collection
  └─ canonical published service index
       └─ rule/_index.yaml
            └─ entity == service
                 ├─ service_id
                 ├─ display_name
                 └─ provider
                       │
                       ▼
Popular-Rules-Icon
  └─ registry/services/<service_id>.json
       └─ icon asset binding
~~~

Collection 中的 provider_aggregate、aggregate、domestic_aggregate、category
不能作为普通 service 身份提供给 Icon Registry。

## 2. 严格语义

### 2.1 service_id

service_id 是跨仓库的主键。

Icon Registry：

- 必须使用 Collection 已存在的 canonical service_id
- 不得创建与 Collection 无关的新 service identity
- 不得把两个 Collection service 合并为一个 service identity
- 不得因为图标来源、App Store 结果或视觉相似而修改 service_id

### 2.2 display_name

display_name 的权威来源是 Collection。

Icon Registry 可以镜像它，但不能把：

- App Store 搜索结果
- 第三方品牌名称
- 产品名
- 母公司名
- 客户端名

重新写回成自己的 service identity。

### 2.3 provider

provider 同样由 Collection 决定。

例如：

- bytedance 是 ByteDance
- feishu 是 Feishu
- microsoft 是 Microsoft
- microsoftedge 是 Microsoft Edge

图标是否来自某个产品，不改变这些身份关系。

## 3. 图标身份

图标资产属于：

~~~
service_id → icon asset
~~~

而不是：

~~~
visual brand → 猜测 service_id
~~~

因此以下情况均不得自动视为等价：

- 母品牌图标 → 子服务
- 子产品图标 → 母品牌
- App 图标 → 公司品牌
- App Store 搜索命中 → canonical service
- 相同 Blob → 相同 service

相同图像只能说明资产字节相同，不能证明服务身份相同。

## 4. 迁移阶段

### Phase A — Contract

本文件与 config/icon_identity_authority.yaml 定义规范。

### Phase B — Snapshot + Gate

Icon Repository 保存 Collection canonical service universe 的 pinned snapshot：

- Collection repository
- Collection commit
- source path
- service_count
- service identity records

CI 使用 snapshot 做 deterministic drift check。

### Phase C — Registry normalization

将 registry/services/*.json 的：

- service_id
- name
- provider

统一到 Collection snapshot。

任何不一致都必须修复，而不是在 Icon Registry 添加新的解释层。

### Phase D — Asset identity review

完成 Registry metadata 对齐后，再审查：

- seed 图标是否真正属于 service
- aggregate/product/parent/child 是否错绑
- placeholder 是否仍被算作真实 coverage
- 重复图标是否有合理的 identity justification

### Phase E — Strict CI

最终切换为强门禁：

~~~
canonical Collection service universe
        ==
Icon Registry service identities
~~~

允许 Icon 有额外的历史 seed/orphan 文件作为待清理资产，
但这些文件不得进入 production registry。

## 5. 例外处理

真正需要共用图标时，不改变身份。

正确模型：

~~~
service A ─┐
           ├─ same icon object
service B ─┘
~~~

而不是：

~~~
service A == service B
~~~

例外必须记录：

- service_id
- shared_icon_reason
- reviewer
- reviewed_at
- evidence
- expiry（适用于临时例外）

## 6. 生产原则

Icon 生产链不得通过网络实时查询 Collection 身份。

生产使用：

~~~
Collection canonical commit
        ↓
pinned snapshot
        ↓
Icon Registry
        ↓
seed / object / variants
~~~

身份 snapshot 改变时，必须显式更新 pinned Collection commit，
并重新通过 identity boundary gate。
