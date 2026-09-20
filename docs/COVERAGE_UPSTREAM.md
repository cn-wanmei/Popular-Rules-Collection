# 上游覆盖与日常使用标准

## 核心原则

1. 只物化有可信上游和证据的服务。
2. 不猜测域名。
3. Source Health 与 Service Coverage 分开判断。
4. Aggregate Coverage 不等于 Dedicated Service Source。
5. IP / Provider / CDN 与 Service Domain 分轨。

## Popular-Rules-Source

PRS 是 Supplemental Source Layer，目标是从服务官方来源自动生成可审计 Domain Source。

当前状态：

~~~text
Registry: registered
Enabled: false
Production-qualified: no
~~~

在 PRS 完成 official-evidence-only Release 前，不应把其候选数据作为 Production Coverage。

## Gap 状态

服务状态使用：

COVERED / PARTIAL / MISSING / SOURCE_DRIFT / INTENTIONAL / CONFLICT / REVIEW。

MISSING 必须来自多维审计，而不是单纯的“找不到 URL”。

## Intentional

无稳定独立可信 Source 时，使用 config/intentional_unmaterialized.yaml。

不得为了补 Coverage 猜测域名。

## IP / CDN

Provider、ASN、CDN 不直接映射 Product Service。

详见 docs/IP_ARCHITECTURE.md。

## Current P0 State

当前 P0 Production 仍为 partial。

Phase O 的 cutover / observation 尚未完成。

因此旧 Phase 报告属于审计证据，不等于当前生产 Cutover 已执行。
