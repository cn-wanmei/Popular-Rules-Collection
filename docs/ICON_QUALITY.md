# Icon Quality（产品质量阶段）

> 不改 Rule / Primary / Builder。图标进入 **Quality / Delivery**。

## 来源优先级

```text
P0  project-brand / official-colors（识别用品牌色）
P1  高质量彩色第三方
P2  Simple Icons → third_party + monochrome
P3  placeholder
```

不强制一切彩色：Apple / GitHub / xAI / Copilot 可为 `monochrome`。

## Manifest

```yaml
source:
  provider: project-brand | simple-icons | project
  provenance: official-colors | third_party | project
  verified: true|false
visual:
  style: brand | geometric
  color_mode: color | monochrome
  background: transparent
```

## CN / AI 高频彩色

- 国内：wechat, baidu, bilibili, alibaba, alipay, zhihu, douyin, huawei, xiaomi, meituan, tencent
- AI：openai, anthropic, claude, gemini, deepseek, perplexity, huggingface
- 故意 mono：copilot, xai, apple, github

## 视觉回归

```bash
python scripts/icon_visual_regression.py --write-baseline
python scripts/icon_visual_regression.py
```

- `color_ratio`：多色丰富度（Google 四色高，微信单绿低但合法）
- `dark_ratio`：近黑占比；official-colors + color 且 dark≥0.85 → WARN
- baseline 骤降 → visual regression WARN

## 命令

```bash
python scripts/sync_service_icons.py    # 不覆盖 official-colors
python scripts/build_icons.py --force # 需 cairosvg
python scripts/icon_validate.py
python scripts/icon_visual_regression.py
```
