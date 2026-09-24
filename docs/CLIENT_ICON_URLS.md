# 客户端 Icon URL — Current V4

当前服务图标不是通过旧的 assets/icons/png/{size} 模板猜路径，而是通过 V4 Service Index 精确解析。

## 解析链

assets/icons/v4/release-pointer.json
      ↓
assets/icons/v4/service-index.json
      ↓
primary = official | one of nine styles
      ↓
icon.raw

## V4 Fallback Raw

https://raw.githubusercontent.com/cn-wanmei/Popular-Rules-Collection/main/assets/icons/v4/styles/<style>/service.svg

真实品牌图标继续从 Current V3 client index 的已发布资产解析。
