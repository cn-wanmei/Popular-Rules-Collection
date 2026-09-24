# Icon Architecture — Current V4

## Current pipeline

Service ID / semantic role
      ↓
V4 Service Index
      ├── Official / Brand Native
      └── 9 Style Semantic Fallbacks
      ↓
Service docs / UI

## 关键不变量

- 每条 Rule Index 记录都有图标解析结果。
- 真实品牌身份优先，不重绘成假品牌 Logo。
- fallback 必须显式标记为 semantic。
- 图标资产与规则文件解耦。
- 当前 V4 Pointer 是用户侧图标 SSOT。

覆盖：262 / 262。
