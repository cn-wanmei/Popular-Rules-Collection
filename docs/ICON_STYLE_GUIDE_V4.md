# PRC Icon Library V4 — Visual Rebuild

> Release：`2026.09.25-prc-icon-matrix-3`

这次不是继续给旧 V4「换线宽」，而是重做 fallback 图形构建规则。旧方案虽然做到 262 / 262 覆盖，但九种 fallback 的共性过强，容易退化成「一个框 + 三条线」，视觉辨识度不足；因此本次重点恢复 V3 所具备的结构差异，同时保留真实品牌资产的身份优先级。

## 1. 最终 10 层

| 层 | 风格 | 构建方向 | 视觉骨架 |
|---|---|---|---|
| Official | Brand Native | 保留已验证品牌身份 | 原生 Logo / V3 品牌资产 |
| 1 | Lucide | refined-outline | 浏览器容器 + 条目 + 路由焦点 |
| 2 | Tabler | precision-stack | 多层条目卡 + 离散节点 |
| 3 | Phosphor | bold-geometric | 几何外轮廓 + 实心焦点 |
| 4 | Material Symbols | rounded-filled | 大色块容器 + 信息槽 + 节点 |
| 5 | Fluent | layered-soft | 前后叠层 + 柔和容器 |
| 6 | Heroicons | secure-outline | Shield 边界 + 中心网络 |
| 7 | Remix | stacked-linefill | line/fill 层叠 + 偏心焦点 |
| 8 | Hugeicons | bulk-rounded | 厚重圆角容器 + bulk 层级 |
| 9 | Solar | radial-orbit | 中心焦点 + 轨道 + 八向节奏 |

本次从 active matrix 中移除 Bootstrap，加入 Hugeicons。Hugeicons 官方免费集合强调 6,000+ 图标以及 Stroke Rounded 等免费风格，适合作为原矩阵中缺少的厚重、圆润、高表现力视觉层参考。citeturn670966search2

Lucide、Tabler、Phosphor、Material Symbols、Fluent、Heroicons、Remix 都具有成熟的开放图标生态，并且分别覆盖 outline、multi-weight、filled、layered 等不同视觉语法，因此这里把它们当作设计语言参考，而不是直接复制第三方 SVG。citeturn670966search7turn850309search0turn850309search10turn670966search0turn850309search1turn670966search4turn850309search5

## 2. V4 新构建规则

### 2.1 三层信息结构

每种 fallback 必须具备自己的「主轮廓、服务结构、焦点节点」三层信息：

```text
主轮廓
  ↓
服务结构
  ↓
焦点 / 路由节点
```

不能把所有风格压缩成同一模板再只更换线宽、圆角或透明度。

### 2.2 统一规格，不统一造型

- 画布固定 64 × 64
- 安全边距约 8px
- 主视觉重心保持居中
- 默认线宽 2.25–3.4px
- 禁止文字、复杂纹理和外部资源
- 允许 outline / filled / layered / linefill / radial 等不同结构

统一的是产品规格；差异来自轮廓、填充比例、内部结构、焦点位置和线面关系。

### 2.3 品牌身份永远优先

真实、可信的品牌资产继续走 Official 层，优先复用 V3 已验证品牌图标。fallback 只用于没有可信品牌身份的条目；不得把 semantic fallback 重绘成看似官方的品牌 Logo。

### 2.4 小尺寸优先

最终检查顺序：48px → 32px → 24px → 20px → 16px。

16–20px 下必须保留外部主轮廓、一个内部结构和一个焦点节点；只有放大后才成立的装饰应删除。

## 3. 覆盖校验

本次 rebuild 前后均按 `rule/_index.yaml` 与 `assets/icons/v4/service-index.json` 做路径级交叉校验。当前结果：

| 检查项 | 结果 |
|---|---:|
| Rule Index | 262 |
| Icon Index | 262 |
| 唯一 Icon Path | 262 |
| 缺失 Icon Path | 0 |
| 多余 Icon Path | 0 |
| 重复 Icon Path | 0 |
| 当前覆盖 | 100% |

因此本次没有凭空新增“缺失图标”：现有规则已经全部有图标路径；真正需要修复的是 fallback 的视觉质量。品牌身份仍保持 Official / V3 优先，其余条目继续使用九种 semantic fallback。

## 4. SSOT

```text
assets/icons/v4/release-pointer.json
        ↓
assets/icons/v4/manifest.json
assets/icons/v4/service-index.json
        ↓
assets/icons/v4/styles/<style>/service.svg
```

任何服务的最终图标地址以 `service-index.json` 为准。

## 5. 资产与授权

九种 active fallback 均为本仓库自有 CC0 semantic glyph。参考库仅提供视觉语言参考，不把第三方原始 SVG 当作本仓库品牌资产。Material Symbols、Tabler、Phosphor、Fluent、Heroicons 等均有公开许可说明；Remix 使用 Remix Icon License v1.0；Hugeicons 免费核心图标集为 MIT。citeturn670966search0turn850309search0turn850309search10turn850309search1turn670966search4turn850309search5turn670966search2

Solar 在这里也只作为视觉语言参考层，本仓库提交的实际文件仍是自有 semantic glyph。

## 6. 参考源

- Lucide：https://lucide.dev/icons/
- Tabler：https://tabler.io/icons
- Phosphor：https://phosphoricons.com/
- Material Symbols：https://fonts.google.com/icons
- Fluent UI：https://github.com/microsoft/fluentui-system-icons
- Heroicons：https://heroicons.com/
- Remix：https://remixicon.com/
- Hugeicons：https://hugeicons.com/icons
- Solar：https://solar-icons.com/
