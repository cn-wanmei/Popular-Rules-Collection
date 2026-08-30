# Policy / Strategy Icons

高频策略组几何图标（实心、全彩、统一语言）。

| ID | 含义 | 色 |
|----|------|----|
| direct | 直连 | 绿 |
| proxy | 代理 | 蓝 |
| reject | 拒绝 | 红 |
| select | 手动选择 | 琥珀 |
| auto | 自动选择 | 紫 |
| urltest | 测速 / 自动 | 紫 |
| fallback | 故障转移 | 紫 |
| loadbalance | 负载均衡 | 靛 |
| match | 命中 | 青 |
| final | 最终规则 | 灰 |
| dns | DNS | 青 |
| adblock | 广告拦截 | 橙 |
| global | 全局 | 蓝 |

```bash
python scripts/icon_policy_set.py
python scripts/build_icons.py --force
```

品牌：Apple / GitHub / X 等**官方黑**保持黑色；其余按品牌色全彩。
